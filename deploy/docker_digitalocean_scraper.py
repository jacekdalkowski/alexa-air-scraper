import os
from docker_digitalocean_common import *

def copy_scraper_src_to_remote_host(ssh_connection_string, deploy_dir):
	pwd = run_local_command("pwd").rstrip()
	local_dir = pwd + "/../*"
	print "Copying scraper src (" + local_dir + ") to remote host."
	os.system("scp -r " + local_dir + " " + ssh_connection_string + ":" + deploy_dir)
	print "Copying scraper src to remote host finished."

def build_scraper_continer_in_remote_host(ssh, tag, build_dir):
	print "Building " + tag + " image in remote host."
	result = ssh("docker build -t " + tag + " " + build_dir)
	print "Building " + tag + " image in remote host result: "
	print result

def run_scraper_container(ssh, image_tag, db_container_name, name):
	print "Starting " + image_tag + " container in remote host."
	result = ssh("docker run -d --name " + name + " --link " + db_container_name + ":air-db " + image_tag)
	print "Starting " + image_tag + " image in remote host result: "
	print result


