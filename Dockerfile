# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY . .

#
RUN apt-get update -y && apt-get install -y gcc npm



# install dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r /app/requeriments.txt

RUN npm install pm2 -g

COPY simulador_Video_Analysis/ simulador_Video_Analysis/
EXPOSE 5007
#CMD [ "pm2", "start Simulador.py –interpreter python3 --name  Suspicious-Activity"]
ENTRYPOINT ["bash", "/app/entrypoint.sh"]