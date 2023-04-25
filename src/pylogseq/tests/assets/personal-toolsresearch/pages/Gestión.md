- #procesar
- #Workflow Gestión de proyectos con [[Logseq]]
  collapsed:: true
  - En [[Logseq]] usamos un único grafo para todo. Proyectos muy, muy, muy concretos y desacoplados pueden usar un grafo aparte para ellos sólos si se considera que su contenido va a polucionar absurdamente al grafo principal de trabajo. Por ejemplo, un proyecto de trabajo debe ir al grafo principal, puesto que aportará información técnica importante y valiosa. Pero una aventura rolera, por ejemplo, sólo molestará.
  - Algunas tags importantes y recurrentes
    - **Reunión:** marca reuniones en el diario;
    - **procesar / TODO:** cosas a revisar.
  - Cada proyecto tendrá una tag del tipo **Work/whatever/whatever**. Las cosas de casa simplemente **Home** o **Fun**.
  - Cada proyecto tendrá una página en la que se utilizará la template **Proyectos - Gestión**, adaptándola a la tag de proyecto para gestionar sus SCHEDULE y DEADLINES encapsuladamente. No se incluirán tareas ni seguimiento de gestión (personas, activos, etc.) en grafos de proyecto específicos, en caso de haberlos, todo se centralizará aquí.
  - Aprovechar al máximo la capacidad de [[Logseq]] de hacer seguimiento de referencias cruzadas directas e indirectas, no hacer vistas absurdas. Las únicas vistas útiles que conservamos son las de SCHEDULED y DEADLINES, para el resto es más versátil usar las referencias.
- #Workflow Gestión de tareas con [[logseq]]
  collapsed:: true
  - Todas las tareas tienen que tener una tag de proyecto.
  - Importante: las **TAGS** de los padres **se heredan**
  - Poner **DEADLINE** apropiadamente a ciertas tareas. No usamos el **SCHEDULED** para marcar cuando realizar las tareas pero sí para indicar recordatorios cuando sea necesario. Las tareas con recordatorio SCHEDULED pueden no llevar prioridad si fuera necesario, ya que se consideran en espera.
  - Algunas tareas con **DEADLINE** tiene sentido que sean movidas al día en el que se llevan a cabo. Por ejemplo, el día X se acuerda celebrar una reunión el día Y. Cuando llegue el día Y tiene sentido cortar la tarea desde X a Y y comenzar a registrar el tiempo de reunión en el día en el que se celebra. Cuando la tarea pase a **DONE**, quitar los SCHEDULED y los DEADLINE.
  - [[Logseq]] ha sido configurado para que siempre muestre el **LOGBOOK** en todos los bloques que lo tengan. Esto permite saber si se le ha registrado tiempo en algún momento.
  - Usamos la aproximación **Current / Backlog / Icebox / Blocked** de Agile. En [[Logseq]]:
    collapsed:: true
    - **Current** tienen una prioridad **A**.
    - **Backlog** es lo que tiene una prioridad **B**, y se esperan que se realicen a corto / medio plazo.
    - **Icebox** es lo que tiene una prioridad **C**, y se esperan que se hagan en algún momento a muy largo plazo.
    - **Blocked** es una categoría especial que indica que estas tareas están bloqueadas a la espera de respuesta de alguna otra persona. Se le da una tag **BLK**. Deben tener usualmente un **SCHEDULED** como recordatorio.
  - Lo que se está haciendo en ese momento lleva un **NOW** / **LATER**, pero quitar estas marcas y dejar sólo la prioridad cuando no se estén trabajando. Las tareas deben llevar sólo la prioridad.
  - **LATER** puede utilizarse como una marca de prioridad absoluta.
  - Por lo tanto, la secuencia de prioridad es **BLOCKED > NOW / LATER > A > B > C**.
  - Otras tags usadas:
    collapsed:: true
    - **TODO** una marca TEMPORAL dentro de tareas complejas con muchos ítems para ver fácilmente qué es lo que está en curso. Quitarlas cuando la tarea esté finalizada.
    - **NOW / LATER** se usan sólo cuando las tareas están actualmente en trabajo, pero no pueden ser muy permanentes.
  - Cuando una tarea alcanza el **DONE**, quitar prioridades.
