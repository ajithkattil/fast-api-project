FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
  && apt-get install -y --no-install-recommends libpq5 \
  && rm -rf /var/lib/apt/lists/*

ARG GEMFURY_TOKEN
ENV GEMFURY_TOKEN=${GEMFURY_TOKEN}

WORKDIR app/

COPY dist/recipes_api-*.whl .

RUN pip install --extra-index-url https://${GEMFURY_TOKEN}@pypi.fury.io/freshrealm-team --no-cache-dir recipes_api-*.whl

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
