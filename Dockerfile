FROM mcr.microsoft.com/playwright/python:v1.58.0-noble

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY . .

CMD ["uv", "run", "python", "main.py"]