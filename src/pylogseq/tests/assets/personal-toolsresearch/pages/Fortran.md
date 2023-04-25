- Notas para un entorno de desarrollo [[Fortran]] saludable.
- # FORD
  collapsed:: true
  - **FORD** is a documentator for Fortran. It is a Python program, check the **docker-fortran-image** repo for installing instructions. A **Markdown** file in the source root is needed to configurate the system. To produce doc:
  - ```shell
    ford config-file.md
    ```
- # Fortran con paralelización con OpenMPI
  collapsed:: true
  - #procesar Esta sección es poco clara y no sabemos muy bien cómo sacarle partido.
  - This procedure is automatized and in place at the **Sunntics-Backend / docker-fortran-image** repo.
  - A non-parallell install is very easy:
    - ```bash
      apt-get install \
        gfortran \
        openmpi-bin \
        less \
        cmake \
        libopenmpi-dev ; \
      pip install ford
      ```
  - FORD is the Fortran Documentator.
  - Then build and install the CoArrays library for parallell Fortran:
    - ```bash
      cd /OpenCoarrays-2.7.1
      - mkdir build
      - cd build
      - FC=gfortran CC=gcc cmake ..
      - make
      - make install
      ```
- # FortLS
  collapsed:: true
  - #fortls ayuda al desarrollo permitiendo que [[Visual Studio Code]] pueda hacer inspección de código como con otros lenguajes. Su página es [esta](https://fortls.fortran-lang.org/index.html).
  - Es una utilidad [[Python]].
  - Para utilizarla en un [[devcontainer]] sencillamente instalarla con Python en el **post-install**: **sudo python -m pip install --upgrade fortls**. Meterá en el sistema un ejecutable llamado **fortls**.
  - Esta aplicación es utilizada por la extensión [[Visual Studio Code]] **Modern Fortan** (id: fortran-lang.linter-gfortran), así que incluirla en la imagen:
    collapsed:: true
    - ```JSON
      "customizations": {
        "vscode": {
          "extensions": [
            "ms-python.python",
            "GitHub.copilot",
            "njpwerner.autodocstring",
            "redhat.vscode-yaml",
            "fortran-lang.linter-gfortran"
          ]
        }
      },
      ```
- # Entorno de desarrollo con [[Visual Studio Code]]
  - Ejemplos de estos entornos se pueden encontrar en [[G/sunntics-core-restricted/fortran_python_dev]]/030-forpy_wrapper.
  - ## Devcontainer
    - En las **customizations/vscode/extensions**, añadir:
      - ```JSON
        "extensions": [
          "ms-python.python",
          "GitHub.copilot",
          "njpwerner.autodocstring",
          "redhat.vscode-yaml",
          "fortran-lang.linter-gfortran",
          "ms-vscode.cpptools",
          "ms-vscode.makefile-tools"
        ]
        ```
    - En el **post_install.sh**:
      - ```shell
        # APT installs
        sudo apt-get update
        
        sudo apt-get install -y \
            gdb \
            inotify-tools \
            cmake \
            git
        
        sudo apt-get -y upgrade
        
        sudo ldconfig
        
        sudo rm -rf /var/lib/apt/lists/*
        
        # Update pip
        python -m pip install --upgrade pip
        
        # PIP installs
        sudo python -m pip install --upgrade fortls
        ```
      - Instala el debuggeador **gdb** y el **fortls**, que es de gran ayuda dentro de [[Visual Studio Code]].
  - ## Lanzamiento, compilación y depuración
    collapsed:: true
    - Primero, crear una **task** para la compilación con **gfortran**, que llama a un target de un **makefile** como el mostrado en esta página:
      collapsed:: true
      - ```JSON
        {
          // See https://go.microsoft.com/fwlink/?LinkId=733558
          // for the documentation about the tasks.json format
          "version": "2.0.0",
          "tasks": [
            {
              "label": "build",
              "type": "shell",
              "command": "make",
              "args": [ "debug" ],
              "options": {
                "cwd": "${workspaceFolder}/010-fortran_sample_module"
              },
              "group": {
                "kind": "build",
                "isDefault": true
              },
              "presentation": {
                "reveal": "silent"
              },
              "problemMatcher": []
            }
          ]
        }
        ```
    - Crear a continuación un **lanzador de depuración** que utilice esta task:
      collapsed:: true
      - ```JSON
        {
          "version": "0.2.0",
          "configurations": [
            {
              "name": "(gdb) Fortran",
              "type": "cppdbg",
              "request": "launch",
              "program": "${workspaceFolder}/010-fortran_sample_module/program",
              "args": [], // Possible input args for "program"
              "stopAtEntry": false,
              "cwd": "${workspaceFolder}/010-fortran_sample_module/",
              "environment": [],
              "externalConsole": false,
              "MIMode": "gdb",
              "preLaunchTask": "build",
              "setupCommands": [
                {
                  "description": "Enable pretty-printing for gdb",
                  "text": "-enable-pretty-printing",
                  "ignoreFailures": true
                }
              ]
            }
          ]
        }
        ```
      - Hay que tener en cuenta que se espera que la task genere un ejecutable llamado **program**, en este caso.
