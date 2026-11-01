# Acceso a datos · RA4 · Objetos ITC

Unidad 4: persistencia de objetos. Continúa las entidades clientes y proyectos
de RA2 y RA3 mediante un almacén YAML didáctico. Incluye ventana gráfica.

Instalar: `python -m pip install -r requirements.txt`.
Desde `02-proyecto-unidad`: `python app.py`.
Pruebas: `python -m unittest -v`.

La ventana importa la SQLite creada por C++ en RA2 o utilizada por el ORM de
RA3. Cada cliente se reconstruye como objeto con sus proyectos anidados.
La importación sustituye el almacén YAML tras confirmación y no modifica SQLite.
También permite buscar clientes y cambiar su estado a activo.

YAML permite inspeccionar objetos estructurados con facilidad, pero requiere
cargar el fichero completo y no proporciona índices ni concurrencia. Este
almacén está diseñado para un único proceso. Su transacción guarda una copia
en memoria y sustituye atómicamente el fichero al confirmar. No es una
transacción distribuida entre YAML y SQLite ni un gestor OODB completo.

Es un prototipo local de portabilidad para Integra Tech Consulting con datos
ficticios, sin conexión empresarial. Integrarlo requeriría permisos,
validación del modelo y pruebas en un entorno aislado.

## Uso de IA

Se ha utilizado asistencia de IA para implementar y revisar esta práctica.
El alumno debe ejecutar el programa, comprender el código y explicar sus
decisiones antes de entregar. Esa revisión personal sigue pendiente.
