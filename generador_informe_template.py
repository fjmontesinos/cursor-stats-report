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

def formatear_fecha_espanol(fecha, formato_corto=False):
    """Formatea una fecha en español."""
    if fecha is None:
        return "N/A"
    
    meses_espanol = {
        'January': 'enero', 'February': 'febrero', 'March': 'marzo', 'April': 'abril',
        'May': 'mayo', 'June': 'junio', 'July': 'julio', 'August': 'agosto',
        'September': 'septiembre', 'October': 'octubre', 'November': 'noviembre', 'December': 'diciembre'
    }
    
    meses_espanol_corto = {
        'Jan': 'ene', 'Feb': 'feb', 'Mar': 'mar', 'Apr': 'abr',
        'May': 'may', 'Jun': 'jun', 'Jul': 'jul', 'Aug': 'ago',
        'Sep': 'sep', 'Oct': 'oct', 'Nov': 'nov', 'Dec': 'dic'
    }
    
    if formato_corto:
        fecha_str = fecha.strftime('%d %b')
        for mes_en, mes_es in meses_espanol_corto.items():
            fecha_str = fecha_str.replace(mes_en, mes_es)
    else:
        fecha_str = fecha.strftime('%d %B %Y')
        for mes_en, mes_es in meses_espanol.items():
            fecha_str = fecha_str.replace(mes_en, mes_es)
    
    return fecha_str

def validar_y_parsear_fechas(fecha_inicio_actual, fecha_fin_actual, fecha_inicio_anterior, fecha_fin_anterior, df):
    """Valida y parsea las fechas personalizadas proporcionadas por el usuario."""
    fechas_personalizadas = {}
    errores = []
    
    # Lista de fechas disponibles en el dataset
    fechas_disponibles = set(df['Date'].dt.date)
    fecha_min = min(fechas_disponibles)
    fecha_max = max(fechas_disponibles)
    
    def parsear_fecha(fecha_str, nombre_campo):
        if not fecha_str:
            return None
        
        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            
            # Verificar que la fecha esté en el dataset
            if fecha_obj not in fechas_disponibles:
                errores.append(f"❌ {nombre_campo}: {fecha_str} no existe en el dataset. Rango disponible: {fecha_min} - {fecha_max}")
                return None
                
            return fecha_obj
        except ValueError:
            errores.append(f"❌ {nombre_campo}: Formato inválido '{fecha_str}'. Use YYYY-MM-DD")
            return None
    
    # Parsear todas las fechas
    fechas_personalizadas['inicio_actual'] = parsear_fecha(fecha_inicio_actual, "Fecha inicio actual")
    fechas_personalizadas['fin_actual'] = parsear_fecha(fecha_fin_actual, "Fecha fin actual")
    fechas_personalizadas['inicio_anterior'] = parsear_fecha(fecha_inicio_anterior, "Fecha inicio anterior")
    fechas_personalizadas['fin_anterior'] = parsear_fecha(fecha_fin_anterior, "Fecha fin anterior")
    
    # Verificar que todas las fechas estén presentes si se usa modo manual
    fechas_proporcionadas = [f for f in fechas_personalizadas.values() if f is not None]
    
    if len(fechas_proporcionadas) > 0 and len(fechas_proporcionadas) < 4:
        errores.append("❌ Si especifica fechas personalizadas, debe proporcionar las 4 fechas: --fecha-inicio-actual, --fecha-fin-actual, --fecha-inicio-anterior, --fecha-fin-anterior")
    
    # Validaciones lógicas si todas las fechas están presentes
    if len(fechas_proporcionadas) == 4:
        inicio_actual = fechas_personalizadas['inicio_actual']
        fin_actual = fechas_personalizadas['fin_actual']
        inicio_anterior = fechas_personalizadas['inicio_anterior']
        fin_anterior = fechas_personalizadas['fin_anterior']
        
        if inicio_actual >= fin_actual:
            errores.append("❌ Fecha inicio actual debe ser anterior a fecha fin actual")
        
        if inicio_anterior >= fin_anterior:
            errores.append("❌ Fecha inicio anterior debe ser anterior a fecha fin anterior")
        
        # Verificar solapamiento de períodos
        if not (fin_anterior < inicio_actual or fin_actual < inicio_anterior):
            logger.warning("⚠️ Los períodos se solapan. Esto puede afectar el análisis de cohortes")
    
    return fechas_personalizadas, errores

