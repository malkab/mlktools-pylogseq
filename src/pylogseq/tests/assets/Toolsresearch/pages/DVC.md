- DVC es un sistema accesorio a [[Git]] para gestionar ficheros grandes.
- La ubicación de su almacén de datos es actualmente **[[Dropbox]]/dvc_storage**. Hemos debatido sobre si llegarlo a [[Amazon/AWS/S3)]], pero mejor no porque gran parte de los datos que generamos en un momento dado serán prescindibles y corremos el riesgo de estar pagando por nada.
- Para buscar ficheros que ser pasen de tamaño, usar **mlkgitlfssearch**
- Para inicializar en un repositorio Git
  - ```shell
    dvc init
    dvc remote add -d storage /mnt/samsung_hdd_1_5tb/dvc_storage/project_name_if_applicable
    dvc config cache.local storage
    ```
- Para añadir ficheros
  collapsed:: true
  - ```Shell
    dvc add path/to/file
    dvc commit
    dvc push
    ```
- Otras operaciones
  collapsed:: true
  - ```shell
    dvc status
    dvc add data
    dvc move old_file_name new_file_name
    dvc commit
    dvc push
    dvc pull
    ```