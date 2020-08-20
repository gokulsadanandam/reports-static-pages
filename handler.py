import json
import os
import pdfkit
import uuid
import boto3
import platform
import time
import jinja2

AWS_ACCESS_KEY_ID = os.environ.get('AccessKeyId')
AWS_SECRET_ACCESS_KEY = os.environ.get('SecretAccessKey')
client = boto3.client('s3',aws_access_key_id = AWS_ACCESS_KEY_ID , aws_secret_access_key = AWS_SECRET_ACCESS_KEY )
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
CurrentPlatform = platform.system()
_max_chunk_size_ = 7
dynamodb = boto3.resource('dynamodb',aws_access_key_id = AWS_ACCESS_KEY_ID , aws_secret_access_key = AWS_SECRET_ACCESS_KEY , region_name  = 'ap-south-1')
from boto3.dynamodb.conditions import Key, Attr

def generate_html_pdf(file,cover):
    UniqueId = str(uuid.uuid4())

    # check os type -> windows / linux -> set config , Html , Css and temp file accordingly.
    if (CurrentPlatform == 'Windows'):
        TempFilePath = 'out2.pdf'
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
    # return pdfkit.from_string(html,TempFilePath,configuration = config)
    pdfkit.from_file(file , TempFilePath , cover = cover , css = CssFile , configuration = config)
    return 
    # upload the pdf to s3 and get the key back.
    client.upload_file(TempFilePath, S3_BUCKET_NAME , UniqueId , ExtraArgs =  { "ContentType" : "Application/pdf" })
    s3File = 'https://{}.s3.ap-south-1.amazonaws.com/{}'.format(S3_BUCKET_NAME,UniqueId)
    return {
        "message" : "saved to s3 bucket" ,
        "s3FileUrl": s3File
    }

def get_attenance_data_by_class_and_date(classname='XII',section='C',daterange=[1596220200000,1597516100000]):
    table = dynamodb.Table('AttendanceRegister')
    response = table.scan(
        # KeyConditionExpression=Key('email').eq('gokulsadanandam@gmail.com') & Key('ClassName').eq(classname) ,
        FilterExpression=Attr('ClassName').eq(classname) & Key('email').eq('gokulsadanandam@gmail.com') & Key('AttendanceDate').gt(daterange[0]) & Key('AttendanceDate').lt(daterange[1]) 
    )
    return response['Items']

classname = "XII"
sectionname = "C"
startdate = 1597429800000
enddate = 1597429886400

