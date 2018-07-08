#FROM ubuntu:latest
#FROM debian:jessie-slim
FROM ubuntu:trusty

# https://www.ekito.fr/people/run-a-cron-job-with-docker/

####################  PYTHON   ####################

RUN echo "$(lsb_release -sc)"

# Add the application resources URL
RUN echo "deb http://archive.ubuntu.com/ubuntu/ trusty main universe" >> /etc/apt/sources.list

# For https sources
RUN apt-get update && apt-get install -y apt-transport-https
RUN echo 'deb http://private-repo-1.hortonworks.com/HDP/ubuntu14/2.x/updates/2.4.2.0 HDP main' >> /etc/apt/sources.list.d/HDP.list
RUN echo 'deb http://private-repo-1.hortonworks.com/HDP-UTILS-1.1.0.20/repos/ubuntu14 HDP-UTILS main'  >> /etc/apt/sources.list.d/HDP.list
RUN echo 'deb [arch=amd64] https://apt-mo.trafficmanager.net/repos/azurecore/ trusty main' >> /etc/apt/sources.list.d/azure-public-trusty.list

RUN apt-get install rsyslog

# Update the sources list
RUN apt-get update \
  && apt-get install -y tar git curl nano wget dialog net-tools build-essential \
  && apt-get install -y python python-dev python-distribute python-pip \
  && apt-get install -y libxml2-dev libxslt-dev python-lxml 
 
#################### CRON STUF ####################

# Add crontab file in the cron directory
ADD src/scrape_air_polution_cron /etc/cron.d/scrape_air_polution_cron
RUN mkdir /scripts
ADD src/scrape_air_polution.py /scripts/scrape_air_polution.py
ADD src/requirements.txt /scripts/requirements.txt

RUN pip install -r /scripts/requirements.txt
 
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/scrape_air_polution_cron
 
# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# hack to make cron run https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=647193
RUN touch /etc/crontab /etc/cron.*/*
 
# Run the command on container startup   && tail -f /var/log/cron.log
CMD rsyslogd && cron -f -L15