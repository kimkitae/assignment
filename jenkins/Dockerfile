FROM jenkins/jenkins:lts

# Allure 설치
USER root
RUN apt-get update && apt-get install -y wget unzip
RUN wget https://github.com/allure-framework/allure2/releases/download/2.18.1/allure-2.18.1.zip && \
    unzip allure-2.18.1.zip -d /opt/ && \
    ln -s /opt/allure-2.18.1/bin/allure /usr/bin/allure && \
    rm allure-2.18.1.zip

# Allure 서비스 설정
RUN mkdir -p /allure-results /allure-reports
VOLUME ["/allure-results", "/allure-reports"]

# Allure 서비스 실행 스크립트 추가
COPY allure-service.sh /usr/local/bin/allure-service.sh
RUN chmod +x /usr/local/bin/allure-service.sh

# tini 설치
RUN apt-get update && apt-get install -y tini

# Jenkins 사용자로 전환
USER jenkins

# Allure 서비스 실행
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/bin/bash", "-c", "/usr/local/bin/allure-service.sh & /usr/local/bin/jenkins.sh"]