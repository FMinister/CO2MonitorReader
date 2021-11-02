
FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN pip install -r requirements.txt
RUN pip install git+https://github.com/heinemml/CO2Meter

COPY . .

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]

