title:: Gestión/Tareas repetitivas

- #[[Tarea repetitiva]] **Tareas bimensuales**
  collapsed:: true
  SCHEDULED: <2023-01-01 Sun .+2m>
  - Limpiar material **Docker antiguo** (ver ((6362a2ff-a13c-4149-9da3-fbc9b285bee9))) (15 min)
    collapsed:: true
    - helios
    - kepler
    - erebus
    - AWS: beta.api.sunnsaas
    - AWS: beta.sunnsaas
  - Resetear los perfiles **tmuxinator** (mlktmuxinatorprofilesclean) (también en **erebus**)
  - Revisar **Dropbox/10-desktop** (15 min)
- #[[Tarea repetitiva]] **Tareas 6 meses**
  collapsed:: true
  SCHEDULED: <2023-01-01 Sun .+6m>
  - Revisar y almacenar repositorios [[Git]] que ocupen mucho espacio y que no se estén utilizando (30 min por máquina)
    collapsed:: true
    - Cada cierto tiempo se revisan los repositorios Git de las diversas máquinas para ver cuáles están ocupando mucho espacio y **no se han utilizado en un mes** para quitarlos de enmedio de forma ordenada y hacerle una copia de seguridad. Los repositorios activos están sometidos a las copias de seguridad caseras, aparte de estar en [[GitHub]], por supuesto, pero una vez se quitan del diretorio **/home/git** se pierde la copia. Por ello, estos repositorios son retirados, comprimidos y almacenados en otro lugar donde también se le hacen copias de seguridad.
    - A la hora de decidir qué repos se almacenan usar **mlkhdsizes** para ver los que ocupan más espacio. Si el último commit (**git log**) tiene una fecha que no es del mes en curso o del mes anterior, es candidato a ser retirado.
    - Una vez identificado un repo a almacenar, seguir los siguientes pasos
      collapsed:: true
      - Solventar cualquier **commit y pull** pendiente y hacer, si procede, Git Flow merges y demás operaciones de mantenimiento
        
        ```shell
        git fetch -av
        
        git status
        
        git branch -av
        
        git tag
        
        git show [ tag ]
        
        git pull --tag
        
        git remote
        
        git remote show origin
        
        dvc status
        
        dvc pull
        ```
      - ir a la página del repo en GitHub y chequear las tags y las ramas ahí, para que la copia local sea un clon de lo que hay en GitHub
      - comprimir el repo con TAR con el material de DVC incluido, si tiene
        
        ```shell
        tar -jcvf YYYY-MM-DD-repo_name.tar.bz2 directorio_repo/
        ```
      - mover el TAR a **euler/barracuda/git_backup** y almacenarlo en su carpeta de familia
      - Borrar el repo del local
    - Máquinas a revisar
      collapsed:: true
      - euler
      - helios
      - erebus
  - Check tags folders (only one level, do not enter into them) to see active and inactive projects
- #[[Tarea repetitiva]] **5 días:** Chequear **@Facilita**, a ver si se ha cerrado mi expediente
  SCHEDULED: <2022-12-26 Mon>
- [#C] #[[Tarea repetitiva]] **1 mes:** revisar **Gmail 001**
  SCHEDULED: <2023-01-22 Sun>
- #[[Tarea repetitiva]] **1 semana:** revisar **df -h** en AWS API SunnSaaS
  SCHEDULED: <2022-12-23 Fri>
- #[[Tarea repetitiva]] **Anual:** crearle al repositorio [[Logseq]] un tag con el año que acaba de acabar y hacer un commit
  SCHEDULED: <2023-01-01 Sun>
- #[[Tarea repetitiva]] **2 meses:** limpieza [[Logseq]] (15 min)
  collapsed:: true
  SCHEDULED: <2023-02-16 Thu>
  - Si ya estamos entrados en otro año y se ha hecho la tag anual de conservación del estado del grafo del año pasado, hacer un **mlkgraphlog** para ver si hay marcas de tiempo en meses que van más allá de Octubre del año pasado para ir liberando espacio en el grafo, borrando esas tareas que tienen logs de tiempo fuera del año actual menos esos tres meses
  - Observar el **grafo** de [[Logseq]] (G G) para identificar tags que no merecen la pena
  - En VSC, ver la lista de **pages** para ver si hay alguna que llame la atención
- #[[Tarea repetitiva]] **2 semanas:** limpiar **Linkedin** (10 min)
  SCHEDULED: <2022-12-28 Wed>
- [#A] #[[Tarea repetitiva]] **2 semanas:** hacer **copia de seguridad de helios** y traer disco duro a casa 
  SCHEDULED: <2023-01-04 Wed>
- #[[Tarea repetitiva]] **1 mes:** chequear pago **oficina Alta Vista**
  SCHEDULED: <2023-01-01 Sun>
- #[[Tarea repetitiva]] **1 mes:** revisar Gmail **002 - Mensual**
  SCHEDULED: <2023-01-01 Sun>
- #[[Tarea repetitiva]] **1 mes:** copia de seguridad en [[kepler]]  de las bases de datos de [[Cell]] (cell_raw_data y cell), el script está en kepler **apps/cell_db_dumps**, ejecutar localmente con una sesión **tmux**. La base del script está en **Dropbox/devops/kepler**.
  SCHEDULED: <2023-01-14 Sat>
- [#C] #[[Tarea repetitiva]] **1 mes:** ver si hay una nueva versión de [[Logseq]]. Se puede ver la instalada en **Settings** (actualmente la 0.8.8 y la 0.8.9 nos han ido realmente mal a la hora de abrir varias pantallas). Revisar actualizaciones de las extensiones también, que van aparte.
  SCHEDULED: <2022-12-01 Thu>
- #[[Tarea repetitiva]] **1 mes:** **Mantenimiento de máquinas:** mlkmaintenance y df -h
  collapsed:: true
  SCHEDULED: <2023-01-02 Mon>
  - helios
  - kepler
  - AWS: beta.api.sunnsaas
  - AWS: beta.sunnsaas
- #[[Tarea repetitiva]] #Work/Toolsresearch **1 mes:** ir deprecando los bloques marcados por la tag [[procesar]] en todos los grafos (15 min)
  SCHEDULED: <2023-01-15 Sun>
  id:: 6358f8fd-6251-4cd0-9641-36d153a43891