FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir huggingface_hub aiohttp pydantic transformers

COPY scripts/ scripts/

ENV PYTHONPATH=/app/scripts

ENTRYPOINT ["python", "scripts/trainer_downloader.py"]
