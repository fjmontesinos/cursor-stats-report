# 🤖 Cursor AI Analytics - Generador de Informes

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Pandas](https://img.shields.io/badge/pandas-required-orange.svg)](https://pandas.pydata.org/)

Herramienta para generar informes completos de adopción y productividad de Cursor AI en equipos de desarrollo con **análisis comparativo temporal automático**.

## 📋 Descripción

Este proyecto analiza los datos de uso de Cursor AI y genera informes HTML interactivos con métricas de productividad, adopción y análisis estratégico. Diseñado específicamente para equipos de desarrollo que quieren:

- 🚀 **Potenciar el uso** de Cursor AI dentro del equipo
- 📊 **Compartir información** que anime y dé visibilidad del impacto
- 💼 **Informar a directivos** sobre la implantación de IA en desarrollo
- 🔄 **Análisis comparativo** automático entre períodos temporales
- 👥 **Seguimiento de cohortes** de usuarios para retención y adopción

## ✨ Características Principales

- 📈 **Informes HTML interactivos** con gráficos Chart.js
- 🎨 **Diseño responsive** optimizado para intranet corporativa
- 🧭 **Menú desplegable** con navegación rápida a todas las secciones
- 🌍 **Formato numérico español** (punto para miles, coma para decimales)
- 📱 **Adaptativo** para desktop, tablet y móvil (4/3/2/1 columnas)
- 🔄 **Sistema de plantillas** para fácil personalización
- ⚡ **Procesamiento automático** de archivos CSV de Cursor Analytics
- 🎯 **Estructura optimizada** con resumen ejecutivo antes de recomendaciones

## 🆕 Análisis Comparativo Temporal

### División Automática de Períodos
- **Enfoque innovador**: Un solo CSV con el doble de días necesarios
- **División inteligente**: Primera mitad como período de referencia, segunda mitad como período actual
- **Ejemplos prácticos**:
  - Para analizar últimos 15 días: CSV de 30 días
  - Para analizar última semana: CSV de 14 días
  - Para analizar último mes: CSV de 60 días
- **División entera**: Días impares se dividen automáticamente (ej: 31 días = 15 actuales vs 16 anteriores)

### Indicadores Comparativos
- **📈 Crecimiento**: Variaciones positivas con porcentaje
- **📉 Decrecimiento**: Variaciones negativas con porcentaje
- **➖ Estabilidad**: Cambios menores al 1%
- **🆕 Nuevos**: Métricas que aparecen por primera vez

### Análisis de Cohortes de Usuarios
- **👥 Usuarios Consistentes**: Activos en ambos períodos
- **🆕 Usuarios Nuevos**: Completamente nuevos en el sistema
- **🔄 Usuarios Reactivados**: Volvieron después de estar inactivos
- **😴 Usuarios Perdidos**: Dejaron de usar la herramienta
- **📊 Tasa de Retención**: Porcentaje de continuidad de usuarios

## 📊 Métricas Generadas

### 🎯 KPIs Principales con Comparación Temporal
**Primera fila - Métricas de Efectividad:**
- **Líneas de Código IA**: Total generadas con indicador de variación
- **% Aceptación Líneas**: Porcentaje con tendencia comparativa
- **Tabs Aceptados**: Total con evolución temporal
- **% Aceptación Tabs**: Porcentaje con análisis de cambio

**Segunda fila - Métricas Generales:**
- **Peticiones Totales**: Interacciones con indicador de crecimiento
- **Promedio Líneas/Usuario**: Productividad individual comparada
- **Tasa de Adopción**: Evolución de usuarios activos
- **Usuarios Inactivos**: Seguimiento de usuarios en riesgo

### 🔍 Textos Dinámicos Contextuales
- **Textos adaptativos**: Cada KPI tiene descripciones que cambian según los valores reales
- **Umbrales inteligentes**: Clasificación automática (Alto/Medio/Bajo) basada en datos
- **Ejemplos contextuales**:
  - "Alta productividad - más de 50K líneas"
  - "Excelente calidad - sugerencias muy relevantes"
  - "Adopción masiva - más del 80% activos"
  - "Dominio tecnológico - gran diversidad"

### 👥 Análisis de Cohortes (5 KPIs en fila horizontal)
- **Usuarios Consistentes**: Intersección de períodos
- **Usuarios Nuevos**: Incorporaciones al sistema
- **Usuarios Reactivados**: Recuperación de usuarios
- **Usuarios Perdidos**: Abandono temporal
- **Tasa de Retención**: Métrica clave de continuidad

### 📈 Análisis Temporal Avanzado
- **Evolución de Líneas**: Gráfico diario con comparación de períodos
- **Evolución de Tabs**: Tendencias de autocompletado
- **Usuarios Activos**: Patrones de adopción temporal
- **Identificación de Tendencias**: Picos, valles y patrones estacionales

### 🏆 Rankings y Estadísticas
- **Top 10 Campeones de Productividad**: Usuarios con más líneas aceptadas
- **Top 10 Power Users**: Usuarios con más peticiones a IA
- **Tecnologías Más Utilizadas**: Lenguajes donde más impacta la IA (27 extensiones con colores)
- **Modelos de IA Preferidos**: Distribución de uso por modelo (gráfico circular)
- **Versiones de Cliente**: Análisis de versions de Cursor utilizadas

### 💡 Insights Estratégicos Automáticos
- **Análisis de productividad**: Evaluación automática de métricas clave
- **Tendencias de adopción**: Identificación de patrones de crecimiento
- **Calidad de sugerencias**: Análisis de tasas de aceptación
- **Diversidad tecnológica**: Evaluación del alcance de la IA
- **Recomendaciones contextuales**: Sugerencias basadas en los datos

### 🎯 Resumen Ejecutivo
**Estructura optimizada para dirección:**
- **🚀 Adopción Excepcional**: Análisis comparativo de tasa de adopción
- **🔬 Innovación Tecnológica**: Diversificación de modelos y experimentación
- **📊 Impacto Mensurable**: Calidad de sugerencias y productividad real
- **📈 Evolución Temporal**: Tendencias y cambios significativos

## 🧭 Navegación Mejorada

### Menú Desplegable Interactivo
- **Botón flotante** en esquina superior derecha
- **Acceso directo** a todas las secciones del informe
- **Múltiples formas de cerrar**: clic fuera, tecla Escape, clic en enlace
- **Diseño moderno** con efectos glassmorphism y animaciones suaves
- **Responsive** para todos los dispositivos

### Secciones Navegables
- 📊 KPIs Comparativos
- 👥 Análisis de Cohortes
- 💡 Insights Estratégicos
- 📈 Evolución Temporal  
- 🔄 Evolución Tabs
- 👥 Análisis Equipos
- 💻 Tecnologías
- 🧠 Modelos IA
- ⚠️ Usuarios Inactivos
- 🎯 Resumen Ejecutivo
- ✅ Recomendaciones

## 🚀 Instalación

### Requisitos
- Python 3.7+
- pandas
- Archivo CSV de Cursor Analytics con **el doble de días** del período a analizar

### Instalar dependencias
```bash
pip install pandas
```

## 📖 Uso

### Comando Básico
```bash
python generador_informe_template.py archivo_cursor_analytics.csv
```

### Ejemplos de Uso Temporal
```bash
# Analizar últimos 15 días (requiere CSV de 30 días)
python generador_informe_template.py cursor_analytics_30_dias.csv

# Analizar última semana (requiere CSV de 14 días)
python generador_informe_template.py cursor_analytics_14_dias.csv

# Analizar último mes (requiere CSV de 60 días)
python generador_informe_template.py cursor_analytics_60_dias.csv
```

### Opciones Avanzadas
```bash
# Especificar archivo de salida personalizado
python generador_informe_template.py datos.csv --salida mi_informe.html

# Usar plantilla personalizada
python generador_informe_template.py datos.csv --plantilla mi_plantilla.html

# Ejemplo completo
python generador_informe_template.py cursor_analytics_2025.csv \
  --salida informe_enero_2025.html \
  --plantilla plantilla_corporativa.html
```

### Ayuda
```bash
python generador_informe_template.py --help
```

## 📁 Estructura del Proyecto

```
cursor-stats-report/
├── README.md                          # Documentación principal
├── CHANGELOG.md                       # Historial de cambios
├── LICENSE                            # Licencia MIT
├── .gitignore                         # Archivos ignorados por Git
├── generador_informe_template.py      # Script principal con análisis comparativo
├── cursor_stats_report_ux.html        # Plantilla HTML con diseño UX y comparación temporal
└── cursor_analytics_*.csv             # Datos de entrada (doble de días necesarios)
```

## 🎨 Personalización

### Modificar el Diseño
Edita `cursor_stats_report_ux.html` para personalizar:
- Colores corporativos
- Logotipos y branding
- Estructura del layout
- Estilos CSS del menú desplegable
- Diseño de indicadores comparativos

### Placeholders Disponibles
La plantilla utiliza estos placeholders que se reemplazan automáticamente:

#### Placeholders Temporales
| Placeholder | Descripción |
|-------------|-------------|
| `{{PERIODO_ANTERIOR_INICIO}}` | Fecha de inicio del período anterior |
| `{{PERIODO_ANTERIOR_FIN}}` | Fecha de fin del período anterior |
| `{{PERIODO_ACTUAL_INICIO}}` | Fecha de inicio del período actual |
| `{{PERIODO_ACTUAL_FIN}}` | Fecha de fin del período actual |

#### Placeholders de KPIs con Comparación
| Placeholder | Descripción |
|-------------|-------------|
| `{{LINEAS_ACEPTADAS}}` | Líneas de código aceptadas período actual |
| `{{LINEAS_ACEPTADAS_INDICADOR}}` | Indicador comparativo (📈 +X%, 📉 -X%) |
| `{{TASA_ACEPTACION}}` | Porcentaje de aceptación período actual |
| `{{TASA_ACEPTACION_INDICADOR}}` | Indicador comparativo de aceptación |
| `{{TABS_ACEPTADOS}}` | Tabs aceptados período actual |
| `{{TABS_ACEPTADOS_INDICADOR}}` | Indicador comparativo de tabs |

#### Placeholders de Cohortes
| Placeholder | Descripción |
|-------------|-------------|
| `{{USUARIOS_CONSISTENTES}}` | Usuarios activos en ambos períodos |
| `{{USUARIOS_NUEVOS}}` | Usuarios completamente nuevos |
| `{{USUARIOS_REACTIVADOS}}` | Usuarios que volvieron |
| `{{USUARIOS_PERDIDOS}}` | Usuarios que dejaron de usar |
| `{{TASA_RETENCION}}` | Porcentaje de retención |

#### Placeholders de Textos Dinámicos
| Placeholder | Descripción |
|-------------|-------------|
| `{{TEXTO_LINEAS_CODIGO}}` | Texto contextual para líneas de código |
| `{{TEXTO_ACEPTACION_LINEAS}}` | Texto contextual para tasa de aceptación |
| `{{TEXTO_TABS_ACEPTADOS}}` | Texto contextual para tabs |
| `{{TEXTO_PETICIONES}}` | Texto contextual para peticiones |

## 📊 Formato de Datos de Entrada

### Requisitos del CSV
El script espera un CSV de Cursor Analytics con **el doble de días** del período a analizar:

**Columnas principales requeridas:**
- `Date`: Fecha del registro (formato YYYY-MM-DD)
- `Email`: Email del usuario
- `Is Active`: Estado de actividad (True/False)
- `Chat Accepted Lines Added`: Líneas aceptadas
- `Chat Suggested Lines Added`: Líneas sugeridas
- `Tabs Accepted`: Tabs de autocompletado aceptados
- `Chat Tabs Shown`: Tabs mostrados al usuario
- `Most Used Tab Extension`: Extensión más utilizada
- `Most Used Model`: Modelo de IA más usado
- `Client Version`: Versión del cliente
- Columnas de peticiones: `Edit Requests`, `Ask Requests`, etc.

### Ejemplo de Estructura Temporal
```
Fecha        | Usuario | Líneas | Tabs | ...
2024-05-26   | user1   | 150    | 25   | ... (Período anterior)
2024-05-27   | user2   | 200    | 30   | ... (Período anterior)
...
2024-06-09   | user1   | 180    | 28   | ... (Período anterior)
2024-06-10   | user1   | 220    | 35   | ... (Período actual)
2024-06-11   | user2   | 190    | 32   | ... (Período actual)
...
2024-06-25   | user3   | 240    | 40   | ... (Período actual)
```

## 🎯 Casos de Uso

### Para Equipos de Desarrollo
- **Comparar evolución**: Ver cómo ha mejorado la productividad
- **Identificar tendencias**: Detectar patrones de adopción
- **Seguir cohortes**: Monitorear retención de usuarios
- **Motivar adopción**: Mostrar impacto real con datos comparativos

### Para Managers y CTOs
- **Medir ROI temporal**: Evolución de la inversión en IA
- **Planificar expansión**: Basado en tendencias de crecimiento
- **Identificar riesgos**: Usuarios perdidos y en riesgo
- **Reportar progreso**: Métricas comparativas para dirección

### Para Recursos Humanos
- **Programas de retención**: Basados en análisis de cohortes
- **Formación dirigida**: Para usuarios nuevos y reactivados
- **Seguimiento de impacto**: Evolución de productividad individual
- **Planificación de recursos**: Basada en tendencias de adopción

## 🔧 Funcionalidades Técnicas

### División Automática de Períodos
```python
def dividir_periodos_temporales(df):
    """
    Divide automáticamente el DataFrame en dos períodos:
    - Primera mitad: período anterior (referencia)
    - Segunda mitad: período actual (análisis)
    """
    # Implementación con división entera y ordenación temporal
```

### Análisis de Cohortes
```python
def analizar_cohortes_usuarios(df_anterior, df_actual):
    """
    Clasifica usuarios en cohortes:
    - Consistentes: Activos en ambos períodos
    - Nuevos: Solo en período actual
    - Reactivados: Volvieron después de inactividad
    - Perdidos: Solo en período anterior
    """
```

### Textos Dinámicos
```python
def generar_textos_alternativos_kpis(metricas):
    """
    Genera textos contextuales basados en valores reales:
    - Umbrales inteligentes para clasificación
    - Descripciones adaptativas por métrica
    - Contexto relevante para cada KPI
    """
```

---

**📊 Cursor AI Analytics** - Transformando equipos de desarrollo con análisis comparativo temporal desde 2025 