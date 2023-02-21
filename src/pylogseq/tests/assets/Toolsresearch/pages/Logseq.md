filters:: {}

- Formato y sintaxis
  collapsed:: true
  - Entre `acentos inversos`
  - Entre **dobles asteriscos**
  - Bloques de código con triples acentos inversos
    collapsed:: true
    - ```shell
      ls -lh
      ```
- Atajos de teclado
  collapsed:: true
  - **Atrás / adelante:** CTRL + [ / ]
  - **Cerrar paneles:** T L / T R
  - **Grafo general:** G G
  - **Ir a Journal:** G J
- Instalación y prueba de nuevas versiones
  collapsed:: true
  - Tenemos un script en [[mlktools-scripts]] llamado [[mlklogsequpdate]] que permite probar sin problemas nuevas versiones (a menudo fallan) de [[Logseq]] haciendo automáticamente backup y cambiar entre unas y otras fácilmente.
- #Web/Herramientas Documentación Logseq [Logseq Community Hub](https://hub.logseq.com/)
- Plugins
  - **Get webpage title:** coger de un enlace HTML el título y configurar automáticamente los metadatos del enlace.
  - **Tidy Blocks:** limpia espacios y saltos de carro.
    - Cambiar los shortcuts a **alt+q** (limpiar espacios), **alt+r** (limpiar espacios y saltos de línea) y **alt+s** (no tenemos claro para qué sirve)
  - **Link Preview:** se pone el ratón encima de un link y se muestra un pequeño extracto de la página.
- Tema: **Dev Theme** es por ahora nuestro preferido, el más claro y eficiente con diferencia.
- Configuraciones
  collapsed:: true
  - Para **cambiar el primer día de la semana** en el **Date picker**, existe una configuración en **config.edn** **:start-of-week 6** que hay que pasar a 0.
  - **Problemas con las incompatibilidades entre los shortcuts de plugins y generales**
    collapsed:: true
    - Entrar en las configuraciones de los plugins y poner en el JSON los shortcuts a **null**.
- Tags importantes
  collapsed:: true
  - **Referencia:** hace referencia a trabajos o métodos que han sido de importancia en proyectos y que merece la pena señalar, recordar y referenciar
- Gestión de los repositorios y proyectos en [[Logseq]]
  collapsed:: true
  - Para cada repositorio **[[Git]]**, se creará un bloque con la template **Documentación repo Git**
  - Dentro de ellos, cada **work package** se documentará con la template **WP: Documentación**. Dentro de ellos, las templates **WP: Linaje de datos** y **WP: Flujo de trabajo** ayudan a documentar procesos y datos de una forma más o menos estándar.
  -