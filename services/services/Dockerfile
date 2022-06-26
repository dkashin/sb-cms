FROM reg.tebox.eu/python-base:dev

WORKDIR /app

COPY *.py requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python", "/app/services.py"]
