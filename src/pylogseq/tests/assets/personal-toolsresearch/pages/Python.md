- Para hacer tests utilizar [[PyTest]].
- Actualización de [[pip]]: **pip install --upgrade pip**.
- # El infierno de los IMPORTS y los PACKAGES y demás, una guía esperamos que definitiva (Python 3)
  collapsed:: true
  - Un **package** Python es un directorio que, aunque no sea obligatorio, tiene un fichero **\_\_init\_\_.py** en el que se hacen inicializaciones del package y/o se hace una selección de lo que se exporta. Un **módulo** no es más que un fichero **.py**, que también es importable.
    collapsed:: true
    - Esta es la estructura del package. **a.py** tiene un miembro llamado A, respectivamente todos los miembros tienen un miembro con su mismo nombre pero en mayúsculas
      - ```txt
        package_folder
        	__init__.py
            subpackage
            	__init__.py
                sub_a.py
                sub_b.py
            a.py
            b.py
            c.py
        ```
    - Para importar desde fuera
      - ```python
        import package_folder
        import package_folder.subpackage as sp
        from package_folder.a import A
        from package_folder.subpackage.sub_a import SUB_A
        ```
    - Pero para importaciones intra modulo, por ejemplo desde **a.py**
      - ```python
        from . import b, c, subpackage
        ```
    - Pero desde **sub_a.py**
      - ```python
        from .sub_b import SUB_B
        from ..a import A
        ```
  - **Búsqueda de packages y módulos**
    collapsed:: true
    - Como norma general, Python busca en el directorio del fichero lanzado con **python whatever.py**. Si el directorio del **package** cuelga del directorio en el que está el fichero de script que se lanza, Python lo encontrará sin problemas. Por ello, en desarrollo, cualquier package que esté en el directorio principal será encontrado. Esto incluye si el **package** está incluido en un árbol de directorios.
    - Si el **package** no cuelga del directorio principal del **script** hay que utilizar la variable **PYTHONPATH**. **PYTHONPATH** permite indicar una serie de directorios donde se buscarán packages en cascada. Se puede definir a nivel de shell:
      ```shell
      export PYTHONPATH="$PYTHONPATH:path/to/folder/a:path/to/folder/b"
      ```
      y en [[Visual Studio Code]] [[Dev Containers]] y otros [[Docker]]:
      ```JSON
      "containerEnv": {
      	"PYTHONPATH": "/workspaces/mlktools/whatever"
      }
      ```
    - Para importar desde directorios **que no están en el tree actual** hay que importar el directorio mínimo común en el **sys.path**
      ```python
      import sys
      import os
      sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
      from common.findmdfiles import findMdFiles
      ```
      En este caso, el directorio **common** estaba justo por encima del directorio del script importador
  - Errores de **importación circular**
    collapsed:: true
    - Estos errores se dan cuando dos módulos intentan importarse mutuamente con los **import** en la cabecera de los ficheros.
    - Una de las formas de solucionarlo es importar uno de los módulos no en la cabecera, sino dentro del método que lo vaya a utilizar.
      - Esto va a fallar, importación circular
        - ```python
          # Fichero a.py
          import b
          
          def a_method():
            b.something()
          
          # Fichero b.py
          import a
          
          def b_method():
            a.something()
          ```
      - Esta es una forma de solucionarlo: **a** carga a **b** en la cabecera, pero **b** carga a **a** en el método que lo va a utilizar. Así se evita el círculo.
        - ```python
          # Fichero a.py
          import b
          
          def a_method():
            b.something()
          
          # Fichero b.py
          def b_method():
            import a
            a.something()
          ```
  - Cómo crear una **API** para un módulo para que funcione de forma natural la sintaxis **modulo.objeto**
    collapsed:: true
    - Partiendo de lo desarrollado en la estructura del primer punto, desde fuera del módulo la sintaxis de los imports no es muy elegante. Debería ser algo como
      ```python
      from package_folder import A, B, C
      from package_folder.subpackage import SUB_A, SUB_B
      ```
    - Para conseguir esta API hay que trabajar un poco los **\_\_init.py\_\_** e incluso a veces los **.py** individuales
    - El \_\_init\_\_.py a nivel de **package_folder** sería así
      ```python
      from .a import A
      from .b import B
      from .c import C
      
      __all__ = [ "A", "B", "C" ]
      ```
    - Lo que expondría los objetos contenidos dentro de los **.py** de forma natural. Además, **\_\_all\_\_** delimitaría de forma unívoca que es lo que se importa al hacer un **import \***, de forma que no se cuele objetos que nos interesa exponer.
    - El **\_\_init\_\_.py** de **subpackage** estaría en la misma línea. Adicionalmente, cuando un **\_\_all\_\_** también se puede utilizar a nivel de un **.py** para definir que se exporta al usar **\***
      ```python
      __all__ = [ "a" ]
      
      def a():
        pass
      
      def b():
        pass
      ```
    - En el ejemplo anterior, sólo **a()** sería exportado desde este **.py** al importar con **\***
