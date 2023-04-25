- Metodología y librería para hacer tests en [[Python]], muy útil. Otra es una librería, también estándar, llamada **unittest** o algo así, pero nosotros usamos esta.
- #Referencia #Python #PyTest Tenemos un buen ejemplo de tests en [[G/sunnsaas/sunnsaas_api_tests]]
- #Referencia #Python #PyTest #API Ejemplo de testeo [[PyTest]] de una API (SunnSaaS) en [[G/sunnsaas/sunnsaas_api_tests]]
- # Instalación
  collapsed:: true
  - Tan sólo **pip install --upgrade pytest**.
- # Uso
  - Crear dentro del directorio de **test** ficheros que terminen en **_test.py**
  - Los tests se pueden lanzar en consola estando en el directorio de los tests
    collapsed:: true
    - ```shell
      # Simple
      pytest
      
      # -v para verbose, -s para mostrar los print() a medida que se ejecutan
      pytest -vs
      
      # Lanzar un módulo de test específico
      pytest -vs block_test.py
      
      # Lanzar un test específico por nombre
      pytest -rP -k "test_ping or test_apiinfo"
      ```
  - Estructura de los ficheros de test
    collapsed:: true
    - ```python
      import sys
      import os
      sys.path \
      	.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
      
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
  - Obviando tests con **skip**
    collapsed:: true
    - Para obviar tests se puede usar, a nivel de **class** o **def**, **skip** o **skipif**
      - ```python
        # skips incondicionales
        @pytest.mark.skip
        class TestPosixCalls:
          @pytest.mark.skip(reason="Porque sí")
          def test_function(self):
          	"will not be setup or run under 'win32' platform"
        
        # skips condicionales
        @pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
        class TestPosixCalls:
          def test_function(self):
            "will not be setup or run under 'win32' platform"
        ```
  - Ejecutar sólo algunos tests
    - ```python
      # Poner una marca
      @pytest.mark.x
      def test_a(self):
          pass
      ```
    - Ejecutar los tests con la marca **x**: **pytest -m x**
  - Utilizar un directorio temporal que el propio **PyTest** crea
    collapsed:: true
    - ```shell
      import os.path as path
      
      def test_ping(self, tmp_path):
      
      	print("D: ", path.join(tmp_path, "example.txt"))
      
          with open(path.join(tmp_path, "example.txt"), "w") as f:
            f.write("A line\n")
      
      	assert 1 == 1
      ```
  - Es importante usar los **fixtures** para reaprovechar configuraciones comunes a varios tests. Se pueden encontrar ejemplos en [[G/sunnsaas/sunnsaas_api_tests]] y en [[G/boilerplates/cookiecutter]], sección **python-tests**.
- # Assertions
  collapsed:: true
  - Algunas de las assertions más utilizadas
  - ```python
    # Tipos
    assert type(a) is str
    assert isinstance(a, str)
    
    # Números float aproximados
    assert a() == pytest.approx(3.3)
    
    # Excepciones
    with pytest.raises(Exception) as a:
      raise_error("This is an error")
    
    assert str(a.value) == "This is an error"
    ```