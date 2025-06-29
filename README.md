# 🤖 Cursor AI Analytics - Generador de Informes

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Pandas](https://img.shields.io/badge/pandas-required-orange.svg)](https://pandas.pydata.org/)

Herramienta para generar informes completos de adopción y productividad de Cursor AI en equipos de desarrollo.

## 📋 Descripción

Este proyecto analiza los datos de uso de Cursor AI y genera informes HTML interactivos con métricas de productividad, adopción y análisis estratégico. Diseñado específicamente para equipos de desarrollo que quieren:

- 🚀 **Potenciar el uso** de Cursor AI dentro del equipo
- 📊 **Compartir información** que anime y dé visibilidad del impacto
- 💼 **Informar a directivos** sobre la implantación de IA en desarrollo

## ✨ Características

- 📈 **Informes HTML interactivos** con gráficos Chart.js
- 🎨 **Diseño responsive** optimizado para intranet corporativa
- 🧭 **Menú desplegable** con navegación rápida a todas las secciones
- 🌍 **Formato numérico español** (punto para miles, coma para decimales)
- 📱 **Adaptativo** para desktop, tablet y móvil (4/3/2/1 columnas)
- 🔄 **Sistema de plantillas** para fácil personalización
- ⚡ **Procesamiento automático** de archivos CSV de Cursor Analytics
- 🎯 **Estructura optimizada** con resumen ejecutivo antes de recomendaciones

## 📊 Métricas Generadas

### 🎯 KPIs Principales (8 métricas en 2 filas)
**Primera fila - Métricas de Efectividad:**
- **Líneas de Código IA**: Total de líneas generadas y aceptadas
- **% Aceptación Líneas**: Porcentaje de sugerencias de líneas aceptadas
- **Tabs Aceptados**: Total de sugerencias de autocompletado aceptadas
- **% Aceptación Tabs**: Porcentaje de tabs aceptados (vs líneas)

**Segunda fila - Métricas Generales:**
- **Peticiones Totales**: Interacciones totales con modelos de IA
- **Promedio Líneas/Usuario**: Líneas de código promedio por desarrollador
- **Tasa de Adopción**: Porcentaje de usuarios activos vs total
- **Usuarios Inactivos**: Número de usuarios que requieren atención

### 📈 Análisis Temporal Avanzado
- **Evolución de Líneas**: Gráfico diario con líneas aceptadas vs sugeridas
- **Evolución de Tabs**: Gráfico diario con tabs aceptados vs mostrados
- **Usuarios Activos**: Tendencia de adopción por días
- **Patrones de Uso**: Identificación de picos y tendencias

### 🏆 Rankings y Estadísticas
- **Top 10 Campeones de Productividad**: Usuarios con más líneas aceptadas
- **Top 10 Power Users**: Usuarios con más peticiones a IA
- **Tecnologías Más Utilizadas**: Lenguajes donde más impacta la IA (27 extensiones con colores)
- **Modelos de IA Preferidos**: Distribución de uso por modelo (gráfico circular)
- **Versiones de Cliente**: Análisis de versiones de Cursor utilizadas

### 🎯 Resumen Ejecutivo
**Estructura optimizada para dirección:**
- **🚀 Adopción Excepcional**: Análisis de tasa de adopción vs estándares
- **🔬 Innovación Tecnológica**: Diversificación de modelos y experimentación
- **📊 Impacto Mensurable**: Calidad de sugerencias y productividad real

### ✅ Recomendaciones Estratégicas
- **Recomendaciones Automáticas**: Basadas en los datos analizados
- **Identificación de Oportunidades**: Usuarios y áreas de mejora
- **Análisis Comparativo**: Benchmarking con estándares del sector

## 🧭 Navegación Mejorada

### Menú Desplegable Interactivo
- **Botón flotante** en esquina superior derecha
- **Acceso directo** a todas las secciones del informe
- **Múltiples formas de cerrar**: clic fuera, tecla Escape, clic en enlace
- **Diseño moderno** con efectos glassmorphism y animaciones suaves
- **Responsive** para todos los dispositivos

### Secciones Navegables
- 📊 KPIs
- 📈 Evolución Temporal  
- 🔄 Evolución Tabs
- 👥 Análisis Equipos
- 💡 Tecnologías
- 🧠 Modelos IA
- ⚠️ Usuarios Inactivos
- 🎯 Resumen Ejecutivo
- ✅ Recomendaciones

## 🚀 Instalación

### Requisitos
- Python 3.7+
- pandas
- Archivo CSV de Cursor Analytics

### Instalar dependencias
```bash
pip install pandas
```

## 📖 Uso

### Comando Básico
```bash
python generador_informe_template.py archivo_cursor_analytics.csv
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
├── generador_informe_template.py      # Script principal
├── cursor_stats_report_ux.html        # Plantilla HTML con diseño UX corporativo
└── cursor_analytics_*.csv             # Datos de entrada
```

## 🎨 Personalización

### Modificar el Diseño
Edita `cursor_stats_report.html` para personalizar:
- Colores corporativos
- Logotipos y branding
- Estructura del layout
- Estilos CSS del menú desplegable

### Placeholders Disponibles
La plantilla utiliza estos placeholders que se reemplazan automáticamente:

| Placeholder | Descripción |
|-------------|-------------|
| `{{PERIODO_INICIO}}` | Fecha de inicio del análisis |
| `{{PERIODO_FIN}}` | Fecha de fin del análisis |
| `{{TASA_ADOPCION}}` | Porcentaje de adopción |
| `{{USUARIOS_ACTIVOS}}` | Número de usuarios activos |
| `{{TOTAL_USUARIOS}}` | Total de usuarios |
| `{{LINEAS_ACEPTADAS}}` | Líneas de código aceptadas |
| `{{TASA_ACEPTACION}}` | Porcentaje de aceptación de líneas |
| `{{TABS_ACEPTADOS}}` | Total de tabs aceptados |
| `{{TASA_ACEPTACION_TABS}}` | Porcentaje de aceptación de tabs |
| `{{PETICIONES_TOTALES}}` | Total de peticiones a IA |
| `{{PROMEDIO_LINEAS}}` | Promedio de líneas por usuario |
| `{{USUARIOS_INACTIVOS}}` | Número de usuarios inactivos |
| `{{CHART_*}}` | Datos para gráficos Chart.js |

## 📊 Formato de Datos de Entrada

El script espera un CSV de Cursor Analytics con estas columnas principales:
- `Date`: Fecha del registro
- `Email`: Email del usuario
- `Is Active`: Estado de actividad
- `Chat Accepted Lines Added`: Líneas aceptadas
- `Chat Suggested Lines Added`: Líneas sugeridas
- `Tabs Accepted`: Tabs de autocompletado aceptados
- `Chat Tabs Shown`: Tabs mostrados al usuario
- `Most Used Tab Extension`: Extensión más utilizada
- `Most Used Model`: Modelo de IA más usado
- `Client Version`: Versión del cliente
- Columnas de peticiones: `Edit Requests`, `Ask Requests`, etc.

## 🎯 Casos de Uso

### Para Equipos de Desarrollo
- Identificar campeones de productividad
- Compartir mejores prácticas
- Motivar adopción entre compañeros
- Analizar tecnologías más beneficiadas
- Comparar efectividad líneas vs tabs

### Para Managers y CTOs
- Medir impacto de la inversión en IA
- Identificar usuarios que necesitan formación
- Planificar expansión de licencias
- Reportar progreso a dirección
- Analizar tendencias de adopción

### Para Recursos Humanos
- Identificar necesidades de formación
- Planificar programas de adopción
- Medir impacto en productividad
- Crear programas de incentivos

## 📄 Licencia

Este proyecto está licenciado bajo la **MIT License** - consulta el archivo [LICENSE](LICENSE) para más detalles.

### ¿Por qué MIT?
- ✅ **Uso libre**: Comercial y personal
- ✅ **Modificación permitida**: Puedes adaptar el código
- ✅ **Distribución libre**: Comparte sin restricciones
- ✅ **Sin garantías**: Uso bajo tu responsabilidad

## 🔧 Resolución de Problemas

### Error: "No module named 'pandas'"
```bash
pip install pandas
```

### Error: "FileNotFoundError"
Verifica que el archivo CSV existe y la ruta es correcta.

### Datos incorrectos en el informe
Verifica que el CSV tiene el formato esperado de Cursor Analytics.

### Gráficos no se muestran
Asegúrate de tener conexión a internet para cargar Chart.js.

### Menú desplegable no funciona
Verifica que JavaScript está habilitado en el navegador.

## 🤝 Contribución

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Realiza tus cambios
4. Envía un pull request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para más detalles.

## 📞 Soporte

Para soporte técnico o consultas:
- Crear un issue en el repositorio
- Contactar al equipo de transformación digital

## 📄 Historial de Cambios

Para ver el historial completo de cambios, consulta el archivo [CHANGELOG.md](CHANGELOG.md).

---

**🤖 Powered by Cursor AI Analytics** | Transformando equipos de desarrollo con IA 