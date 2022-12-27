- **Run a Remote Command with SSH**
  title:: SSH
	- Just:
	  ```Shell
	  ssh user@host "echo \$HOME"
	  
	  ssh user@host "echo $HOME"
	  ```
	- The **\\** in the first command escapes the **$** on the remote, thus the remote $HOME variable will be echoed. In contrast, in the second one, it is the local $HOME the one to be echoed.
- df #procesar
  collapsed:: true
	- #procesar
	  ```shell
	  # SSH
	  
	  SSH and SFTP configuration and recipes.
	  
	  
	  ## Configure SSH
	  
	  To install from repos:
	  
	  ```Shell
	  apt-get install openssh-server openssh-client
	  ```
	  
	  After setting up a static IP network, configure the SSH at the
	  **/etc/ssh/sshd_config/** file. First, configure it to allow login with
	  user / password:
	  
	  ```Shell
	  UseLogin yes
	  AllowUsers malkab
	  Port 22
	  ```
	  
	  Copy the pub key from the workstation into the Linux machine and add it
	  to the **~/.ssh/authorized_keys** file:
	  
	  ```Shell
	  cat id_rsa.pub >> .ssh/authorized_keys
	  ```
	  
	  **authorized_keys** and the **.ssh** folder must be owned by the user and have read only access.
	  
	  Then modify SSH configuration to allow only for login with keys:
	  
	  ```Shell
	  UseLogin no
	  AllowUsers malkab
	  Port 22
	  PermitRootLogin no
	  PubkeyAuthentication yes
	  PasswordAuthentication no
	  ```
	  
	  Restart the service:
	  
	  ```Shell
	  service ssh restart
	  ```
	  
	  
	  ## Generating SSH Keys for Machine Identification
	  
	  Just:
	  
	  ```Shell
	  ssh-keygen -t rsa -C "jp.perez.alcantara@gmail.com"
	  ```
	  
	  Leave a blank password. Will generate an **id_rsa** (secret, don't share) and an **id_rsa.pub** (shareable).
	  
	  
	  ## Authorizing Access into a Server from a System
	  
	  It's just a matter of copying the dev machine public SSH key into the
	  **.ssh/authorized_keys** file. Also the **ssh-copy-id** comes very
	  handy:
	  
	  ```Shell
	  ssh-copy-id your_username@192.0.2.0
	  ```
	  
	  
	  ## Configuring SSH & SFTP
	  
	  The SSH config file is found at __/etc/ssh/sshd_config__. Things to configure:
	  
	  ```Shell
	  UseLogin yes
	  AllowUsers jesus visor_vivienda
	  Port 443
	  Subsystem sftp internal-sftp
	  ```
	  
	  The first sentence allows for login, the second states the users allowed to log in, the third, the port SSH will be listening to, and finally, the fourth tells SSH to use its internal SFTP server for SFTP access.
	  
	  To configure a user to use SSH, simply create it this way:
	  
	  ```Shell
	  adduser --home /whatever/home --ingroup whatevergroup --shell /bin/bash username
	  ```
	  
	  Check user creation section for details on available shells.
	  
	  It is also possible to configure a user to log in only to the SFTP service. First, make sure that the SFTP "shell", __/usr/lib/openssh/sftp-server__, is listed in __/etc/shells__. Second, create the user this way or edit __/etc/passwd__:
	  
	  ```Shell
	  adduser --home /whatever/home --ingroup whatevergroup --shell
	  ```
	  
	  Don't forget to restart SSH service:
	  
	  ```Shell
	  service ssh restart
	  ```
	  
	  Don't forget also to add the user to __AllowUsers__ in __sshd_config__. To try access:
	  
	  ```Shell
	  ssh -p 443 user@host
	  sftp -P 443 user@host
	  ```
	  
	  The first shouldn't work, the second should do.
	  
	  
	  ## Service Management
	  
	  The usual:
	  
	  ```Shell
	  service ssh start
	  service ssh stop
	  service ssh restart
	  ```
	  
	  Also manual start for Dockers:
	  
	  ```Shell
	  /usr/sbin/sshd -D
	  ```
	   ```