- Ver también [[SunnSaaS]].
- # Despliegue de una nueva versión del algoritmo
  - Tenemos una **TEMPLATE** para documentar el despliegue de versiones del algoritmo, utilizar.
  - Diferenciamos dos escenarios: despliegue con cambios en los ficheros de configuración (**InpF.txt** y **InpFOptPar.txt**) y los que no, que se pueden desplegar en caliente.
  - ## Compilación del algoritmo en [[G/sunntics-core-restricted/monolithic-core-algorithms]]
    collapsed:: true
    - Pasos a seguir:
      + [ ] Abrir el repo en [[Visual Studio Code]] y examinar los últimos commits, sección **files changed**. Lo que se haya tocado va a determinar la forma de proceder y si estamos en un escenario **Hot Swap / API Changes**.
      + [ ] Si solo se han tocado ficheros **.for**, estamos en un escenario de caja negra. La API del algoritmo no ha cambiado y todo son cambios internos en los cálculos. Estamos en un escenario **Caja negra / Hot Swap**, que tiene un procedimiento abreviado en el que el algoritmo no tiene que pasar por un testeo en el entorno de la librería **[[libsunnsaasbackend]]**.
      + [ ] Si se han tocado los ficheros de inputs como **InpF.txt** y/o **InpFOptPar.txt** estamos en un escenario de cambio de interfaz y habrá que hacer tests en **[[libsunnsaasbackend]]**. Es el escenario **API Changes**.
      + [ ] Documentar en [[Logseq]] el cambio de algoritmo guardando el **versions.json** antiguo y el nuevo.
      + [ ] **Ambos escenarios:** una vez evaluados los cambios estaremos en un escenario de **Hot Swap** / **API Changes** hacemos pull de los commits y anotamos el **hash** del último como referencia.
      + [ ] **Ambos escenarios:** ejecutamos **docker/010** para tener un entorno de build de Fortran y hacemos **cd fortran** y **make all-prod**.
      + [ ] Se compilará y comenzará a funcionar. Generará binarios en el directorio **bin**, junto a la información de versión. Chequear el **hash**.
      + [ ] **Ambos escenarios:** salir del Docker y ejecutar **000-curated_inputs/copy_assets_to_algorithm_ready_sunnsaas.sh**. Esto copiará los binarios de **000-curated_inputs/inputs** y **fortran/bin** a las plantillas de ejecución de FEE de **[[G/sunntics-core-restricted/algorithm-ready-sunnsaas]]**. Los inputs se copiarán en ese repo a **input_new_compare** para que se puedan comparar con los actuales y detectar cambios en los ficheros de inputs como **InpF.txt** y **InpFOptPar.txt**.
  - ## Procesamiento y documentación del nuevo despliegue en [[G/sunntics-core-restricted/algorithm-ready-sunnsaas]]
    - Pasos a seguir:
      + [ ] **Ambos escenarios:** pasar a procesar en el repo [[G/sunntics-core-restricted/algorithm-ready-sunnsaas]]
      + [ ] Comprobar los nuevos cambios generados por la copia de los nuevos binarios realizada por [[G/sunntics-core-restricted/monolithic-core-algorithms]] en [[Visual Studio Code]]. Anotar en [[Logseq]] los detalles de la substitución, hashes y fechas, así como los binarios Fortran que se han visto afectados (utilizar la template).
      + [ ] **Ambos escenarios:** ejecutar **install_production** para instalar los FEE en [[G/sunntics-generic-libraries/libsunnsaasbackend]] y en [[G/sunnsaas/sunnsaas_v1]]
  - ## Despliegue final en [[G/sunnsaas/sunnsaas_v1]]
    - Pasos a seguir:
      + [ ] **Hot Swap:** ir a [[G/sunnsaas/sunnsaas_v1]], pero no hace falta generar las imágenes de los servicios.
      + [ ] Asegurarse de que la versión correcta de los **nuevos binarios y plantillas FEE** han llegado a este repositorio revisando **assets/fortran/fee/UC_EYA/bin/versions.json**. Estos cambios no están sometidos a revisión Git.
      + [ ] Ir directamente a **030_swarms**, activar el **mlkctxt** correspondiente y hacer **rsync** al host remoto objetivo.
      + [ ] Hacer **ssh** al remoto y engancharse o arrancar a la sesión **tmux** de la instancia. Asegurarse de que los nuevos binarios han llegado al host remoto (las plantillas FEE también lo habrán hecho en este caso): **cat assets/assets/fortran/fee/UC_EYA/bin/versions.json**
      + [ ] Parar el stack con **CAUTION-DATA_LOSS/900** y **905**.
      + [ ] Recargar los assets en los volúmenes con **CAUTION-DATA_LOSS/907**.
      + [ ] Chequear con el contenedor de inspección de volúmenes (**110**) que las nuevas versiones de FEE están cargadas.
      + [ ] Relanzar con **010**.
      + [ ] Lanzar cualquier cosa para ver que se está lanzando con el nuevo algoritmo.
      + [ ] **FINAL DEL PROCESO**