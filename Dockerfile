FROM rockylinux:9
RUN dnf update -y
RUN dnf install python3.11 -y
RUN dnf install python3.11-pip -y
WORKDIR /SniffOsu
ADD . /SniffOsu
RUN pip3.11 install -r requirements.txt
WORKDIR /SniffOsu/src
ENTRYPOINT ["python3.11", "manage.py", "runserver", "0.0.0.0:9000"]