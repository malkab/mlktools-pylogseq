filters:: {"done" false}

- [#C] Recordar que nosotros estamos trabajando en **24_polar_dev_slope_inarow** y que toda nuestra documentación está yendo a esa rama. Debería estar en **develop** para ser independientes de esta gente, pero no hay manera.
- # Versiones
  collapsed:: true
  - Tenemos la versión 1, en [[Node]], en [[G/sunnsaas/sunnsaas_v1]].
  - Tenemos la versión 2, en [[Python]], en [[G/sunnsaas_v2]].
- # IT
  collapsed:: true
  - Ahora mismo la instancia más actualizada es **beta/latest**
  - Tenemos dos instancias en dos servidores AWS llamados **beta** (uno minúsculo para el frontend, otro medianito para los backend) para que se vayan alternando:
    collapsed:: true
    - **latest:** identificadores:
      - **sunnsaas_v1** en el servidor backend para la API y el backend
      - **sunnsaas-frontend** en el servidor frontend
      - responde en muchos aspectos al nombre **latest**
    - **stable:** identificadores:
      - **sunnsaas_v1_stable** en el servidor backend para la API y el backend
      - **sunnsaas-frontend-stable** en el servidor frontend
      - responde en muchos aspectos al nombre **stable**
- # Variables SunnSaaS
  collapsed:: true
  - Receiver Type
    collapsed:: true
    - Define el tipo de receptor
      - **0:** circular field
      - **1:** Polar field cylinder section
      - **2:** rectangle receiver
      - **3:** rectangle entrance to cavity
  - Estados de ejecución de Analysis y Tasks **EROSTATUS**, tanto en código TS y en la DB
    collapsed:: true
    - **0:** NOTREADY
    - **1:** READY
    - **2:** ONHOLD
    - **3:** RUNNING
    - **4:** POSTPROCESSING
    - **5:** ERROR
    - **6:** COMPLETED
- # Autenticación de usuarios
  collapsed:: true
  - A la hora de restaurar una base de datos entre instancias los nervios pueden quebrarse a la hora de la autenticación de los usuarios y su acceso a la API. Que no cunda el pánico. Hay que revisar bien el **mlkctxt** de la instancia. Mirar la configuración **api**, sobre todo: las distintas **init_password** y compañía, **hashedpasswords** y las *sales* **jwt_access_token_secret**, que pueden ser distintas en cada instancia.
  - Revisar también el acceso principal a la base de datos en **sunnsaas_db.password**
- # Migración de volúmenes PostgreSQL: almacén corrupto
  collapsed:: true
  - Si se hace a lo burro, sin tener el servidor apagado, lo normal es que el dumpeo del volumen venga echo trizas y haya que repararlo. Al arrancar la base de datos, se quejará con un error **PANIC: could not locate a valid checkpoint record**. Tenemos un script para entrar en modo bash para reparar el almacen con:
    ``` shell
        pg_resetwal DATADIR
    
        pg_resetwal -f DATADIR
    ```
  - Si Dios quiere, saldrá andando