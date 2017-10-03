#!/bin/bash

fab production build
fab production push
fab production create_project_directory
fab production update_compose_file
fab production compose_up
