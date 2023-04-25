- # Atajos de teclado
  collapsed:: true
  - Capturas de pantalla
    collapsed:: true
    - **Impr pant:** interfaz general de captura
    - **Shift + Impr pant:** todos los monitores
    - **Alt + Impr pant:** ventana activa
  - Atajos de teclado de sistema
    collapsed:: true
    - **Super + A:** ver todas las aplicaciones
    - **Super + D:** ver el escritorio
    - **Custom Shortcuts:** en Settings / Keyboard / Custom Shortcuts
      collapsed:: true
      - **Super + Z:** Gnome Clocks
      - **Super + W:** Firefox
      - **Super + L:** Logseq
      - **Super + T:** Terminal
      - **Super + C:** VSC
- # Aplicaciones
  collapsed:: true
  - **apt-file:** buscador de ficheros dentro de los paquetes. Instalar con apt y actualizar con **apt-file update**.
  - **[[Dadroit JSON Viewer]]:** un visualizador de JSON muy potente, descargable desde la página del desarrollador, [Dadroit JSON Viewer](https://dadroit.com/). De todas formas, tenemos una copia funcional en **D/app-repository/linux**, por si acaso desapareciera. Necesita tener instalado **fuse** para funcionar (apt install fuse). Es un [[AppImage]], se hace ejecutable y se copia a /usr/local/bin y ya está.
  - **Firefox:** instalar desde el descargable que proporcionan ellos, instalar desde apt el módulo **ubuntu-restricted-extras** para poder escuchar Ivoox.
  - **gnome-clocks:** alarmas, timers, etc. para [[Gnome]], instalar desde apt.
  - **gnome-sushi:** el previsualizador para Nautilus, instalar con apt.
  - **[[jq]]:** una herramienta de línea de comando para hacer manipulaciones de JSON, muy impresionante. Instalar con apt (jq).
  - **locate:** paquete que tiene el **updatedb** y el **locate**. Instalar con apt.
  - **Settings:** muchas veces los Settings se van. Reinstalar con **apt-get install gnome-control-center**.
  - **Variety:** gestión de wallpapers, instalar con apt.
- # Versión
  collapsed:: true
  - ```shell
    lsb_release -a
    lsb_release -r
    uname -a
    uname -r
    uname -m
    uname -s
    ```
- # Inicializar un nuevo desktop Linux
  collapsed:: true
  - [Versiones de Ubuntu](https://wiki.ubuntu.com/Releases).
  - Estos pasos fueron probados por última vez en una **Ubuntu 22.04.02 Jammy Jellyfish** en abril de 2023.
  - ## En la máquina saliente
      + [ ] do a **mount** to check mounted file systems;
      + [ ] enter into all of them and perform a **mlkhdsizes** to recover any valuable data;
      + [ ] if possible, commit all git repos;
      + [ ] move the Git folder;
      + [ ] Descargar las configuraciones clave con el script **mlklinuxdesktopbackupessentials** de **mlktools-scripts**, con **.gnupg** y zipeada (opciones -g -c), generando un **backup_essentials.tar.bz2**.
      + [ ] check Desktop and Downloads;
      + [ ] make sure Dropbox is fully sync and disconnect;
      + [ ] delete any sensitive info, or format.
  - ## En la máquina entrante
    tátil con este repo y el móvil para autenticar servicios.
      + [X] Descargar la **ISO** de la distribución y grabarla en un USB de 4 - 7 GB ([Create a bootable USB stick on Ubuntu | Ubuntu](https://ubuntu.com/tutorials/create-a-usb-stick-on-ubuntu#3-launch-startup-disk-creator)).
      + [X] Pinchar el USB en la máquina a inicializar y administrar desde la BIOS la secuencia de arranque.
      + [X] **Configurar particiones:** el boot loader tiene que estar en la unidad de arranque, crear una partición de 5 MB **Reserved BIOS boot area**, una partición de 245 MB **EFI System Partition**, otra principal donde se monta / de tipo **EXT4** y finalmente la **SWAP**.
      + [X] **Montar** unidades adicionales en **/mnt**.
      + [X] Make sure with **id** that the current user is uid:gid 1000:1000 to map Docker.
      + [X] Configurar la **IP estática** con el Network Manager de Ubuntu y reiniciar.
      + [ ] Instalar paquetes:
    
        ```shell
    apt-get install ssh net-tools tmux git
    ```
      + [X] Create the **git** folder and assign ownership to 1000:1000.
      + [X] Clonar el directorio **git** de la máquina saliente.
      + [X] Sincronizar Firefox con la cuenta de usuario y habilitar extensiones.
      + [X] Generate an SSH key to identify the machine. Create the .ssh folder if needed. Autorizar la nueva máquina en la antigua si está presente en la red. No dar ninguna contraseña:
    
        ```Shell
    ssh-keygen -t rsa -C "jp.perez.alcantara@gmail.com"
    
    cat id_rsa.pub >> ~/.ssh/authorized_keys
    ```
      + [X] Instalar el **Visual Studio Code**.
      + [ ] Coger el fichero **backup_essentials** de la máquina saliente y desplegar los activos que tengan sentido en la máquina entrante.