def dividir_periodos_personalizados(df, fechas_personalizadas):
    """Divide el DataFrame usando fechas personalizadas especificadas por el usuario."""
    # Crear timestamps con la misma zona horaria que el DataFrame
    tz = df['Date'].dt.tz if hasattr(df['Date'].dt, 'tz') and df['Date'].dt.tz is not None else None
    
    inicio_actual = pd.Timestamp(fechas_personalizadas['inicio_actual'], tz=tz)
    fin_actual = pd.Timestamp(fechas_personalizadas['fin_actual'], tz=tz)
    inicio_anterior = pd.Timestamp(fechas_personalizadas['inicio_anterior'], tz=tz)
    fin_anterior = pd.Timestamp(fechas_personalizadas['fin_anterior'], tz=tz)
    
    # Filtrar DataFrames por rangos de fechas
    df_actual = df[(df['Date'] >= inicio_actual) & (df['Date'] <= fin_actual)].copy()
    df_anterior = df[(df['Date'] >= inicio_anterior) & (df['Date'] <= fin_anterior)].copy()
    
    # Calcular días únicos en cada período
    dias_actual = df_actual['Date'].nunique()
    dias_anterior = df_anterior['Date'].nunique()
    
    info_division = {
        'total_dias': dias_actual + dias_anterior,
        'dias_actual': dias_actual,
        'dias_anterior': dias_anterior,
        'periodo_anterior_inicio': inicio_anterior,
        'periodo_anterior_fin': fin_anterior,
        'periodo_actual_inicio': inicio_actual,
        'periodo_actual_fin': fin_actual,
        'comparativa_valida': dias_anterior > 0 and dias_actual > 0,
        'modo_personalizado': True
    }
    
    logger.info(f"📊 División temporal personalizada:")
    logger.info(f"   • Período anterior: {dias_anterior} días ({inicio_anterior.strftime('%d/%m')} - {fin_anterior.strftime('%d/%m')})")
    logger.info(f"   • Período actual: {dias_actual} días ({inicio_actual.strftime('%d/%m')} - {fin_actual.strftime('%d/%m')})")
    
    return df_actual, df_anterior, info_division

def dividir_periodos_temporales(df):
    """Divide el DataFrame en dos períodos: anterior (primera mitad) y actual (segunda mitad)."""
    # Ordenar por fecha
    df_ordenado = df.sort_values('Date').copy()
    
    # Obtener fechas únicas
    fechas_unicas = sorted(df_ordenado['Date'].unique())
    total_dias = len(fechas_unicas)
    
    logger.info(f"📅 Total de días únicos en el dataset: {total_dias}")
    
    if total_dias < 4:
        logger.warning("⚠️ Dataset muy pequeño para análisis comparativo")
        return df_ordenado, pd.DataFrame(), {
            'total_dias': total_dias,
            'dias_actual': total_dias,
            'dias_anterior': 0,
            'comparativa_valida': False
        }
    
    # Dividir en dos períodos (división entera)
    punto_corte = total_dias // 2
    fechas_anteriores = fechas_unicas[:punto_corte]
    fechas_actuales = fechas_unicas[punto_corte:]
    
    # Filtrar DataFrames
    df_anterior = df_ordenado[df_ordenado['Date'].isin(fechas_anteriores)].copy()
    df_actual = df_ordenado[df_ordenado['Date'].isin(fechas_actuales)].copy()
    
    info_division = {
        'total_dias': total_dias,
        'dias_actual': len(fechas_actuales),
        'dias_anterior': len(fechas_anteriores),
        'periodo_anterior_inicio': fechas_anteriores[0] if fechas_anteriores else None,
        'periodo_anterior_fin': fechas_anteriores[-1] if fechas_anteriores else None,
        'periodo_actual_inicio': fechas_actuales[0] if fechas_actuales else None,
        'periodo_actual_fin': fechas_actuales[-1] if fechas_actuales else None,
        'comparativa_valida': len(fechas_anteriores) > 0 and len(fechas_actuales) > 0,
        'modo_personalizado': False
    }
    
    logger.info(f"📊 División temporal:")
    logger.info(f"   • Período anterior: {len(fechas_anteriores)} días ({fechas_anteriores[0].strftime('%d/%m')} - {fechas_anteriores[-1].strftime('%d/%m')})")
    logger.info(f"   • Período actual: {len(fechas_actuales)} días ({fechas_actuales[0].strftime('%d/%m')} - {fechas_actuales[-1].strftime('%d/%m')})")
    
    return df_actual, df_anterior, info_division

def calcular_metricas_periodo(df, nombre_periodo=""):
    """Calcula métricas para un período específico."""
    if df.empty:
        return {
            'usuarios_activos': 0,
            'lineas_aceptadas': 0,
            'lineas_sugeridas': 0,
            'tasa_aceptacion': 0,
            'tabs_aceptados': 0,
            'tabs_mostrados': 0,
            'tasa_aceptacion_tabs': 0,
            'peticiones_totales': 0,
            'promedio_lineas_usuario': 0
        }
    
    df_activos = df[df['Is Active'] == True]
    
    # Métricas básicas (incluyendo líneas añadidas Y eliminadas)
    usuarios_activos = df_activos['Email'].nunique()
    lineas_aceptadas = df_activos['Chat Accepted Lines Added'].sum() + df_activos['Chat Accepted Lines Deleted'].sum()
    lineas_sugeridas = df_activos['Chat Suggested Lines Added'].sum() + df_activos['Chat Suggested Lines Deleted'].sum()
    tasa_aceptacion = (lineas_aceptadas / lineas_sugeridas * 100) if lineas_sugeridas > 0 else 0
    
    # Métricas de tabs
    tabs_aceptados = df_activos['Tabs Accepted'].sum()
    tabs_mostrados = df_activos['Chat Tabs Shown'].sum()
    tasa_aceptacion_tabs = (tabs_aceptados / tabs_mostrados * 100) if tabs_mostrados > 0 else 0
    
    # Peticiones totales
    peticiones_totales = (
        df_activos['Edit Requests'].sum() + 
        df_activos['Ask Requests'].sum() + 
        df_activos['Agent Requests'].sum() + 
        df_activos['Cmd+K Usages'].sum() + 
        df_activos['Subscription Included Reqs'].sum() + 
        df_activos['API Key Reqs'].sum() + 
        df_activos['Usage Based Reqs'].sum()
    )
    
    # Promedio por usuario
    promedio_lineas_usuario = (lineas_aceptadas / usuarios_activos) if usuarios_activos > 0 else 0
    
    return {
        'usuarios_activos': usuarios_activos,
        'lineas_aceptadas': int(lineas_aceptadas),
        'lineas_sugeridas': int(lineas_sugeridas),
        'tasa_aceptacion': round(tasa_aceptacion, 1),
        'tabs_aceptados': int(tabs_aceptados),
        'tabs_mostrados': int(tabs_mostrados),
        'tasa_aceptacion_tabs': round(tasa_aceptacion_tabs, 1),
        'peticiones_totales': int(peticiones_totales),
        'promedio_lineas_usuario': round(promedio_lineas_usuario, 0)
    }

