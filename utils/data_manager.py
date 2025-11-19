import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

"""
Módulo para manejo de datos de sesiones de estudio.
Maneja guardado/carga de datos desde base de datos SQLite.
"""


# Ruta absoluta del archivo de base de datos (independiente del cwd)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.abspath(os.path.join(BASE_DIR, "..", "study_sessions.db"))


def get_db_connection():
    """
    Crear conexión a la base de datos SQLite.
    Crea la base de datos y la tabla si no existen.
    
    Returns:
        sqlite3.Connection: Conexión a la base de datos
    """
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
    
    # Crear tabla si no existe
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            day INTEGER,
            date TEXT NOT NULL,
            category TEXT,
            topic TEXT,
            duration TEXT,
            daily_win TEXT,
            key_learnings TEXT,
            resources TEXT,
            difficulty TEXT,
            focus_level TEXT,
            obstacles TEXT,
            next_steps TEXT,
            practical_application TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    return conn


def load_sessions() -> List[Dict]:
    """
    Cargar todas las sesiones desde la base de datos SQLite.
    
    Returns:
        List[Dict]: Lista de sesiones, o lista vacía si no hay datos
    """
    try:
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM sessions ORDER BY date ASC")
        
        sessions = []
        for row in cursor:
            session_dict = {
                'id': row['id'],
                'day': row['day'],
                'date': row['date'],
                'category': row['category'],
                'topic': row['topic'],
                'duration': row['duration'],
                'daily_win': row['daily_win'],
                'key_learnings': row['key_learnings'],
                'resources': row['resources'],
                'difficulty': row['difficulty'],
                'focus_level': row['focus_level'],
                'obstacles': row['obstacles'],
                'next_steps': row['next_steps'],
                'practical_application': row['practical_application'],
                'created_at': row['created_at']
            }
            sessions.append(session_dict)
        
        conn.close()
        return sessions
    except Exception as e:
        print(f"Error al cargar sesiones: {e}")
        return []


def save_session(session_data: Dict) -> bool:
    """
    Guardar una sesión en la base de datos SQLite.
    
    Args:
        session_data: Datos de la sesión a guardar
        
    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    try:
        conn = get_db_connection()
        
        conn.execute("""
            INSERT INTO sessions (
                id, day, date, category, topic, duration, daily_win,
                key_learnings, resources, difficulty, focus_level,
                obstacles, next_steps, practical_application, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_data.get('id'),
            session_data.get('day'),
            session_data.get('date'),
            session_data.get('category'),
            session_data.get('topic'),
            session_data.get('duration'),
            session_data.get('daily_win'),
            session_data.get('key_learnings'),
            session_data.get('resources'),
            session_data.get('difficulty'),
            session_data.get('focus_level'),
            session_data.get('obstacles'),
            session_data.get('next_steps'),
            session_data.get('practical_application'),
            session_data.get('created_at')
        ))
        
        conn.commit()
        conn.close()
        return True
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
    
    # Generar ID único
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_data['id'] = f"session_{timestamp}"
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
        conn = get_db_connection()
        conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        conn.commit()
        conn.close()
        
        # Recalcular números de día
        sessions = load_sessions()
        for idx, session in enumerate(sessions, 1):
            conn = get_db_connection()
            conn.execute("UPDATE sessions SET day = ? WHERE id = ?", (idx, session['id']))
            conn.commit()
            conn.close()
        
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
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
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
    from datetime import date
    today = date.today().isoformat()
    
    # Si la última sesión no es de hoy, no hay racha
    if sessions_sorted[0].get('date') != today:
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
    
    from datetime import date
    today = date.today()
    last_date = datetime.fromisoformat(last_study_date).date()
    
    return (today - last_date).days


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

