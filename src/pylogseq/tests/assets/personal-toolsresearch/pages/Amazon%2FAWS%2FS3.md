title:: Amazon/AWS/S3

- # Subida y descarga
  - ## Descarga con sincronía
    collapsed:: true
    - ```shell
      #!/bin/bash
      
      # BEWARE! BY USING '--DELETE' MISSING FILES WILL BE DELETED AT S3.
      # THEREFORE, REMOVE COMPLETELY THE FOLDER IF SPACE IS NEEDED SO
      # THE SCRIPT JUST FAILS AND THE FILES ARE KEPT AT S3
      
      aws s3 sync --delete --storage-class STANDARD_IA \
      	s3://mlk-lfs/phd-test_runs/ \
      	./docs/2018-07-distributed_computing_test_runs/test_runs
      ```
  - ## Subida con sincronía
    collapsed:: true
    - Ejemplos de scripts de subida
      collapsed:: true
      - ```shell
        #!/bin/bash
        
        # BEWARE! BY USING '--DELETE' MISSING FILES WILL BE DELETED AT S3. THEREFORE, REMOVE COMPLETELY THE FOLDER
        # IF SPACE IS NEEDED SO THE SCRIPT JUST FAILS AND THE FILES ARE KEPT AT S3
        
        aws s3 sync --delete --storage-class STANDARD_IA \
        ./docs/2018-07-distributed_computing_test_runs/test_runs \
        s3://mlk-lfs/phd-test_runs/
        
        aws s3 sync --delete --storage-class STANDARD_IA \
        ./data/2018-07-cell_source_data_processing/in \
        s3://mlk-lfs/phd-cell_source_data_processing-in/
        
        aws s3 sync --delete --storage-class STANDARD_IA \
        ./data/data_wrangling/hic/in \
        s3://mlk-lfs/phd-data_wrangling_hic_in/
        
        aws s3 sync --delete --storage-class STANDARD_IA \
        ./data/data_processing/hic_processing/in \
        s3://mlk-lfs/phd-data_processing_hic_processing/
        
        aws s3 sync --delete --storage-class STANDARD_IA \
        ./data/data_final/catastro-database/csv \
        s3://mlk-lfs/phd-csv_catastro/
        
        aws s3 sync --delete --storage-class STANDARD_IA \
        ./test \
        s3://mlk-lfs/phd-test/
        ```
    - Script de subida con sincronía
      collapsed:: true
      - ```shell
        #!/bin/bash
        
        # -----------------------------------------------------------------
        #
        # Uploads to a S3 bucket all relevant LFS information of the project.
        # Uploads all the work-packages/wp/data/000-in folders, the
        # docker-persistent-volumes, the rsync configs in the root, and an
        # arbitrary set of folders and files.
        #
        # Keep in mind that at the target bucket local paths will be replicated
        # from the git/project-family whatevertheproject level, so beware of
        # possible project name conflicts, that should exist because the paths
        # are sync with the dev machines, GitLab, and the LFS S3 bucket. The
        # selected bucket should be one only used to store data coming from
        # /home/git projects.
        #
        # -----------------------------------------------------------------
        # Source folder
        SOURCE=./somefolder
        # Target bucket
        TARGET=s3://somebucket/something
        # Storage class
        STORAGE_CLASS=STANDARD_IA
        
        # ---
        
        aws s3 sync --storage-class \
            $STORAGE_CLASS \
            $SOURCE \
            $TARGET
        ```
  - ## Movimientos sin sincronía
    collapsed:: true
    - ```shell
      aws s3 cp --recursive s3://mlk-data-science-lfs .
      ```