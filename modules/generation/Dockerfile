FROM python:3.7

# RUN apt-get update -y
# RUN apt-get install -y python3.10
# RUN apt-get install -y python3-pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN ls

COPY . .

# RUN gdown 1-WwbgGFprq9lxc6UZC-rGUQ4vGG8b-kS -O ckpts/best_ckpt_epoch=9_valid_loss=3.2331.ckpt

CMD ["python3", "src/api.py", "--mode=interact"]
# CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "3000"]
