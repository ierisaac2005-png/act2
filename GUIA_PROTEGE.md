# Completar la actividad en Protégé

El OWL ya contiene el diseño y los casos. Estos pasos permiten revisarlo en la herramienta solicitada y obtener la imagen requerida. La ejecución previa con Python no sustituye esta parte de la actividad.

## Abrir y revisar

1. Instalar Protégé Desktop desde https://protege.stanford.edu/software/ y abrirlo.
2. Seleccionar **File → Open** y abrir `softtek_soporte_ti.owl`.
3. En **Classes**, revisar las seis clases principales y las cuatro subclases. `owl:Thing` es la raíz estándar, no una clase adicional diseñada para la actividad.
4. En **Object Properties**, seleccionar cada una de las siete propiedades y comprobar **Domain** y **Range** con la tabla del README.
5. En **Data Properties**, revisar los tipos y la característica funcional de las diez propiedades.
6. En **Individuals**, abrir `INC001`, `AnaTorres` y `ProcedimientoAcceso` y revisar sus valores y relaciones. Los nombres exactos de las pestañas pueden variar según la distribución.

## Ejecutar el razonador

1. En el menú **Reasoner**, elegir **HermiT** si está disponible y luego **Start reasoner**. Si ya está iniciado después de un cambio, sincronizarlo.
2. Confirmar que no se informa una inconsistencia. Revisar también que ninguna clase propia aparezca bajo `owl:Nothing` en la jerarquía inferida.
3. Revisar que `PortalClientes`, declarado como `Aplicacion`, también pertenece a `Sistema`; y que `ProcedimientoAcceso` pertenece a `Documento` por su tipo `Procedimiento`.
4. Si se modifica el modelo, volver a ejecutar o sincronizar el razonador antes de guardar.

## Generar la imagen en OntoGraf

1. Activar **Window → Tabs → OntoGraf**. La documentación del proyecto indica que OntoGraf viene incluido en la instalación estándar de Protégé Desktop.
2. Buscar y añadir al gráfico `Tecnico`, `Incidente`, `Sistema`, `Documento`, `Herramienta` y `Area`.
3. Expandir los nodos y habilitar las relaciones relevantes en los filtros. Mostrar las conexiones de dominio/rango y las subclases; no dejar únicamente la jerarquía.
4. Para mostrar relaciones concretas, añadir también los individuos de INC001 y expandir sus conexiones: `AnaTorres`, `ConsolaIdentidad`, `MesaServicio`, `INC001`, `ProcedimientoAcceso`, `PortalClientes` y `ServidorAplicaciones`.
5. Ajustar el diseño, zoom y posición de los nodos para que los nombres y relaciones sean legibles. Comprobar que los filtros no oculten las relaciones que se quieren mostrar.
6. Usar la función de guardar el grafo como imagen de la barra de OntoGraf, elegir PNG y guardar como `grafo_ontograf.png`. Identificar el botón por su descripción emergente; su icono puede cambiar según la versión.

La imagen debe mostrar conceptos, relaciones y estructura general. Una captura de la lista de clases por sí sola no cumple ese objetivo. Si la vista combinada queda demasiado cargada, exportar un esquema de clases y otra vista de individuos.

## Guardar el modelo y subir al repo nuevo

1. Guardar desde **File → Save as**, manteniendo el nombre `softtek_soporte_ti.owl` y seleccionando RDF/XML si se solicita un formato.
2. Conservar el espacio de nombres y no reemplazarlo por el enlace de un repositorio inexistente.
3. Subir el OWL guardado y `grafo_ontograf.png` junto con el README y los demás archivos de esta actividad, en un repositorio independiente.
4. Agregar al README `![Visualización en Protégé](grafo_ontograf.png)` y actualizar la tabla de requisitos solo después de realizar esos pasos.

No hace falta un botón de Colab para revisar esta entrega: la herramienta principal solicitada es Protégé Desktop. El script de Python es una comprobación adicional.

Documentación de la herramienta: https://github.com/protegeproject/ontograf y https://protegewiki.stanford.edu/wiki/OntoGraf
