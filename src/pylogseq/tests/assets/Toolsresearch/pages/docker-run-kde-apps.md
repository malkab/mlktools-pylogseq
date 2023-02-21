- #procesar

# Running KDE Apps on Mac with Docker

This has been fairly easy to accomplish. There is an image for **KDE
Plasma** development, **kdeneon/plasma**, that can be used as a starting
point for installing KDE compatible software. It is not used in the
traditional way of creating a Dockerfile with a **FROM** clause, but
instead, the base image is run in a non-volatile container, desktop, UI
software like Anaconda is installed, and then the container is exited,
stoped, and fixed in a new image:

```shell
docker commit [the-container-name]

docker tag [image-hash] [the-tag]

docker push [the-tag]
```

This will create a new image with the software installed (and
potentially, with the KDE menus and such configured) that is given a
proper tag and then uploaded to DockerHub.

This has been used to create a KDE desktop environment with the Anaconda
installed and it works.
