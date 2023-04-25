filters:: {}

- # #Workflow Mantenimiento Docker - Limpieza de infraestructura en desuso
  id:: 6362a2ff-a13c-4149-9da3-fbc9b285bee9
  collapsed:: true
  - Hacerlo manualmente, nunca automáticamente, ya que se puede perder información (nos ha pasado).
  - Chequeos:
    collapsed:: true
    - Limpieza de stacks:
      - docker stack ls
      - docker stack rm
    - Limpieza de servicios:
      - docker service ls
      - docker service rm
    - Limpieza de contenedores:
      - Utilizar la extensión de Docker de **VSC** e ir eliminando ahí. Lo normal es que al borrar contenedores se van borrando sus volúmenes. Comprobar qué volúmenes tienen asociados.
      - Para no locales, utilizar los comandos siguientes:
        - ```shell
          docker ps -a
          ```
    - Limpieza de volúmenes:
      - Utilizar la extensión de Docker de **VSC**.
      - Para no locales, utilizar los comandos siguientes:
        - ```shell
          docker volume ls
          ```
    - Limpieza de imágenes:
      - Hacer una revisión con **docker images**.
      - Si todas son potencialmente prescindibles, hacer un **docker rmi $(docker images -q)**. Es seguro, las que están en uso no se borrarán.
      - Revisar aquellas que tienen varios tags y borrar manualmente con **docker rmi -f XXX** las que no sirvan.
    - Limpieza de redes:
      - Utilizar **docker network rm $(docker network ls -q)** contestando a todo que **no**.
- # Ejecutar aplicaciones GUI en Docker MacOS
  collapsed:: true
  - Ejemplo QGIS
    collapsed:: true
    - ```shell
      #!/bin/bash
      
      # Tests a Docker container with a GUI
      
      socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\" &
      
      open -a Xquartz
      
      docker run --rm -e DISPLAY=192.168.1.186:0 -v `pwd`:/qgis \
          --entrypoint /usr/bin/qgis kartoza/qgis-desktop:3.0.3
      ```
  - Ejemplo XEYES
    collapsed:: true
    - ```shell
      #!/bin/bash
      
      # Tests a Docker container with a GUI
      
      socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\" &
      
      open -a Xquartz
      
      docker run --rm -e DISPLAY=192.168.1.186:0 gns3/xeyes
      ```
