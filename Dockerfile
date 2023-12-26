FROM python:3.9.13

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install email-validator

ARG ENV_FILE=.env
RUN test -f $ENV_FILE && sed 's/^export //' $ENV_FILE | xargs -r -i echo export {} >> /etc/profile.d/project-env.sh || true

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]