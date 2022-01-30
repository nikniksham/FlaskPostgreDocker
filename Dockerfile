FROM python:3.9

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

#ENTRYPOINT ["python"]
EXPOSE 5000
COPY . /app
#ADD run.py /
#CMD ["python", "run.py", "--host=0.0.0.0"]