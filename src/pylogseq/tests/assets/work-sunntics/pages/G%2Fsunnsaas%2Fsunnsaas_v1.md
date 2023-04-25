filters:: {"a" true}

- # Despliegue en producción
  - Este procedimiento está descrito en el **README.md** de **docker/020_production**.
  - ## Preliminares
    - Seguir los siguientes pasos:
      + [X] Build y publicación del algoritmo. Ver [[G/sunntics-core-restricted/monolithic-core-algorithms]].
      + [X] Build y publicación de **libsunnsaasdef**. Ver [[G/sunntics-generic-libraries/libsunnsaasdef]].
      + [X] Build y publicación de **libsunnsaasbackend**. Ver [[G/sunntics-generic-libraries/libsunnsaasbackend]].
  - ## SunnSaaS V1
    - Esto está en el **README.md** de **020_production**.
    - Seguir los siguientes pasos:
      + [X] Abrir el **tmuxinator** de **sunnsaas_v1**.
      + [X] Arrancar el stack de persistencia en la pestaña **sunnsaasds** con **010**.
      + [X] Para cada componente (API, controlador y worker), activar el **mlkctxt default**, entrar en el entorno de desarrollo con **010** y hacer **yarn outdated**, **yarn upgrade** y **yarn build**. Ver que todo ha compilado correctamente.
      + [X] Testear la API y el frontend.
      + [X] Configurar el **SunnSaaS version** en **mlkctxt** (impares menores para dev, pares para estables). El sistema nunca usa la tag Docker **latest**, todas las imágenes necesitan tener una tag bien definida por esta versión. Solemos poner la versión de la plataforma, si es que ha cambiado (cambios en algún componente) y siempre que haya cambio de algoritmo el hash del commit y la fecha del mismo.
      + [X] Ir a una sesión fresca (tmux **deployment**), ir a **020_production** y activar el **mlkctxt** de producción (actualmente, el **beta_api_latest** y el **beta_api_stable**). Para testeo local, **default**.
      + [X] Si se va a subir las imágenes a GitLab (despliegue no Hot Swap), tener a mano un **GitLab full API token** y hacer login con **003**.
      + [X] Reconstruir las imágenes de producción con **005** o alguna en especial con las instrucciones de dentro de sus directorios (no se recomienda).
      + [X] Probar si eso localmente con **910-test**.
      + [X] Ir a **SWARMS** y desplegar.
  - # SWARMS
    - Esto está en el **README.md** de **030_swarms**.
    - Seguir los siguientes pasos:
      + [ ] Activar el contexto remoto correspondiente (actualmente, **beta_api_latest** y **beta_api_stable**).
      + [ ] Ejecutar el **rsync** y entrar en el remoto con **ssh**.
      + [ ] Lanzar o entrar en el **tmuxinator** correspondiente.
    - Ahora, **ATENCIÓN**. Ir a **CAUTION-DATA_LOSS**.
      - Para un **soft update**, conservando los datos:
        + [ ] **900**
        + [ ] **905**
        + [ ] **907**
        + [ ] **920**
        + [ ] **940**
      - Para un **hard update**, borrando los datos:
        - To be done
    - Salir de **CAUTION-DATA_LOSS**.
      - Seguir:
        + [ ] Log in y pull de imágenes con **005**. Se necesita un **Read registry token** de GitLab.
        + [ ] Desplegar con **010**.
        + [ ] Probar que la nueva versión ha sido desplegada con el **test API cURL 010-ServiceRouter/020-apiinfo.sh**.
    - Por último, desplegar el **frontend** en [[SunnSaaS/Frontend]].
- # Imagen Docker [[registry.gitlab.com/sunnsaas/sunnsaas_v1/sunnsaas-worker-dev]]
  collapsed:: true
  - Esta es la imagen se usa para todo lo que tiene que ver con Fortran. Se usa en el componente [[worker]] y para compilar los binarios [[Fortran]]. Su definición está en **docker/010_fortran_worker_dev_image**.
  - Existe una versión **DEPRECATED** que se guarda por si acaso.
  -