def calcular_indicador_comparativo(actual, anterior):
    """Calcula el indicador visual de comparación entre períodos."""
    if anterior == 0:
        if actual > 0:
            return ' <span class="comparison-indicator positive">🆕 Nuevo</span>'
        return ' <span class="comparison-indicator neutral">➖ Sin cambios</span>'
    
    variacion = ((actual - anterior) / anterior) * 100
    
    if variacion > 5:
        return f' <span class="comparison-indicator positive">📈 +{formato_numero_espanol(variacion)}%</span>'
    elif variacion < -5:
        return f' <span class="comparison-indicator negative">📉 {formato_numero_espanol(variacion)}%</span>'
    else:
        return f' <span class="comparison-indicator neutral">➖ {formato_numero_espanol(variacion)}%</span>'

def analizar_cohortes_usuarios(df_actual, df_anterior):
    """Analiza las cohortes de usuarios entre períodos."""
    usuarios_actuales = set(df_actual[df_actual['Is Active'] == True]['Email'].unique())
    usuarios_anteriores = set(df_anterior[df_anterior['Is Active'] == True]['Email'].unique()) if not df_anterior.empty else set()
    
    # Clasificar usuarios
    usuarios_consistentes = usuarios_actuales & usuarios_anteriores
    usuarios_nuevos = usuarios_actuales - usuarios_anteriores
    usuarios_perdidos = usuarios_anteriores - usuarios_actuales
    usuarios_reactivados = usuarios_nuevos & set(df_anterior['Email'].unique()) if not df_anterior.empty else set()
    usuarios_nuevos_reales = usuarios_nuevos - usuarios_reactivados
    
    return {
        'consistentes': list(usuarios_consistentes),
        'nuevos': list(usuarios_nuevos_reales),
        'perdidos': list(usuarios_perdidos),
        'reactivados': list(usuarios_reactivados),
        'total_actual': len(usuarios_actuales),
        'total_anterior': len(usuarios_anteriores),
        'tasa_retencion': (len(usuarios_consistentes) / len(usuarios_anteriores) * 100) if usuarios_anteriores else 0
    }

def generar_insights_comparativos(metricas_actual, metricas_anterior, cohortes, info_division):
    """Genera insights estratégicos basados en el análisis comparativo."""
    insights = []
    
    if not info_division['comparativa_valida']:
        insights.append("📊 <strong>Análisis Base:</strong> Dataset inicial para establecer métricas de referencia.")
        return insights
    
    # Análisis de crecimiento en líneas de código
    if metricas_anterior['lineas_aceptadas'] > 0:
        crecimiento_lineas = ((metricas_actual['lineas_aceptadas'] - metricas_anterior['lineas_aceptadas']) / metricas_anterior['lineas_aceptadas']) * 100
        
        if crecimiento_lineas > 20:
            insights.append(f"🚀 <strong>Crecimiento Acelerado:</strong> Productividad aumentó {formato_numero_espanol(crecimiento_lineas)}%. Excelente momento para escalar la adopción.")
        elif crecimiento_lineas > 5:
            insights.append(f"📈 <strong>Crecimiento Sostenido:</strong> Mejora del {formato_numero_espanol(crecimiento_lineas)}% indica adopción exitosa.")
        elif crecimiento_lineas < -10:
            insights.append(f"⚠️ <strong>Alerta de Descenso:</strong> Caída del {formato_numero_espanol(abs(crecimiento_lineas))}%. Revisar posibles causas.")
        else:
            insights.append(f"📊 <strong>Estabilidad:</strong> Variación del {formato_numero_espanol(crecimiento_lineas)}% indica uso consistente.")
    
    # Análisis de retención de usuarios
    if cohortes['tasa_retencion'] > 90:
        insights.append(f"💎 <strong>Retención Excelente:</strong> {formato_numero_espanol(cohortes['tasa_retencion'])}% de usuarios mantienen actividad.")
    elif cohortes['tasa_retencion'] < 70:
        insights.append(f"🔄 <strong>Oportunidad de Retención:</strong> Solo {formato_numero_espanol(cohortes['tasa_retencion'])}% mantienen actividad. Plan de re-engagement necesario.")
    else:
        insights.append(f"👥 <strong>Retención Aceptable:</strong> {formato_numero_espanol(cohortes['tasa_retencion'])}% de retención con margen de mejora.")
    
    # Usuarios nuevos
    if len(cohortes['nuevos']) > 0:
        insights.append(f"🌟 <strong>Expansión Activa:</strong> {len(cohortes['nuevos'])} nuevos usuarios adoptaron la herramienta.")
    
    # Usuarios reactivados
    if len(cohortes['reactivados']) > 0:
        insights.append(f"🔄 <strong>Reactivación Exitosa:</strong> {len(cohortes['reactivados'])} usuarios volvieron a usar la herramienta.")
    
    # Análisis de calidad (tasa de aceptación)
    if metricas_actual['tasa_aceptacion'] > metricas_anterior['tasa_aceptacion'] + 5:
        insights.append(f"⚡ <strong>Mejora en Calidad:</strong> Tasa de aceptación subió a {formato_numero_espanol(metricas_actual['tasa_aceptacion'])}%.")
    elif metricas_actual['tasa_aceptacion'] < metricas_anterior['tasa_aceptacion'] - 5:
        insights.append(f"🔍 <strong>Revisar Calidad:</strong> Tasa de aceptación bajó a {formato_numero_espanol(metricas_actual['tasa_aceptacion'])}%.")
    
    # ROI y productividad
    if metricas_actual['promedio_lineas_usuario'] > 1000:
        insights.append(f"💰 <strong>Alto ROI:</strong> Promedio de {formato_numero_espanol(metricas_actual['promedio_lineas_usuario'])} líneas por usuario justifica inversión.")
    
    return insights

