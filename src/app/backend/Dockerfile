FROM python:3.10.9-slim as builder

ENV PATH /app/venv/bin:$PATH

WORKDIR /app

RUN apt update && apt install -y python3-pip gcc libc-dev libffi-dev
RUN pip install --upgrade pip && \
    pip3 install torch --extra-index-url https://download.pytorch.org/whl/cu118 && \
    pip3 install "ray[tune]"

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN useradd -m myuser
RUN chown -R myuser /app

USER myuser

COPY --chown=myuser:myuser . .

ENV BROKER_URI="redis://redis:6379/0"
ENV BACKEND_URI="redis://redis:6379/0"

ENV TRAIN_USERNAME="admin"
ENV TRAIN_PASSWORD="admin"

EXPOSE 8000

CMD ["bash", "run.sh"]