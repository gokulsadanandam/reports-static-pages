import json
import os
import pdfkit
import uuid
import boto3
import platform

AWS_ACCESS_KEY_ID = os.environ.get('AccessKeyId')
AWS_SECRET_ACCESS_KEY = os.environ.get('SecretAccessKey')
client = boto3.client('s3',aws_access_key_id = AWS_ACCESS_KEY_ID , aws_secret_access_key = AWS_SECRET_ACCESS_KEY )
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
CurrentPlatform = platform.system()

def lambda_handler(event, context):
    UniqueId = str(uuid.uuid4())

    # check os type -> windows / linux -> set config , Html , Css and temp file accordingly.
    if (CurrentPlatform == 'Windows'):
        TempFilePath = 'out.pdf'
        WkhtmltopdfPath = os.getcwd() + '\\binary-windows\\wkhtmltox-windows\\bin\\wkhtmltopdf.exe'
        HtmlTemplateFile = os.getcwd() + '\\reports-static-pages\\attendance-report\\attendance-report.html'
        CssFile = [  os.getcwd() + '/reports-static-pages/attendance-report/font.css' , os.getcwd() + '/reports-static-pages/attendance-report/attendance-report.css']
    else:
        TempFilePath = '/tmp/{key}'.format(key=UniqueId)
        WkhtmltopdfPath = '/opt/bin/wkhtmltopdf'
        HtmlTemplateFile = os.getcwd() + '/reports-static-pages/attendance-report/attendance-report.html'
        CssFile = [  os.getcwd() + '/reports-static-pages/attendance-report/attendance-report.css' ]
    # generate_pdf from given html file and store in temp folder
    config = pdfkit.configuration(wkhtmltopdf=WkhtmltopdfPath)
    pdfkit.from_file(HtmlTemplateFile , TempFilePath , css = CssFile , configuration = config)
    
    # upload the pdf to s3 and get the key back.
    client.upload_file(TempFilePath, S3_BUCKET_NAME , UniqueId , ExtraArgs =  { "ContentType" : "Application/pdf" })
    s3File = 'https://{}.s3.ap-south-1.amazonaws.com/{}'.format(S3_BUCKET_NAME,UniqueId)
    return {
        "message" : "saved to s3 bucket" ,
        "s3FileUrl": s3File
    }


if (CurrentPlatform == 'Windows'):
	lambda_handler(False,False)