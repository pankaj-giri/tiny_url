FROM python:3.8-slim as base_image

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM base_image AS app_build

COPY . ./

CMD [ "python", "app.py" ]