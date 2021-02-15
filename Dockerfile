FROM python:3-alpine
WORKDIR /youtubehandybot
COPY . .
RUN apk add gcc python3-dev build-base libffi-dev
RUN pip install --no-cache-dir -r requirements.txt
CMD python bot.py