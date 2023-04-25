- Superutilidad para la conversión de vídeo.
- # Recetas
  - Convertir desde [[webm]] a [[mp4]]. webm es el formato en el que escribe la capturadora de pantalla incorporada con Ubuntu:
    - ```shell
      ffmpeg \
          -i in.webm \
          -vcodec libx264 \
      	-vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" \
          -r 24 \
      	-y -an \
          video.mp4
      ```