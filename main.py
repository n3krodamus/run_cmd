import threading
import queue
import time
import subprocess
import re
import logging
import sys
import os

from dotenv import load_dotenv

#q = queue.Queue()
#kitty_socket = "unix:/tmp/mykitty"
#error_flag = False


## kittys
# "kitty", "@", "send-text", "--from-file "
# "kitty", "@", "--to", "unix:/tmp/mykitty", "send-text", c, "\n"
# "kitty", "@", "--to", "unix:/tmp/mykitty", "get-text"

def worker():
    global error_flag

    while True:
        item = q.get()
        logging.info(f'--Iniciando task en {item[0]}')

        if error_flag:
            # dump host on pending file
            dump_host(item[0],pending_file)
            logging.debug('Error flag seteado con anterioridad')
        else:
            connect_host(item[0])

            if verify_host(item[0]):
                logging.info(f"Conectado al host: {item[0]}")
                for command in item[1]:
                    logging.info(f'Ejecutando comando:{command}')
                    ## Lanza el comando y verifica si termina ok
                    if run_verify_command(command) == 'error':
                        logging.error(f'Finalizo con error el comando: {command}')
                        break
                    time.sleep(5)
                # Disconnect
                logging.info('Desconectando')
                disconnect(item[0])

                # dump host on procesed_file
                dump_host(item[0],processed_file)
            else:
                error_flag = True
                logging.info("No conectado")
                # dump host on failed_file
                dump_host(item[0],failed_file)

        logging.info('--Task finalizada')
        q.task_done()


def dump_host(h,f):
    print(f"Voy a escribir {h} en :{f}")
    with open(f, "a") as status_file:
        status_file.write(f'{h}\n')


def run_verify_command(c):
    command =  c + ' || echo RUN_CMD_ERROR'
    run_command(command)
    time.sleep(2)
    if not last_command_ok():
        return 'error'

def last_command_ok():
    kitty = read_screen()
    if re.search('^RUN_CMD_ERROR', kitty, flags=re.MULTILINE):
        return False
    return True



def run_command(c):
    try:
        kitty = subprocess.run(
                ["kitty", "@", "--to", kitty_socket, "send-text", c, "\n"],
                encoding='utf8',
                timeout=10,
                check=True,
                stderr=True,
                stdout=True)

    except subprocess.TimeoutExpired as exc:
        logging.error(f"Process timed out.\n{exc}")
        logging.debug(kitty.stderr)

    except subprocess.CalledProcessError as exc:
        print("ERROR")
        logging.info(f"Process failed because did not return a successful return code.")
        logging.info(f"Returned {exc.returncode}\n{exc}")


def read_screen():
    k = subprocess.run(
        ["kitty", "@", "--to", kitty_socket, "get-text"],
        encoding='utf8',
        timeout=10,
        check=True,
        capture_output=True)
    return(k.stdout)


def verify_host(h):
    kitty = read_screen()
    if not re.search(h + '_RUN_CMD', kitty):
        return False
    return True



def connect_host(h):
    connection = read_file(connection_command)
    connection_sequence = read_file(connection_init)

    for command in connection:
        run_command(command + " " + h)
        time.sleep(5)

    for command in connection_sequence:
        run_command(command)
        time.sleep(2)

def disconnect(h):
    disconnection = read_file(disconnection_command)
    for command in disconnection:
        run_command(command)
        time.sleep(5)

def read_file(f):
    with open(f) as file:
        data = [line.strip() for line in file]
    return(data)


if __name__ == "__main__":
    # Conf files
    conf = load_dotenv('.env')
    processed_file = os.getenv("PROCESSED_FILE")
    pending_file = os.getenv("PENDING_FILE")
    failed_file = os.getenv("FAILED_FILE")
    hosts_file = os.getenv("HOSTS_FILE")
    connection_command = os.getenv("CONNECTION_COMMAND")
    disconnection_command = os.getenv("DISCONNECTION_COMMAND")
    connection_init = os.getenv("CONNECTION_INIT")

    file_log = os.getenv("FILE_LOG")
    kitty_socket = os.getenv("KITTY_SOCKET")

    # Array de comandos
    commands = ['echo hola mundo', 'lalalalala','echo continuo']
    error_flag = False

    # Start queue object
    q = queue.Queue()

    # Start logging
    logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    # Define the thread
    threading.Thread(target=worker, daemon=True).start()

    # Start
    logging.info('Starting process')
    hosts = read_file(hosts_file)
    for line in hosts:
        q.put((line, commands))


    # Block until all tasks are done.
    q.join()
    logging.info('All work completed')

