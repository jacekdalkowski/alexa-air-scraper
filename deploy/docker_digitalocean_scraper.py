import os
from docker_digitalocean_common import *

def copy_scraper_src_to_remote_host(ssh_con_str):
	pwd = run_local_command("pwd").rstrip()
	local_dir = pwd + "/../*"
	print "Copying scraper src (" + local_dir + ") to remote host."
	os.system("scp -r " + local_dir + " " + ssh_con_str + ":/root/apps/alexa/air/dev/web/scraper")
	print "Copying scraper src to remote host finished."

def build_scraper_continer_in_remote_host(ssh):
	print "Building alexa-air-dev/web-scraper image in remote host."
	result = ssh("docker build -t alexa-air-dev/web-scraper /root/apps/alexa/air/dev/web/scraper")
	print "Building alexa-air-dev/web-scraper image in remote host result: "
	print result

def run_scraper_container(ssh):
	print "Starting alexa-air-dev/web-scraper container in remote host."
	result = ssh("docker run -d --name alexa-air-dev-web-scraper --link alexa-air-dev-web-db:air-db alexa-air-dev/web-scraper")
	print "Starting alexa-air-dev/web-scraper container in remote host result: "
	print result


