FROM python:3.7.5
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]