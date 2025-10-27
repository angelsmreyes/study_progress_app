"""
Módulo para visualizaciones con Plotly.
Incluye gráficos de progreso, distribución, y análisis de patrones.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict
from collections import Counter
from datetime import datetime
import pandas as pd


def create_progress_chart(sessions: List[Dict]) -> go.Figure:
    """
    Crear gráfico de progreso en el tiempo.
    
    Args:
        sessions: Lista de sesiones
        
    Returns:
        go.Figure: Gráfico de línea con progreso
    """
    if not sessions:
        return _create_empty_chart("No hay datos disponibles")
    
    # Preparar datos
    df = pd.DataFrame(sessions)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Calcular progreso acumulado
    df['cumulative_days'] = range(1, len(df) + 1)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['cumulative_days'],
        mode='lines+markers',
        name='Progreso',
        line=dict(color='#4F46E5', width=3),
        marker=dict(size=8, color='#6366F1'),
        fill='tonexty',
        fillcolor='rgba(79, 70, 229, 0.1)'
    ))
    
    fig.update_layout(
        title=dict(
            text='📈 Progreso del Desafío',
            x=0.5,
            font=dict(size=20, color='#1F2937')
        ),
        xaxis_title='Fecha',
        yaxis_title='Días Completados',
        plot_bgcolor='white',
        paper_bgcolor='#F9FAFB',
        height=400,
        hovermode='x unified'
    )
    
    return fig


def create_weekday_distribution(sessions: List[Dict]) -> go.Figure:
    """
    Crear gráfico de barras con distribución de días de la semana.
    
    Args:
        sessions: Lista de sesiones
        
    Returns:
        go.Figure: Gráfico de barras
    """
    if not sessions:
        return _create_empty_chart("No hay datos disponibles")
    
    # Días de la semana en español
    weekdays_es = {
        0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves',
        4: 'Viernes', 5: 'Sábado', 6: 'Domingo'
    }
    
    # Contar sesiones por día de la semana
    df = pd.DataFrame(sessions)
    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = df['date'].dt.dayofweek.map(weekdays_es)
    
    weekday_counts = df['weekday'].value_counts().sort_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=weekday_counts.index,
        y=weekday_counts.values,
        marker_color='#10B981',
        text=weekday_counts.values,
        textposition='outside'
    ))
    
    fig.update_layout(
        title=dict(
            text='📅 Distribución por Día de la Semana',
            x=0.5,
            font=dict(size=18)
        ),
        xaxis_title='Día de la Semana',
        yaxis_title='Número de Sesiones',
        plot_bgcolor='white',
        paper_bgcolor='#F9FAFB',
        height=350
    )
    
    return fig


def create_category_distribution(sessions: List[Dict]) -> go.Figure:
    """
    Crear gráfico pie con distribución por categoría.
    
    Args:
        sessions: Lista de sesiones
        
    Returns:
        go.Figure: Gráfico pie
    """
    if not sessions:
        return _create_empty_chart("No hay datos disponibles")
    
    categories = [s.get('category', 'Sin categoría') for s in sessions]
    category_counts = Counter(categories)
    
    labels = list(category_counts.keys())
    values = list(category_counts.values())
    
    colors = px.colors.qualitative.Set3
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=colors,
        textinfo='label+percent',
        textfont=dict(size=12)
    )])
    
    fig.update_layout(
        title=dict(
            text='📊 Distribución por Categoría',
            x=0.5,
            font=dict(size=18)
        ),
        height=400,
        paper_bgcolor='#F9FAFB'
    )
    
    return fig


def create_difficulty_pie(sessions: List[Dict]) -> go.Figure:
    """
    Crear gráfico pie con distribución de dificultad.
    
    Args:
        sessions: Lista de sesiones
        
    Returns:
        go.Figure: Gráfico pie
    """
    if not sessions:
        return _create_empty_chart("No hay datos disponibles")
    
    difficulties = [s.get('difficulty', 'Sin especificar') for s in sessions]
    difficulty_counts = Counter(difficulties)
    
    labels = list(difficulty_counts.keys())
    values = list(difficulty_counts.values())
    
    # Colores por dificultad
    color_map = {
        'Muy fácil': '#10B981',
        'Fácil': '#34D399',
        'Medio': '#F59E0B',
        'Difícil': '#F97316',
        'Muy difícil': '#EF4444'
    }
    
    colors = [color_map.get(label, '#94A3B8') for label in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker_colors=colors,
        textinfo='label+percent'
    )])
    
    fig.update_layout(
        title=dict(
            text='📉 Distribución de Dificultad',
            x=0.5,
            font=dict(size=18)
        ),
        height=350,
        paper_bgcolor='#F9FAFB'
    )
    
    return fig


def create_focus_pie(sessions: List[Dict]) -> go.Figure:
    """
    Crear gráfico pie con distribución de nivel de concentración.
    
    Args:
        sessions: Lista de sesiones
        
    Returns:
        go.Figure: Gráfico pie
    """
    if not sessions:
        return _create_empty_chart("No hay datos disponibles")
    
    focus_levels = [s.get('focus_level', 'Sin especificar') for s in sessions]
    focus_counts = Counter(focus_levels)
    
    labels = list(focus_counts.keys())
    values = list(focus_counts.values())
    
    # Colores por nivel de concentración
    color_map = {
        'Excelente': '#10B981',
        'Alto': '#34D399',
        'Medio': '#F59E0B',
        'Bajo': '#F97316',
        'Muy bajo': '#EF4444'
    }
    
    colors = [color_map.get(label, '#94A3B8') for label in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker_colors=colors,
        textinfo='label+percent'
    )])
    
    fig.update_layout(
        title=dict(
            text='🎯 Distribución de Concentración',
            x=0.5,
            font=dict(size=18)
        ),
        height=350,
        paper_bgcolor='#F9FAFB'
    )
    
    return fig


def create_topic_frequency(sessions: List[Dict]) -> go.Figure:
    """
    Crear gráfico de barras con los temas más frecuentes.
    
    Args:
        sessions: Lista de sesiones
        
    Returns:
        go.Figure: Gráfico de barras horizontal
    """
    if not sessions:
        return _create_empty_chart("No hay datos disponibles")
    
    topics = [s.get('topic', 'Sin tema') for s in sessions]
    topic_counts = Counter(topics)
    
    # Obtener top 10 temas más frecuentes
    top_topics = topic_counts.most_common(10)
    
    if not top_topics:
        return _create_empty_chart("No hay temas registrados")
    
    labels = [item[0] for item in top_topics]
    values = [item[1] for item in top_topics]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=values,
        y=labels,
        orientation='h',
        marker_color='#4F46E5',
        text=values,
        textposition='outside'
    ))
    
    fig.update_layout(
        title=dict(
            text='🔤 Temas Más Estudiatedos',
            x=0.5,
            font=dict(size=18)
        ),
        xaxis_title='Frecuencia',
        yaxis_title='',
        plot_bgcolor='white',
        paper_bgcolor='#F9FAFB',
        height=400,
        yaxis=dict(autorange='reversed')
    )
    
    return fig


def create_balance_chart(sessions: List[Dict]) -> go.Figure:
    """
    Crear gráfico que muestre el balance entre Data Analytics y Physics.
    
    Args:
        sessions: Lista de sesiones
        
    Returns:
        go.Figure: Gráfico de barras apiladas
    """
    if not sessions:
        return _create_empty_chart("No hay datos disponibles")
    
    # Categorizar sesiones
    data_categories = ['Data Analysis', 'SQL', 'Statistics', 'Visualization']
    physics_categories = ['Physics']
    
    data_count = sum(1 for s in sessions if s.get('category') in data_categories)
    physics_count = sum(1 for s in sessions if s.get('category') in physics_categories)
    other_count = len(sessions) - data_count - physics_count
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['Categorías'],
        y=[data_count],
        name='📊 Data Analytics',
        marker_color='#4F46E5'
    ))
    
    fig.add_trace(go.Bar(
        x=['Categorías'],
        y=[physics_count],
        name='⚛️ Physics',
        marker_color='#10B981'
    ))
    
    if other_count > 0:
        fig.add_trace(go.Bar(
            x=['Categorías'],
            y=[other_count],
            name='📚 Otros',
            marker_color='#94A3B8'
        ))
    
    fig.update_layout(
        title=dict(
            text='⚖️ Balance Data Analytics vs Physics',
            x=0.5,
            font=dict(size=18)
        ),
        yaxis_title='Número de Sesiones',
        barmode='stack',
        plot_bgcolor='white',
        paper_bgcolor='#F9FAFB',
        height=350
    )
    
    return fig


def _create_empty_chart(message: str) -> go.Figure:
    """
    Crear gráfico vacío con mensaje.
    
    Args:
        message: Mensaje a mostrar
        
    Returns:
        go.Figure: Gráfico vacío
    """
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16, color='#6B7280')
    )
    fig.update_layout(
        paper_bgcolor='#F9FAFB',
        plot_bgcolor='white',
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False),
        height=300
    )
    return fig

