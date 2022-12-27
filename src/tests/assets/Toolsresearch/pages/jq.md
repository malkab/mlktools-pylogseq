- Una aplicación de línea de comando para manipular [[JSON]]. Muy potente.
- **Visualizar el JSON con colores**
	- ```shell
	  jq --color-output "." file.json
	  ```
- **Exportar el JSON a forma "pretty"**
	- ```shell
	  jq "." non-pretty.json > pretty.json
	  ```
- **Examinar sólo las claves**
	- ```shell
	  jq ". | keys" file.json
	  
	  jq ".data | keys" file.json
	  ```
- **Añadir claves**
	- Añade una clave **NRecTyp** dentro del elemento **data** con valor 0
		- ```shell
		  jq '.data += { "NRecTyp": 0 }' file.json > new_file.json
		  ```
	- Retorna el elemento **data** (sin el resto del fichero) con una nueva clave **NRecTyp** con valor 0 (cambio de **=** por **+=**)
		- ```shell
		  jq '.data + { "NRecTyp": 0 }' file.json > new_file.json
		  ```
- **Minimizar el JSON**
	- ```shell
	  jq -r tostring file.json > minified.json
	  ```