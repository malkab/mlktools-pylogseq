- #procesar
- User Snippets
  collapsed:: true
  - Ubicación de los snippets
    - En [[Linux]] `~/.config/Code/Users/snippets`
    - En [[MacOS]] `$HOME/Library/Application\ Support/Code/User/`
    - En [[Windows]] `%APPDATA%\Code\User\`
  - Los **snippets** se guardan en el [[GitRepo/boilerplates/boilerplates]] devops/system_setup_procedures/common, donde tiene un instalador para [[Linux]]
- **Extensiones**
  collapsed:: true
  - AWS Toolkit
  - Bookmarks
  - C/C++
  - Color Info
  - CSS Peek
  - Docker
  - GitLens
  - HTTP Server / HTML Preview
  - Jupyter
  - Jupyter Keymap
  - Jupyter Notebook Renderers
  - LaTeX language support
  - Live Server
  - Lorem Ipsum
  - Mapfile Syntax
  - Mardown All in One
  - Material Icon Theme
  - Modern Fortran
  - PostgreSQL
  - Prettier
  - Project Manager
  - Pylance
  - Python
  - Rainbow CSV
  - Dev Containers
  - Remote - SSH
  - Remote - SSH: Editing Configuration Files
  - Rewrap
  - Thunder Client
  - Word Count
- #[[Dev Containers]]
  - Los contenedores de desarrollo ([[Dev Containers]]) permite guardar en los proyectos las imágenes [[Docker]] que se utilizan para desarrollar un proyecto
  - A partir de estas definiciones se crea una imagen [[Docker]] que genera un contenedor en el que se inyecta el directorio del proyecto
  - Lo bueno es que a esos contenedores, que pueden partir de cualquier imagen ya existente (no hay que heredar ninguna imagen base ni necesita nada especial) se pueden instalar extensiones de VSC para poder, por ejemplo, depurar lenguajes como [[Python]] dentro del contenedor
  - En su forma más simple, los directorios de proyecto deben contener un directorio **.devcontainer** donde va el entorno y la definición de la imagen. Se puede incluso contener un **Dockerfile** para generar la imagen, pero en nuestro caso es mejor partir de una imagen que se pueda utilizar autónomamente e instalarle simplemente extensiones de VSC.
  - Aunque existe documentada la opción de usar un **Docker Compose**, no hemos conseguido hacerlo bien, así que cualquier infraestructura (bases de datos, etc.) se definirá en un **Compose** externo con una network attachable a la que el Dev Container se podrá conectar (ver abajo). Sin embargo, esto se ve severamente afectado por la limitación comentada más abajo.
  - La definición de la imagen del dev container se hace con un simple fichero JSON llamado **devcontainer.json**. En ella se define la imagen a utilizar, las extensiones VSCode a instalar, el usuario y argumentos de ejecución adicionales en **runArgs**. Ahí, por ejemplo, se puede designar la red de un **Compose** externo que sea attacheable. El Compose está definido y levantado externamente (con **compose up**) a VSCODE.
    - devcontainer.json
      - ```JSON
        {
          "image": "malkab/python:3.9-buster",
        
          "runArgs": [
            "--network=network_name"
          ],
        
          "customizations": {
            "vscode": {
              "extensions": [ "ms-python.python" ]
            }
          },
        
          "containerEnv": {
            "PYTHONPATH": "/workspaces/mlktools/pylogseq"
          },
        
          "remoteUser": "1000",
        
          "postCreateCommand": "bash -c \"sudo apt-get update ; pip install something\""
        }
        ```
    - docker-compose.yaml
      - ```yaml
        version: '3.5'
        
        networks:
          the_network:
            external: false
            name: network_name
            attachable: true
        
        services:
          postgis:
            image: malkab/postgis:holistic_hornet
            container_name: x_postgis
        
            networks:
              - the_network
        
            ports:
              - "5432:5432"
        
            volumes:
              - ../docker-volumes/x_postgis:/data
        
        ```
  - **Limitación:** sólo existe un problema con esta forma de proceder. La red que crea el **Compose** tiene un código que es al que intenta conectarse el dev container, en lugar de conectar directamente al nombre. Si el Compose se destruye con **compose down** la red cae, y si se rehace, ésta tendrá un ID distinto. El dev container no se conectará porque busca el ID antiguo. Hay que reconectar el dev container con la nueva red:
    ```shell
    docker network connect [nombre red] [ID dev container]
    ```
    y entonces ya arrancará el dev container de nuevo. Otra forma de arreglarlo es no destruir durante una buena temporada ni el Compose ni el Dev Container. Rehacerlo todo de nuevo es otra forma de volver a ponerlo todo en pié.
  - Sobre esta definición se creará primero una imagen y después un contenedor. Este contenedor es persistente y se quedará en el sistema hasta que sea borrado. Eso quiere decir que lo que se le haga al contenedor, como por ejemplo la instalación de paquetes **PIP**, persistirá. Por lo tanto, hay **dos niveles de persistencia**: lo que se le haga a la imagen y lo que se le haga al contenedor. El parámetro de configuración **postCreateCommand** sirve para lanzar un script que instale software adicional en el Dev Container.
  - Estas características hacen obsoleto el uso del **virtualenv**.
  - #Web/Herramientas #Web/Docker Algunos enlaces útiles
    - [devcontainer.json reference](https://containers.dev/implementors/json_reference/)
  - #Web/Herramientas #Web/Docker Algunas imágenes de desarrollo útiles
    - [GitHub - malkab/docker-python: A heavy Docker for Python development and tinkering. Installs some key libraries and componentes.](https://github.com/malkab/docker-python)
    - [GitHub - malkab/docker-grass: A GRASS and general purpose GIS image.](https://github.com/malkab/docker-grass)
    - [GitHub - malkab/docker-node_js_dev: Node.js development image.](https://github.com/malkab/docker-node_js_dev)
- **Atajos de teclado en Linux** #TODO
  collapsed:: true
  - **C** es CTRL, **S** es SHIFT y **A** es ALT
  - **Vistas**
    | **Atajo** | **Efecto** |
    | --- | --- |
    | **C+o C+o** | Abrir **Outline** |
    | g | v |
  -
  - ```shell
    ## Use of the Search Box
    
    Invoke with **C + S + p** (Command selection):
    
    - prefix with **>** for looking for a command;
    
    - prefix with **@** for looking for a symbol in current file (depends on the context);
    
    - prefix with **#** for looking for a symbol in current workspace (depends on context);
    
    - prefix with **:** for jumping to a line;
    
    
    - without prefix for looking for a file.
    
    
    ## General Shortcuts
    
    These are the good ones:
    
    Shortcut           | Effect
    ------------------ | ----------------------
    C + s              | Save
    C + k C + s        | Open keyboard shortcuts
    
    
    ## Project Files and Symbols Search
    
    To look for files or symbols in the current workspace, several shortcuts are available, although all of them do the same:
    
    Shortcut         | Effect
    ---------------- | -----------------------------
    C + S + o        | Search symbol in current file
    CTRL + t         | Search symbol in all files
    C + e            | Open file in workspace
    
    
    ## Editing & Navigation Text
    
    Shortcut             | Effect
    -------------------- | ---------------------
    C + up / down        | Scroll text without changing the cursor line
    C + left / right     | Move cursor word
    C + S + arrows       | Cursor selection
    C + S + up / down    | Multicursor or line selection once a selection has started
    C + S + l            | Given a selection, get a multicursor on all ocurrences
    C + k C + c          | Comment selection
    C + k C + u          | Uncomment selection
    C + z                | New empty line
    C + space            | Snippets
    
    
    ## Environment Navigation Shortcuts
    
    Shortcuts to navigate the VSC environment.
    
    Panes and Modes:
    
    Windows:
    
    Shortcut        | Effect
    --------------- | ---------------
    C + S + n       | New window
    C + w w         | Window selector
    
    
    ## Console
    
    To work with the console, the current line can be executed on it. To
    execute the current file, this has to be saved to disk and have run
    permissions.
    
    In the terminal a Docker bash container can be launched. Mount the local
    folder with the same path:
    
    ```
    
    This will allow to both launch lines against the Docker console or the
    file itself, making for a very integrated experience.
    
    Console specific shortcuts:
    
    | Shortcut                      | Effect                            |
    | ----------------------------- | --------------------------------- |
    | CTRL + \`                     | Move between terminal and window  |
    | CMD + k                       | Clear                             |
    | CMD + SHIFT + c               | Open external terminal            |
    | CTRL + SHIFT + \`             | Create new terminal               |
    | CMD + ALT + PageUp / PageDown | Scroll                            |
    | CMD + Home / End              | Scroll to start / end             |
    | (CTRL + SHIFT + T) x 2        | Run current line or selected code |
    |                               | in current terminal               |
    | (CTRL + SHIFT + F) x 2        | Run file in terminal              |
    | ALT + p                       | Toggle panel position             |
    | CTRL + CMD + arrows           | Resize console                    |
## Markdown Shortcuts

 | Shortcut       | Effect      |
 | -------------- | ----------- |
 | CTRL + CMD + b | Toggle bold |

 ```