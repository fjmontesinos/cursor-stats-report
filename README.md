# 🤖 Cursor AI Analytics - Generador de Informes

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Pandas](https://img.shields.io/badge/pandas-required-orange.svg)](https://pandas.pydata.org/)

Herramienta para generar informes completos de adopción y productividad de Cursor AI en equipos de desarrollo con **análisis comparativo temporal automático**.

## � Documentación Adicional

📁 **Carpeta `doc/`**: Documentación completa del proyecto y plan de migración a Firebase:
- [`doc/resumen_repositorio.md`](doc/resumen_repositorio.md) - Análisis detallado del proyecto actual
- [`doc/plan_implementacion_firebase.md`](doc/plan_implementacion_firebase.md) - Plan completo de migración a Firebase
- [`doc/guia_rapida.md`](doc/guia_rapida.md) - Comandos y referencias rápidas
- [`doc/archivos_creados.md`](doc/archivos_creados.md) - Índice de toda la documentación

## �📋 Descripción

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
- Archivo CSV de Cursor Analytics (modo automático: doble de días del período a analizar)
- Para fechas personalizadas: CSV que contenga todas las fechas especificadas

### Instalar dependencias
```bash
pip install pandas
```

## 📖 Uso

### Modo Automático (División Automática)
```bash
# Comando básico - divide automáticamente el CSV en dos períodos
python generador_informe_template.py archivo_cursor_analytics.csv
```

### Modo Manual (Fechas Personalizadas) 🆕
```bash
# Especificar fechas exactas para análisis personalizado
python generador_informe_template.py archivo_cursor_analytics.csv \
  --fecha-inicio-actual 2025-06-16 \
  --fecha-fin-actual 2025-06-29 \
  --fecha-inicio-anterior 2025-06-02 \
  --fecha-fin-anterior 2025-06-15
```

### Ejemplos de Uso Temporal

#### División Automática
```bash
# Analizar últimos 15 días (requiere CSV de 30 días)
python generador_informe_template.py cursor_analytics_30_dias.csv

# Analizar última semana (requiere CSV de 14 días)
python generador_informe_template.py cursor_analytics_14_dias.csv

# Analizar último mes (requiere CSV de 60 días)
python generador_informe_template.py cursor_analytics_60_dias.csv
```

#### Fechas Personalizadas 🆕
```bash
# Comparar segunda quincena de junio vs primera quincena
python generador_informe_template.py cursor_analytics.csv \
  --fecha-inicio-actual 2025-06-16 \
  --fecha-fin-actual 2025-06-30 \
  --fecha-inicio-anterior 2025-06-01 \
  --fecha-fin-anterior 2025-06-15 \
  --salida informe_quincenas_junio.html

# Comparar último trimestre vs trimestre anterior
python generador_informe_template.py cursor_analytics.csv \
  --fecha-inicio-actual 2025-04-01 \
  --fecha-fin-actual 2025-06-30 \
  --fecha-inicio-anterior 2025-01-01 \
  --fecha-fin-anterior 2025-03-31 \
  --salida comparativa_trimestres.html

# Análisis de sprint específico vs sprint anterior
python generador_informe_template.py cursor_analytics.csv \
  --fecha-inicio-actual 2025-06-16 \
  --fecha-fin-actual 2025-06-29 \
  --fecha-inicio-anterior 2025-06-02 \
  --fecha-fin-anterior 2025-06-15 \
  --salida sprint_comparison.html \
  --verbose
```

### Opciones de Línea de Comandos

#### Parámetros Básicos
| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `archivo_csv` | **(Obligatorio)** Archivo CSV con datos de Cursor | `cursor_analytics.csv` |
| `--salida` o `-o` | Archivo HTML de salida | `--salida mi_informe.html` |
| `--plantilla` o `-t` | Plantilla HTML personalizada | `--plantilla mi_plantilla.html` |
| `--verbose` o `-v` | Logging detallado para debugging | `--verbose` |

#### Parámetros de Fechas Personalizadas 🆕
| Parámetro | Descripción | Formato | Ejemplo |
|-----------|-------------|---------|---------|
| `--fecha-inicio-actual` | Fecha inicio período actual | YYYY-MM-DD | `2025-06-16` |
| `--fecha-fin-actual` | Fecha fin período actual | YYYY-MM-DD | `2025-06-29` |
| `--fecha-inicio-anterior` | Fecha inicio período anterior | YYYY-MM-DD | `2025-06-02` |
| `--fecha-fin-anterior` | Fecha fin período anterior | YYYY-MM-DD | `2025-06-15` |

#### Reglas de Fechas Personalizadas
- **Todas las 4 fechas requeridas**: Si usas una fecha personalizada, debes especificar las 4
- **Formato obligatorio**: YYYY-MM-DD (año-mes-día)
- **Fechas existentes**: Las fechas deben existir en tu archivo CSV
- **Sin solapamiento**: Los períodos no pueden solaparse entre sí

### Opciones Avanzadas
```bash
# Ejemplo completo con todas las opciones
python generador_informe_template.py cursor_analytics_2025.csv \
  --fecha-inicio-actual 2025-06-01 \
  --fecha-fin-actual 2025-06-30 \
  --fecha-inicio-anterior 2025-05-01 \
  --fecha-fin-anterior 2025-05-31 \
  --salida informe_junio_vs_mayo.html \
  --plantilla plantilla_corporativa.html \
  --verbose
```

### Ayuda y Documentación
```bash
# Ver todas las opciones disponibles
python generador_informe_template.py --help

# Ejemplo de salida de ayuda
usage: generador_informe_template.py [-h] [--salida SALIDA] [--plantilla PLANTILLA] [--verbose]
                                      [--fecha-inicio-actual FECHA_INICIO_ACTUAL]
                                      [--fecha-fin-actual FECHA_FIN_ACTUAL]
                                      [--fecha-inicio-anterior FECHA_INICIO_ANTERIOR]
                                      [--fecha-fin-anterior FECHA_FIN_ANTERIOR]
                                      archivo_csv
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
- **🆕 Análisis de sprints**: Comparar sprints específicos con fechas exactas
- **🆕 Evaluación de releases**: Impacto antes/después de nuevas versiones

### Para Managers y CTOs
- **Medir ROI temporal**: Evolución de la inversión en IA
- **Planificar expansión**: Basado en tendencias de crecimiento
- **Identificar riesgos**: Usuarios perdidos y en riesgo
- **Reportar progreso**: Métricas comparativas para dirección
- **🆕 Análisis trimestral**: Comparativas exactas entre trimestres
- **🆕 Evaluación de objetivos**: Seguimiento de KPIs en períodos específicos

### Para Recursos Humanos
- **Programas de retención**: Basados en análisis de cohortes
- **Formación dirigida**: Para usuarios nuevos y reactivados
- **Seguimiento de impacto**: Evolución de productividad individual
- **Planificación de recursos**: Basada en tendencias de adopción
- **🆕 Evaluaciones de desempeño**: Períodos específicos de evaluación
- **🆕 Onboarding tracking**: Seguimiento de nuevos empleados en fechas exactas

### Casos de Uso Específicos con Fechas Personalizadas 🆕

#### Análisis de Sprints Ágiles
```bash
# Sprint 12 vs Sprint 11 (2 semanas cada uno)
python generador_informe_template.py cursor_analytics.csv \
  --fecha-inicio-actual 2025-06-16 --fecha-fin-actual 2025-06-29 \
  --fecha-inicio-anterior 2025-06-02 --fecha-fin-anterior 2025-06-15 \
  --salida sprint_12_vs_11.html
```

#### Comparativa de Trimestres
```bash
# Q2 2025 vs Q1 2025
python generador_informe_template.py cursor_analytics.csv \
  --fecha-inicio-actual 2025-04-01 --fecha-fin-actual 2025-06-30 \
  --fecha-inicio-anterior 2025-01-01 --fecha-fin-anterior 2025-03-31 \
  --salida Q2_vs_Q1_2025.html
```

#### Análisis Pre/Post Implementación
```bash
# 30 días después de implementar Cursor vs 30 días antes
python generador_informe_template.py cursor_analytics.csv \
  --fecha-inicio-actual 2025-06-01 --fecha-fin-actual 2025-06-30 \
  --fecha-inicio-anterior 2025-04-01 --fecha-fin-anterior 2025-04-30 \
  --salida impacto_implementacion.html
```

#### Evaluación de Vacaciones/Festivos
```bash
# Comparar productividad en períodos laborales vs períodos con festivos
python generador_informe_template.py cursor_analytics.csv \
  --fecha-inicio-actual 2025-06-01 --fecha-fin-actual 2025-06-15 \
  --fecha-inicio-anterior 2025-05-01 --fecha-fin-anterior 2025-05-15 \
  --salida productividad_sin_festivos.html
```

#### Análisis de Equipos Específicos
```bash
# Comparar antes/después de formación en IA para el equipo
python generador_informe_template.py cursor_analytics.csv \
  --fecha-inicio-actual 2025-06-15 --fecha-fin-actual 2025-06-30 \
  --fecha-inicio-anterior 2025-06-01 --fecha-fin-anterior 2025-06-14 \
  --salida post_formacion_ia.html
```

## 🔧 Funcionalidades Técnicas

### Doble Modo de Operación 🆕

#### Modo Automático (División Automática)
```python
def dividir_periodos_temporales(df):
    """
    Divide automáticamente el DataFrame en dos períodos:
    - Primera mitad: período anterior (referencia)
    - Segunda mitad: período actual (análisis)
    """
    # Implementación con división entera y ordenación temporal
```

#### Modo Manual (Fechas Personalizadas) 🆕
```python
def dividir_periodos_personalizados(df, fechas_personalizadas):
    """
    Divide el DataFrame usando fechas específicas:
    - Período anterior: fechas definidas por el usuario
    - Período actual: fechas definidas por el usuario
    - Validación automática de zona horaria (UTC compatible)
    """
    # Detección automática de zona horaria para compatibilidad
    tz = df['Date'].dt.tz if hasattr(df['Date'].dt, 'tz') and df['Date'].dt.tz is not None else None
    # Creación de timestamps compatibles con el DataFrame
```

### Compatibilidad de Zona Horaria 🔧
- **Detección automática**: Identifica si el CSV tiene zona horaria UTC
- **Compatibilidad total**: Funciona con CSVs con y sin zona horaria
- **Error resuelto**: Soluciona `TypeError: Invalid comparison between dtype=datetime64[ns, UTC] and Timestamp`
- **Robustez**: Manejo automático de diferentes formatos de fecha

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

### Validación de Fechas
```python
def validar_y_parsear_fechas(fecha_inicio_actual, fecha_fin_actual, fecha_inicio_anterior, fecha_fin_anterior, df):
    """
    Valida fechas personalizadas:
    - Formato YYYY-MM-DD obligatorio
    - Verificación de existencia en dataset
    - Detección de solapamiento de períodos
    - Manejo completo de errores
    """
```

---

**📊 Cursor AI Analytics** - Transformando equipos de desarrollo con análisis comparativo temporal automático y fechas personalizadas desde 2025 🚀 