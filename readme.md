# Trabajo Practico N°2 Cvs 

## Instalación
1. Clona el repositorio.
2. Crea un entorno virtual en la misma carpeta utilizando el comando:
   ```cmd
   virtualenv {nombre_del_entorno}
   ``` 
3. Ingresa a la dirección del archivo `activate` con el comando:
   ```cmd
   cd {nombre_del_entorno}/Scripts
   ```
4. Activa el entorno con el siguiente comando (CMD):
   ```cmd
   .\activate
   ```
5. Vuelve a la carpeta del proyecto con el comando:
   ```cmd
   cd ../..
   ```
6. Instala el driver de MySQL con el comando:
   ```cmd
   pip install mysqlclient
   ```
7. Antes de ejecutar el código, asegúrate de crear una base de datos con el nombre `localprovdb` en la base de datos MariaDB, incluida en el paquete de XAMPP.
8. Por último, ejecuta el archivo:
   ```cmd
   python app.py
   ```
   Una vez realizados estos pasos, se crearán los archivos CSV en la carpeta `localidad_provincia`.