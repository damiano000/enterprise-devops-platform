FROM jenkins/jenkins:lts

USER root

# Installa Docker CLI
RUN apt-get update && \
    apt-get install -y docker.io

# Installa AWS CLI v2
RUN apt-get install -y curl unzip && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" && \
    unzip /tmp/awscliv2.zip -d /tmp && \
    /tmp/aws/install && \
    rm -rf /tmp/aws /tmp/awscliv2.zip

USER jenkins