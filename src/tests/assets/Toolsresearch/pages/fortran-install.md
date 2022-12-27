- #procesar

# Installing a Fortran Dev Environment

This procedure is automatized and in place at the **Sunntics-Backend /
docker-fortran-image** repo.

A non-parallell install is very easy:

```bash
apt-get install \
    gfortran \
    openmpi-bin \
    less \
    cmake \
    libopenmpi-dev ; \
pip install ford
```

FORD is the Fortran Documentator.

Then build and install the CoArrays library for parallell Fortran:

```bash
cd /OpenCoarrays-2.7.1

mkdir build

cd build

FC=gfortran CC=gcc cmake ..

make

make install
```



## Developing with Parallellization

To develop with parallellization features, write the program and use the
**caf** program to compile it:

```bash
caf program.f90 -o program
```

**caf** is just a wrapper for the Fortran compiler that launches it with
the linking options needed to compile with CoArrays support.

Similarly, to run the program with CoArrays support, a similar wrapper
called **cafrun** is used:

```bash
cafrun -np 2 program
```

although this has a problem in Docker with running as sudo that will not
allow the program to run. Instead, check the underlying command being
launched (it will depend on the CoArrays libraries used):

```bash
cafrun --show
```

In the case of the aforementioned Docker image, that uses the MPI
library, it is:

```bash
/usr/bin/mpiexec -n (number of images) program
```

Run this with sudo allowance:

```bash
mpiexec -n 2 --allow-run-as-root program
```

However, the Docker image uses a non-root user for easy of operation. In
MacOS, this user writes to the mounted volumes with the MacOS UID:GID,
so no problem.
