import threading
import queue
import time
import subprocess
import re

q = queue.Queue()
kitty_socket = "unix:/tmp/mykitty"

## kittys
# "kitty", "@", "send-text", "--from-file "
# "kitty", "@", "--to", "unix:/tmp/mykitty", "send-text", c, "\n"
# "kitty", "@", "--to", "unix:/tmp/mykitty", "get-text"


def worker():
    while True:
        item = q.get()
        print(f'Working on {item[0]}')
        if not connect_host(item[0]):
            print(f"No fue posible conectarse a:{item[0]}")
        else:
            print(f"Conectado al host: {item[0]}")

            for command in item[1]:
                run_command(command)

        print('Finalizado')
        q.task_done()


def run_command(c):
    try:
        kitty = subprocess.run(
            ["kitty", "@", "--to", kitty_socket, "send-text", c, "\n"],
            encoding='utf8',
            timeout=10,
            check=True,
            stdout=True,
            stderr=True)

    except subprocess.TimeoutExpired as exc:
        print(f"Process timed out.\n{exc}")
        print(kitty.stderr)

    except subprocess.CalledProcessError as exc:
        print(f"Process failed because did not return a successful return code.")
        print(f"Returned {exc.returncode}\n{exc}")


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
    match = re.search(h + '_RUN_CMD', kitty)

    if not match:
        return False
    return True


def connect_host(h):
    connectionSequence = ['ssh -p2022 ' + h, 'export TERM=xterm', 'clear', 'PS1="\h_RUN_CMD:>"']

    for command in connectionSequence:
        run_command(command)
        time.sleep(5)

    if not verify_host(h):
        return False






if __name__ == "__main__":
    hosts_file = 'hosts.txt'
    commands = ['ls -l /opt', 'echo "desinstalado" > /tmp/uninstall.txt', 'exit']

    threading.Thread(target=worker, daemon=True).start()

    with open(hosts_file) as file:
        for line in file:
            line = line.rstrip('\n')  # preprocess line
            q.put((line, commands))

    # Block until all tasks are done.
    q.join()
    print('All work completed')
