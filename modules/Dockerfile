FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3.10
RUN apt-get install zip -y
RUN apt-get install unzip -y
RUN apt-get update && apt-get install -y python3-pip 


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# WORKDIR /modules

# Models
RUN gdown --id 1UQcByqwmp0qrybipC3r4mNDiQumCF9mX
RUN unzip models.zip

# Data
RUN gdown --id 1tl2nmpfp6-V4WQmEhQSyrxGFGDm5wYbW
RUN unzip data.zip

COPY . .

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]
# CMD [ "python3", "app.py"]