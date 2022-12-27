title:: Docker/Compose

- **Docker Compose up:** levanta un Compose
  - **-f** es el fichero YAML que describe el Compose, por defecto es **.**
  - **-d** ejecuta el Compose en mode detached
  - ```shell
    docker compose -f path/to/docker-compose-file up -d
    ```
- **Docker Compose down:** echa abajo un Compose
  - **-t** es el tiempo antes de provocar un shutdown forzoso
  - [#C] #Work/Toolsresearch **-v** borra los volúmenes (¡CUIDADO!). No sabemos muy bien qué hace exactamente, probar.
  - ```shell
    docker compose down -t 30 -v
    ```
- **Docker Compose start:** arranca un Compose compuesto de servicios, sólo [[Docker/SWARM]]. Usar **compose up** para despliegues no SWARM
  collapsed:: true
  - ```shell
    docker compose start [[nombre servicio]]
    ```
- **Docker Compose stop:** para un Compose, manteniendo los contenedores, las redes y demás. Se vuelve a arrancar con un **start** o un **up**.
  - ```shell
    docker compose stop
    ```
- Ejemplos de **docker-compose.yaml**
  collapsed:: true
  - [[PostGIS]] más API en [[Node]]
    - ```yaml
      version: '3.5'
      
      networks:
      	marvel:
        	external: false
        	name: marvel
        	attachable: true
      
      services:
        postgis:
          image: malkab/postgis:holistic_hornet
          container_name: marvel_postgis
      
          networks:
            - marvel
      
          volumes:
            - ../docker-volumes/marvel_postgis:/data
      
        api:
          image: malkab/nodejs-dev:16.13.2
          container_name: marvel_api
          working_dir: /src
      
          ports:
            - 8080:8080
      
          networks:
            - marvel
      
          volumes:
            - ../../020-api/node/:/src
            - ./docker-volumes/api-logs:/logs/
      
          command: -c "yarn start"
      ```
- #Procesar
  collapsed:: true
  - **Operaciones Compose básicas** #procesar
    collapsed:: true
    - ```shell
      #!/bin/bash
      
      # -----------------------------------------------------------------
      #
      # Drops data persistence layer Compose. Drops containers but not
      # locally folders mounted volumes, so losing data should not be a
      # concern.
      #
      # -----------------------------------------------------------------
      # Check mlkctxt to check. If void, no check will be performed. If NOTNULL,
      # any activated context will do, but will fail if no context was activated.
      MATCH_MLKCTXT=default
      
      # Check mlkctxt
      if command -v mlkctxt &> /dev/null ; then
      
        mlkctxtcheck $MATCH_MLKCTXT
      
        if [ ! $? -eq 0 ] ; then
      
          echo Invalid context set, required $MATCH_MLKCTXT
      
          exit 1
      
        fi
      
      fi
      
      # -v drops named volumes defined in Compose file, BEWARE!!!
      docker-compose -p sunnsaas_v1 down -t 600 -v
      ```
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
      
        mlkctxtcheck $MATCH_MLKCTXT
      
        if [ ! $? -eq 0 ] ; then
      
          echo Invalid context set, required $MATCH_MLKCTXT
      
          exit 1
      
        fi
      
      fi
      
      docker-compose -f path/to/docker-compose-file -p sunnsaas_v1 up -d
      ```
    - ```shell
      #!/bin/bash
      
      # Docker SWARM commands
      
      # Get all depoloyed SWARM names
      docker stack ls --format "{{.Name}}"
      
      # Deploy a SWARM stack based on a Compose file
      docker stack deploy -c docker-compose.yaml name_of_the_stack
      ```
    - ```Shell
      version: '3.5'
      
      networks:
        sunnsaas:
          external: false
          name: network_name
          attachable: true
      
      volumes:
        phd-data-postgis:
          external: false
          name: phd-data-postgis
      
      configs:
        config_a:
          file: ./conf/config_a.json
      
      services:
        postgis:
          image: malkab/postgis:holistic_hornet
          container_name: sunnsaas_postgis_v1
      
          # Put here other configs as described at the Docker image documentation
          environment:
            - PASSWORD=postgres
      
          networks:
            - sunnsaas
      
          ports:
            - "${MLKC_SUNNSAAS_DB_OUTER_PORT}:5432"
      
          # This tmpfs volume is a workaround to increase the shared memory allowed to be
          # used by the container in a SWARM deployment. PG uses this in demanding queries.
          # This example increases the default to aprox. 8GB.
          tmpfs:
            - /tmp:size=8000000000
      
          volumes:
            - ./000_localhost_volumes/sunnsaas_postgis:/data
            - ../../assets/pg/postgresql.conf:/default_confs/postgresql.conf
            - phd-data-postgis:/whatever
            - type: tmpfs
              target: /dev/shm
      
          configs:
            - source: config_a
              target: /path/to/mount/config
              mode: 644
      ```
    - ```shell
      version: '3.5'
      
      networks:
        XXX:
          external: false
          name: XXX
          attachable: true
      
      services:
        postgis:
          image: malkab/postgis:holistic_hornet
          container_name: XXX_postgis
      
          networks:
            - XXX
      
          volumes:
            - ../docker-volumes/XXX_postgis:/data
      ```
  - ```shell
    version: '3.5'
    
    networks:
      carto_bcn:
        external: false
        name: carto_bcn
        attachable: true
    
    services:
      postgis:
        image: malkab/postgis:holistic_hornet
        container_name: carto_bcn
    
        networks:
          - carto_bcn
    
        ports:
          - "5432:5432"
    
        volumes:
          - ./docker_persistent_volumes/pg:/data
    
    
    
    version: '3.5'
    
    networks:
      sunnsaas:
        external: false
        name: ${MLKC_SUNNSAAS_APP_NAME}
        attachable: true
    
    volumes:
      phd-data-postgis:
        external: false
        name: phd-data-postgis
    
    services:
      postgis:
        image: malkab/postgis:gargantuan_giraffe
        container_name: sunnsaas_postgis_v1
    
        environment:
          - PASSWORD=${MLKC_SUNNSAAS_DB_PASSWORD}
    
        networks:
          - sunnsaas
    
        ports:
          - "${MLKC_SUNNSAAS_DB_OUTER_PORT}:5432"
    
        volumes:
          - ./000_localhost_volumes/sunnsaas_postgis:/data
          - ../../assets/pg/postgresql.conf:/default_confs/postgresql.conf
          - phd-data-postgis:/whatever
    
    
    
    
    
    version: '3.5'
    
    networks:
      cell_raw_data:
        name: cell_raw_data_holistic_hornet
        external: false
        attachable: true
    
    configs:
      pg_hba_conf:
        file: ./configs/pg_hba.conf
      postgresql_conf:
        file: ./configs/postgresql.conf
    
    volumes:
      cell_raw_data_postgis:
        external: false
        name: cell_raw_data_postgis_holistic_hornet
    
    services:
      cell_raw_data_postgis:
        image: malkab/postgis:holistic_hornet
        shm_size: "20GB"
    
        environment:
          - PASSWORD=jju3kn3332bgb4@hh
    
        networks:
          - cell_raw_data
    
        ports:
          - "5643:5432"
    
        tmpfs:
          - /tmp:size=20GB
    
        volumes:
          - cell_raw_data_postgis:/data
          - type: tmpfs
            target: /dev/shm
    
    
        configs:
          - source: pg_hba_conf
            target: /default_confs/pg_hba.conf
            uid: '1000'
            gid: '1000'
            mode: 0644
          - source: postgresql_conf
            target: /default_confs/postgresql.conf
            uid: '1000'
            gid: '1000'
            mode: 0644
    ```