import pandas as pd
import sys
from datetime import datetime
import argparse
import re
import json
import html
import logging
from typing import Dict, List, Optional, Any

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Esquema esperado del CSV
ESQUEMA_CSV_REQUERIDO = {
    'Date': 'datetime',
    'Email': 'object',
    'Is Active': 'bool',
    'Chat Accepted Lines Added': 'numeric',
    'Chat Suggested Lines Added': 'numeric',
    'Tabs Accepted': 'numeric',
    'Chat Tabs Shown': 'numeric',
    'Most Used Tab Extension': 'object',
    'Most Used Model': 'object',
    'Client Version': 'object',
    'Edit Requests': 'numeric',
    'Ask Requests': 'numeric',
    'Agent Requests': 'numeric',
    'Cmd+K Usages': 'numeric',
    'Subscription Included Reqs': 'numeric',
    'API Key Reqs': 'numeric',
    'Usage Based Reqs': 'numeric'
}

def sanitizar_html(texto: str) -> str:
    """Sanitiza texto para prevenir XSS en HTML."""
    if not isinstance(texto, str):
        texto = str(texto)
    
    # Escapar caracteres HTML peligrosos
    texto_sanitizado = html.escape(texto, quote=True)
    
    # Remover caracteres de control y caracteres no imprimibles
    texto_sanitizado = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', texto_sanitizado)
    
    # Limitar longitud para prevenir ataques de buffer
    if len(texto_sanitizado) > 1000:
        texto_sanitizado = texto_sanitizado[:997] + "..."
        logger.warning(f"Texto truncado por seguridad: longitud original {len(texto)}")
    
    return texto_sanitizado

def validar_email(email: str) -> bool:
    """Valida formato de email básico."""
    if not isinstance(email, str):
        return False
    
    patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron_email, email.strip()))

