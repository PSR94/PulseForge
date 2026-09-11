FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml README.md /app/
COPY apps/api /app/apps/api
RUN pip install --no-cache-dir .
EXPOSE 8000
CMD ["uvicorn", "pulseforge.main:app", "--app-dir", "apps/api", "--host", "0.0.0.0", "--port", "8000"]