- #Workflow Gmail
  collapsed:: true
  - **Prioridades** Gmail :
    - **Starred:** prioridad total, tomar una decisión hoy, o se actúa, o se pasa a otra prioridad;
    - **000 - Diario:** revisión diaria, a ir solucionando;
    - **001 - Semanal:** revisión semanal;
    - **002 - Mensual:** revisión mensual.
- **Copias de seguridad de Desktop Linux**
  collapsed:: true
  - Para **euler** y **helios**
  - **Scripts** en **D/devops**
  - **euler:** se usan los discos externos **Alice** y **Barracura**, que duermen en Alta Vista
  - **helios:** se usa el disco **WD3000**, que duerme en casa
  - Para crear nuevos scripts, hay una plantilla de script en **mlktools-scripts/scripts_templates**
  - Las copias de **euler** de configuraciones importantes, hechas con el script **mlklinuxdesktopbackupessentials**, se hacen en los discos duros pequeños **SSD Toshiba y Samsung** y duermen en casa, uno abajo y otro arriba
- **Software Version Numbers:** start new projects always at **version 1.0.0** and start working on it at the fix number no matter what the changes are. **0 or odd** minor versions means developing versions, never go out of that until it is considered stable, at which point move to an **even** minor version number and make fixes to that. Only change major version changes on truly backward incompatible changes. **LET THE CODE MATURE BEFORE COMITTING EVEN VERSION NUMBERS**. #Workflow #software
- **Project Data** #Workflow
  collapsed:: true
  - The primary project data reservoir is **D/tags**, using the folder structure outlined at the matching boilerplate. Specially the workpackages folder is important, follow the guidelines at the boilerplate READMEs.
  - There is **Git** for code for software and data science projects. Big data goes to **DVC**.
- **Didactica and Blog Projects** #Workflow
  collapsed:: true
  - Create exercises and the like in isolated, course-independent repos. Add for example different title pages for each of the courses the exercise is being used at, and store course-dependant stuff in a Dropbox tag or repo, linking a reference to the exercises being used at the course. Same thing with the presentations.
- **Project Life Cycle** #Workflow
  collapsed:: true
  - project's start and active: **D/tags/000-current**;
  - project's not being currently working on, but somewhat active: **D/tags/010-backlog**;
  - project is done, but held for future reference: **D/tags/020-done**;
  - project archived and not very prone to revisits or reference: **samsung_hdd_1_5tb/valuable_legacy_stuff**.
- **Task Management** #Workflow
  collapsed:: true
  Follow these guidelines:
  - organize work on focus periods of 50 minutes, that is the coin of time management and is called **Focus Point (FP)**;
  - Monday, Tuesday, Wednesday, and Thursday has each 7 focus for work and 1 focus for management. Friday has 1 focus of management and 4 of work. That makes for 32 FP and 5 hours of management each week, but allocate **35 FP per week**;
  - start the week at the **Pivotal Work** project. There, set **35 hours of Sprint length** and add all the tasks for the week. For **SunnSaaS development**, just add a placeholder, since their tasks are at the **Pivotal SunnSaaS project**;
  - don't bring Pivotal Stories from one week to another. Close it with the Focus Points spent in the week that is closing and make a copy if necessary in the incoming week with its own Focus Point;
  - organize **Pivotal Work** in **Epics** for each activity, like the different **Freelancing stuff** and **Sunntics**;
  - do not add **Fun** or **Home** stuff to **Pivotal Work**. Leave it for the **mlk-docs/task** lists.

    Each time a Focus is over, do the following:
    - in Phys, mark the overall category of the activity done (MANagement, SUNntics, US, IOT, EOI, etc.);
    - in Pivotal Work, review active tasks: mark everything done as completed, but the sum of them must be 1 Focus Point. Set small ones to 0 points if necessary. If the Focus was expended in a long story, just put it in WIP mode and note the Focus Point spent in brackets in its name, like "Desarrollo SunnSaaS [4]";
    - if it was a SunnSaaS Development Story, go to the SunnSaaS Pivotal and do the same: check everything completed and add one Focus Point as described above.
