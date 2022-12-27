- #procesar

Python in Visual Studio Code
---
__TAGS:__ visual, studio, code, python

Install Python extension by Don Jayamanne. Configure environments:

- click Debug > Open configurations

- configure Python 2.7 and 3.6:

`JSON
{
	"name": "Python PhD preprocessor",
	"type": "python",
	"request": "launch",
	"stopOnEntry": false,
	"args": ["--boilerplate"],
	"pythonPath": "/usr/local/bin/python3.6",
	"program": "/Users/git/phd-writing/src/preprocessor/preprocessor.py",
	"cwd": "/Users/git/phd-writing/src/preprocessor",
	"env": {},
	"envFile": "${workspaceRoot}/.env",
	"debugOptions": [
		"WaitOnAbnormalExit",
		"WaitOnNormalExit",
		"RedirectOutput"
	],
	"args": [ "/Users/git", "/Users/malkab/sysgit" ]
},
{
	"name": "Python 2",
	"type": "python",
	"request": "launch",
	"stopOnEntry": true,
	"pythonPath": "/usr/local/bin/python2.7",
	"program": "${file}",
	"cwd": "${workspaceRoot}",
	"env": {},
	"envFile": "${workspaceRoot}/.env",
	"debugOptions": [
		"WaitOnAbnormalExit",
		"WaitOnNormalExit",
		"RedirectOutput"
	]
}
`

Configurations are stored project-wise, along with settings overriding global config settings, in a .vscode folder. Git this folder.

To run and debug, switch to the Debug section, select the desired configuration and run to your heart's content.


Configuring Tasks in Visual Studio Code
---
__TAGS:__ visual, studio, code, build, tasks

Tasks allow the launching of arbitrary commands (like build commands, or build command run inside a Docker container). There are many different, platforms specific tasks (to transpile TypeScript, for example), but there is also the wide spectrum shell tasks:

`JSON
{
	"taskName": "make pdf-introduccion",
	"type": "shell",
	"command": "build-commands/make_pdf-introduccion.sh",
	"group": {
		"kind": "build",
		"isDefault": true
	}
}
`

Tasks are stored in project's workspace in .vscode/tasks.json, so Git it.


Jupyter Notebooks in VS Code
---
__TAGS:__ visual, studio, code, jupyter, notebooks

Just:

`Python
# Model

#%%
# This is a cell
%matplotlib inline

import pandas as pd
import matplotlib as mpl, matplotlib.pyplot as plt, seaborn as sns

gravityPoints = pd.read_csv("Sevilla/src/csv/gravitational_point-pandas.csv")
portals = pd.read_csv("Sevilla/src/csv/portal-pandas.csv")


#%%
# This is another cell
sample = portals.sample(n=10000)

print(sample.count())
`
