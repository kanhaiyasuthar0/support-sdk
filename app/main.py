from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS for React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in prod
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PostgreSQL connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT", 5432)
)

class Ticket(BaseModel):
    name: str
    email: str
    message: str

@app.get("/")
def root():
    return {"message": "Support API is up!"}

@app.post("/submit-ticket")
def submit_ticket(ticket: Ticket):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO support_tickets (name, email, message) VALUES (%s, %s, %s)",
        (ticket.name, ticket.email, ticket.message),
    )
    conn.commit()
    cursor.close()
    return {"status": "success", "message": "Ticket submitted"}
