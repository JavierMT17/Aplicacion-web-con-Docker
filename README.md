# Aplicación de Login con Docker y HTTPS

Una aplicación web sencilla con registro, inicio de sesión y cierre de sesión. La aplicación usa Flask y PostgreSQL, y se despliega con Docker Compose.

## Características

- Registro de usuario.
- Inicio de sesión con validación de contraseña.
- Cierre de sesión.
- Usuarios almacenados en PostgreSQL.
- Servidor HTTPS con certificado autofirmado.
- Arquitectura con contenedor web y contenedor de base de datos.

## Estructura del proyecto

- `docker-compose.yml` - Define los servicios `web` y `db`.
- `app/Dockerfile` - Construye la aplicación Flask.
- `app/app.py` - Código de la aplicación.
- `app/templates/` - Plantillas HTML.
- `app/static/style.css` - Estilos de la aplicación.
- `app/entrypoint.sh` - Genera el certificado SSL y arranca la app.

## Requisitos

- Docker
- Docker Compose

## Cómo ejecutar

1. Clona el repositorio: 
```bash
git clone https://github.com/JavierMT17/Aplicacion-web-con-Docker.git
```
2. Abre una terminal en el directorio clonado.
3. Ejecuta:

```bash
docker-compose up -d
```

4. Abre en tu navegador:

```text
https://localhost:8443
```

> En algunos navegadores aparecerá una advertencia porque el certificado es autofirmado. Puedes aceptar el riesgo para continuar.

## Uso

1. Registra un nuevo usuario desde la pantalla de registro.
2. Ve al formulario de login y accede con el usuario registrado.
3. Si ingresas contraseña incorrecta, se mostrará un error y podrás intentarlo de nuevo.
4. Una vez dentro, haz clic en "Cerrar sesión" para volver al login.

## Notas

- La base de datos PostgreSQL se monta en un volumen llamado `db_data`.
- La aplicación crea tablas automáticamente cuando arranca.
- El servidor web se expone con HTTPS en el puerto `8443`.
