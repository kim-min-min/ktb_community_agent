FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 전체 복사 (.env, app/, etc)
COPY . .

EXPOSE 8000

# app/main.py 안에 app = create_app() 형태일 때
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
