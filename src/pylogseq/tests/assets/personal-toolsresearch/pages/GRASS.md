- # Importación de una capa de una ESRI File Geodatabase
  collapsed:: true
  - ```shell
    grass path/to/db/PERMANENT --exec \
      v.in.ogr --overwrite \
        input=../data/000_in/adrh_secciones_2020.gdb \
        layer=adrh_secciones_2020
        snap=0.01
    ```
- # Creación de un espacio de trabajo GRASS
  collapsed:: true
  - **-c:** crear la base de datos
  - **EPSG:25830:** el EPSG para usar en la base de datos
  - **-e:** salir después de la creación
  - **ruta:** dónde crearla
  - ```shell
    grass -c EPSG:25830 -e ../data/900_out/grass_db
    ```
- # Importación de una capa desde PostGIS
  collapsed:: true
  - ```shell
    grass path/to/db/PERMANENT --exec \
      v.in.ogr --overwrite \
        input="PG:host=$PG_HOST dbname=$PG_DB user=$PG_USER port=$PG_PORT password=$PG_PASS" \
        layer=municipios \
        output=municipios \
        snap=0.01
    ```