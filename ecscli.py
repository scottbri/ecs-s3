from boto.s3.connection import S3Connection
from timeit import default_timer as timer
import argparse

from credentials import *

host = 'object.ecstestdrive.com'
conn = S3Connection(aws_access_key_id=accessKeyId, aws_secret_access_key=secretKey, host=host)

def printBucketList():
    for bucket in conn.get_all_buckets():
        print "{name}\t\tCreated at {created}".format(name = bucket.name, created = bucket.creation_date)

def createBucket( bucketName ):
    conn.create_bucket(bucketName)

def createKeyFromString( bucketName, keyName, keyString ):
    bucket = conn.get_bucket(bucketName)
    key = bucket.new_key(keyName)
    key.set_contents_from_string(keyString)

def createKeyFromFilename( bucketName, keyName, fileName):
    bucket = conn.get_bucket(bucketName)
    key = bucket.new_key(keyName)
    key.set_contents_from_filename(fileName)

def printKeyTree():
    for bucket in conn.get_all_buckets():
     print "{name}:".format(name = bucket.name)
     for key in bucket.list():
         print "{size}\t{modified}\t{bucketname}/{keyname}".format(size = key.size, modified = key.last_modified, bucketname = bucket.name, keyname = key.name)

def printKeyText( bucketName, keyName ):
    bucket = conn.get_bucket(bucketName)
    key = bucket.get_key(keyName)
    print key.get_contents_as_string()

def downloadKey( bucketName, keyName, fileName ):
    bucket = conn.get_bucket(bucketName)
    key = bucket.get_key(keyName)
    key.get_contents_to_filename(fileName)

def printKeyTreeUrls():
    for bucket in conn.get_all_buckets():
     for key in bucket.list():
         print "http://{tenantname}.public.ecstestdrive.com/{bucketname}/{keyname}".format(tenantname = tenantId, bucketname = bucket.name, keyname = key.name)

def printKeyTreeACLs():
    for bucket in conn.get_all_buckets():
     for key in bucket.list():
         print "{bucketname}/{keyname}\t{aclString}".format(bucketname = bucket.name, keyname = key.name, aclString = key.get_acl())

def deleteKey( bucketName, keyName ):
    bucket = conn.get_bucket(bucketName)
    key = bucket.get_key(keyName)
    key.delete()

def deleteBucket( bucketName ):
    bucket = conn.get_bucket(bucketName)
    bucket.delete()

def deleteKeyTree():
    for bucket in conn.get_all_buckets():
        for key in bucket.list():
         print "Deleting {bucketname}/{keyname}".format(bucketname = bucket.name, keyname = key.name)
         deleteKey( bucket.name, key.name )

    for bucket in conn.get_all_buckets():
        print "Deleting bucket {name}".format(name = bucket.name)
        deleteBucket( bucket.name )

parser = argparse.ArgumentParser(description="command line interface to S3 based object storage")
group = parser.add_mutually_exclusive_group()
group.add_argument("-pb", "--printbucketlist", action="store_true",  help="print all buckets on store")
group.add_argument("-cb", "--createbucket", type=str, help="create a new bucket")
group.add_argument("-cks", "--createkeyfromstring", nargs=3, type=str, help="create a new key from string: bucket, key, string (key content)")
group.add_argument("-ckf", "--createkeyfromfilename", nargs=3, type=str, help="create a new key from a filename: bucket, key, filename")
group.add_argument("-pkt", "--printkeytree", action="store_true", help="print entire bucket and key tree")
group.add_argument("-pku", "--printkeyurls", action="store_true", help="print all key urls")
group.add_argument("-pka", "--printkeyacls", action="store_true", help="print all key acls")
group.add_argument("-pk", "--printkeytext", nargs=2, type=str, help="print contents of a key as text: bucket, key")
group.add_argument("-df", "--downloadfile", nargs=3, type=str, help="download a key into a local file: bucket, key, filename")
group.add_argument("-dk", "--deletekey", nargs=2, type=str, help="delete a key: bucket, key")
group.add_argument("-db", "--deletebucket", type=str, help="delete bucket")
group.add_argument("-dkt", "--deletekeytree", action="store_true", help="delete everything in the store including all buckets and keys")
args = parser.parse_args()

if args.printbucketlist:
    printBucketList()
elif args.createbucket:
    createBucket(args.createbucket)
elif args.printkeytree:
    printKeyTree()
elif args.printkeyurls:
    printKeyTreeUrls()
elif args.printkeyacls:
    printKeyTreeAcls()
elif args.deletebucket:
    deleteBucket(args.deletebucket)
elif args.deletekey:
    deleteKey(args.deletekey[0], args.deletekey[1])
elif args.deletekeytree:
    deleteKeyTree()
elif args.createkeyfromstring:
    createKeyFromString(args.createkeyfromstring[0], args.createkeyfromstring[1], args.createkeyfromstring[2])
elif args.createkeyfromfilename:
    createKeyFromFilename(args.createkeyfromfilename[0], args.createkeyfromfilename[1], args.createkeyfromfilename[2])
elif args.printkeytext:
    printKeyText(args.printkeytext[0], args.printkeytext[1])
elif args.downloadfile:
    downloadKey(args.downloadfile[0], args.downloadfile[1], args.downloadfile[2])

