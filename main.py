from json import JSONEncoder
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mistralai import *
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from enum import Enum
from pathlib import Path
import base64
import tempfile
import requests

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

API_KEY = os.getenv("MISTRAL_API_KEY")

# Modelo que permite OCR
model = "mistral-ocr-latest"

client = Mistral(api_key=API_KEY)

class Document(BaseModel):
    Name: str
    DocumentType: str
    DocumentNumber: str
    SeemsValid: bool


class StructuredOCR(BaseModel):
    FileName: str 
    OcrContents: Document

class ValidateRequest(BaseModel):
    image_path: str

@app.get("/")
async def root():
    return {"message": "API Furia"}

@app.post("/validate")
async def validate(request: ValidateRequest) -> StructuredOCR:
    temp_file = None
    try:
        # Detecta se é URL
        if request.image_path.startswith("http://") or request.image_path.startswith("https://"):
            response = requests.get(request.image_path)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Falha ao baixar a imagem da URL.")
            suffix = os.path.splitext(request.image_path)[1]
            if suffix.lower() not in [".jpg", ".jpeg", ".png"]:
                raise HTTPException(status_code=400, detail="Formato do arquivo não suportado. Formatos suportados: jpg, jpeg, png")
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            temp_file.write(response.content)
            temp_file.close()
            image_file = Path(temp_file.name)
        else:
            image_file = Path(request.image_path)
            if not image_file.is_file():
                raise HTTPException(
                    status_code=500, 
                    detail={"data": "Arquivo não  encontrado."}
                )
            if not image_file.suffix.lower() in [".jpg", ".jpeg", ".png"]: 
                raise HTTPException(
                    status_code=400, 
                    detail=f"Formato do arquivo não suportado. Formatos suportados: jpg, jpeg, png"
                )

        encoded_image = base64.b64encode(image_file.read_bytes()).decode()
        base64_data_url = f"data:image/jpeg;base64,{encoded_image}"

        image_response = client.ocr.process(
            document=ImageURLChunk(image_url=base64_data_url),
            model="mistral-ocr-latest"
        )

        image_ocr_markdown = image_response.pages[0].markdown

        chat_response = client.chat.parse(
            model="pixtral-12b-latest",
            messages=[
                {
                    "role": "user",
                    "content": [
                        ImageURLChunk(image_url=base64_data_url),
                        TextChunk(text=(
                            f"This is the image's OCR in markdown:\n{image_ocr_markdown}\n.\n"
                            "Convert this into a structured JSON response "
                            "with the OCR contents in a sensible dictionnary\n"
                            "Also return a boolean field 'seemsValid' that indicates if the picture has a document structure pattern."
                            )
                        )
                    ]
                }
            ],
            response_format=StructuredOCR,
            temperature=0
        )
        return chat_response.choices[0].message.parsed
    finally:
        if temp_file is not None:
            try:
                os.unlink(temp_file.name)
            except Exception:
                pass

@app.get("/ping")
async def ping():
    try:
        chat_response = client.chat.complete(
            model= model,
            temperature=0.1,
            messages = [
                {
                    "role": "user",
                    "content": "Forma comum de testar apis, eu mando ping e voce responde pong",
                },
            ]
        )
        return chat_response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))