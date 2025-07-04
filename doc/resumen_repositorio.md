# 📊 Resumen del Repositorio: Cursor AI Analytics

## 🎯 Propósito Principal

Este repositorio contiene una **herramienta de análisis de productividad para Cursor AI**, diseñada para equipos de desarrollo que quieren medir y visualizar el impacto de la inteligencia artificial en su productividad de programación.

## 🚀 Funcionalidad Central

La herramienta procesa datos exportados desde Cursor AI Analytics y genera **informes HTML interactivos** con análisis comparativo entre períodos temporales, permitiendo:

- 📈 **Análisis comparativo temporal** automático o personalizado
- 🎨 **Informes HTML responsive** con gráficos interactivos
- 👥 **Análisis de cohortes de usuarios** (nuevos, consistentes, perdidos, reactivados)
- 📊 **Métricas de productividad** y adopción detalladas
- 💡 **Insights estratégicos automáticos** basados en los datos

## 🔧 Características Técnicas

### Modos de Operación
1. **Modo Automático**: Divide automáticamente el dataset en dos períodos (primera mitad vs segunda mitad)
2. **Modo Personalizado**: Permite especificar fechas exactas para comparaciones específicas

### Métricas Principales
- **Líneas de código generadas por IA** (aceptadas vs sugeridas)
- **Tasa de aceptación** de sugerencias
- **Análisis de tabs** (autocompletado)
- **Peticiones totales** a la IA
- **Usuarios activos** y patrones de adopción
- **Tecnologías más utilizadas**
- **Modelos de IA preferidos**

### Análisis de Cohortes
- **Usuarios Consistentes**: Activos en ambos períodos
- **Usuarios Nuevos**: Completamente nuevos
- **Usuarios Reactivados**: Que volvieron después de inactividad
- **Usuarios Perdidos**: Que dejaron de usar la herramienta
- **Tasa de Retención**: Porcentaje de continuidad

## 📁 Estructura del Repositorio

```
├── generador_informe_template.py     # Script principal (1085 líneas)
├── cursor_stats_report_ux.html       # Plantilla HTML con diseño UX (1610 líneas)
├── README.md                         # Documentación completa (495 líneas)
├── CHANGELOG.md                      # Historial de cambios (630 líneas)
├── LICENSE                           # Licencia MIT
└── .gitignore                        # Archivos ignorados
```

## 🛠️ Uso

### Instalación
```bash
pip install pandas
```

### Uso Básico (Modo Automático)
```bash
python generador_informe_template.py archivo_cursor_analytics.csv
```

### Uso Avanzado (Fechas Personalizadas)
```bash
python generador_informe_template.py archivo_cursor_analytics.csv \
  --fecha-inicio-actual 2025-06-16 \
  --fecha-fin-actual 2025-06-29 \
  --fecha-inicio-anterior 2025-06-02 \
  --fecha-fin-anterior 2025-06-15 \
  --salida sprint_comparison.html
```

## 🎯 Casos de Uso Principales

### Para Equipos de Desarrollo
- Medir el impacto real de Cursor AI en la productividad
- Identificar patrones de adopción y uso
- Comparar productividad entre períodos (sprints, meses, trimestres)
- Motivar la adopción mostrando métricas concretas

### Para Managers y CTOs
- Reportar ROI de la inversión en herramientas de IA
- Planificar expansión basada en datos
- Identificar usuarios en riesgo de abandono
- Análisis estratégico para toma de decisiones

### Para Recursos Humanos
- Programas de retención basados en análisis de cohortes
- Formación dirigida para usuarios nuevos
- Seguimiento de productividad individual
- Evaluaciones de desempeño con métricas objetivas

## 🔍 Características Destacadas

### Diseño UX Avanzado
- **Responsive design** (4/3/2/1 columnas según dispositivo)
- **Menú desplegable** con navegación rápida
- **Gráficos interactivos** con Chart.js
- **Formato numérico español** (punto para miles, coma para decimales)

### Análisis Inteligente
- **Textos dinámicos contextuales** que se adaptan a los datos
- **Indicadores comparativos** automáticos (📈, 📉, 🆕, ➖)
- **Insights estratégicos** generados automáticamente
- **Validación robusta** de datos con manejo de errores

### Flexibilidad Temporal
- **División automática** inteligente de períodos
- **Fechas personalizadas** para análisis específicos
- **Compatibilidad de zona horaria** automática
- **Validación de fechas** con mensajes de error claros

## 🌟 Valor Agregado

Este proyecto no es solo una herramienta de reportes, sino una **plataforma de análisis estratégico** que:

- ✅ **Democratiza el análisis de productividad** con IA
- ✅ **Facilita la comunicación de resultados** a todos los niveles organizacionales
- ✅ **Proporciona insights accionables** para mejorar la adopción
- ✅ **Permite seguimiento temporal** para medir progreso
- ✅ **Integra análisis de retención** para optimizar la inversión

## 📊 Estado del Proyecto

- **Lenguaje**: Python 3.7+
- **Dependencias**: pandas (única dependencia externa)
- **Licencia**: MIT
- **Documentación**: Muy completa con ejemplos detallados
- **Código**: Bien estructurado con validaciones y manejo de errores
- **Madurez**: Proyecto completo y funcional con historial de cambios detallado

## 🎯 Conclusión

Es una herramienta especializada y madura para organizaciones que han implementado Cursor AI y necesitan **medir, visualizar y comunicar su impacto de forma profesional**. Combina análisis técnico profundo con presentación ejecutiva, siendo útil tanto para desarrolladores como para directivos.