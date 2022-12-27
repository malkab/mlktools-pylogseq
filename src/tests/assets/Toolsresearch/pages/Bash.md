- Script para obtener información de **GIT** y registrar metadatos en un fichero de texto
  id:: 633b159d-8282-4ae0-90ac-d01afa927d17
  collapsed:: true
  - Guarda la rama de desarrollo, el hash del commit y el hash de varios ficheros clave, así como el tiempo de proceso
  - ```Bash
    #!/bin/bash
    
    # Writes Git commit hash and binary hashes to versions.json
    
    # Get Git branch name
    GITBRANCH=$(git branch --show-current)
    
    # Get Git commit hash
    GITHASH=$(git log --pretty=format:'%h' -n 1)
    
    # Get binary hashes
    METEOHASH=`md5sum ../fortran/bin/Meteo | awk '{print $1}'`
    STFIELDWHASH=`md5sum ../fortran/bin/STFieldW | awk '{print $1}'`
    
    # Timestamp
    TIMESTAMP=`date +"%Y-%m-%d %H:%M:%S"`
    
    cat <<EOF > bin/versions.json
    {
    	"gitBranch": "${GITBRANCH}",
    	"hashGitCommit": "${GITHASH}",
    	"hashMeteoBinary": "${METEOHASH}",
    	"hashStfieldwBinary": "${STFIELDWHASH}",
    	"time": "${TIMESTAMP}"
    }
    EOF
    ```
- **apt-get install** y borrado de los caches
  id:: 633b159d-8f38-4f89-8c9b-1b6852fde435
  collapsed:: true
  - ```shell
    DEBIAN_FRONTEND=noninteractive
    
    apt-get update
    
    apt-get install -y \
      locales \
      python3 \
      python3-distutils \
      libpython3-all-dev
    
    dpkg-reconfigure --frontend noninteractive tzdata
    
    apt-get -y upgrade
    
    ldconfig
    
    rm -rf /var/lib/apt/lists/*
    ```
- **Iterar variables** de entorno por un prefijo en su nombre
  id:: 633b159e-6a63-4b51-8cb7-e868cfe0a485
  collapsed:: true
  - ```bash
    for V in "${!THE_PREFIX_@}" ; do
    
      echo $V
    
    done
    ```
- Manipulaciones de **cadenas**
  id:: 633b159e-e236-4806-91f8-daf4cfd462a5
  collapsed:: true
  - ```bash
    PATH=a/b/c/d.ext
    
    # Drop file extension
    echo "${PATH%.*}"
    
    # Drop first folder
    echo "${PATH#*/}"
    
    # Get the file name of a path
    echo $(basename /a/path/to/nowhere)
    ```
- Acceder al valor de una **variable de entorno por el nombre** de una variable que apunta a la primera de ellas
  id:: 633b159e-e588-4aa0-bf03-8087ecfccb01
  collapsed:: true
  - ```bash
    X=42
    
    THE_ENV_NAME=X
    
    echo ${!THE_ENV_NAME}
    ```
- Pregunta de seguridad **Yes / No**
  id:: 633b159e-7821-4d09-98cd-643568df2417
  collapsed:: true
  - ```bash
    #!/bin/bash
    
    # Inform about something dangerous
    read -p "WARNING! Data volume is about to be removed. Proceed? (y/N): " -t 10 STR
    if [ "$STR" == "y" ] ; then
    
    	# do the dangerous thing...
    
    else
    
    	echo skipping...
    
    fi
    ```
  -
- #Referencia #Bash Scripts para **rsync** y **ssh**: están en el repo **mlktools-scripts**
  id:: 633b159e-022e-43f0-ac6e-5c8396dd7e00