- # Convenciones de nombre de objetos
  collapsed:: true
  - **Packages y modulos:** los guiones bajos están desaconsejados, nombres cortos lowercase.
- # Ejecutar **virtualenv** dentro de [[Docker]]
  collapsed:: true
  - **Esto está anticuado porque los [[Dev Containers]] de [[Visual Studio Code]] hacen un trabajo mejor.**
  - Lo interesante de [[virtualenv]] es que permite una aproximación flexible como NPM para instalar paquetes a nivel de proyecto, no global. Una vez el código está listo para producción, instalar en la imagen [[Docker]] de producción los paquetes de forma global. [[Virtualenv]] está instalado en la imagen [[Docker]] **malkab/python**.
  - El uso de [[virtualenv]] permite mantener paquetes instalados de sesión en sesión sin tener que instalarlos en el contenedor [[Docker]].
  - Lo normal es instalar en el [[virtualenv]] [[ipython]] para hacer sesiones interactivas.
  - Pasos para crear el [[virtualenv]], dentro del contenedor [[Docker]] de Python
    collapsed:: true
    - ```shell
      # Creación
      virtualenv libpyexample
      
      # Activación
      . libpyexample/bin/activate
      
      # Listar los paquetes instalados
      pip list
      
      # Instalar paquetes
      pip install ipython
      
      # Salir del entorno
      deactivate
      ```
- # Crear **scripts de línea de comando** en Python
  - Ejemplo de **shebang**
    collapsed:: true
    - ```shell
      #!/usr/bin/env python3
      # coding=UTF8
      # -*- coding: utf-8 -*-
      
      print("This is the Python3 shebang")
      ```
  - Ejemplo de **getop**
    collapsed:: true
    - ```shell
      #!/usr/bin/env python3
      # coding=UTF8
      
      import getopt, sys
      
      # Help function
      def help():
        print("""
      Help 0
      Help 1
      """)
      
      # Default values for program parameters
      timeLimit = "today"
      dessagre = "diary"
      path = "."
      
      try:
        print("D: sys.argv[1:] ", sys.argv[1:])
      
        # Acepta tres argumentos r, m y t con parámetro
        # y tres k, l y h sin parámetro
        opts, args = getopt.getopt(sys.argv[1:], "r:m:t:klh")
      
      except getopt.GetoptError as err:
        print("Error: ", err)
        help()
        sys.exit(2)
      
      print("D: opts ", opts)
      print("D: args ", args)
      
      for o, a in opts:
        print("D: Final ", o, a)
      
        # Check for certain options
        if o == "-r":
          timeLimit = a
        if o == "-m":
          dessagre = a
        if o == "-h":
          help()
          sys.exit(0)
      
      # Process path arg
      if len(args) > 0:
        path = args[0]
      ```
  - Ver la librería [[Typer]] para los argumentos y [[Rich]] para mostrar información por pantalla.
  - Tenemos un buen ejemplo de [[Typer]] y [[Rich]] en [[G/sunnsaas_v2/backend]]/sunnsaas_cli.
  - Ejemplo de **Typer**
    collapsed:: true
    - ```Python
      #!/usr/bin/env python3
      # coding=UTF8
      
      import typer
      from typing import Optional
      
      # Typer app
      app = typer.Typer()
      
      # A command
      @app.command()
      def hello(name: str):
          print(f"Hello {name}")
      
      # Another command, with a mandatory argument and an optional option
      @app.command()
      def goodbye(name: str = typer.Argument(..., help="Docs name"),
          formal: bool = typer.Option(False, help="Docs formal")):
          """Main Doc.
      
          If --formal...
          """
          if not formal:
              print(f"Goodbye {name}")
          else:
              print(f"Goodbye Ms. {name}")
      
      if __name__ == "__main__":
          app()
      ```
