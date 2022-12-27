- 000 - Journal diario
  template:: 000 - Journal diario
  template-including-parent:: false
  - **Entrada**
    - Deadlines & Schedules
      collapsed:: true
      - #+BEGIN_QUERY
        {:title "Vencidos"
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
    - [[LATER]]
    - [[A]]
    - [[B]]
    - [[C]]
  - **Cierre**
    - Cerrar en orden los **escritorios**, haciendo commits de repos
    - revisar **perfiles tmux** abiertos
    - apagar **máquinas** accesorias
    - arreglar **commit** (sin cerrarlo), cierre de **NOW**
    - **mlkgraphclock** y **mlkgraphlog** y correcciones si se tercia
    - Cierre de **[[Logseq]]**
    - commit final **[[Logseq]]**
    - **mlkgitstatus**