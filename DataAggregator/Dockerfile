FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY API.py main.py

# DB connection strings — override at runtime via -e or docker-compose env
ENV MATERIALS_DB_URL=mongodb://admin:toor@localhost:27018/
ENV SUPPLIERS_DB_URL=mongodb://admin:toor@localhost:27019/
ENV ORDERS_DB_URL=mongodb://admin:toor@localhost:27016/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]