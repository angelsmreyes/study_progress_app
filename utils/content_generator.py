"""
Módulo para generación de contenido: posts sociales y artículos de Medium.
"""

import re
from typing import Dict
from datetime import datetime


def format_date_spanish(date_str: str) -> str:
    """
    Formatear fecha en formato español legible.
    
    Args:
        date_str: Fecha en formato ISO (YYYY-MM-DD)
        
    Returns:
        str: Fecha formateada en español
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        months_es = {
            1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
            5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
            9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
        }
        
        weekday_es = {
            0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves',
            4: 'Viernes', 5: 'Sábado', 6: 'Domingo'
        }
        
        day_name = weekday_es[date_obj.weekday()]
        month_name = months_es[date_obj.month]
        
        return f"{day_name}, {date_obj.day} de {month_name} de {date_obj.year}"
    except:
        return date_str


def generate_social_post(session: Dict) -> str:
    """
    Generar post para redes sociales (Twitter/LinkedIn).
    
    Args:
        session: Datos de la sesión
        
    Returns:
        str: Post formateado para redes sociales
    """
    day = session.get('day', '?')
    category = session.get('category', 'General')
    topic = session.get('topic', 'Sin tema')
    duration = session.get('duration', 'Tiempo indeterminado')
    learnings = session.get('key_learnings', 'Sin aprendizajes registrados')
    daily_win = session.get('daily_win', 'Sin victoria del día')
    
    # Truncar aprendizajes si son muy largos
    learnings_short = learnings[:200] + '...' if len(learnings) > 200 else learnings
    
    post = f"""🚀 Día {day}/100 - Mejorando como Data Analyst

📊 Categoría: {category}
📚 Tema: {topic}
⏱️ Duración: {duration}

✨ Aprendizajes clave:
{learnings_short}

🏆 Victoria del día: {daily_win}

#100DaysOfLearning #DataAnalytics #Physics #Python #SQL #DataScience"""
    
    return post


def generate_medium_article(session: Dict) -> str:
    """
    Generar borrador de artículo para Medium.
    
    Args:
        session: Datos de la sesión
        
    Returns:
        str: Artículo completo en formato Markdown
    """
    day = session.get('day', '?')
    category = session.get('category', 'General')
    topic = session.get('topic', 'Sin tema')
    duration = session.get('duration', 'Tiempo indeterminado')
    date = session.get('date', 'Fecha no disponible')
    
    learnings = session.get('key_learnings', 'Por definir')
    daily_win = session.get('daily_win', 'Por definir')
    resources = session.get('resources', 'No especificados')
    obstacles = session.get('obstacles', 'Ninguno especificado')
    next_steps = session.get('next_steps', 'Por definir')
    practical_application = session.get('practical_application', 'Por definir')
    
    formatted_date = format_date_spanish(date)
    
    # Crear emoji según categoría
    category_emoji = {
        'Data Analysis': '📊',
        'Physics': '⚛️',
        'Statistics': '📈',
        'SQL': '💾',
        'Visualization': '📈',
        'Mixed': '🎯'
    }
    
    emoji = category_emoji.get(category, '📚')
    
    article = f"""---
title: "Día {day}/100: {topic}"
date: {formatted_date}
category: {category}
---

{emoji} # Día {day} - {topic}

{formatted_date}

---

## ⏱️ Tiempo Dedicado

{duration}

## 📚 Categoría

{category}

## 🎯 Tema de Hoy

{topic}

## ✨ Aprendizajes Clave

{learnings}

## 🏆 Victoria del Día

{daily_win}

## 📖 Recursos Utilizados

{resources}

## 🤔 Obstáculos Enfrentados

{obstacles}

## 🚀 Próximos Pasos

{next_steps}

## 💼 Aplicación Práctica

{practical_application}

---

## 📝 Reflexión Personal

[Tu reflexión personal aquí]

---

**Progreso del desafío:** {day}/100 días completados

#100DaysOfLearning #DataAnalytics #Physics #DataScience"""
    
    return article


def get_social_post_summary(session: Dict) -> str:
    """
    Obtener un resumen corto para previsualizar el post.
    
    Args:
        session: Datos de la sesión
        
    Returns:
        str: Resumen del post
    """
    day = session.get('day', '?')
    category = session.get('category', 'General')
    topic = session.get('topic', 'Sin tema')
    
    return f"Día {day}/100 | {category} | {topic}"


def get_session_preview(session: Dict) -> str:
    """
    Generar vista previa compacta de una sesión.
    
    Args:
        session: Datos de la sesión
        
    Returns:
        str: Vista previa formateada
    """
    day = session.get('day', '?')
    date = session.get('date', 'Sin fecha')
    topic = session.get('topic', 'Sin tema')
    duration = session.get('duration', 'Sin duración')
    category = session.get('category', 'General')
    
    formatted_date = format_date_spanish(date)
    
    preview = f"""
### Día {day} | {formatted_date}
**Tema:** {topic}  
**Categoría:** {category}  
**Duración:** {duration}
"""
    
    return preview