def procesar_datos_cursor(archivo_csv, fechas_personalizadas=None):
    """Procesa el archivo CSV con análisis comparativo temporal automático o personalizado."""
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
    
    # DIVISIÓN TEMPORAL: PERSONALIZADA O AUTOMÁTICA
    if fechas_personalizadas and all(fechas_personalizadas.values()):
        logger.info("🎯 Usando fechas personalizadas especificadas por el usuario")
        df_actual, df_anterior, info_division = dividir_periodos_personalizados(df, fechas_personalizadas)
    else:
        logger.info("🔄 Usando división temporal automática")
        df_actual, df_anterior, info_division = dividir_periodos_temporales(df)
    
    # Calcular métricas para ambos períodos
    metricas_actual = calcular_metricas_periodo(df_actual, "actual")
    metricas_anterior = calcular_metricas_periodo(df_anterior, "anterior")
    
    # Análisis de cohortes
    cohortes = analizar_cohortes_usuarios(df_actual, df_anterior)
    
    # Generar insights comparativos
    insights = generar_insights_comparativos(metricas_actual, metricas_anterior, cohortes, info_division)
    
    # Métricas del período actual (NO todo el período)
    df_actual_activos = df_actual[df_actual['Is Active'] == True]
    total_usuarios_actual = df_actual['Email'].nunique()
    usuarios_activos_actual = df_actual_activos['Email'].nunique()
    tasa_adopcion_actual = round((usuarios_activos_actual / total_usuarios_actual) * 100, 1)
    
    # Usuarios inactivos del período actual
    usuarios_con_actividad_actual = set(df_actual_activos['Email'].unique())
    todos_usuarios_actual = set(df_actual['Email'].unique())
    usuarios_inactivos_actual = list(todos_usuarios_actual - usuarios_con_actividad_actual)
    usuarios_inactivos_actual = [email for email in usuarios_inactivos_actual if pd.notna(email) and email.strip()]
    
    # Rankings del período actual
    # Top productividad con líneas totales (Added + Deleted)
    df_actual_activos = df_actual_activos.copy()  # Evitar SettingWithCopyWarning
    df_actual_activos['Chat Accepted Lines Total'] = (
        df_actual_activos['Chat Accepted Lines Added'] + 
        df_actual_activos['Chat Accepted Lines Deleted']
    )
    top_productividad = (df_actual_activos.groupby('Email')['Chat Accepted Lines Total']
                        .sum()
                        .sort_values(ascending=False)
                        .head(10))
    
    df_actual_activos = df_actual_activos.copy()
    df_actual_activos['Total_Requests'] = (
        df_actual_activos['Edit Requests'] + 
        df_actual_activos['Ask Requests'] + 
        df_actual_activos['Agent Requests'] + 
        df_actual_activos['Cmd+K Usages'] + 
        df_actual_activos['Subscription Included Reqs'] + 
        df_actual_activos['API Key Reqs'] + 
        df_actual_activos['Usage Based Reqs']
    )
    
    top_peticiones = (df_actual_activos.groupby('Email')['Total_Requests']
                     .sum()
                     .sort_values(ascending=False)
                     .head(10))
    
    # Tecnologías más utilizadas (período actual) con líneas totales
    extensiones_activas = df_actual_activos[df_actual_activos['Chat Accepted Lines Total'] > 0]
    top_extensiones = (extensiones_activas.groupby('Most Used Tab Extension').agg({
        'Chat Accepted Lines Total': 'sum',
        'Email': 'nunique'
    }).sort_values('Chat Accepted Lines Total', ascending=False).head(8))
    
    # Modelos de IA más utilizados (período actual)
    modelos_uso = df_actual_activos['Most Used Model'].value_counts().head(6)
    
    # Versiones de cliente (período actual)
    versiones_cliente = df_actual_activos[df_actual_activos['Client Version'].notna()]
    versiones_uso = versiones_cliente['Client Version'].value_counts().head(8)
    
    # Evolución temporal por días (SOLO período desde inicio anterior hasta fin actual)
    fecha_inicio_grafico = info_division['periodo_anterior_inicio']
    fecha_fin_grafico = info_division['periodo_actual_fin']
    
    # Filtrar datos solo para el período de los gráficos (anterior + actual)
    df_grafico = df[(df['Date'] >= fecha_inicio_grafico) & (df['Date'] <= fecha_fin_grafico)]
    df_grafico_activos = df_grafico[df_grafico['Is Active'] == True]
    
    evolucion_diaria = df_grafico_activos.groupby('Date').agg({
        'Chat Accepted Lines Added': 'sum',
        'Chat Accepted Lines Deleted': 'sum', 
        'Chat Suggested Lines Added': 'sum',
        'Chat Suggested Lines Deleted': 'sum',
        'Tabs Accepted': 'sum',
        'Chat Tabs Shown': 'sum',
        'Email': 'nunique'
    }).reset_index()
    
    # Calcular totales (Added + Deleted) para el gráfico
    evolucion_diaria['Chat Accepted Lines Total'] = evolucion_diaria['Chat Accepted Lines Added'] + evolucion_diaria['Chat Accepted Lines Deleted']
    evolucion_diaria['Chat Suggested Lines Total'] = evolucion_diaria['Chat Suggested Lines Added'] + evolucion_diaria['Chat Suggested Lines Deleted']
    evolucion_diaria = evolucion_diaria.sort_values('Date')
    
    # Fechas formateadas en español
    fecha_inicio_actual = formatear_fecha_espanol(info_division['periodo_actual_inicio'])
    fecha_fin_actual = formatear_fecha_espanol(info_division['periodo_actual_fin'])
    fecha_inicio_anterior = formatear_fecha_espanol(info_division['periodo_anterior_inicio'])
    fecha_fin_anterior = formatear_fecha_espanol(info_division['periodo_anterior_fin'])
    
    return {
        'periodo': {
            'inicio': fecha_inicio_actual,
            'fin': fecha_fin_actual,
            'anterior_inicio': fecha_inicio_anterior,
            'anterior_fin': fecha_fin_anterior,
            'comparativa_valida': info_division['comparativa_valida'],
            'dias_actual': info_division['dias_actual'],
            'dias_anterior': info_division['dias_anterior']
        },
        'usuarios': {
            'total': total_usuarios_actual,
            'activos': usuarios_activos_actual,
            'inactivos': len(usuarios_inactivos_actual),
            'tasa_adopcion': tasa_adopcion_actual,
            'lista_inactivos': usuarios_inactivos_actual
        },
        'codigo': {
            'lineas_aceptadas': metricas_actual['lineas_aceptadas'],
            'tasa_aceptacion': metricas_actual['tasa_aceptacion'],
            'promedio_por_usuario': metricas_actual['promedio_lineas_usuario']
        },
        'tabs': {
            'tabs_aceptados': metricas_actual['tabs_aceptados'],
            'tasa_aceptacion_tabs': metricas_actual['tasa_aceptacion_tabs']
        },
        'peticiones': {
            'total': metricas_actual['peticiones_totales']
        },
        'metricas_actual': metricas_actual,
        'metricas_anterior': metricas_anterior,
        'cohortes': cohortes,
        'insights': insights,
        'rankings': {
            'top_productividad': top_productividad,
            'top_peticiones': top_peticiones,
            'top_extensiones': top_extensiones,
            'modelos_uso': modelos_uso,
            'versiones_uso': versiones_uso
        },
        'evolucion': evolucion_diaria,
        'info_division': info_division
    }

