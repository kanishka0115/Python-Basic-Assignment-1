import boto3
S3_RESOURCE = boto3.resource('s3')
print('My S3 buckets:')
for bucket in S3_RESOURCE.buckets.all():
    print(bucket.name)