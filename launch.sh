#!/usr/bin/env bash

source ./.env
echo Lanzando Kitty terminal para control remoto...
nohup kitty -o allow_remote_control=yes --listen-on ${KITTY_SOCKET}  --title "Remote Command" --start-as normal > tmp/nohup.out &
sleep 2

read -p "Continuar ? (s/n)" ANSWER
if [[ ${ANSWER} == "s" ]]; then
  python main.py
else
  echo Termino
fi


