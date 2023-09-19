import csv
import io
import os
import sys
import traceback
import requests
import json
from optparse import OptionParser
#1gNI2zy7cavlCor4_IsJdHqTJSy-U89aR
 
CLIENT_ID="xxxx.apps.googleusercontent.com"
REFRESH_TOKEN="1//xxxxx"
CLIENT_SECRET="Gxxxx"


AUTH_URL="https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}&grant_type=refresh_token"



def upload_file_to_gdrive(filename,folderid,filedescription,filetype):
    payload={}
    headers = {}
    url = AUTH_URL.format(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,refresh_token=REFRESH_TOKEN)
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    response_json = response.json()

    access_token = response_json["access_token"]
      url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&convert=true"

    payload={}

    if folderid :
        filemetadata = {
                "name" : filename,
                "description" : filedescription if filedescription else "Test File",
                "parents" : [folderid],
                "mimeType" : filetype if filetype else "application/vnd.google-apps.spreadsheet"
        }
    else :
         filemetadata = {
            "name" : filename,
            "description" : filedescription if filedescription else "Test File",
            "mimeType" : filetype if filetype else "application/vnd.google-apps.spreadsheet"
        }


    with open("metadata.json", "w") as outfile:
        json.dump(filemetadata, outfile)


    files=[
      ('',('metadata.json',open('metadata.json','rb'),'application/json')),
      ('',(filename,open(filename,'rb'),'text/csv'))
    ]
    headers = {
      'Authorization': 'Bearer ' + access_token
    }

    #response = requests.request("POST", url, headers=headers, data=payload, files=files)

    #print(response.text)
    fileId = "1Y6RxS3Bl0BENnQpGtMQLcFobjLq8S7vNNmJrnUJQoGQ"
    file_url = "https://drive.google.com/uc?export=download&id=1Y6RxS3Bl0BENnQpGtMQLcFobjLq8S7vNNmJrnUJQoGQ"
    file_url = "https://www.googleapis.com/drive/v3/files/%s/export?mimeType=text/csv" % (fileId)
    print(file_url)


    # Specify the local file path where you want to save the downloaded file
    local_file_path = "downloaded_file.xlsx"
    # Send a GET request to the Google Drive file's download URL
    response = requests.get(file_url,headers=headers)
    print(response.text)
if __name__ == '__main__':

    name = "upload_file_to_gdrive.py"
    parser = OptionParser(version=name)
    parser.add_option('--filename',dest='filename',default=None,type='string', help='Specify the filename')
    parser.add_option('--folderid',dest='folderid',default=None,type='string', help='Specify the folder')
    parser.add_option('--filedescription',dest='filedescription',default=None,type='string', help='Specify the description')
    parser.add_option('--filetype',dest='filetype',default=None,type='string', help='Specify the filetype')
    options, args = parser.parse_args()

    try :
      if not options.filename:
        print "Please provide the filename!!"
        sys.exit(1)
      else :
        filename = options.filename
        folderid = options.folderid
        filedescription = options.filedescription
        filetype = options.filetype
        upload_file_to_gdrive(filename,folderid,filedescription,filetype)
    except Exception as fault:
      traceback.print_exc()
      print str(fault)
      sys.exit(1)