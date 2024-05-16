FROM python:3.9
WORKDIR /usr/src/app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY ./source ./
CMD ["fastapi", "run", "main.py", "--port", "8000"]

