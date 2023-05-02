#!/usr/bin/env bash

## Cread directorios
mkdir {tmp,logs}

## Virtual env
python -m venv venv

cat << 'EOF' > .env
PROCESSED_FILE='conf/processed.txt'
PENDING_FILE='conf/processed.txt'
FAILED_FILE='conf/processed.txt'
HOSTS_FILE='conf/hosts.txt'
COMMANDS_FILE='conf/commands.txt'
CONNECTION_COMMAND='conf/connection_command.txt'
CONNECTION_INIT='conf/connection_init.txt'
DISCONNECTION_COMMAND='conf/disconnection_command.txt'

FILE_LOG='logs/run.log'
KITTY_SOCKET='unix:/tmp/kitty-remote'
EOF


echo Instalado