- **Web bookmarks**: **Firefox bookmarks** is the main bookmark manager for projects. #Workflow
- **Organizing Music MP3** #worflow #audio
  collapsed:: true
  - Protocol for music storage and organization in MP3.

    Use **EasyTag** in Linux.

    Use **VLC** in Mac, Linux, and Windows for playing.

    All files must be in MP3 format. Convert as needed.

    Organize albums in folders that starts with the letter of the artist. Then, a folder with the artist name. And at least, a folder for the album with the structure [year]-[artist]-[name]:

    ```
    a

      acdc

        1976-acdc-dirty_deeds_done_dirt_cheap

          1976-acdc-dirty_deeds_done_dirt_cheap-00.mp3

          1976-acdc-dirty_deeds_done_dirt_cheap-01.mp3

          1976-acdc-dirty_deeds_done_dirt_cheap-02.mp3

        1976-acdc-high_voltage-international_edition

      alex_north

        1968-alex_north-2001_a_space_odyssey

    b

      basil_poledouris

        1982-basil_poledouris-conan_the_barbarian

        1997-basil_poledouris-starship_troopers

    ```

    Not available data, or lone tracks, go to folders like this:

    ```

    0000-jewel-varios

    ```

    Unknown information is to be left blank. Unknown albums are labeled as unknown in folder and file names:

    ```

    0000-scissor_sisters-unknown

      000-scissor_sisters-unknown.mp3

    ```

    As such, completely unknown files will go to:

    ```

    u

      unknown

        0000-unknown-unknown

          000-unknown-unknown.mp3

    ```

    The file name of the items from iVoox must include always the date of the item as uploaded to iVoox.

    Enter tag details:
    - **song title:** name of the episode (for example, "Valdemar | Parte 01");
    - **artist:** the people doing the radio theater (for example, "Historias (RNE)");
    - **album artist:** the original author of the work (for example, "Edgar Allan Poe");
    - **album:** the name of the dramatized work (for example, "El extraño caso del señor Valdemar");
    - **year:** if known;
    - **track;**
    - **genre:** Radio Theater for radio theater;
    - **total number of tracks.**

      Finally, give the files a square (300x300 minimum) picture. Leave the cover picture in the folder with the name **00-cover.png**.
- **FNMT Certificate** #Workflow
  collapsed:: true
  - A .p12 certificate is given by the FNMT. Import the certificate inside Firefox and protect Firefox with a master password. Then export the certificate from Firefox, creating a password protected copy. This copy is the one to be used instead of the original. Keep the original safe, or destroy it.
  - This backup can be imported then into the Mac KeyChain, where the Common Name can be accessed.
  - To configure the CICA VPN, use Tunnelblick. A folder must be created (at home) to hold all needed info. Put into it the **__ca_terena.pem__**, the .ovpn configuration, and the exported .p12 certificate. Edit and configure the .ovpn accordingly so it can reach the .p12 certificate. Then just drag and drop the .ovpn file into Tunnelblick. To connect, both the CICA user / pass and the certificate pass are needed.
- **Nóminas** #Workflow
  collapsed:: true
  - El lugar para guardar las nóminas es D/docs/administrativos/040-nominas. Hay una tarea bimensual programada para su recopilación y puesta en orden. El formato de nombre de fichero debe ser **YYYY-MM-[pagador / descripción]**. No olvidar tampoco añadir las nóminas al **log de finances**.
- **DevOps** #Workflow
  collapsed:: true
  - Machine details are stored at **mlkctxt/system**, and then all relevant setup configs are stored at **D/devops**.
