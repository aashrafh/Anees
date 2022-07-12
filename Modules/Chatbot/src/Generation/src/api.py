import uvicorn
from typing import List
from pyngrok import ngrok
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from main import load_arz_model, load_msa_model


BASE_PATH = '/content/drive/MyDrive/anees'

print("Loading the ARZ model...")
arz = load_arz_model(f'{BASE_PATH}/data/chats', f'{BASE_PATH}/chats_monsoon_ckpts',
                     'best_ckpt_epoch=2_valid_loss=4.4047')

print("Loading the MSA model...")
msa = load_msa_model(f'{BASE_PATH}/data', f'{BASE_PATH}/translated_aragpt2_ckpts',
                     'best_ckpt_epoch=9_valid_loss=3.2331')

print("Setting up the API...")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


class Data(BaseModel):
    utter: str
    history: List[dict]


@app.get("/")
def hello():
    return {
        'response': "مرحبا، انا انيس"
    }


@app.post("/arz")
def arz_response(utter, history):
    resp = ''
    try:
        resp = arz.respond(utter, history)
    except:
        resp = 'انا مش قادر افهمك للاسف'
    return {
        'response': resp
    }


@app.post("/msa")
def msa_response(data: Data):
    resp = ''
    utter = data.utter
    history = data.history
    try:
        resp = msa.respond(utter, history)
    except:
        resp = 'لا استطيع فهمك. انا اسف'
    return {
        'response': resp
    }


ngrok_tunnel = ngrok.connect(8000)
print('Public URL:', ngrok_tunnel.public_url)
uvicorn.run(app, port=8000)