- # Ejemplo de **[[JSON]] [[ETL]]**
  collapsed:: true
  - Lee un fichero [[JSON]], lo modifica y lo vuelve a escribir en un fichero
    collapsed:: true
    - ```shell
      import json
      
      # -------------------------
      #
      # Reads JSON from file, process it, and save results
      #
      # -------------------------
      
      wpBaseFolder = "workpackages/wp-2022-04-13-010-process-heliostat_fields/src"
      
      with open("%s/data/000_in/Hel_Eff_param.json" % wpBaseFolder) as f:
        data = json.load(f)
      
      coordinates = [ { \
        "id": i["id_hel"], \
        "x": i["coordinates"]["x"], \
        "y": i["coordinates"]["y"], \
        "z": i["coordinates"]["z"] \
      } for i in data["Hel_Eff_param_03_01"][0]]
      
      print(json.dumps(coordinates))
      
      with open("%s/data/900_out/hel_field.json" % wpBaseFolder, "w") as outfile:
        json.dump(coordinates, outfile)
      ```
  - Ejemplo de lectura de [[JSON]] para cargar en [[PostgreSQL]] con [[psycopg]] (consulta parametrizada)
    - ```python
      import json
      import os.path
      import psycopg
      
      # --------------------------------------
      #
      # Marvel CDB JSON data ingestor.
      #
      # --------------------------------------
      jsonPath = "../marvelsdb-json-data-master"
      
      connectionData = "host=postgis dbname=marvel user=postgres port=5432 password=postgres"
      
      # --------------------------------------
      #
      # Import of packtypes.json.
      #
      # --------------------------------------
      with open(os.path.join(jsonPath, "packtypes.json"), "r") as f:
        data = json.load(f)
      
      with psycopg.connect(connectionData) as conn:
        with conn.cursor() as cur:
          for i in data:
            cur.execute("""
              insert into marvelcdb.packtypes
              values (%(code)s, %(name)s)
              on conflict (code) do update set name = EXCLUDED.name;""", i)
      ```
- # Generar un **ejecutable Linux** a partir de un proyecto Python
  collapsed:: true
  - Utilizar **pyinstaller**:
    ```shell
    pip install -U pyinstaller
    ```
  - Generar el **build**:
    ```shell
    pyinstaller --onefile --clean main_program.py
    ```
  - **pyinstaller** tiene que ser instalado como **root** porque tiene un ejecutable global.
- # Generar paquetes [[wheel]]
  collapsed:: true
  - Instalar el builder: **pip install --upgrade build**.
  - Hacer el build: **python -m build** donde está el **pyproject.toml**.
  - Dejará en el directorio **dist** un fichero **.whl** con el paquete. Tiene el siguiente nombre: **pyfortest-0.0.1-py3-none-any.whl**, donde:
    collapsed:: true
    - **pyfortest** es el nombre del paquete;
    - **0.0.1** es la versión;
    - **py3** es la versión de Python;
    - **none** es el ABI, algo no sabemos muy bien lo que es pero es algo que depende de la plataforma si es que se usa algo de ella. **none** quiere decir que no se usa ninguna;
    - **any** es la plataforma, que puede ser **linux_x86_64**, por ejemplo, si es que tiene alguna dependencia. No sabemos muy bien cómo se relaciona con el ABI.
- # Leer ficheros en [[Python]]
  collapsed:: true
  - ```python
    with open(path_to_file) as f:
      contents = f.read()
      lines = f.readlines()
      line = f.readline
    
      f.close()
    ```
- # Escribir ficheros en [[Python]]
  collapsed:: true
  - ```shell
    import os.path as path
    
    with open(path.join(tmp_path, "fichero.txt"), "w") as f:
    	f.write("JJJJ")
    ```
