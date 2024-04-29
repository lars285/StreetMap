import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse


app = FastAPI()

def connectDatabase():
    conn = psycopg2.connect(database = "street", 
                        user = "test", 
                        host= 'localhost',
                        password = "test",
                        port = 5432)
    return conn
    
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