- # Atajos de teclado en Linux
  collapsed:: true
  - **C** es control, **S** shift y **A** alt
  - Navegación de código
    - **Posición de cursor atrás:** C + A + -
    - **Posición de cursor adelante:** C + S + -
- # Extensiones
  collapsed:: true
  - Imprescindibles
    collapsed:: true
    - **AWS Toolkit (Amazon Web Services):** para enganchar con instancias AWS
    - **Bookmarks (Alessandro Fragnani):** bookmarks de código
    - **Debugger for Firefox (Firefox DevTools):** para depurar páginas sencillas HTML + CSS + JS en Firefox (para Chrome viene de serie)
    - **Dev Containers (Microsoft):** para la gestión de contenedores Docker de desarrollo
    - **Docker (Microsoft):** para la gestión de Docker
    - **GitHub Copilot (GitHub):** la IA
    - **GitLens - Git supercharged (GitKraken):** Git mejorado (creemos que tiene funcionalidad de pago)
    - **isort (Microsoft):** algo de Python (¿?)
    - **Jupyter (Microsoft):** para manejar Jupyter
    - **Jupyter Cell Tags (Microsoft):** algo de Jupyter (¿?)
    - **Jupyter Keymap (Microsoft):** ¿atajos de teclado para Jupyter?
    - **Jupyter Notebook Renderers (Microsoft):** ¿?
    - **Live Preview (Microsoft):** monta un servidor local HTTP para mostrar en tiempo real cambios en HTML + CSS + JavaScript
    - **Material Icon Theme (Philipp Kief):** mejores iconos
    - **Project Manager (Alessandro Fragnani):** imprescindible
    - **Pylance (Microsoft):** básico para el trabajo con [[Python]]
    - **Python (Microsoft):** utilidades para [[Python]]
    - **Remote - SSH (Microsoft):** para desarrollo remoto, imprescindible
    - **Remote - SSH: Editing Configuration Files (Microsoft):** para desarrollo remoto, imprescindible
    - **Remote Explorer (Microsoft):** para desarrollo remoto, otra vez imprescindible
    - **Rewrap (stkb):** rewrapeo suave de líneas
    - **YAML (Red Hat):** parseo de YAML
  - Otras opcionales, según el caso
    collapsed:: true
    - LaTeX language support
    - Lorem Ipsum
    - Mapfile Syntax
    - Mardown All in One
    - Modern Fortran
    - PostgreSQL
    - Prettier
    - Rainbow CSV
    - Dev Containers
    - Thunder Client
    - Word Count
    - C/C++
- # #HTML #CSS #JavaScript Depurar páginas web sencillas
  collapsed:: true
  - Para empezar, instalar la extensión **Debugger for Firefox (Firefox DevTools)** si se quiere utilizar ese navegador. Chrome viene ya de serie y no hay que instalar nada.
  - Instalar también la extensión **Live Preview (Microsoft)**, que permite ver en un panel lateral el HTML a medida que se escribe, muy útil. El workspace es accesible por navegador en **http://127.0.0.1:3000**.
  - Asumimos esta estructura de repo:
    - ```txt
      root
       +- src
           +- index.html
           +- js.js
           +- styles.css
      ```
  - Crear un fichero de perfiles de debugging con las entradas:
    - ```JSON
      {
        // Use IntelliSense to learn about possible attributes.
        // Hover to view descriptions of existing attributes.
        // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
        "version": "0.2.0",
        "configurations": [
          {
            "type": "firefox",
            "request": "launch",
            "reAttach": true,
            "name": "Firefox: index.html",
            "file": "${workspaceFolder}/src/index.html"
          },
          {
            "type": "chrome",
            "request": "launch",
            "name": "Chrome: index.html",
            "file": "${workspaceFolder}/src/index.html"
          }
        ]
      }
      ```
