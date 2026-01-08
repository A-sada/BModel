FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND=Agg

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} appuser \
    && useradd -m -u ${UID} -g ${GID} -s /bin/bash appuser \
    && chown -R appuser:appuser /app

USER appuser

CMD ["python", "MODEL/VRPTW-main.py", "--input-dir", "datefile"]
