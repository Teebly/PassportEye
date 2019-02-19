FROM teebly/pyocr-public 
# base image is in teebly/pyocr


RUN apt-get update && apt-get install -y tesseract-ocr
COPY . /usr/src/app
RUN pip install gunicorn flask
RUN pip install -e .

WORKDIR /usr/src/app
ENV PORT="3008"
ENV PYTHONPATH="."
EXPOSE 3008

CMD gunicorn --worker-class sync --threads 1 --workers 1  --bind 0.0.0.0:3008 passporteye.server
