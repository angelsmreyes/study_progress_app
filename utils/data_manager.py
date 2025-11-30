import os
from datetime import datetime
from typing import List, Dict, Optional
import streamlit as st
from supabase import create_client, Client

"""
Módulo para manejo de datos de sesiones de estudio.
Maneja guardado/carga de datos desde Supabase.
"""

# Inicializar cliente de Supabase
@st.cache_resource
def init_supabase() -> Client:
    try:
        # Intentar obtener credenciales de st.secrets
        # Soporta tanto formato [supabase] como variables directas
        if "supabase" in st.secrets:
            url = st.secrets["supabase"]["DB_URL"]
            key = st.secrets["supabase"]["DB_TOKEN"]
        else:
            url = st.secrets["DB_URL"]
            key = st.secrets["DB_TOKEN"]
            
        return create_client(url, key)
    except Exception as e:
        st.error(f"Error al conectar con Supabase: {e}")
        st.warning("Asegúrate de configurar .streamlit/secrets.toml correctamente.")
        return None

def load_sessions() -> List[Dict]:
    """
    Cargar todas las sesiones desde Supabase.
    
    Returns:
        List[Dict]: Lista de sesiones, o lista vacía si no hay datos
    """
    try:
        supabase = init_supabase()
        if not supabase:
            return []
            
        response = supabase.table("study_sessions").select("*").order("date", desc=False).execute()
        return response.data
    except Exception as e:
        print(f"Error al cargar sesiones: {e}")
        return []


def recalculate_days() -> bool:
    """
    Recalcular los números de día basados en la fecha.
    Ordena por fecha y asigna día 1, 2, 3...
    
    Returns:
        bool: True si se actualizó correctamente
    """
    try:
        supabase = init_supabase()
        if not supabase:
            return False
            
        # Obtener todas las sesiones ordenadas por fecha
        # Usamos created_at como tie-breaker para fechas iguales
        response = supabase.table("study_sessions").select("id, day, date, created_at").order("date", desc=False).order("created_at", desc=False).execute()
        sessions = response.data
        
        if not sessions:
            return True
            
        updates = []
        for idx, session in enumerate(sessions, 1):
            # Si el día no coincide con el índice, necesita actualización
            if session.get('day') != idx:
                updates.append({
                    "id": session['id'],
                    "day": idx,
                    # Necesitamos incluir otros campos requeridos si upsert falla sin ellos,
                    # pero upsert parcial debería funcionar si el ID existe.
                    # Para seguridad, solo actualizamos el campo day.
                    # Supabase-py upsert suele requerir todos los campos NOT NULL si es un insert,
                    # pero para update parcial es mejor usar .update() o upsert con ignore_duplicates=False?
                    # La forma más limpia para updates masivos parciales es upsert con los datos cambiados.
                })
        
        if updates:
            print(f"🔄 Recalculando días para {len(updates)} sesiones...")
            # Upsert en batch
            # Nota: upsert requiere que pasemos los datos. Si pasamos solo ID y day, 
            # y hay otras columnas not null sin default, podría fallar si lo trata como insert.
            # Pero como los IDs existen, debería ser un update.
            # Sin embargo, para evitar problemas con columnas not null faltantes,
            # lo mejor es hacer updates individuales o un upsert con cuidado.
            # Probemos upsert batch solo con id y day.
            
            # Estrategia segura: Updates individuales (más lento pero seguro) o upsert si estamos seguros.
            # Dado que upsert podría borrar datos si no pasamos todo el objeto,
            # vamos a iterar y hacer updates. Para 100 días no es tan grave.
            # O mejor aún, upsert con todos los datos es pesado.
            
            # Optimización: Usar upsert solo con id y day funciona si la tabla permite nulls o tiene defaults,
            # PERO si es un update, Postgres no valida nulls de otras columnas.
            
            for update in updates:
                supabase.table("study_sessions").update({"day": update['day']}).eq("id", update['id']).execute()
                
        return True
    except Exception as e:
        print(f"Error al recalcular días: {e}")
        return False