- # Leer **[[YAML]]** en Python
  collapsed:: true
  - Instalar el módulo **pyyaml**: pip install pyyaml
  - ```python
    #!/usr/bin/env python3
    # coding=UTF8
    
    import yaml
    
    # Context, remember it will close the file at the end of the block
    with open("../yaml_db/campaign.yml") as f:
      y = yaml.safe_load(f.read())
    
      print("D: ", y)
    ```
- # Pasar **argumentos** a una función
  collapsed:: true
  - Lo normal, posicionales
    - ```python
      def func(a, b):
        print("Positional arguments", a, b)
      
      func("arg a", "arg b")
      ```
  - Posicionales con keywords opcionales
    - ```python
      def func(a, b, opt_a=None, opt_b=None):
        print("Positional arguments", a, b, opt_a, opt_b)
      
      # Esto funciona
      func("arg a", "arg b", opt_b="Optional B")
      
      # Pero esto va a dar un error de parámetro desconocido opt_c
      func("arg a", "arg b", opt_b="Optional B", opt_c="c")
      ```
  - Un posicional con un número indeterminado de no posicionales
    - ```python
      def func(a, b, *args):
        print("Positional arguments", a, b)
      
        for a in args:
          print(a)
      
      func("arg a", "arg b", "Indeterminado 0", "Indeterminado 1", "Indeterminado 2")
      ```
  - Un posicional e indeterminados con keywords
    - ```python
      def func(a, b, **kwargs):
        print("Positional arguments", a, b, opt_a, opt_b)
      
        for k, v in kwargs.items():
          print(k, v)
      
      func("arg a", "arg b", key0="Indeterminado 0", key1="Indeterminado 1")
      ```
  - Totalmente con keywords indeterminados, muy útil a la hora de pasar diccionarios de argumentos como en TypeScript
    - ```python
      def func(**kwargs):
        for k, v in kwargs.items():
          print(k, v)
      
      d = { "a": "arg a", "b": "arg b", "key0": "Indeterminado 0", "key1": "Indeterminado 1" }
      func(**d)
      ```
  - Pasar un diccionario como argumentos
    - ```Python
      def func(a: int, b: int) -> int:
      	return a + b
        
      d = { "a": 1, "b": 2 }
      func(**d)
      ```
- # #PostgreSQL Ejemplos **[[psycopg]] 3**
  collapsed:: true
  - Con contextos. Las conexiones o cursores se cierran automáticamente al terminar el contexto.
    - ```python
      # Note: the module name is psycopg, not psycopg3
      import psycopg
      from psycopg.rows import dict_row
      
      # Connect to an existing database
      # At the end of the context blocks resources are liberated
      with psycopg.connect("host=localhost dbname=postgres user=postgres") as conn:
      
        # Open a cursor to perform database operations
        with conn.cursor(row_factory=dict_row) as cur:
      
          # Execute a command: this creates a new table
          cur.execute("""
            CREATE TABLE test3 (
                id serial PRIMARY KEY,
                num integer,
                data text)
            """)
      
          # Pass data to fill a query placeholders and let Psycopg perform
          # the correct conversion (no SQL injections!)
          cur.execute(
            "INSERT INTO test (num, data) VALUES (%s, %s)",
            (100, "abc'def"))
      
          # Query the database and obtain data as Python objects.
          cur.execute("SELECT * FROM test")
          cur.fetchone()
          # will return a record as a dict
      
          # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
          # of several records, or even iterate on the cursor
          for record in cur:
            print(record)
      
          # Make the changes to the database persistent
          conn.commit()
      ```
  - Sin contextos, con registros de tipo diccionario. Hay que cerrar los objetos.
    - ```python
      import psycopg
      from psycopg.rows import dict_row
      
      c = psycopg.connect("host=localhost dbname=postgres user=postgres")
      
      cur = c.cursor(row_factory=dict_row)
      
      cur.execute("SELECT * FROM the_table ORDER BY campo_a");
      
      ans = cur.fetchall()
      
      for record in ans:
        print("AA", record["campo_a"], record["campo_b"])
      
      cur.close()
      
      c.close()
      ```
  - Consulta **parametrizada**
    collapsed:: true
    - ```python
      # Con un diccionario
      cur.execute("""
        insert into marvelcdb.packtypes
        values (%(code)s, %(name)s)
        on conflict (code) do update set name = EXCLUDED.name;""",
        { "code": "the_code", "name": "the_name" });
      
      # Con una tupla
      cur.execute("""
        INSERT INTO some_table (id, created_at, last_name)
        VALUES (%s, %s, %s);""",
        (10, datetime.date(2020, 11, 18), "O'Reilly"))
      ```
