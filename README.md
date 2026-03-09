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

---

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

### 3. Activar permisos de la Action
- En el repo: **Settings → Actions → General → Workflow permissions**
- Selecciona **"Read and write permissions"** → **Save**

### 4. Activar GitHub Pages
- En el repo: **Settings** → **Pages**
- Source: **Deploy from a branch**
- Branch: `main` / folder: `/ (root)`
- Guarda → en ~2 minutos tendrás una URL del tipo:
  `https://TU_USUARIO.github.io/escape-rooms-tracker`

### 5. Primera ejecución de la Action
Al subir el Excel por primera vez, la Action se ejecutará automáticamente y generará `data.json`. Puedes seguirlo en la pestaña **Actions** del repo.

---

## 🔄 Flujo de actualización (uso diario)

1. **Edita tu Excel** localmente (añade rooms, cambia valoraciones, añade opiniones...)
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
| Descripción | Descripción breve del escape room *(opcional)* |

### Hoja «Hechos»
Mismas columnas que Pendientes, más:
| Columna | Descripción |
|---------|-------------|
| Valoración Grupo | Vuestra puntuación (0-10) |
| Descripción | **Tu opinión/reseña personal** del escape room *(opcional)* |

> **Nota sobre la columna Descripción:**
> - En **Pendientes** se muestra como descripción informativa en la tarjeta.
> - En **Hechos** se muestra como **reseña personal** en una vista expandida tipo revista.
> - Puede llamarse: `Descripción`, `Descripcion`, `Description`, `Descripción del Escape` o `Resumen`.

---

## 🖥 Vistas de la web

### Pestaña Pendientes
Cuadrícula de tarjetas con filtros por ciudad, dificultad y tipo. Ordenación por rating, nombre, duración o dificultad. Incluye widget de votación con **medias estrellas** (nota del 1 al 10 en pasos de 1).

### Pestaña Hechos
Vista de **reseñas** — cada escape ocupa una fila dividida en tres columnas:
- **Izquierda:** posición en el ranking (🥇🥈🥉 para el podio)
- **Centro:** info técnica completa + puntuaciones (Escapistas / Grupo / Comunidad) + widget de votación
- **Derecha:** tu opinión personal extraída de la columna Descripción del Excel

### Pestaña Ranking
Tabla comparativa de todos los hechos con columnas: posición, nombre, empresa, temática, dificultad, duración, rating Escapistas, nota del Grupo y **media de votos de la Comunidad** (con número de votantes entre paréntesis). La columna Comunidad solo aparece si Firebase está configurado.

---

## ⭐ Sistema de votación

Cada tarjeta (Pendientes y Hechos) incluye un widget de **medias estrellas**:
- 5 estrellas clicables, cada una dividida en mitad izquierda (½ estrella) y mitad derecha (estrella entera)
- Permite notas del **1 al 10 en pasos de 1** (pasando por las medias: 1, 2, 3... 10, pero también 3, 5, 7...)
- Al pasar el ratón se previsualiza la nota antes de votar
- Muestra tu nota y la **media de la comunidad** con número de votos
- Los votos se guardan en Firebase en tiempo real

---

## 🔥 Configurar votaciones con Firebase

Las votaciones requieren una base de datos gratuita de Firebase. Solo necesitas configurarla una vez.

### 1. Crear proyecto Firebase
- Ve a [console.firebase.google.com](https://console.firebase.google.com)
- Haz clic en **Añadir proyecto** → ponle un nombre (ej: `scapesrooms`)
- Desactiva Google Analytics (no hace falta) → **Crear proyecto**

### 2. Crear la base de datos
- En el menú izquierdo: **Compilación → Realtime Database**
- Haz clic en **Crear una base de datos**
- Elige la región: **Belgium (europe-west1)**
- Selecciona **Empezar en modo de prueba** → **Habilitar**

### 3. Copiar la URL de la base de datos
Verás una URL del tipo:
```
https://scapesrooms-default-rtdb.europe-west1.firebasedatabase.app
```
Cópiala.

### 4. Pegar la URL en index.html
Abre `index.html` y busca esta línea (está al principio del `<script>`):
```js
const FIREBASE_URL = '';
```
Sustitúyela por:
```js
const FIREBASE_URL = 'https://scapesrooms-default-rtdb.europe-west1.firebasedatabase.app';
```
Guarda y sube el archivo a GitHub. ¡Listo! 🎉

### 5. Reglas de seguridad (importante)
El modo prueba expira en 30 días. Para uso permanente ve a **Realtime Database → Reglas** y pega esto:
```json
{
  "rules": {
    "votes": {
      ".read": true,
      ".write": true
    }
  }
}
```
Haz clic en **Publicar**.

### ¿Cómo funciona el sistema de votación?
- Cada persona que abre la web tiene un **ID anónimo** generado automáticamente en su navegador (no hace falta registrarse)
- Pueden votar con medias estrellas → nota del 1 al 10
- Pueden cambiar su voto en cualquier momento
- Cada tarjeta muestra la **media de la comunidad** y el número de votantes
- El **Ranking** tiene una columna extra con la media comunitaria de cada escape
- Los votos se guardan en Firebase en tiempo real

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

**La Action falla con error de permisos**
Ve a Settings → Actions → General → Workflow permissions y activa "Read and write permissions".

**La web muestra error 404 en data.json**
La Action aún no se ha ejecutado o falló. Ve a la pestaña Actions, comprueba el log y si es necesario dale a "Re-run jobs".

**Las votaciones no aparecen**
Asegúrate de haber puesto la URL de Firebase en `index.html` y de haber subido el archivo actualizado al repo.
