from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from m_database import User_token
import snowflake_helper as snowflake_helper
from pydantic import BaseModel

class Snowflake_data(BaseModel):
    email: str
    token: str

app = FastAPI()

@app.post("/get_data")
async def get_data_from_snowflake(payload:Snowflake_data):
    
    token_from_mongo = User_token.find_one({'email':payload.email.lower()})
    

    if not token_from_mongo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please login again')

    if (not token_from_mongo['token'] == payload.token) and datetime.utcnow().timestamp() <= float(token_from_mongo['expires_at']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide correct refresh token')
    customer_data = fetch_customer_data()

    return customer_data

def fetch_customer_data():
    connection = snowflake_helper.get_snowflake_connection()  
    cursor = connection.cursor()
    query = "SELECT ID, FIRST_NAME, LAST_NAME FROM RAW.JAFFLE_SHOP.CUSTOMERS"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    customer_data = [{'ID': row[0], 'FIRST_NAME': row[1], 'LAST_NAME': row[2]} for row in results]
    return customer_data

