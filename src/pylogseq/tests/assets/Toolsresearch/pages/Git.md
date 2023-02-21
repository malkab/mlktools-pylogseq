- #procesar
- **Generalidades**
  collapsed:: true
  - **NO** meter repos Git en [[Dropbox]], la cosa se vuelve rara.
- Operaciones con branches
  - ```shell
    # Crear una nueva rama desde la actual
    git checkout -b branch_name
    
    # Fetch remote branches info
    git fetch -av
    
    # Check a branch from a remote and track it
    git checkout -t origin/remote-branch-name
    
    # To change the name of the local branch on checkout (be careful)
    git checkout -b local-branch-name origin/remote-branch-name
    
    # Delete remote branches (and their local counterpart)
    git push origin :branchtodelete
    git fetch --prune
    
    # Delete local branches
    git branch [ -D / -d ] branchname
    
    # To check all branches, local and remote tracked
    # Branches are not pulled, however
    git branch -av
    
    # To check diff between branches
    git diff [ branch name ]
    git difftoom [ branch name ]
    
    # Hacer que una rama local siga a una rama del remoto
    git push -u origin [ branch name ]
    ```
- **Operaciones con tags**
  collapsed:: true
  - ```shell
    # Añadir una etiqueta
    git tag etiqueta
    
    # Borrar una etiqueta local
    git tag -d etiqueta
    
    # Borrar una etiqueta remota
    git push origin :etiqueta
    
    # Listar etiquetas
    git tag
    ```
- **Borrando commits**
  collapsed:: true
  - ```shell
    # Completely trash last commits (WARNING!!!)
    # First, make sure what you're trashing
    # Then, git reset, where X is the number of commits to be trashed
    # (1 will trash the last one, 2 the two last ones, etc.)
    git log
    git reset --hard HEAD~X
    ```
- Ver el **grafo** de commits
  collapsed:: true
  - ```shell
    git log --graph
    ```