FROM python:3.10

RUN addgroup --system --gid 10000 app && \
    adduser --system --uid 10000 --ingroup app app

ENV CLIENT_ID=${CLIENT_ID}
ENV SECRET_TOKEN=${SECRET_TOKEN} 

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /app /app

USER app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]