attendancelist = [{
    'AttendanceDate': 1597429800000,
    'SectionName': 'C',
    'ClassName': 'XII',
    'isDefault': True,
    'Students': [{
        'Attendance': True,
        'StudentName': 'Gokul'
    }, {
        'Attendance': True,
        'StudentName': 'Muri'
    }, {
        'Attendance': True,
        'StudentName': 'Velu'
    }],
    'id': '0ca112f8-9393-47f7-b455-bf5528f6d762',
    'email': 'gokulsadanandam@gmail.com'
},{
    'AttendanceDate': 1597517100000,
    'SectionName': 'C',
    'ClassName': 'XII',
    'isDefault': True,
    'Students': [{
        'Attendance': True,
        'StudentName': 'Gokul'
    }, {
        'Attendance': False,
        'StudentName': 'Muri'
    }, {
        'Attendance': True,
        'StudentName': 'Velu'
    }],
    'id': '0ca112f8-9393-47f7-b455-bf5528f6d762',
    'email': 'gokulsadanandam@gmail.com'
},
{
    'AttendanceDate': 1597619200000,
    'SectionName': 'C',
    'ClassName': 'XII',
    'isDefault': True,
    'Students': [{
        'Attendance': True,
        'StudentName': 'Gokul'
    }, {
        'Attendance': True,
        'StudentName': 'Muri'
    }, {
        'Attendance': False,
        'StudentName': 'Velu'
    }],
    'id': '0ca112f8-9393-47f7-b455-bf5528f6d762',
    'email': 'gokulsadanandam@gmail.com'
},
{
    'AttendanceDate': 1597705600000,
    'SectionName': 'C',
    'ClassName': 'XII',
    'isDefault': True,
    'Students': [{
        'Attendance': True,
        'StudentName': 'Gokul'
    }, {
        'Attendance': True,
        'StudentName': 'Muri'
    }, {
        'Attendance': False,
        'StudentName': 'Velu'
    }],
    'id': '0ca112f8-9393-47f7-b455-bf5528f6d762',
    'email': 'gokulsadanandam@gmail.com'
},
{
    'AttendanceDate': 1,
    'SectionName': 'C',
    'ClassName': 'XII',
    'isDefault': True,
    'Students': [{
        'Attendance': True,
        'StudentName': 'Gokul'
    }, {
        'Attendance': True,
        'StudentName': 'Muri'
    }, {
        'Attendance': False,
        'StudentName': 'Velu'
    }],
    'id': '0ca112f8-9393-47f7-b455-bf5528f6d762',
    'email': 'gokulsadanandam@gmail.com'
},
{
    'AttendanceDate': 1598705600000,
    'SectionName': 'C',
    'ClassName': 'XII',
    'isDefault': True,
    'Students': [{
        'Attendance': True,
        'StudentName': 'Gokul'
    }, {
        'Attendance': True,
        'StudentName': 'Muri'
    }, {
        'Attendance': False,
        'StudentName': 'Velu'
    }],
    'id': '0ca112f8-9393-47f7-b455-bf5528f6d762',
    'email': 'gokulsadanandam@gmail.com'
},
{
    'AttendanceDate': 1599705600000,
    'SectionName': 'C',
    'ClassName': 'XII',
    'isDefault': True,
    'Students': [{
        'Attendance': True,
        'StudentName': 'Gokul'
    }, {
        'Attendance': True,
        'StudentName': 'Muri'
    }, {
        'Attendance': False,
        'StudentName': 'Velu'
    }],
    'id': '0ca112f8-9393-47f7-b455-bf5528f6d762',
    'email': 'gokulsadanandam@gmail.com'
},
{
    'AttendanceDate': 1600705600,
    'SectionName': 'C',
    'ClassName': 'XII',
    'isDefault': True,
    'Students': [{
        'Attendance': True,
        'StudentName': 'Gokul'
    }, {
        'Attendance': True,
        'StudentName': 'Muri'
    }, {
        'Attendance': True,
        'StudentName': 'Velu'
    }],
    'id': '0ca112f8-9393-47f7-b455-bf5528f6d762',
    'email': 'gokulsadanandam@gmail.com'
},
{
    'AttendanceDate': 1601705600000,
    'SectionName': 'C',
    'ClassName': 'XII',
    'isDefault': True,
    'Students': [{
        'Attendance': True,
        'StudentName': 'Gokul'
    }, {
        'Attendance': True,
        'StudentName': 'Muri'
    }, {
        'Attendance': True,
        'StudentName': 'Velu'
    }],
    'id': '0ca112f8-9393-47f7-b455-bf5528f6d762',
    'email': 'gokulsadanandam@gmail.com'
},
{
    'AttendanceDate': 1603705600000,
    'SectionName': 'C',
    'ClassName': 'XII',
    'isDefault': True,
    'Students': [{
        'Attendance': True,
        'StudentName': 'Gokul'
    }, {
        'Attendance': True,
        'StudentName': 'Muri'
    }, {
        'Attendance': True,
        'StudentName': 'Velu'
    }],
    'id': '0ca112f8-9393-47f7-b455-bf5528f6d762',
    'email': 'gokulsadanandam@gmail.com'
},
{
    'AttendanceDate': 1605033000000,
    'SectionName': 'C',
    'ClassName': 'XII',
    'isDefault': True,
    'Students': [{
        'Attendance': True,
        'StudentName': 'Gokul'
    }, {
        'Attendance': True,
        'StudentName': 'Muri'
    }, {
        'Attendance': True,
        'StudentName': 'Velu'
    }],
    'id': '0ca112f8-9393-47f7-b455-bf5528f6d762',
    'email': 'gokulsadanandam@gmail.com'
}] 

