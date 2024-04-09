FROM python:3.11-buster as base

RUN apt-get update && apt-get install libpq5 -y

ENV VIRTUAL_ENV=/opt/venv 

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m venv ${VIRTUAL_ENV}

RUN pip install -U pip setuptools wheel build

FROM base as builder

COPY ./requirements.txt /app/requirements.txt

RUN --mount=type=cache,target=/opt/pip_cache pip install -Ur /app/requirements.txt

FROM base as runtime

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY ./*.py /app/

WORKDIR /app/

CMD ["uvicorn","api:app","--host","0.0.0.0","--port","8000"]