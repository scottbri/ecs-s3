from boto.s3.connection import S3Connection

accessKeyId='130905237756716034@ecstestdrive.emc.com'
secretKey='ySNRk1xpFFcKG0wJbaTQgF2TeeBQdetUB5NC28dz'
host = 'object.ecstestdrive.com'
conn = S3Connection(aws_access_key_id=accessKeyId, aws_secret_access_key=secretKey, host=host)


##########################################
## Iterate through the list of buckets and delete all the keys and buckets
for bucket in conn.get_all_buckets():
    for key in bucket.list():
        print "Deleting {bucketname}/{keyname}".format(bucketname = bucket.name, keyname = key.name)
        key.delete()

for bucket in conn.get_all_buckets():
    print "Deleting bucket {name}".format(name = bucket.name)
    bucket.delete()
