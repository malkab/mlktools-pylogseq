#!/bin/bash

pipx uninstall pylogseq
pipx install dist/pylogseq-0.0.1-py3-none-any.whl
pipx inject pylogseq typer arrow pandas marko rich pyyaml