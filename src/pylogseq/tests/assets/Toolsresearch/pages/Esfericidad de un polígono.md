- #Math Esfericidad de un polígono #procesar
  - ```txt
    
    Sphericity of a Polygon
    
    =======================
    
    **__TAGS:__** sphericity, polygons
    
    It is the proportion between the perimeter of the polygon and that of a circle the same area as the polygon.
    
    Perimeter of a circle:
    
        pc = 2 pi r
    
    Area of a circle:
    
        ac = pi r²
    
    The areas of both the polygon and the circle must be the same:
    
        ac = ap = pi r²
    
    Let's express the perimeter of the circle based on the area of the polygon:
    
        (pc)² = (2 pi r)² = 4 pi² r² = 4 pi (pi r²) = 4 pi ap
    
        pc = 2 sqrt(pi ap)
    
    This is the perimeter of the circle based on known area of the polygon. Now, ratio between the perimeter of the circle and that of the polygon:
    
        sphericity = (2 sqrt(pi ap)) / pp
    
    If the polygon is a circle:
    
        sphericity = (2 sqrt(pi (pi r²))) / (2 pi r) =
    
        (2 sqrt(pi² r²)) / (2  pi r) = (2 pi r) / (2 pi r) = 1
    
    So, rounded polygons tend to have sphericity of 1, irregular ones, tend to have it near 0.
    
    ```