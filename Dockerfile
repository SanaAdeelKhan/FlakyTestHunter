FROM node:22-slim

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv curl && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://bob.ibm.com/download/bobshell.sh | bash -s -- --pm npm

WORKDIR /app
COPY backend/requirements.txt .
RUN pip3 install --break-system-packages -r requirements.txt

COPY backend/ .

EXPOSE 10000
CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