- #[[Dev Containers]]
  collapsed:: true
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
            "PYTHONPATH": "/workspaces/mlktools/whatever"
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
- # User Snippets
  - Ubicación de los snippets
    - En [[Linux]] `~/.config/Code/Users/snippets`
    - En [[MacOS]] `$HOME/Library/Application\ Support/Code/User/`
    - En [[Windows]] `%APPDATA%\Code\User\`
  - Los **snippets** se guardan en el [[G/boilerplates/boilerplates]] devops/system_setup_procedures/common, donde tiene un instalador para [[Linux]]
  - Para incluir un nuevo snippet, ir al repo de **boilerplates** y configurar el snippet allí. Después usar el script de instalación para instalarlo en el VSC local.
-
-
-
- #procesar A partir de aquí, por encima está correcto
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
- #procesar

  Python in Visual Studio Code
  ---
  __TAGS:__ visual, studio, code, python

  Install Python extension by Don Jayamanne. Configure environments:
- click Debug > Open configurations
- configure Python 2.7 and 3.6:

  `JSON
  {
  	"name": "Python PhD preprocessor",
  	"type": "python",
  	"request": "launch",
  	"stopOnEntry": false,
  	"args": ["--boilerplate"],
  	"pythonPath": "/usr/local/bin/python3.6",
  	"program": "/Users/git/phd-writing/src/preprocessor/preprocessor.py",
  	"cwd": "/Users/git/phd-writing/src/preprocessor",
  	"env": {},
  	"envFile": "${workspaceRoot}/.env",
  	"debugOptions": [
  "WaitOnAbnormalExit",
  "WaitOnNormalExit",
  "RedirectOutput"
  	],
  	"args": [ "/Users/git", "/Users/malkab/sysgit" ]
  },
  {
  	"name": "Python 2",
  	"type": "python",
  	"request": "launch",
  	"stopOnEntry": true,
  	"pythonPath": "/usr/local/bin/python2.7",
  	"program": "${file}",
  	"cwd": "${workspaceRoot}",
  	"env": {},
  	"envFile": "${workspaceRoot}/.env",
  	"debugOptions": [
  "WaitOnAbnormalExit",
  "WaitOnNormalExit",
  "RedirectOutput"
  	]
  }
  `

  Configurations are stored project-wise, along with settings overriding global config settings, in a .vscode folder. Git this folder.

  To run and debug, switch to the Debug section, select the desired configuration and run to your heart's content.


  Configuring Tasks in Visual Studio Code
  ---
  __TAGS:__ visual, studio, code, build, tasks

  Tasks allow the launching of arbitrary commands (like build commands, or build command run inside a Docker container). There are many different, platforms specific tasks (to transpile TypeScript, for example), but there is also the wide spectrum shell tasks:

  `JSON
  {
  	"taskName": "make pdf-introduccion",
  	"type": "shell",
  	"command": "build-commands/make_pdf-introduccion.sh",
  	"group": {
  "kind": "build",
  "isDefault": true
  	}
  }
  `

  Tasks are stored in project's workspace in .vscode/tasks.json, so Git it.







# Visual Studio Code

Wonderfull editor, for code, Markdown, and more.



## Debugging TypeScript

Check the boilerplate at Code Exampler **javascript/boilerplates/webpack-barebone-non-web** for a description on how to debug on a Docker container.



## Shortcuts

Useful shortcuts.



### Movement & Navigation

Movement is Vim-like with ctrl prefixed:

| Shortcut | Effect |
| -------- | ------ |
| CTRL + h / j / k / l | Cursor movement |
| Up | Window switcher |
| Down | Switch pane |
| Left | Move to the left file in pane |
| Right | Move to the right file in pane |
| CRTL + CMD + h / l | Move to words at left / right |
| CTRL + o | Insert line below |
| CTRL + SHIFT + o | Insert line above |
| CTRL + d CTRL + d | Delete line |
| CTRL + a | Move to end of line |
| CTRL + i | Move to start of line |
| CTRL + SHIFT + d | Delete to end of line |
| SHIFT + cursors | Selection |
| ALT + CMD + up / down | Multicursor |
| CRTL + x | Delete left |



### General

General:

| Shortcut | Effect |
| -------- | ------ |
| CMD + s | Save |
| CMD + k z | Toggle Zen mode |
| CMD + B | Toggle side bar |
| CMD + j | Toggle pane |
| CMD + w | Close tab / editor |
| CTRL + w | Switch window |
| CMD + w CMD + w | Next window |
| CMD + q CMD + q | Previous window |



# Remote File Editing

Use the **SSH FS** extension. Configure a remote point:

```JSON
"sshfs.configs": [
	{
"label": "Docker PostGIS compilation",
"root": "/home/malkab/compilation",
"host": "sheep",
"port": 22,
"name": "dockerpostgiscompilation",
"username": "malkab",
"password": true
	}
]
```

That’s all. Connect and use as folder.
# VVVVVVV DEPRECATE VVVVVVV
## Shortcuts
---------
__TAGS:__ visual, studio, code, shortcuts

| Shortcut | Effect |
| -------- | ------ |

| Cycle files in group | Ctrl+Tab |
| Box select | Shift+Cmd+Alt+Keys (ESC to exit) |
| Move between terminal and window | Ctrl+` |
| Snippets | Ctrl+Space |


Python in Visual Studio Code
---
__TAGS:__ visual, studio, code, python

Install Python extension by Don Jayamanne. Configure environments:
- click Debug > Open configurations
- configure Python 2.7 and 3.6:

  `JSON
  {
  	"name": "Python PhD preprocessor",
  	"type": "python",
  	"request": "launch",
  	"stopOnEntry": false,
  	"args": ["--boilerplate"],
  	"pythonPath": "/usr/local/bin/python3.6",
  	"program": "/Users/git/phd-writing/src/preprocessor/preprocessor.py",
  	"cwd": "/Users/git/phd-writing/src/preprocessor",
  	"env": {},
  	"envFile": "${workspaceRoot}/.env",
  	"debugOptions": [
  "WaitOnAbnormalExit",
  "WaitOnNormalExit",
  "RedirectOutput"
  	],
  	"args": [ "/Users/git", "/Users/malkab/sysgit" ]
  },
  {
  	"name": "Python 2",
  	"type": "python",
  	"request": "launch",
  	"stopOnEntry": true,
  	"pythonPath": "/usr/local/bin/python2.7",
  	"program": "${file}",
  	"cwd": "${workspaceRoot}",
  	"env": {},
  	"envFile": "${workspaceRoot}/.env",
  	"debugOptions": [
  "WaitOnAbnormalExit",
  "WaitOnNormalExit",
  "RedirectOutput"
  	]
  }
  `

  Configurations are stored project-wise, along with settings overriding global config settings, in a .vscode folder. Git this folder.

  To run and debug, switch to the Debug section, select the desired configuration and run to your heart's content.


  Configuring Tasks in Visual Studio Code
  ---
  __TAGS:__ visual, studio, code, build, tasks

  Tasks allow the launching of arbitrary commands (like build commands, or build command run inside a Docker container). There are many different, platforms specific tasks (to transpile TypeScript, for example), but there is also the wide spectrum shell tasks:

  `JSON
  {
  	"taskName": "make pdf-introduccion",
  	"type": "shell",
  	"command": "build-commands/make_pdf-introduccion.sh",
  	"group": {
  "kind": "build",
  "isDefault": true
  	}
  }
  `

  Tasks are stored in project's workspace in .vscode/tasks.json, so Git it.
