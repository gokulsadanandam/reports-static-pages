import json
import pdfkit
import boto3
import os
import platform
import uuid

# Get the bucket name environment variables to use in our code
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
client = boto3.client('s3',aws_access_key_id = AWS_ACCESS_KEY_ID , aws_secret_access_key = AWS_SECRET_ACCESS_KEY )
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

# make a db entry.
# return the s3 key and link to download pdf.

def generate_pdf():
    # check os type -> windows / linux -> set config , Html , Css and temp file accordingly.
    CurrentPlatform = platform.system()
    if (CurrentPlatform == 'Windows'):
        TempFilePath = 'out.pdf'
        WkhtmltopdfPath = os.getcwd() + '\\binary\\wkhtmltox-windows\\bin\\wkhtmltopdf.exe'
        HtmlTemplateFile = os.getcwd() + '\\reports-static-pages\\attendance-report\\attendance-report.html'
        CssFile = [  os.getcwd() + '/reports-static-pages/attendance-report/font.css' , os.getcwd() + '/reports-static-pages/attendance-report/attendance-report.css']
    else:
        TempFilePath = './temp/{key}'.format(key=key)
        WkhtmltopdfPath = os.getcwd() + '/binary/wkhtmltopdf/bin/wkhtmltopdf'
        HtmlTemplateFile = os.getcwd() + '/reports-static-pages/attendance-report/attendance-report.html'
        CssFile = [  os.getcwd() + '/reports-static-pages/attendance-report/font.css' , os.getcwd() + '/reports-static-pages/attendance-report/attendance-report.css' ]
    # generate_pdf from given html file and store in temp folder
    config = pdfkit.configuration(wkhtmltopdf=WkhtmltopdfPath)
    pdfkit.from_file(HtmlTemplateFile , TempFilePath , css = CssFile , configuration = config)

    # upload the pdf to s3 and get the key back.
    UniqueId = str(uuid.uuid4())
    client.upload_file(TempFilePath, S3_BUCKET_NAME , UniqueId , ExtraArgs =  { "ContentType" : "Application/pdf" })

generate_pdf()