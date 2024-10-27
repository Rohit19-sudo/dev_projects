import boto3
import requests
import json


OBJECT_NAME_TO_UPLOAD = 'test5.txt'
API_URL = ''


def test_presigned_url():

    body = {'source': 'TestApp',
            'filename': "test5.txt",
            'metadata': {
            'file_format': 'json',
            'description': 'test file'
        }
    }

    header = {'Content-type': 'application/json'}
    response = requests.post(API_URL,data = json.dumps(body), headers=header)

    presigned_response = response.json()
    #Upload file to S3 using presigned URL
    fileob =open(OBJECT_NAME_TO_UPLOAD,'rb')
    files = { 'file': fileob }
    r = requests.post(presigned_response['url'], data=presigned_response['fields'], files=files)
    print(r.status_code)

    fileob.close()


if __name__ == "__main__":
    test_presigned_url()
