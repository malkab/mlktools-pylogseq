- Perfil que busca la variable de entorno **MLK_GIT_HOME** para determinar el directorio Git del repositorio
  collapsed:: true
	- ```yaml
	  # Set GIT home if the MLK_GIT_HOME env var exists
	  # If not set, defaults to /home/git
	  <% GITDIR=ENV["MLK_GIT_HOME"] %>
	  <% if GITDIR=="" %>
	  <% GITDIRF="/home/git" %>
	  <% else %>
	  <% GITDIRF=GITDIR %>
	  <% end %>
	  
	  name: cli_helpers
	  root: <%= GITDIRF %>/libraries_python/cli_helpers
	  
	  windows:
	    - docker: >
	        cd docker ;
	        sleep 0.2 ;
	        clear ;
	        echo Run dev environment at 010
	  ```