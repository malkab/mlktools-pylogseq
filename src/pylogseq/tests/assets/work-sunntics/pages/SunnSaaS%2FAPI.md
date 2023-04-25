- # Consideraciones generales para el diseño de la API
  collapsed:: true
  - [#A] #RD Hay que mirar la especificación [[OpenAPI]] para implementarla y utilizar las herramientas de [[Swagger]] para implementar la documentación.
  - Los [[casos de uso]] se tratarán de forma separada. En **libsunnsaasbackend** evitaremos hacer desarrollos demasiado generalistas, no ha funcionado. Terminan siendo muy disimilares y todo se embarulla mucho. Por lo tanto, cada una tendrá su clase y sus propios métodos. Algunos serán compartidos y se intentará que tengan la misma API de clases dentro de lo posible.
  - En cuanto a la [[OpenAPI]], también se intentará que haya entradas únicas para funcionalidades que tengan varios de los [[casos de uso]]. Por ejemplo, tanto el [[Design & Optimization]] como el [[Energy Yield Assessment]] tienen un método que se llama **heliostatfield**, que sirve para los mismo, por lo que deben tener el mismo esquema y compartir la misma entrada API.
  - Por tanto, el esquema de las entradas API será el siguiente:
    - **/analysis/:analysisId/heliostatfield/(csv/json)**
    - En el caso de que el **:analysisId** considerado no soporte dicho método, error.
- # Testeo e interacción con la [[SunnSaaS/API]]
  collapsed:: true
  - Tenemos varias formas de testear e interaccionar con la API.
  - Tenemos material [[Postman]] a descartar. No lo vamos a seguir usando porque se cuelga mucho y es inestable.
  - Para interaccionar directamente con una instancia [[SunnSaaS]] tenemos un conjunto de scripts [[cURL]] en **010_api/api_testing/curl_api**, para algo rápido y cómodo.
  - Para los tests sistemáticos, tenemos un repositorio [[G/sunnsaas/sunnsaas_api_tests]] con tests en [[Python]].
- # Librería libsunnsaasdef
  collapsed:: true
  - En el [[frontend]] se sabe de qué output Dataset está tirando una pantalla por la URL. Por ejemplo, **operations/resource/1JJ6ZMFNt/EYA_OUT_PLANT_GENERATION_OUTPUTS/output** está mostrando el Dataset **EYA_OUT_PLANT_GENERATION_OUTPUTS** de un EYA.
- # Ejemplos de tareas repetitivas importantes
  collapsed:: true
  - ## Exportación de CSV (fichero) y JSON
    collapsed:: true
    - El método **/analysis/:analysisId/heliostatfield/:format?** de **analysisrouter.ts** tiene un ejemplo de exportación de datos tanto en CSV como en JSON.