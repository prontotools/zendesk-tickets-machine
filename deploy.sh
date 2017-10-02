#!/bin/bash

# Show the output of the following commands (useful for debugging)
set -x

fab production build
fab production push:username=$DOCKER_USERNAME,password=$DOCKER_PASSWORD
fab production create_project_directory
fab production update_compose_file
fab production compose_up
