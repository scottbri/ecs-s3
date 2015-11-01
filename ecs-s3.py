from boto.s3.connection import S3Connection
from timeit import default_timer as timer
import os

#accessKeyId='yourAccessKey@ecstestdrive.emc.com'
#tenantId='yourTenantId'
#secretKey='yourSecretKey'
from credentials import *

host = 'object.ecstestdrive.com'
conn = S3Connection(aws_access_key_id=accessKeyId, aws_secret_access_key=secretKey, host=host)

waitForUser = True

##########################################
## Prove that there are no buckets
print "Listing all buckets"
print conn.get_all_buckets()

if waitForUser: raw_input()

##########################################
## Create some example buckets
print "Creating some buckets"
conn.create_bucket('images')
bucket = conn.get_bucket('images')
conn.create_bucket('docs')
conn.create_bucket('eng')
conn.create_bucket('hr')
conn.create_bucket('cust1')
conn.create_bucket('cust2')

##########################################
## Print a list of all buckets
for bucket in conn.get_all_buckets():
    print "{name}\t\tCreated at {created}".format(name = bucket.name, created = bucket.creation_date)

if waitForUser: raw_input()
##########################################
## Create some keys from scratch
bucket = conn.get_bucket('eng')
key = bucket.new_key('listOfProjects.txt')
projects = '1) mission to mars 2) new app for customer retention 3) self driving cars'
print "Creating key eng/listOfProject.txt from a string of content"
key.set_contents_from_string(projects)

if waitForUser: raw_input()
##########################################
## Create some keys by uploading some files
# ...
bucket = conn.get_bucket('docs')
key = bucket.new_key('continuous-delivery.pdf')
print "Uploading file docs/continuous-delivery.pdf"
start = timer()
key.set_contents_from_filename('docs/continuous-delivery.pdf')
end = timer()
print "Uploaded in {elapseTime} sec".format(elapseTime = end - start)

key = bucket.new_key('network-speeds.xls')
print "Uploading file docs/network-speeds.xls"
start = timer()
key.set_contents_from_filename('docs/network-speeds.xls')
end = timer()
print "Uploaded in {elapseTime} sec".format(elapseTime = end - start)

bucket = conn.get_bucket('images')
key = bucket.new_key('emcopenstack.jpeg')
print "Uploading file images/emcopenstack.jpeg"
start = timer()
key.set_contents_from_filename('images/emcopenstack.jpeg')
end = timer()
print "Uploaded in {elapseTime} sec".format(elapseTime = end - start)
key.set_acl('public-read')

key = bucket.new_key('ecs.png')
print "Uploading file images/ecs.png"
start = timer()
key.set_contents_from_filename('images/ecs.png')
end = timer()
print "Uploaded in {elapseTime} sec".format(elapseTime = end - start)
key.set_acl('public-read')

print "Done with uploads"

if waitForUser: raw_input()
##########################################
## Iterate through the list of buckets and print all the keys
for bucket in conn.get_all_buckets():
    print "{name}:".format(name = bucket.name)

    ## For each bucket print all the keys in that bucket
    for key in bucket.list():
        print "{size}\t{modified}\t{bucketname}/{keyname}".format(size = key.size, modified = key.last_modified, bucketname = bucket.name, keyname = key.name)

##########################################
## Show contents of text key
print "Getting contents of eng/listOfProjects.txt"
bucket = conn.get_bucket('eng')
key = bucket.get_key('listOfProjects.txt')
print "Projects are:"
print key.get_contents_as_string()

if waitForUser: raw_input()
##########################################
## Download one of the images into a new filename
print "Downloading images/ecs.png into new file ./ecs-new.png"
bucket = conn.get_bucket('images')
key = bucket.get_key('ecs.png')
key.get_contents_to_filename('ecs-new.png')
os.system("open ecs-new.png")

if waitForUser: raw_input()
##########################################
## Reveal all keys as urls
for bucket in conn.get_all_buckets():
    for key in bucket.list():
        print "http://{tenantname}.public.ecstestdrive.com/{bucketname}/{keyname}".format(tenantname = tenantId, bucketname = bucket.name, keyname = key.name)


##########################################
## Reveal all security acl
for bucket in conn.get_all_buckets():
    for key in bucket.list():
        print "{bucketname}/{keyname}\t{aclString}".format(bucketname = bucket.name, keyname = key.name, aclString = key.get_acl())
