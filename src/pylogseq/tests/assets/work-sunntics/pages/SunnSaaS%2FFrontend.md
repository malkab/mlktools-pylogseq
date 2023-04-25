- Frontend Angular
  collapsed:: true
  - Ubicación del código de las distintas pantallas según su URL
    - Todas parten de la ruta común **app/views/contenido/operations/resources/custom-resource/**
    - **Hel_Eff_param** (visualización del campo de heliostatos): heliostat-hourly-power
    - **Aiming_FlatPlane** (visualización de los puntos de apuntado): solar-flux-on-receiver
  - Vista de apuntado de heliostatos **Aiming_FlatPlane**
    - Usa el componente de visualización **d3-scatter-plot** (selector Angular app-d3-scatter-plot)
  - D3
    - **d3-scatter-plot** (selector Angular app-d3-scatter-plot)
      - Se encarga de la visualización de los aiming points en **Aiming_FlatPlane (solar-flux-on-receiver)**
      - El componente por si mismo no controla su tamaño, sino que es su inmediato padre, usualmente el elemento **app-d3-scatter-plot**, el que controla el tamaño interno. Usar el max-height y max-width.
- # Custom Resource
  collapsed:: true
  - Una pantalla personalizada para un **Dataset** no estándar.
  - Los **Custom Resources** se renderizan en el contexto del componente padre **app/shared/resource-wrapper**.
  - El **resource-wrapper** usa un servicio llamado **ResourceService** en **app/services/resource.service.ts** donde se definen las llamadas API que utilizan los Resources, incluidos los custom puesto que este servicio se hereda.
- # Descarga personalizada de CSV y JSON
  collapsed:: true
  - En el componente **app/shared/resource-wrapper** se carga unas funciones llamadas **getJSON()** y **getCSV()** para personalizar la descarga de JSON y CSV.  Esto viene de un servicio de tipo **ResourceService** que se inyectan en el constructor.
  - Para la descarga de ficheros en el frontend, hay un servicio en **app/utils/file-utils.service.ts** llamado **FileUtilsService** que tiene un método llamado **downloadFile** que permite la descarga de un fichero que se le pasa una URL de una entrada API. Inyectar el servicio en el constructor.
- # Despliegue
  collapsed:: true
  - ## 020-production-image
    - Creación de la imagen Docker de producción. Esto está en el **README.md** de **020-production-image**.
    - Seguir los siguientes pasos:
      + [ ] Buscar en el código marcas de debuggeo como **console.log("D:** y **HTML <p>D:**.
      + [ ] Activar el **mlkctxt default**.
      + [ ] Lanzar el **entorno de desarrollo** con **010-dev** y hacer **npm outdated**, **npm upgrade** y **npm run build** para ver que compila.
      + [ ] Editar la **versión** en **package.json**.
      + [ ] Editar la **image_tag** en el **mlkctxt**.
      + [ ] Asegurarse que el APP_BUILD está en **true** en **010**.
      + [ ] Ir a **020-production-image** y activar el **mlkctxt production_image**.
      + [ ] Coger un token de GitLab **Full API** y hacer login con **003**.
      + [ ] Ejecutar **005** o seguir el procedimiento detallado.
    - Procedimiento detallado alternativo:
      + [ ] Ejecutar **010**.
      + [ ] Testear con **020**.
      + [ ] Coger un token API y ejecutar **040**.
  - ## 030-swarms
    - Seguir los siguientes pasos:
      + [ ] Activar el contexto **mlkctxt** adecuado (actualmente, **beta** y **stable**).
      + [ ] Hacer **rsync** y **ssh**.
      + [ ] Ir al directorio de la aplicación y ejecutar **005**. Se necesita tener a mano un **token Read Registry** de GitLab.
      + [ ] **¡MUY IMPORTANTE!** Borrar cachés antes de probar el despliegue, puesto que los paquetes generados por el builder se quedan en la caché y son incompatibles.
