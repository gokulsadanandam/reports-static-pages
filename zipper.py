from zipfile import ZipInfo, ZipFile, ZIP_DEFLATED 
import os

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_name = os.path.join(root, file)
            zip_info = ZipInfo(file_name)
            zip_info.compress_type = ZIP_DEFLATED
            zip_info.create_system = 3 # Specifies Unix
            zip_info.external_attr = 0o777 << 16 # Sets chmod 777 on the file
            ziph.write(file_name) # You have to write the file contents in with ZipInfo

def zipfilesindirectory(path,ziph):
    abs_src = os.path.abspath(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            absname = os.path.abspath(os.path.join(root, file))
            arcname = absname[len(abs_src) + 1:]
            ziph.write(absname, arcname)   

def fix_zip():
 
    list_of_file_names = ['handler.py']
    list_of_folders = ['reports-static-pages','binary\\wkhtmltopdf\\bin']
    list_of_files_in_folder = ['site-packages']
    zip_file_name = 'aws-html-to-pdf-package.zip'
 
    zip_file = ZipFile(zip_file_name, 'w', compression=ZIP_DEFLATED)
 
    for file_name in list_of_file_names:
        zip_info = ZipInfo(file_name)
        zip_info.compress_type = ZIP_DEFLATED
        zip_info.create_system = 3 # Specifies Unix
        zip_info.external_attr = 0o777 << 16 # Sets chmod 777 on the file
        f = open(file_name,"r")
        zip_file.writestr(zip_info, f.read()) # You have to write the file contents in with ZipInfo
    
    for folders in list_of_folders:
        zipdir(folders,zip_file)

    for folders in list_of_files_in_folder:
        zipfilesindirectory(folders,zip_file)

    zip_file.close()


fix_zip()