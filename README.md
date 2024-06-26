# Project background

The Projects is used to connect a Pothole Detection AI. The goal is visualize the detected pothols on a map, using different colors to indicate various types of potholes.

The Map looks like this:
![alt text](/README/map.png?raw=true)

## Environment variables

| Var         | Default   | Required | Description                  |
| ----------- | --------- | -------- | ---------------------------- |
| DOCS        | None      | No       | FastAPI Documentation        |
| REDOC       | None      | No       | FastAPI Documentation        |
| PG_DB       | test      | No       | PostgreSQL database Name     |
| PG_USER     | test      | No       | PostgreSQL database user     |
| PG_HOST     | localhost | No       | PostgreSQL database host     |
| PG_PASSWORD | test      | No       | PostgreSQL database password |
| PG_PORT     | 5432      | No       | PostgreSQL database port     |

# Hardware
- D1 mini Lite ESP8266
- Button
- GPS-Modul GY-NEO6MV2

For my project, I used a D1 mini Lite ESP8266. While you don't have to use this exact microcontroller, my code is compatible with it. The same applies to the GPS module; I used the GY-NEO6MV2.

## Wiring diagram
![alt text](/README/schaltplan.png?raw=true)