#!/bin/bash

# change directory to the script location
cd "$( dirname "${BASH_SOURCE[0]}")"

project=${1?usage: ./gcloud_create_instace <project> <zone> <from> <to>}
zone=${2?usage: ./gcloud_create_instace <project> <zone> <from> <to>}
from=${3?usage: ./gcloud_create_instace <project> <zone> <from> <to>}
to=${4?usage: ./gcloud_create_instace <project> <zone> <from> <to>}

v_name="v-$from-$to"

to=$((to-1))

startup_file=$(mktemp -t "startup_XXXXX.sh")
chmod +x "$startup_file"

cat > "$startup_file" << EOF

/home/ubuntu/game_emulation/build_router.sh
/home/ubuntu/game_emulation/build_netscanning.sh
/home/ubuntu/game_emulation/build_testservice.sh

for i in {$from..$to}; do
	/home/ubuntu/game_emulation/start_router.sh \$i
	/home/ubuntu/game_emulation/start_testservice.sh \$i
done

for i in {$from..$((from + 8 - 1))}; do
	/home/ubuntu/game_emulation/start_netscanning.sh \$i
done

EOF

echo Making an instance
gcloud --project="$project" compute instances create "$v_name" --zone "$zone" --machine-type "n1-standard-1" --image "https://www.googleapis.com/compute/v1/projects/ubuntu-os-cloud/global/images/ubuntu-1404-trusty-v20141031a" --boot-disk-type "pd-standard" --metadata-from-file startup-script="$startup_file"

echo "Copying files"
until gcloud --project="$project" compute copy-files ../game_emulation "ubuntu@$v_name:/home/ubuntu/" --zone "$zone"; do
	echo Retrying filecopy
done

echo "Install pkgs and reset an instance"
gcloud --project="$project" compute ssh "ubuntu@$v_name" --zone "$zone" --command="sudo apt-get update; sudo apt-get -y upgrade; sudo apt-get -y install docker.io arping bridge-utils; sudo shutdown -r now"
