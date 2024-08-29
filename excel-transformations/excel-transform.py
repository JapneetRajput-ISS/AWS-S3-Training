import pandas as pd
import boto3
from io import StringIO, BytesIO
from openpyxl import Workbook
from dotenv import load_dotenv
import os

load_dotenv()

s3 = boto3.client('s3',
                    aws_access_key_id = os.getenv("ACCESS_KEY_ID"),
                    aws_secret_access_key = os.getenv("ACCESS_SECRET_KEY"),
                    )

BUCKET_NAME='s3-bucket-training'

# Read excel file
# df = pd.read_csv('input.csv')
df = pd.read_excel("https://s3-bucket-training.s3.ap-south-1.amazonaws.com/Effects-of-COVID-19-on-trade-1-February-16-December-2020-provisional.xlsx")

# Rename Direction to Category
df.rename(columns={'Direction': 'Category'}, inplace=True)
print("Rename operation")
print(df.head())

# Check if Category values are either Imports or Exports
df = df.drop(df[(df['Category'] != "Imports") & (df['Category'] != "Exports")].index)
print("Category enum check operation")
print(df.head())

# Cast Current_Match to Date format
df["Current_Match"] = pd.to_datetime(df["Current_Match"], format="%d/%m/%Y")
# print("Date transformation")
# print(df.head())

# Sort values by Current_Match field
df = df.sort_values(by='Current_Match')
# print("Sort by Date")
# print(df.head())

# Aggregate sum value by Country
print(df.groupby(['Country'])['Value'].sum())

# Aggregate sum value by Commodity
print(df.groupby(['Commodity'])['Value'].sum())

# Create an in-memory Excel file
buffer = BytesIO()
# writer = pd.ExcelWriter(buffer, engine='openpyxl')

with pd.ExcelWriter(buffer, engine='openpyxl') as writer:  
    df.to_excel(writer, sheet_name='base')
    df.groupby(['Commodity'])['Value'].sum().to_excel(writer, sheet_name='avg')
    df.groupby(['Country'])['Value'].sum().to_excel(writer, sheet_name='sum')

# Reset the file pointer to the beginning
buffer.seek(0)

# Define your key
key = 'output.xlsx'
bucket_name = 's3-bucket-training'

# Upload the in-memory Excel file to S3
s3.put_object(Body=buffer.getvalue(), Bucket=bucket_name, Key=key)