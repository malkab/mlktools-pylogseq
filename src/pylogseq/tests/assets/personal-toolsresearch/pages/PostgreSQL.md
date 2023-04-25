filters:: {}

- # Dump and Restore #procesar
  collapsed:: true
  - Before restoring, make sure roles and database exists at the destination server. Dump and restore always with a superuser. There's no need to convert the database to PostGIS to import a PostGIS database, nor it is necessary to turn on the plpgsql language.
  - If the database set ownerships to other users than the given by pg_restore's -U, those roles must already exists in the database. Roles aren't backed up by pg_dump. Use option -O in pg_restore to skip permissions assignments.
  - There is an option -e to stop the process when an error arises. Use it to check for errors, or log the output to a file with &>.
  - Option -a dumps only data, not schema.
  - Backups
    collapsed:: true
    - Backup con **Docker** en formato comprimido con plantilla **mlkctxt**
      collapsed:: true
      - ```shell
        docker run -ti --rm \
        	--name shared_db_psql \
        	--hostname shared_db_psql \
        	--network=[{kerdes_main_db.network}] \
        	--user 1000:1000 \
        	-v $(pwd):$(pwd) \
        	--workdir $(pwd) \
        	-e "HOST=[{kerdes_main_db.host}]" \
        	-e "PORT=[{kerdes_main_db.port}]" \
        	-e "DB_TO_DUMP=data" \
        	-e "USER=[{kerdes_main_db.user}]" \
        	-e "PASS=[{kerdes_main_db.pass}]" \
        	--entrypoint /bin/bash \
        	malkab/postgis:idiosyncratic_ibex \
        	-c 'PGPASSWORD=${PASS} pg_dump -F c -v \
        		-f $(pwd)/catastro_dump_2020 \
        		-h ${HOST} \
        		-p ${PORT} \
        		-U ${USER} \
        		${DB_TO_DUMP}'
        ```
    - Backup de una sola tabla en inserts planos
      			collapsed:: true
      collapsed:: true
      - ```shell
        				# Dumps a certain table in plain, insert formats, without ownership.
        				# This is supossed to be a very portable format.
        				PGPASSWORD=$PASS pg_dump --inserts -b -E UTF8 -F p -O -v \
        -f tablename \
        -h localhost \
        -p 5454 \
        -t sometable \
        -U postgres \
        databasename
        				```
    - Backup de un esquema determinado (argumento **-n**) en texto plano, formato insert, sin ownership
      collapsed:: true
      - ```bash
        				# Dumps a given schema with the same characteristics
        				# as above (**-n** argument)
        				PGPASSWORD=$PASS3 pg_dump --inserts -b -E UTF8 -F p -O -v \
        -f $ROOTFOLDER/esquema_indicadores.sql \
        	-h $HOST3 \
        	-p $PORT3 \
        	-n indicadores \
        	-U $USER3 \
        	e_catastro
        		```
    - Backup de un esquema determinado (argumento **-n**) en formato comprimido, sin ownership
      			collapsed:: true
      collapsed:: true
      - ```bash
        				# Dumps a given schema with the same characteristics
        				# as above (**-n** argument)
        				PGPASSWORD=$PASS3 pg_dump -F c -O -v \
        -f $ROOTFOLDER/esquema_indicadores_dump \
        -h $HOST3 \
        -p $PORT3 \
        -n indicadores \
        -U $USER3 \
        e_catastro
        		```
  - Restores
    collapsed:: true
    - Restore simple
      - ```bash
        # Simple restore
        PGPASSWORD=${PASS} pg_restore -F c -v \
            -d databasename \
        	-h localhost \
        	-p 5432 \
        	-U postgres \
        	post.backup
        ```
    - Restore con un Docker, sin permisos (esto parece que es difícil de controlar, pero vamos)
      - ```shell
        docker run -ti --rm \
        	--name shared_db_psql \
        	--hostname shared_db_psql \
        	--network=[{kerdes_main_db.network}] \
        	--user 1000:1000 \
        	-v $(pwd):$(pwd) \
        	--workdir $(pwd) \
        	-e "HOST=[{kerdes_main_db.host}]" \
        	-e "PORT=[{kerdes_main_db.port}]" \
        	-e "DB=postgres" \
        	-e "USER=[{kerdes_main_db.user}]" \
        	-e "PASS=[{kerdes_main_db.pass}]" \
        	--entrypoint /bin/bash \
        	malkab/postgis:idiosyncratic_ibex \
        	-c 'PGPASSWORD=${PASS} pg_restore -F c -v -O --no-acl \
        		-d cell_raw_data \
        		-h ${HOST} \
        		-p ${PORT} \
        		-U ${USER} \
            	$(pwd)/data/000_in/catastro_dump_2020'
        ```
  - Examples
    collapsed:: true
    - ```bash
      # Simple dump
      pg_dump -b -E UTF8 -F c -v -Z 9 \
      	-f ssl_dump \
          -h localhost \
          -p 5432 \
          -U postgres \
          databasename
      
      # Clean before restore
      pg_restore --clean --format=c --verbose --jobs=4 \
      	--dbname dea100_2009 \
          --host=localhost \
          --port=5432 \
          --username=postgres \
          DEA100Postgres.backup
      
      # This creates the database using -d postgres
      # database as stepping point for database creation
      pg_restore -C -F c -v \
      	-h localhost \
          -d postgres \
          -p 5432 \
          -U postgres \
          post.backup
      
      # This creates the database using -d postgres database
      # as stepping point for database creation, and ignores
      # ownership commands (-O option)
      pg_restore -C -F c -O -v \
      	-h localhost \
          -d postgres \
          -p 5432 \
          -U postgres \
          post.backup
      
      # Bypass password prompt
      PGPASSWORD="gugu23" /usr/local/pgsql/bin/pg_restore  -F c -v \
      	-d postgis_test \
          -h viv3.cica.es \
          -p 5518 \
          -U postgres \
          backup_juanma.backup
      
      # Single table dump
      pg_dump -b -E UTF8 -F c -v -Z 9 \
      	-t tablename-f ssl_dump \
          -h localhost \
          -p 5432 \
          -U postgres \
          databasename
      
      # Single schema dump
      pg_dump -b  -E UTF8 -F c -v -Z 9 \
      	-n schemaname \
          -f ssl_dump \
          -h localhost \
          -p 5432 \
          -U postgres \
          databasename
      
      # Jobs for directory store format with -j parameter
      pg_dump -b -E UTF8 -F d -v -j 4 -Z 9 \
      	-f scandal_test_dump \
      	-h localhost \
          -p 5454 \
          -U postgres \
          scandal_test
      ```