- # #Referencia Creación de PyPI packages
  collapsed:: true
  - Prerrequisitos
    collapsed:: true
    - ```shell
      python -m pip install --upgrade pip
      python -m pip install --upgrade build
      ```
  - Existe un magnífico ejemplo en **[[G/boilerplates/boilerplates]]/python/package_name**
  - Configurar el **pyproject.toml** y ejecutar **python -m build** para hacer el build en el directorio de dicho fichero de configuración
  - Instalar como 0:0 después con **pip install xxx.whl**
  - Se puede subir a **PyPI**
  - Los ficheros **.whl** se pueden instalar con **pip**
    collapsed:: true
    - ```shell
      pip install whatever.whl
      ```
  - Estructura de nombres de los paquetes **.whl**
    collapsed:: true
    - ```shell
      [ nombre de módulo ]-[ versión ]-[ versiones Python compatibles ]-[ ABI disponibles ]-[ plataforma ].whl
      ```
    - donde para Python normal y corriente **ABI** será **none** y **plataforma** **any**.
- # #Referencia Python in **[[Dev Containers]]**
  collapsed:: true
  - Hay un gran **ejemplo** en [[G/boilerplates/boilerplates]]/python_programs
  - Para instalar paquetes hay que hacerlo como root. En el boilerplate hay un fichero Docker llamado **020** que permite acceder al Dev Container con cualquier usuario.
- # Ejemplo de creación de un **context manager**
  collapsed:: true
  - ```python
    # Librería estándar que ayuda a la creación de contextos
    from contextlib import contextmanager
    import psycopg
    
      # Esta función crea un contexto, abriendo y cerrando una
      # conexión psycopg
      @contextmanager
      def get_connection(self):
        """Returns a connection to use within a with context manager.
    
        Yields:
            psycopg.connection: A connection to the database.
        """
        conn = psycopg.connect(self.env.get_connection_data())
    
        try:
          # Operaciones de apertura del contexto
          yield conn
        finally:
          # Operaciones de cierre
          conn.close()
    ```
- # #Referencia Ejemplo de **excepción** (**error**) personalizado
  collapsed:: true
  - ```python
    from typing import Dict
    
    # --------------------------------------
    #
    # Errors for workflow.
    #
    # --------------------------------------
    class ErrorWorkflow(Exception):
      """Error in workflow."""
    
      # --------------------------------------
      #
      # Workflow definition as dict.
      #
      # --------------------------------------
      workflow_definition: Dict[str, any] = None
      """Workflow definition as dict."""
    
      # --------------------------------------
      #
      # Error message.
      #
      # --------------------------------------
      message: str = None
      """Error message."""
    
      # --------------------------------------
      #
      # Constructor.
      #
      # --------------------------------------
      def __init__(self, workflow_definition: Dict[str, any], message: str=None):
        """Constructor.
    
        Args:
            workflow_definition (Dict[str, any]): The workflow definition as dict.
            message (str, optional): The error message. Defaults to None.
        """
        self.workflow_definition = workflow_definition
    
        if "process" in workflow_definition:
          self.message = message if message else \
            "Unknown workflow '%s'" % workflow_definition["process"]
        else:
          self.message = message if message else \
            "Malformed process: no 'process' identifier"
    
        super().__init__(self.message)
    ```
