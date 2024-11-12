import boto3
from botocore.exceptions import ClientError
from flask import current_app
import PyPDF2
from docx import Document as DocxDocument
from PIL import Image
import io

def upload_file_to_s3(file, bucket_name, object_name):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
    )
    try:
        s3_client.upload_fileobj(file, bucket_name, object_name)
    except ClientError as e:
        current_app.logger.error(f"Error uploading file to S3: {e}")
        return False
    return True

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_document_content(s3_key, bucket_name):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
    )
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        file_content = response['Body'].read()

        if s3_key.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfFileReader(io.BytesIO(file_content))
            content = [pdf_reader.getPage(i).extract_text() for i in range(pdf_reader.numPages)]
        elif s3_key.endswith('.docx'):
            doc = DocxDocument(io.BytesIO(file_content))
            content = [paragraph.text for paragraph in doc.paragraphs]
        elif s3_key.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image = Image.open(io.BytesIO(file_content))
            content = image
        else:
            content = file_content.decode('utf-8')

        return content
    except ClientError as e:
        current_app.logger.error(f"Error retrieving file from S3: {e}")
        return None
