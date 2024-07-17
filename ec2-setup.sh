yum update
yum install docker -y
service docker start
usermod -a -G docker ec2-user
mkdir -p /usr/local/lib/docker/cli-plugins
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -oP '(?<=tag_name": "v)[^"]*')
curl -SL "https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-linux-x86_64" -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose