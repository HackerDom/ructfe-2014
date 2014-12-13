#!/bin/bash

# change directory to the script location
cd "$( dirname "${BASH_SOURCE[0]}")"

project=${1?usage: ./gcloud_create_teams <project>}

#./gcloud_create_instance.sh $project europe-west1-c 0 64 &
#./gcloud_create_instance.sh $project europe-west1-c 64 128 &
#./gcloud_create_instance.sh $project europe-west1-c 128 192 &
#./gcloud_create_instance.sh $project europe-west1-c 192 256 &

#./gcloud_create_instance.sh $project asia-east1-b 256 320 &
#./gcloud_create_instance.sh $project asia-east1-b 320 384 &
#./gcloud_create_instance.sh $project asia-east1-b 384 448 &
#./gcloud_create_instance.sh $project asia-east1-b 448 512 &

#./gcloud_create_instance.sh $project us-central1-b 512 576 &
#./gcloud_create_instance.sh $project us-central1-b 576 640 &
#./gcloud_create_instance.sh $project us-central1-b 640 704 &
#./gcloud_create_instance.sh $project us-central1-b 704 768 &

#./gcloud_create_instance.sh $project europe-west1-c 128 160 &
#./gcloud_create_instance.sh $project europe-west1-c 160 192 &
#./gcloud_create_instance.sh $project europe-west1-c 192 224 &
#./gcloud_create_instance.sh $project europe-west1-c 224 256 &

#./gcloud_create_instance.sh $project europe-west1-c 128 144 &
#./gcloud_create_instance.sh $project europe-west1-c 144 160 &
#./gcloud_create_instance.sh $project europe-west1-c 160 176 &
#./gcloud_create_instance.sh $project europe-west1-c 176 192 &
#./gcloud_create_instance.sh $project europe-west1-c 192 208 &
#./gcloud_create_instance.sh $project europe-west1-c 208 224 &
#./gcloud_create_instance.sh $project europe-west1-c 224 240 &
#./gcloud_create_instance.sh $project europe-west1-c 240 256 &
 
#./gcloud_create_instance.sh $project asia-east1-c 256 272 &
#./gcloud_create_instance.sh $project asia-east1-c 272 288 &
#./gcloud_create_instance.sh $project asia-east1-c 288 304 &
#./gcloud_create_instance.sh $project asia-east1-c 304 320 &
#./gcloud_create_instance.sh $project asia-east1-c 320 336 &
#./gcloud_create_instance.sh $project asia-east1-c 336 352 &
#./gcloud_create_instance.sh $project asia-east1-c 352 368 &
#./gcloud_create_instance.sh $project asia-east1-c 368 384 &
 
#./gcloud_create_instance.sh $project us-central1-f 384 400 &
#./gcloud_create_instance.sh $project us-central1-f 400 416 &
#./gcloud_create_instance.sh $project us-central1-f 416 432 &
#./gcloud_create_instance.sh $project us-central1-f 432 448 &
#./gcloud_create_instance.sh $project us-central1-f 448 464 &
#./gcloud_create_instance.sh $project us-central1-f 464 480 &
#./gcloud_create_instance.sh $project us-central1-f 480 496 &
#./gcloud_create_instance.sh $project us-central1-f 496 512 &

./gcloud_create_instance.sh $project europe-west1-c 512 528 &
./gcloud_create_instance.sh $project europe-west1-c 528 544 &
./gcloud_create_instance.sh $project europe-west1-c 544 560 &
./gcloud_create_instance.sh $project europe-west1-c 560 576 &
./gcloud_create_instance.sh $project europe-west1-c 576 592 &
./gcloud_create_instance.sh $project europe-west1-c 592 608 &
./gcloud_create_instance.sh $project europe-west1-c 608 624 &
./gcloud_create_instance.sh $project europe-west1-c 624 640 &

./gcloud_create_instance.sh $project asia-east1-c 640 656 &
./gcloud_create_instance.sh $project asia-east1-c 656 672 &
./gcloud_create_instance.sh $project asia-east1-c 672 688 &
./gcloud_create_instance.sh $project asia-east1-c 688 704 &
./gcloud_create_instance.sh $project asia-east1-c 704 720 &
./gcloud_create_instance.sh $project asia-east1-c 720 736 &
./gcloud_create_instance.sh $project asia-east1-c 736 752 &
./gcloud_create_instance.sh $project asia-east1-c 752 768 &


wait