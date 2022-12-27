- # Instalación y ejecución en [[Linux]]
  - Descargar y ejecutar, se instala en **~/anaconda3**
  - Tiene una aplicación en **bin/anaconda-navigator** que permite lanzar las apps del ecosistema
  - Anaconda modifica el **.bashrc** metiendo cosas propias que rompen la instalación local de Python. Por ello, el siguiente **script** lanza [[Anaconda]] Navigator sin interferir en él.
    - ```shell
      # -----------------------------------------------------------------
      #
      # Anaconda Navigator launch script. Put this in 
      # /usr/local/bin/anaconda-navigator.
      #
      # -----------------------------------------------------------------
      export PYTHONPATH=
      export ANACONDA_HOME=/home/malkab/anaconda3
      
      # -----------------------------------------------------------------
      #
      # This block is what Anaconda hideously inject in our .bashrc (not nice!)
      #
      # -----------------------------------------------------------------
      # >>> conda initialize >>>
      # !! Contents within this block are managed by 'conda init' !!
      __conda_setup="$('/home/malkab/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
      if [ $? -eq 0 ]; then
          eval "$__conda_setup"
      else
          if [ -f "/home/malkab/anaconda3/etc/profile.d/conda.sh" ]; then
              . "/home/malkab/anaconda3/etc/profile.d/conda.sh"
          else
              export PATH="/home/malkab/anaconda3/bin:$PATH"
          fi
      fi
      unset __conda_setup
      # <<< conda initialize <<<
      
      # Run Anaconda Navigator
      $ANACONDA_HOME/bin/anaconda-navigator &
      ```
    - Sacar por tanto lo que Anaconda mete en el **.bashrc** y meterlo aquí. Darle permisos de ejecución y poner en **/usr/local/bin/anaconda-navigator**.
- # Actualización
  - Al menos en [[MacOS]] funciona con la siguiente instrucción
    - ```shell
      conda update anaconda
      ```