#!/bin/bash

eval $(aws ecr get-login --no-include-email --region eu-west-1)
fab production build
fab production push
fab production create_project_directory
fab production update_compose_file
fab production compose_up