- # Instalación
  collapsed:: true
  - La guía aquí: [Install Docker Engine on Ubuntu | Docker Documentation](https://docs.docker.com/engine/install/ubuntu/)
  - ```shell
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    
    sudo add-apt-repository \
      "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) \
      stable"
    
    sudo apt update -y
    
    sudo apt install -y docker.io
    
    # Add user to the Docker group
    sudo usermod -aG docker $USER
    
    # Set Docker to autostart
    sudo systemctl enable --now docker.service
    
    # Install Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    # Init Docker SWARM
    sudo docker swarm init
    
    # Test Docker
    sudo mlktestdocker
    ```
- Docker run con [[mlkctxt]]
  id:: 636b894d-3979-43c8-b6c4-ec73c46340c4
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    # -----------------------------------------------------------------
    #
    # Starts the data persistence layer Compose.
    #
    # -----------------------------------------------------------------
    # Check mlkctxt to check. If void, no check will be performed. If NOTNULL,
    # any activated context will do, but will fail if no context was activated.
    MATCH_MLKCTXT=default
    
    # Check mlkctxt
    if command -v mlkctxt &> /dev/null ; then
    
      if [ ! -z "$MATCH_MLKCTXT" ] ; then
    
        mlkctxtcheck $MATCH_MLKCTXT
    
        if [ ! $? -eq 0 ] ; then
    
          echo Invalid context set, required $MATCH_MLKCTXT
    
          exit 1
    
        fi
    
      fi
    
    fi
    
    docker run -ti --rm \
        --name libwk32_node_dev \
        --hostname libwk32_node_dev \
        --network host \
        --user 1000:1000 \
        -v $(pwd)/../:$(pwd)/../ \
        --workdir $(pwd)/../node \
        -e NODE_ENV=development \
        -e NODE_MEMORY=2GB \
        -v /home/malkab/.npmrc:/root/.npmrc \
        -v /home/malkab/.npmrc:/home/node/.npmrc \
        malkab/nodejs-dev:16.13.2
    ```
- Docker run para [[Node]]
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    # -----------------------------------
    #
    # Runs Node.
    #
    # -----------------------------------
    docker run -ti --rm \
        --name libwk32_node_dev \
        --hostname libwk32_node_dev \
        --network host \
        --user 1000:1000 \
        -v $(pwd)/../:$(pwd)/../ \
        --workdir $(pwd)/../node \
        -e NODE_ENV=development \
        -e NODE_MEMORY=2GB \
        -v /home/malkab/.npmrc:/root/.npmrc \
        -v /home/malkab/.npmrc:/home/node/.npmrc \
        malkab/nodejs-dev:16.13.2
    ```
- Networking
  collapsed:: true
  - Conectarse a un contenedor: **--network=container:[container name]**
- #PostgreSQL #PostGIS Ejecuta un **servidor de base de datos** para cosas rápidas, sin Compose ni persistencia
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    # -----------------------------------------------------------------
    #
    # Runs the database server.
    #
    # -----------------------------------------------------------------
    docker run -ti --rm \
      --name xxx_pg \
      --hostname xxx_pg \
      -p 5432:5432 \
      -e LOCALE=es_ES \
      malkab/postgis:idiosyncratic_ibex
    ```
- #Referencia #PostgreSQL #GRASS #Topology **GRASS topology clean** and a workflow with the malkab/grass Docker image using GRASS and PostgreSQL commands: freelancings-us-secciones_censales
- #Referencia #PostgreSQL **Docker tmpfs shm_size** modification in SWARM mode for high-performance in PostgreSQL configuration: cell_raw_data database compose
- #PostgreSQL #Referencia **PostgreSQL en un Docker SWARM** con mlkctxt para entornos múltiples: boilerplate docker_postgresql_standalone
- #nginx Ejecutar un servidor **nginx** para contenido estático
  collapsed:: true
  - Ver también [[G/boilerplates/boilerplates]] **docker-deployments**
  - ```bash
    docker run -d \
      --name container_name \
      -p 80:80 \
      -v /some/content/:/usr/share/nginx/html:ro \
      -v nginx.conf:/etc/nginx/nginx.conf \
      nginx
    ```
- Volume removal
  collapsed:: true
  - ```bash
    docker volume rm volume_name
    ```
- #Web/Geo/PostGIS #PostGIS Notas de producción de la última versión de la imagen Docker de PostGIS: [docker-postgis/docker-tags/holistic_hornet/020_production at main · malkab/docker-postgis · GitHub](https://github.com/malkab/docker-postgis/tree/main/docker-tags/holistic_hornet/020_production)
- # Docker build
  - **--no-cache** ignora la caché de imágenes intermedias, **--force-rm** fuerza el borrado de imágenes intermedias**, **-t** indica el nombre de la nueva imagen. El punto final es la ruta al fichero **Dockerfile**.
    - ```shell
      docker build --no-cache --force-rm -t malkab/python:3.9-buster .
      ```
- # Docker tag
  collapsed:: true
  - Añade una tag a una imagen existente
    collapsed:: true
    - ```shell
      docker tag malkab/python:3.9-buster malkab/python:latest
      ```
- # Docker login
  collapsed:: true
  - Hace login en un registro privado, por ejemplo una cuenta privada en [[DockerHub]], [[GitHub]] o [[GitLab]]
    - ```shell
      docker login [ registro ] -u [ usuario ]
      ```
- # Docker push
  collapsed:: true
  - Sube una imagen a un registro (ver **docker login**)
    - ```shell
      docker push malkab/python:3.9-buster
      ```
- # Filtrar imágenes para borrar
  collapsed:: true
  - ```shell
    # Remove dangling images
    docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
    
    # Find images with a tag
    docker images | grep 1.3.1
    
    # Get their hashes
    docker images | grep 1.3.1 | tr -s ' ' | cut -d ' ' -f 3
    
    # Remove when very sure
    docker rmi $(docker images | grep 1.3.1 | tr -s ' ' | cut -d ' ' -f 3)
    ```
- # Registro Docker de [[GitLab]]
  collapsed:: true
  - **GitLab** proporciona tokens de acceso a diversos niveles, como **API** (total) o **Read Registry** (leer el registro para bajar imágenes)
  - ```shell
    # Proporcionar el token como contraseña
    docker login registry.gitlab.com -u user -p pass
    
    # Modo interactivo
    docker login registry.gitlab.com -u user
    ```
- # Running [[X Server]] apps on [[Docker]] for [[MacOS]]
  collapsed:: true
  - It’s possible to run graphic interfaces apps on Docker for Mac by using **Xquartz**, a X11 implementation for Mac
  - **CHECK THIS ONE NEXT TIME** PRETTY MUCH SURE THIS IS NEEDED BUT PERHAPS XQUARTZ IS NOT. Install **Xquartz** from the official website and configure **Security** to allow remote connections (in **Preferences**)
  - To run a container with access to the host screen:
        ```shell
        xhost + 127.0.0.1
    
        docker run -ti --rm \
        -e DISPLAY=host.docker.internal:0 \
        malkab/anaconda3
        ```
  - The **DISPLAY** env var is doing the magic
- # Comprobar si un contenedor se está ejecutando
  collapsed:: true
  - Así, dos de ellos
    - ```shell
      # Check if relevant containers are running
      if
      
        [ "$(docker container inspect -f '{{.State.Running}}' libsunnsaasbackend_postgis)" != "true" ] ||
        [ "$(docker container inspect -f '{{.State.Running}}' libsunnsaasbackend_redis)" != "true" ]
      
      then
      
        echo The persistence stack must be running, check 002-compose_up.sh.
        exit 1
      
      fi
      ```
- # Imágenes: guardar y restaurar desde ficheros
  collapsed:: true
  - Para almacenar una imagen en un fichero usar **save**:
    ```shell
    docker save -o busybox.tar busybox
    
    tar -jcvf busybox.tar.bz2 busybox.tar
    ```
    Este TAR se puede comprimir posteriormente con BZ2, pero ese archivo **NO** es cargable directamente con **load**, hay que descomprimirlo primero.
  - Para cargar una imagen desde fichero usar **load**, descomprimiendo primero el BZ2 si estuviera comprimido así. Se necesita el TAR plano:
    ```shell
    tar -jxvf busybox.tar.bz2
    
    docker load -i busybox.tar
    ```
- #procesar Poner un poco de orden en esta página y coger material de páginas de Journal.