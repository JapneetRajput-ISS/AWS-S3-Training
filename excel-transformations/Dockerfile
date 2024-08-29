# 
FROM python:3.9

# 
WORKDIR /

COPY ./ /code

# 
# COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
# COPY ./excel-transform.py /code/app.py

# 
CMD ["python", "code/excel-transform.py"]