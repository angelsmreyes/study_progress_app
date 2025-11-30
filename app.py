import streamlit as st
from datetime import datetime
from utils import data_manager, content_generator, visualizations
import json

"""
Study Tracker 100 Days - Streamlit App
Application for tracking study sessions during 100 days
"""


def main():
    """Main function of the application."""
    
    # Inicialización de session_state
    if 'show_form' not in st.session_state:
        st.session_state.show_form = False
    if 'edit_session' not in st.session_state:
        st.session_state.edit_session = None
    
    # Header principal
    st.markdown("""
    <div style='background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: white; text-align: center; margin: 0;'>📚 Study Tracker 100 Days</h1>
        <p style='color: white; text-align: center; margin: 0.5rem 0 0 0; opacity: 0.9;'>
            Getting better as Data Analyst | Physics Review | Preparing for Master's
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cargar datos
    sessions = data_manager.load_sessions()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Menu")
        
        page = st.radio(
            "Select a section:",
            ["🏠 Dashboard", "➕ New Session", "📊 Analysis and Visualizations", 
             "📝 History", "🤝 Accountability Partner"],
            key='page_selector'
        )
        
        st.markdown("---")
        
        # Estadísticas rápidas
        total_sessions = len(sessions)
        progress_percent = total_sessions / 100 * 100
        
        st.markdown("### 📈 Progress")
        st.progress(progress_percent / 100)
        st.caption(f"{total_sessions}/100 days")
        
        if total_sessions > 0:
            streak = data_manager.get_current_streak()
            total_hours = data_manager.get_total_hours_studied()
            
            st.markdown(f"**🔥 Current streak:** {streak} days")
            st.markdown(f"**⏱️ Total studied:** {total_hours}")
    
    # Router de páginas
    if page == "🏠 Dashboard":
        show_dashboard(sessions)
    elif page == "➕ New Session":
        show_session_form()
    elif page == "📊 Analysis and Visualizations":
        show_analytics(sessions)
    elif page == "📝 History":
        show_history(sessions)
    elif page == "🤝 Accountability Partner":
        show_accountability_partner()


def show_dashboard(sessions):
    """Show main dashboard with metrics and summary."""
    
    st.markdown("## 🎯 Main Dashboard")
    
    if not sessions:
        # Initial state without sessions
        st.info("""
        👋 Hello! Welcome to your Study Tracker.
        
        This is your space to document your learning during the next 100 days.
        From data analysis to physics, here you can keep a complete record of your progress.
        
        **To start:**
        1. Click on "➕ New Session" in the sidebar
        2. Register your first study session
        3. Start your challenge!
        """)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 10px; text-align: center; margin-top: 2rem;'>
            <h2 style='color: white;'>🏆 Let's complete this challenge!</h2>
            <p style='color: white; font-size: 1.2rem;'>
                Each day counts. Each session brings you closer to your goal.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        return
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    total_sessions = len(sessions)
    progress_percent = (total_sessions / 100 * 100) if total_sessions <= 100 else 100
    
    with col1:
        st.metric("📊 Days Completed", f"{total_sessions}/100", f"{progress_percent:.1f}%")
    
    with col2:
        streak = data_manager.get_current_streak()
        st.metric("🔥 Current Streak", f"{streak} days")
    
    with col3:
        total_hours = data_manager.get_total_hours_studied()
        st.metric("⏱️ Total Studied", total_hours)
    
    with col4:
        days_since = data_manager.get_days_since_last_study()
        if days_since == 0:
            st.metric("✅ Last Study", "Today")
        else:
            st.metric("⏰ Last Study", f"{days_since} day(s)")
    
    st.markdown("---")
    
    # Alerts and feedback
    if total_sessions > 0:
        days_since = data_manager.get_days_since_last_study()
        
        if days_since == 0:
            st.success("✅ ¡Excellent! You studied today. Keep it up.")
        elif days_since == 1:
            st.warning("⚠️ You didn't study yesterday. Return to the routine today.")
        elif days_since > 1:
            st.error(f"🚨 {days_since} days have passed since your last study. It's time to resume the challenge.")
    
    # Messages motivational milestones
    if total_sessions == 10:
        st.balloons()
        st.success("🎉 ¡First milestone! You've completed 10 days. Keep it up!")
    elif total_sessions == 25:
        st.snow()
        st.success("🎊 ¡25 days completed! You're in the fourth of the journey.")
    elif total_sessions == 50:
        st.balloons()
        st.success("🏆 ¡50 days! You've reached the middle of the challenge!")
    elif total_sessions == 75:
        st.snow()
        st.success("🔥 ¡75 days! You're in the final stretch.")
    elif total_sessions == 100:
        st.balloons()
        st.success("🎉🎉🎉 ¡Congratulations! You've completed 100 days. You're incredible!")    
    
    # Last session
    if sessions:
        st.markdown("### 📝 Last Session Registered")
        last_session = sessions[-1]
        
        with st.container():
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                **📅 Day {last_session.get('day', '?')}/100** - {last_session.get('date', 'Sin fecha')}  
                **📚 Topic:** {last_session.get('topic', 'Sin tema')}  
                **🏷️ Category:** {last_session.get('category', 'Sin categoría')}  
                **⏱️ Duration:** {last_session.get('duration', 'Sin duración')}
                """)
                
                if last_session.get('daily_win'):
                    st.markdown(f"**🏆 Daily win:** {last_session.get('daily_win')}")
            with col2:
                if last_session.get('practical_application'):
                    st.info(f"💼 **Practical application:** {last_session.get('practical_application')}")
    
    # Progress chart
    st.markdown("---")
    st.markdown("### 📈 Your Progress Over Time")
    progress_chart = visualizations.create_progress_chart(sessions)
    st.plotly_chart(progress_chart, width='stretch')


