- #Referencia #Geo #PostgreSQL En **[[G/freelancing_us/cell_db]]** hay buenos scripts de conversión y limpieza topológica de polígonos con [[GRASS]] a [[PostGIS]]
- # Ejecución interactiva en Docker
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    # -----------------------------------------------------------------
    #
    # Ejecuta una sesión interactiva en el container GRASS.
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
        --name grass_dev \
        --hostname grass_dev \
        --network host \
        --user 1000:1000 \
        -v $(pwd):$(pwd) \
        --workdir $(pwd) \
        -e "PG_HOST=[{cell_db.host}]" \
      	-e "PG_PORT=[{cell_db.port}]" \
      	-e "PG_DB=cell_raw_data" \
      	-e "PG_USER=[{cell_db.users.postgres.user}]" \
      	-e "PG_PASS=[{cell_db.users.postgres.pass}]" \
        malkab/grass:holistic_hornet
    ```
- # Información de ficheros
  collapsed:: true
  - ```shell
    ogrinfo adrh_secciones_2020.gdb
    
    gdalinfo imagen.tif
    ```
- # Migraciones de formatos
  - Consideraciones generales
    collapsed:: true
    - Evitar siempre las columnas OGC_FID, renombrarlas en [[PostgreSQL]], puesto que a la hora de exportar GDAL las interpreta como claves primarias y es un lío.
  - **[[PostgreSQL]] / [[PostGIS]]:** tratamiento como parámetro de la cadena de conexión
    - Es un poco mosqueante en [[Bash]]
      - ```shell
        CELL_RAW_DATA_PG="host=${PG_HOST} user=${PG_USER} dbname=cell_raw_data password=${PG_PASS} port=${PG_PORT}"
        
        PGCLIENTENCODING=UTF-8 ogr2ogr \
          -progress \
          -f GPKG ../data/900_out/renta_pob_cat_grid.gpkg \
          PG:"${CELL_RAW_DATA_PG}" \
          -a_srs EPSG:3035 \
          -lco GEOMETRY_NAME=geom \
          -nlt MULTIPOLYGON \
          $SCHEMA.renta_pob_cat $SCHEMA.renta_pob_cat_250m
        ```
  - **[[GeoJSON]]** a **[[PostGIS]]**
    - ```shell
      PGCLIENTENCODING=UTF-8 ogr2ogr \
      ogr2ogr \
        -overwrite \
        -progress \
        -f PostgreSQL PG:"host=$PG_HOST user=$PG_USER dbname=$PG_DB password=$PG_PASS port=$PG_PORT" \
        -s_srs "EPSG:4326" \
        -a_srs "EPSG:4326" \
        -nln import.countries_json \
        -lco SCHEMA=import \
        -lco GEOMETRY_NAME=geom \
        -nlt MULTIPOLYGON \
        countries.geojson
      ```
  - **[[PostgreSQL]] / [[PostGIS]]** a **[[GeoPackage]]**
    collapsed:: true
    - Los **GeoPackage** son bases de datos **SQLite3**, por lo que se pueden abrir con ella
      collapsed:: true
      - ```shell
        sqlite3 geopackage.gpkg
        ```
    - Toda la base de datos
      - ```shell
        PGCLIENTENCODING=UTF-8 ogr2ogr \
          -progress \
          -f GPKG thegeopackage.gpkg \
          -lco GEOMETRY_NAME=geom \
          -a_srs EPSG:4326 \
          -nlt MULTIPOLYGON \
          PG:"host=localhost user=postgres dbname=dental password=postgres port=5432"
        ```
    - Varios esquemas
      collapsed:: true
      - ```shell
        PGCLIENTENCODING=UTF-8 ogr2ogr \
          -progress \
          -f GPKG thegeopackage.gpkg \
          -lco GEOMETRY_NAME=geom \
          -a_srs EPSG:4326 \
          -nlt MULTIPOLYGON \
          PG:"host=localhost user=postgres dbname=dental password=postgres port=5432 schemas=def,test"
        ```
    - Varias tablas, una con nombre complejo entre comillas
      collapsed:: true
      - ```shell
        PGCLIENTENCODING=UTF-8 ogr2ogr \
          -progress \
          -f GPKG geopackage_file_name.gpkg \
          -a_srs EPSG:4326 \
          -nlt MULTIPOLYGON \
          PG:"host=host user=user dbname=db password=password port=port" \
          "pg_schema.pg_table_to_export" test.bcn
        ```
    - Selección de una columna geométrica determinada cuando hay más de una en una tabla (GeoPackage no soporta múltiples columnas geométricas)
      collapsed:: true
      - ```shell
        PGCLIENTENCODING=UTF-8 ogr2ogr \
          -progress \
          -f GPKG ../data/900_out/rentas_celda_ieca.gpkg \
          -lco GEOMETRY_NAME=geom \
          -a_srs EPSG:3035
          -nlt MULTIPOLYGON \
          PG:"host=localhost user=postgres dbname=dental password=postgres port=5432 tables=ieca_250_cells_renta.cells(geom_centroid)"
        ```
  - Exportación de **[[PostgreSQL]] / [[PostGIS]]** a **[[GeoJSON]]**
    collapsed:: true
    - ```shell
      # Conexión a cell_raw_data
      CELL_RAW_DATA_PG="host=${PG_HOST} user=${PG_USER} dbname=cell_raw_data password=${PG_PASS} port=${PG_PORT}"
      FILE=../data/900_out/renta_pob_cat_grid.geojson
      
      PGCLIENTENCODING=UTF-8 ogr2ogr \
        -progress \
        -f GeoJSON $FILE \
        -nlt MULTIPOLYGON \
        PG:"${CELL_RAW_DATA_PG}" \
        -nln "Rejilla de renta y población completa" \
        -sql "
          select
            gid,
            zoom,
            st_transform(geom, 4326) as geom
          from
            ${SCHEMA}.renta_pob_cat"
      ```
  - Importación de **[[Shape]]** a **[[PostGIS]]**
    - ```shell
      PGCLIENTENCODING=UTF-8 ogr2ogr \
        -overwrite \
        -progress \
        -lco GEOMETRY_NAME=geom \
        -nln municipios \
        -nlt MULTIPOLYGON \
        -a_srs EPSG:25830 \
        -lco SCHEMA=ads_meteo_b \
        -f PostgreSQL PG:"host=$PG_HOST user=$PG_USER dbname=$PG_DB password=$PG_PASS port=$PG_PORT" \
        ../data/13_01_TerminoMunicipal.shp
      ```
  - Exportación de **[[PostgreSQL]] / [[PostGIS]]** a **[[CSV]]**
    collapsed:: true
    - Por defecto parece que no se exporta la geometría, aunque en la página de GDAL hay un ejemplo de cómo exportarla en GeoJSON
    - ```shell
      PGCLIENTENCODING=UTF-8 ogr2ogr \
        -progress \
        -overwrite \
        -nlt MULTIPOLYGON \
        -f CSV ../data/900_out/grid_data.csv \
        PG:"host=${PG_HOST} user=${PG_USER} dbname=cell_raw_data password=${PG_PASS} port=${PG_PORT}" \
        -sql "
          select
            gid,
            grid_id
          from ${SCHEMA}.renta_pob_cat"
      ```
    - ```shell
        PGCLIENTENCODING=UTF-8 ogr2ogr \
          -progress \
          -nlt MULTIPOLYGON \
          -f CSV "../../src/data/900_out/${NAME}_singlebuilding.csv" \
          PG:"host='$PG_HOST' user='$PG_USER' dbname='cell_raw_data' password='$PG_PASS' port='$PG_PORT'" \
          $SCHEMANAME.mvw__buildingsingle_poblacion_estimada
      ```
  - **[[ESRI]] [[File GDB]]** a **[[PostGIS]]**
    collapsed:: true
    - ```shell
      #!/bin/bash
      
      PGCLIENTENCODING=UTF-8 ogr2ogr \
        -progress \
        -lco GEOMETRY_NAME=geom \
        -nln poblacion_ieca_2020.poblacion_ieca_2020 \
        -a_srs EPSG:25830 \
        -nlt MULTIPOLYGON \
        -f PostgreSQL PG:"host=$PG_HOST user=$PG_USER dbname=$PG_DB password=$PG_PASS port=$PG_PORT" \
        ../data/000_in/datos2020.gdb
      ```
  - Importación de **[[JSON]]**: no parece ser posible importar JSON simple (no GeoJSON) con GDAL
  - Migración desde **[[PostgreSQL]]** a **[[PostgreSQL]]**, combinada con creación de índices sobre los datos exportados, a ejecutar desde la imagen Docker **[[malkab/grass]]**
    collapsed:: true
    - ```shell
      #!/bin/bash
      
      # Define the source and destination PostgreSQL connections
      src_conn="PG:host=${PG_HOST} port=${PG_PORT} dbname=cell user=${PG_USER} password=${PG_PASS}"
      dst_conn="PG:host=${PG_HOST} port=${PG_PORT} dbname=cell_raw_data user=${PG_USER} password=${PG_PASS}"
      
      # Define the source and destination tables
      src_table="export.renta_pob_cat"
      dst_table="ads_meto_b_andalucia.renta_pob_cat"
      
      # Copy data
      ogr2ogr -f "PostgreSQL" \
      	-nlt MULTIPOLYGON \
      	-overwrite -progress \
          -nln ${dst_table} \
          "${dst_conn}" \
          "${src_conn}" \
          ${src_table}
      
      # Create indexes
      PGPASSWORD=$PG_PASS psql \
        -h ${PG_HOST} \
        -p ${PG_PORT} \
        -U ${PG_USER} \
        -d cell_raw_data \
        -c "
          create index renta_pob_cat_idx
          on ${dst_table}
          using btree(grid_id, epsg, zoom, x, y);
      
          create index renta_pob_cat_geom_gist
          on ${dst_table}
          using gist(geom);
        "
      ```
  - Migración desde **[[PostgreSQL]]** a **[[PostgreSQL]]**, con una instrucción [[SQL]], iterando la creación de múltiples tablas
    collapsed:: true
    - ```shell
      #!/bin/bash
      
      # -----------------------------------------------------------------
      #
      # Migración de datos desde la base de datos de kerdes hasta kepler.
      #
      # -----------------------------------------------------------------
      # Define the source and destination PostgreSQL connections
      KERDES_CONN="PG:host=${KERDES_PG_HOST} port=${KERDES_PG_PORT} dbname=data user=${KERDES_PG_USER} password=${KERDES_PG_PASS}"
      KEPLER_CONN="PG:host=${KEPLER_PG_HOST} port=${KEPLER_PG_PORT} dbname=cell_raw_data user=${KEPLER_PG_USER} password=${KEPLER_PG_PASS}"
      
      # Define the source and destination tables
      DST_SCHEMA="analisis_datos_turisticos"
      DST_TABLE="imported_data"
      
      # Create schema if not exists
      PGPASSWORD=$KEPLER_PG_PASS psql \
        -h ${KEPLER_PG_HOST} \
        -p ${KEPLER_PG_PORT} \
        -U ${KEPLER_PG_USER} \
        -d cell_raw_data \
        -c "create schema if not exists ${DST_SCHEMA};"
      
      # Copy data, creating a new table for each variable
      VARIABLES=('V_1' 'V_2' 'V_3' 'V_12' 'V_13' 'V_14' 'V_23')
      
      for VARIABLE in "${VARIABLES[@]}"
      do
      
        echo $VARIABLE
      
        SRC_SQL="
          select *
          from dat_oferta_turistica.variables_num_rejilla_ok
          where cod_variable = '${VARIABLE}'
        "
      
        ogr2ogr -f "PostgreSQL" \
          -overwrite \
          -progress \
          -lco GEOMETRY_NAME=geom \
          -a_srs EPSG:3035 \
          -nln ${DST_SCHEMA}.${DST_TABLE}_${VARIABLE} \
          -nlt MULTIPOLYGON \
          "${KEPLER_CONN}" \
          "${KERDES_CONN}" \
          -sql "${SRC_SQL}"
      
        # Create indexes
        PGPASSWORD=$KEPLER_PG_PASS psql \
          -h ${KEPLER_PG_HOST} \
          -p ${KEPLER_PG_PORT} \
          -U ${KEPLER_PG_USER} \
          -d cell_raw_data \
          -c "
            alter table ${DST_SCHEMA}.${DST_TABLE}_${VARIABLE}
            drop column ogc_fid;
      
            create index ${DST_TABLE}_${VARIABLE}_id_grid_idx
            on ${DST_SCHEMA}.${DST_TABLE}_${VARIABLE}
            using btree(id_grid_25);
      
            create index ${DST_TABLE}_${VARIABLE}_cod_variable_idx
            on ${DST_SCHEMA}.${DST_TABLE}_${VARIABLE}
            using btree(cod_variable);
          "
      
      done;
      ```