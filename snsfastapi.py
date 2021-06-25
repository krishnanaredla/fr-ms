'''from fastapi import FastAPI
from typing import Dict,Any
app = FastAPI()
data = []

@app.post("/", status_code=201)
async def postData(payload:Dict[Any,Any]):
    data.append(payload)

@app.get("/data")
async def getData():
    return data'''

from flask import Flask, json,request

data = []

api = Flask(__name__)

@api.route('/', methods=['POST'])
def post_companies():
   data.append(request.data)
   return "Success"


@api.route('/data', methods=['GET'])
def get_companies():
  return {'data':str(data)}

if __name__ == '__main__':
    api.run(host='0.0.0.0',port=5000)

