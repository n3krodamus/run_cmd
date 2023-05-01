#!/usr/bin/env bash

## Cread directorios
mkdir {tmp,logs}

## Virtual env
python -m venv venv

## PIP3
pip3 install --upgrade pip
pip3 install -r requirements.txt

echo Instalado