FROM python:3.11.11
WORKDIR /mnt

COPY requirements.txt /mnt/requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends xclip && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt

EXPOSE 5000
VOLUME [ "/mnt/" ]
CMD ["python", "app.py"]
