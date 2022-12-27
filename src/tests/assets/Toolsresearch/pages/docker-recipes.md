- #procesar

# Docker Recipes

Some Docker recipes:

```Shell
# Info and testing
docker --version
docker info
status docker
docker run hello-world

# Get ID from containers based on a certain image
docker container ls -aq --filter ancestor=gns3/xeyes

# Delete containers based on a filter
docker container rm $(docker ps -aq --filter ancestor=gns3/xeyes)

# Delete images based on reference (note the / that denotes image filiation)
docker image rm -f $(docker images -q --filter reference=*/sunntics/*)

# Saves legacy images to tar files for later restoration
docker save -o thefile.tar imagename

# Remove stopped containers
docker container rm $(docker container ls –aq)

# Delete dangling images
docker image rm $(docker image ls -qf dangling=true)

# Delete images with a certain name (up to the last /)
docker image rm $(docker images -qf "registry.gitlab.com/sunnsaas/sunnsaas/*:*")

# Extract an image to a file and load it again:
docker save -o imagefile image1 image2 imagen
docker load -i imagefile

# (Re)tag an image
docker tag 2dd8 registry.gitlab.com/cell-platform/cell-cellworker/gridderworker:v0.4

# Docker Swarm Stacks & Services
Docker swarm stacks are the proper way of launching applications until we get a grasp on Kubernetes:

# Convert machine into a Docker Swarm controller
docker swarm init
```
## Labels

Add labels to all images for ease management.


## Deploy a Docker-Compose as a stack
# With login into a private registry
docker login registry.gitlab.com \
-u $GITLAB_USERNAME \
-p $GITLAB_REGISTRY_TOKEN

docker stack deploy -c cellgriddercontroller-full-swarm.yaml \
cell_cellgriddercontroller --with-registry-auth
- # Without any private registry
  docker stack deploy -c docker-compose.yml stackname


  List existing stacks
  docker stack ls


  # Removes a stack
  docker stack rm malkab
# Check services in a stack
docker stack services stackname
# Check all services
docker service ls
# Check service log
docker service logs 8133
# Update an env variable in a service
docker service update --env-add AUTHORIZEDKEYS=whatever servicename


# Inspect a service
docker service inspect servicename | less
# Check status
docker service ps zork
## Get Run Stats

Easy:

```Shell
docker stats
```
# Secrets
Secrets are used to store sensitive information in a SWARM.

```
# List secrets
docker secrets ls
```
## Fully Parametrized Build System with ENV Variables

Check the **docker/docker-postgis** repo, section **endangered_equidna**, for a full example.
#  Delete all containers and attached volumes
docker rm -fv $(docker ps -aq)
# Delete dangling or orphaned volumes
docker volume rm $(docker volume ls -qf dangling=true)
#  Extract a file from a container when no other means are available (use volumes!)
docker cp 83ec:/usr/local/tomcat/webapps/geonetwork/WEB-INF/data_geonetwork.tar.bz2 .
## Running Bash Commands with Entrypoint with Docker Run

As silly as it can get:

```Shell
docker run -ti --rm \
  --entrypoint /bin/bash \
  $IMAGE_NAME \
  -c 'echo $AN_ENV_VAR'

docker run -ti --rm \
  --entrypoint /bin/bash \
  $IMAGE_NAME \
  -c "echo $AN_ENV_VAR"
```

The first one expands the env var, the second one not. That silly it gets. The quotes.
## Docker SWARM Stacks

Managing SWARM stacks:

```Shell
# List
docker stack ls

# Remove
docker stack rm cell003dev
```





Docker for Mac
---
__TAGS:__ docker, for, mac, macos

To see a service on the host, use the following built-in domain: __docker.for.mac.host.internal__. For example, a dockerized PostgreSQL creates a FDW to another dockerized PostgreSQL exposing its port to the host:

```
`SQL
```
create server if not exists cellds_main
foreign data wrapper postgres_fdw
options (host 'docker.for.mac.host.internal', dbname 'cellds', port '7000');
```
`
```
