import os
import subprocess
import psutil

def is_service_running(service_name):
    try:
        result = subprocess.run(["sc", "query", service_name], capture_output=True, text=True)
        return "RUNNING" in result.stdout
    except subprocess.SubprocessError:
        return False

def find_lol_client():
    for process in psutil.process_iter(['pid', 'name']):
        if "LeagueClientUx.exe" in process.info['name']:
            return process
    return None

def read_lockfile():
    client_process = find_lol_client()
    if client_process:
        base_folder = os.path.dirname(client_process.exe())
        lockfile_path = os.path.join(base_folder, "lockfile")
        try:
            with open(lockfile_path, "r") as file:
                data = file.read().strip().split(':')
                api_port = data[2]
                api_pwd = data[3]
                return api_port, api_pwd
        except FileNotFoundError:
            return None, None
        except IndexError:
            return None, None
    else:
        print("The League of Legends client is not running.")
        return None, None

def verify_replay_file(filepath):
    try:
        with open(filepath, "rb") as file:
            return file.read(4) == b"RIOT"
    except IOError:
        return False

def check_lol_client_running():
    if find_lol_client() is None:
        print("The League of Legends client is not running.")
        return False
    return True