- #procesar Arreglar esta página, está manga por hombro
- #Workflow #Grafo **Gestión de proyectos con [[Logseq]]**
  collapsed:: true
  - Existen **un grafo principal de gestión** que es el único que admite tareas, **000-Gestión**
  - En **D/logseq/graphs** existen algunos grafos que no tienen otro sitio y que son muy transversales, como **Fun** o **ToolsResearch**
  - Los proyectos que tienen una **D/tag** deben tener su grafo en su directorio **tag**
  - Estos grafos son **KB** de referencia, **no** admiten tareas, ni SCHEDULES ni DEADLINES. Toda la gestión debe estar centralizada en **000-Gestión**.
  - Algunos **grafos** importantes que residen en el propio repo de [[Logseq]] son:
    - #Logseq #Grafo **Home:** temas de casa
    - #Logseq #Grafo **Fun:** proyectos y material de diversión
    - #Logseq #Grafo **Toolsresearch:** material técnico no relacionado específicamente con ningún proyecto
  - Algunas tags importantes y recurrentes:
    - **Reunión:** marca reuniones en el diario;
    - **procesar / TODO:** cosas a revisar.
  - Cada proyecto tendrá una página en la que se utilizará la template **Proyectos - Gestión**, adaptándola a la tag de proyecto para gestionar sus tareas aisladamente. No se incluirán tareas ni seguimiento de gestión (personas, activos, etc.) en grafos de proyecto específicos, todo se centralizará aquí.
  - Aprovechar la capacidad que tiene [[Logseq]] de tener varias ventanas abiertas a la vez con distintos grafos.
- #Workflow **Gestión de tareas con [[logseq]]**
  collapsed:: true
  - Todas las tareas tienen que tener una tag de proyecto.
  - Poner **DEADLINE** apropiadamente a ciertas tareas. No usamos el **SCHEDULED** para marcar cuando realizar las tareas pero sí para indicar recordatorios cuando sea necesario. Las tareas con recordatorio SCHEDULED pueden no llevar prioridad si fuera necesario, ya que se consideran en espera.
  - Usamos la aproximación **Current / Backlog / Icebox / Freezed / Blocked** de Agile. En [[Logseq]]:
    - **Current** tienen una prioridad **A**.
    - **Backlog** es lo que tiene una prioridad **B**, y se esperan que se realicen a corto / medio plazo.
    - **Icebox** es lo que tiene una prioridad **C**, y se esperan que se hagan en algún momento a muy largo plazo.
    - **Freezed** es una categoría especial que se indica con la tag **FZ** y que son ocurrencias tan marginales que no queremos ni que aparezcan en los cuadros de revisión de tareas, pero que se apuntan de todas formas.
    - **Blocked** es una categoría especial que indica que estas tareas están bloqueadas a la espera de respuesta de alguna otra persona. Se le da una tag **BLK**. Deben tener un **SCHEDULED** como recordatorio.
  - Lo que se está haciendo en ese momento lleva un **NOW** / **LATER**, pero quitar estas marcas y dejar sólo la prioridad cuando no se estén trabajando. Las tareas deben llevar sólo la prioridad.
  - **LATER** puede utilizarse como una marca de prioridad absoluta.
  - Por lo tanto, la secuencia de prioridad es **BLOCKED > NOW / LATER > A > B > C > FZ**.
  - Otras tags usadas:
    - **TODO** una marca TEMPORAL dentro de tareas complejas con muchos ítems para ver fácilmente qué es lo que está en curso. Quitarlas cuando la tarea esté finalizada.
    - **NOW / LATER** se usan sólo cuando las tareas están actualmente en trabajo, pero no pueden ser muy permanentes.
  - Cuando una tarea alcanza el **DONE**, quitar prioridades.
