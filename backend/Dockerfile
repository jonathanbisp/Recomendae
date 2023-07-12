FROM python:3.11.3 AS build-image

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.11.3-slim

WORKDIR /app
EXPOSE 3000

COPY --from=build-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./src /app

ENTRYPOINT ["uvicorn", "main:app", "--port", "3000", "--host", "0.0.0.0"]