def save_session(session_data: Dict) -> bool:
    """
    Guardar una sesión en Supabase (insertar o actualizar).
    
    Args:
        session_data: Datos de la sesión a guardar
        
    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    try:
        supabase = init_supabase()
        if not supabase:
            return False
            
        # Upsert maneja tanto insert como update si el ID existe
        response = supabase.table("study_sessions").upsert(session_data).execute()
        
        # Recalcular días para asegurar orden cronológico
        # Esto es importante si se cambió la fecha
        recalculate_days()
        
        # Verificar si hubo respuesta exitosa (data no vacía)
        return bool(response.data)
    except Exception as e:
        print(f"Error al guardar sesión: {e}")
        return False


def add_session(session_data: Dict) -> bool:
    """
    Agregar una nueva sesión.
    
    Args:
        session_data: Datos de la sesión a agregar
        
    Returns:
        bool: True si se agregó correctamente
    """
    # Calcular número de día
    sessions = load_sessions()
    session_data['day'] = len(sessions) + 1
    
    # Generar ID único si no existe
    if 'id' not in session_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_data['id'] = f"session_{timestamp}"
    
    if 'created_at' not in session_data:
        session_data['created_at'] = datetime.now().isoformat()
    
    return save_session(session_data)


def delete_session(session_id: str) -> bool:
    """
    Eliminar una sesión por ID.
    
    Args:
        session_id: ID de la sesión a eliminar
        
    Returns:
        bool: True si se eliminó correctamente
    """
    try:
        supabase = init_supabase()
        if not supabase:
            return False
            
        supabase.table("study_sessions").delete().eq("id", session_id).execute()
        
        # Recalcular números de día
        recalculate_days()
        
        return True
    except Exception as e:
        print(f"Error al eliminar sesión: {e}")
        return False


def get_session_by_id(session_id: str) -> Optional[Dict]:
    """
    Obtener una sesión específica por ID.
    
    Args:
        session_id: ID de la sesión
        
    Returns:
        Optional[Dict]: Sesión encontrada o None
    """
    try:
        supabase = init_supabase()
        if not supabase:
            return None
            
        response = supabase.table("study_sessions").select("*").eq("id", session_id).execute()
        
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error al obtener sesión: {e}")
        return None


def get_sessions_count() -> int:
    """
    Obtener el total de sesiones registradas.
    
    Returns:
        int: Número total de sesiones
    """
    try:
        supabase = init_supabase()
        if not supabase:
            return 0
        
        # Usar count exacto es más eficiente
        response = supabase.table("study_sessions").select("*", count="exact").execute()
        return response.count if response.count is not None else len(response.data)
    except:
        return len(load_sessions())


def get_current_streak() -> int:
    """
    Calcular la racha actual de días consecutivos estudiando.
    
    Returns:
        int: Número de días consecutivos
    """
    sessions = load_sessions()
    
    if not sessions:
        return 0
    
    # Ordenar por fecha descendente
    sessions_sorted = sorted(sessions, key=lambda x: x.get('date', ''), reverse=True)
    
    # Verificar si el último día estudiado es hoy
    # Si la última sesión no es de hoy, no hay racha
    # MODIFICACIÓN: Permitir que la última sesión sea de ayer para manejar diferencias de zona horaria
    # (ej. usuario en UTC-4 estudia "hoy", servidor en UTC ya es "mañana")
    from datetime import date
    last_session_date = datetime.fromisoformat(sessions_sorted[0]['date']).date()
    today_date = date.today()
    
    if (today_date - last_session_date).days > 1:
        return 0
    
    # Contar días consecutivos
    streak = 1
    for i in range(len(sessions_sorted) - 1):
        current_date = datetime.fromisoformat(sessions_sorted[i]['date']).date()
        next_date = datetime.fromisoformat(sessions_sorted[i + 1]['date']).date()
        
        if (current_date - next_date).days == 1:
            streak += 1
        else:
            break
    
    return streak


def get_days_since_last_study() -> int:
    """
    Obtener los días transcurridos desde la última sesión de estudio.
    
    Returns:
        int: Número de días desde última sesión
    """
    sessions = load_sessions()
    
    if not sessions:
        # Si nunca ha estudiado, retornar un número alto
        return 999
    
    # Ordenar por fecha descendente
    sessions_sorted = sorted(sessions, key=lambda x: x.get('date', ''), reverse=True)
    last_study_date = sessions_sorted[0].get('date')
    
    from datetime import date, datetime, timedelta
    today = date.today()
    last_date = datetime.fromisoformat(last_study_date).date()
    
    diff = (today - last_date).days
    
    # Si hay 1 día de diferencia, verificar si fue una sesión reciente (timezone issue)
    if diff == 1:
        try:
            # Intentar obtener created_at para verificar si fue hace poco
            created_at_str = sessions_sorted[0].get('created_at')
            if created_at_str:
                created_at = datetime.fromisoformat(created_at_str)
                # Si created_at no tiene timezone, asumir que es compatible con datetime.now()
                # (ambos UTC o ambos local server time)
                now = datetime.now()
                
                # Si la sesión fue creada hace menos de 12 horas, contarla como "hoy"
                if (now - created_at).total_seconds() < 12 * 3600:
                    return 0
        except Exception as e:
            print(f"Error verificando created_at: {e}")
            pass
            
    return diff


def get_total_hours_studied() -> str:
    """
    Calcular el total de horas de estudio (aproximado).
    
    Returns:
        str: Total de horas formateado
    """
    sessions = load_sessions()
    total_minutes = 0
    
    for session in sessions:
        duration = session.get('duration', '0 minutos')
        
        # Extraer números de la duración
        try:
            # Buscar patrones como "2 horas", "45 minutos", etc.
            if 'hora' in duration.lower() or 'hour' in duration.lower():
                import re
                numbers = re.findall(r'\d+', duration)
                if numbers:
                    total_minutes += int(numbers[0]) * 60
            elif 'minuto' in duration.lower() or 'minute' in duration.lower():
                import re
                numbers = re.findall(r'\d+', duration)
                if numbers:
                    total_minutes += int(numbers[0])
        except:
            pass
    
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    if hours > 0 and minutes > 0:
        return f"{hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h"
    else:
        return f"{minutes}m"


