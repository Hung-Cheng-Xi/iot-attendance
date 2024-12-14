FROM ghcr.io/astral-sh/uv:latest as uv-stage

FROM python:3.12

WORKDIR /app

COPY --from=uv-stage /uv /bin/uv

RUN apt-get update && \
  apt-get install -y netcat-openbsd curl && \
  curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
  chmod +x wait-for-it.sh

COPY requirements.txt .
RUN uv pip install --system --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "./wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT -- alembic upgrade head && python main.py"]
