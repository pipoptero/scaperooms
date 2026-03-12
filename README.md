# 🔐 The Vault — Escape Room Chronicles

Web interactiva para llevar el seguimiento de escape rooms. Se actualiza automáticamente al subir el Excel.

## 🗂 Estructura del repositorio

```
escape-rooms-tracker/
├── index.html                          ← La web (no tocar)
├── convert.py                          ← Script de conversión (no tocar)
├── data.json                           ← Generado automáticamente por la Action
├── escape_rooms_tracker_mejorado.xlsx  ← TU ARCHIVO EXCEL ← aquí actualizas
└── .github/
    └── workflows/
        └── update-data.yml             ← La GitHub Action (no tocar)
```

---

## 🚀 Configuración inicial (solo una vez)

### 1. Crear el repositorio en GitHub
- Ve a github.com → **New repository**
- Nombre: `escape-rooms-tracker` (o el que quieras)
- Visibilidad: **Public** (necesario para GitHub Pages gratis)
- No inicialices con README

### 2. Subir los archivos
Sube todos los archivos de esta carpeta al repo arrastrándolos desde la interfaz web de GitHub, o con Git desde terminal:
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
- En el repo: **Settings → Pages**
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
| Duración | Duración en minutos *(entero)* |
| Dificultad | Alta / Media-Alta / Media / Baja |
| Valoración | Rating de escapistas.com (0-10) *(acepta decimales: 8.5 o 8,5)* |
| Web | URL de la web |
| Max_personas | Número máximo de jugadores *(opcional)* |
| Descripción | Descripción breve del escape room *(opcional)* |
| Posición TERPECA | Posición en el ranking mundial TERPECA *(opcional, entero)* |

### Hoja «Hechos»
Mismas columnas que Pendientes (incluida Posición TERPECA), más:
| Columna | Descripción |
|---------|-------------|
| Valoración Grupo | Vuestra puntuación personal (0-10) *(acepta decimales: 9.2 o 9,2)* |
| Descripción | **Tu opinión/reseña personal** del escape *(opcional)* |
| Historia | Valoración de la historia (0-10) *(opcional)* |
| Ambientación | Valoración de la ambientación (0-10) *(opcional)* |
| Jugabilidad | Valoración de la jugabilidad (0-10) *(opcional)* |
| GameMaster | Valoración del game master (0-10) *(opcional)* |

> **Notas sobre el formato:**
> - Los valores numéricos con decimal deben escribirse con **punto** (`8.5`). El script también acepta coma (`8,5`) como fallback.
> - ⚠️ Si Excel muestra un valor decimal como una fecha (por ejemplo `8.9` aparece como `08/09/2026`), selecciona la celda, formato → **Número**, y vuelve a escribir el valor. El script detecta y corrige este problema automáticamente.
> - La columna Descripción puede llamarse: `Descripción`, `Descripcion`, `Description`, `Descripción del Escape` o `Resumen`.
> - Las columnas de categorías (Historia, Ambientación, Jugabilidad, GameMaster) son opcionales.
> - No dejes filas con cabeceras repetidas ni bloques de datos duplicados en el Excel — el script elimina duplicados automáticamente pero es mejor mantener el Excel limpio.

---

## 🖥 Vistas de la web

### Header — The Vault
Cabecera con estilo steampunk/metálico con el título **THE VAULT** y subtítulo *Escape Room Chronicles*.

Debajo del título, una **barra de estadísticas** muestra en tiempo real:
- Escapes completados, pendientes y total
- Media de valoración del grupo
- Horas totales jugadas
- **Barra de progreso animada** con % completado de la lista
- **Insights dinámicos:** mejor escape, empresa top, ciudad top y temática favorita — calculados automáticamente desde los datos del Excel

### Pestaña Pendientes
Cuadrícula de tarjetas con filtros por ciudad, dificultad y tipo. Ordenación por rating, nombre, duración o dificultad. Cada tarjeta incluye:
- **Logo circular** obtenido automáticamente del favicon de la web del escape
- Nombre, empresa
- Si tiene posición en el ranking TERPECA: **badge oficial TERPECA** con el número de posición debajo
- **♥ botón de favorito** con contador de likes de todos los usuarios
- Ciudad · Temática · **★ Rating** alineado a la derecha
- Tipo, descripción (si existe), duración, dificultad, máximo de jugadores
- Widget de votación con **medias estrellas** (nota 1-10)

El botón **♥ Favoritos (N)** en la barra de filtros muestra solo los escapes que tú has marcado.

### Pestaña Hechos
Vista de **reseñas** — cada escape ocupa una fila con tres columnas:
- **Izquierda:** posición en el ranking según votos de la comunidad (🥇🥈🥉 para el podio)
- **Centro:** logo circular + nombre + badge TERPECA si aplica, info técnica, puntuaciones (Escapistas / Grupo / Comunidad) y widget de votación
- **Derecha:** opinión personal (columna Descripción del Excel) y, si existen, **valoraciones por categorías** (Historia, Ambientación, Jugabilidad, Game Master) con estrellas visuales

