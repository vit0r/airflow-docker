"""Main
"""

from platform import system
from subprocess import run
from sys import argv

if __name__ == "__main__":
    print(f">>> sandbox airflow {argv[1]} <<<")
    DOCKER_PS = ["docker", "ps"]
    if argv[1] == "up":
        OS_NAME = system()
        if OS_NAME == "Linux":
            DOCKER_PS.insert(0, "watch")
        run(DOCKER_PS, check=False)
    else:
        run(DOCKER_PS, check=False)
