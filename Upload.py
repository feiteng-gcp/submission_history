# from google.cloud import storage
import logging
import boto3
from botocore.exceptions import ClientError
import os


def upload_blob_s3(bucket, file_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print("File {} uploaded to {}.".format(file_name, object_name))
    except ClientError as e:
        logging.error(e)
        return False
    return True

def upload_blob_gcp(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def upload_file(file_name):
    upload_blob_s3('yanglaoduidu', file_name, file_name)
    
def updateDeadline():
    file_name = 'assets/deadline.json'
    upload_blob_s3('yanglaoduidu', file_name, file_name)

if __name__ == '__main__':
    updateDeadline()
