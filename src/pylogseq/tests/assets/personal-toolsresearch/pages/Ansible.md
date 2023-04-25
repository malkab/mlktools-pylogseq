- #Referencia Tenemos un ejemplo del uso de [[Ansible]] en **devops/kerdes**.
- # Instalación
  collapsed:: true
  - Sólo **python3 -m pip install --user ansible**
  - Algunos módulos requieren paquetes adicionales en los hosts, pero avisa cuando no los encuentra.
- # Inventarios
  collapsed:: true
  - Crear un inventario en el directorio local con nombre **inventory.yaml**. Se pueden combinar con [[mlkctxt]]:
    collapsed:: true
    - ```yaml
      machines:
        hosts:
          kerdes:
            ansible_host: 172.0.4.5
        vars:
          ansible_user: whatever
      ```
  - Listar hosts y hacer ping:
    collapsed:: true
    - ```shell
      ansible-inventory -i inventory.yaml --list
      
      ansible machines -m ping -i inventory.yaml
      ansible kerdes -m ping -i inventory.yaml
      ```
  - ## Inventario jerarquizado
    collapsed:: true
    - Este es un ejemplo de inventario jerarquizado:
      - ```yaml
        # Todos los
        all_my_machines:
          hosts:
            api_a:
              ansible_host: 1.1.1.1
            frontend_a:
              ansible_host: 2.2.2.2
            test:
              ansible_host: 0.0.0.0
          children:
            api:
              hosts:
                api_a:
            frontend:
              hosts:
                frontend_a:
          vars:
            ansible_user: ubuntu
        ```
    - Se llaman de esta manera:
      - ```shell
        # Ping al supergrupo all_my_machines
        ansible all_my_machines - m ping -i inventory.yaml
        
        # Ping a un host determinado
        ansible api_a -m ping -i inventory.yaml
        
        # Ping a un grupo
        ansible api -m ping -i inventory.yaml
        
        # Ping al grupo predeterminado "all" (equivalente a "all_my_machines")
        ansible all -m ping -i inventory.yaml
        
        # Ping a los hosts que no pertenecen a ningún grupo (en este caso, sólo "test")
        ansible ungrouped -m ping -i inventory.yaml
        ```