- #Referencia #Bash **Scripts útiles:** están en el repo **mlktools-scripts**
- Ejemplo **getopts**
  collapsed:: true
  - Ejemplo completo
    collapsed:: true
    - ```shell
      #!/bin/bash
      
      # A getopts example
      
      # Version function
      function version() {
      
        echo v1.0.0
      
      }
      
      # Help function
      
      function help() {
      cat <<EOF
      Example of getopts
      
          ./getopts.sh [options] arg1 arg2
      
      Usage:
          -a    <some text or number>
          -b    <some text or number>
          -c    <some text or number>
      EOF
      
      return 0
      }
      
      POS=0
      
      # Analizes the options provided with the command. a:bc: means: an
      # argument a with a parameter, an argument b without a parameter, the
      # help flag, and finally an argument c with a parameter
      
      while getopts "a:bhc:" opt
      do
      	case "$opt" in
          a)  echo "Found option a: ${OPTARG}."
              POS=$((POS+2))
              ;;
          b)  echo "Found obtion b."
              POS=$((POS+1))
              ;;
          c)  echo "Found option c: ${OPTARG}."
              POS=$((POS+2))
              ;;
          h)  help
              exit 0
              ;;
          v)  version
              exit 0
              ;;
          \?) help
              exit 0
              ;;
      	esac
      done
      
      shift $POS
      
      echo "Argument 1:" $1
      echo "Argument 2:" $2
      ```
  - Otro ejemplo
    collapsed:: true
    - ```shell
      #!/bin/bash
      
      # A getopts example
      
      # Help function
      help(){
      cat <<EOF
      Example of getopts
      
          ./getopts.sh [options] arg1 arg2
      
      Usage:
          -a    <some text or number>
          -b    <some text or number>
          -c    <some text or number>
      EOF
      
      return 0
      }
      
      POS=0
      
      # Analizes the options provided with the command.
      # a:bc: means: an argument a with a parameter, an argument b without a parameter, and finally an argument c with a parameter
      while getopts :a:bc: opt
      do
      	case "$opt" in
      	    a) echo "Found option a: ${OPTARG}."
      	       POS=$((POS+2))
      	       ;;
      	    b) echo "Found obtion b."
      	       POS=$((POS+1))
      	       ;;
      	    c) echo "Found option c: ${OPTARG}."
      	       POS=$((POS+2))
      	       ;;
      	    ?) help
      	    ;;
      	esac
      done
      
      shift $POS
      
      echo "Argument 1:" $1
      echo "Argument 2:" $2
      ```
- Parametros de comando simple sin **getopts**
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    if [ "$1" = "-h" ] ; then
      echo Usage: $0 [ container hash or name ] [ optional user U:G ]
      exit 0
    fi
    
    if [ -z "$1" ] ; then
      echo Specify a container hash or name and an optional user, as in 0:0 \(defaults to 1000:1000\)
      exit 2
    fi
    
    USER=1000:1000
    
    if [ ! -z "$2" ] ; then
      USER=$2
    fi
    
    docker exec -ti \
      -u $USER \
      -w /workspaces/mlktools-geowhale/src \
      -e PYTHONPATH=$PYTHONPATH:/workspaces/libraries_python-postgresql_helpers/src \
      $1 \
      /bin/bash
    ```
- **IF THEN**
  collapsed:: true
  - **Variable** vacía
    collapsed:: true
    - ```shell
      #!/bin/bash
      
      if [ -z "$var" ] ; then
        echo "\$var is empty"
      else
        echo "\$var is NOT empty"
      fi
      
      # Negación
      if [ ! -z "$2" ] ; then
        USER=$2
      fi
      ```
  - Igualdad de **cadenas**
    collapsed:: true
    - ```shell
      if [ "$1" = "-h" ] ; then
        echo Usage: $0 [ container hash or name ] [ optional user U:G ]
        exit 0
      fi
      ```
- **date**, generación de **timestamps**
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    echo $(date +"%Y%m%d-%H%M%S")
    echo $(date +"%Y-%m-%d")
    
    # Timestamp
    TIMESTAMP=`date +"%Y-%m-%d %H:%M:%S"`
    ```
