# 
FROM python:3.9

# 
WORKDIR /

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app.py /code/app.py

# 
CMD ["fastapi", "run", "code/app.py", "--port", "8000"]