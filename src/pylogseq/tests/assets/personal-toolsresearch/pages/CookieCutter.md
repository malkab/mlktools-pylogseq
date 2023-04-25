- Es una herramienta para gestionar templates
- Tenemos un ejemplo en [[G/boilerplates/cookiecutter]] llamado **cookiecutter-test** y un ejemplo de los desarrolladores llamado **cookiecutter-example**
- El [[G/boilerplates/cookiecutter]] tiene los templates. Es práctico hacerle un **ln -s** a este directorio a **~** para hacer cómodo el acceso
  - ```shell
    ln -s /home/git/boilerplates/boilerplates-cookiecutter /home/malkab/cookiecutter

    cookiecutter ~/cookiecutter/whaterver
    ```
- # Instalación
  collapsed:: true
  - Se instala en el sistema host
    ```shell
    python3 -m pip install --user cookiecutter
    ```
- # Utilización
  collapsed:: true
  - Simplemente apuntar al directorio que contiene la template
    ```shell
    cookiecutter /home/git/boilerplates/boilerplates/whatever
    ```
