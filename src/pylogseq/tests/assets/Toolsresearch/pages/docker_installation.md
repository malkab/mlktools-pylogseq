- #procesar

# Docker Installation & Setup

**NOTE:** there is a Linux installation script at
**dev-miscellaneous/development/docker/install-docker.sh** that installs
everything out-of-the-box.

Installation procedure on Ubuntu is well documented at the official
docs. For MacOS and Windows, use Docker for Mac and Docker for Windows.

In Docker for Mac there are certain problems when using private Docker
registries (like GitLab’s) with the **.raw** virtual HD file format on
systems with the APFS file system. Revert to the **.qcow2** older file
format to avoid it.


## Ubuntu Focal Fossa Installation

Just:

```Shell
sudo apt-get install docker.io

# To check if autostart is enabled
sudo systemctl list-unit-files | grep docker

# To enable autostart
sudo systemctl enable --now docker.service

# Add privileges to a non-root user
sudo usermod -aG docker WHATEVERUSER

docker --version
```


## Ubuntu Installation

Refer to the official documentation at
[Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/).

Also, **docker-compose** is installed in Linux separately. Install it
following the official instructions
[here](https://docs.docker.com/compose/install/).

Check with **docker info** where the default registry is installed. It
can be reconfigured as explained below.

Configure the Docker base folder. This folder container image,
containers, and volume definitions, and will eat the HD size, so use a
big partition. By default, the base folder is located at
**/var/lib/docker**, but it can be changed.

In an Ubuntu with systemd, follow this steps:

- create a **daemon.json** file at **/etc/docker/**;

- configure by adding:

```Shell
{
  "graph": "/mnt/docker-data",
  "storage-driver": "overlay2",
  "hosts": ["tcp://127.0.0.1:5000", "unix:///var/run/docker.sock"]
}
```

- add privileges to a non-root user

```Shell
sudo usermod -aG docker WHATEVERUSER
```

- restart service:

```Shell
service docker restart
```

- check everything is in place:

```Shell
docker info
```

- check:

```Shell
docker container run hello-world
```

- the old root folder can be dropped.
