from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
import snowflake_helper

app = FastAPI()


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")


def authenticate_user(username: str, password: str):
    if username == "admin" and password == "password":
        return True
    return False


@app.post("/token")
async def login_for_access_token(username: str, password: str):
    if not authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected/")
async def protected_route(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    return {"message": "You are authenticated!"}


def fetch_customer_data():
    query = "SELECT ID, FIRST_NAME, LAST_NAME FROM RAW.JAFFLE_SHOP.CUSTOMERS"
    connection = snowflake_helper.get_snowflake_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    customer_data = [{'ID': row[0], 'FIRST_NAME': row[1], 'LAST_NAME': row[2]} for row in results]
    return customer_data


customer_data = {customer['ID']: {'first_name': customer['FIRST_NAME'], 'last_name': customer['LAST_NAME']} for customer in fetch_customer_data()}


@app.get("/customer_info/")
async def get_customer_info(customer_id: int, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if customer_id not in customer_data:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer_data[customer_id]
