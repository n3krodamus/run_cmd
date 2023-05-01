
# RUN_CMD

Ejecucion automatizada de comandos utilizando kitty termina.
Download kitty: https://sw.kovidgoyal.net/kitty/

## Instalacion

```bash
git clone https://github.com/n3krodamus/run_cmd.git
cd run_cmd
./install.sh
```

Luego editar los archivos dentro del directorio conf

```bash
commands.txt                    ## Comandos a ejecutar en forma remota 
connection_command.txt          ## Comando para hacer la coneccion, ej ssh -p 
connection_init.txt             ## Se configura el prompt y variables de ambiente
disconnection_command.txt       ## Comando de desconeccion   
failed.txt                      ## Hosts a los que no pudo conectarse
hosts.txt                       ## Lista de hosts                                                                                                 
pending.txt                     ## Hosts restantes para completar la tarea en caso de interrupcion                                                                                                
processed.txt                   ## Hosts ya realizados

```

Configurar las variables de ambiente en .env

```bash

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

```



## Uso

```
./launch.sh
```
Se lanzara una instancia de kitty y quedara esperando para ejecutar el script run_cmd.py. Mientras este se encuentre en ejecucion la instancia de kitty lanzada tambien permanecera interactiva por si se desea realizar alguna correccion en caliente.

