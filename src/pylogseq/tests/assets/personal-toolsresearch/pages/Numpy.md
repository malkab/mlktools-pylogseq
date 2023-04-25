- # Distribuciones de frecuencia aleatoria
  collapsed:: true
  - ```python
    s = 1000
    
    gum0 = np.random.gumbel(50, 10, s)
    poisson0 = np.random.poisson(5, s)
    logistic0 = np.random.logistic(70, 25, s)
    
    gum1 = np.random.gumbel(40, 8, s)
    poisson1 = np.random.poisson(2, s)
    logistic1 = np.random.logistic(100, 15, s)
    
    gum2 = np.random.gumbel(64, 12, s)
    poisson2 = np.random.poisson(4, s)
    logistic2 = np.random.logistic(84, 40, s)
    ```
- # Selección de los índices de un array que cumple una propiedad
  collapsed:: true
  - ```python
    left_indices = np.argwhere(X[node_indices,feature] == 1)[:,0].tolist()
    ```