def generar_textos_alternativos_kpis(metricas):
    """Genera textos alternativos dinámicos para cada KPI basado en los datos."""
    textos = {}
    
    # KPI Líneas de Código IA
    lineas = metricas['codigo']['lineas_aceptadas']
    if lineas > 100000:
        textos['LINEAS_TEXTO'] = "Productividad excepcional - superando las 100K líneas"
    elif lineas > 50000:
        textos['LINEAS_TEXTO'] = "Alta productividad - más de 50K líneas generadas"
    elif lineas > 10000:
        textos['LINEAS_TEXTO'] = "Productividad sólida - más de 10K líneas"
    else:
        textos['LINEAS_TEXTO'] = "Fase inicial de adopción"
    
    # KPI Tasa de Aceptación
    tasa = metricas['codigo']['tasa_aceptacion']
    if tasa > 70:
        textos['TASA_TEXTO'] = "Excelente calidad - alta precisión de sugerencias"
    elif tasa > 50:
        textos['TASA_TEXTO'] = "Buena calidad - sugerencias relevantes"
    elif tasa > 30:
        textos['TASA_TEXTO'] = "Calidad aceptable - margen de mejora"
    else:
        textos['TASA_TEXTO'] = "Requiere optimización de prompts y configuración"
    
    # KPI Tabs Aceptados
    tabs = metricas['tabs']['tabs_aceptados']
    if tabs > 5000:
        textos['TABS_TEXTO'] = "Uso intensivo del autocompletado inteligente"
    elif tabs > 1000:
        textos['TABS_TEXTO'] = "Buen aprovechamiento del autocompletado"
    elif tabs > 100:
        textos['TABS_TEXTO'] = "Uso moderado del autocompletado"
    else:
        textos['TABS_TEXTO'] = "Oportunidad de aumentar uso de autocompletado"
    
    # KPI Eficiencia Tabs
    eficiencia = metricas['tabs']['tasa_aceptacion_tabs']
    if eficiencia > 30:
        textos['EFICIENCIA_TEXTO'] = "Autocompletado muy efectivo"
    elif eficiencia > 20:
        textos['EFICIENCIA_TEXTO'] = "Autocompletado efectivo"
    elif eficiencia > 10:
        textos['EFICIENCIA_TEXTO'] = "Autocompletado moderadamente efectivo"
    else:
        textos['EFICIENCIA_TEXTO'] = "Autocompletado requiere ajustes"
    
    # KPI Peticiones Totales
    peticiones = metricas['peticiones']['total']
    if peticiones > 20000:
        textos['PETICIONES_TEXTO'] = "Interacción muy activa con IA"
    elif peticiones > 10000:
        textos['PETICIONES_TEXTO'] = "Interacción activa con modelos de IA"
    elif peticiones > 5000:
        textos['PETICIONES_TEXTO'] = "Interacción moderada con IA"
    else:
        textos['PETICIONES_TEXTO'] = "Potencial para mayor interacción"
    
    # KPI Promedio por Usuario
    promedio = metricas['codigo']['promedio_por_usuario']
    if promedio > 2000:
        textos['PROMEDIO_TEXTO'] = "Productividad individual excepcional"
    elif promedio > 1000:
        textos['PROMEDIO_TEXTO'] = "Buena productividad individual"
    elif promedio > 500:
        textos['PROMEDIO_TEXTO'] = "Productividad individual moderada"
    else:
        textos['PROMEDIO_TEXTO'] = "Oportunidad de mejora individual"
    
    # KPI Usuarios Activos
    adopcion = metricas['usuarios']['tasa_adopcion']
    if adopcion > 90:
        textos['USUARIOS_TEXTO'] = "Adopción casi universal - excelente"
    elif adopcion > 80:
        textos['USUARIOS_TEXTO'] = "Alta adopción - muy buena cobertura"
    elif adopcion > 60:
        textos['USUARIOS_TEXTO'] = "Adopción aceptable - margen de crecimiento"
    else:
        textos['USUARIOS_TEXTO'] = "Adopción inicial - gran potencial"
    
    # KPI Usuarios Inactivos
    inactivos = len(metricas['usuarios']['lista_inactivos'])
    if inactivos == 0:
        textos['INACTIVOS_TEXTO'] = "¡Adopción completa! Todos los usuarios activos"
    elif inactivos <= 5:
        textos['INACTIVOS_TEXTO'] = "Muy pocos usuarios sin actividad"
    elif inactivos <= 15:
        textos['INACTIVOS_TEXTO'] = "Grupo pequeño requiere atención"
    else:
        textos['INACTIVOS_TEXTO'] = "Oportunidad significativa de activación"
    
    # KPIs de Cohortes
    consistentes = len(metricas['cohortes']['consistentes'])
    nuevos = len(metricas['cohortes']['nuevos'])
    reactivados = len(metricas['cohortes']['reactivados'])
    perdidos = len(metricas['cohortes']['perdidos'])
    retencion = metricas['cohortes']['tasa_retencion']
    
    # Texto para Usuarios Consistentes
    if retencion > 90:
        textos['CONSISTENTES_TEXTO'] = "Base sólida de usuarios fieles"
    elif retencion > 75:
        textos['CONSISTENTES_TEXTO'] = "Buena base de usuarios regulares"
    else:
        textos['CONSISTENTES_TEXTO'] = "Oportunidad de fidelización"
    
    # Texto para Usuarios Nuevos
    if nuevos > 10:
        textos['NUEVOS_TEXTO'] = "Excelente crecimiento orgánico"
    elif nuevos > 5:
        textos['NUEVOS_TEXTO'] = "Buen crecimiento de usuarios"
    elif nuevos > 0:
        textos['NUEVOS_TEXTO'] = "Crecimiento moderado pero positivo"
    else:
        textos['NUEVOS_TEXTO'] = "Sin nuevos usuarios en este período"
    
    # Texto para Usuarios Reactivados
    if reactivados > 10:
        textos['REACTIVADOS_TEXTO'] = "Excelente recuperación de usuarios"
    elif reactivados > 5:
        textos['REACTIVADOS_TEXTO'] = "Buena reactivación de usuarios"
    elif reactivados > 0:
        textos['REACTIVADOS_TEXTO'] = "Algunos usuarios han vuelto"
    else:
        textos['REACTIVADOS_TEXTO'] = "Sin reactivaciones en este período"
    
    # Texto para Usuarios Perdidos
    if perdidos == 0:
        textos['PERDIDOS_TEXTO'] = "¡Retención perfecta! Sin pérdidas"
    elif perdidos <= 3:
        textos['PERDIDOS_TEXTO'] = "Pérdida mínima de usuarios"
    elif perdidos <= 10:
        textos['PERDIDOS_TEXTO'] = "Pérdida controlada de usuarios"
    else:
        textos['PERDIDOS_TEXTO'] = "Atención: pérdida significativa"
    
    # Texto para Tasa de Retención
    if retencion > 95:
        textos['RETENCION_TEXTO'] = "Retención excepcional"
    elif retencion > 85:
        textos['RETENCION_TEXTO'] = "Muy buena retención"
    elif retencion > 70:
        textos['RETENCION_TEXTO'] = "Retención aceptable"
    else:
        textos['RETENCION_TEXTO'] = "Requiere plan de retención"
    
    return textos

