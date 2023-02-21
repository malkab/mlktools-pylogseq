- #procesar

# Docker Guidelines

Volume policy:

- dev Composes always store their info in folders at the project's folder for persistence without risking losing info in Docker maintenance;

- SWARMS must use Docker volumes, stacks must be running when performing maintenance so information is not lost.
