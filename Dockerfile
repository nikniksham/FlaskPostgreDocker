FROM python:3.8

WORKDIR /app
COPY . .

RUN pip install -r requirement.txt

ENTRYPOINT ["python"]
CMD ["run.py"]