- # Documentación de código [[Python]]
  collapsed:: true
  - Utilizar la extensión de [[VSC]] **autoDocstring - Python Docstring Generator** para las funciones. Se activa con **C+S+2**. Sigue el estándar de documentación de [[Google]]. Sin embargo, no es capaz de ocuparse de todo. A continuación lo más importante.
    - [Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)
    - Se indenta con **4 espacios**
    - Usar para el rewrapping la extensión de [[VSC]] Rewrap (Alt + Q)
    - ## Nombre de objetos
      collapsed:: true
      - **Packages:** lower_with_under
      - **Modules:** lower_with_under, _lower_with_under
      - **Classes:** CapWords, _CapWords
      - **Exceptions:** CapWords
      - **Functions:** lower_with_under(), _lower_with_under()
      - **Global/Class Constants:** CAPS_WITH_UNDER, _CAPS_WITH_UNDER
      - **Global/Class Variables:** lower_with_under, _lower_with_under
      - **Instance Variables:** lower_with_under, _lower_with_under (protected)
      - **Method Names:** lower_with_under(), _lower_with_under() (protected)
      - **Function/Method Parameters:** lower_with_under
      - **Local Variables:** lower_with_under
    - ## Documentación en \_\_init\_\_.py
      collapsed:: true
      - El **\_\_init\_\_.py** puede llevar un comentario de bloque que aparece en la documentación de **[[pydoc]]**
      - ```python
        """Minim consequat minim laborum elit sint. Qui consectetur tempor duis eiusmod
        commodo consequat. Quis pariatur mollit nulla ex ut aliquip consectetur et et
        nisi.
        
        Irure quis eiusmod veniam ad excepteur excepteur non quis aliqua in. Sint esse
        fugiat veniam culpa nisi cupidatat ut fugiat anim pariatur laborum aliqua.
        Irure aute irure elit sint amet labore Lorem consequat cupidatat ea.
        
        Commodo veniam laboris officia esse pariatur eiusmod veniam culpa ea officia
        esse mollit eiusmod commodo.
        """
        ```
    - ## Ejemplo de clase
      - Para la Docstring general de la clase, usar el **VSC Snippet Class Docstring**.
      - ```python
        """This one is not generated by AutoDocString.
        
        USE THE VSC Rewrap extension (Alt + Q) extensively.
        
        Ex in eiusmod officia magna consequat quis consequat mollit. Cupidatat aliqua ex
        ea reprehenderit ea ullamco mollit voluptate reprehenderit adipisicing labore ad
        deserunt qui. Non aliqua fugiat do ipsum aliqua. Laborum aliquip exercitation
        aute magna exercitation eu elit. Est sunt sunt eiusmod labore tempor sint culpa
        ullamco ad eu cupidatat quis. Amet consectetur amet ipsum pariatur adipisicing
        cupidatat cupidatat reprehenderit enim labore. Commodo est eu nulla et dolor ut
        aute consectetur cupidatat.
        
        Amet dolore duis non enim in non. Culpa eu qui officia do ipsum commodo sit
        voluptate. Eiusmod incididunt nisi cupidatat consequat consectetur. Sit duis eu
        sit laborum veniam cillum adipisicing minim non velit cillum.
        """
        
        import x
        
        class MarvelousClass:
            """Summary of class here.
        
            Longer class information...
            Longer class information...
        
            The following Attributes section is not generated by AutoDocString.
        
            Attributes:
                likes_spam (int): A boolean indicating if we like SPAM or not.
                eggs (int): An integer count of the eggs we have laid.
        
            Raises:
            	Exception: Description.
            """
        
            def __init__(self, a: int):
                """Fully generated by AutoDocString.
        
                Args:
                    a (int):
                    	Whatever
                """
                self.a = a
        
            def a_method(self, a: int, b: int) -> int:
                """Fully generated by AutoDocString.
        
                Nisi anim id amet exercitation labore aliquip enim minim. Eiusmod labore
                nostrud dolore quis proident ut dolor aute. Velit duis incididunt sunt
                deserunt quis veniam officia sunt pariatur consectetur Lorem voluptate
                exercitation.
        
                Args:
                    a (int):
                        Amet dolore sit anim ut aute cupidatat cupidatat elit.
        
                        Nulla culpa eiusmod dolor mollit nisi veniam amet mollit. Elit
                        adipisicing ad ut proident dolor. Nostrud esse culpa nostrud
                        pariatur Lorem eu quis commodo exercitation eiusmod eu.
                    b (int):
                        Amet reprehenderit ullamco velit proident. Labore irure aliquip
                        eu laboris ullamco cupidatat tempor labore adipisicing qui aute
                        ad.
        
                        Labore aliqua tempor cupidatat et officia minim sunt ipsum irure
                        nulla exercitation laboris. Veniam nulla consequat do magna anim
                        amet eu occaecat. Aliquip laboris et nostrud irure aliqua
                        labore. Nostrud elit nisi exercitation elit deserunt non.
        
                        Nisi aliqua culpa anim eu laboris ullamco minim nulla in
                        consectetur veniam ipsum Lorem.
        
                Returns:
                    int:
                        Exercitation cupidatat sunt commodo est aliqua anim exercitation
                        in nisi. Sint esse aliquip laboris enim do. Pariatur sunt ex
                        aliqua mollit irure est aute ea ex. Ut duis minim labore Lorem
                        non Lorem aliquip exercitation minim laboris veniam commodo
                        ullamco ad. Eu ex velit magna tempor esse elit. Adipisicing
                        nostrud duis minim mollit pariatur ut laboris amet ipsum
                        occaecat.
                """
                return a + b
        
        ```
    - ## Ejemplo de módulo
      collapsed:: true
      - ```python
        """A module. Aliqua aliqua ex esse incididunt in exercitation magna ea nostrud
        occaecat. Pariatur est qui excepteur voluptate sint amet consectetur pariatur
        veniam laborum. Exercitation amet Lorem et ad deserunt voluptate consectetur
        voluptate aute ipsum. Magna nisi velit est incididunt irure labore ea. Sunt
        reprehenderit consequat nostrud id veniam.
        """
        
        import x
        
        A_CONSTANT = 89
        """Description. In ad tempor irure sint dolor. Ad est et eiusmod ullamco enim
        commodo veniam pariatur. Elit aute fugiat ipsum dolor excepteur sunt dolore nisi
        cupidatat. Nulla laboris duis magna id adipisicing tempor aute laboris est magna
        do.
        """
        
        def a_function(a: int, b: int, c: str) -> str:
            """Sumary. Veniam amet ea labore Lorem proident dolor aute laborum
            laboris qui non do occaecat. Consectetur esse aliquip laborum esse culpa
            occaecat quis culpa officia non laborum. Aute sunt tempor occaecat dolore
            aute minim. Mollit reprehenderit culpa duis velit ex dolor aliqua voluptate
            irure nisi. Dolore qui velit incididunt esse fugiat irure duis officia
            officia voluptate. Occaecat magna do adipisicing consequat mollit. Eu id
            nulla duis nisi officia tempor deserunt.
        
            Excepteur amet Lorem id magna exercitation excepteur irure cupidatat et
            ullamco fugiat amet. Laborum anim culpa laborum consequat fugiat minim
            nostrud voluptate laborum. Ullamco proident exercitation amet quis cupidatat
            esse ullamco quis nostrud excepteur consequat. Nulla incididunt est aliqua
            ea labore officia do. Voluptate nulla elit do ut sit nisi sit adipisicing.
        
            Args:
                a (int):
                    Dolor ex culpa nulla sint culpa laboris elit commodo excepteur
                    eiusmod enim aute et. Occaecat qui veniam dolore ullamco duis
                    excepteur esse officia magna tempor. Et ut tempor eiusmod nulla
                    deserunt. Mollit qui sint magna do.
                b (int):
                    Nostrud irure amet esse labore aliquip dolore nostrud esse magna
                    dolore enim nostrud occaecat. Deserunt veniam amet consectetur esse
                    qui. Enim magna velit adipisicing esse consectetur ipsum ut duis
                    aliquip amet aliqua non quis elit. Fugiat laborum nisi cillum
                    nostrud pariatur sunt nostrud duis Lorem aliquip.
                c (str):
                    Cillum sint aliquip qui mollit tempor qui officia ad quis voluptate
                    cupidatat laborum. Exercitation adipisicing esse culpa tempor elit
                    culpa. Ipsum ex cupidatat proident eu amet dolore deserunt tempor
                    adipisicing. Aute deserunt id sit est laborum ut minim commodo nulla
                    laborum laboris pariatur. Amet ut elit est voluptate non cillum
                    dolor qui occaecat velit labore duis.
        
            Returns:
                str:
                    Cillum laborum id nisi laboris qui mollit ut esse qui et dolore.
                    Non minim et id officia. Dolor laboris nostrud laborum qui proident
                    deserunt aliquip sint laborum ipsum irure magna.
        
                    Qui in nisi ullamco cupidatat nisi eu ipsum laboris amet esse
                    laborum aute ea nostrud. Ullamco adipisicing Lorem eiusmod cupidatat
                    dolore laboris. Incididunt cillum dolor magna mollit veniam ex do
                    enim cillum amet tempor ullamco reprehenderit laborum. Labore nisi
                    officia ipsum nostrud sunt quis anim sit esse veniam labore
                    cupidatat eiusmod nostrud.
            """
            return f"{c}: {a + b}"
        ```
  - Utilizar también nuestros code snippets en [[VSC]]
  - Para ver la documentación de los módulos instalados se usa el módulo **pydoc**
    - ```shell
      # Consulta en línea de un módulo
      python -m pydoc cli_helpers
      
      # Consulta en línea de un elemento de módulo
      python -m pydoc cli_helpers.multiinputtree
      
      # Apertura de un servidor HTTP para consulta interactiva
      # (funciona desde dentro de los Dev Containers de VSC).
      # Ejecutar este comando dentro del directorio src/package
      # del paquete que se quiere examinar.
      python -m pydoc -b
      ```