- # Playbooks
  - Añadir una clave [[PEM]] para que Ansible contacte servidores por ejemplo en [[AWS]]. Es muy sencillo, se hace por cada sesión
    - ```shell
      ssh-add path/to/pem/file.pem
      ```
  - Ejecución de Playbooks
    - ```shell
      ansible-playbook -i inventory.yaml -v -f 10 010-playbook-despliegue_web.yaml
      ```
    - **-i** para indicar el inventorio;
    - **-v** para verbose;
    - **-f X** para multiproceso;
    - finalmente, el **fichero** del Playbook.
  - Crear un fichero **playbook.yaml**
    collapsed:: true
    - ```yaml
      - name: My first play
        hosts: machines
        tasks:
         - name: Ping my hosts
           ansible.builtin.ping:
         - name: Print message
           ansible.builtin.debug:
             msg: Hello world
      ```
  - Combinar [[Cookiecutter]] con [[Ansible]]
    collapsed:: true
    - Dado que ambos sistemas usan [[Jinja2]] para hacer templating, hay conflictos entre ellos. En el caso de que [[Ansible]] necesite dejar intacto una macro de substitución de Jinja2, la sintaxis es la siguiente:
      - ```yaml
        # Esto es una substitución de Cookiecutter
        - name: Arrancar proxy HTTPS
          community.docker.docker_stack:
        	state: present
        	name: nginx_https_proxy
        	compose:
        	  - "{{ cookiecutter.nginx_proxy_folder }}/020-docker-compose-https.yaml"
        
        # Pero esto es una substitución de Ansible que Cookiecutter respeta
        # gracias a {% raw %} loquesea {% endraw %}
        - name: Levantar stacks
          ansible.builtin.script: "profiles/{% raw %}{{ profile }}{% endraw %}/scripts/x
        ```
  - ## Tasks
    collapsed:: true
    - **Hacer dumps de bases de datos remotas y traer el dump a local:** para ello, en [[G/boilerplates/boilerplates]]/devops/postgres_db_dumps_docker hay un Ansible para hacer los dumps.
    - Ejemplos de tareas comunes
      collapsed:: true
      - ```yaml
        # -----------------------
        #
        # Trabajo con ficheros y directorios
        #
        # -----------------------
        - name: Borra un directorio
          ansible.builtin.file:
        	state: absent
        	path: /home/jpperez/cloudrisk_web
        
        - name: Crea un directorio con permisos
          ansible.builtin.file:
            path: /home/jpperez/cloudrisk_web
            state: directory
            mode: '0755'
        
        - name: Darle a un fichero permisos
          ansible.builtin.file:
        	path: "whatever/certbot_script/certbot_script.sh"
        	mode: "0755"
        
        
        # -----------------------
        #
        # Subida de datos
        #
        # -----------------------
        - name: Sube un directorio, creando el directorio en "dest"
          ansible.builtin.copy:
        	src: web_src
        	dest: /home/jpperez/cloudrisk_web
        
        # Copiar los contenidos un directorio a un directorio remoto
        # Nótese el / final, el directorio remoto se crea sólo
        - name: Subida de assets
          ansible.builtin.copy:
        	src: assets/beta_sunnsaas/
        	dest: ~/nginx_proxy
            
            
        # -----------------------
        #
        # Bajada de datos
        #
        # -----------------------
        # Bajada de los contenidos de un directorio remoto
        # Es un poco enrevesado puesto que fetch no permite
        # descargar directamente directorios, por lo que 
        # primero hay que encontrar los ficheros que están
        # dentro
        
        # Lista de ficheros a descargar
        - shell: (cd /home/apps/cell_db_dumps; find . -maxdepth 1 -type f) | cut -d'/' -f2
          register: files
        
        # Bajada
        - name: Bajada de las copias de seguridad
          ansible.builtin.fetch:
          	src: /home/apps/cell_db_dumps/{{ item }}
          	dest: /home/malkab/Desktop
          	owner: malkab
        	group: malkab
          	mode: 0644
          with_items: "{{ files.stdout_lines}}"
        
        
        # -----------------------
        #
        # Ejecución de scripts
        #
        # -----------------------
        # Se ejecuta en un directorio determinado
        - name: Ejecuta un script local en el remoto
          ansible.builtin.script: ./whatever/script.sh
          args:
        	chdir: /home/apps/test_temp
        
        # Ejecuta un script definido por una variable
        - name: Script por variable
          ansible.builtin.script: scripts/{{ x }}
          args:
        	chdir: /home/apps/test_temp
        
        
        # -----------------------
        #
        # Bajar datos desde URL
        #
        # -----------------------
        - name: Bajada de datos desde URL
          ansible.builtin.get_url:
            url: https://s3.amazonaws.com/kepler-cell-db-dumps/cell_db_dumps.tar.gz
            dest: /home/apps/cell_db_dumps/cell_db_dumps.tar.gz
            mode: 0644
            owner: apps
            group: apps
        
        
        # -----------------------
        #
        # Docker
        #
        # -----------------------
        # El docker-compose.yaml debe estar en el remoto previamente
        - name: Levanta un Compose
          community.docker.docker_stack:
        	state: present
        	name: nginx_test
        	compose:
        	  - /home/apps/test_temp/assets/docker-compose-nginx.yaml
        
        - name: Parar un Docker Compose
          community.docker.docker_stack:
        	state: absent
        	name: nginx_https_proxy
        
        - name: Descargar imagen Docker
          docker_image:
          	name: certbot/certbot
          	tag: latest
          	source: pull
        
        - name: Borrar imagen Docker
          docker_image:
            name: certbot/certbot
            tag: latest
            state: absent
        
        - name: Levanta un contenedor Docker
          docker_container:
        	  name: web_hello_world
        	  image: tutum/hello-world
        	  ports:
        	  - 8097:80
        
        
        # -----------------------
        #
        # Ejecución de comandos
        #
        # -----------------------
        - name: Ejecuta un comando en remoto
          ansible.builtin.shell: echo XXX
        
        - name: Ejecuta comando remoto con una variable
          ansible.builtin.shell: echo {{ x }}
        
        - name: Ejecución pero formateando la salida del output
          ansible.builtin.shell: df -h
          register: out
        
        - debug: var=out.stdout_lines
        
        
        # -----------------------
        #
        # Pausar el Playbook
        #
        # -----------------------
        - name: Pausar el Playbook
          ansible.builtin.pause:
        	seconds: 10
        
        
        # -----------------------
        #
        # Reinicio de sistema
        #
        # -----------------------
        - name: Reinicio
          become: true
          ansible.builtin.reboot:
        	reboot_timeout: 3600
        ```