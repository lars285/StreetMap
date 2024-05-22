import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os

docs_url = os.getenv('DOCS', None)
redoc_url = os.getenv('REDOC', None)

app = FastAPI(docs_url=docs_url, redoc_url=redoc_url)


database = os.getenv('PG_DB', 'test')
user = os.getenv('PG_USER', 'test')
host = os.getenv('PG_HOST', 'localhost')
password = os.getenv('PG_PASSWORD', 'test')
port = os.getenv('PG_PORT', 5432)

def connectDatabase():
    conn = psycopg2.connect(database = database, 
                        user = user, 
                        host= host,
                        password = password,
                        port = port)
    return conn
    
conn = connectDatabase()
cur = conn.cursor()
cur.execute("""DO $$
            BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname  = 'damage') THEN
            CREATE TYPE damage AS ENUM ('D00', 'D10', 'D20', 'D40');
            END IF;
            END$$;""")

cur.execute("""CREATE TABLE IF NOT EXISTS OpenStreetMap(
            id SERIAL PRIMARY KEY,
            lat VARCHAR (50)  NOT NULL,
            long VARCHAR (50) NOT NULL,
            imageName VARCHAR (60) NOT NULL,
            damage damage NOT NULL
            );
            """)

conn.commit()
cur.close()
conn.close()

class Item(BaseModel):
    lat: float
    long: float
    imagename: str
    damage: str

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/image/{image_id}")
def read_root(image_id: str):
    return FileResponse('images/' + image_id)

@app.post("/gps")
async def create_item(item: Item):
    conn = connectDatabase()
    cur = conn.cursor()
    cur.execute("INSERT INTO OpenStreetMap(lat, long, imagename, damage) VALUES(%s, %s, %s, %s)", (item.lat, item.long, item.imagename, item.damage))
    conn.commit()
    cur.close()
    return "ok"

@app.get("/marker/{damage}")
def read_root(damage: str): # D10, D20
    damages = {
        "D00": "gruen-marker.png",
        "D10": "gelb-marker.png",
        "D20": "blau-marker.png",
        "D40": "rot-marker.png"
    }
    return FileResponse('markers/' + damages[damage])


@app.get("/points")
async def getpoints():

    message = []
    conn = connectDatabase()
    cur = conn.cursor()
    cur.execute('SELECT * FROM OpenStreetMap;')
    rows = cur.fetchall()
    for row in rows:
        message.append({"lat": row[1], "long": row[2], "imageName": row[3], "damage": row[4]})
    conn.commit()
    conn.close()
    return message