# ⚡ Guía Rápida - Cursor AI Analytics + Firebase

## 🎯 **TU FLUJO DE TRABAJO (Solo 3 pasos)**

### **1. Para Features Nuevas**
```bash
# En GitHub:
1. Ver PR que YO creé
2. Clic en "Merge" (hacia develop)
3. Probar en: https://cursor-analytics-staging.web.app
```

### **2. Para Release a Producción**
```bash
# En GitHub:
1. Crear PR: develop → main
2. Clic en "Merge"
3. ¡Listo! → https://cursor-analytics-prod.web.app
```

### **3. Setup Inicial (Solo una vez)**
```bash
# En GitHub → Settings → Secrets:
FIREBASE_SERVICE_ACCOUNT_STAGING  # JSON de staging
FIREBASE_SERVICE_ACCOUNT_PROD     # JSON de producción
```

## 🔧 **Secretos GitHub (Copy-Paste)**

### **Ruta**: `Repository → Settings → Secrets and Variables → Actions`

### **Secretos a crear**:
- `FIREBASE_SERVICE_ACCOUNT_STAGING`
- `FIREBASE_SERVICE_ACCOUNT_PROD`
- `GITHUB_TOKEN` (automático)

### **Cómo obtener JSONs**:
1. Firebase Console → Project Settings → Service accounts
2. Generate new private key
3. Copiar JSON completo
4. Pegar en GitHub secret

## 🌍 **URLs de Referencia**

- **Staging**: `https://cursor-analytics-staging.web.app`
- **Production**: `https://cursor-analytics-prod.web.app`
- **Firebase Console**: `https://console.firebase.google.com`

## 📊 **Estados de Deploy**

- **develop branch** → Deploy a **STAGING** (automático)
- **main branch** → Deploy a **PRODUCTION** (automático)

## 🚀 **Comandos de Emergencia**

### **Si necesitas deploy manual**:
```bash
# Staging
firebase use staging && firebase deploy

# Production  
firebase use production && firebase deploy
```

### **Si necesitas rollback**:
```bash
# En Firebase Console → Hosting → Release history
# Clic en versión anterior → "Rollback"
```

---

**📋 Documento completo**: `plan_implementacion_firebase.md`