- **Generación de SHA** basado en la fecha
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    # Generates a sha1sum hash based on the current timestamp
    echo docker-$(date '+%Y%m%d-%H%M%S%MS%N' | sha1sum | cut -d' ' -f1)
    ```
- **Gestión de usuarios**
  collapsed:: true
  - **Script para ver el UID de un directorio**
    collapsed:: true
    - ```shell
      #!/bin/bash
      
      # This script returns the UID of the owner of a folder
      
      # Usage:
      # folder_uid.sh folder
      
      PARENT="$(dirname $1)"
      DIR="$(basename $1)"
      
      USER_ID=`ls -lahn ${PARENT} | grep ${DIR} | awk {'print $3'}`
      
      echo ${USER_ID}
      ```
  - **Script para ver el GID de un directorio**
    collapsed:: true
    - ```shell
      #!/bin/bash
      
      # This script returns the GID of the owner of a folder
      
      # Usage:
      # folder_gid.sh folder
      
      PARENT="$(dirname $1)"
      DIR="$(basename $1)"
      
      GROUP_ID=`ls -lahn ${PARENT} | grep ${DIR} | awk {'print $4'}`
      
      echo $GROUP_ID
      ```
  - **Script para crear un usuario con el UID / GID  de un directorio**
    collapsed:: true
    - ```shell
      #!/bin/bash
      
      # This is script examines the ownership from a folder or file and creates a user and group
      # with the same UID and GID as the given folder. It is used in Docker containers to map the
      # user in the host from a volume
      
      # Usage:
      # map_user username password groupname target_folder
      
      USER_ID=$(folder_uid $4)
      GROUP_ID=$(folder_gid $4)
      
      groupadd -g $GROUP_ID $3
      useradd --uid $USER_ID --gid $GROUP_ID $1
      echo "${1}:${2}" | chpasswd -e
      ```
- **Read de consola**
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    # A read example:
    # 	-	-p is the prompt
    # 	-	-t is the timeout
    # 	-	str recieves the input value
    
    read -p "Input string: " -t 10 STR
    
    # Default value
    STR=${STR:-Default answer}
    
    
    # -z $str check if the string is empty
    
    if [ -z $str ]
    then
    	echo
    	echo "You have not entered any string in less than 10 seconds"
    else
    	echo "Your string: ${str}"
    fi
    ```
- **Creación de ficheros README.md**
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    # This is an example of how to write long, formatted text to a file using cat
    
    cat > ./data/10-out-db-dump/README.md <<'endmsg'
    These are dumps of the main processing database. They should substitute at the end the **00-in/caser.backup** initial database and be discarded.
    endmsg
    ```
- **shebang**
  collapsed:: true
  - ```shell
    #!/bin/bash
    ```
- Operaciones con **arrays**
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    # Declare the array
    folders=('Abacus' 'Bergamonte' 'Clemence' 'Dardanelles')
    
    # Print all array
    echo "The whole array: ${folders[@]}"
    echo
    
    # Print an element
    echo "Element 1: ${folders[1]}"
    echo
    
    # Length of the array
    echo "Array length: ${#folders[@]}"
    echo
    
    # Iteration
    echo 'Iteration:'
    for folder in "${folders[@]}"
    do
      echo $folder
    done;
    echo
    
    # Iteration by index
    echo 'Iteration by index:'
    total=${#folders[@]}
    for ((i=0;i<=(($total-1));i++))
    do
    		echo ${folders[i]}
    done;
    echo
    
    # Length of one of the elements in the array
    echo "Length of array element 1: ${#folders[1]}"
    echo
    
    # Extraction by offset and length
    echo "Extraction by offset and length beginning in object 1 for 2 elements: ${folders[@]:1:2}"
    echo
    
    # Search and replace
    echo "Replacing string 'Berga' for 'Clara': ${folders[@]/Berga/Clara}"
    echo
    
    # Add an element
    folders=("${folders[@]}" "Easop")
    echo "Added an element: ${folders[@]}"
    echo
    
    # Unsets an element, it just makes it null
    unset folders[3]
    echo "Reverted element 3 to null: ${folders[3]}"
    echo
    
    # Physically removes an element from the array
    folders=(${folders[@]:0:3} ${folders[@]:4})
    echo "Physically removed the element 3: ${folders[3]}"
    echo
    
    # Copying an array
    newArray=("${folders[@]}")
    echo "Copied the array to another one: ${newArray[@]}"
    echo
    
    # Deleting the entire array
    unset newArray
    echo "Deleted the whole array. Length: ${#newArray[@]}"
    echo
    
    # Break a string into pieces and iterate
    IFS=',' read -r -a array <<< "a,b,c,d,e"
    
    echo "${array[@]}"
    
    for i in "${array[@]}"
    do
        echo $i
    done;
    ```
- Parseo de la **línea de comando**
  collapsed:: true
  - ```shell
    #!/bin/bash -vx
    
    # This script explains the shift technique to parse the command line. To see more command line parsing techniques, refer to the 
    # getopts.sh script example.
    
    # Number of parameters
    echo $#
    # This represents the command itself
    echo $0
    
    # This loop pass through all the parameters. The shift function discards the parameter and moves to the next one.
    # It can be used, for example, shift 2, which discards that number of parameters in a row. This is useful when parsing -o <value>
    # parameters.
    while [ "$1" ]
    do
    	echo $1
    	shift 1
    done
    
    # This launches a command appending all passed command line arguments.
    # It gently skips $0, which is the invoked script name itself.
    # For example, "script_name -ls" will run "ls -ls".
    
    ls $*
    ```
