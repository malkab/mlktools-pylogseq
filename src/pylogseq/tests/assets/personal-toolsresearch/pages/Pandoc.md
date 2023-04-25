- #procesar
- #Docker Existe un repositorio llamado **docker-latex** que contiene los programas para hacer un flujo de trabajo de texto [[LaTeX]], [[Markdown]] y [[Pandoc]]. Este repo genera una imagen Docker llamada **malkab/latex:latest** para trabajar con estas herramientas.
- # Publicación desde páginas de [[Logseq]]
  - Exportar el grafo como **Markdown** limpio, sin elementos de bloque (aunque esto no llega a ser así, se deja algunas marcas detrás).
  - Utilizar un contenedor **Docker de LaTeX**:
    - ```shell
      docker run -ti --rm \
          --name docs \
          --hostname docs \
          --user 1000:1000 \
          -v $(pwd):$(pwd) \
          -e "PATH=/usr/local/opt/coreutils/libexec/gnubin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/texlive/2021/bin/x86_64-linux" \
          --workdir $(pwd) \
          malkab/latex:latest \
          -c "./scripts/800-generar_documentacion.sh"
      ```
  - Utilizar un script de este corte:
    - ```shell
      pandoc -s --self-contained \
        -f md \
        -t pdf \
        --metadata title="Documentación" \
        ./docs/documentacion.md > ./docs/documentacion.pdf
      
      pandoc -s --self-contained \
        -f md \
        -t html \
        --metadata title="Documentación" \
        ./docs/documentacion.md > ./docs/documentacion.html
      ```
  -
- Explicación de **opciones comunes**
  collapsed:: true
  - **-f** y **-t** son las opciones estándar para indicar los formatos de entrada y salida
  - **-s** hace que Pandoc componga un HTML de un sólo fichero
  - **--self-contained** crea un fichero que incluye todos los assets
  - **--template** define la template a utilizar
- Pandoc usa la **plantilla por defecto** para componer el documento
  collapsed:: true
  - Para verla
    ```Shell
    pandoc -D html
    ```
- Transformar desde **GitHub Markdown** a **HTML**
  collapsed:: true
  - Comando
    ```Shell
     pandoc -s --self-contained \
       -f gfm \
       -t html \
       --metadata title="Documentación" \
       ../data/000_in/documentacion.md > ../data/900_out/documentacion.pdf
    ```
- Transformar desde **GitHub Markdown** a **PDF**
  collapsed:: true
  - Comando
    ```Shell
     pandoc -s --self-contained \
       -f gfm \
       -t pdf \
       --metadata title="Documentación" \
       ../data/000_in/documentacion.md > ../data/900_out/documentacion.pdf
    ```
- #procesar abajo
## From GitHub Markdown to PDF

This is a header that sets hyphenation properties and graphic insertion options:

```LaTeX
\exhyphenpenalty=10000 \hyphenpenalty=10000
\usepackage{graphicx}
\setkeys{Gin}{width=\linewidth}
```

Save this header to a file called __nohyphenation__ and put it in the same folder as de document. Set images at 300 DPI. Some more testing is to be done. Don't use cartographic lines that are too thin, they would not show up neatly at such resolutions.

```Shell
pandoc -s --include-in-header=nohyphenation -f markdown_github Final_Memory.md -o doc.pdf
```



## From GitHub Markdown to DOCX and ODT

```Shell
pandoc -s -f markdown_github -t docx Final_Memory.md -o doc.docx

pandoc -s -f markdown_github Final_Memory.md -o doc.odt
```
- #procesar Pandoc
  
  # Pandoc
  
  There is a repo called **text-workflows** that builds a Docker image with TexLive and Pandoc to work with LaTEX.
  
  To install from packages:
  
  ```Shell
  apt-get install pandoc texlive-fonts-recommended
  ```
  
  
  ## From GitHub Markdown to HTML
  
  Check the Markdown section for details.
## From GitHub Markdown to PDF

This is a header that sets hyphenation properties and graphic insertion options:

```LaTeX
\exhyphenpenalty=10000 \hyphenpenalty=10000
\usepackage{graphicx}
\setkeys{Gin}{width=\linewidth}
```

Save this header to a file called __nohyphenation__ and put it in the same folder as de document. Set images at 300 DPI. Some more testing is to be done. Don't use cartographic lines that are too thin, they would not show up neatly at such resolutions.

```Shell
pandoc -s --include-in-header=nohyphenation -f gfm Final_Memory.md -o doc.pdf
```


## From GitHub Markdown to Word DOCX and LibreOffice ODT

```Shell
pandoc -s -f gfm -t docx Final_Memory.md -o doc.docx

pandoc -s -f gfm Final_Memory.md -o doc.odt
```
## From LaTeX to Markdown

Just:

```Shell
pandoc -s example.tex -o example.md
```