FROM python:3.12-alpine AS builder

LABEL stage=builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY uv.lock pyproject.toml ./

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

FROM python:3.12-alpine

RUN apk update && apk add --no-cache tini && \
    addgroup -g 1001 nonroot &&  \
    adduser -u 1001 -S -D -G nonroot -h /home/nonroot nonroot

COPY --from=builder --chown=nonroot:nonroot /app /app
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

USER nonroot

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python3", "main.py"]