- **Gmail and Email in General** #Workflow #procesar
  collapsed:: true
  - **Prioridades** Gmail :
    - **Starred:** priority, take a decision or act inmediatly;
    - **000 - Current:** important emails that are related with current tasks programmed in WK32. Review daily;
    - **001 - Backlog:** things that aren't critical but must be acted upon. Review weekly;
    - **002 - Icebox:** something that may be acted upon someday. Review monthly.
  - Use only the jp.perez.alcantara@gmail.com and leave the other accounts in the wild, reviewing it from time to time. Make all other accounts forward all messages to a dedicated tag at the main one. Add to the main Gmail SMTP configurations to send emails as the other accounts, plus dedicated signatures. Create inside **020 - Tags** label a structure to classify messages coming from these other accounts.
  - For Gmail, in the forwarding options, set the **Mark copy as read** option.
- **Copias de seguridad de Desktop Linux**
  collapsed:: true
  - Para **euler** y **helios**
  - **Scripts** en **D/devops**
  - **euler:** se usan los discos externos **Alice** y **Barracura**, que duermen en Alta Vista
  - **helios:** se usa el disco **WD3000**, que duerme en casa
  - Para crear nuevos scripts, hay una plantilla de script en **mlktools-scripts/scripts_templates**
  - Las copias de **euler** de configuraciones importantes, hechas con el script **mlklinuxdesktopbackupessentials**, se hacen en los discos duros pequeños **SSD Toshiba y Samsung** y duermen en casa, uno abajo y otro arriba
- **Software Version Numbers:** start new projects always at **version 1.0.0** and start working on it at the fix number no matter what the changes are. **0 or odd** minor versions means developing versions, never go out of that until it is considered stable, at which point move to an **even** minor version number and make fixes to that. Only change major version changes on truly backward incompatible changes. **LET THE CODE MATURE BEFORE COMITTING EVEN VERSION NUMBERS**. #Workflow #software
- **Project Data** #Workflow
  collapsed:: true
  - The primary project data reservoir is **D/tags**, using the folder structure outlined at the matching boilerplate. Specially the workpackages folder is important, follow the guidelines at the boilerplate READMEs.
  - There is **Git** for code for software and data science projects. Big data goes to **DVC**.
- **Project Life Cycle** #Workflow
  collapsed:: true
  - project's start and active: **D/tags/000-current**;
  - project's not being currently working on, but somewhat active: **D/tags/010-backlog**;
  - project is done, but held for future reference: **D/tags/020-done**;
  - project archived and not very prone to revisits or reference: **samsung_hdd_1_5tb/valuable_legacy_stuff**.
- **Task Management** #Workflow
  collapsed:: true
  Follow these guidelines:
  - organize work on focus periods of 50 minutes, that is the coin of time management and is called **Focus Point (FP)**;
  - Monday, Tuesday, Wednesday, and Thursday has each 7 focus for work and 1 focus for management. Friday has 1 focus of management and 4 of work. That makes for 32 FP and 5 hours of management each week, but allocate **35 FP per week**;
  - start the week at the **Pivotal Work** project. There, set **35 hours of Sprint length** and add all the tasks for the week. For **SunnSaaS development**, just add a placeholder, since their tasks are at the **Pivotal SunnSaaS project**;
  - don't bring Pivotal Stories from one week to another. Close it with the Focus Points spent in the week that is closing and make a copy if necessary in the incoming week with its own Focus Point;
  - organize **Pivotal Work** in **Epics** for each activity, like the different **Freelancing stuff** and **Sunntics**;
  - do not add **Fun** or **Home** stuff to **Pivotal Work**. Leave it for the **mlk-docs/task** lists.

    Each time a Focus is over, do the following:
    - in Phys, mark the overall category of the activity done (MANagement, SUNntics, US, IOT, EOI, etc.);
    - in Pivotal Work, review active tasks: mark everything done as completed, but the sum of them must be 1 Focus Point. Set small ones to 0 points if necessary. If the Focus was expended in a long story, just put it in WIP mode and note the Focus Point spent in brackets in its name, like "Desarrollo SunnSaaS [4]";
    - if it was a SunnSaaS Development Story, go to the SunnSaaS Pivotal and do the same: check everything completed and add one Focus Point as described above.
