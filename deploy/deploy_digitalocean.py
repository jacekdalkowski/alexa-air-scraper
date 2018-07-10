import subprocess
import re
import os
import time
import sh
import time
from docker_digitalocean_common import *
from docker_digitalocean_scraper import *
from docker_digitalocean_config import config
import sys


if __name__ == '__main__':
	deployment_info = None
	env = sys.argv[1]

	if env == 'dev':
		env_config = config['dev']
	elif env == 'prod1':
		env_config = config['prod1']
	elif env == 'prod2':
		env_config = config['prod2']
	else:
		raise "No config for env: " + env

	ssh_con_str = env_config['ssh_con_str']

	print "NOTICE: this script has to be run as a user with access to SSH keys."
	print "Deployment to remote server (" + ssh_con_str + ") started."

	ssh = sh.ssh.bake('-oStrictHostKeyChecking=no', ssh_con_str)

	print "Successfully connected to remote server."

	kill_and_remove_all_containers(ssh, env_config['container_name'])

	copy_scraper_src_to_remote_host(ssh_con_str, env_config['deploy_dir'])
	build_scraper_continer_in_remote_host(ssh, env_config['image_tag'], env_config['deploy_dir'])
	run_scraper_container(ssh, env_config['image_tag'], env_config['db_container_name'], env_config['container_name'])





