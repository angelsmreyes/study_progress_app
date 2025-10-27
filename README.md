# 📚 Study Tracker 100 Days

Una aplicación completa de Streamlit para tracking de sesiones de estudio durante 100 días, diseñada específicamente para data analysts y físicos en preparación para maestría.

## 🎯 Características

- **📊 Dashboard Interactivo**: Visualiza tu progreso con métricas en tiempo real
- **➕ Registro Detallado**: Captura información completa de cada sesión (categoría, tema, victoria del día, aprendizajes, recursos, etc.)
- **📱 Generación de Contenido**: Genera posts para redes sociales y artículos para Medium automáticamente
- **📈 Visualizaciones**: Gráficos interactivos con Plotly (progreso temporal, distribución por categoría, dificultad, concentración, etc.)
- **🤝 Accountability Partner**: Sistema de detección de procrastinación con estrategias específicas
- **📝 Historial Filtrable**: Busca y ordena tus sesiones por diferentes criterios
- **🎨 Diseño ADHD-Friendly**: Colores vibrantes, espaciado generoso, emojis guía visual, feedback inmediato

## 🚀 Deployment en Streamlit Cloud

### Paso 1: Crear Repositorio en GitHub

1. Ve a [GitHub](https://github.com) e inicia sesión
2. Haz clic en el botón verde "New" (o ve a github.com/new)
3. Nombra tu repositorio: `study-tracker-100days`
4. Opcional: marca "Add a README file"
5. Haz clic en "Create repository"

### Paso 2: Subir Archivos al Repositorio

#### Opción A: Usando GitHub Desktop (Recomendado para principiantes)

1. Descarga e instala [GitHub Desktop](https://desktop.github.com/)
2. Abre GitHub Desktop e inicia sesión
3. Clic en "Clone" en GitHub Desktop
4. Selecciona el repo `study-tracker-100days` y clic en "Clone"
5. Copia todos los archivos del proyecto a la carpeta clonada
6. En GitHub Desktop, verás los archivos como "changes"
7. Haz clic en "Commit to main" con mensaje "Initial commit"
8. Clic en "Push origin" para subir a GitHub

#### Opción B: Usando Git en Terminal

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/study-tracker-100days.git

# Navegar al directorio
cd study-tracker-100days

# Añadir todos los archivos
git add .

# Hacer commit
git commit -m "Initial commit"

# Subir a GitHub
git push origin main
```

### Paso 3: Deploy en Streamlit Cloud

1. Ve a [Streamlit Cloud](https://share.streamlit.io/)
2. Haz clic en "Sign in" y autoriza con tu cuenta de GitHub
3. Haz clic en "New app"
4. Selecciona tu repositorio: `study-tracker-100days`
5. Deja la rama en `main` (o `master`)
6. El archivo principal debería detectarse automáticamente como `app.py`
7. Haz clic en "Deploy"
8. ¡Espera 1-2 minutos mientras Streamlit Cloud construye tu app!

### Paso 4: Acceder a tu Aplicación

Una vez deployada, Streamlit Cloud te dará una URL como:
```
https://TU_APP_NAME.streamlit.app
```

¡Guarda esta URL para acceder a tu app desde cualquier dispositivo!

## 📦 Instalación Local (Opcional)

Si quieres correr la aplicación localmente:

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/study-tracker-100days.git

# Navegar al directorio
cd study-tracker-100days

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

La app estará disponible en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
study-tracker-100days/
├── app.py                      # Aplicación principal
├── requirements.txt            # Dependencias
├── .gitignore                 # Archivos ignorados en Git
├── README.md                  # Este archivo
├── .streamlit/
│   └── config.toml           # Configuración de Streamlit
└── utils/
    ├── __init__.py
    ├── data_manager.py        # Manejo de datos JSON
    ├── content_generator.py   # Generación de posts y artículos
    └── visualizations.py      # Visualizaciones con Plotly
```

## 🔧 Configuración

### Persistencia de Datos

Los datos se guardan en `study_sessions.json`. Esto funciona bien para uso personal, pero recuerda:

- **⚠️ Importante**: Los datos se guardan localmente en tu máquina cuando corres la app localmente
- **⚠️ En Streamlit Cloud**: Los datos NO persisten entre reinicios (cada vez que la app se apaga, pierdes los datos)
- **💡 Solución**: Usa una base de datos en la nube (PostgreSQL en Railway, MongoDB Atlas, etc.) para producción

### Backup de Datos

Para hacer backup de tus sesiones:

1. Descarga el archivo `study_sessions.json` manualmente desde la app
2. O usa Git para hacer versionado de tus datos:
   ```bash
   git add study_sessions.json
   git commit -m "Backup de sesiones"
   git push
   ```

## 🎨 Personalización

### Cambiar Colores

Edita `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#4F46E5"           # Color primario
backgroundColor = "#F9FAFB"        # Fondo principal
secondaryBackgroundColor = "#FFFFFF" # Fondo secundario
textColor = "#1F2937"              # Color de texto
```

### Agregar Categorías

Edita `app.py`, busca la línea con `st.selectbox` para categoría y agrega tus opciones:

```python
category = st.selectbox(
    "Categoría (*)",
    ["Data Analysis", "Physics", "Statistics", "SQL", "Visualization", "Mixed", "TU_CATEGORIA"]
)
```

## 🐛 Troubleshooting

### Error al cargar datos

**Problema**: "Error al cargar sesiones: ..."

**Solución**: 
- Verifica que `study_sessions.json` exista (se crea automáticamente en la primera sesión)
- Si hay un archivo corrupto, renómbralo a `study_sessions_backup.json` y la app creará uno nuevo

### La app no despliega en Streamlit Cloud

**Problema**: Error en el deployment

**Solución**:
1. Verifica que `app.py` esté en la raíz del repositorio
2. Verifica que `requirements.txt` tenga todas las dependencias necesarias
3. Revisa los logs en Streamlit Cloud para ver el error específico

### Los datos no persisten en Streamlit Cloud

**Problema**: Pierdo mis sesiones cada vez que uso la app

**Solución**: Esto es normal. Streamlit Cloud recrea el contenedor cada vez. Para solución permanente:
1. Integra con base de datos (PostgreSQL, MongoDB)
2. Usa Google Sheets API
3. Guarda en un archivo compartido en Google Drive

### No se muestran los gráficos

**Problema**: Los gráficos aparecen vacíos o con error

**Solución**:
1. Verifica que tengas datos registrados (al menos 1 sesión)
2. Actualiza las dependencias: `pip install --upgrade plotly`
3. Limpia caché de Streamlit: `streamlit cache clear`

## 💡 Uso de la Aplicación

### Registrar Nueva Sesión

1. Haz clic en "➕ Nueva Sesión" en el menú lateral
2. Completa los campos obligatorios (marcados con *)
3. Opcional: completa campos adicionales para un registro más rico
4. Haz clic en "💾 Guardar Sesión"
5. ¡Celebra tu progreso! (los balloons aparecerán automáticamente)

### Generar Post para Redes Sociales

1. Ve a "📝 Historial"
2. Expande la sesión que quieres compartir
3. Haz clic en "📱 Generar Post Social"
4. Copia el texto que aparece
5. Pega en Twitter, LinkedIn, etc.

### Generar Artículo para Medium

1. Ve a "📝 Historial"
2. Expande la sesión deseada
3. Haz clic en "📄 Generar Artículo Medium"
4. Haz clic en "📥 Descargar .md"
5. Abre el archivo en tu editor y personaliza
6. Publica en Medium (formato ya listo en Markdown)

### Usar el Accountability Partner

1. Ve a "🤝 Accountability Partner"
2. Lee el diagnóstico de procrastinación (si aplica)
3. Selecciona razones por las que no has estudiado
4. Sigue las estrategias específicas que aparecen
5. Revisa tus patrones de estudio en los gráficos

## 🎯 Funcionalidades Detalladas

### Dashboard Principal

- **Contador de progreso**: X/100 días completados
- **Barra de progreso**: Visual intuitivo del avance
- **Racha actual**: Días consecutivos estudiando
- **Total de horas**: Tiempo acumulado de estudio
- **Último estudio**: Días transcurridos desde la última sesión
- **Alertas inteligentes**: Sistema de colores (verde/amarillo/rojo)

### Sistema de Hitos

La app celebra automáticamente cuando alcanzas:
- 🎉 **Día 10**: Primer hito
- 🎊 **Día 25**: Cuarto del camino
- 🏆 **Día 50**: Mitad del desafío
- 🔥 **Día 75**: Recta final
- 🎉🎉🎉 **Día 100**: ¡COMPLETADO!

### Visualizaciones Disponibles

1. **Progreso en el tiempo**: Línea temporal de días completados
2. **Distribución por día de semana**: Identifica tus días más productivos
3. **Distribución por categoría**: Balance entre diferentes áreas
4. **Distribución de dificultad**: Qué tan retador ha sido tu camino
5. **Distribución de concentración**: Nivel de enfoque promedio
6. **Balance Data vs Physics**: Balance entre análisis de datos y física
7. **Temas más estudiados**: Top 10 temas más frecuentes

## 📝 Ejemplo de Uso

### Sesión 1: Variables de entorno
```
Fecha: 2025-01-15
Categoría: Data Analysis
Tema: Configuración de variables de entorno en Python
Duración: 45 minutos
Victoria del día: Configuré mi primer .env y lo conecté con la API
Aprendizajes: Usar dotenv para cargar variables, nunca commitear .env
Dificultad: Fácil
Concentración: Alta
```

### Sesión 2: Window Functions en SQL
```
Fecha: 2025-01-16
Categoría: SQL
Tema: Window Functions - OVER(), PARTITION BY, ROW_NUMBER()
Duración: 2 horas
Victoria del día: Finalmente entendí la diferencia entre LAG y LEAD
Aprendizajes: Las window functions no reducen filas, solo calculan por partición
Dificultad: Difícil
Concentración: Excelente
Recursos: Mode Analytics tutorial, PostgreSQL docs
```

## 🤝 Contribuir

Este es un proyecto personal, pero siéntete libre de:
- Fork el repositorio
- Crear una rama para tu versión
- Agregar nuevas características
- Hacer pull requests

## 📄 Licencia

Este proyecto está bajo Licencia MIT. Siéntete libre de usarlo, modificarlo y distribuirlo.

## 🎓 Sobre el Autor

Un físico trabajando como Data Analyst, preparándose para una maestría mientras documenta el aprendizaje continuo.

**Conecta conmigo en:**
- Twitter: [@TU_USUARIO](https://twitter.com)
- LinkedIn: [Tu Perfil](https://linkedin.com/in/TU_PERFIL)
- Medium: [@TU_USUARIO](https://medium.com/@TU_USUARIO)

## 🌟 Agradecimientos

- Streamlit por la plataforma increíble
- Plotly por las visualizaciones hermosas e interactivas
- La comunidad open source

---

**¡Feliz aprendizaje y que cumplas los 100 días! 🎉**