- **Web bookmarks**: **Firefox bookmarks** is the main bookmark manager for projects. #Workflow
- **Organizing Music MP3** #worflow #audio
  collapsed:: true
  - Protocol for music storage and organization in MP3.

    Use **EasyTag** in Linux.

    Use **VLC** in Mac, Linux, and Windows for playing.

    All files must be in MP3 format. Convert as needed.

    Organize albums in folders that starts with the letter of the artist. Then, a folder with the artist name. And at least, a folder for the album with the structure [year]-[artist]-[name]:

    ```
    a

      acdc

        1976-acdc-dirty_deeds_done_dirt_cheap

          1976-acdc-dirty_deeds_done_dirt_cheap-00.mp3

          1976-acdc-dirty_deeds_done_dirt_cheap-01.mp3

          1976-acdc-dirty_deeds_done_dirt_cheap-02.mp3

        1976-acdc-high_voltage-international_edition

      alex_north

        1968-alex_north-2001_a_space_odyssey

    b

      basil_poledouris

        1982-basil_poledouris-conan_the_barbarian

        1997-basil_poledouris-starship_troopers

    ```

    Not available data, or lone tracks, go to folders like this:

    ```

    0000-jewel-varios

    ```

    Unknown information is to be left blank. Unknown albums are labeled as unknown in folder and file names:

    ```

    0000-scissor_sisters-unknown

      000-scissor_sisters-unknown.mp3

    ```

    As such, completely unknown files will go to:

    ```

    u

      unknown

        0000-unknown-unknown

          000-unknown-unknown.mp3

    ```

    The file name of the items from iVoox must include always the date of the item as uploaded to iVoox.

    Enter tag details:
    - **song title:** name of the episode (for example, "Valdemar | Parte 01");
    - **artist:** the people doing the radio theater (for example, "Historias (RNE)");
    - **album artist:** the original author of the work (for example, "Edgar Allan Poe");
    - **album:** the name of the dramatized work (for example, "El extraño caso del señor Valdemar");
    - **year:** if known;
    - **track;**
    - **genre:** Radio Theater for radio theater;
    - **total number of tracks.**

      Finally, give the files a square (300x300 minimum) picture. Leave the cover picture in the folder with the name **00-cover.png**.
- **FNMT Certificate** #Workflow
  collapsed:: true
  - A .p12 certificate is given by the FNMT. Import the certificate inside Firefox and protect Firefox with a master password. Then export the certificate from Firefox, creating a password protected copy. This copy is the one to be used instead of the original. Keep the original safe, or destroy it.
  - This backup can be imported then into the Mac KeyChain, where the Common Name can be accessed.
  - To configure the CICA VPN, use Tunnelblick. A folder must be created (at home) to hold all needed info. Put into it the **__ca_terena.pem__**, the .ovpn configuration, and the exported .p12 certificate. Edit and configure the .ovpn accordingly so it can reach the .p12 certificate. Then just drag and drop the .ovpn file into Tunnelblick. To connect, both the CICA user / pass and the certificate pass are needed.
- **Nóminas** #Workflow
  collapsed:: true
  - El lugar para guardar las nóminas es D/docs/administrativos/040-nominas. Hay una tarea bimensual programada para su recopilación y puesta en orden. El formato de nombre de fichero debe ser **YYYY-MM-[pagador / descripción]**. No olvidar tampoco añadir las nóminas al **log de finances**.
- **DevOps** #Workflow
  collapsed:: true
  - Machine details are stored at **mlkctxt/system**, and then all relevant setup configs are stored at **D/devops**.
- #procesar Arreglar esta página, está manga por hombro
- # Facturas, recibos, etc.
  collapsed:: true
  - Principalmente están en **D/docs/administrativos/030/00**, donde se organizan por año
  - La **plantilla** está en **990**
  - También más o menos todo suele estar en **OneDrive**, al ser ficheros Word, en la carpeta **Financial**, pero la **SOT** (Source Of Truth) debe ser las copias en Dropbox
