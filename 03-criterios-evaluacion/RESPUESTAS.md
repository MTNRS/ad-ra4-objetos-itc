# Criterios RA4

| Criterio | Evidencia |
|---|---|
| a | README explica legibilidad, estructura, límites y concurrencia |
| b | Almacen abre y cierra mediante context manager; SQLite se cierra en finally |
| c | Cliente sin proyectos se guarda y recupera en la primera prueba |
| d | Cliente contiene una lista de Proyecto reconstruida desde YAML |
| e | consultar filtra objetos por nombre; ventana permite búsqueda |
| f | La ventana activa el cliente seleccionado y persiste el cambio |
| g | transaccion revierte memoria ante error y sustituye atómicamente el fichero |
| h | test_objetos prueba persistencia, modificación, rollback, cierre e integración |
