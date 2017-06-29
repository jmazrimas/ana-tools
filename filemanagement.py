# import urllib.request
import urllib
import zipfile
import os
import json

def download_data(url, filename):
        urllib.urlretrieve(url, filename)
        print("Data Downloaded")

def unzip_directories():
    # zip_ref = zipfile.ZipFile("HOOPS.zip", 'r')
    zip_ref = zipfile.ZipFile("HOOPS.zip", 'r')
    zip_ref.extractall('./')
    zip_ref.close()

    zip_ref = zipfile.ZipFile("ModuleDLL.zip", 'r')
    zip_ref.extractall('./')
    zip_ref.close()

def get_credentials():
    local_directory = os.getcwd()
    local_directory = local_directory + "\\"

    creds = {}
    with open(local_directory+"credentials.json") as json_data:
        d = json.load(json_data)
        creds["access_key"] = d['accessKeyId']
        creds["secret_key"] = d['secretAccessKey']
    return creds

def upload_report(output_file, creds):

    import time
    timestamp = int(time.time())

    # save local dir
    # local_directory = os.getcwd()
    # local_directory = local_directory + "\\"

    # with open(local_directory+"credentials.json") as json_data:
    #     d = json.load(json_data)
    #     access_key = d['accessKeyId']
    #     secret_key = d['secretAccessKey']

    from boto.s3.connection import S3Connection
    conn = S3Connection(creds["access_key"], creds["secret_key"])

    # NEED NEW BUCKET
    bucket = conn.get_bucket('151602')

    from boto.s3.key import Key
    k = Key(bucket)
    file_name = str(timestamp)+'report.pdf'
    k.key = file_name
    k.set_contents_from_filename(output_file)

    signed_url = conn.generate_url(
           expires_in=1814400,
           method='GET',
           bucket='151602',
           key=k.key,
           query_auth=True
       )

    return signed_url