- # psql
  collapsed:: true
  - #Docker psql con Docker
    - ```shell
      #!/bin/bash
      
      # -----------------------------------------------------------------
      #
      # Runs a psql interactive session
      #
      # Remember:
      #   - use --network=host to use the local host native network interface
      #     (for example to connect to DB accesible on the Internet)
      #   - use --network=container:[container name] to connect to the local network
      #     of an existing container (option "hostname" is incompatible with this
      #     option)
      #
      # Check mlkctxt to check. If void, no check will be performed. If NOTNULL,
      # any activated context will do, but will fail if no context was activated.
      #
      # -----------------------------------------------------------------
      MATCH_MLKCTXT=NOTNULL
      
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
        --name wk32_psql \
        --hostname wk32_psql \
        --network wk32 \
        --user 1000:1000 \
        -v $(pwd)/../database/src:$(pwd)/../database/src \
        --workdir $(pwd)/../database/src \
        -e "HOST=[{cell_db.host}]" \
        -e "PORT=[{cell_db.port}]" \
        -e "DB=cell_raw_data" \
        -e "USER=[{cell_db.users.postgres.user}]" \
        -e "PASS=[{cell_db.users.postgres.pass}]" \
        --entrypoint /bin/bash \
        malkab/postgis:holistic_hornet \
        -c run_psql.sh
      ```
  - #Docker psql con Docker y filtro mlkctxt
    collapsed:: true
    - ```shell
      #!/bin/bash
      
      # How to properly use mlkctxt context check feature
      # Add at top of the script:
      MATCH_MLKCTXT=default
      
      # Check mlkctxt
      if command -v mlkctxt &> /dev/null ; then
      
        mlkctxtcheck $MATCH_MLKCTXT
      
        if [ ! $? -eq 0 ] ; then
      
          echo Invalid context set, required $MATCH_MLKCTXT
      
          exit 1
      
        fi
      
      fi
      
      docker run -ti --rm \
        --name wk32_psql \
        --hostname wk32_psql \
        --network=wk32 \
        --user 1000:1000 \
        -v $(pwd)/../database/src:$(pwd)/../database/src \
        --workdir $(pwd)/../database/src \
        -e "HOST=wk32_db" \
        -e "PORT=5432" \
        -e "DB=postgres" \
        -e "USER=postgres" \
        -e "PASS=postgres" \
        --entrypoint /bin/bash \
        malkab/postgis:holistic_hornet \
        -c run_psql.sh
      ```
