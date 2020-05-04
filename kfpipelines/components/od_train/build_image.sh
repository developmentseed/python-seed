#!/bin/bash -e

image_name=gcr.io/voltaire-266718/voltaire-training
image_tag=v1-gpu
full_image_name=${image_name}:${image_tag}

cd "$(dirname "$0")" 
docker build --no-cache -t "${full_image_name}" .
docker push "$full_image_name"

# Output the strict image name (which contains the sha256 image digest)
docker inspect --format="{{index .RepoDigests 0}}" "${IMAGE_NAME}"
