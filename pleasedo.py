import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error

DEFAULT_TEMP = '/tmp'
HEALTH_URL = 'http://localhost:3000/health'

FILE_URL = 'https://s3.eu-central-1.amazonaws.com/devops-exercise/pandapics.tar.gz'
DOCKER_COMPOSE_YAML_DIR = '.'
APP_PATH = './ops-exercise/'
TEMP_PATH = './tmp/'


def download(url: str, save_as: str):
    try:
        urllib.request.urlretrieve(url, save_as)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'Can\'t download resources from {url}: "{e}"')


def extract(tar_path: str, out_path: str):
    if not os.path.isdir(out_path):
        os.makedirs(out_path)

    args = ['tar', 'xvzf', tar_path, '-C', out_path]
    try:
        subprocess.check_call(args=args)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f'Error while extracting resources from {tar_path} to {out_path}: "{e}"')


def docker_compose_up(yaml_dir):
    build_cmd = 'docker-compose build'
    up_cmd = ['docker-compose', 'up']
    try:
        subprocess.check_call(args=build_cmd, cwd=yaml_dir, shell=True)
        subprocess.Popen(args=up_cmd, cwd=yaml_dir, shell=False, stdout=subprocess.DEVNULL)

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f'Error while running docker-compose: "{e}"')


def health_check(url: str, attempts: int = 3) -> bool:
    for attempt in range(0, attempts):
        time.sleep(5)
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                result = json.loads(response.read())
                if all([result['isSuccessful'],
                        result['checkDatabase']['success'],
                        result['checkDisk']['success']]):
                    return True
                else:
                    raise ValueError(f'bad response from health end-point {result}')
        except Exception as e:
            print(f'health check #{attempt+1} failed: "{e}"')

    return False


if __name__ == '__main__':
    timestamp = int(time.time())
    tar_path = os.path.join(TEMP_PATH, f'app-res-{timestamp}.tar.gz')

    print(f'Downloading "{FILE_URL}"')
    download(url=FILE_URL, save_as=tar_path)

    resources_path = os.path.join(APP_PATH, 'public', 'images')

    print(f'Extracting images to "{resources_path}"')
    extract(tar_path=tar_path, out_path=resources_path)

    docker_compose_up(yaml_dir=DOCKER_COMPOSE_YAML_DIR)

    if not health_check(HEALTH_URL, attempts=3):
        print(f'Health check failed.')
        exit(1)
    else:
        print('Grate success!')