- # Makefile para Fortran
  collapsed:: true
  - Un ejemplo bastante versátil, ya que compila los fuentes implícitamente por su nombre:
    - ```Makefile
      .SUFFIXES:
      
      # ------------------
      #
      # Config
      #
      # ------------------
      
      # Compiler
      FC=gfortran
      
      # Compilation options
      #    Optimization (for level 3) flags
      #    Compiler warnings
      #    Strictest adherence to the latest standards
      FCFLAGS=-O3 -Wall -Wextra -std=f2008
      FCFLAGSDEBUG=-g -std=f2008 -w
      
      # Executable name
      EXECUTABLE=program
      
      # Shortcut to compilator
      COMPILE.F08=$(FC) $(FCFLAGS)
      COMPILE.F08.DEBUG=$(FC) $(FCFLAGSDEBUG)
      
      # Dependencies for all and debug targets
      ALLDEPS=program.F90 forpy_mod.o pyfortestwrapper_mod.o
      
      
      # ------------------
      #
      # Targets
      #
      # ------------------
      
      # Make executable
      all: $(ALLDEPS)
      	$(COMPILE.F08) $(ALLDEPS) `python3-config --ldflags --embed` -o $(EXECUTABLE)
      
      # For debugging in VSC. Only the main program .F90 will be
      # compiled with debug symbols. Check below to debug modules.
      debug: $(ALLDEPS)
      	$(COMPILE.F08.DEBUG) $(ALLDEPS) `python3-config --ldflags --embed` -o $(EXECUTABLE)
      
      # Clean
      .PHONY: clean
      clean:
      	-rm -f *.o *.mod $(EXECUTABLE)
      
      # Compilation of object files.
      # Add -g here to compile with debug symbols.
      %.o: %.F90
      	$(COMPILE.F08.DEBUG) -c $<
      	@touch $@
      ```
- # Submódulos
  collapsed:: true
  - Esto es un ejemplo de módulo:
    collapsed:: true
    - ```Fortran
      ! Example of a module with a private and public subroutines and functions
      ! Use only functions because they are encapsulated
      
      module formodtest_mod
      
          implicit none
      
          private :: p_b
          public :: sum, prod, another
      
      contains
      
          subroutine prod(a, b, c)
      
              integer, intent(in) :: a, b
              integer, intent(out) :: c
      
              c = a * b
      
          end subroutine prod
      
          ! This is private
          subroutine p_b(a, b, c)
      
              integer, intent(in) :: a, b
              integer, intent(out) :: c
      
              c = a - b
      
          end subroutine p_b
      
          ! Functions are the preferred way to build modules.
          function another(a, b) result(c)
      
              integer, intent(in) :: a
              integer, intent(in) :: b
              integer :: i
              integer :: c
      
              call p_b(a, b, i)
      
              c = i + 10
      
          end function another
      
      end module formodtest_mod
      ```
  - Y esto de programa usando una función concreta del módulo:
    - ```Fortran
      program p
      
          use formodtest_mod, only: another
          implicit none
      
          ! another function, preferred way to build modulese
          Print*, "another, the function", another(1, 6)
      
      end program p
      ```
  - El módulo debe compilarse por separado. Generará un fichero **.mod** con su interface y otro **.o** para el linker.
- # [[Forpy]]: Fortran y [[Python]]
  collapsed:: true
  - [[Forpy]] es un módulo [[Fortran]] que permite embeber [[Python]] dentro de programas Fortran.
  - #Referencia Tenemos un gran ejemplo de uso de [[Forpy]] en [[G/sunntics-core-restricted/fortran_python_dev]], ver [[L/010-work/sunntics]].
  - Para utilizar, compilarla primero y linkarla con el programa Fortran que lo usa, pero con unas opciones de compilación especiales
    collapsed:: true
    - ```shell
      # Python 3.8 and higher
      gfortran -c forpy_mod.F90
      gfortran program.F90 forpy_mod.o `python3-config --ldflags --embed`
      ```
  - Para depurar, llamar a la función **err_print** tras una instrucción problemática ahorra un montón de disgustos
    - ```Fortran
      ! La instrucción problemática
      pyfortestwrapper_error = arr%getitem(c, 2)
      
      ! Si Dios quiere esto ayudará a entender qué puede estar pasando
      call err_print
      ```
- # Watch: vigilar los ficheros fuente para recompilar y ejecutar en consola a medida que se hacen cambios
  collapsed:: true
  - Utilizar el siguiente script:
    - ```shell
      #!/bin/bash
      
      while inotifywait -e modify *.F90 ; do
      
          clear
          make all
          ./program
      
      done
      ```