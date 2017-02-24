from fabric.api import (
    cd,
    env,
    put,
    run,
    sudo,
    task
)


PRODUCTION_IP = '54.154.235.243'
PROJECT_DIRECTORY = '/home/ubuntu/ztm/'
COMPOSE_FILE = 'compose-production.yml'


@task
def production():
    env.run = sudo
    env.hosts = [
        'ubuntu@' + PRODUCTION_IP + ':22',
    ]


def create_project_directory():
    run('mkdir -p ' + PROJECT_DIRECTORY)


def update_compose_file():
    put('./' + COMPOSE_FILE, PROJECT_DIRECTORY)


@task
def deploy():
    create_project_directory()
    update_compose_file()
    with cd(PROJECT_DIRECTORY):
        env.run('docker-compose -f ' + COMPOSE_FILE + ' pull')
        env.run('docker-compose -f ' + COMPOSE_FILE + ' up -d')
