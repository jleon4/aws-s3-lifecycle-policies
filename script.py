#!/usr/bin/env python3
import os
import csv
import json

# Function is used to get all S3 bucket names
def get_all_s3_buckets():
    bucket_names = os.popen("aws s3api list-buckets --query 'Buckets[].Name'").read()
    buckets = json.loads(bucket_names)
    return buckets

# Function is used to collect the json format of the lifecycle policy based on S3 bucket name
def get_s3_bucket_lifecycle_policy(bucket_name, writer):
    row=[]
    row.append(bucket_name)
    try:
        policy_response = os.popen(f"aws s3api get-bucket-lifecycle-configuration --bucket {bucket_name}").read()
        policy = json.loads(policy_response)
        print(policy)
        row.append(policy)
        writer.writerow(row)
    except:
        print(f'no lifecycle policy for bucket: {bucket_name}')
        row.append("N/A")
        writer.writerow(row)

# Main function used to getting all S3 bucket lifecycle data and write to csv file
def main():
    buckets = []
    buckets = get_all_s3_buckets()
    with open('s3_bucket_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Bucket Name", "Lifecycle Policy"])
        for bucket in buckets:
            get_s3_bucket_lifecycle_policy(bucket, writer)
        print("See output")

if __name__=="__main__":
    main()
