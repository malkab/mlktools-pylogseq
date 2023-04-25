- # Montar una nueva instancia [[SunnSaaS]] en [[AWS]]
  collapsed:: true
  - #procesar, algunas notas desordenadas.
  - Always keep the Docker root at an EBS volume, by default at **/data/docker/**. Mount the big volume there. This way, instance types can be switched and the core system maintained.
  - EBS volumes aren't automatically mounted in the instance, it's something that needs to be done by hand:
    collapsed:: true
    - ```Shell
      # Create mount folder and change ownership
      # Remember, however, that the Docker registry should ideally go to
      # /data/docker, so mount there accordingly. When doing so, don't
      # alter ownership
      mkdir /mnt/whatever
      chown ubuntu:ubuntu /mnt/whatever
      
      # With parted, locate the EBS volume
      parted -l
      
      # Create a GPT partition table
      parted -a optimal /dev/whatever mklabel gpt
      
      # Create a partition
      parted -a optimal /dev/whatever mkpart ext4 0% 100%
      
      # Keep in mind that AWS tend to name the partitions as whateverpX
      # Create the filesystem
      mkfs -t ext4 /dev/whateverpX
      
      # Use blkid to check the UUID
      blkid /dev/whateverpX
      ```
  - Finally, add to **fstab**:
    collapsed:: true
    - ```Shell
      UUID=xxx /mount_point ext4 defaults,nofail 0 2	
      ```
  - Reboot and check ownership again.
- # Notas sobre rendimiento
  collapsed:: true
  - Algunas notas desorganizadas sobre rendimiento, mirar #procesar
    - ```txt
      # Performance Notes
      
      ## 2020-11-19
      
      Nominal system at startup:
      
      - 6 complete Analysis, large
      - 9 ready Analysis
      - 6 workers
      - 800 open connections to DB.
      - 750 MB of DB size.
      - 12GB / 790GB HD.
      - 7GB of DB logs, that's the biggest problem.
      
      
      ## 2020-11-24 - itpbeta disconnection
      
      8 full, long analysis (~9000 heliostats):
      
      - 6 workers
      - 86GB / 790GB HD
      - 54GB of FEE
      - 28GB of PostGIS data store
      - 24GB of PostGIS logs, still the biggest problem
      - working for 4 days with 0 containers down
      - API: 0 errors
      - Controller: some minor errors checking system status when trying to access files opened by other processes
      - Node memory idle: 1.26GB
      - Used memory idle: 47.57GB
      - DB clientes idle: 13
      - Redis connections: 22
      - Redis memory: 4.91MB
      ```