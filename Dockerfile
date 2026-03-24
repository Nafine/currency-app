FROM python:3.12-alpine@sha256:7747d47f92cfca63a6e2b50275e23dba8407c30d8ae929a88ddd49a5d3f2d331 AS builder

LABEL stage=builder

COPY --from=ghcr.io/astral-sh/uv:0.10.12-python3.12-trixie@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/
COPY uv.lock pyproject.toml /app/

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

# Keep cache between rebuilds
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

FROM python:3.12-alpine@sha256:7747d47f92cfca63a6e2b50275e23dba8407c30d8ae929a88ddd49a5d3f2d331 AS runner

RUN apk add --no-cache  \
    tini=0.19.0-r3  \
    zlib=1.3.2-r0 && \
    addgroup -g 1001 currency-service &&  \
    adduser -u 1001 -S -D -G currency-service -h /home/currency-service currency-service

COPY --from=builder --chown=currency-service:currency-service /app /app
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

USER currency-service

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python3", "main.py"]
