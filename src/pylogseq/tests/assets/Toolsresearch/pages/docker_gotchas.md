- #procesar

# A Big Gotcha that Means a lot of Trouble Easily Avoidable

**Docker Compose** uses the name of folders for internal administration,
so having multiple Composes running at the same time in a machine can be
a problem if, say, all container folders are named **dev**. Use very
specific names (for example, **dev-NAME_OF_PROJECT**) for folders
containing Compose deployments.


## PostgreSQL and Shared Memory Segment

In intensive, paralellized queries PostgreSQL can easily throw a "could
not resize shared memory segment "/PostgreSQL.682207201" to 283432
bytes: No space left on device" error. This is because Docker, by
default, assign a very small shared memory to the containers. To raise
it:

```Shell
docker run -it --shm-size=2gb pg_image /bin/bash
```

or if in a Compose:

```yaml
services:
  postgis:
    image: malkab/postgis:feral_fennec
    container_name: phd-data-postgis
    shm_size: '2gb'

    networks:
      - cell

[...]
```
