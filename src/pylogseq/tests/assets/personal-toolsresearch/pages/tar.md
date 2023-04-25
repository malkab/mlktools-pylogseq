- Ejemplos de ejecución:
  - ```shell
    # TAR
    tar -cvf archive.tar folder
    tar -xvf archive.tar -C folder_to_deploy --strip 1
    tar -tvf archive.tar
    
    # BZ2
    tar -jcvf archive.tar.bz2 folder
    tar -jxvf archive.tar.bz2 -C folder_to_deploy --strip 1
    tar -jtvf archive.tar.bz2
    
    # GZ
    tar -zcvf archive.tar.gz folder
    tar -zxvf archive.tar.gz -C folder_to_deploy --strip 1
    tar -ztvf archive.tar.gz
    
    # XZ
    tar -xf archive.tar.xz
    
    # TBZ
    tar -xvjf archive.tar.tbz
    
    # TGZ
    tar -xvzf /path/to/yourfile.tgz
    ```