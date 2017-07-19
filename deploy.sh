#!/bin/bash

# Show the output of the following commands (useful for debugging)
set -x 

# Import the SSH deployment key
echo -e "Host *\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config
openssl aes-256-cbc -K $encrypted_4dc5f4c62575_key -iv $encrypted_4dc5f4c62575_iv -in deploy-key.enc -out deploy-key -d
rm deploy-key.enc # Don't need it anymore
chmod 400 deploy-key
mv deploy-key ~/.ssh/id_rsa

if [ "$TRAVIS_PULL_REQUEST" == "false" -a "$TRAVIS_BRANCH" == "master" ]; then
  pip2.7 install fabric
  fab production build
  fab production push:username=$DOCKER_USERNAME,password=$DOCKER_PASSWORD
  fab production create_project_directory
  fab production update_compose_file
  fab production compose_up
else
  echo "Not deploying since this branch isn't master."
  exit 0
fi
