#!/bin/bash

# change directory to the script location
cd "$( dirname "${BASH_SOURCE[0]}")"

project=${1?usage: ./gcloud_create_teams <project>}

./gcloud_create_instance.sh $project europe-west1-b 0 64 &
./gcloud_create_instance.sh $project europe-west1-b 64 128 &
./gcloud_create_instance.sh $project europe-west1-b 128 192 &
./gcloud_create_instance.sh $project europe-west1-b 192 256 &

./gcloud_create_instance.sh $project asia-east1-b 256 320 &
./gcloud_create_instance.sh $project asia-east1-b 320 384 &
./gcloud_create_instance.sh $project asia-east1-b 384 448 &
./gcloud_create_instance.sh $project asia-east1-b 448 512 &

./gcloud_create_instance.sh $project us-central1-b 512 576 &
./gcloud_create_instance.sh $project us-central1-b 576 640 &
./gcloud_create_instance.sh $project us-central1-b 640 704 &
./gcloud_create_instance.sh $project us-central1-b 704 768 &

wait