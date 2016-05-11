import random

from fabric.api import env, local
from fabric.contrib.files import append, exists, sed, run, sudo, settings

REPO_URL = 'https://github.com/Nuttycomputer/tdd.git'
env.key_filename = 'private_key.pem'


def provision():
    _install_dependencies()
    _install_virtualenv()


def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _nginx_config(source_folder, env.host)
    _upstart_config(source_folder, env.host)
    _start_services(env.host)


def _install_dependencies():
    sudo('apt-get install -y nginx git python3 python3-pip')


def _install_virtualenv():
    sudo('pip3 install virtualenv')


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % source_folder)
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % site_name
        )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % key)
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % virtualenv_folder)

    run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder,
        source_folder)
        )


def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % source_folder)


def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % source_folder)


def _nginx_config(source_folder, site_name):
    run('cd %s && '
        'sed "s/SITENAME/%s/g" '
        'deploy_tools/nginx.template.conf '
        '| '
        'sudo tee /etc/nginx/sites-available/%s' % (source_folder,site_name, site_name))

    if not exists('/etc/nginx/sites-enabled/%s' % site_name):
        sudo('ln -s /etc/nginx/sites-available/%s /etc/nginx/sites-enabled/%s' % (site_name, site_name))


def _upstart_config(source_folder, site_name):
    run('cd %s && sed "s/SITENAME/%s/g" \
    deploy_tools/gunicorn-upstart.template.conf | sudo tee \
    /etc/init/gunicorn-%s.conf' % (source_folder,site_name, site_name))


def _start_services(site_name):
    sudo('service nginx reload')
    with settings(warn_only=True):
        sudo('stop gunicorn-%s' % site_name)
    sudo('start gunicorn-%s' % site_name)