- # Python Typing
  collapsed:: true
  - Python con tipos, para referencia más que nada de los IDE y para el propio programador. Muy útil.
  - Ejemplos
    collapsed:: true
    - **Retorno de tuplas**
      collapsed:: true
      - ```Python
        import typing
        
        def authenticateToken(root: str, user: str, password: str) -> typing.Tuple[str, dict]:
          return ("str", { "a": 1 })
        
        # Para devolver el "self" dentro de una clase
        def load_yaml_data(self, yaml_data: Any) -> "Ware":
          pass
        ```
    - **Retorno de "self" dentro de una propia clase**
      collapsed:: true
      - Por ejemplo, si la clase se llama **Ware**
      - ```Python
        def load_yaml_data(self, yaml_data: Any) -> "Ware":
          pass
        ```
- # [[Jupyter Notebooks]] y [[Jupyter Labs]]
  collapsed:: true
  - Utilizamos la imagen [[Docker]] [[malkab/grass]] para lanzarlo
  - Este script lanza una instancia de [[Jupyter Labs]] en el puerto local **8888** con el token de acceso **token**
    - ```shell
      #!/bin/bash
      
      docker run -ti --rm \
        -p 8888:8888 \
        --user 1000:1000 \
        -v $(pwd)/notebooks:$(pwd)/notebooks \
        --workdir $(pwd)/notebooks \
        malkab/grass:holistic_hornet \
        -c "jupyter lab --ip 0.0.0.0 --allow-root --no-browser --NotebookApp.token="
      ```
  - Lo anterior se lanza en el navegador con **http://localhost:8888**
  - Otros lanzadores
    - ```shell
      # Con tokens de acceso, para proteger el acceso al servidor
      # Se accedería con http://localhost:8888?token=token
      jupyter notebook --ip 0.0.0.0 --allow-root --no-browser \
      	--NotebookApp.token='token' \
          --notebook-dir='/workspaces/didactica-coursera_machine_learning_specialization'
      
      jupyter lab --ip 0.0.0.0 --allow-root --no-browser --NotebookApp.token='token'
      ```
  - Uso dentro de [[Visual Studio Code]]
    - Arrancar [[Jupyter Notebooks]] (no el Lab ) en un contenedor [[Docker]] con un token (por ejemplo **token**), como se ve arriba
    - Una vez dentro de [[Visual Studio Code]], abrir el cuaderno y en la barra inferior, donde pone **Jupyter Server**, pulsar y meter el acceso al servidor con el token incluido: **http://localhost:8888?token=token**
- # [[IPython]]
  collapsed:: true
  - ## Ejecución de un Magic Command desde CLI
    collapsed:: true
    - ```bash
      ipython -c "%run -t script.py"
      ```
  - ## Magic Command %run
    collapsed:: true
    - Ejemplos:
      ```shell
      %run -d script.py
      %run -t -N5 script.py
      %run -p script.py
      ```
    - **-d** ejecuta con debugging, **-t -N5** ejecuta 5 veces el script y mide tiempo de ejecución, **-p** ejecuta con perfilador
  -
- # Instalación con [[pip]] de versiones concretas
  collapsed:: true
  - Así:
    - ```shell
      pip install -U \
          "numpy>=1.22,<1.24" \
          ipympl \
          matplotlib \
          tensorflow
      ```
- #procesar Poner un poco de orden aquí.