def show_session_form():
    """Show form for new session or editing."""
    
    is_edit = st.session_state.edit_session is not None
    session_to_edit = st.session_state.edit_session if is_edit else {}
    
    title = "✏️ Edit Session" if is_edit else "➕ Register your Study Session"
    st.markdown(f"## {title}")
    
    if is_edit:
        st.info(f"Editing session for day {session_to_edit.get('day')}")
    else:
        st.info("""
        📝 Completa este formulario para registrar tu sesión de estudio.
        Todos los campos marcados con (*) son obligatorios.
        """)
    
    with st.form("session_form", clear_on_submit=not is_edit):
        # Fecha
        default_date = datetime.now()
        if is_edit and session_to_edit.get('date'):
            default_date = datetime.fromisoformat(session_to_edit.get('date'))
            
        date_input = st.date_input("Fecha (*)", value=default_date, disabled=False) # Permitir editar fecha si es necesario
        date_str = date_input.strftime('%Y-%m-%d')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Categoría
            cat_index = 0
            categories = ["Data Analysis", "Physics", "Statistics", "SQL", "Visualization", "Mixed"]
            if is_edit and session_to_edit.get('category') in categories:
                cat_index = categories.index(session_to_edit.get('category'))
                
            category = st.selectbox(
                "Categoría (*)",
                categories,
                index=cat_index
            )
        
        with col2:
            # Dificultad
            diff_options = ["Easy", "Medium", "Hard", "Very Hard"]
            diff_value = "Medium"
            if is_edit and session_to_edit.get('difficulty') in diff_options:
                diff_value = session_to_edit.get('difficulty')
                
            difficulty = st.select_slider(
                "Difficulty (*)",
                options=diff_options,
                value=diff_value
            )
        
        # Tema
        topic = st.text_input(
            "Topic studied (*)",
            value=session_to_edit.get('topic', ''),
            placeholder="Ej: Window Functions in SQL, Time Series Analysis, etc.",
            help="Briefly describe the topic you studied"
        )
        
        # Duration
        duration = st.text_input(
            "Duration (*)",
            value=session_to_edit.get('duration', ''),
            placeholder="Ej: 2 hours, 45 minutes, 1h 30min",
            help="Free format: you can write as you prefer (2 hours, 90 minutes, etc.)"
        )
        
        # Daily win
        daily_win = st.text_area(
            "Daily win (*)",
            value=session_to_edit.get('daily_win', ''),
            placeholder="What specific achievement did you get today? Ej: Finally understood how CTEs work",
            help="The most important or satisfying achievement of this session",
            height=80
        )
        
        # Key learnings
        key_learnings = st.text_area(
            "Key learnings",
            value=session_to_edit.get('key_learnings', ''),
            placeholder="What did you learn today? What concepts or ideas were the most important?",
            help="The most important or satisfying achievement of this session",
            height=100
        )
        
        # Resources used
        resources = st.text_area(
            "Resources used",
            value=session_to_edit.get('resources', ''),
            placeholder="Links, books, courses, videos, articles you used...",
            help="Resources you consulted during the session",
            height=100
        )
        
        # Focus level
        focus_options = ["Muy bajo", "Bajo", "Medio", "Alto", "Excelente"]
        focus_value = "Medio"
        if is_edit and session_to_edit.get('focus_level') in focus_options:
            focus_value = session_to_edit.get('focus_level')
            
        focus_level = st.select_slider(
            "Focus level",
            options=focus_options,
            value=focus_value
        )
        
        # Obstacles
        obstacles = st.text_area(
            "Obstacles faced",
            value=session_to_edit.get('obstacles', ''),
            placeholder="What difficulties did you face? (optional)",
            help="Problems, blocks or challenges you faced",
            height=80
        )
        
        # Next steps
        next_steps = st.text_area(
            "Next steps",
            value=session_to_edit.get('next_steps', ''),
            placeholder="What do you plan to study in your next session? (optional)",
            help="What you want to review or learn next",
            height=80
        )
        
        # Practical application
        practical_application = st.text_area(
            "Practical application",
            value=session_to_edit.get('practical_application', ''),
            placeholder="How can you apply this in your work as an analyst? (optional)",
            help="Connection between what you learned and your current job",
            height=80
        )
        
        # Submit button
        btn_label = "💾 Update Session" if is_edit else "💾 Save Session"
        submitted = st.form_submit_button(
            btn_label,
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            # Validate required fields
            if not topic:
                st.error("❌ Please complete the 'Topic studied' field")
            elif not duration:
                st.error("❌ Please complete the 'Duration' field")
            elif not daily_win:
                st.error("❌ Please complete the 'Daily win' field")
            else:
                # Create session object
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
                
                if is_edit:
                    # Maintain ID and other fields
                    session_data['id'] = session_to_edit['id']
                    session_data['day'] = session_to_edit['day']
                    session_data['created_at'] = session_to_edit['created_at']
                    
                    if data_manager.save_session(session_data):
                        st.success("✅ ¡Session updated successfully!")
                        st.session_state.edit_session = None # Limpiar estado
                        st.balloons()
                    else:
                        st.error("❌ Error updating session.")
                else:
                    # Guardar nueva sesión
                    if data_manager.add_session(session_data):
                        st.success("✅ ¡Session saved successfully!")
                        st.balloons()
                        
                        # Show summary
                        st.info(f"""
                        📊 **Session registered:**
                        - Day {len(data_manager.load_sessions())}/100
                        - Topic: {topic}
                        - Category: {category}
                        
                        You can generate a post for social media in the "📝 History" section
                        """)
                    else:
                        st.error("❌ Error saving session. Please try again.")


def show_analytics(sessions):
    """Show analytics and visualizations."""
    
    st.markdown("## 📊 Analytics and Visualizations")
    
    if not sessions:
        st.info("No data to visualize yet. Register your first session to start.")
        return
    
    # Layout of charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            visualizations.create_weekday_distribution(sessions),
            width='stretch'
        )
    
    with col2:
        st.plotly_chart(
            visualizations.create_category_distribution(sessions),
            width='stretch'
        )
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.plotly_chart(
            visualizations.create_difficulty_pie(sessions),
            width='stretch'
        )
    
    with col4:
        st.plotly_chart(
            visualizations.create_focus_pie(sessions),
            width='stretch'
        )
    
    st.markdown("---")
    
    st.plotly_chart(
        visualizations.create_balance_chart(sessions),
        width='stretch'
    )
    
    st.markdown("---")
    
    st.plotly_chart(
        visualizations.create_topic_frequency(sessions),
        width='stretch'
    )


