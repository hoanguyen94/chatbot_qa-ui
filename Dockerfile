# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN pip3 install --no-cache-dir --upgrade pip

COPY . .

RUN find /app/lib -name __pycache__ -exec rm -rf {} \+

RUN pip3 install -r requirement.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "research-buddy.py"]