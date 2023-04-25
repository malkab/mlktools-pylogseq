- # Instalación
  - Ir a la página oficial [Node.js](https://nodejs.org/) y descargar el **tar.xz**
  - Untar
    - ```shell
      tar -xf node-vXX.XX.XX-linux-x64.tar.xz
      ```
  - Se descomprimirá una estructura típica de directorios **bin / include / lib / share**. Copiarla a **/usr/local**.
    - ```shell
      sudo cp -R * /usr/local/
      ```
  - Probar
    collapsed:: true
    - ```shell
      node -v
      ```