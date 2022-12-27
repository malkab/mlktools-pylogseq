- Ejecución interactiva en Docker
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    # -----------------------------------------------------------------
    #
    # Ejecuta una sesión interactiva en el container GRASS.
    #
    # -----------------------------------------------------------------
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
- Información de ficheros
  collapsed:: true
  - ```shell
    ogrinfo adrh_secciones_2020.gdb
    
    gdalinfo imagen.tif
    ```
- Evitar siempre las columnas OGC_FID, renombrarlas en [[PostgreSQL]], puesto que a la hora de exportar GDAL las interpreta como claves primarias y es un lío
- #Referencia #Geo #PostgreSQL En **[[GitRepo/freelancing_us/cell_db]]** hay buenos scripts de conversión y limpieza topológica de polígonos con [[GRASS]] a [[PostGIS]]
- **Migraciones** de formatos
  - Importación de **[[GeoJSON]]** a **[[PostGIS]]**
    collapsed:: true
    - ```shell
      ogr2ogr -overwrite \
        -f PostgreSQL  PG:"host=localhost user=elcano_iepg_admin dbname=elcano_iepg" \
        -s_srs "EPSG:4326" \
        -a_srs "EPSG:4326" \
        -nln import.countries_json \
        -lco SCHEMA=import \
        countries.geojson
      ```
  - Exportación de **[[PostgreSQL]] / [[PostGIS]]** a **[[GeoPackage]]**
    - Los **GeoPackage** son bases de datos **SQLite3**, por lo que se pueden abrir con ella
      - ```shell
        sqlite3 geopackage.gpkg
        ```
    - Toda la base de datos
      - ```shell
        PGCLIENTENCODING=UTF-8 ogr2ogr \
          -f GPKG thegeopackage.gpkg \
          -lco GEOMETRY_NAME=geom \
          -a_srs EPSG:4326 \
          PG:"host=localhost user=postgres dbname=dental password=postgres port=5432"
        ```
    - Varios esquemas
      - ```shell
        PGCLIENTENCODING=UTF-8 ogr2ogr \
          -f GPKG thegeopackage.gpkg \
          -lco GEOMETRY_NAME=geom \
          -a_srs EPSG:4326 \
          PG:"host=localhost user=postgres dbname=dental password=postgres port=5432 schemas=def,test"
        ```
    - Varias tablas, una con nombre complejo entre comillas
      - ```shell
        PGCLIENTENCODING=UTF-8 ogr2ogr \
          -f GPKG geopackage_file_name.gpkg \
          -a_srs EPSG:4326 \
          PG:"host=host user=user dbname=db password=password port=port" \
          "pg_schema.pg_table_to_export" test.bcn
        ```
    - Selección de una columna geométrica determinada cuando hay más de una en una tabla (GeoPackage no soporta múltiples columnas geométricas)
      - ```shell
        PGCLIENTENCODING=UTF-8 ogr2ogr \
          -f GPKG ../data/900_out/rentas_celda_ieca.gpkg \
          -lco GEOMETRY_NAME=geom \
          -a_srs EPSG:3035
          PG:"host=localhost user=postgres dbname=dental password=postgres port=5432 tables=ieca_250_cells_renta.cells(geom_centroid)"
        ```
  - Importación de **[[Shape]]** a **[[PostGIS]]**
    collapsed:: true
    - ```shell
      PGCLIENTENCODING=UTF-8 ogr2ogr \
        -overwrite \
        -progress \
        -lco GEOMETRY_NAME=geom \
        -nln municipios \
        -nlt MULTIPOLYGON \
        -a_srs EPSG:25830 \
        -f PostgreSQL PG:"host=$PG_HOST user=$PG_USER dbname=$PG_DB password=$PG_PASS port=$PG_PORT" \
        ../data/13_01_TerminoMunicipal.shp
      ```
  - Migración de [[ESRI]] **[[File GDB]]** a **[[PostGIS]]**
    collapsed:: true
    - ```shell
      #!/bin/bash
      
      PGCLIENTENCODING=UTF-8 ogr2ogr \
        -lco GEOMETRY_NAME=geom \
        -nln poblacion_ieca_2020.poblacion_ieca_2020 \
        -a_srs EPSG:25830 \
        -f PostgreSQL PG:"host=$PG_HOST user=$PG_USER dbname=$PG_DB password=$PG_PASS port=$PG_PORT" \
        ../data/000_in/datos2020.gdb
      ```
  - Importación de **[[JSON]]**: no parece ser posible importar JSON simple (no GeoJSON) con GDAL