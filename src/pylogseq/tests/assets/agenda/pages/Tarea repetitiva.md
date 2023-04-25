title:: Tarea repetitiva

- [#C] #[[Tarea repetitiva/2 semanas]]: limpiar **Linkedin** (10 min).
  SCHEDULED: <2023-04-25 Tue>
- [#C] #[[Tarea repetitiva/1 mes]]: revisar los emails **GM**.
  SCHEDULED: <2023-05-17 Wed>
- [#A] #[[Tarea repetitiva/2 semanas]]: hacer **copia de seguridad de helios** y traer disco duro a casa. El disco duro es **WD3000**. El script está en **devops**.
  SCHEDULED: <2023-05-02 Tue>
- [#A] #[[Tarea repetitiva/1 mes]]: chequear pago **oficina Alta Vista**
  SCHEDULED: <2023-05-08 Mon>
  collapsed:: true
  - Se ha pasado la factura a [[Manolo Quero]].
- [#A] #[[Tarea repetitiva/1 mes]]: **Mantenimiento de máquinas:** mlkmaintenance y df -h
  SCHEDULED: <2023-05-13 Sat>
  + [x] helios
  + [X] kepler
- [#C] #[[Tarea repetitiva/3 meses]]: limpiar material de **Docker** antiguo (ver notas **Docker** en el grafo de Toolsresearch)
  SCHEDULED: <2023-04-25 Tue>
  collapsed:: true
  - helios
  - kepler
- [#C] #[[Tarea repetitiva/2 meses]]: resetear perfiles **tmuxinator** (mlktmuxinatorprofilesclean)
  SCHEDULED: <2023-05-20 Sat>
  collapsed:: true
  - erebus
  - helios
  - euler
- [#C] #[[Tarea repetitiva/6 meses]]: revisar y almacenar repositorios [[Git]] en **helios** que ocupen mucho espacio y que no se estén utilizando (30 min por máquina)
  collapsed:: true
  SCHEDULED: <2023-07-20 Thu>
  - Cada cierto tiempo se revisan los repositorios Git de las diversas máquinas para ver cuáles están ocupando mucho espacio y **no se han utilizado en un mes** para quitarlos de enmedio de forma ordenada y hacerle una copia de seguridad. Los repositorios activos están sometidos a las copias de seguridad caseras, aparte de estar en [[GitHub]], por supuesto, pero una vez se quitan del diretorio **/home/git** se pierde la copia. Por ello, estos repositorios son retirados, comprimidos y almacenados en otro lugar donde también se le hacen copias de seguridad.
  - También hay muchos repositorios de tratamiento de datos que utilizan datos transitorios y resultados que se pueden borrar.
  - A la hora de decidir qué repos se almacenan usar **mlkhdsizes** para ver los que ocupan más espacio. Si el último commit (**git log**) tiene una fecha que no es del mes en curso o del mes anterior, es candidato a ser retirado.
  - #Git #GitHub #Procedimiento Una vez identificado un repo a almacenar, seguir los siguientes pasos
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
      ```
    - ir a la página del repo en GitHub y chequear las tags y las ramas ahí, para que la copia local sea un clon de lo que hay en GitHub
    - comprimir el repo con TAR con el material de DVC incluido, si tiene
      
      ```shell
      tar -jcvf YYYY-MM-DD-repo_name.tar.bz2 directorio_repo/
      ```
    - mover el TAR a **euler/barracuda/git_backup** y almacenarlo en su carpeta de familia
    - Borrar el repo del local
- [#C] #[[Tarea repetitiva/6 meses]]: revisar las **D/tags** para ver cuales están activas y cuales no
  SCHEDULED: <2023-07-20 Thu>
- [#A] #[[Tarea repetitiva/1 semana]]: revisar **df -h** en AWS API SunnSaaS, tenemos un Playbook Ansible en **devops** para hacerlo remoto
  SCHEDULED: <2023-04-25 Tue>
  collapsed:: true
  - ```shell
    ssh-add ~/.aws/aws-ec2-keys.pem
    
    ansible-playbook -i inventory.yaml -v 010-playbook-df_h.yaml
    ```
- [#A] #[[Tarea repetitiva/1 mes]]: **Mantenimiento de máquinas:** mlkmaintenance y df -h
  collapsed:: true
  SCHEDULED: <2023-05-13 Sat>
  - Tenemos un **Ansible** en **devops**
    collapsed:: true
    - ```shell
      ssh-add ~/.aws/aws-ec2-keys.pem
      ansible-playbook -i inventory.yaml -v 020-playbook-mlkmaintenance.yaml
      ```
  - Máquinas
    + [X] AWS: beta.api.sunnsaas
    + [X] AWS: beta.sunnsaas
- [#C] #[[Tarea repetitiva/3 meses]]: limpiar material de **Docker** antiguo (ver notas **Docker** en el grafo de Toolsresearch)
  SCHEDULED: <2023-04-25 Tue>
  collapsed:: true
  - AWS: beta.api.sunnsaas
  - AWS: beta.sunnsaas
- [#C] #[[Tarea repetitiva/1 mes]]: ver si hay una nueva versión de Logseq para instalar en [[helios]] y [[euler]]. Utilizar el script mlklogsequpdate tras haber bajado la última versión Linux Zip desde [Releases · logseq/logseq · GitHub](https://github.com/logseq/logseq/releases). La última versión, la 0.9.1, tiene una pinta magnífica, los whiteboards funcionan y el sync también. Hay que hacer resync y el config.edn tiene fallos, copiar desde agenda. Instalada la 0.9.1, funciona muy bien.
  SCHEDULED: <2023-05-01 Mon>
- [#A] #[[Tarea repetitiva/2 semanas]]: copia de seguridad en [[kepler]]  de las bases de datos de [[Cell]] (cell_raw_data y cell)
  SCHEDULED: <2023-04-25 Tue>
  collapsed:: true
  - Activar el tmux **devops**
  - Ir a **kepler** y activar el contexto **default**
  - **ssh** y abrir una sesión **tmux remota**, ir a **apps/cell_db_dumps** y ejecutar el script
  - Traer a **D/Tags**
- [#C] #[[Tarea repetitiva/3 meses]]: revisar **GM 002 - Long Term**.
  SCHEDULED: <2023-04-25 Tue>