#!/usr/bin/env bash

# simple script to sync this repository to the server I am currently using to process the data.

rsync -Pav -e "ssh -i ${AWS_RSA_KEY}" ~/projects/zeisel_hca ec2-user@54.210.155.150:/home/ec2-user