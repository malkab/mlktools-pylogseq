title:: Docker/SWARM

- **Docker Stack deployment**
  collapsed:: true
	- Parámetros
		- **-c** indica el fichero Compose que hay que utilizar para desplegar el SWARM
		- **--prune** tira servicios que ya no hacen falta
		- **--with-registry-auth** pasa al agente SWARM detalles de autenticación
	- ```shell
	  docker stack deploy \
	  		--with-registry-auth \
	          --prune \
	          -c cellgriddercontroller-full-swarm.yaml \
	  		cell_cellgriddercontroller
	  ```
- **Docker Stack remove**
  collapsed:: true
	- ```bash
	  docker stack rm stack_name
	  ```