filters:: {"wp" true, "done" false, "c" true}
title:: Work/Freelancing/US

- Personas
  collapsed:: true
  - [[Pepe Ojeda]] Pepe Ojeda
  - [[Jesús Rodríguez]] Jesús Rodríguez
  - [[Teresa Rodríguez]] Teresa Rodríguez (hija de Jesús)
- Activos
  collapsed:: true
  - Tenemos en el CICA un servidor de la Amaya llamado **us-dgf-001**.
- #GitRepo/freelancing_us/cell_db_2022/010-process-integracion_datos_poblacion_2020 Integración de los datos de población de [[Antonio Campos]]
  collapsed:: true
  - [#A] DOCUMENTAR la función nullif() y documentar el cambio en cómo hemos tratado todos los secretos estadísticos -1 en datos que no son la población final
  - Integración de los datos de población 2020 de [[Antonio Campos]] para dejarlos listos para posteriores procesos
  - No repetir nunca códigos de scripts, y fragmentarlos mucho, no intentar hacer muchos pasos en uno sólo
  - Los scripts marcados con **(C)** son contextuales y necesitan configuración, los scripts o pasos marcados con **(D)** incluyen digitalización manual de datos no trivial
  - Marcar con un comentario **-- D:** cualquier marca de debugging
  - Prefijos de objetos en la BD
    collapsed:: true
    - **tablas:** ninguno
    - **vistas:** vw\_\_
    - **materialized views:** mvw\_\_
  - A partir de aquí, usar entradas del **Template WP 020: Documentación de script**
  - **005-database_preparations.sql:** creación del esquema **poblacion_ieca_2020**
    collapsed:: true
    - **ETE:** despreciable
    - 900_out
      - **poblacion_ieca_2020:** esquema para llevar a cabo el trabajo del WP
  - **010-gdal.sh:** importación de la información origen a [[PostgreSQL]] con [[GDAL]]
    collapsed:: true
    - **ETE:** no evaluado
    - 000_in
      - **datos originales:** la última vez, una [[File Geodatabase]] de [[ESRI]] con una tabla única posiblemente llamada **poblacion_ieca_2020**
    - 900_out
      - **poblacion_ieca_2020.poblacion_ieca_2020:** tabla en bruto importada
  - **020-etl.sql:** ETL de datos originales
    collapsed:: true
    - **ETE:** por evaluar
    - ETL con [[SQL]] de datos originales, creando el esquema **ieca_250_cells_bundle_2020** para los datos transformados
    - 000_in
      - **poblacion_ieca_2020.poblacion_ieca_2020:** datos originales en bruto
    - 900_out
      - **ieca_250_cells_bundle_2020.cells:** los datos exportados y normalizados como vista materializada. Tiene la geometría transformada a 3035. Incluye todas las celdas, incluidas las de secreto estadístico, pero las celdas que tenían en **población_total** la marca de secreto estadístico -1 ha sido substituida por el valor máximo **4**, dejando el valor original de campo en el campo **poblacion_total_original**.
- #GitRepo/freelancing_us/cell_db_2022/025-etl-renta_espe_2019 Datos de renta de [[Esperanza Sánchez]], año 2019
  collapsed:: true
  - **NOTA IMPORTANTE:** se usa esta versión de los datos de [[Esperanza Sánchez]] dado que la versión 2020 tiene datos de origen a **NULL** de difícil resolución. Se adapta, con ayuda de [[GeoWhale]], el esquema de esta versión de los datos a la esperada en 2020 para que se integren con facilidad en el análisis de [[GitRepo/freelancing_us/cell_db_2022/080-adscripcion_variable_b]].
  - No repetir nunca códigos de scripts, y fragmentarlos mucho, no intentar hacer muchos pasos en uno sólo
  - Los scripts marcados con **(C)** son contextuales y necesitan configuración, los scripts o pasos marcados con **(D)** incluyen digitalización manual de datos no trivial
  - Marcar con un comentario **-- D:** cualquier marca de debugging
  - Prefijos de objetos en la BD
    collapsed:: true
    - **tablas:** ninguno
    - **vistas:** vw\_\_
    - **materialized views:** mvw\_\_
  - A partir de aquí, usar entradas del **Template WP 020: Documentación de script**
  -
- #GitRepo/freelancing_us/cell_db_2022/030-etl-renta_espe_2020 Tratamiento de la información sobre secciones censales generada por [[Esperanza Sánchez]]
  collapsed:: true
  - **NOTA IMPORTANTE:** estos datos tienen algunas secciones censales **NULL** en origen que lo invalidan para ser procesados junto a otros datos del 2020 (catastro e IECA). A la espera de que [[Esperanza Sánchez]] y [[Pepe Ojeda]] lleguen a alguna conclusión acerca de cómo solucionarlo.
  - Este WP genera la primera fuente de datos, la renta en secciones. De por sí, esta fuente de datos no es suficiente. Se necesita la renta, la población y el catastro para generar una capa en la que la resolución se baja desde las secciones aquí planteadas a los building de catastro.
  - No repetir nunca códigos de scripts, y fragmentarlos mucho, no intentar hacer muchos pasos en uno sólo
  - Los scripts marcados con **(C)** son contextuales y necesitan configuración, los scripts o pasos marcados con **(D)** incluyen digitalización manual de datos no trivial
  - Marcar con un comentario **-- D:** cualquier marca de debugging
  - Prefijos de objetos en la BD
    collapsed:: true
    - **tablas:** ninguno
    - **vistas:** vw\_\_
    - **materialized views:** mvw\_\_
  - **010-load_data.sh (C):** importación de datos en bruto. Configuración en el propio script para seleccionar la información de origen.
    collapsed:: true
    - **ETE:** EVALUAR
    - Depurar los contenidos de los esquemas objetivo con **\\d+ esquema.***
    - Crea el esquema **renta_espe_2020** en la base de datos
    - Importa desde el origen de datos (el último válido era una File Geodatabase) la tabla de puntos con [[GDAL]]
    - Importa desde el origen de datos la tabla de polígonos con [[GDAL]], previa limpieza topológica con [[GRASS]]
    - 000_in
      - **origen de datos en File Geodatabase/adrh_secciones_2020_puntos:** SC como puntos
      - **origen de datos en File Geodatabase/adrh_secciones_2020:** SC como polígonos
    - 500_temp
      - Un espacio de trabajo [[GRASS]] para la limpieza topológica
    - 900_out
      - **renta_espe_2020.renta_original_point:** importación de la capa puntual
      - **renta_espe_2020.renta_original_poly:** importación de la capa poligonal
  - **020-process.sql (C):** procesamiento ETL de los datos en SQL. Configuración en el propio script para seleccionar la tabla de origen.
    collapsed:: true
    - **ETE:** 2.5s
    - Sólo se trata la tabla de polígonos. Se le hacen algunas transformaciones de esquema para adecuarlas a la primera versión del mismo y se filtran las provincias andaluzas. Se adapta al esquema de la primera versión de la renta (del 2018) ya planteada en el [[GitRepo/freelancing_us/cell_db/wp-2021-06-12-00-etl-renta_espe]]. Las geometrías están ya transformadas a 3035.
    - Transforma la capa poligonal con [[SQL]] para generar la capa de polígonos final, incluyendo reproyección a 3035. Abandona la clave primaria original **ogc_fid** y la transforma a **ogc_fid_original**, creando una clave primaria **gid** en su lugar.
    - 000_in
      - **renta_espe_2020.renta_poly:** información original poligonal
    - 900_out
      - **renta_espe_2020.renta_poly:** vista materializada con el resultado de la transformación
  - **100-test_ieca_sc-DEPRECATED.sql:** distribuye los datos de la sección censal sobre la cuadrícula del IECA en función del porcentaje del área colisionante.
    collapsed:: true
    - **DEPRECATED:** este análisis ha sido descartado por Pepe Ojeda.
    - **ETE:** por determinar
    - 000_in
      - **renta_espe_2020.renta_poly:** datos de renta poligonales
      - **ieca_250_cells_bundle_2020.cells:** datos de población IECA
    - 900_out
      - **trash.a:** vista materializada con resultados
- #Work/Freelancing/US #GitRepo/freelancing_us/cell_db_2022/070-adscripcion_variable_a
  collapsed:: true
  - **Este WP está obsoleto en favor de 080.**
  - En este WP se hace el análisis final de overlay de las capas de **catastro**, **población** y **secciones censales** por el procedimiento A, es decir, el que no tiene en cuenta el dato de **tamanyo_medio_hogar** de las secciones censales. El método B, en [[GitRepo/freelancing_us/cell_db_2022/080-adscripcion_variable_b]], sí lo tiene en cuenta.
  - No repetir nunca códigos de scripts, y fragmentarlos mucho, no intentar hacer muchos pasos en uno sólo
  - Los scripts marcados con **(C)** son contextuales y necesitan configuración, los scripts o pasos marcados con **(D)** incluyen digitalización manual de datos no trivial
  - Marcar con un comentario **-- D:** cualquier marca de debugging
  - Prefijos de objetos en la BD
    collapsed:: true
    - **tablas:** ninguno
    - **vistas:** vw\_\_
    - **materialized views:** mvw\_\_
  - **010:** contextos SQL, **test** y **production**. Test hace los procesos sobre la información que colisiona por BB con un municipio objetivo y sus vecinos
  - **020 (C):** creación de esquema y datos **test**
    collapsed:: true
    - **ETE:** <20s en **test** denso (Sevilla), <5s en **test** ligeros (Puebla de los Infantes)
    - **NOTA:** si no se especifica esquema de objeto, éste será **:schema**
    - Creación del esquema de trabajo **:schema** y, si se ha activado el contexto **test**, de los datos de ejemplo en forma de vistas materializadas. Los datos de ejemplo se generan cogiendo un municipio por objetivo (por código INE) y seleccionando toda la información que colisiona con él y adyacentes.
    - 000_in
      - **context.municipio:** solo **test**, catálogo de municipios
      - **dat_catastro_2020_process.buildingsingle:** la vista materializada de los buildings single part con el reparto estimado de las viviendas por área, pero se incluyen todas los building, incluidos los que no tienen viviendas, reproyectadas a 3035. Se utiliza el campo **estimatednumberofdwellings_constru** como estimación. Producida por [[GitRepo/freelancing_us/cell_db_2022/050-etl-catastro_2020]] .
      - **ieca_250_cells_bundle_2020.cells:** producida por [[GitRepo/freelancing_us/cell_db_2022/010-process-integracion_datos_poblacion_2020]], contiene las celdas IECA proyectadas a 3035. Las celdas que tenían en **población_total** la marca de secreto estadístico -1 ha sido substituida por el valor máximo **4**, dejando el valor original de campo en el campo **población_total_original**.
      - **renta_espe_2020.renta_poly:** producida por [[GitRepo/freelancing_us/cell_db_2022/030-etl-renta_espe_2020]], contiene los datos de secciones censales sin filtro, con esquema estándar, y transformación geom a 3035.
    - 100_digitalizacion
    - 500_temp
      - **mvw\_\_test_mun:** sólo test, selección de municipios objetivo
      - **mvw\_\_buildingsingle:** sólo test, extracción de los building de dat_catastro_2020_process.buildingsingle colisionantes con zona test
      - **mvw\__ieca_cells:** sólo test, extracción de los buildings de ieca_250_cells_bundle_2020.cells colisionantes con zona test
      - **mvw\__secciones:** sólo test, extracción de las secciones censales de renta_espe_2020.renta_poly colisionantes con la zona test
    - 900_out
      - **:schema:** esquema de trabajo
  - **030 (C):** proceso principal
    collapsed:: true
    - **ETE:** <2min en **test** denso (Sevilla), <15s en **test** ligeros (Puebla de los Infantes)
    - **NOTA:** si no se especifica esquema de objeto, éste será **:schema**
    - Se hace la intersección entre las celdas del IECA y los single buildings para obtener la tabla **mvw\__poblacion_building_inter** con la que se obtiene el reparto del área para cada building part según caen en distintas celdas del IECA con idea de hacer un reparto de las viviendas que hay en dichas subpartes de los building part. El **área** sirve, no hay que ir al volumen, dado que el polígono tiene siempre la misma altura. De esta intersección salen tanto polígonos como multipolígonos, por lo que no hay que preocuparse por reunificar partes que caen en la misma celda IECA. En el campo **estimatednumberofdwellings_constru_ratio_area** se encuentra el reparto por área del número total de viviendas. En el **ratio_area** la fracción de área del total del fragmento. Se arrastran todos los campos de las tablas participantes, con geometría de los fragmentos de buildings.
    - Posteriormente se hace, basada en **mvw\__poblacion_building_inter**, el sumatorio total por celda IECA del número de viviendas (**estimatednumberofdwellings_constru_ratio_area**) en la celda, obteniéndose la tabla auxiliar **mvw\__total_dwellings_in_ieca_cell**
    - Basándose en las dos tablas anteriores se genera **mvw\__poblacion_building**, en la que la población de cada celda IECA se reparte proporcionalmente al número de viviendas en cada fragmento de building. El total de población asignada al fragmento de building se codifica en el campo **poblacion_building**.
    - Se obtiene, como control de calidad y errores, la tabla **mvw\__error_ieca_poblacion_no_viviendas**, que contiene los fragmentos de building en celdas IECA que, presentando población, no encuentran viviendas
    - Ahora hay que hacer el overlay con las **secciones censales**. Las secciones censales contienen más o menos bien los fragmentos de building, por lo que no se va a hacer una intersección poligonal como en el caso de los buildingsingle originales y las celdas IECA. Se hará un JOIN espacial entre los centroides de los fragmentos de building (**mvw\__poblacion_building.building_geom_centroid**) y los polígonos de secciones censales, por inclusión. Para ver la magnitud de los errores que se puedan estar cometiendo se ha creado la tabla **mvw\__qa_building_2_sc** en la que se vuelcan todos los fragmentos de building (con sus centroides) que pisan más de una sección censal. La tabla final resultante se llama **mvw\__building_poblacion_sc** y **contiene todo lo necesario** para hacer la **asignación de rejilla por media ponderada de las rentas y población:** una **geometría puntual** (el centroide de los fragmentos de building), la **población total asignada** al fragmento en virtud del porcentaje de viviendas asignadas al fragmento (factor de ponderación) y todos los datos de renta.
    - 000_in
      - **dat_catastro_2020_process.buildingsingle:** catastro o su equivalente testing
      - **ieca_250_cells_bundle_2020.cells:** celdas IECA o su equivalente testing
      - **renta_espe_2020.renta_poly:** secciones censales o su equivalente testing
    - 500_temp
      - **mvw\__poblacion_building_inter:** la tabla descrita arriba
      - **mvw\__total_dwellings_in_ieca_cell:** sumatorio transitorio del total de fragmentos de viviendas asociados a los fragmentos de building (según lo comentado en **mvw\__poblacion_building_inter**) para cada celda IECA, de forma que ayude a la distribución proporcional de la población en los fragmentos
    - 900_out
      - **mvw\__poblacion_building:** asignación final de la población a cada uno de los fragmentos de building (campo **poblacion_building**). Este proceso tiene un problema, y es que algunas celdas del IECA no colisionan con ningún fragmento de building con viviendas, por lo que el total de viviendas en la celda es 0 y da un error de división. Estas celdas IECA se están filtrando en la tabla **error_ieca_poblacion_no_viviendas**. Además, esta tabla lleva una nueva geometría puntual con el **centroide** del fragmento del building, que se usará para vincularlo a los datos de **secciones censales**.
      - **mvw\__error_ieca_poblacion_no_viviendas:** set de celdas del IECA que no colisionan con ningún fragmento de building con vivienda. El IECA dice que hay población, pero el catastro no encuentra viviendas donde puedan estar. Aunque es un poco contraintuitivo, la geometría no es la de la celda del IECA, sino la de los fragmentos de building que colisionan con ella. De todas formas, cada uno de ellos lleva toda la información de la celda IECA colisionante. De esta forma se puede depurar tanto los building como la propia celda.
      - **mvw\__qa_building_2_sc:** fragmentos de buildings que colisionan con más de una sección censal, polígono y centroide
      - **mvw\__building_poblacion_sc:** gran **tabla final** con la agregación a nivel de fragmento de building de todos los datos necesarios para la adscripción a rejilla
      - **mvw\__export_building_poblacion_sc_point:** exportación de puntos de la tabla final, para la exportación en GeoPackage, que no soporta múltiples columnas geom
        **mvw\__export_building_poblacion_sc_poly:** ídem, para polígonos
- LATER [#A] #Work/Freelancing/US #GitRepo/freelancing_us/cell_db_2022/080-adscripcion_variable_b
  collapsed:: true
  :LOGBOOK:
  CLOCK: [2022-12-01 Thu 09:48:37]--[2022-12-01 Thu 14:29:35] =>  04:40:58
  CLOCK: [2022-12-02 Fri 12:54:35]--[2022-12-02 Fri 13:03:00] =>  00:08:25
  CLOCK: [2022-12-02 Fri 13:03:02]--[2022-12-02 Fri 13:18:44] =>  00:15:42
  CLOCK: [2022-12-02 Fri 13:26:08]--[2022-12-02 Fri 13:30:47] =>  00:04:39
  CLOCK: [2022-12-02 Fri 13:40:06]--[2022-12-02 Fri 14:41:58] =>  01:01:52
  CLOCK: [2022-12-21 Wed 13:24:40]--[2022-12-21 Wed 13:43:24] =>  00:18:44
  CLOCK: [2022-12-21 Wed 17:34:03]--[2022-12-21 Wed 20:21:59] =>  02:47:56
  CLOCK: [2022-12-22 Thu 10:29:03]--[2022-12-22 Thu 11:11:30] =>  00:42:27
  CLOCK: [2022-12-22 Thu 11:14:14]--[2022-12-22 Thu 11:44:18] =>  00:30:04
  CLOCK: [2022-12-22 Thu 12:02:58]--[2022-12-22 Thu 12:06:04] =>  00:03:06
  CLOCK: [2022-12-22 Thu 12:15:54]--[2022-12-22 Thu 12:21:03] =>  00:05:09
  CLOCK: [2022-12-22 Thu 12:35:53]--[2022-12-22 Thu 12:45:38] =>  00:09:45
  CLOCK: [2022-12-22 Thu 12:50:21]--[2022-12-22 Thu 12:52:16] =>  00:01:55
  CLOCK: [2022-12-23 Fri 09:42:10]--[2022-12-23 Fri 09:45:31] =>  00:03:21
  :END:
  - **NOTA IMPORTANTE:** dado que los datos de renta de [[Esperanza Sánchez]] del 2020 contienen, de origen, datos a **NULL** de difícil solución inmediata, se adopta la soluión de integrar aquí los datos de renta del 2019. El tratamiento de los datos de renta del 2019 se hacen en [[GitRepo/freelancing_us/cell_db_2022/025-etl-renta_espe_2019]], mientras que los del 2020 se hacen en [[GitRepo/freelancing_us/cell_db_2022/030-etl-renta_espe_2020]]. Se hace una conversión del esquema del año 2019 al planteado para el 2020 fallido usando GeoWhale.
  - Este WP es una variación del [[GitRepo/freelancing_us/cell_db_2022/070-adscripcion_variable_a]] para ver cómo integrar el parámetro de la sección censal **tamanyo_medio_hogar**
  - No repetir nunca códigos de scripts, y fragmentarlos mucho, no intentar hacer muchos pasos en uno sólo
  - Los scripts marcados con **(C)** son contextuales y necesitan configuración, los scripts o pasos marcados con **(D)** incluyen digitalización manual de datos no trivial
  - Marcar con un comentario **-- D:** cualquier marca de debugging
  - Prefijos de objetos en la BD
    collapsed:: true
    - **tablas:** ninguno
    - **vistas:** vw\_\_
    - **materialized views:** mvw\_\_
  - **010:** contextos SQL, **test**, **production** y **litoral**. Test hace los procesos sobre la información que colisiona por BB con un municipio objetivo y sus vecinos
  - **020 (C):** creación de esquema y datos **test**
    collapsed:: true
    - **ETE:** <10s en **test** denso (Sevilla), <2s en **test** ligeros (Puebla de los Infantes)
    - **NOTA:** si no se especifica esquema de objeto, éste será **:schema**
    - Creación del esquema de trabajo **:schema** y, si se ha activado el contexto **test**, de los datos de ejemplo en forma de vistas materializadas. Los datos de ejemplo se generan cogiendo un municipio por objetivo (por código INE) y seleccionando toda la información que colisiona con él y adyacentes.
    - 000_in
      collapsed:: true
      - **context.municipio:** solo **test**, catálogo de municipios
      - **dat_catastro_2020_process.buildingsingle:** la vista materializada de los buildings single part con el reparto estimado de las viviendas por área, pero se incluyen todas los building, incluidos los que no tienen viviendas, reproyectadas a 3035. Se utiliza el campo **estimatednumberofdwellings_constru** como estimación. Producida por [[GitRepo/freelancing_us/cell_db_2022/050-etl-catastro_2020]] .
      - **ieca_250_cells_bundle_2020.cells:** producida por [[GitRepo/freelancing_us/cell_db_2022/010-process-integracion_datos_poblacion_2020]], contiene las celdas IECA proyectadas a 3035. Las celdas que tenían en **población_total** la marca de secreto estadístico -1 ha sido substituida por el valor máximo **4**, dejando el valor original de campo en el campo **población_total_original**.
      - **renta_espe_2020.renta_poly:** producida por [[GitRepo/freelancing_us/cell_db_2022/030-etl-renta_espe_2020]], contiene los datos de secciones censales sin filtro, con esquema estándar, y transformación geom a 3035.
    - 500_temp
      collapsed:: true
      - **mvw\_\_test_mun:** sólo test, selección de municipios objetivo
      - **mvw\_\_buildingsingle:** sólo test, extracción de los building de dat_catastro_2020_process.buildingsingle colisionantes con zona test
      - **mvw\__ieca_cells:** sólo test, extracción de los buildings de ieca_250_cells_bundle_2020.cells colisionantes con zona test, con geometría poligonal y centroide
      - **mvw\__secciones:** sólo test, extracción de las secciones censales de renta_espe_2020.renta_poly colisionantes con la zona test
    - 900_out
      collapsed:: true
      - **:schema:** esquema de trabajo
  - **030 (C):** proceso principal
    - **ETE:** <2min en **test** denso (Sevilla), <1min en **test** denso (Málaga), <15s en **test** ligeros (Puebla de los Infantes), **producción** aprox 15 min
    - **NOTA:** si no se especifica esquema de objeto, éste será **:schema**
    - **010:** overlay entre **building single** y **secciones censales**
      collapsed:: true
      - Se relacionan los **building single** y las **secciones censales** por contención del centroide del building, pasándose sin transformaciones toda la información de las secciones censales a los buildings. Se genera la vista materializada **:schema.mvw__building_sc**. Muy importante es que destacamos las tres estimaciones de dwellings:
        - **building_estimatednumberofdwellings_constru:** proviene del análisis de los datos CAT, del campo **estimatednumberofdwellings_constru**
        - **building_estimatednumberofdwellings_atom:** proviene del análisis de los datos ATOM, del campo **estimatednumberofdwellings**
        - **building_estimatednumberofdwellings_ieca:** proviene del análisis de la información propia del IECA, para el año 2022, lo hace Ana, y del campo **estimatednumberofdwellings_ieca**
    - **020:** overlay con **celdas IECA**
      collapsed:: true
      - Ahora se relacionan los buildings con la información de las secciones censales con las celdas del IECA. Las celdas del IECA cortan a los buildings fragmentándolos, de forma que la geometría final de esta vista materializada son los **fragmentos de buildings** según las **celdas IECA colisionantes**. Se calculan las siguientes magnitudes derivadas de esa fragmentación:
        - **ratio de área del fragmento de building frente al área del building original:** esto nos servirá posteriormente para distribuir las magnitudes asignadas a los building (entre ellas las de las secciones censales) en función de las celdas IECA. Es la columna **building_ratio_area**;
        - **distribución de los dwellings del building original en función del ratio de área:** se hace para las tres estimaciones de dwellings disponibles, distribuyendo entre los fragmentos de building en función del ratio de área descrito anteriormente:
          - **building_estimatednumberofdwellings_constru_ratio_area:** a partir de **building_estimatednumberofdwellings_constru**
          - **building_estimatednumberofdwellings_atom_ratio_area:** a partir de **building_estimatednumberofdwellings_atom**
          - **building_estimatednumberofdwellings_ieca_ratio_area:** a partir de **building_estimatednumberofdwellings_ieca**
    - **030:** cálculo de **totales en celdas IECA** para calcular los ratios de reparto
      collapsed:: true
      - Se calcula una pequeña tabla auxiliar llamada **:schema.mvw__totals_ieca_cell** en la que se sumariza el total de dwellings en fragmentos de building dentro de cada celda IECA, para las tres estimaciones de dwellings, con la idea de que este total sea el que se use para establecer el ratio de dwellings de cada fragmento con respecto a este total para distribuir las magnitudes de la celda del IECA y la renta en los propios buildings. A diferencia del **método A** del [[GitRepo/freelancing_us/cell_db_2022/070-adscripcion_variable_a]], donde la población total del IECA se repartía en función del número de dwellings asignado a cada fragmento de building, en este se tiene en cuenta el **tamaño medio del hogar** que dice la sección censal. Para ello, se multiplica dicho parámetro por el número de dwellings del fragmento en las tres estimaciones, lo que nos dará una nueva magnitud que llamamos **potencial_poblacion_vivienda_tamanyo_hogar_X**. La suma total de dicho magnitud se suma para toda la celda IECA para después repartir la población proporcionalmente al mismo. Se calculan los sumatorios de las estimaciones de **dwellings** y del potencial de población teniendo en cuenta el tamaño medio del hogar de la sección censal para las **tres estimaciones de dwellings** (constru, ATOM e IECA).
    - **040:** distribución de la **población** en los fragmentos de edificio
      collapsed:: true
      - Se distribuye la población del IECA entre los fragmentos de buildings ponderados por el ratio del fragmento en **potencial_poblacion_vivienda_tamanyo_hogar** y el total de este parámetro para toda la celda IECA. Estos son los **datos finales** en los que tanto los datos de la sección censal como del IECA están asignados a fragmentos de edificios. Se generan datos completos de población estimada distribuida para las tres estimaciones de dwellings (con prefijos constru, atom e ieca).
    - **050:** suma de los **efectivos poblacionales** de los **fragmentos de edificio**
      collapsed:: true
      - Una vez tenemos la información referida a los **fragmentos de building**, que es la base de la nube de puntos para la **teselación**, pasamos a reconstruir una capa de edificios completos en los que se van a sumar los efectivos poblacionales calculados. Se hace a partir de la tabla **:schema.mvw__building_poblacion_estimada** con un **sum()** de las estimaciones de población para las tres estimaciones de **dwellings**. Se crea la tabla **:schema.mvw__buildingsingle_poblacion_estimada_sums**.
    - **060:** reconstrucción de los **buildings single** con las **estimaciones de población**
      collapsed:: true
      - Se hace un **left join** entre los edificios single originales de catastro y los datos de población obtenidos en **050**. Con esto se consigue tener de nuevo todos los edificios con los datos de población en la tabla **:schema.mvw__buildingsingle_poblacion_estimada**.
    - **000_in**
      collapsed:: true
      - **dat_catastro_2020_process.buildingsingle:** catastro o su equivalente testing
      - **ieca_250_cells_bundle_2020.cells:** celdas IECA o su equivalente testing
      - **renta_espe_2020.renta_poly:** secciones censales o su equivalente testing
    - **500_temp**
      collapsed:: true
      - **mvw__building_sc:** overlay de los buildings y las secciones censales por contención punto / polígono para pasar a los buildings los datos de las secciones censales en las que cae
      - **mvw\__poblacion_building_sc_inter:** intersección entre la anterior y las celdas del IECA, cortando los buildings con las celdas para obtener fragmentos de building con los datos del mismo, del IECA y de la sección censal
      - **mvw__totals_ieca_cell:** pequeña tabla auxiliar con los totales de viviendas en fragmentos de edificio por cada celda IECA
      - **testing:** diversas extracciones de testing
    - **900_out**
      collapsed:: true
      - **mvw__building_poblacion_estimada:** resultado final, población total asignada a cada fragmento de building con la población estimada por medio de los dwellings de las constru combinados con el tamaño medio del hogar de las secciones censales. Son los datos finales a gridear.
      - **mvw__buildingsingle_poblacion_estimada_sums:** reconstrucción a partir de mvw__building_poblacion_estimada de los datos totales de población para los edificios fragmentados
      - **mvw__buildingsingle_poblacion_estimada:** los buildings single originales de [[Jesús Rodríguez]] con los datos calculados de población añadidos (left join)