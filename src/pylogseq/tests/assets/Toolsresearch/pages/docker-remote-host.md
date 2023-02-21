- #procesar

# Docker Remote Host Usage Recipes

## Configure the Docker Engine for Remote Use

WARNING! This setup is unsecure, use only at LAN. For Ubuntu / systemd, create file named

  **/etc/systemd/system/docker.service.d/docker.conf**

and configure:

```Shell
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock
```

Now this Docker Engine can be accessed at a system with SSH root access at DOCKER_HOST=tcp://HOSTNAME:2375.



## Using

Running containers at a remote host in the same LAN (BEWARE: SECURITY!!!) is a great advantage when working from a small laptop. The laptop edits code and the remote Docker host runs it. This is great for API programming, data science, etc.

First, SSH root access is needed. That's why this is so dangerous outside a LAN. Configure **/etc/ssh/sshd_config** this way:

```Text
UseLogin no
AllowUsers malkab root
Port 22
PermitRootLogin yes
PubkeyAuthentication yes
PasswordAuthentication no
```

Copy the public key of the laptop to the Linux root SSH **authorized_keys**:

```Shell
sudo cat id_rsa.pub >> /root/.ssh/authorized_keys
```

Use the envvars DOCKER_HOST or DOCKER_CONTEXT to select a context or a host, create a **Docker Context:**

```Shell
docker context create remotehost --docker "host=ssh://root@remotehost"

docker context ls

docker context use remotehost
```

Now all Docker commands will target the remote Docker host.
