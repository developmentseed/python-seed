#!/bin/bash
su -l ec2-user
yum update -y
yum install -y python37
yum install -y python-pip
yum install -y git
yum install -y docker
usermod -a -G docker ec2-user
curl -L https://github.com/docker/compose/releases/download/1.9.0/docker-compose-`uname -s`-`uname -m` | sudo tee /usr/local/bin/docker-compose > /dev/null
isharp-core
chmod +x /usr/local/bin/docker-compose
service docker start
chkconfig docker on
yum update -y
cd ~ec2-user
git clone https://github.com/jeremycward/isharp-core.git
export PYTHONPATH = /home/ec2-user/isharp-core
