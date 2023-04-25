title:: Gestión/IT

- External Hard Disks
  collapsed:: true
  - TOSHIBA_500GB: important information backup like GPG keys, .aws, and .mlkctxt/system, at the drawer.
  - WD3000, 2.7TB, /mnt/external_wd3000_hdd_2_7tb: My Book 1140, EXT4, empty.
  - ALICE, 2.8TB, /mnt/external_alice_hdd_2_8tb: Ext HDD 1021, EXT4, empty.
  - BARRACUDA01, 4TB: Backup of euler.
  - There are three small SSD (120GB, 120GB, and 256GB) and 1TB HDD, not in use.
- **[[euler]]**
  collapsed:: true
  - Currently the Linux box to work at home. Storage:
    collapsed:: true
    - **/dev/sde3:** montado en /, 1T, SSD, WDC WDS100T2B0B, utilizado para System, Docker registry, git, home, apps
    - **/dev/sda1:** montado en /mnt/samsung_hdd_1_5tb, 1.5T, 900G, HDD, HD154UI, usado para phd_legacy_data, phd_process
    - **/dev/sdb1:** montado en /mnt/wd3000red_hdd_3tb, 2.7T, 500G, HDD, WD30EFRX-68E, Dropbox, datascience repos
    - **/dev/sdc1:** montado en /mnt/barracuda_hdd_4tb, 3.6T, 2.3T, HDD, ST4000DM004-2CV1, euler backups, git final backups
    - **/dev/sdd1:** montado en /mnt/sandisk_sdd_1tb, 900G, 100G, SDD, SDSSDA-1, phd_process
  - Key folders to back up, check back up scripts:
    collapsed:: true
    - /mnt/wd3000red_hdd_3tb/Dropbox, 1.7T
    - /mnt/wd3000red_hdd_3tb/git_data_science_lfs, 430G
    - /mnt/sandisk_sdd_1tb/phd_process, 750G
    - /mnt/samsung_hdd_1_5tb/phd_legacy_data, 56G
    - /mnt/samsung_hdd_1_5tb/phd_process, 877G/
    - home/malkab/.aws
    - /home/malkab/Desktop
    - /home/malkab/.docker
    - /home/makab/Downloads
    - /home/git, 640G
    - /home/.gnupg
    - /home/.mlkctxt
    - /mnt/barracuda_hdd_4tb/git_backup
- **[[erebus]]**
  collapsed:: true
  - No important stuff should go here.
- **[[kepler]]**
  collapsed:: true
  - Server to work and to serve content from home. Storage:
    - **/dev/sdb3:** montado en /, 3.2G, HDD, WDC WD20EZRZ-00Z, System, no critical stuff.
    - **/dev/sda1:** montado en /mnt/wdc_wd30purx_64p_2_75tb, 2.75T, HDD, WDC WD30PURX-64P