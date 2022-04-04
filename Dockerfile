FROM python:latest
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src .


#CMD [ "python", "./your-daemon-or-script.py" ]