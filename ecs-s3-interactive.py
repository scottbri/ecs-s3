from boto.s3.connection import S3Connection

accessKeyId='yourAccessKeyId@ecstestdrive.emc.com'
secretKey='yourSecretKey'
host = 'object.ecstestdrive.com'
conn = S3Connection(aws_access_key_id=accessKeyId, aws_secret_access_key=secretKey, host=host)

## Prove that there are no buckets
print conn.get_all_buckets()

## Create some example buckets
conn.create_bucket('images')
conn.create_bucket('docs')
conn.create_bucket('eng')
conn.create_bucket('hr')
conn.create_bucket('cust1')
conn.create_bucket('cust2')

## Print a list of all buckets
for bucket in conn.get_all_buckets():
    print "{name}\t\tCreated at {created}".format(name = bucket.name, created = bucket.creation_date)

## Create some keys from scratch
bucket = conn.get_bucket('eng')
key = bucket.new_key('listOfProjects.txt')
key.set_contents_from_string('1) mission to mars 2) new app for customer retention 3) self driving cars')

## Create some keys by uploading some files
bucket = conn.get_bucket('docs')
key = bucket.new_key('continuous-delivery.pdf')
key.set_contents_from_filename('docs/continuous-delivery.pdf')

key = bucket.new_key('network-speeds.xls')
key.set_contents_from_filename('docs/network-speeds.xls')

bucket = conn.get_bucket('images')
key = bucket.new_key('emcopenstack.jpeg')
key.set_contents_from_filename('images/emcopenstack.jpeg')

key = bucket.new_key('ecs.png')
key.set_contents_from_filename('images/ecs.png')

## Iterate through the list of buckets and print all the keys
for bucket in conn.get_all_buckets():
    print "{name}:".format(name = bucket.name)
    for key in bucket.list():
        print "{size}\t{modified}\t{bucketname}/{keyname}".format(size = key.size, modified = key.last_modified, bucketname = bucket.name, keyname = key.name)


## Show contents of text key
bucket = conn.get_bucket('eng')
key = bucket.get_key('listOfProjects.txt')
print "Projects are:"
print key.get_contents_as_string()

## Download one of the images into a new filename
bucket = conn.get_bucket('images')
key = bucket.get_key('ecs.png')
key.get_contents_to_filename('ecs-new.png')

## Generate a url to download the image
print key.generate_url(0, query_auth=False, force_http=True)
