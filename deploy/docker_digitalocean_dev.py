import subprocess
import re
import os
import time
import sh
import time
from docker_digitalocean_common import *
from docker_digitalocean_scraper import *

ssh_con_str = "root@174.138.58.1"

print "NOTICE: this script has to be run as a user with access to SSH keys."
print "Deployment to remote server (" + ssh_con_str + ") started."

ssh = sh.ssh.bake('-oStrictHostKeyChecking=no', ssh_con_str)

print "Successfully connected to remote server."

kill_and_remove_all_containers(ssh, 'alexa-air-dev-web-scraper')

copy_scraper_src_to_remote_host(ssh_con_str)
build_scraper_continer_in_remote_host(ssh)
run_scraper_container(ssh)