- Chequear si un **usuario existe** o no
  collapsed:: true
  - ```shell
    # This checks if a user exists: 0 if yes, 1 if no
    export user_exists=$(id -u malkab > /dev/null 2>&1; echo $?)
    ```
- Establecer una **variable a la salida de un comando**
  collapsed:: true
  - ```shell
    # This sets a variable to the output of a command
    cd="$(pwd)"
    echo $cd
    ```
- Parsear una **línea delimitada**
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    IN="key1#key2"
    
    IFS='#' read -ra ADDR <<< "$IN"
    for i in "${ADDR[@]}"; do
        echo $i
    done
    
    unset IFS
    ```
- **Loop** de secuencia numérica
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    for i in `seq 1 100`;
    do
        echo $i
    done
    ```
- Descomposición de un **path**
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    VAR=/home/me/folder
    
    DIR="$(dirname $VAR)"
    FILE="$(basename $VAR)"
    
    echo $DIR
    echo $FILE
    ```
- **Leer** desde la línea de comando
  collapsed:: true
  - ```shell
    #!/bin/bash -vx
    
    # A read example
    # -p is the prompt
    # -t is the timeout
    # str recieves the input value
    read -p "Input string: " -t 10 str
    
    # -z $str check if the string is empty
    if [ -z $str ]
    then
    	echo
    	echo "You have not entered any string in less than 10 seconds"
    else
    	echo "Your string: ${str}"
    fi
    ```
- **rsync**
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    PORT=443
    USER=shared
    HOST=viv3.cica.es
    
    # Synch in file mode, verbose, compressed, human-readable, delete extraneous files
    # (without affecting those in the origin), with ssh on a given port
    rsync -avzh --delete --progress \
      --rsh="ssh -p ${PORT}" \
      $USER@$HOST:~/Data-ETL_Workflow/* .
    ```
- timestamp
  collapsed:: true
  - ```shell
    #!/bin/bash
    
    timestamp() {
      date +"%Y%m%d-%H%M%S"
    }
    
    echo $(timestamp)
    
    # If it where as a command in the path...
    echo "use_timestamp-`timestamp`"
    
    
    # Also...
    T=`date '+%Y%m%d-%H%M%S'`
    
    echo Timestamp: $T
    
    T_no_time=`date '+%Y-%m-%d'`
    
    echo Timestamp: $T_no_time
    
    TIMESTAMP=$(date +"%Y_%m_%d_%H_%M_%S")
    ```
- sed
  collapsed:: true
  - **sed** es un **Stream EDitor**, un editor en línea con el que se pueden hacer muchos trucos
  - ```shell
    sed -i 's/original/new/g' file.txt
    ```
  - **-i** significa **in place**, modificando el fichero directamente. Si no, sed simplemente emite el resultado.
  - El comando significa:
    - **s:** comando substitución
    - **original:** expresión regular a buscar en el fichero
    - **new:** expresión regular de reemplazo
    - **g:** global, reemplaza todas las ocurrencias, no sólo la primera
  - El delimitador puede cambiar, por ejemplo: sed "s|###pwd###|${cd}|g" file
- # Comando grep
  collapsed:: true
  - ```shell
     ls -lh | grep down
     ls -lh | grep -v down
    ```
  - La opción **-v** elimina las filas donde aparece el término de búsqueda *down*.
- # Depurar un script bash
  collapsed:: true
  - Añadir al **shebang** el modificador **-vx**
    - ```shell
        #!/bin/bash -vx
      ```
- # Terminar procesos con kill
  collapsed:: true
  - ```shell
    # Termina el proceso inmediatamente, sin salida limpia
    kill -9 pid
    # Envía al proceso unja señal TERM, para que intente salir limpiamente
    kill -15 pid
    ```
- # Comando ps
  collapsed:: true
  - Para encontrar exclusivamente el PID de un proceso:
    ```shell
    ps aux | grep -v grep | grep /usr/local/apache-tomcat-8.0.18/ | awk '{print $2}'
    ```
- # Comandos pgrep y pkill
  collapsed:: true
  - Están en el paquete **procps**. El primero devuelve todos los PID de los procesos que cumplen el criterio de búsqueda, mientras que el segundo los termina.
- # Contar líneas, palabras, etc. en un fichero
  collapsed:: true
  - ```shell
    # Usar wc, -l cuenta las líneas
    docker ps -a | grep cursoclima | wc  -l
    ```