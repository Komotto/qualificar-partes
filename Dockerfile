FROM registry.access.redhat.com/ubi9/ubi-minimal

RUN  microdnf install git -y

RUN  git clone https://gitlab.tjpa.jus.br/administracao-de-dados/datawarehouse.git
RUN  mkdir -p /app/datawarehouse/scripts
RUN  cp -r datawarehouse/scripts/ia-qualificarpartes /app/datawarehouse/scripts/

WORKDIR  /app

RUN  ls -R /app/datawarehouse/scripts/ia-qualificarpartes

COPY . .

#Instalar tools
RUN  microdnf install unzip -y
RUN  microdnf install wget -y

#Instalar Java correto para o projeto
RUN  wget https://download.oracle.com/java/17/archive/jdk-17.0.12_linux-x64_bin.rpm
RUN  rpm -ivh jdk-17.0.12_linux-x64_bin.rpm

#Instalar Python
RUN  microdnf install python3 python3-pip -y

RUN  pip3 install -r requirements.txt

#Instalar SQLcl
WORKDIR  /opt
RUN  wget https://download.oracle.com/otn_software/java/sqldeveloper/sqlcl-latest.zip
RUN  unzip sqlcl-latest.zip -d /opt
RUN  chmod -R a+rX /opt/sqlcl
RUN  ln -s /opt/sqlcl/bin/sql /usr/local/bin/sql
RUN  chmod a+x /usr/local/bin/sql
RUN  rm sqlcl-latest.zip

#Dependencias do Python
WORKDIR  /app/datawarehouse/scripts/ia-qualificarpartes/classificador

RUN ls -R /app

RUN  pip3 install fastapi uvicorn

#Permissões 
RUN  chmod -R g+rwX /app /opt/sqlcl
RUN  chmod +x /app/datawarehouse/scripts/ia-qualificarpartes/*.sh
RUN  chmod +x /app/datawarehouse/scripts/ia-qualificarpartes/classificador/*.sh
RUN  chmod +x /app/datawarehouse/scripts/ia-qualificarpartes/root.sh

RUN  microdnf clean all

EXPOSE  8080

WORKDIR /app

CMD  ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
