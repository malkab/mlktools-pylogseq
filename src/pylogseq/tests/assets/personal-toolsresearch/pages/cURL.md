- Excelente herramienta de línea de comandos para hacer tests de API e interaccionar con ellas, a nivel crudo
- [[cURL]] tiene muchísimas opciones. Su documentación [aquí](https://curl.se/docs/manpage.html)
- Un complemento excelente para trabajar con estos scripts, que van a las API a recabar sobre todo datos en JSON, es usar la excelente herramienta [[jq]], que procesa JSON
  collapsed:: true
  - **formatear salida JSON para fácil lectura**
    collapsed:: true
    - ```shell
      ./010-login.sh | jq .
      ```
  - **extracción de un elemento de la estructura JSON**
    - ```shell
      ./010-login.sh | jq .success.accessToken
      ```
    - **.** es el raíz de la estructura JSON
- # Ejemplos
  - ## GET
    - **GET sencillo** con comprobación de contexto
      collapsed:: true
      - ```shell
        #!/bin/bash
        
        # ----------------
        #
        # Ping
        #
        # ----------------
        curl -k -s $(mlkp api_entry)/services/ping
        ```
      - **-k** hace la petición de forma insegura, sin estar tratando con certificados y demás. **-s** lo hace en silencio, sin eco, ya que [[cURL]] muestra mucha información de depuración y progreso de la petición.
    - **GET con argumentos** con info de contexto
      collapsed:: true
      - ```shell
        #!/bin/bash
        
        # ----------------
        #
        # Login
        #
        # ----------------
        
        # Get some ENVVARS
        API_USER=$(mlkp api.init_email)
        API_PASS=$(mlkp api.init_password)
        API_ENTRY=$(mlkp api_entry)
        
        curl -k -s \
          -d "user=${API_USER}&pass=${API_PASS}" \
          $API_ENTRY/auth/login
        ```
      - Aquí, **-d** sirve para designar la carga de datos de parámetros que el **GET** necesita
    - **GET** con autenticación por Bearer Token
      collapsed:: true
      - ```shell
        TOKEN=$(curl -s -k \
          -d "user=${API_USER}&pass=${API_PASS}" \
          ${API_ENTRY}/auth/login | jq -r ".success.accessToken")
        
        curl -k -s \
          -H "Authorization: Bearer ${TOKEN}" \
          $API_ENTRY/auth/logout
        ```
    - Guardado de la salida en un fichero
      collapsed:: true
      - ```shell
        curl -k -H "Authorization: Bearer ${TOKEN}" \
          $API_ENTRY/analysis/export/$1 --output $1.json
        ```
  - ## POST
    - Es una mala práctica en los POST mezclar la subida de un payload [[JSON]] con argumentos de URL. O una cosa o la otra, pero no mezcla.
    - **POST** con un payload JSON y un argumento URL (antipattern)
      collapsed:: true
      - ```shell
        TOKEN=$(curl -s -k -X POST \
          -d "user=${API_USER}&pass=${API_PASS}" \
          ${API_ENTRY}/auth/login | jq -r ".success.accessToken")
        
        curl -k -X POST \
          -H "Authorization: Bearer ${TOKEN}" \
          -H "Content-Type: application/json" \
          -d @${1} \
          $API_ENTRY/project?forceId=${2} | jq .
        ```
    - **POST** para la subida de un JSON monstruoso (probado con 700MB)
      - ```shell
        # $1 contiene el nombre del fichero a subir
        TOKEN=$(curl -s -k -X POST \
          -d "user=${API_USER}&pass=${API_PASS}" \
          $MLKC_API_ENTRY/auth/login | jq -r ".success.accessToken")
        
        curl -k -X POST -H "Authorization: Bearer ${TOKEN}" \
          -F "data=@${1}" \
          $API_ENTRY/analysis/import/$2 \
          --output import_report.json
        
        echo Analysis ID: $(cat import_report.json | jq -r ".success.analysisId")
        echo Project ID: $(cat import_report.json | jq -r ".success.projectId")
        ```