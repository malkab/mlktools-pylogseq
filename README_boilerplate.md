# Boilerplate for Python Programs

This is the boilerplate to create Python standalone programs, like CLI utilities.


# Management of Virtualenv

Just:

```shell
# Activate
. virtualenv/bin/activate

# List packages
pip list

# Deactivate
deactivate
```


# Publishing Workflow

Steps:

- [] check for **print("D:** left behind;

- [] review changes with Git to get a clear idea of changes in the current version, but don't commit yet;

- [] close the **Git Flow Feature** and go back to **develop**, if any. Get a clear idea of changes in the current version;

- [] if applicable, create a new **Git Flow Release**;

- [] push all branches and tags to **GitHub**:

```Shell
# This will push ALL branches to origin, even the non-existant ones. Remove sporious branches with git push origin :branch_name
git push --all origin
git push --tags
git fetch -av --prune
git branch -av
```


# DVC Operations

Most used DVC operations:

```shell
dvc status
dvc add data
dvc move old_file_name new_file_name
dvc commit
dvc push
dvc pull
```