def edit_session_callback(session):
    """Callback para preparar la edición de una sesión."""
    st.session_state.edit_session = session
    st.session_state.page_selector = "➕ Nueva Sesión"

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
            col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
            
            with col_btn1:
                st.button(
                    "✏️ Editar", 
                    key=f"edit_{session.get('id')}",
                    on_click=edit_session_callback,
                    args=(session,)
                )

            with col_btn2:
                if st.button("📱 Post Social", key=f"post_{session.get('id')}"):
                    post_es = content_generator.generate_social_post(session, language="es")
                    post_en = content_generator.generate_social_post(session, language="en")
                    
                    tabs = st.tabs(["🇪🇸 Español", "🇺🇸 English"])
                    
                    with tabs[0]:
                        st.text_area(
                            "📝 Post para Redes Sociales (ES):",
                            post_es,
                            height=220,
                            key=f"post_es_{session.get('id')}"
                        )
                    
                    with tabs[1]:
                        st.text_area(
                            "📝 Social Post (EN):",
                            post_en,
                            height=220,
                            key=f"post_en_{session.get('id')}"
                        )
            
            with col_btn3:
                if st.button("📄 Artículo Medium", key=f"article_{session.get('id')}"):
                    article = content_generator.generate_medium_article(session)
                    st.download_button(
                        label="📥 Descargar .md",
                        data=article,
                        file_name=f"día_{session.get('day')}_{session.get('date')}_medium.md",
                        mime="text/markdown"
                    )
            
            with col_btn4:
                if st.button("🗑️ Eliminar", key=f"delete_{session.get('id')}"):
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
        st.plotly_chart(weekday_data, width='stretch')
        
        st.info("""
        **💡 Consejo:** 
        Identifica en qué días de la semana eres más productivo.
        Planifica tus sesiones de estudio intensas en esos días.
        """)


if __name__ == "__main__":
    main()

