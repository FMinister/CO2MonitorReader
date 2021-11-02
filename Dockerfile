
FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install git+https://github.com/heinemml/CO2Meter

COPY . .

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]

