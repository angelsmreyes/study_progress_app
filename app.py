"""
Study Tracker 100 Days - Streamlit App
Aplicación para tracking de sesiones de estudio durante 100 días
"""

import streamlit as st
from datetime import datetime
from utils import data_manager, content_generator, visualizations
import json

# Configuración de la página
st.set_page_config(
    page_title="Study Tracker 100 Days",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialización de session_state
if 'show_form' not in st.session_state:
    st.session_state.show_form = False


def main():
    """Función principal de la aplicación."""
    
    # Header principal
    st.markdown("""
    <div style='background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: white; text-align: center; margin: 0;'>📚 Study Tracker 100 Days</h1>
        <p style='color: white; text-align: center; margin: 0.5rem 0 0 0; opacity: 0.9;'>
            Mejorando como Data Analyst | Physics Review | Preparación para Maestría
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cargar datos
    sessions = data_manager.load_sessions()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Menú")
        
        page = st.radio(
            "Selecciona una sección:",
            ["🏠 Dashboard", "➕ Nueva Sesión", "📊 Análisis y Visualizaciones", 
             "📝 Historial", "🤝 Accountability Partner"],
            key='page_selector'
        )
        
        st.markdown("---")
        
        # Estadísticas rápidas
        total_sessions = len(sessions)
        progress_percent = total_sessions / 100 * 100
        
        st.markdown("### 📈 Progreso")
        st.progress(progress_percent / 100)
        st.caption(f"{total_sessions}/100 días")
        
        if total_sessions > 0:
            streak = data_manager.get_current_streak()
            total_hours = data_manager.get_total_hours_studied()
            
            st.markdown(f"**🔥 Racha actual:** {streak} días")
            st.markdown(f"**⏱️ Total estudiado:** {total_hours}")
    
    # Router de páginas
    if page == "🏠 Dashboard":
        show_dashboard(sessions)
    elif page == "➕ Nueva Sesión":
        show_new_session_form()
    elif page == "📊 Análisis y Visualizaciones":
        show_analytics(sessions)
    elif page == "📝 Historial":
        show_history(sessions)
    elif page == "🤝 Accountability Partner":
        show_accountability_partner()


def show_dashboard(sessions):
    """Mostrar dashboard principal con métricas y resumen."""
    
    st.markdown("## 🎯 Dashboard Principal")
    
    if not sessions:
        # Estado inicial sin sesiones
        st.info("""
        👋 ¡Hola! Bienvenido a tu Study Tracker.
        
        Este es tu espacio para documentar tu aprendizaje durante los próximos 100 días.
        Desde análisis de datos hasta física, aquí podrás llevar un registro completo de tu progreso.
        
        **Para comenzar:**
        1. Haz clic en "➕ Nueva Sesión" en el menú lateral
        2. Registra tu primera sesión de estudio
        3. ¡Comienza tu desafío!
        """)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 10px; text-align: center; margin-top: 2rem;'>
            <h2 style='color: white;'>🏆 ¡Vamos a completar este desafío!</h2>
            <p style='color: white; font-size: 1.2rem;'>
                Cada día cuenta. Cada sesión te acerca a tu meta.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        return
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    total_sessions = len(sessions)
    progress_percent = (total_sessions / 100 * 100) if total_sessions <= 100 else 100
    
    with col1:
        st.metric("📊 Días Completados", f"{total_sessions}/100", f"{progress_percent:.1f}%")
    
    with col2:
        streak = data_manager.get_current_streak()
        st.metric("🔥 Racha Actual", f"{streak} días")
    
    with col3:
        total_hours = data_manager.get_total_hours_studied()
        st.metric("⏱️ Total Estudiado", total_hours)
    
    with col4:
        days_since = data_manager.get_days_since_last_study()
        if days_since == 0:
            st.metric("✅ Último Estudio", "Hoy")
        else:
            st.metric("⏰ Último Estudio", f"{days_since} día(s)")
    
    st.markdown("---")
    
    # Alertas y feedback
    if total_sessions > 0:
        days_since = data_manager.get_days_since_last_study()
        
        if days_since == 0:
            st.success("✅ ¡Excelente! Has estudiado hoy. Mantén el ritmo.")
        elif days_since == 1:
            st.warning("⚠️ Ayer no estudiaste. Vuelve a la rutina hoy.")
        elif days_since > 1:
            st.error(f"🚨 Han pasado {days_since} días sin estudiar. Es momento de retomar el desafío.")
    
    # Mensajes motivacionales por hitos
    if total_sessions == 10:
        st.balloons()
        st.success("🎉 ¡Primer hito! Has completado 10 días. ¡Sigue así!")
    elif total_sessions == 25:
        st.snow()
        st.success("🎊 ¡25 días completados! Estás en el cuarto del camino.")
    elif total_sessions == 50:
        st.balloons()
        st.success("🏆 ¡50 días! ¡Haz llegado a la mitad del desafío!")
    elif total_sessions == 75:
        st.snow()
        st.success("🔥 ¡75 días! Estás en la recta final.")
    elif total_sessions == 100:
        st.balloons()
        st.success("🎉🎉🎉 ¡FELICIDADES! Has completado los 100 días. ¡Eres increíble!")
    
    # Última sesión
    if sessions:
        st.markdown("### 📝 Última Sesión Registrada")
        last_session = sessions[-1]
        
        with st.container():
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                **📅 Día {last_session.get('day', '?')}/100** - {last_session.get('date', 'Sin fecha')}  
                **📚 Tema:** {last_session.get('topic', 'Sin tema')}  
                **🏷️ Categoría:** {last_session.get('category', 'Sin categoría')}  
                **⏱️ Duración:** {last_session.get('duration', 'Sin duración')}
                """)
                
                if last_session.get('daily_win'):
                    st.markdown(f"**🏆 Victoria del día:** {last_session.get('daily_win')}")
            with col2:
                if last_session.get('practical_application'):
                    st.info(f"💼 **Aplicación:** {last_session.get('practical_application')}")
    
    # Gráfico de progreso
    st.markdown("---")
    st.markdown("### 📈 Tu Progreso en el Tiempo")
    progress_chart = visualizations.create_progress_chart(sessions)
    st.plotly_chart(progress_chart, use_container_width=True)


def show_new_session_form():
    """Mostrar formulario para nueva sesión."""
    
    st.markdown("## ➕ Registra tu Sesión de Estudio")
    
    st.info("""
    📝 Completa este formulario para registrar tu sesión de estudio.
    Todos los campos marcados con (*) son obligatorios.
    """)
    
    with st.form("new_session_form", clear_on_submit=True):
        # Fecha (auto-completada con hoy)
        today = datetime.now().strftime('%Y-%m-%d')
        date_input = st.date_input("Fecha (*)", value=datetime.now(), disabled=True)
        date_str = date_input.strftime('%Y-%m-%d')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Categoría
            category = st.selectbox(
                "Categoría (*)",
                ["Data Analysis", "Physics", "Statistics", "SQL", "Visualization", "Mixed"]
            )
        
        with col2:
            # Dificultad
            difficulty = st.select_slider(
                "Dificultad (*)",
                options=["Muy fácil", "Fácil", "Medio", "Difícil", "Muy difícil"],
                value="Medio"
            )
        
        # Tema
        topic = st.text_input(
            "Tema estudiado (*)",
            placeholder="Ej: Window Functions en SQL, Análisis de Series Temporales, etc.",
            help="Describe brevemente el tema que estudiaste"
        )
        
        # Duración
        duration = st.text_input(
            "Duración (*)",
            placeholder="Ej: 2 horas, 45 minutos, 1h 30min",
            help="Formato libre: puedes escribir como prefieras (2 horas, 90 minutos, etc.)"
        )
        
        # Victoria del día
        daily_win = st.text_area(
            "🏆 Victoria del día (*)",
            placeholder="¿Qué logro específico conseguiste hoy? Ej: Finalmente entendí cómo funcionan las CTEs",
            help="El logro más importante o satisfactorio de esta sesión",
            height=80
        )
        
        # Aprendizajes clave
        key_learnings = st.text_area(
            "✨ Aprendizajes clave",
            placeholder="¿Qué aprendiste hoy? ¿Qué conceptos o ideas fueron las más importantes?",
            help="Principales aprendizajes de la sesión",
            height=100
        )
        
        # Recursos utilizados
        resources = st.text_area(
            "📖 Recursos utilizados",
            placeholder="Links, libros, cursos, videos, artículos que usaste...",
            help="Recursos que consultaste durante la sesión",
            height=100
        )
        
        # Nivel de concentración
        focus_level = st.select_slider(
            "Nivel de concentración",
            options=["Muy bajo", "Bajo", "Medio", "Alto", "Excelente"],
            value="Medio"
        )
        
        # Obstáculos
        obstacles = st.text_area(
            "🤔 Obstáculos enfrentados",
            placeholder="¿Qué dificultades encontraste? (opcional)",
            help="Problemas, bloqueos o desafíos que enfrentaste",
            height=80
        )
        
        # Próximos pasos
        next_steps = st.text_area(
            "🚀 Próximos pasos",
            placeholder="¿Qué planeas estudiar en tu próxima sesión? (opcional)",
            help="Lo que te gustaría revisar o aprender después",
            height=80
        )
        
        # Aplicación práctica
        practical_application = st.text_area(
            "💼 Aplicación práctica",
            placeholder="¿Cómo puedes aplicar esto en tu trabajo como analista? (opcional)",
            help="Conexión entre lo aprendido y tu trabajo actual",
            height=80
        )
        
        # Botón de envío
        submitted = st.form_submit_button(
            "💾 Guardar Sesión",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            # Validar campos obligatorios
            if not topic:
                st.error("❌ Por favor, completa el campo 'Tema estudiado'")
            elif not duration:
                st.error("❌ Por favor, completa el campo 'Duración'")
            elif not daily_win:
                st.error("❌ Por favor, completa el campo 'Victoria del día'")
            else:
                # Crear objeto de sesión
                session_data = {
                    'date': date_str,
                    'category': category,
                    'topic': topic,
                    'duration': duration,
                    'daily_win': daily_win,
                    'key_learnings': key_learnings if key_learnings else "",
                    'resources': resources if resources else "",
                    'difficulty': difficulty,
                    'focus_level': focus_level,
                    'obstacles': obstacles if obstacles else "",
                    'next_steps': next_steps if next_steps else "",
                    'practical_application': practical_application if practical_application else ""
                }
                
                # Guardar sesión
                if data_manager.add_session(session_data):
                    st.success("✅ ¡Sesión guardada exitosamente!")
                    st.balloons()  # ¡Celebración!
                    
                    # Mostrar resumen
                    st.info(f"""
                    📊 **Sesión registrada:**
                    - Día {len(data_manager.load_sessions())}/100
                    - Tema: {topic}
                    - Categoría: {category}
                    
                    Puedes generar un post para redes sociales en la sección "📝 Historial"
                    """)
                    
                    # Auto-redirigir al dashboard después de 2 segundos
                    st.balloons()  # Más celebración
                else:
                    st.error("❌ Error al guardar la sesión. Por favor, intenta de nuevo.")


def show_analytics(sessions):
    """Mostrar análisis y visualizaciones."""
    
    st.markdown("## 📊 Análisis y Visualizaciones")
    
    if not sessions:
        st.info("No hay datos para visualizar aún. Registra tu primera sesión para comenzar.")
        return
    
    # Layout de gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            visualizations.create_weekday_distribution(sessions),
            use_container_width=True
        )
    
    with col2:
        st.plotly_chart(
            visualizations.create_category_distribution(sessions),
            use_container_width=True
        )
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.plotly_chart(
            visualizations.create_difficulty_pie(sessions),
            use_container_width=True
        )
    
    with col4:
        st.plotly_chart(
            visualizations.create_focus_pie(sessions),
            use_container_width=True
        )
    
    st.markdown("---")
    
    st.plotly_chart(
        visualizations.create_balance_chart(sessions),
        use_container_width=True
    )
    
    st.markdown("---")
    
    st.plotly_chart(
        visualizations.create_topic_frequency(sessions),
        use_container_width=True
    )


def show_history(sessions):
    """Mostrar historial de sesiones con filtros."""
    
    st.markdown("## 📝 Historial de Sesiones")
    
    if not sessions:
        st.info("No hay sesiones registradas aún.")
        return
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_option = st.selectbox(
            "Filtrar por período:",
            ["Todas", "Últimas 7", "Últimas 30", "Hitos (10, 20, 30...)"]
        )
    
    with col2:
        search_term = st.text_input("🔍 Buscar por tema:", "")
    
    with col3:
        sort_option = st.selectbox(
            "Ordenar por:",
            ["Más reciente", "Más antigua", "Por día"]
        )
    
    # Aplicar filtros
    filtered_sessions = sessions.copy()
    
    if filter_option == "Últimas 7":
        filtered_sessions = filtered_sessions[-7:]
    elif filter_option == "Últimas 30":
        filtered_sessions = filtered_sessions[-30:]
    elif filter_option == "Hitos (10, 20, 30...)":
        filtered_sessions = [s for s in filtered_sessions if s.get('day', 0) % 10 == 0]
    
    if search_term:
        filtered_sessions = [
            s for s in filtered_sessions
            if search_term.lower() in s.get('topic', '').lower()
        ]
    
    # Ordenar
    if sort_option == "Más reciente":
        filtered_sessions = list(reversed(filtered_sessions))
    elif sort_option == "Por día":
        filtered_sessions = sorted(filtered_sessions, key=lambda x: x.get('day', 0))
    
    st.caption(f"Mostrando {len(filtered_sessions)} de {len(sessions)} sesiones")
    st.markdown("---")
    
    # Mostrar sesiones
    for session in filtered_sessions:
        with st.expander(
            f"📅 Día {session.get('day', '?')}/100 - {session.get('date', 'Sin fecha')} | {session.get('topic', 'Sin tema')}",
            expanded=False
        ):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **🏷️ Categoría:** {session.get('category', 'N/A')}  
                **⏱️ Duración:** {session.get('duration', 'N/A')}  
                **📊 Dificultad:** {session.get('difficulty', 'N/A')}  
                **🎯 Concentración:** {session.get('focus_level', 'N/A')}
                """)
            
            with col2:
                st.markdown(f"""
                **✨ Aprendizajes clave:**  
                {session.get('key_learnings', 'N/A')}
                """)
            
            st.markdown(f"**🏆 Victoria del día:** {session.get('daily_win', 'N/A')}")
            
            if session.get('resources'):
                st.markdown(f"**📖 Recursos:** {session.get('resources')}")
            
            if session.get('obstacles'):
                st.markdown(f"**🤔 Obstáculos:** {session.get('obstacles')}")
            
            if session.get('next_steps'):
                st.markdown(f"**🚀 Próximos pasos:** {session.get('next_steps')}")
            
            if session.get('practical_application'):
                st.info(f"**💼 Aplicación:** {session.get('practical_application')}")
            
            # Botones de acción
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("📱 Generar Post Social", key=f"post_{session.get('id')}"):
                    post = content_generator.generate_social_post(session)
                    st.text_area("📝 Post para Redes Sociales:", post, height=200)
            
            with col_btn2:
                if st.button("📄 Generar Artículo Medium", key=f"article_{session.get('id')}"):
                    article = content_generator.generate_medium_article(session)
                    st.download_button(
                        label="📥 Descargar .md",
                        data=article,
                        file_name=f"día_{session.get('day')}_{session.get('date')}_medium.md",
                        mime="text/markdown"
                    )
            
            with col_btn3:
                if st.button("🗑️ Eliminar Sesión", key=f"delete_{session.get('id')}"):
                    if data_manager.delete_session(session.get('id')):
                        st.success("✅ Sesión eliminada")
                        st.rerun()
                    else:
                        st.error("❌ Error al eliminar")
            
            st.markdown("---")


def show_accountability_partner():
    """Mostrar página de accountability partner."""
    
    st.markdown("## 🤝 Tu Accountability Partner")
    
    sessions = data_manager.load_sessions()
    
    days_since = data_manager.get_days_since_last_study()
    total_sessions = len(sessions)
    
    # Diagnóstico
    if total_sessions == 0:
        st.info("🎯 Comienza tu desafío registrando tu primera sesión.")
        return
    
    # Alertas
    if days_since == 0:
        st.success("✅ ¡Excelente! Has estudiado hoy. Mantén la consistencia.")
    elif days_since == 1:
        st.warning("⚠️ No estudiaste ayer. ¿Qué pasó?")
    elif days_since >= 2:
        st.error(f"🚨 Llevas {days_since} días sin estudiar. Es momento de retomar.")
    
    # Sistema de detección de procrastinación
    st.markdown("---")
    st.markdown("### 🔍 Detector de Procrastinación")
    
    if days_since == 0:
        status_color = "#10B981"  # Verde
        status_emoji = "✅"
        status_text = "Todo bien"
    elif days_since == 1:
        status_color = "#F59E0B"  # Amarillo
        status_emoji = "⚠️"
        status_text = "Atención"
    else:
        status_color = "#EF4444"  # Rojo
        status_emoji = "🚨"
        status_text = "Acción requerida"
    
    st.markdown(f"""
    <div style='background-color: {status_color}; padding: 1rem; border-radius: 8px; text-align: center;'>
        <h2 style='color: white; margin: 0;'>{status_emoji} {status_text}</h2>
        <p style='color: white; margin: 0.5rem 0 0 0;'>
            Días sin estudiar: <strong>{days_since}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Diagnóstico interactivo
    if days_since > 0:
        st.markdown("---")
        st.markdown("### 🤔 ¿Por qué no has estudiado?")
        
        blockages = st.multiselect(
            "Selecciona lo que resuena contigo:",
            [
                "Miedo al fracaso o ansiedad",
                "Sobreestimado/a",
                "Distraído/a",
                "Sin energía física",
                "No sé por dónde empezar",
                "No tengo tiempo",
                "Prefiero hacer otras cosas",
                "Otro"
            ]
        )
        
        if blockages:
            st.markdown("### 💡 Estrategias Específicas")
            
            strategies = {
                "Miedo al fracaso o ansiedad": """
                **🎯 Rompe el ciclo del miedo:**
                - Estudia por solo 15 minutos. Nadie falla en 15 minutos.
                - Define un "fallo tolerable": el peor escenario realista.
                - Anota 3 cosas que pasarán SI estudias (no si no lo haces).
                """,
                "Sobreestimado/a": """
                **🎯 Simplifica:**
                - Reduce tu meta: ¿Qué es lo MÍNIMO que te haría sentir bien hoy?
                - Usa la regla de 2 minutos: "Solo voy a abrir el libro/laptop"
                - Divide en micro-tareas: ver un video de 10 min, no una clase entera.
                """,
                "Distraído/a": """
                **🎯 Control del ambiente:**
                - Modo avión en el teléfono durante 25 minutos.
                - Usa pomodoro: 25 min estudiar, 5 min descanso.
                - Ambient noise (puedo recomendarte sitios).
                - Un solo programa abierto (poca opción = menos decisiones).
                """,
                "Sin energía física": """
                **🎯 Energía física vs mental:**
                - Diferencia entre cansancio físico (cuerpo) y mental (cerebro).
                - Si es físico: descansa 20 min con timer, luego intenta.
                - Si es mental: haz algo sencillo primero (revisar apuntes, no crear nuevo contenido).
                - Hidrátate, come ligero, y observa: ¿en qué horario ESTOY más concentrado?
                """,
                "No sé por dónde empezar": """
                **🎯 Define el punto de entrada:**
                - Haz una lista de 3 temas posibles.
                - Usa una ruleta para decidir.
                - O elige el que suene MENOS apetecible (lo importante es empezar, no la perfección).
                - Meta tipo "investigar X" en vez de "dominar X".
                """,
                "No tengo tiempo": """
                **🎯 Revisa tu agenda real:**
                - Anota durante 3 días en qué pierdes tiempo (sin juzgar).
                - Identifica gaps de 15 min: en el transporte, antes de almorzar, etc.
                - Acuérdate: 15 min de 100 días = 25 horas acumuladas.
                """,
                "Prefiero hacer otras cosas": """
                **🎯 Honestidad primero:**
                - ¿Es realmente que prefieres no estudiar, o es resistencia interna?
                - Formula: "Haré 10 minutos, y luego puedo hacer lo otro"
                - O asume el costo real: "¿Cuánto va a doler en 3 meses si NO lo hago?"
                """,
                "Otro": """
                **🎯 Personaliza:**
                - Escribe libremente durante 10 minutos POR QUÉ no lo haces (sin autocensura).
                - Identifica el patrón detrás del rechazo.
                - Prueba la estrategia de "contrato contigo mismo": 
                  "Hoy haré X, y si lo cumplo, [recompensa específica].
                """
            }
            
            for blockage in blockages:
                st.markdown(f"#### {blockage}")
                st.markdown(strategies.get(blockage, "Estrategia personalizada pendiente."))
                st.markdown("---")
    
    # Análisis de patrones
    if total_sessions >= 5:
        st.markdown("### 📈 Análisis de Patrones")
        
        # Día más productivo
        weekday_data = visualizations.create_weekday_distribution(sessions)
        st.plotly_chart(weekday_data, use_container_width=True)
        
        st.info("""
        **💡 Consejo:** 
        Identifica en qué días de la semana eres más productivo.
        Planifica tus sesiones de estudio intensas en esos días.
        """)


if __name__ == "__main__":
    main()

