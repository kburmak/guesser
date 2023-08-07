FROM python:latest

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN ["python3", "-c", "import nltk; nltk.download('stopwords', download_dir='/usr/local/nltk_data')"]
RUN ["python3", "-c", "import nltk; nltk.download('wordnet', download_dir='/usr/local/nltk_data')"]
RUN ["python3", "-c", "import nltk; nltk.download('punkt', download_dir='/usr/local/nltk_data')"]
COPY . .

CMD ["panel", "serve", "/app/webapp.py", "--address", "0.0.0.0", "--port", "7860", "--allow-websocket-origin", "guesser.onrender.com"]
