FROM python:3.11-slim
RUN apt-get update && apt-get install -y nodejs npm
WORKDIR /app

COPY front ./front
RUN cd front && npm ci && npm run build

COPY end ./end
WORKDIR /app/end
RUN pip install -r requirements.txt

RUN mkdir -p static && cp -r ../front/dist/* ./static/
EXPOSE 5000
CMD ["python", "app.py"]