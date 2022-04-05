FROM python:latest
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src .
ENTRYPOINT python init_prod.py
CMD [ "python", "./main.py" ]