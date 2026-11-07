# Aprendido en el desarrollo del proyecto

## Docker 

### `docker compose config`
Este comando nos permite checar si la sintaxis es correcta para nuestro archivo `.yml` antes de intentar levantar los servicios. Valida la indentación, variables y volúmenes definidos.

### `docker compose up -d <servicio>`
Levanta los contenedores en segundo plano (`-d` significa *detached mode*), liberando la terminal. Si especificas el nombre de un servicio al final (ej. `docker compose up -d minio`), Docker levantará únicamente ese contenedor y las dependencias que tenga configuradas en su `depends_on`. *(Nota: Se usa `docker compose` sin repetir la palabra docker)*.

### `docker compose down`
Detiene y elimina los contenedores, redes y volúmenes internos creados por el archivo de Compose. Es ideal para limpiar el entorno cuando terminas de trabajar. Si quieres borrar también los volúmenes persistentes globales, puedes usar `docker compose down -v`.

### `docker compose ps`
Muestra el estado actual de los contenedores de este proyecto (si están corriendo, detenidos o reiniciándose) y qué puertos tienen expuestos hacia tu máquina.

### Variables de Entorno (Interpolación)
Permiten pasar datos dinámicos desde tu máquina o desde un archivo `.env` hacia el contenedor usando dos reglas clave:
* **`${VARIABLE:-defecto}` (Opcional):** Si la variable no está definida, Docker usa el valor por `defecto`. Se usa para configuraciones comunes (ej. usuarios o puertos).
* **`${VARIABLE:?Mensaje}` (Obligatoria):** Si la variable no existe, Docker detiene la ejecución por seguridad y muestra el `Mensaje` en la terminal. Se usa para datos sensibles (ej. contraseñas o tokens).
