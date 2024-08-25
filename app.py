from typing import Annotated
import boto3
from fastapi import FastAPI, File, UploadFile
from dotenv import load_dotenv
import os 

load_dotenv()

app = FastAPI()

s3 = boto3.client('s3',
                    aws_access_key_id = os.getenv("ACCESS_KEY_ID"),
                    aws_secret_access_key = os.getenv("ACCESS_SECRET_KEY"),
                    )

BUCKET_NAME='s3-bucket-training'

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        if file:
            print(file.filename)
            s3.upload_fileobj(file.file, BUCKET_NAME, file.filename)
            return "file uploaded"
        else:
            return "error in uploading."
    except Exception as e:
        return e