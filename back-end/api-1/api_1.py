from fastapi import FastAPI, Depends, HTTPException, Response, UploadFile, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
import hashlib
import requests
from uuid import uuid4
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import magic
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    aws_access_key_id= os.getenv("aws_access_key_id"),
    aws_secret_access_key= os.getenv("aws_secret_access_key")
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

file_details=[]

app = FastAPI() 

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")


def authenticate_user(username: str, password: str):
    if username == "admin" and password == "password":
        return True
    return False

token=""
user_name=""

@app.post("/token")
async def login_for_access_token(username: str, password: str):
    if not authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    global token, user_name
    token = access_token
    user_name = username
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/see")
async def see():
    return [os.getenv("SECRET_KEY"), os.getenv("aws_access_key_id"), os.getenv("aws_secret_access_key")]

AWS_Bucket = 'file-storage-assignment-4'
s3 = boto3.resource('s3')
bucket = s3.Bucket(AWS_Bucket)

supported_file_types={
    'application/pdf': 'pdf'
}

async def s3_upload(contents: bytes, key: str, folder: str):
    s3_client = boto3.client('s3',
    aws_access_key_id= os.getenv("aws_access_key_id"),
    aws_secret_access_key= os.getenv("aws_secret_access_key"))
    full_key = os.path.join(folder, key)
    s3_client.put_object(Bucket="file-storage-assignment-4", Key=full_key, Body=contents)


def check_s3_connection():
    try:
        s3_client = session.client('s3')
        print("Connected to S3 successfully")
        return True
    except NoCredentialsError:
        print("Credentials not found")
        return False
    except ClientError as e:
        print(f"Connection error: {e}")
        return False
    
def check_exists(file_md5):
    if file_details==[]:
        return False
    else:
        for each in file_details:
            each["md5"] == file_md5
            return True
        
@app.post('/see_details')
async def see_details():
    return(file_details)

@app.post('/check_connection')
async def see_details_connection():
    return(check_s3_connection())

@app.post('/upload')
async def upload(file: UploadFile):
    if token != "": 
        decoded_token = decode_token(token)
        current_user = decoded_token.get("sub")
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Operation is not authorized"
        )
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No file found!'
        )
    contents = await file.read()
    size = len(contents)

    file_type = magic.from_buffer(buffer=contents, mime=True)
    if file_type not in supported_file_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Unsupported file type'
        )
    result = str((hashlib.md5(contents)).digest())
    if check_exists(result) == True:
        return {"details": "file already exists"}
    else:
        unique_identifier = uuid4()
        file_name = f'{unique_identifier}.{supported_file_types[file_type]}'
        await s3_upload(contents=contents, key=file_name, folder='raw_pdf_files/')
        s3_location = "s3://" + AWS_Bucket + "/" + "raw_pdf_files/"+file_name
        details = {
            "user_name": current_user,
            "file_name": file.filename,
            "unique_identifier": unique_identifier,
            "md5": result
        }
        file_details.append(details)
        return {'s3 location': s3_location, "md5": result}


AIRFLOW_API_BASE_URL = "http://airflow-server:8080/api/v1"

@app.post('trigger_airflow')
async def trigger_dag(s3_location: str):
    if token != "": 
        decoded_token = decode_token(token)
        current_user = decoded_token.get("sub")
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Operation is not authorized"
        )
    endpoint = f"{AIRFLOW_API_BASE_URL}/dags/dagRuns"
    data = {
        "conf": {"s3_location": s3_location}, 
        "execution_date": "now"
    }
    response = requests.post(endpoint, json=data)
    if response.status_code == 200:
        return {"message": "DAG triggered successfully"}
    else:
        return {"error": "Failed to trigger DAG"}
    