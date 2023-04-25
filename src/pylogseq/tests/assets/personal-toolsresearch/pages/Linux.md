- Mucha información también en la página de [[Ubuntu]].
- # Montaje permanente de unidades discos duros grandes externas por USB
  collapsed:: true
  - Darle un nombre a la unidad y etiquetarla
  - Pinchar la unidad
  - Ver su **UUID** y su tipo de sistema de ficheros con **lsblk -f**
  - Crear en **/mnt/** el punto de montaje con el siguiente nombre: **[external_]alice_hdd_2_8tb**
  - Añadir a **/etc/fstab** una entrada para la unidad
    collapsed:: true
    - ```txt
      # Externo WD3000
      UUID=b1f0044e-892e-44ec-b1cb-80afde4a7a60 /mnt/x ext4 defaults,noauto,exec,nofail,user 0 2
      ```
  - Esta entrada permite, sin **sudo**, montar y desmontar unidades
    collapsed:: true
    - ```shell
      mount /mnt/external_alice_hdd_2_8tb
      umount /mnt/external_alice_hdd_2_8tb
      ```
  - Probar por primera vez la creación de un fichero (**touch**). Si no hay permisos, cambiar con **chown** el dueño del directorio, que es un cambio que permanece de montaje en montaje.
- # Montaje de particiones
  collapsed:: true
  - Ver la partición con **fdisk** y el ID del usuario que va a ser el dueño del montaje
    - ```shell
      fdisk -l
      id malkab
      ```
  - Montar
    - ```shell
      mount /dev/sde1 /media/special -o gid=1000,uid=1000,umask=0755
      mount /dev/sde1 /media/special -o gid=1000,uid=1000,umask=0022
      mount -t iso9660 -o loop,ro microsoft_visio_2003.iso ~/media/cd-iso/
      ```
    - El **umask** del último comando es para montar [[NTFS]]
    - El último comando monta una imagen ISO
- #Referencia #Linux #DevOps #GeoServer #PostgreSQL Ejemplo de despliegue de un stack PostgreSQL + GeoServer + visor HTML en el repositorio **freelancing_us/visor_erosion**, WP **wp-2022-09-14-010-version_5_anyos**. Básicamente juega con los volumenes Docker como base del despliegue en producción.
  id:: 634d60c4-56fb-4778-96af-3595e4cc926d
- #Referencia **Copias de seguridad:** ver D/devops para máquinas que son Linux Desktop. El script está en **mlktools-scripts/scripts_templates**.
  id:: 634d60c5-702b-4fe4-98de-3e3d0dd28210
- #Referencia #Linux #DevOps Para desplegar un servidor Linux con facilidad tenemos en **Boilerplates** un directorio llamado **system_setup_procedures/linux_server** en el que se explica todo paso por paso.
  id:: 634d60c4-4113-421c-bd1d-31399ab2c2c5
- #Web/Linux #Linux #Sistemas #Servidores Configuración y arranque de un nuevo servidor Linux
  id:: 634d60c4-f1f8-4b17-bcb0-d6da85b89a83
  collapsed:: true
  - [DevOps - Configurar un nuevo servidor Linux · GitHub](https://gist.github.com/malkab/82c9b9e261539f28fe6cda7485814837)
- #DevOps Formateo de un disco duro **NTFS** a **EXT4**
  collapsed:: true
  - Pinchar el disco duro (si es externo)
  - Utilizar **fdisk -l** y **lsblk -f** para ver su código **/dev/sdX**
  - Formatear con **mkfs -t ext4 /dev/sdX** (tiene que estar desmontado)
  - Utilizar **tune2fs** para modificar el sistema de ficheros recién creado
    collapsed:: true
    - ```shell
      # Información
      tune2fs -l /dev/sdX
      
      # Cambiar nombre del volumen
      tune2fs -L nombre /dev/sdX
      
      # Cambiar la reserva de bloques para root
      tune2fs -m 1 /dev/sdf1
      ```
- **[[apt]] y [[dpkg]]: instalación de dependencias a la fuerza**
  collapsed:: true
  - A veces [[dpkg]] intenta instalar algún [[.deb]] y no encuentra alguna dependencia. Para instalarlas, después del [[dpkg]], ejecutar **apt-get install -f**.
- **Terminal**
  collapsed:: true
  - Atajos de teclado:
    - **CTRL + L:** clear
- Network
  collapsed:: true
  - Ficheros clave
    collapsed:: true
    - **/etc/network/interfaces :** definición de interfaces de red
    - **/etc/hostname :** el nombre de host de la máquina
    - **/etc/hosts :** mapeo de host local
  - Reiniciar la red en [[Ubuntu]]s modernos
    collapsed:: true
    - ```shell
      # Esta puede que sea más antigua
      sudo /etc/init.d/network-manager restart
      
      # Esta es más probable
      sudo service networking restart
      ```
  - Chequeo de interfaces: **nmcli**
  - Chequeo de hostname: **hostname -f**
  - DNS gratuítas de Google: 8.8.8.8, 8.8.4.4
  - Ejemplos de **/etc/network/interfaces**, para el improbable caso de que haya que configurarlos a mano alguna vez
    - Con DHCP
      - ```txt
        auto lo eth0
        iface lo inet loopback
        ```
    - Interfaz estático
      - ```txt
        auto wlan0
        iface wlan0 inet static
        address 192.168.1.250
        netmask 255.255.255.0
        gateway 192.168.1.1
        dns-nameservers 150.214.186.69 150.214.130.15
        ```
  - Encontrar el gateway local: **route -n**
  - Escaneo de puertos con **nmap:** nmap -sn -v 10.30.102.* | grep -v down
  - Encontrar la velocidad duplex: ethtool eth0
  - Encontrar conflictos de IP
    collapsed:: true
    - Encontrar la IP local: ifconfig | grep broadcast
    - Escaneo con **arp-scan**
      collapsed:: true
      - ```shell
        arp-scan -I eth0 -l
        
        arp-scan -I eth0 193.147.172.0/24
        
        arp-scan -I eth0 193.147.172.0/255.255.255.0
        
        arp-scan -I eth0 192.168.1.1
        
        arp-scan -I eth0 193.147.172.1-193.147.172.10
        
        arp-fingerprint -o "--interface=eth0 --numeric" 192.168.1.111
        ```
  - Look up de DNS: nslookup 193.147.172.57
- Monitorización de sistema
  collapsed:: true
  - ```shell
    top -o %MEM
    free -h
    top -p [PID]
    ps aux --sort=-%mem | awk 'NR<=10{print $0}'
    ps aux --sort=-%cpu | awk 'NR<=10{print $0}'
    ```
  - Comandos de **top**
    collapsed:: true
    - **h:** ayuda
    - **W:** escribir configuración a **~/.toprc**
    - **E / e:** cambiar unidades de memoria
    - **z:** color / mono
    - **?:** help
    - **R:** ordenar por columna
    - **< / >:** seleccionar columna para ordenar
  - Input / output de disco: iotop -P -a
  - Rendimiento de escritura
    collapsed:: true
    - Genera un fichero de 0 a 1 GB con 0
      ```shell
      dd if=/dev/zero of=/root/testfile bs=1GB count=1 oflag=direct
      ```
  - Árbol de procesos: pstree -p
- Chequear características del sistema
  collapsed:: true
  - **CPU:** lscpu
- Crear un USB bootable con **dd**
  collapsed:: true
  - ```shell
    dd if=kubuntu-16.04-desktop-amd64.iso of=/dev/sdb
    ```