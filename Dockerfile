FROM python:3.9

WORKDIR .

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

# RUN python3 run.py

# CMD ["python3", "run.py"]

#ENTRYPOINT ["python"]
#COPY . /app
#ADD run.py /
#CMD ["python", "run.py", "--host=0.0.0.0"]
