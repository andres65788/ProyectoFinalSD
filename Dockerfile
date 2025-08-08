# Dockerfile para fragment_manager
FROM python:3.10-slim

WORKDIR /app
COPY fragment_manager.py ./

RUN pip install flask

EXPOSE 5001
CMD ["python", "fragment_manager.py"]