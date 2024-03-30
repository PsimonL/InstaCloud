import boto3
import os

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')

class S3_Client:
   
    def __init__(self) -> None:
        self.client = boto3.client(
            service_name='s3',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )
    
    def upload_file(self, file, filename_in_s3):
        self.client.upload_fileobj(file, AWS_BUCKET_NAME, filename_in_s3)
    
    def download_file(self, local_filename, filename_in_s3):
        self.client.download_file(Bucket=AWS_BUCKET_NAME, Key=filename_in_s3, Filename=local_filename)

    def list_all_files(self):
        response = self.client.list_objects_v2(Bucket=AWS_BUCKET_NAME)
        if 'Contents' in response:
            file_names = [obj['Key'] for obj in response['Contents']]
        
        return file_names

