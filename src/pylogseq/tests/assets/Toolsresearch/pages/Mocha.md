- [#A] CONTINUAR creando la boilerplate de Mocha y haciendo pruebas de cómo se usa Node como devcontainer en VSC, ahora que tenemos la nueva v18.12.1 con acceso sudo para instalar cosas
- Usar **.skip** and **.only** para seleccionar los test a ejecutar
- A la hora de escribir tests para **[[TypeScript]]**, hay que tener en cuenta que Mocha sólo entiende JavaScript, por lo que hay que paralelizar el build con Nodemon para que siempre esté actualizado. Se necesita como dependencias de desarrollo el **[[npm-run-all]]** para ejecutar varios targets del **package.json** simultáneamente, el propio **Mocha** y **[[Chai]]** como librería de *assertions*.
- Encerrar todos los tests de un fichero en un bloque **describe** de forma que se pueden ejecutar sólo los que hay en dicho fichero con **.only** sobre el bloque padre. No indentar dentro y señalar el cierre bien
  - ```shell
    /**

      Comentario del test.

    */
    describe.only("Meteo data processing tests", function() {

    // Tests aquí
    describe...

    // This ends the main describe block
    });
    ```
- En el **package.json** hay que definir una serie de targets
  - Para
- # Cómo estructurar tests Mocha
  - La estructura de directorios es
    - ```txt
      tests
        +-- main.test.ts      # imports de tests, para ejecutarlos de golpe
      ```
