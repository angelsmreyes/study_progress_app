import streamlit as st

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
    st.plotly_chart(progress_chart, width='stretch')