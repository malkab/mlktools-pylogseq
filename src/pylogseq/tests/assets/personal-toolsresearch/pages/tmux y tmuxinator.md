- [[tmux y tmuxinator]] es un multiplexor de consola, lo que permite tener varias consolas persistentes abiertas a la vez en una máquina. Imprescindible para mantener sesiones de trabajo en servidores remotos.
  title:: tmux y tmuxinator
- **Instalación y configuración:** desde paquetes. Instalar también **[[tmuxinator]]**, que es un gestor y configurador sobre [[tmux y tmuxinator]]
  collapsed:: true
  - ```shell
    # Ruby es para Tmuxinator
    apt-get install tmux ruby

    gem isntall tmuxinator
    ```
  - El fichero de configuración de [[tmux y tmuxinator]] es **~/.tmux.conf**. Tenemos templates en las plantillas **boilerplates/devops/system_setup_procedures**.
  - Las configuraciones de [[tmuxinator]] van a **~/.config/tmuxinator**
- # [[tmux]]: comandos
  - Algunos comandos CLI
    collapsed:: true
    - ```shell
      # Ver versión
      tmux -V

      # Ejecuta una nueva sesión sin nombre
      tmux

      # Ejecuta una nueva sesión con nombre
      tmux new -s basic

      # Ejecuta una nueva sesión con nombre,
      # como daemon (no entra en ella)
      tmux new -s session_namen -d

      # Ejecuta una nueva sesión con nombre y
      # creando una nueva ventana con nombre
      # shell
      tmux new -s windows -n shell

      # Lista de sesiones
      tmux list-sessions
      tmux ls

      # Abre una sesión, la última utilizada
      tmux attach
      tmux a

      # Abre una sesión con nombre
      tmux attach -t session_name
      tmux a -t session_name

      # Cierra una sesión con nombre
      tmux kill-session -t session_name
      ```
  - Comandos de sesión, que se lanzan con **Prefix + :**
    - **kill-session:** cerrar la sesión en curso
- # [[tmux]]: atajos de teclado
  - El prefijo por defecto es **Ctrl + b**
  - ## Sesiones anidadas y manejo de sesiones
    - **Prefix Prefix:** enviar prefix anidado
    - **Prefix + $:** renombrar sesión
    - **Prefix + d:** desvincularse de la sesión
  - ## Gestión de ventanas
    - **Prefix + c:** crear una nueva ventana
    - **Prefix + 1...0:** cambiar a ventana 1...0
    - **Prefix + w:** lista de ventanas (se puede navegar por ellas estilo Vim)
    - **Prefix + ,:** renombrar ventana
    - **Prefix + f:** buscar en ventana, busca texto en las ventanas, pero lamentablemente es sensible a mayúsculas
    - **Prefix + Ctrl h / Ctrl l:** moverse por las ventanas
    - **Prefix + &:** cerrar ventana
  - ## Gestión de paneles
    - **Prefix + l:** moverse al último panel
    - **Prefix + h / j / k / l:** moverse por los paneles, á la Vim
    - **Prefix + H / J / K / L:** redimensionar paneles, á la Vim, mantener presionado la mayúscula para redimensionar
    - **Prefix + o:** pasar por los paneles
    - **Prefix + |:** abrir panel vertical
    - **Prefix + -:** abrir panel horizontal
    - **Prefix + Ctrl o:** intercambiar paneles de posición
    - **Prefix + espacio:** ciclo de disposiciones de paneles
    - **Prefix + x:** cierre del panel
  - ## Modo edición y copy / paste
    - **Prefix [:** entrar en modo edición
    - **v:** en modo edición, seleccionar
    - **V:** en modo edición, selección de filas
    - **y:** copiar y sale de edición
    - [#C] **Prefix ]:** pegar en terminal, no funciona aún en el portapapeles de sistema, necesita configuración adicional #tmux
    - **h / j / k / l:** movimiento Vim
    - **Mays + Insert:** copiar el portapapeles del sistema en la terminal (no tiene nada que ver con tmux en realidad)
    - **/:** en edición, buscar, después utilizar **n** y **N** para ciclar resultados
  - ## Otros
    - **Prefix + l:** hace un _clear_ de la consola actual, muy útil porque limpia dentro de sesiones [[psql]], por ejemplo
    - **Prefix + ::** abrir modo comando, se puede introducir un comando (tiene autocomplete) en la sesión
    - **Prefix + ?:** mostrar atajos de teclado
    - **Prefix + r:** recargar configuración, para cuando se hacen cambios
- # [[tmux]] en servidores
  collapsed:: true
  - Se pueden crear sesiones de [[tmux]] anidadas en sesiones SSH de servidores. Tendremos entonces dos [[tmux]] anidados. Para mandarle comandos a la sesión remota, usar el doble prefijo **Prefix + b Prefix + b**.
  - Otra opción es, en una terminal sin [[tmux]] local, hacer SSH y abrir una en el remoto. No estarán anidadas y los comandos irán directos a la sesión en remoto. Para abrir directamente con SSH:
    - ```shell
      ssh -p 440 user@host -t tmux new -s session_name
      ssh -p 440 user@host -t tmux ls
      ssh -p 440 user@host -t tmux attach -t session_name
      ```
- # Copy / Paste
  collapsed:: true
  - Es un tema un poco jodido. Básicamente, utilizar **Prefix + [** para entrar en modo scroll. Tenemos que leer más de esto para sacarlo adelante.
  - [#C] Ver cómo configurar correctamente el COPY / PASTE en [[tmux]]
- # [[tmuxinator]]
  collapsed:: true
  - Comandos
    - ```shell
      # Listado de proyectos existentes
      tmuxinator ls

      # Crea un nuevo proyecto
      tmuxinator new [ project name ]

      # Edita un proyecto
      tmuxinator open [ project name ]

      # Lanza un proyecto como sesión
      tmuxinator start [ project name ]

      # Para una sesión
      tmuxinator stop [ project name ]
      ```
  - Configuración de ejemplo
    - ```shell
      name: master_us_bbddgg
      root: /Users/malkab/Dropbox/00-wip-work-in-progress/master_us_2019/didactica-master_us-asignatura_bbddgg-NUEVO

      windows:
        - folder: sleep .5 ; clear
        - postgis-psql: cd data_preparation/docker ; sleep 2 ; clear ; ./docker-psql.sh
        - grass-session: cd data_preparation/docker ; sleep .5 ; clear ; ./docker-grass.sh
        - postgis-data-preparation: cd data_preparation/docker && clear && ./docker-pg-run.sh
      ```
    - Tenemos más ejemplos por ahí, en **boilerplates** o donde sea
