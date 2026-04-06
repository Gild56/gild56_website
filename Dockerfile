FROM python:3.11.11

WORKDIR /mnt

COPY requirements.txt /mnt/requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
