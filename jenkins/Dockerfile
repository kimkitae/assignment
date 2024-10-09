FROM jenkins/jenkins:lts

# 필요한 도구 설치
USER root
RUN apt-get update && apt-get install -y lsb-release
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce-cli

# Jenkins 사용자로 전환
USER jenkins

# 볼륨 마운트 설정
VOLUME /var/jenkins_home

# 포트 설정
EXPOSE 8080
EXPOSE 50000

# Jenkins 실행
CMD ["jenkins.sh"]
