FROM reg.tebox.eu/python-base:dev

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY *.mmdb ./
COPY *.py ./

CMD ["python", "/app/georesolver.py"]
