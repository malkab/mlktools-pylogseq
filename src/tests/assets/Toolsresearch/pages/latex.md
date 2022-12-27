- #procesar Latex

# LaTeX

The image **text-workflows** installs the full TeX Live ISO image.



## TeX Live

To handle TeX Live, there is an application called **tlmgr** that is the
package manager for the system. Some recipes:

```shell
# Full list of packages, installed or not
tlmgr info

# Info, including version, about a package
tlmgr info [package name]

# List of updatable packages
tlmgr update --list
```
