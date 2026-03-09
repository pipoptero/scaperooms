# 🔐 Escape Rooms Tracker

Web interactiva para llevar el seguimiento de escape rooms. Se actualiza automáticamente al subir el Excel.

## 🗂 Estructura del repositorio

```
escape-rooms-tracker/
├── index.html                        ← La web (no tocar)
├── convert.py                        ← Script de conversión (no tocar)
├── data.json                         ← Generado automáticamente por la Action
├── escape_rooms_tracker_mejorado.xlsx ← TU ARCHIVO EXCEL ← aquí actualizas
└── .github/
    └── workflows/
        └── update-data.yml           ← La GitHub Action (no tocar)
```

## 🚀 Configuración inicial (solo una vez)

### 1. Crear el repositorio en GitHub
- Ve a github.com → **New repository**
- Nombre: `escape-rooms-tracker` (o el que quieras)
- Visibilidad: **Public** (necesario para GitHub Pages gratis)
- No inicialices con README

### 2. Subir los archivos
Sube todos los archivos de esta carpeta al repo. Puedes hacerlo:
- Arrastrando los archivos desde la interfaz web de GitHub
- O con Git desde terminal:
  ```bash
  git init
  git add .
  git commit -m "🔐 Initial commit"
  git remote add origin https://github.com/TU_USUARIO/escape-rooms-tracker.git
  git push -u origin main
  ```

### 3. Activar GitHub Pages
- En el repo: **Settings** → **Pages**
- Source: **Deploy from a branch**
- Branch: `main` / folder: `/ (root)`
- Guarda → en ~2 minutos tendrás una URL del tipo:
  `https://TU_USUARIO.github.io/escape-rooms-tracker`

### 4. Primera ejecución de la Action
Al subir el Excel por primera vez, la Action se ejecutará automáticamente y generará `data.json`. Puedes seguirlo en la pestaña **Actions** del repo.

---

## 🔄 Flujo de actualización (uso diario)

1. **Edita tu Excel** localmente (añade rooms, cambia valoraciones...)
2. **Sube el Excel** a GitHub (arrastra y suelta en la interfaz web, o `git push`)
3. **GitHub Action** se ejecuta automáticamente (~30 segundos)
4. **La web** se actualiza sola con los nuevos datos ✅

---

## 📋 Formato del Excel

El Excel debe tener **dos hojas**:

### Hoja «Pendientes»
| Columna | Descripción |
|---------|-------------|
| Nombre del Escape | Nombre del escape room |
| Empresa | Empresa/local |
| Ciudad | Ciudad |
| Temática | Temática del escape |
| Tipo | Tipo de experiencia |
| Duración | Duración en minutos |
| Dificultad | Alta / Media-Alta / Media / Baja |
| Valoración | Rating de escapistas.com (0-10) |
| Web | URL de la web |

### Hoja «Hechos»
Mismas columnas que Pendientes, más:
| Columna | Descripción |
|---------|-------------|
| Valoración Grupo | Vuestra puntuación (0-10) |

---

## ❓ Preguntas frecuentes

**¿Cuánto tarda en actualizarse tras subir el Excel?**
Normalmente menos de 1 minuto. La Action tarda ~20-30s en ejecutarse.

**¿Cómo comparto la web con el grupo?**
Simplemente comparte la URL de GitHub Pages. No necesitan cuenta de GitHub.

**¿Puedo cambiar el nombre del archivo Excel?**
Sí, el script detecta automáticamente cualquier `.xlsx` en la raíz del repo.

**¿El repositorio tiene que ser público?**
Para GitHub Pages gratis, sí. Si quieres repo privado, necesitas GitHub Pro (o usar Netlify que permite repos privados gratis).
