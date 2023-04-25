- #SQL #Geo Ejemplo de **st_intersection** y como resolver las **GEOMETRYCOLLECTION** con estilo
  collapsed:: true
  - Ver cómo se extraen las **geometrías del tipo requerido** de las GEOMETRYCOLLECTION con **st_collectionextract** (tipo 1 puntos, tipo 2 linestrings, tipo 3 polígonos). Todas las geometrías que no son GEOMETRYCOLLECTION son filtradas al tipo requerido.
    - ```sql
      /*
      
        Crea una vista con los límites de los municipios, viendo a
        quién hace frontera cada uno. Esto sólo funcionará bien si
        la topología es limpia.
      
      */
      
      /*
      
        Primero, interseccionamos las geometrías. Nos dará un montón de tipos de
        geometrías distintas, entre ellas, LineStrings con las fronteras compartidas
        entre los municipios.
      
      */
      begin;
      
      drop table if exists test.mun_inter;
      
      create table test.mun_inter as
      select
        row_number() over () as gid,
        a.cod_mun as acod_mun,
        b.cod_mun as bcod_mun,
        a.nombre as anombre,
        b.nombre as bnombre,
        a.provincia as aprovincia,
        b.provincia as bprovincia,
        st_intersection(a.geom, b.geom) as geom
      from
        test.municipios_parcial a inner join
        test.municipios_parcial b on a.ogc_fid < b.ogc_fid;
      
      alter table test.mun_inter
      add constraint mun_inter_pkey
      primary key(gid);
      
      create index mun_inter_geom_gist
      on test.mun_inter
      using gist(geom);
      
      /*
      
        Extracción de los puntos de intersección.
      
      */
      drop table if exists test.mun_inter_point;
      
      create table test.mun_inter_point as
      select
        row_number() over () as gid,
        acod_mun,
        bcod_mun,
        anombre,
        bnombre,
        aprovincia,
        bprovincia,
        st_multi(st_collectionextract(geom, 1)) as geom
      from test.mun_inter;
      
      alter table test.mun_inter_point
      add constraint mun_inter_point_pkey
      primary key(gid);
      
      create index mun_inter_point_geom_gist
      on test.mun_inter_point
      using gist(geom);
      
      /*
      
        Extracción de las líneas de intersección.
      
      */
      drop table if exists test.mun_inter_linestring;
      
      create table test.mun_inter_linestring as
      select
        row_number() over () as gid,
        acod_mun,
        bcod_mun,
        anombre,
        bnombre,
        aprovincia,
        bprovincia,
        st_multi(st_collectionextract(geom, 2)) as geom
      from test.mun_inter;
      
      alter table test.mun_inter_linestring
      add constraint mun_inter_linestring_pkey
      primary key(gid);
      
      create index mun_inter_linestring_geom_gist
      on test.mun_inter_linestring
      using gist(geom);
      
      /*
      
        Extracción de los polígonos de intersección.
      
      */
      drop table if exists test.mun_inter_poly;
      
      create table test.mun_inter_poly as
      select
        row_number() over () as gid,
        acod_mun,
        bcod_mun,
        anombre,
        bnombre,
        aprovincia,
        bprovincia,
        st_multi(st_collectionextract(geom, 3)) as geom
      from test.mun_inter;
      
      alter table test.mun_inter_poly
      add constraint mun_inter_poly_pkey
      primary key(gid);
      
      create index mun_inter_poly_geom_gist
      on test.mun_inter_poly
      using gist(geom);
      
      commit;
      ```
- # #SQL #Geo Cómo resetear los metadatos de una columna en geometry_columns con el tipo de geometría y SRID correcto
  collapsed:: true
  - Después de hacer **create table** como estos:
    ```sql
    create table context.grid_250 as
    select
      gid,
      grd_fixid,
      id_grid_25 as id_grid_250m,
      id_grid_1k as id_grid_1km,
      st_geometryn(st_transform(geom, 3035), 1) as geom
    from
      context.grid_250_import;
    ```
    La columna **geom** se queda sin metadatos de **geometrytype** y **SRID** en la tabla **geometry_columns**. Para restablecerlo:
    ```sql
    alter table context.grid_250
    alter column geom type geometry(POLYGON, 3035);
    ```
- # #SQL #Geo Coger la N geometría de un multi
  collapsed:: true
  - Ya no hay que recurrir a dump:
    ```sql
    select
      gid,
      grd_fixid,
      id_grid_25 as id_grid_250m,
      id_grid_1k as id_grid_1km,
      st_geometryn(st_transform(geom, 3035), 1) as geom
    from
      context.grid_250_import;
    ```