- # pg_hba.conf
  collapsed:: true
  - ```text
    local all all md5
    host all all 127.0.0.1/32 md5
    host all all 0.0.0.0/0 md5
    host all all ::1/128 md5
    ```
- # postgresql.conf
  collapsed:: true
  - Configuradores
    collapsed:: true
    - [PGConfig](https://www.pgconfig.org/)
    - [PGTune](https://pgtune.leopard.in.ua)
    - [Ejemplo exhaustivo en GitHub](https://github.com/postgres/postgres/blob/master/src/backend/utils/misc/postgresql.conf.sample)
      id:: 63e4f3ee-ba80-47c1-8c44-3b55f9172709
  - Para producción
    collapsed:: true
    - ```text
      checkpoint_completion_target=0.9
      client_connection_check_interval=0
      client_min_messages=WARNING
      datestyle='iso, mdy'
      default_statistics_target=500
      dynamic_shared_memory_type=posix
      effective_cache_size=6GB
      effective_io_concurrency=2
      idle_in_transaction_session_timeout=0
      lc_messages='C'
      listen_addresses='*'
      log_autovacuum_min_duration=0
      log_checkpoints=ON
      log_connections=ON
      log_destination='stderr,csvlog'
      log_directory='pg_log'
      log_disconnections=ON
      log_error_verbosity=DEFAULT
      log_filename='postgresql-%Y-%m-%d_%H%M%S.log'
      log_line_prefix='%a %u %d %r %h %m %i %e'
      log_lock_waits=ON
      log_min_duration_statement='10s'
      log_min_error_statement=ERROR
      log_min_messages=WARNING
      log_rotation_age=1d
      log_rotation_size=500MB
      log_statement='none'
      log_temp_files=0
      log_timezone='UTC'
      logging_collector=ON
      maintenance_work_mem=410MB
      max_connections=200
      max_locks_per_transaction=1024
      max_parallel_maintenance_workers=2
      max_parallel_workers_per_gather=2
      max_parallel_workers=2
      max_wal_senders=5
      max_wal_size=3GB
      max_worker_processes=8
      min_wal_size=2GB
      random_page_cost=4.0
      reserved_connections=0
      shared_buffers=2GB
      superuser_reserved_connections=3
      tcp_keepalives_count=0
      tcp_keepalives_idle=0
      tcp_keepalives_interval=0
      tcp_user_timeout=0
      timezone='UTC'
      wal_buffers=16MB
      work_mem=8MB
      ```
  - Para desarrollo, muy exhaustivo en sus logs
    collapsed:: true
    - ```text
      checkpoint_completion_target=0.9
      client_connection_check_interval=0
      client_min_messages=NOTICE
      datestyle='iso, mdy'
      default_statistics_target=500
      dynamic_shared_memory_type=posix
      effective_cache_size=6GB
      effective_io_concurrency=2
      idle_in_transaction_session_timeout=0
      lc_messages='C'
      listen_addresses='*'
      log_autovacuum_min_duration=0
      log_checkpoints=ON
      log_connections=ON
      log_destination='stderr,csvlog'
      log_directory='pg_log'
      log_disconnections=ON
      log_error_verbosity=DEFAULT
      log_filename='postgresql-%Y-%m-%d_%H%M%S.log'
      log_line_prefix='%a %u %d %r %h %m %i %e'
      log_lock_waits=ON
      log_min_duration_statement='10s'
      log_min_error_statement=NOTICE
      log_min_messages=NOTICE
      log_rotation_age=1d
      log_rotation_size=500MB
      log_statement='none'
      log_temp_files=0
      log_timezone='UTC'
      logging_collector=ON
      maintenance_work_mem=410MB
      max_connections=200
      max_locks_per_transaction=1024
      max_parallel_maintenance_workers=2
      max_parallel_workers_per_gather=2
      max_parallel_workers=2
      max_wal_senders=5
      max_wal_size=3GB
      max_worker_processes=8
      min_wal_size=2GB
      random_page_cost=4.0
      reserved_connections=0
      shared_buffers=2GB
      superuser_reserved_connections=3
      tcp_keepalives_count=0
      tcp_keepalives_idle=0
      tcp_keepalives_interval=0
      tcp_user_timeout=0
      timezone='UTC'
      wal_buffers=16MB
      work_mem=8MB
      ```
- Vistas materializadas
  collapsed:: true
  - Las vistas materializadas no pueden tener **primary keys**, pero se le pueden hacer índices
    - ```sql
      create materialized view dat_catastro_2020_process.buildingsingle as
      select
        ogc_fid,
        buildingnumber,
        totalbuildings,
        st_transform(the_geom, 3035) as geom
      from dat_catastro_2020.buildingsingle
      where estimatednumberofdwellings_constru > 0;
      
      create unique index
      on dat_catastro_2020_process.buildingsingle (ogc_fid);
      
      create index buildingsingle_ogc_fid
      on dat_catastro_2020_process.buildingsingle
      using btree(buildingnumber);
      
      create index buildingsingle_geom_gist
      on dat_catastro_2020_process.buildingsingle
      using gist(geom);
      ```
- # Vacuum
  collapsed:: true
  - **vacuum verbose:** simplemente elimina la información borrada de la tabla, pero no actualiza el planner ni devuelve espacio al SO. No necesita locks exclusivos.
  - **vacuum verbose analyze:** igual que el anterior, pero actualiza el planner.
  - **vacuum full verbose analyze:** reescribe las tablas con locks exclusivos. Devuelve espacio al SO.
- #Referencia #Docker/Compose Compose para un despliegue de PostgreSQL con el shared memory para poder hacer operaciones pesadas en [[G/boilerplates/boilerplates]]/docker-deployments
- #Referencia Trabajo con contextos SQL
  collapsed:: true
  - Esto está en [[G/boilerplates/boilerplates]], boilerplate **git_datascience_project**
  - Establecer como primer script SQL del proceso el controlador del contexto. En este fichero se establece el contexto en las primeras líneas.
    collapsed:: true
    - ```sql
      /**
      
        Process contexts.
      
        Available contexts:
      
        - test
        - production
      
        Set below the selected context:
      
      */
      \c database
      
      \set context production
      
      /**
      
        --------------------------------
      
        Context processing.
      
        --------------------------------
      
      */
      \o /dev/null
      
      select
        :'context' = 'test' as istest,
        :'context' = 'production' as isproduction;
      
      \gset
      
      \echo
      \echo -------------------
      \echo
      \echo Context :context
      \echo
      \echo -------------------
      \echo
      
      /**
      
        Common variables.
      
      */
      \set common0                0
      \set common1                1
      
      /**
      
        Context dependant.
      
      */
      \if :istest
      
        \set var_a                            var_a_test
        \set var_b                            var_b_test
      \set composite_var_a					:common0.:var_a
      \set composite_var_b					:common1 :var_b
      
      \endif
      
      \if :isproduction
      
        \set var_a                            var_a_production
        \set var_b                            var_b_production
      
      \endif
      
      \o
      ```
  - Utilizar el script anterior como primera entrada en sucesivos scripts
    collapsed:: true
    - ```psql
      /**
      
        Uses contexts.
      
        Set the context at 010.
      
      */
      \i 010-contexts.sql
      
      \echo :var_a
      
      \if :istest
      
      \echo IS TEST
      
      \endif
      
      \if :isproduction
      
      \echo IS PRODUCTION
      
      \endif
      ```
- #plpgsql Funciones con parámetros opcionales con valores por defecto
  collapsed:: true
  - ```sql
    create or replace function mlk_clockstart(
      _clock_name varchar default null
    )
    returns varchar as
    $$
    declare
      _var_name varchar;
    begin
    
      return 'AAA';
    
    end;
    $$
    language plpgsql;
    ```
- #plpgsql Ejemplo de función de agregado
  collapsed:: true
  - ```sql
    -- This is a function that takes two numbers and sums to the first
    -- double of the second
    
    create or replace function fn__add_double(anyelement, anyelement)
    returns anyelement as
    $$
      select $1+($2*2);
    $$
    language sql strict;
    
    
    
    -- Drop aggregate in case it exists
    
    drop aggregate if exists fn__agg_add_double(anyelement);
    
    
    
    -- Create aggregate with fn__add_double as sfunc, generic
    
    create aggregate fn__agg_add_double(anyelement)
    (
      sfunc = fn__add_double,
      stype = anyelement,
      initcond = 0
    );
    
    
    -- Returns 12
    -- init = 0
    -- Step 0: 0+(1*2) = 2
    -- Step 1: 2+(2*2) = 6
    -- Step 2: 6+(3*2) = 12
    
    with a as (
      select 1 as i
      union
      select 2 as i
      union
      select 3 as i)
    select fn__agg_add_double(i)
    from a;
    
    
    
    -- Another example
    
    create or replace function fn__add_arrays(anyarray, anyarray)
    returns anyarray as
    $$
      select $1 || $2;
    $$
    language sql strict;
    
    drop aggregate if exists fn__agg_add_arrays(anyarray);
    
    create aggregate fn__agg_add_arrays(anyarray)
    (
      sfunc = fn__add_arrays,
      stype = anyarray,
      initcond = '{}'
    );
    
    -- Returns {1,2,3,4,5,6}
    -- init = {}
    -- Step 0: {} || {1,2} = {1,2}
    -- Step 1: {1,2} || {3,4} = {1,2,3,4}
    -- Step 2: {1,2,3,4} || {5,6} = {1,2,3,4,5,6}
    
    with a as (
      select array[1,2]::double precision[] as i
      union
      select array[3,4]::double precision[] as i
      union
      select array[5,6]::double precision[] as i)
    select fn__agg_add_arrays(i)
    from a;
    ```
- #Docker/Compose Despliegue mínimo
  collapsed:: true
  - docker-compose.yaml
    collapsed:: true
    - ```yaml
      version: '3.5'
      
      networks:
        pg_helpers:
          external: false
          name: pg_helpers
          attachable: true
      
      services:
        postgis:
          image: malkab/postgis:idiosyncratic_ibex
          container_name: postgis
      
          networks:
            - pg_helpers
      
          ports:
            - "5432:5432"
      
          # This tmpfs volume is a workaround to increase the shared memory allowed to be
          # used by the container in a SWARM deployment. PG uses this in demanding queries.
          # This example increases the default to aprox. 8GB.
          tmpfs:
            - /tmp:size=8000000000
      
          volumes:
            - type: tmpfs
              target: /dev/shm
      ```
  - Up and down commands
    collapsed:: true
    - ```shell
      # Up
      docker compose -f docker-compose.yaml -p pg_helpers up -d
      
      #Down, not destroying any volume
      docker compose -p pg_helpers down -t 30
      ```
- #Web/Geo/PostGIS #Web/Herramientas/PostgreSQL #PostGIS Configuración de PostgreSQL / PostGIS
  collapsed:: true
  - [PGConfig](https://www.pgconfig.org/)
  - [PGTune - calculate configuration for PostgreSQL based on the maximum performance for a given hardware configuration](https://pgtune.leopard.in.ua/#/)
- #Bash Comando **mlkpghfromasprefixed**
  collapsed:: true
  - Este comando permite obtener los campos de select de una consulta de forma ordenada, tal como se ve debajo
    collapsed:: true
    - ```sql
      create materialized view :schema.mvw__building_sc as
      select
        -- keys
        row_number() over ()                 as gid,
        a.gid                                as building_gid,
        b.gid                                as sc_gid,
      
        -- building
        a.ogc_fid_original                   as building_ogc_fid_original,
        buildingnumber                       as building_buildingnumber,
        totalbuildings                       as building_totalbuildings,
        building_currentuse                  as building_building_currentuse,
        building_conditionofconstruction     as building_building_conditionofconstruction,
        building_beginconstruction           as building_building_beginconstruction,
        volumeaboveground                    as building_volumeaboveground,
        numberoffloorsaboveground_maxarea    as building_numberoffloorsaboveground_maxarea,
        volumebelowground                    as building_volumebelowground,
        numberoffloorsbelowground_maxarea    as building_numberoffloorsbelowground_maxarea,
        estimatednumberofdwellings           as building_estimatednumberofdwellings,
        cod_ine                              as building_cod_ine,
        id_parcela                           as building_id_parcela,
        cod_dgc                              as building_cod_dgc,
        cod_seccion_censal                   as building_cod_seccion_censal,
        estimatednumberofdwellings_constru   as building_estimatednumberofdwellings_constru,
        estimatednumberofdwellings_ieca      as building_estimatednumberofdwellings_ieca
      from whatever;
      ```
  - Sintaxis
    collapsed:: true
    - Opciones
      - **-a [indentación]:** espacios precedentes a las entradas de columna
      - **-c [columna objetivo]:** columna objetivo donde dejar los **as**
      - **-p [prefijo de columnas]:** el prefijo para los nombres de los columnas
      - **-e [prefijo para los alias]:** el prefijo de los **as**
    - ```shell
      mlkpghfromasprefixed -a 4 -c 40 -p a. -e a_ "the_table a, the_table b"
      ```
  - Se encuentra en el [[G/libraries_python/postgresql_helpers]] y se actualiza también en [[G/mlktools/scripts]] para instalarlo en nuevos equipos
- Notas **[[SQL]]**
  collapsed:: true
  - #SQL Contar registros y registros distintos (útil para identificar claves primarias)
    collapsed:: true
    - ```sql
      # Contar total de registros
      select count(*) from dat_catastro_2020.buildingsingle;
      
      # Contar ocurrencias distintas
      select count(distinct(ogc_fid)) from dat_catastro_2020.buildingsingle;
      ```
  - #SQL Claúsula **ON CONFLICT**
    collapsed:: true
    - Si hay conflicto en la clave primaria **code**, se actualizará en campo **name** con el valor entrante descartado por la colisión de clave
    - ```sql
      INSERT INTO marvelcdb.packtypes (code, name)
      VALUES ('a', 'b')
      ON CONFLICT (code) DO UPDATE SET name = EXCLUDED.name;
      ```
  - #SQL Ejemplo de **vista materializada** bien conformada para legibilidad
    collapsed:: true
    - ```sql
      create materialized view :schema.mvw__building_sc as
      select
        -- keys
        row_number() over ()                 as gid,
        a.gid                                as building_gid,
        b.gid                                as sc_gid,
      
        -- building
        a.ogc_fid_original                   as building_ogc_fid_original,
        buildingnumber                       as building_buildingnumber,
        totalbuildings                       as building_totalbuildings,
        building_currentuse                  as building_building_currentuse,
        building_conditionofconstruction     as building_building_conditionofconstruction,
        building_beginconstruction           as building_building_beginconstruction,
        volumeaboveground                    as building_volumeaboveground,
        numberoffloorsaboveground_maxarea    as building_numberoffloorsaboveground_maxarea,
        volumebelowground                    as building_volumebelowground,
        numberoffloorsbelowground_maxarea    as building_numberoffloorsbelowground_maxarea,
        estimatednumberofdwellings           as building_estimatednumberofdwellings,
        cod_ine                              as building_cod_ine,
        id_parcela                           as building_id_parcela,
        cod_dgc                              as building_cod_dgc,
        cod_seccion_censal                   as building_cod_seccion_censal,
        estimatednumberofdwellings_constru   as building_estimatednumberofdwellings_constru,
        estimatednumberofdwellings_ieca      as building_estimatednumberofdwellings_ieca,
      
        -- secciones censales
        b.ogc_fid_original                   as sc_ogc_fid_original,
        cat                                  as sc_cat,
        cod_seccion                          as sc_cod_seccion,
        cod_distrito                         as sc_cod_distrito,
        cod_municipio                        as sc_cod_municipio,
        municipio                            as sc_municipio,
        cod_provincia                        as sc_cod_provincia,
        provincia                            as sc_provincia,
        cod_comunidad                        as sc_cod_comunidad,
        comunidad                            as sc_comunidad,
        media_renta_por_unidad_consumo       as sc_media_renta_por_unidad_consumo,
        mediana_renta_por_unidad_consumo     as sc_mediana_renta_por_unidad_consumo,
        renta_bruta_media_por_hogar          as sc_renta_bruta_media_por_hogar,
        renta_bruta_media_por_persona        as sc_renta_bruta_media_por_persona,
        renta_neta_media_por_hogar           as sc_renta_neta_media_por_hogar,
        renta_neta_media_por_persona         as sc_renta_neta_media_por_persona,
        fuente_otras_prestaciones            as sc_fuente_otras_prestaciones,
        fuente_otros_ingresos                as sc_fuente_otros_ingresos,
        fuente_pensiones                     as sc_fuente_pensiones,
        fuente_desempleo                     as sc_fuente_desempleo,
        fuente_salario                       as sc_fuente_salario,
        p80_p20                              as sc_p80_p20,
        gini                                 as sc_gini,
        edad_media                           as sc_edad_media,
        poblacion                            as sc_poblacion,
        porcentaje_hogares_unipersonales     as sc_porcentaje_hogares_unipersonales,
        porcentaje_65_y_mayor                as sc_porcentaje_65_y_mayor,
        porcentaje_menor_18                  as sc_porcentaje_menor_18,
        tamanyo_medio_hogar                  as sc_tamanyo_medio_hogar,
      
        -- geom from building
        a.geom as geom
      from
        :buildingsingle a inner join
        :secciones b on
        st_contains(b.geom, st_centroid(a.geom));
      ```
  - #SQL Ver las **conexiones** a la base de datos
    collapsed:: true
    - ```sql
      select *
      from pg_stat_activity
      where application_name = 'geowhale';
      ```
  - #SQL Función **nullif**
    collapsed:: true
    - Útil función que devuelve **null** si se encuentra un determinado valor en un campo. Muy útil para evitar divisiones por cero, puesto que nos **null**, a diferencia de los 0, evita la división y devuelve null
    - ```sql
      -- Prototipo
      select nullif(campo, valor);
      
      -- Evitando la división por cero
      select 50/nullif(campo_con_ceros, null);
      ```
  - #SQL Evitando la **división por cero**
    collapsed:: true
    - En [[PostgreSQL]], la división de algo por NULL da NULL, así que lo que hay que hacer es convertir el divisor en NULL:
      - ```sql
        select a/NULLIF(b, 0);
        ```
- #SQL Gestión de **permisos** en la BD
  collapsed:: true
  - Dar permisos a todas las tablas (creo que también se incluyen las vistas) en un esquema a un usuario, dar permisos de uso del esquema y aplicar un privilegio por defecto futuro para que todos los objetos tabla que se creen tengan un determinado privilegio
    - ```sql
      grant select on all tables in schema dat_oferta_turistica to researcher;
      
      grant usage on schema dat_oferta_turistica to researcher;
      
      alter default privileges
      in schema dat_oferta_turistica
      grant select on tables to researcher;
      ```
- # Utilidades
  collapsed:: true
  - **vacuumdb:** para hacer vacuums
    collapsed:: true
    - Modificadores
      - **-v:** verbose
      - **-f:** full
      - **-F:** freezing agresivo
      - **-a:** todas las bases de datos
      - **-P x:** x trabajadores
      - **-z:** analyze
    - Ejemplo de vacuum de todas las bases de datos
      collapsed:: true
      - ```shell
        PGPASSWORD=whatever vacuumdb -v -f -F -a -P 4 -z \
          --force-index-cleanup \
          --maintenance-db=postgres \
          -h postgis \
          -p 5432 \
          -U postgres
        ```
    - Ejemplo de vacuum de una tabla de una base de datos, analizando sólo una columna
      collapsed:: true
      - ```shell
        PGPASSWORD=whatever vacuumdb -v -f -F -a -P 4 -z \
          --force-index-cleanup \
          --maintenance-db=postgres \
          --table='table(column)' \
          -h postgis \
          -p 5432 \
          -U postgres \
          base_de_datos
        ```
  - **reindexdb:** para rehacer los índices. **OJO:** bloquea la base de datos.
    - Modificadores
      - **-v:** verbose
      - **-j X:** número de trabajadores en paralelo
      - **-a:** reindexar todas las bases de datos
      - **-S schema:** esquema a reindexar, pueden darse múltiples opciones -S
      - **-d database:** base de datos a reindexar
    - Ejemplo para reindexar un esquema
      - ```bash
        PGPASSWORD=pass reindexdb -v -j 4 \
        	-h postgis \
            -p 5432 \
            -U postgres \
            --maintenance-db=postgres \
            -S sunnsaas \
            -d sunnsaas
        ```
    - Ejemplo para reindexar todas las bases de datos
      - ```bash
        PGPASSWORD=pass reindexdb -v -j 4 -a \
        	-h postgis \
            -p 5432 \
            -U postgres \
            --maintenance-db=postgres
        ```
- # Triggers
  collapsed:: true
  - ## Ejemplo de trigger que preprocesa los datos antes de insertarlos
    collapsed:: true
    - Un trigger simple que preprocesa las filas a insertar o actualizar antes de insertarlas. Modifica los datos de entrada en la tabla objetivo.
    - Primero, crear una función [[PL/PgSQL]] que devuelve un **trigger**. En esta función, **NEW** se refiere a los nuevos datos que van a entrar en la tabla, mientras que **OLD** se refiere a los antiguos datos, si los hubiera (update).
      - ```SQL
        create or replace function public.fn__urban_limit_preprocessing()
        returns trigger as
        $$
        begin
        
        	NEW.column_a = round(st_area(NEW.geom));
        	NEW.column_b = OLD.column_b * 2;
        
        	return NEW;
        
        end;
        $$
        language plpgsql;
        ```
    - Basado en esta función, definimos el trigger sobre la tabla.
      - ```SQL
        create trigger urban_limit_preprocess
        before insert or update on settlement.urban_limit
        for each row
        execute function fn__urban_limit_preprocessing();
        ```