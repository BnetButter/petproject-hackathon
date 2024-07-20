docker run --rm \
  -it \
  --network petproject_pet_network \
  --env-file ../.env    \
  -v $(pwd):/app \
  geoserver-updator \
  /bin/bash
