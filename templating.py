import jinja2

# [{
#     'AttendanceDate': Decimal('1597429800000'),
#     'SectionName': 'C',
#     'ClassName': 'XII',
#     'isDefault': True,
#     'Students': [{
#         'Attendance': True,
#         'StudentName': 'Gokul'
#     }, {
#         'Attendance': True,
#         'StudentName': 'Muri'
#     }, {
#         'Attendance': True,
#         'StudentName': 'Velu'
#     }],
#     'id': '0ca112f8-9393-47f7-b455-bf5528f6d762',
#     'email': 'gokulsadanandam@gmail.com'
# }, {
#     'AttendanceDate': Decimal('1597429800000'),
#     'SectionName': 'C',
#     'ClassName': 'XII',
#     'isDefault': True,
#     'Students': [{
#         'Attendance': True,
#         'StudentName': 'Gokul'
#     }, {
#         'Attendance': True,
#         'StudentName': 'Muri'
#     }, {
#         'Attendance': True,
#         'StudentName': 'Velu'
#     }],
#     'id': '1e087d54-96d8-4629-9c15-c1f6ae4d02d4',
#     'email': 'gokulsadanandam@gmail.com'
# }] 

def LoadJinjaConfigForAttendanceReport():
  templateLoader = jinja2.FileSystemLoader(searchpath="./reports-static-pages/attendance-report")
  templateEnv = jinja2.Environment(loader=templateLoader)
  TEMPLATE_FILE = "attendance-report.html"
  return templateEnv.get_template(TEMPLATE_FILE)




def generate_html_template():
	template = LoadJinjaConfigForAttendanceReport()
	op = template.render(headerlist=d,studentlist=a,contentlist=s)
