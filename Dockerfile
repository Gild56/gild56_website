FROM python:3.11.11
WORKDIR /mnt

COPY requirements.txt /mnt/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000
VOLUME [ "/mnt/" ]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
