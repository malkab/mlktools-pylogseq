- El infierno de los **IMPORTS** y los **PACKAGES** y demás, una guía esperamos que definitiva (Python 3)
  collapsed:: true
  - Un **package** Python es un directorio que, aunque no sea obligatorio, tiene un fichero **\_\_init\_\_.py** en el que se hacen inicializaciones del package y/o se hace una selección de lo que se exporta. Un **módulo** no es más que un fichero **.py**, que también es importable.
  - Por ejemplo, un package compuesto por tres ficheros fuente **a.py**, **b.py** y **c.py**
    collapsed:: true
    - ```python
      u = 44
      ```
    - ```python
      def sum(a, b):
        return a+b
      ```
    - ```python
      from .b import sum
      
      class CL:
        def sumPlus4(self, a,b):
          return 4+sum(a,b)
      ```
  - Nótese que el tercer fichero importa del propio package un elemento con **import .b import sum**.
    collapsed:: true
    - Para este módulo queremos exportar **a.py/u** y **c.py/CL**. Por ello, en el **\_\_init\_\_.py**
      - ```python
        from .a import u
        from .c import CL
        ```
  - Para usar el package en **código**
    collapsed:: true
    - ```python
      from apack import u, CL
      
      print(u)
      
      obj = CL()
      
      print(obj.sumPlus4(3,2))
      
      ```
  - **Búsqueda de packages y módulos**
    collapsed:: true
    - Como norma general, Python busca en el directorio del fichero lanzado con **python whatever.py**. Si el directorio del **package** cuelga del directorio en el que está el fichero de script que se lanza, Python lo encontrará sin problemas. Por ello, en desarrollo, cualquier package que esté en el directorio principal será encontrado. Esto incluye si el **package** está incluido en un árbol de directorios. Por ejemplo, si la estructura de directorio es:
      ```shell
      src
        + - package_container
              + - packA
              + - packB
      ```
      para importar **packA** desde **src** habría que importar:
      ```python
      from package_container.packA import whatever
      ```
    - Si el **package** no cuelga del directorio principal del **script** hay que utilizar la variable **PYTHONPATH**. **PYTHONPATH** permite indicar una serie de directorios donde se buscarán packages en cascada. Se puede definir a nivel de shell:
      ```shell
      export PYTHONPATH="$PYTHONPATH:path/to/folder/a:path/to/folder/b"
      ```
      y en [[Visual Studio Code]] [[Dev Containers]] y otros [[Docker]]:
      ```JSON
      "containerEnv": {
      	"PYTHONPATH": "/workspaces/mlktools/pylogseq"
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
    - Estos errores se dan cuando dos módulos intentan importarse mutuamente con los **import** en la cabecera de los ficheros
    - Una de las formas de solucionarlo es importar uno de los módulos no en la cabecera, sino dentro del método que lo vaya a utilizar
      collapsed:: true
      - Esto va a fallar, importación circular
        collapsed:: true
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
        collapsed:: true
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
- Ejecutar **virtualenv** dentro de [[Docker]]
  collapsed:: true
  - **Esto está anticuado porque los [[Dev Containers]] de [[Visual Studio Code]] hacen un trabajo mejor**
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
- Crear **scripts de línea de comando** en Python
  collapsed:: true
  - Ejemplo de **shebang**
    - ```shell
      #!/usr/bin/env python3
      # coding=UTF8
      # -*- coding: utf-8 -*-
      
      print("This is the Python3 shebang")
      ```
  - Ejemplo de **getop**
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
- Ejemplo de **[[JSON]] [[ETL]]**
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
- Generar un **ejecutable Linux** a partir de un proyecto Python
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
- Leer **ficheros** en Python
  collapsed:: true
  - ```python
    with open(path_to_file) as f:
      contents = f.read()
      lines = f.readlines()
      line = f.readline
    
      f.close()
    ```
- Leer **[[YAML]]** en Python
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
- Distribuciones de **frecuencia aleatoria** en Numpy
  collapsed:: true
  - ```python
    s = 1000
    
    gum0 = np.random.gumbel(50, 10, s)
    poisson0 = np.random.poisson(5, s)
    logistic0 = np.random.logistic(70, 25, s)
    
    gum1 = np.random.gumbel(40, 8, s)
    poisson1 = np.random.poisson(2, s)
    logistic1 = np.random.logistic(100, 15, s)
    
    gum2 = np.random.gumbel(64, 12, s)
    poisson2 = np.random.poisson(4, s)
    logistic2 = np.random.logistic(84, 40, s)
    ```
- Pasar **argumentos** a una función
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
- #PostgreSQL Ejemplos **[[psycopg]] 3**
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
- #Referencia Creación de **PyPI packages**
  collapsed:: true
  - Prerrequisitos
    - ```shell
      python -m pip install --upgrade pip
      python -m pip install --upgrade build
      ```
  - Existe un magnífico ejemplo en **[[GitRepo/boilerplates/boilerplates]]/python_programs/package_name**
  - Configurar el **pyproject.toml** y ejecutar **python -m build** para hacer el build en el directorio de dicho fichero de configuración
  - Instalar como 0:0 después con **pip install xxx.whl**
  - Se puede subir a **PyPI**
- #Referencia Python in **[[Dev Containers]]**
  collapsed:: true
  - Hay un gran **ejemplo** en [[GitRepo/boilerplates/boilerplates]]/python_programs
  - Para instalar paquetes hay que hacerlo como root. En el boilerplate hay un fichero Docker llamado **020** que permite acceder al Dev Container con cualquier usuario.
- Ejemplo de creación de un **context manager**
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
- #Referencia Ejemplo de **excepción** (**error**) personalizado
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
- #Referencia Ejemplo **PyTest**
  - Crear dentro del directorio de test ficheros que terminen en **_test.py**
  - Los tests se pueden lanzar en consola estando en el directorio de los tests
    - ```shell
      # Simple
      pytest
      
      # -v para verbose, -s para mostrar los print() a medida que se ejecutan
      pytest -vs
      ```
  - Estos ficheros tienen la siguiente esctructura:
    - ```python
      import sys
      import os
      sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
      
      import pytest
      
      from geowhale.src.geowhale.columns.basecolumn import BaseColumn
      from geowhale.src.geowhale.exceptions.errorcolumncreation import ErrorColumnCreation
      from geowhale.src.geowhale.exceptions.errorschemavalidator import ErrorSchemaValidator
      
      # --------------------------------------
      #
      # Suite de tests A
      #
      # La clase debe comenzar por Test
      #
      # --------------------------------------
      class TestInstantiation:
        
        # Los tests dentro deben comenzar por test_
        def test_no_name(self):
          with pytest.raises(ErrorColumnCreation) as e:
            BaseColumn()
            
            # Si la excepción se produce en la línea anterior, 
            # esta nunca llegará
            print("Nunca se llega aquí porque la excepción salta arriba")
      
          # ¡Atención! El assert está fuera del contexto
          assert e.value.message == "Error creating column: no name provided"
      
        def test_a(self):
          assert 4 < 5
          
        # No type
        def test_no_type(self):
          with pytest.raises(ErrorColumnCreation) as e:
            BaseColumn(name="A")
      
          assert e.value.message == "Error creating column A: no udt_name provided"
      
        # No position
        def test_no_position(self):
          a: BaseColumn = BaseColumn(name="A", udt_name="int")
      
          assert a.name == "A"
          assert a.udt_name == "int"
          assert a.position == None
      
      # --------------------------------------
      #
      # Suite de tests B
      #
      # --------------------------------------
      class TestEquality:
        
        def test_equality_bad_name(self):
          with pytest.raises(ErrorSchemaValidator) as e:
            a: BaseColumn = BaseColumn(name="A", udt_name="int")
            b: BaseColumn = BaseColumn(name="B", udt_name="int")
      
            a == b
      
          assert e.value.message == "Column name mismatch: A / B"
      
        def test_equality_bad_type(self):
          with pytest.raises(ErrorSchemaValidator) as e:
            a: BaseColumn = BaseColumn(name="A", udt_name="int")
            b: BaseColumn = BaseColumn(name="A", udt_name="varchar")
      
            a == b
      
          assert e.value.message == "Column data type mismatch for column A: int / varchar"
      ```