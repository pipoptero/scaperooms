# Cambios aplicados

Archivo modificado: `index.html`

## Qué se ha cambiado

1. **CSS responsive para la sección Ranking**
   - En pantallas de hasta 760px, la tabla del ranking deja de comportarse como una tabla clásica.
   - Cada fila pasa a visualizarse como una tarjeta vertical.
   - Se oculta la cabecera (`thead`) en móvil.
   - Cada celda muestra su etiqueta mediante `data-label`.
   - El nombre del escape y la posición quedan destacados para mejorar la lectura en móvil.

2. **Render del ranking**
   - Se ha actualizado `renderRanking()` para añadir `data-label` en cada `<td>`.
   - Se han sustituido estilos inline importantes por clases CSS:
     - `rank-room-name`
     - `rank-score-group`
     - `rank-score-community`
     - `comm-avg`
     - `comm-count`
     - `comm-empty`
   - Se mantiene la lógica existente:
     - Orden por `Valoración Grupo`.
     - Podio con medallas.
     - Columna Comunidad solo si Firebase está configurado.
     - Uso de `voteStats()` y `slugify()` sin cambios.

## Archivos incluidos

- `index.html`: versión ya modificada y lista para subir al repositorio.
- `README_CAMBIOS_APLICADOS.md`: este resumen.
- `index.diff`: diff aproximado respecto al archivo original subido.

## Cómo aplicarlo

Sustituye tu `index.html` actual por el `index.html` incluido en este ZIP y súbelo a GitHub.

GitHub Pages debería reflejar el cambio tras refrescar/desplegar.
