El contenedor de dev recuerda el ID de la red del Compose en lugar de su nombre. Si el Compose se destruye con down, el dev container no arrancará. Hay que revincular la red con:

docker network connect [nombre red] [nombre dev container]
