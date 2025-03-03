import boto3
import os
import sys

bucket_name, remote_dir_name, host_dir = sys.argv[1:4]

def uploadDirectoryToS3(bucketName, remoteDirectoryName, hostDirectoryName):
    s3_resource = boto3.resource(
        service_name='s3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        endpoint_url="http://gloomy.lan.crlab:9000",
        use_ssl=False,
    )
    bucket = s3_resource.Bucket(bucketName)
    for root, dirs, files in os.walk(hostDirectoryName):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, hostDirectoryName)
            s3_file_path = os.path.join(remoteDirectoryName, relative_path)
            print(f"Uploading {local_file_path} to {s3_file_path}")

            # Check if the file exists on S3 and delete it if it does
            try:
                s3_resource.Object(bucketName, s3_file_path).load()
                print(f"File {s3_file_path} exists on S3, deleting it.")
                s3_resource.Object(bucketName, s3_file_path).delete()
            except s3_resource.meta.client.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print(f"File {s3_file_path} does not exist on S3, uploading it.")
                else:
                    raise

            bucket.upload_file(local_file_path, s3_file_path)

uploadDirectoryToS3(bucket_name, remote_dir_name, host_dir)