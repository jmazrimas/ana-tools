import urllib.request
import zipfile
import os
import json

def download_data(url, filename):
        urllib.request.urlretrieve(url, filename)
        print("Data Downloaded")

def unzip_directories():

    directory = os.fsencode('./')
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".zip"):
            zip_ref = zipfile.ZipFile(filename, 'r')
            if filename.startswith("TDP"):
                zip_ref.extractall('./TDPdata')
            else:
                zip_ref.extractall('./')
            zip_ref.close()
            continue
        else:
            continue

def upload_report(output_file):
    import time
    timestamp = int(time.time())

    with open('credentials.json') as json_data:
        d = json.load(json_data)
        access_key = d['accessKeyId']
        secret_key = d['secretAccessKey']

    from boto.s3.connection import S3Connection
    conn = S3Connection(access_key, secret_key)

    # NEED NEW BUCKET
    bucket = conn.get_bucket('151602')

    from boto.s3.key import Key
    k = Key(bucket)
    file_name = str(timestamp)+'output.dmi'
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