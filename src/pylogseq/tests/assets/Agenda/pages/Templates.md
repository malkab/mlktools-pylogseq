- 000 - Journal diario
  template:: 000 - Journal diario
  template-including-parent:: false
  collapsed:: true
  - **Re-index Logseq**
  - #[[Gestión general]]
  - Este es el **único grafo que mide tiempo** y que **recoge tareas**
  - Este es un grafo **Agenda:** admite tareas y fechas
  - 30 min de **gestión general**
  - Ver los **Deadlines & Schedules**, **BLK** y **A** de **Home**
  - Todo lo etiquetado con **Work/** debe estar sometido a control de tiempo
  - **Límites de tiempo:** si puede evitarse, no más de 20 min de Toolsresearch
  - **Eisenhower**
    collapsed:: true
    - **Urgente:** LATER, estrella Gmail
    - **Importante:** A / C
    - No dedicar los **Urgentes no importantes (LATER + C)** más de 30 min al día si se puede evitar
    - No dedicar a los **Ni importantes ni urgentes (C)** más de 10 min al día si se puede evitar
  - **Entrada**
    collapsed:: true
    - **mlkgitstatus**
    - Revisar actividad en **SunnSaaS**
    - Revisar **Journals** anteriores, limpiarlos y usar el **today** para ir arrastrando tareas a hoy
    - Notas PHYS
    - Procesar **Firefox Core Bookmarks**
    - Vistacillo rápido a **Raindrop.io**
    - Deadlines & Schedules
      - #+BEGIN_QUERY
        {:title "Vencidos (incluye tareas repetitivas)"
        :query [
          :find (pull ?b [*])
          :in $ ?start ?next
          :where
          (or
            [?b :block/deadline ?d]
            [?b :block/scheduled ?d]
          )
          (not (task ?b #{"DONE"}))
          [(> ?d ?start)]
          [(< ?d ?next)]
        ]
        :inputs [:900d-before :today]
        :collapsed? true
        :breadcrumb-show? true}
        #+END_QUERY
      - #+BEGIN_QUERY
         {:title "1 semana"
        :query [
          :find (pull ?b [*])
          :in $ ?start ?next
          :where
            (or
               [?b :block/deadline ?d]
               [?b :block/scheduled ?d]
             )
             (not [?p :block/name "tarea repetitiva"]
             [?b :block/refs ?p])
            [(> ?d ?start)]
            [(< ?d ?next)]
        ]
        :inputs [:today :9d-after]
        :collapsed? true
        :breadcrumb-show? true}
         #+END_QUERY
      - #+BEGIN_QUERY
          {
            :title [:h5 "2 semanas"]
            :query [
              :find (pull ?b [*])
              :in $ ?start ?next
              :where
                (or
                  [?b :block/deadline ?d]
                  [?b :block/scheduled ?d]
                )
                (not [?p :block/name "tarea repetitiva"]
                [?b :block/refs ?p])
                [(> ?d ?start)]
                [(< ?d ?next)]
            ]
            :inputs [:8d-after :15d-after]
            :collapsed? true
            :breadcrumb-show? true
          }
          #+END_QUERY
      - #+BEGIN_QUERY
          {
            :title [:h5 "Próximo mes"]
            :query [
              :find (pull ?b [*])
              :in $ ?start ?next
              :where
                (or
                  [?b :block/deadline ?d]
                  [?b :block/scheduled ?d]
                )
                (not [?p :block/name "tarea repetitiva"]
                [?b :block/refs ?p])
                [(> ?d ?start)]
                [(< ?d ?next)]
            ]
            :inputs [:14d-after :31d-after]
            :collapsed? true
            :breadcrumb-show? true
          }
          #+END_QUERY
      - #+BEGIN_QUERY
          {
            :title [:h5 "2 próximos meses"]
            :query [
              :find (pull ?b [*])
              :in $ ?start ?next
              :where
                (or
                  [?b :block/deadline ?d]
                  [?b :block/scheduled ?d]
                )
                (not [?p :block/name "tarea repetitiva"]
                [?b :block/refs ?p])
                [(> ?d ?start)]
                [(< ?d ?next)]
            ]
            :inputs [:30d-after :62d-after]
            :collapsed? true
            :breadcrumb-show? true
          }
          #+END_QUERY
      - #+BEGIN_QUERY
          {
            :title [:h5 "6 próximos meses"]
            :query [
              :find (pull ?b [*])
              :in $ ?start ?next
              :where
                (or
                  [?b :block/deadline ?d]
                  [?b :block/scheduled ?d]
                )
                (not [?p :block/name "tarea repetitiva"]
                [?b :block/refs ?p])
                [(> ?d ?start)]
                [(< ?d ?next)]
            ]
            :inputs [:61d-after :180d-after]
            :collapsed? true
            :breadcrumb-show? true
          }
          #+END_QUERY
      - #+BEGIN_QUERY
          {
            :title [:h5 "Año próximo"]
            :query [
              :find (pull ?b [*])
              :in $ ?start ?next
              :where
                (or
                  [?b :block/deadline ?d]
                  [?b :block/scheduled ?d]
                )
                (not [?p :block/name "tarea repetitiva"]
                [?b :block/refs ?p])
                [(> ?d ?start)]
                [(< ?d ?next)]
            ]
            :inputs [:179d-after :365d-after]
            :collapsed? true
            :breadcrumb-show? true
          }
          #+END_QUERY
    - [[BLK]]
    - [[LATER]] y estrellas Gmail
    - [[A]] y Gmail 000
    - [[B]] (a deprecar)
    - [[C]] y Gmail 001
  - **Cierre**
    collapsed:: true
    - apagar **máquinas** accesorias
    - **mlkgitstatus**
    - Comprobar **docker ps**
    - Cerrar en orden los **escritorios**, haciendo commits de repos
    - revisar **perfiles tmux** abiertos
    - arreglar **commit** (sin cerrarlo), cierre de **NOW**
    - **mlkgraphclock** y **mlkgraphlog** y correcciones si se tercia
    - Cierre de **[[Logseq]]**
    - commit final **[[Logseq]]**
- WP 010: Documentación
  template:: WP 010: Documentación
  collapsed:: true
  - **Configuración de la documentación:** añadir al bloque padre las siguientes tags (en este orden para más claridad):
    collapsed:: true
    - tag de **proyecto**
    - Si es un WP de **Dropbox/tags**, añadir la tag **Dropbox/tag/tipo/nombre**, como por ejemplo **Dropbox/freelancing/cloudia/scientific/010-documentacion**
    - Si es un WP de **Git**, añadir la tag **GitRepo/familia/repo/wp**, como por ejemplo en **GitRepo/freelancing_us/cell_db_2022/010-it-main_kerdes_db**
  - **Descripción** del Work Package
  - No repetir nunca códigos de scripts, y fragmentarlos mucho, no intentar hacer muchos pasos en uno sólo
  - Los scripts marcados con **(C)** son contextuales y necesitan configuración, los scripts o pasos marcados con **(D)** incluyen digitalización manual de datos no trivial
  - Marcar con un comentario **-- D:** cualquier marca de debugging
  - Prefijos de objetos en la BD
    collapsed:: true
    - **tablas:** ninguno
    - **vistas:** vw\_\_
    - **materialized views:** mvw\_\_
  - A partir de aquí, usar entradas del **Template WP 020: Documentación de script**
- WP 020: Documentación de script
  template:: WP 020: Documentación script
  template-including-parent:: false
  collapsed:: true
  - **XXX (CD):** descripción sumaria
    - **ETE:** por determinar
    - Depurar los contenidos de los esquemas objetivo con **\\d+ esquema.***
    - **010:** posible paso A
    - **020:** posible paso B
    - **000_in**
      collapsed:: true
      - **esquema.objeto:** descripción
    - **100_digitalizacion**
      collapsed:: true
      - **esquema.objeto:** descripción
    - **500_temp**
      collapsed:: true
      - **esquema.objeto:** descripción
    - **900_out**
      collapsed:: true
      - **esquema.objeto:** descripción
- Proyectos - Gestión
  template:: Proyectos - Gestión
  template-including-parent:: false
  collapsed:: true
  - Personas
    - Usar tags de personas aquí, como por ejemplo **MQ**, etc.
    - **MQ** Álguien
    - **ME** Otra persona
  - Activos
    - Activos aquí, como repos, etc.
  - Deadlines & Schedules **NO OLVIDAR MODIFICAR EL CÓDIGO DEL PROYECTO EN LAS CONSULTAS**
      collapsed:: true
    - #+BEGIN_QUERY
      {:title "Vencidos (incluye tareas repetitivas)"
      :query [
        :find (pull ?b [*])
        :in $ ?start ?next
        :where
        [?p :block/name "work/freelancing/cloudia"]
        [?b :block/refs ?p]
        (or
          [?b :block/deadline ?d]
          [?b :block/scheduled ?d]
        )
        (not (task ?b #{"DONE"}))
        [(> ?d ?start)]
        [(< ?d ?next)]
      ]
      :inputs [:900d-before :today]
      :collapsed? true
      :breadcrumb-show? true}
      #+END_QUERY
    - #+BEGIN_QUERY
      {:title [:h5 "Hoy"]
      :query [
        :find (pull ?b [*])
        :in $ ?start ?next
        :where
        [?p :block/name "work/freelancing/cloudia"]
        [?b :block/refs ?p]
        (or
          [?b :block/deadline ?d]
          [?b :block/scheduled ?d]
        )
        (not (task ?b #{"DONE"}))
        [(> ?d ?start)]
        [(< ?d ?next)]
      ]
      :inputs [:1d-before :1d-after]
      :collapsed? true
      :breadcrumb-show? true}
      #+END_QUERY
    - #+BEGIN_QUERY
        {:title "1 semana"
      :query [
        :find (pull ?b [*])
        :in $ ?start ?next
        :where
          [?p :block/name "work/freelancing/cloudia"]
          [?b :block/refs ?p]
          (or
            [?b :block/deadline ?d]
            [?b :block/scheduled ?d]
          )
          (not
            [?p :block/name "tarea repetitiva"]
            [?b :block/refs ?p]
          )
          [(> ?d ?start)]
          [(< ?d ?next)]
      ]
      :inputs [:today :9d-after]
      :collapsed? true
      :breadcrumb-show? true}
        #+END_QUERY
    - #+BEGIN_QUERY
        {
          :title [:h5 "2 semanas"]
          :query [
            :find (pull ?b [*])
            :in $ ?start ?next
            :where
              [?p :block/name "work/freelancing/cloudia"]
              [?b :block/refs ?p]
              (or
                [?b :block/deadline ?d]
                [?b :block/scheduled ?d]
              )
              (not
                [?p :block/name "tarea repetitiva"]
                [?b :block/refs ?p]
              )
              [(> ?d ?start)]
              [(< ?d ?next)]
          ]
          :inputs [:8d-after :15d-after]
          :collapsed? true
          :breadcrumb-show? true
        }
        #+END_QUERY
    - #+BEGIN_QUERY
        {
          :title [:h5 "Próximo mes"]
          :query [
            :find (pull ?b [*])
            :in $ ?start ?next
            :where
              [?p :block/name "work/freelancing/cloudia"]
              [?b :block/refs ?p]
              (or
                [?b :block/deadline ?d]
                [?b :block/scheduled ?d]
              )
              (not
                [?p :block/name "tarea repetitiva"]
                [?b :block/refs ?p]
              )
              [(> ?d ?start)]
              [(< ?d ?next)]
          ]
          :inputs [:14d-after :31d-after]
          :collapsed? true
          :breadcrumb-show? true
        }
        #+END_QUERY
    - #+BEGIN_QUERY
        {
          :title [:h5 "2 próximos meses"]
          :query [
            :find (pull ?b [*])
            :in $ ?start ?next
            :where
              [?p :block/name "work/freelancing/cloudia"]
              [?b :block/refs ?p]
              (or
                [?b :block/deadline ?d]
                [?b :block/scheduled ?d]
              )
              (not
                [?p :block/name "tarea repetitiva"]
                [?b :block/refs ?p]
              )
              [(> ?d ?start)]
              [(< ?d ?next)]
          ]
          :inputs [:30d-after :62d-after]
          :collapsed? true
          :breadcrumb-show? true
        }
        #+END_QUERY
    - #+BEGIN_QUERY
        {
          :title [:h5 "6 próximos meses"]
          :query [
            :find (pull ?b [*])
            :in $ ?start ?next
            :where
              [?p :block/name "work/freelancing/cloudia"]
              [?b :block/refs ?p]
              (or
                [?b :block/deadline ?d]
                [?b :block/scheduled ?d]
              )
              (not
                [?p :block/name "tarea repetitiva"]
                [?b :block/refs ?p]
              )
              [(> ?d ?start)]
              [(< ?d ?next)]
          ]
          :inputs [:61d-after :180d-after]
          :collapsed? true
          :breadcrumb-show? true
        }
        #+END_QUERY
    - #+BEGIN_QUERY
        {
          :title [:h5 "Año próximo"]
          :query [
            :find (pull ?b [*])
            :in $ ?start ?next
            :where
              [?p :block/name "work/freelancing/cloudia"]
              [?b :block/refs ?p]
              (or
                [?b :block/deadline ?d]
                [?b :block/scheduled ?d]
              )
              (not
                [?p :block/name "tarea repetitiva"]
                [?b :block/refs ?p]
              )
              [(> ?d ?start)]
              [(< ?d ?next)]
          ]
          :inputs [:179d-after :365d-after]
          :collapsed? true
          :breadcrumb-show? true
        }
        #+END_QUERY
- Documentación repo GIT
  template:: Documentación repo GIT
  collapsed:: true
  - Añadir tags de proyecto y nombre del repo y añadirle la tag **GitRepo/familia del repo/nombre del repo sin la familia**
  - Descripción del repo