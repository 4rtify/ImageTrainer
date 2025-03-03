import boto3
import os
import sys

bucket_name, remote_dir_name, host_dir = sys.argv[1:4]

def downloadDirectoryFromS3(bucketName, remoteDirectoryName, hostDirectoryName):
    s3_resource = boto3.resource(
        service_name='s3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        endpoint_url="http://gloomy.lan.crlab:9000",
        use_ssl=False,
    )
    bucket = s3_resource.Bucket(bucketName)
    for obj in bucket.objects.filter(Prefix=remoteDirectoryName):
        local_file_path = os.path.join(hostDirectoryName, os.path.relpath(obj.key, remoteDirectoryName))
        if not os.path.exists(os.path.dirname(local_file_path)):
            os.makedirs(os.path.dirname(local_file_path))
        print(f"Downloading {obj.key} to {local_file_path}")
        bucket.download_file(obj.key, local_file_path)

downloadDirectoryFromS3(bucket_name, remote_dir_name, host_dir)