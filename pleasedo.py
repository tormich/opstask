"""
TODO:

- Download 'https://s3.eu-central-1.amazonaws.com/devops-exercise/pandapics.tar.gz'

- Extract it's content to '/public/images' path.

- Create, build & run the App + DB using “docker-compose up” command.

- Check the App's health (See App's healthcheck below) at the end of the deployment flow
    and fail the deployment flow upon bad App health.
"""
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error

RESOURCES_TAR_URL = 'https://s3.eu-central-1.amazonaws.com/devops-exercise/pandapics.tar.gz'
DEFAULT_TEMP = '/tmp'


def download(url: str, save_as: str):
    try:
        a = urllib.request.urlretrieve(url, save_as)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'Can\'t download resources from {url}: "{e}"')


def extract(tar_path: str, extract_path: str):
    if not os.path.isdir(extract_path):
        os.makedirs(extract_path)

    args = ['tar', 'xvzf', tar_path, '-C', extract_path]
    try:
        subprocess.check_call(args=args)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f'Error while extracting resources from {tar_path} to {extract_path}: "{e}"')


def make_compose_yaml(app_path: str):
    db_path = os.path.join(app_path, 'db')
    return f'''
        version: '3'
        services:
          web:
            build: "{app_path}"
            ports:
             - "3000:3000"
          db:
            build: "{db_path}"'''


def docker_compose_up(yaml_dir):
    args = ['docker-compose', '<<', 'echo', f'"{yaml}"']
    try:
        subprocess.check_call(args=args)
    except subprocess.CalledProcessError as e:
        print(yaml)
        raise RuntimeError(f'Error while running docker-compose: "{e}"')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        app_path, temp_path = sys.argv[1], DEFAULT_TEMP
    elif len(sys.argv) == 3:
        app_path, temp_path = sys.argv[1:]
    else:
        raise AttributeError(
            f'Application path is missing. Please run: >> '
            f'"python {sys.argv[0]} /application/path [/tmp/path]"')

    timestamp = int(time.time())
    tar_path = os.path.join(temp_path, f'app-res-{timestamp}.tar.gz')
    download(url=RESOURCES_TAR_URL, save_as=tar_path)

    resources_path = os.path.join(app_path, 'public', 'images')
    extract(tar_path=tar_path, extract_path=resources_path)

    yaml_dir = os.path.join(temp_path, f'app-dc-{timestamp}')
    yaml_path = os.path.join(yaml_dir, 'docker_compose.yml')
    with open(yaml_path, 'w') as f:
        f.write(make_compose_yaml(app_path=app_path))
    docker_compose_up(yaml_path=yaml_path)

    print('Grate success!')