def generar_tablas_html(metricas):
    """Genera las tablas HTML para insertar en la plantilla."""
    
    # Top productividad
    top_prod_html = ""
    for email, lineas in metricas['rankings']['top_productividad'].items():
        email_sanitizado = sanitizar_html(str(email))
        lineas_formateadas = formato_numero_espanol(int(lineas))
        top_prod_html += f"<tr><td>{email_sanitizado}</td><td class=\"text-right\">{lineas_formateadas}</td></tr>\n                            "
    
    # Top peticiones
    top_pet_html = ""
    for email, peticiones in metricas['rankings']['top_peticiones'].items():
        email_sanitizado = sanitizar_html(str(email))
        peticiones_formateadas = formato_numero_espanol(int(peticiones))
        top_pet_html += f"<tr><td>{email_sanitizado}</td><td class=\"text-right\">{peticiones_formateadas}</td></tr>\n                            "
    
    # Tecnologías
    tech_html = ""
    for extension, data in metricas['rankings']['top_extensiones'].iterrows():
        lineas = int(data['Chat Accepted Lines Total'])
        usuarios = int(data['Email'])
        extension_sanitizada = sanitizar_html(str(extension))
        badge_class = re.sub(r'[^a-zA-Z0-9_-]', '', str(extension))  # Sanitizar clase CSS
        tech_html += f"<tr><td><span class=\"badge {badge_class}\">{extension_sanitizada}</span></td><td class=\"text-right\">{formato_numero_espanol(lineas)}</td><td class=\"text-right\">{usuarios}</td></tr>\n                            "
    
    # Modelos de IA - Comentado porque no se usa en la plantilla actual
    # models_html = ""
    # total_modelos = metricas['rankings']['modelos_uso'].sum()
    # for modelo, uso in metricas['rankings']['modelos_uso'].items():
    #     modelo_sanitizado = sanitizar_html(str(modelo))
    #     porcentaje = (uso / total_modelos) * 100
    #     models_html += f"<tr><td>{modelo_sanitizado}</td><td>{uso}</td><td>{formato_numero_espanol(porcentaje)}%</td></tr>\n                            "
    
    # Versiones de cliente
    versions_html = ""
    total_versiones = metricas['rankings']['versiones_uso'].sum()
    for version, uso in metricas['rankings']['versiones_uso'].items():
        version_sanitizada = sanitizar_html(str(version))
        porcentaje = (uso / total_versiones) * 100
        versions_html += f"<tr><td>{version_sanitizada}</td><td class=\"text-right\">{uso}</td><td class=\"text-right\">{formato_numero_espanol(porcentaje)}%</td></tr>\n                            "
    
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
    
    # Insights estratégicos
    insights_html = ""
    for insight in metricas['insights']:
        insights_html += f"<li>{insight}</li>\n                "
    
    # Datos para gráficos (sanitizados) - Solo para gráfico de donut, no para tabla HTML
    total_modelos = metricas['rankings']['modelos_uso'].sum()
    chart_models_labels = sanitizar_datos_para_json(list(metricas['rankings']['modelos_uso'].index))
    chart_models_data = sanitizar_datos_para_json([round((uso / total_modelos) * 100, 1) for uso in metricas['rankings']['modelos_uso'].values])
    
    # Datos para gráfico de evolución temporal (sanitizados)
    evolucion_df = metricas['evolucion']
    chart_evolution_labels = sanitizar_datos_para_json([formatear_fecha_espanol(fecha, formato_corto=True) for fecha in evolucion_df['Date']])
    chart_evolution_accepted = sanitizar_datos_para_json(evolucion_df['Chat Accepted Lines Total'].fillna(0).tolist())
    chart_evolution_suggested = sanitizar_datos_para_json(evolucion_df['Chat Suggested Lines Total'].fillna(0).tolist())
    chart_evolution_users = sanitizar_datos_para_json(evolucion_df['Email'].fillna(0).tolist())
    chart_tabs_accepted = sanitizar_datos_para_json(evolucion_df['Tabs Accepted'].fillna(0).tolist())
    chart_tabs_shown = sanitizar_datos_para_json(evolucion_df['Chat Tabs Shown'].fillna(0).tolist())
    
    return {
        'TOP_PRODUCTIVIDAD': top_prod_html,
        'TOP_PETICIONES': top_pet_html,
        'TECNOLOGIAS_UTILIZADAS': tech_html,
        # 'MODELOS_IA': models_html,  # Comentado - no se usa en plantilla actual
        'VERSIONES_CLIENTE': versions_html,
        'USUARIOS_INACTIVOS_LISTA': usuarios_inactivos_html,
        'RECOMENDACIONES_ESTRATEGICAS': recomendaciones_html,
        'INSIGHTS_ESTRATEGICOS': insights_html,
        'CHART_MODELS_LABELS': json.dumps(chart_models_labels, ensure_ascii=False),
        'CHART_MODELS_DATA': json.dumps(chart_models_data, ensure_ascii=False),
        'CHART_EVOLUTION_LABELS': json.dumps(chart_evolution_labels, ensure_ascii=False),
        'CHART_EVOLUTION_ACCEPTED': json.dumps(chart_evolution_accepted, ensure_ascii=False),
        'CHART_EVOLUTION_SUGGESTED': json.dumps(chart_evolution_suggested, ensure_ascii=False),
        'CHART_EVOLUTION_USERS': json.dumps(chart_evolution_users, ensure_ascii=False),
        'CHART_TABS_ACCEPTED': json.dumps(chart_tabs_accepted, ensure_ascii=False),
        'CHART_TABS_SHOWN': json.dumps(chart_tabs_shown, ensure_ascii=False)
    }