def timeformatter(epoch):
    return time.strftime('%d-%m-%y', time.localtime(epoch/1000))


def LoadJinjaConfigForAttendanceReport(file):
  templateLoader = jinja2.FileSystemLoader(searchpath="./reports-static-pages/attendance-report")
  templateEnv = jinja2.Environment(loader=templateLoader)
  TEMPLATE_FILE = file
  return templateEnv.get_template(TEMPLATE_FILE)

def generate_cover_page(file):
    template = LoadJinjaConfigForAttendanceReport(file)
    templateHtmlString  = template.render(classname=classname,sectionname=sectionname,startdate=timeformatter(startdate),enddate=timeformatter(enddate))
    if (CurrentPlatform == 'Windows'):
        templateHtmlFilePath = 'temp-file-cover.html'
        templateHtmlFile = open(templateHtmlFilePath,"w")
        templateHtmlFile.write(templateHtmlString)
        templateHtmlFile.close()
    else:
        templateHtmlFilePath = '/tmp/report-file-cover-{key}.html'
        templateHtmlFile =  open(templateHtmlFilePath.format(key=str(uuid.uuid4())),"w")
        templateHtmlFile.write(templateHtmlString)
        templateHtmlFile.close()
    return templateHtmlFilePath


def break_dict_logic(dictionary,size=8):
    limit = 0
    dict_list = []
    temp_dict = {} 
    for items in dictionary:
        if (limit == 8):
            limit = 0
            dict_list.append(temp_dict)
            temp_dict = {}
        limit = limit + 1
        temp_dict[items] = dictionary[items]
    dict_list.append(temp_dict)
    return dict_list

def generate_html_template(file):
    headerlist = []
    studentlist = []
    studentattendancedict = {}
    contentlist = {}

    for i in range(0,len(attendancelist)):
        studentattendancedict = {}
        timestring = timeformatter(attendancelist[i]['AttendanceDate'])
        headerlist.append(timestring)
        for j in range(0,len(attendancelist[i]['Students'])):
            studentlist.append(attendancelist[i]['Students'][j]['StudentName'])
            studentattendancedict[attendancelist[i]['Students'][j]['StudentName']] = attendancelist[i]['Students'][j]['Attendance'] 
        contentlist[timestring] = studentattendancedict
    
    headerlist = sorted(list(set(headerlist)))
    studentlist = sorted(list(set(studentlist)))
    template = LoadJinjaConfigForAttendanceReport(file)
    headerlistchunks = [headerlist[i: i + _max_chunk_size_] for i in range(0, len(headerlist) , _max_chunk_size_ )]
    templateHtmlString  = template.render(headerlist=headerlistchunks,studentlist=studentlist,contentlist=contentlist)
    if (CurrentPlatform == 'Windows'):
        templateHtmlFilePath = 'temp-file.html'
        templateHtmlFile = open(templateHtmlFilePath,"w")
        templateHtmlFile.write(templateHtmlString)
        templateHtmlFile.close()
    else:
        templateHtmlFilePath = '/tmp/report-file-{key}.html'
        templateHtmlFile =  open(templateHtmlFilePath.format(key=str(uuid.uuid4())),"w")
        templateHtmlFile.write(templateHtmlString)
        templateHtmlFile.close()
    return templateHtmlFilePath

if __name__ == '__main__':
    cover_page_html = generate_cover_page("attendance-report.html")
    attendance_report_html = generate_html_template("reports-table.html")
    # print (attendance_report_html)
    generate_html_pdf(attendance_report_html,cover_page_html)        
