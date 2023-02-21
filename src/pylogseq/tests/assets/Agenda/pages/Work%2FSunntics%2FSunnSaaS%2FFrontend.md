filters:: {"a" true, "done" false}
title:: Work/Sunntics/SunnSaaS/Frontend

- Frontend Angular
	- Ubicación del código de las distintas pantallas según su URL
		- Todas parten de la ruta común **app/views/contenido/operations/resources/custom-resource/**
		- **Hel_Eff_param** (visualización del campo de heliostatos): heliostat-hourly-power
		- **Aiming_FlatPlane** (visualización de los puntos de apuntado): solar-flux-on-receiver
	- Vista de apuntado de heliostatos **Aiming_FlatPlane**
		- Usa el componente de visualización **d3-scatter-plot** (selector Angular app-d3-scatter-plot)
	- D3
		- **d3-scatter-plot** (selector Angular app-d3-scatter-plot)
			- Se encarga de la visualización de los aiming points en **Aiming_FlatPlane (solar-flux-on-receiver)**
			- El componente por si mismo no controla su tamaño, sino que es su inmediato padre, usualmente el elemento **app-d3-scatter-plot**, el que controla el tamaño interno. Usar el max-height y max-width.