### Pestaña Ranking
Tabla ordenada por **Valoración Grupo** (nota personal del Excel). Columnas: posición, nombre, empresa, temática, dificultad, duración, rating Escapistas, nota Grupo y **media de votos de la Comunidad** con número de votantes. La columna Comunidad solo aparece si Firebase está configurado.

---

## 🏆 Badge TERPECA

Si un escape tiene valor en la columna **Posición TERPECA**, se muestra automáticamente el logo oficial de los *Top Escape Rooms Project Enthusiasts' Choice Awards* con el número de posición debajo. Aparece tanto en Pendientes como en Hechos.

---

## ⭐ Sistema de votación con estrellas

Cada tarjeta incluye un widget de **medias estrellas**:
- 5 estrellas clicables, cada una con mitad izquierda (½ estrella) y mitad derecha (1 estrella)
- Permite dar notas del **1 al 10**
- Al pasar el ratón se previsualiza la nota antes de confirmar
- Muestra tu nota personal y la **media de la comunidad** con número de votantes
- El Ranking incluye la media comunitaria de cada escape
- Requiere Firebase configurado

---

## ♥ Sistema de favoritos / likes

Cada tarjeta de Pendientes tiene un botón **♥** junto al nombre:
- El corazón es gris si no lo has marcado, rojo si sí
- Debajo del corazón se muestra el **total de likes de todos los usuarios**
- Al pulsar se sincroniza con Firebase en tiempo real
- Tus favoritos se recuerdan entre visitas y dispositivos
- El botón **♥ Favoritos** en la barra de filtros muestra solo tus escapes marcados
- Sin Firebase, los favoritos se guardan solo localmente en el navegador

---

## 🔥 Configurar Firebase (votaciones y likes)

Firebase es gratuito y solo necesitas configurarlo una vez.

### 1. Crear proyecto
- Ve a [console.firebase.google.com](https://console.firebase.google.com)
- **Añadir proyecto** → nombre: `scapesrooms` → desactiva Analytics → **Crear proyecto**

### 2. Crear la base de datos
- Menú izquierdo: **Compilación → Realtime Database**
- **Crear una base de datos** → región: **Belgium (europe-west1)**
- Selecciona **Empezar en modo de prueba** → **Habilitar**

### 3. Copiar la URL
Verás una URL del tipo:
```
https://scapesrooms-default-rtdb.europe-west1.firebasedatabase.app
```

### 4. Pegar en index.html
Busca esta línea al inicio del `<script>`:
```js
const FIREBASE_URL = '';
```
Sustitúyela por:
```js
const FIREBASE_URL = 'https://scapesrooms-default-rtdb.europe-west1.firebasedatabase.app';
```
Guarda y sube el `index.html` a GitHub. ¡Listo! 🎉

### 5. Reglas de seguridad (importante — expiran en 30 días)
Ve a **Realtime Database → Reglas** y pega:
```json
{
  "rules": {
    "votes": {
      ".read": true,
      ".write": true
    },
    "likes": {
      ".read": true,
      ".write": true
    }
  }
}
```
Haz clic en **Publicar**.

### Estructura de datos en Firebase
```
tu-proyecto/
├── votes/
│   └── {slug_escape}/
│       └── {user_id}: 4.5        ← nota en estrellas (0.5–5)
└── likes/
    └── {slug_escape}/
        └── {user_id}: true       ← ha marcado favorito
```

---

## ❓ Preguntas frecuentes

**¿Cuánto tarda en actualizarse tras subir el Excel?**
Normalmente menos de 1 minuto. La Action tarda ~20-30s en ejecutarse.

**¿Cómo comparto la web con el grupo?**
Simplemente comparte la URL de GitHub Pages. No necesitan cuenta de GitHub ni registrarse.

**¿Puedo cambiar el nombre del archivo Excel?**
Sí, el script detecta automáticamente cualquier `.xlsx` en la raíz del repo.

**¿El repositorio tiene que ser público?**
Para GitHub Pages gratis, sí. Si quieres repo privado necesitas GitHub Pro, o puedes usar Netlify (permite repos privados gratis).

**La Action falla con error de permisos**
Ve a Settings → Actions → General → Workflow permissions y activa "Read and write permissions".

**La web muestra error 404 en data.json**
La Action aún no se ha ejecutado o falló. Ve a la pestaña Actions, comprueba el log y dale a "Re-run jobs" si es necesario.

**Las votaciones o likes no aparecen / dan error 401**
Ve a Firebase Console → Realtime Database → Reglas y asegúrate de tener los nodos `votes` y `likes` con `.read: true` y `.write: true` publicados.

**Los decimales en el Excel aparecen como fechas**
Es un problema de formato de celda en Excel. Selecciona la celda → formato → **Número** → vuelve a escribir el valor. El script lo detecta y corrige automáticamente.

**Aparecen escapes duplicados o un escape con nombre raro sin datos**
Revisa el Excel buscando filas de cabecera repetidas o bloques de datos pegados dos veces. El script elimina duplicados automáticamente y avisa en el log de la Action (`⚠ Duplicados eliminados: N`).

**El favicon/logo no aparece en alguna tarjeta**
Es normal si el escape no tiene web configurada en el Excel, o si la web no tiene favicon. Se muestra 🔐 como fallback automáticamente.
