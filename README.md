# RDS Snapshot Replicator

This is a small lambda function to replicate snapshot from one region to another and I'm fully aware that there is an AWS feature for this but in only works for certain database engines. [Look](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReplicateBackups.html) 

## Requirements
- python >= 3.9

## Notes
I left a github action code to deploy this lambda function, you will need aws credentials.