def validar_esquema_csv(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Valida que el DataFrame tenga las columnas requeridas y tipos correctos.
    
    Returns:
        Dict con 'errores' y 'advertencias'
    """
    resultado = {'errores': [], 'advertencias': []}
    
    # Verificar columnas requeridas
    columnas_faltantes = set(ESQUEMA_CSV_REQUERIDO.keys()) - set(df.columns)
    if columnas_faltantes:
        resultado['errores'].extend([
            f"Columna requerida faltante: '{col}'" for col in columnas_faltantes
        ])
    
    # Verificar tipos de datos
    for columna, tipo_esperado in ESQUEMA_CSV_REQUERIDO.items():
        if columna not in df.columns:
            continue
            
        try:
            if tipo_esperado == 'datetime':
                pd.to_datetime(df[columna], errors='coerce')
                if df[columna].isna().all():
                    resultado['advertencias'].append(f"Columna '{columna}': No se pudieron convertir fechas")
                    
            elif tipo_esperado == 'numeric':
                pd.to_numeric(df[columna], errors='coerce')
                valores_nulos = df[columna].isna().sum()
                if valores_nulos > len(df) * 0.5:  # Más del 50% nulos
                    resultado['advertencias'].append(f"Columna '{columna}': {valores_nulos} valores no numéricos de {len(df)}")
                    
            elif tipo_esperado == 'bool':
                valores_unicos = df[columna].unique()
                valores_bool_validos = {True, False, 'True', 'False', 1, 0, '1', '0'}
                if not all(val in valores_bool_validos or pd.isna(val) for val in valores_unicos):
                    resultado['advertencias'].append(f"Columna '{columna}': Contiene valores no booleanos")
                    
        except Exception as e:
            resultado['advertencias'].append(f"Error validando columna '{columna}': {str(e)}")
    
    # Validar emails
    if 'Email' in df.columns:
        emails_invalidos = []
        for email in df['Email'].dropna().unique():
            if not validar_email(str(email)):
                emails_invalidos.append(str(email))
        
        if emails_invalidos:
            resultado['advertencias'].append(f"Emails con formato inválido: {len(emails_invalidos)} encontrados")
            logger.warning(f"Emails inválidos: {emails_invalidos[:5]}...")  # Solo mostrar los primeros 5
    
    # Verificar cantidad mínima de registros
    if len(df) < 10:
        resultado['advertencias'].append(f"Dataset muy pequeño: solo {len(df)} registros")
    
    return resultado

def sanitizar_datos_para_json(datos: Any) -> Any:
    """Sanitiza datos antes de convertir a JSON para gráficos."""
    if isinstance(datos, list):
        return [sanitizar_datos_para_json(item) for item in datos]
    elif isinstance(datos, dict):
        return {key: sanitizar_datos_para_json(value) for key, value in datos.items()}
    elif isinstance(datos, str):
        return sanitizar_html(datos)
    elif isinstance(datos, (int, float)):
        # Verificar que los números sean válidos
        if pd.isna(datos) or not pd.api.types.is_number(datos):
            return 0
        # Limitar valores extremos para prevenir problemas en gráficos
        if abs(datos) > 1e15:
            logger.warning(f"Valor numérico extremo detectado y limitado: {datos}")
            return 1e15 if datos > 0 else -1e15
        return datos
    else:
        return str(datos) if datos is not None else ""

def formato_numero_espanol(numero):
    """Convierte número a formato español: punto para miles, coma para decimales"""
    if isinstance(numero, (int, float)):
        if numero == int(numero):
            # Es un entero
            return f"{int(numero):,}".replace(",", ".")
        else:
            # Es decimal
            return f"{numero:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return str(numero)

def procesar_datos_cursor(archivo_csv):
    """Procesa el archivo CSV y extrae las métricas principales."""
    logger.info(f"📊 Procesando datos de {archivo_csv}...")
    
    try:
        df = pd.read_csv(archivo_csv)
        logger.info(f"✅ Archivo cargado: {len(df)} registros encontrados")
        
        # Validar esquema del CSV
        validacion = validar_esquema_csv(df)
        
        if validacion['errores']:
            logger.error("❌ Errores críticos en el CSV:")
            for error in validacion['errores']:
                logger.error(f"  • {error}")
            return None
            
        if validacion['advertencias']:
            logger.warning("⚠️ Advertencias en el CSV:")
            for advertencia in validacion['advertencias']:
                logger.warning(f"  • {advertencia}")
        
        # Convertir fecha con manejo de errores
        try:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            fechas_invalidas = df['Date'].isna().sum()
            if fechas_invalidas > 0:
                logger.warning(f"⚠️ {fechas_invalidas} fechas no válidas encontradas y excluidas")
                df = df.dropna(subset=['Date'])
        except Exception as e:
            logger.error(f"❌ Error al convertir fechas: {e}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error al leer el archivo CSV: {e}")
        return None
    
    # Filtrar usuarios activos
    df_activos = df[df['Is Active'] == True]
    
    # Métricas básicas
    total_usuarios = df['Email'].nunique()
    usuarios_activos = df_activos['Email'].nunique()
    tasa_adopcion = round((usuarios_activos / total_usuarios) * 100, 1)
    
    # Usuarios inactivos
    usuarios_con_actividad = set(df_activos['Email'].unique())
    todos_usuarios = set(df['Email'].unique())
    usuarios_inactivos = list(todos_usuarios - usuarios_con_actividad)
    usuarios_inactivos = [email for email in usuarios_inactivos if pd.notna(email) and email.strip()]
    
    # Métricas de código
    total_lineas_aceptadas = df_activos['Chat Accepted Lines Added'].sum()
    total_lineas_sugeridas = df_activos['Chat Suggested Lines Added'].sum()
    tasa_aceptacion = round((total_lineas_aceptadas / total_lineas_sugeridas) * 100, 1) if total_lineas_sugeridas > 0 else 0
    promedio_lineas_usuario = round(total_lineas_aceptadas / usuarios_activos, 0) if usuarios_activos > 0 else 0
    
    # Peticiones a IA
    total_peticiones = (df_activos['Edit Requests'].sum() + 
                       df_activos['Ask Requests'].sum() + 
                       df_activos['Agent Requests'].sum() + 
                       df_activos['Cmd+K Usages'].sum() + 
                       df_activos['Subscription Included Reqs'].sum() + 
                       df_activos['API Key Reqs'].sum() + 
                       df_activos['Usage Based Reqs'].sum())
    
    # Rankings
    top_productividad = (df_activos.groupby('Email')['Chat Accepted Lines Added']
                        .sum()
                        .sort_values(ascending=False)
                        .head(10))
    
    df_activos['Total_Requests'] = (df_activos['Edit Requests'] + 
                                   df_activos['Ask Requests'] + 
                                   df_activos['Agent Requests'] + 
                                   df_activos['Cmd+K Usages'] + 
                                   df_activos['Subscription Included Reqs'] + 
                                   df_activos['API Key Reqs'] + 
                                   df_activos['Usage Based Reqs'])
    
    top_peticiones = (df_activos.groupby('Email')['Total_Requests']
                     .sum()
                     .sort_values(ascending=False)
                     .head(10))
    
    # Tecnologías más utilizadas
    extensiones_activas = df_activos[df_activos['Chat Accepted Lines Added'] > 0]
    top_extensiones = (extensiones_activas.groupby('Most Used Tab Extension').agg({
        'Chat Accepted Lines Added': 'sum',
        'Email': 'nunique'
    }).sort_values('Chat Accepted Lines Added', ascending=False).head(8))
    
    # Modelos de IA más utilizados
    modelos_uso = df_activos['Most Used Model'].value_counts().head(6)
    
    # Versiones de cliente
    versiones_cliente = df_activos[df_activos['Client Version'].notna()]
    versiones_uso = versiones_cliente['Client Version'].value_counts().head(8)
    
    # Fechas del período
    fecha_inicio = df['Date'].min().strftime('%d %B %Y')
    fecha_fin = df['Date'].max().strftime('%d %B %Y')
    
    # Métricas de tabs
    total_tabs_aceptados = df_activos['Tabs Accepted'].sum()
    total_tabs_mostrados = df_activos['Chat Tabs Shown'].sum()
    tasa_aceptacion_tabs = (total_tabs_aceptados / total_tabs_mostrados) * 100 if total_tabs_mostrados > 0 else 0
    
    # Evolución temporal por días
    evolucion_diaria = df_activos.groupby('Date').agg({
        'Chat Accepted Lines Added': 'sum',
        'Chat Suggested Lines Added': 'sum',
        'Tabs Accepted': 'sum',
        'Chat Tabs Shown': 'sum',
        'Email': 'nunique'
    }).reset_index()
    evolucion_diaria = evolucion_diaria.sort_values('Date')
    
    return {
        'periodo': {
            'inicio': fecha_inicio,
            'fin': fecha_fin
        },
        'usuarios': {
            'total': total_usuarios,
            'activos': usuarios_activos,
            'inactivos': len(usuarios_inactivos),
            'tasa_adopcion': tasa_adopcion,
            'lista_inactivos': usuarios_inactivos
        },
        'codigo': {
            'lineas_aceptadas': int(total_lineas_aceptadas),
            'tasa_aceptacion': tasa_aceptacion,
            'promedio_por_usuario': int(promedio_lineas_usuario)
        },
        'tabs': {
            'tabs_aceptados': int(total_tabs_aceptados),
            'tasa_aceptacion_tabs': tasa_aceptacion_tabs
        },
        'peticiones': {
            'total': int(total_peticiones)
        },
        'rankings': {
            'top_productividad': top_productividad,
            'top_peticiones': top_peticiones,
            'top_extensiones': top_extensiones,
            'modelos_uso': modelos_uso,
            'versiones_uso': versiones_uso
        },
        'evolucion': evolucion_diaria
    }

def generar_tablas_html(metricas):
    """Genera las tablas HTML para insertar en la plantilla."""
    
    # Top productividad
    top_prod_html = ""
    for email, lineas in metricas['rankings']['top_productividad'].items():
        email_sanitizado = sanitizar_html(str(email))
        lineas_formateadas = formato_numero_espanol(int(lineas))
        top_prod_html += f"<tr><td>{email_sanitizado}</td><td>{lineas_formateadas}</td></tr>\n                            "
    
    # Top peticiones
    top_pet_html = ""
    for email, peticiones in metricas['rankings']['top_peticiones'].items():
        email_sanitizado = sanitizar_html(str(email))
        peticiones_formateadas = formato_numero_espanol(int(peticiones))
        top_pet_html += f"<tr><td>{email_sanitizado}</td><td>{peticiones_formateadas}</td></tr>\n                            "
    
    # Tecnologías
    tech_html = ""
    for extension, data in metricas['rankings']['top_extensiones'].iterrows():
        lineas = int(data['Chat Accepted Lines Added'])
        usuarios = int(data['Email'])
        extension_sanitizada = sanitizar_html(str(extension))
        badge_class = re.sub(r'[^a-zA-Z0-9_-]', '', str(extension))  # Sanitizar clase CSS
        tech_html += f"<tr><td><span class=\"badge {badge_class}\">{extension_sanitizada}</span></td><td>{formato_numero_espanol(lineas)}</td><td>{usuarios}</td></tr>\n                            "
    
    # Modelos de IA
    models_html = ""
    total_modelos = metricas['rankings']['modelos_uso'].sum()
    for modelo, uso in metricas['rankings']['modelos_uso'].items():
        modelo_sanitizado = sanitizar_html(str(modelo))
        porcentaje = (uso / total_modelos) * 100
        models_html += f"<tr><td>{modelo_sanitizado}</td><td>{uso}</td><td>{formato_numero_espanol(porcentaje)}%</td></tr>\n                            "
    
    # Versiones de cliente
    versions_html = ""
    total_versiones = metricas['rankings']['versiones_uso'].sum()
    for version, uso in metricas['rankings']['versiones_uso'].items():
        version_sanitizada = sanitizar_html(str(version))
        porcentaje = (uso / total_versiones) * 100
        versions_html += f"<tr><td>{version_sanitizada}</td><td>{uso}</td><td>{formato_numero_espanol(porcentaje)}%</td></tr>\n                            "
    
    # Lista de usuarios inactivos
    usuarios_inactivos_html = ""
    for email in metricas['usuarios']['lista_inactivos']:
        email_sanitizado = sanitizar_html(str(email))
        usuarios_inactivos_html += f"<li>{email_sanitizado}</li>\n                "
    
    # Recomendaciones estratégicas
    recomendaciones = []
    
    # Recomendación sobre versiones si hay fragmentación
    version_principal = metricas['rankings']['versiones_uso'].index[0]
    porcentaje_version_principal = (metricas['rankings']['versiones_uso'].iloc[0] / total_versiones) * 100
    
    if porcentaje_version_principal < 50:
        recomendaciones.append(f"<li><strong>🔄 Actualización de Versiones:</strong> Estandarizar en la versión {version_principal} para optimizar compatibilidad y soporte. Actualmente hay fragmentación de versiones.</li>")
    
    recomendaciones.extend([
        "<li><strong>🚀 Expansión Inmediata:</strong> Aumentar cobertura al 100% en equipos de desarrollo. La alta tasa de adopción actual justifica plenamente la inversión adicional en licencias.</li>",
        "<li><strong>🎓 Centro de Excelencia IA:</strong> Crear programa de formación interno liderado por los 'Campeones de Productividad' identificados.</li>",
        "<li><strong>📊 Dashboard Ejecutivo:</strong> Implementar métricas en tiempo real de productividad para seguimiento continuo.</li>",
        "<li><strong>🤝 Red de Embajadores:</strong> Formalizar red de 'AI Champions' que promuevan mejores prácticas entre equipos.</li>",
        "<li><strong>🔄 Optimización Continua:</strong> Revisiones trimestrales para evaluar nuevos modelos y optimizar costes.</li>",
        f"<li><strong>👥 Atención Personalizada:</strong> Plan específico para los {len(metricas['usuarios']['lista_inactivos'])} usuarios inactivos con formación y soporte dedicado.</li>"
    ])
    
    recomendaciones_html = "\n                ".join(recomendaciones)
    
    # Datos para gráficos (sanitizados)
    chart_models_labels = sanitizar_datos_para_json(list(metricas['rankings']['modelos_uso'].index))
    chart_models_data = sanitizar_datos_para_json([round((uso / total_modelos) * 100, 1) for uso in metricas['rankings']['modelos_uso'].values])
    
    # Datos para gráfico de evolución temporal (sanitizados)
    evolucion_df = metricas['evolucion']
    chart_evolution_labels = sanitizar_datos_para_json([fecha.strftime('%d %b') for fecha in evolucion_df['Date']])
    chart_evolution_accepted = sanitizar_datos_para_json(evolucion_df['Chat Accepted Lines Added'].fillna(0).tolist())
    chart_evolution_suggested = sanitizar_datos_para_json(evolucion_df['Chat Suggested Lines Added'].fillna(0).tolist())
    chart_evolution_users = sanitizar_datos_para_json(evolucion_df['Email'].fillna(0).tolist())
    chart_tabs_accepted = sanitizar_datos_para_json(evolucion_df['Tabs Accepted'].fillna(0).tolist())
    chart_tabs_shown = sanitizar_datos_para_json(evolucion_df['Chat Tabs Shown'].fillna(0).tolist())
    
    return {
        'TOP_PRODUCTIVIDAD': top_prod_html,
        'TOP_PETICIONES': top_pet_html,
        'TECNOLOGIAS_UTILIZADAS': tech_html,
        'VERSIONES_CLIENTE': versions_html,
        'USUARIOS_INACTIVOS_LISTA': usuarios_inactivos_html,
        'RECOMENDACIONES_ESTRATEGICAS': recomendaciones_html,
        'CHART_MODELS_LABELS': json.dumps(chart_models_labels, ensure_ascii=False),
        'CHART_MODELS_DATA': json.dumps(chart_models_data, ensure_ascii=False),
        'CHART_EVOLUTION_LABELS': json.dumps(chart_evolution_labels, ensure_ascii=False),
        'CHART_EVOLUTION_ACCEPTED': json.dumps(chart_evolution_accepted, ensure_ascii=False),
        'CHART_EVOLUTION_SUGGESTED': json.dumps(chart_evolution_suggested, ensure_ascii=False),
        'CHART_EVOLUTION_USERS': json.dumps(chart_evolution_users, ensure_ascii=False),
        'CHART_TABS_ACCEPTED': json.dumps(chart_tabs_accepted, ensure_ascii=False),
        'CHART_TABS_SHOWN': json.dumps(chart_tabs_shown, ensure_ascii=False)
    }

def generar_informe_desde_plantilla(metricas, archivo_plantilla="cursor_stats_report.html", archivo_salida="informe_cursor_analytics.html"):
    """Genera el informe usando la plantilla HTML con placeholders."""
    logger.info(f"📝 Generando informe desde plantilla...")
    
    try:
        with open(archivo_plantilla, 'r', encoding='utf-8') as f:
            html_content = f.read()
        logger.debug(f"Plantilla cargada exitosamente: {len(html_content)} caracteres")
    except FileNotFoundError:
        logger.error(f"❌ Archivo de plantilla no encontrado: {archivo_plantilla}")
        return None
    except Exception as e:
        logger.error(f"❌ Error al leer plantilla: {e}")
        return None
    
    # Generar tablas HTML
    tablas = generar_tablas_html(metricas)
    
    # Crear diccionario de reemplazos (sanitizados)
    placeholders = {
        'PERIODO_INICIO': sanitizar_html(metricas['periodo']['inicio']),
        'PERIODO_FIN': sanitizar_html(metricas['periodo']['fin']),
        'TASA_ADOPCION': formato_numero_espanol(metricas['usuarios']['tasa_adopcion']),
        'USUARIOS_ACTIVOS': metricas['usuarios']['activos'],
        'TOTAL_USUARIOS': metricas['usuarios']['total'],
        'LINEAS_ACEPTADAS': formato_numero_espanol(metricas['codigo']['lineas_aceptadas']),
        'TASA_ACEPTACION': formato_numero_espanol(metricas['codigo']['tasa_aceptacion']),
        'TABS_ACEPTADOS': formato_numero_espanol(metricas['tabs']['tabs_aceptados']),
        'TASA_ACEPTACION_TABS': formato_numero_espanol(metricas['tabs']['tasa_aceptacion_tabs']),
        'PROMEDIO_LINEAS': formato_numero_espanol(metricas['codigo']['promedio_por_usuario']),
        'PETICIONES_TOTALES': formato_numero_espanol(metricas['peticiones']['total']),
        'USUARIOS_INACTIVOS': len(metricas['usuarios']['lista_inactivos']),
        'FECHA_GENERACION': sanitizar_html(datetime.now().strftime('%d de %B de %Y')),
        **tablas
    }
    
    # Reemplazar placeholders
    placeholders_reemplazados = 0
    for placeholder, valor in placeholders.items():
        patron = f"{{{{{placeholder}}}}}"
        if patron in html_content:
            html_content = html_content.replace(patron, str(valor))
            placeholders_reemplazados += 1
        else:
            logger.warning(f"⚠️ Placeholder no encontrado en plantilla: {placeholder}")
    
    logger.debug(f"Placeholders reemplazados: {placeholders_reemplazados}/{len(placeholders)}")
    
    # Guardar archivo
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.debug(f"Archivo guardado exitosamente: {len(html_content)} caracteres")
    except Exception as e:
        logger.error(f"❌ Error al guardar archivo: {e}")
        return None
    
    logger.info(f"✅ Informe generado: {archivo_salida}")
    return archivo_salida

def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(description='Generador de Informes de Cursor AI Analytics usando Plantilla')
    parser.add_argument('archivo_csv', help='Archivo CSV con datos de Cursor')
    parser.add_argument('--salida', '-o', default='informe_cursor_analytics.html', 
                       help='Archivo HTML de salida (default: informe_cursor_analytics.html)')
    parser.add_argument('--plantilla', '-t', default='cursor_stats_report.html',
                       help='Archivo de plantilla HTML (default: cursor_stats_report.html)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Activar logging detallado')
    
    args = parser.parse_args()
    
    # Configurar nivel de logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("🚀 Iniciando generación de informe de Cursor AI Analytics")
    logger.info("=" * 60)
    
    # Procesar datos
    metricas = procesar_datos_cursor(args.archivo_csv)
    
    if metricas is None:
        logger.error("❌ Error al procesar los datos. Abortando.")
        sys.exit(1)
    
    # Generar informe desde plantilla
    archivo_generado = generar_informe_desde_plantilla(metricas, args.plantilla, args.salida)
    
    if archivo_generado:
        logger.info("=" * 60)
        logger.info(f"🎉 ¡Informe completado exitosamente!")
        logger.info(f"📄 Archivo generado: {archivo_generado}")
        logger.info(f"📊 Resumen de métricas:")
        logger.info(f"   • Período: {metricas['periodo']['inicio']} - {metricas['periodo']['fin']}")
        logger.info(f"   • Usuarios activos: {metricas['usuarios']['activos']}/{metricas['usuarios']['total']} ({metricas['usuarios']['tasa_adopcion']}%)")
        logger.info(f"   • Líneas de código IA: {metricas['codigo']['lineas_aceptadas']:,}")
        logger.info(f"   • Tasa de aceptación: {metricas['codigo']['tasa_aceptacion']}%")
        logger.info(f"   • Peticiones totales: {metricas['peticiones']['total']:,}")
    else:
        logger.error("❌ Error al generar el informe.")
        sys.exit(1)

if __name__ == "__main__":
    main() 