def generar_informe_desde_plantilla(metricas, archivo_plantilla="cursor_stats_report_ux.html", archivo_salida="informe_cursor_analytics.html"):
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
    
    # Generar textos alternativos dinámicos
    textos_alternativos = generar_textos_alternativos_kpis(metricas)
    
    # Crear diccionario de reemplazos (sanitizados)
    placeholders = {
        'PERIODO_INICIO': sanitizar_html(metricas['periodo']['inicio']),
        'PERIODO_FIN': sanitizar_html(metricas['periodo']['fin']),
        'PERIODO_ANTERIOR_INICIO': sanitizar_html(metricas['periodo']['anterior_inicio']),
        'PERIODO_ANTERIOR_FIN': sanitizar_html(metricas['periodo']['anterior_fin']),
        'COMPARATIVA_VALIDA': 'true' if metricas['periodo']['comparativa_valida'] else 'false',
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
        'FECHA_GENERACION': sanitizar_html(f"{datetime.now().day} de {formatear_fecha_espanol(datetime.now()).split()[1]} de {datetime.now().year}"),
        # Métricas comparativas
        'LINEAS_ACEPTADAS_INDICADOR': calcular_indicador_comparativo(
            metricas['metricas_actual']['lineas_aceptadas'], 
            metricas['metricas_anterior']['lineas_aceptadas']
        ),
        'USUARIOS_ACTIVOS_INDICADOR': calcular_indicador_comparativo(
            metricas['metricas_actual']['usuarios_activos'], 
            metricas['metricas_anterior']['usuarios_activos']
        ),
        'TASA_ACEPTACION_INDICADOR': calcular_indicador_comparativo(
            metricas['metricas_actual']['tasa_aceptacion'], 
            metricas['metricas_anterior']['tasa_aceptacion']
        ),
        'PETICIONES_INDICADOR': calcular_indicador_comparativo(
            metricas['metricas_actual']['peticiones_totales'], 
            metricas['metricas_anterior']['peticiones_totales']
        ),
        'TABS_INDICADOR': calcular_indicador_comparativo(
            metricas['metricas_actual']['tabs_aceptados'], 
            metricas['metricas_anterior']['tabs_aceptados']
        ),
        'TASA_ACEPTACION_TABS_INDICADOR': calcular_indicador_comparativo(
            metricas['metricas_actual']['tasa_aceptacion_tabs'], 
            metricas['metricas_anterior']['tasa_aceptacion_tabs']
        ),
        'PROMEDIO_LINEAS_INDICADOR': calcular_indicador_comparativo(
            metricas['metricas_actual']['promedio_lineas_usuario'], 
            metricas['metricas_anterior']['promedio_lineas_usuario']
        ),
        # Cohortes de usuarios
        'USUARIOS_CONSISTENTES': len(metricas['cohortes']['consistentes']),
        'USUARIOS_NUEVOS': len(metricas['cohortes']['nuevos']),
        'USUARIOS_PERDIDOS': len(metricas['cohortes']['perdidos']),
        'USUARIOS_REACTIVADOS': len(metricas['cohortes']['reactivados']),
        'TASA_RETENCION': formato_numero_espanol(metricas['cohortes']['tasa_retencion']),
        **tablas,
        **textos_alternativos
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
    parser.add_argument('--plantilla', '-t', default='cursor_stats_report_ux.html',
                       help='Archivo de plantilla HTML (default: cursor_stats_report_ux.html)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Activar logging detallado')
    
    # Parámetros para fechas personalizadas
    parser.add_argument('--fecha-inicio-actual', type=str,
                       help='Fecha inicio período actual (YYYY-MM-DD). Si no se especifica, usa división automática')
    parser.add_argument('--fecha-fin-actual', type=str,
                       help='Fecha fin período actual (YYYY-MM-DD). Si no se especifica, usa división automática')
    parser.add_argument('--fecha-inicio-anterior', type=str,
                       help='Fecha inicio período anterior (YYYY-MM-DD). Si no se especifica, usa división automática')
    parser.add_argument('--fecha-fin-anterior', type=str,
                       help='Fecha fin período anterior (YYYY-MM-DD). Si no se especifica, usa división automática')
    
    args = parser.parse_args()
    
    # Configurar nivel de logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("🚀 Iniciando generación de informe de Cursor AI Analytics")
    logger.info("=" * 60)
    
    # Validar fechas personalizadas si se proporcionan
    fechas_personalizadas = None
    if any([args.fecha_inicio_actual, args.fecha_fin_actual, args.fecha_inicio_anterior, args.fecha_fin_anterior]):
        # Cargar CSV temporalmente para validar fechas
        try:
            df_temp = pd.read_csv(args.archivo_csv)
            df_temp['Date'] = pd.to_datetime(df_temp['Date'], errors='coerce')
            df_temp = df_temp.dropna(subset=['Date'])
            
            fechas_personalizadas, errores = validar_y_parsear_fechas(
                args.fecha_inicio_actual, args.fecha_fin_actual,
                args.fecha_inicio_anterior, args.fecha_fin_anterior, df_temp
            )
            
            if errores:
                logger.error("❌ Errores en fechas personalizadas:")
                for error in errores:
                    logger.error(f"  • {error}")
                sys.exit(1)
                
            logger.info("✅ Fechas personalizadas validadas correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error al validar fechas personalizadas: {e}")
            sys.exit(1)
    
    # Procesar datos
    metricas = procesar_datos_cursor(args.archivo_csv, fechas_personalizadas)
    
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