FROM pypy:3.8

WORKDIR /app

COPY install.sh .
RUN ./install.sh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["pypy3", "main.py"]
