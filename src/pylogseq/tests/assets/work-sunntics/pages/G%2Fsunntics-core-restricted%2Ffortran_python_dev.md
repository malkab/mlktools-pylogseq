- Este repo contiene los experimentos y la guía operativa de integración de [[Python]] y [[Fortran]] gracias a la librería Fortran [[Forpy]].
- # #G/sunntics-core-restricted/fortran_python_dev/010-docker-fortran_python
  collapsed:: true
  - Imagen [[Docker]] para la programación de [[Python]] + [[Fortran]] con [[Forpy]].
- # #G/sunntics-core-restricted/fortran_python_dev/020-pyfortest
  collapsed:: true
  - Un módulo de Python con funciones y un objeto, para hacer pruebas de concepto de encapsulamiento de su API en Fortran.
  - Se genera un módulo Wheels.
- # #G/sunntics-core-restricted/fortran_python_dev/025-pyfortest_additional
  collapsed:: true
  - Un módulo Python adicional para ver cómo pueden interaccionar varios wrappers Fortran en un mismo programa. El wrapper está en **030** junto al wrapper del **020**.
- # #G/sunntics-core-restricted/fortran_python_dev/030-forpy_wrapper
  collapsed:: true
  - El directorio **010-fortran_sample_module** investiga y prueba la creación de un módulo 100% Fortran que después se puede importar y utilizar en otros programas con **use**.
  - Prototipos y tests de creación de wrappers en un módulo reusable Fortran.
- # #G/sunntics-core-restricted/fortran_python_dev/040-test_fortran_env
  - Es WP establece tres entornos de prueba para todo lo desarrollado en **030**:
    - la creación desde un **Ubuntu barebone** de un entorno que permitiera la compilación de **030**, para probar lo que esta gente necesitaría;
    - un entorno **Ubuntu completamente barebone**, para ver qué habría que tener instalado para que el **compilado de 030 funcionara**;
    - la imagen de producción de los trabajadores, **[[registry.gitlab.com]]/sunnsaas/sunnsaas_v1/sunnsaas-worker-dev**, para evaluar que necesitaría ser instalado extra para que el compilado de 030 funcionara.
  - El entorno de prueba **010**, barebone para compilar, funciona perfectamente con una serie de instalaciones mínimas y los paquetes Python instalados en el sistema con **pip**.
  - El entorno de prueba **020**, barebone para ejecutar, funciona perfectamente también con dependencias de **pip** y **libgfortran5**.
  - El problema ha venido en el entorno **030**. Los dos entornos anteriores han utilizado Python 3.10, el Worker utiliza el 3.8, vamos a intentar compilar con el 3.8 desde 010. Ha sido fácil, ya que la imagen Docker oficial de **Ubuntu 20.04** carga directamente desde **apt** el Python adecuado. Todo ha compilado y funcionado sin problemas. Con esto cerramos satisfactoriamente las pruebas.