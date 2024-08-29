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
        print(file.filename)
        s3.upload_fileobj(file.file, BUCKET_NAME, file.filename)
        return "file uploaded"
    except Exception as e:
        return e
    
# Lambda with API Gateway -> Step function (lambda) -> ECS -> SNS -> 
# tasks/01H27THKWKQG6KDF1SMGZ3S03P/input/AMG-MF LMS-Territory Map-20230127.txt