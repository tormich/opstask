"""
TODO:

- Download 'pics.tar.gz'

- Extract it's content to '/public/images' path.

- Create, build & run the App + DB using “docker-compose up” command.

- Check the App's health (See App's healthcheck below) at the end of the deployment flow
    and fail the deployment flow upon bad App health.
"""
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error


DEFAULT_TEMP = '/tmp'
HEALTH_URL = 'http://localhost:3000/health'


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


def make_compose_yaml(app_path: str, out_path: str):
    db_path = os.path.join(app_path, 'db')
    yaml = f'''
        version: '3'
        services:
          web:
            build: "{app_path}"
            ports:
             - "3000:3000"
          db:
            build: "{db_path}"
            ports:
             - 27017:27017
            '''

    with open(out_path, 'w') as f:
        f.write(yaml)


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

        except Exception as e:
            print(f'health check #{attempt+1} failed: "{e}"')

    return False


if __name__ == '__main__':
    if len(sys.argv) == 3:
        resources_tar_url, app_path = sys.argv[1:]
        temp_path = DEFAULT_TEMP
    elif len(sys.argv) == 4:
        resources_tar_url, app_path, temp_path = sys.argv[1:]
    else:
        raise AttributeError(
            f'Application path or tar url missing. Please run: >> '
            f'python {sys.argv[0]} "https://tar-url" "/application/path" ["/tmp/path"]')

    timestamp = int(time.time())
    tar_path = os.path.join(temp_path, f'app-res-{timestamp}.tar.gz')
    download(url=resources_tar_url, save_as=tar_path)

    resources_path = os.path.join(app_path, 'public', 'images')
    extract(tar_path=tar_path, out_path=resources_path)

    yaml_dir = os.path.join(temp_path, f'app-dc-{timestamp}')
    yaml_path = os.path.join(yaml_dir, 'docker_compose.yml')
    os.makedirs(yaml_dir)

    make_compose_yaml(app_path=app_path, out_path=yaml_path)
    docker_compose_up(yaml_dir=yaml_dir)

    if health_check(HEALTH_URL, attempts=3):
        print('Grate success!')
    else:
        raise RuntimeError('Health check failed.')
