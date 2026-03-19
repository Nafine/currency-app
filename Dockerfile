FROM alpine:3.14

#Install python3
RUN apk update && apk add \
    python3 && \
    addgroup -g 1001 -S nonroot && \
    adduser -u 1001 -S -D -G nonroot -h /home/nonroot nonroot

#Install uv
COPY --from=ghcr.io/astral-sh/uv:0.10.11 /uv /uvx /bin/
ENV UV_NO_DEV=1

RUN uv sync --locked

COPY . /app
WORKDIR /app

USER nonroot

EXPOSE $PORT

CMD ["uv", "run", "main.py"]