## The task

Your mission in this task is to implement a deployment flow of a containerized application and it's DB:

- The deployment flow script needs to be coded using Python language (please specify which version you ran it with)
- The App + DB containers need to be run using Docker and Docker-compose:
- If you don't know docker-compose, don't worry - Go to https://docs.docker.com/compose/gettingstarted/#step-3-define-services-in-a-compose-file to view a guide on how to create a docker-compose.yml and run it.
- You DO NOT need to create any Dockerfiles, they are already given to you in the App's repo (See “About the App” section below.


## The script

The deployment flow script should perform the following steps:

- Download image resources file from AWS S3 (https://s3.eu-central-1.amazonaws.com/devops-exercise/pandapics.tar.gz) and extract it's content to '/public/images' path.
- Create, build & run the App + DB using “docker-compose up” command.
- Check the App's health (See App's healthcheck below) at the end of the deployment flow and fail the deployment flow upon bad App health.


##  more info About the App:

You can find the App including instructions on how to run it here:

https://github.com/bigpandaio/ops-exercise


The App is a simple NodeJS application that displays images found in following App's path: '/public/images'. Any image that will be placed in this path upon loading the APP will be written to the DB and displayed in the App's root URI 
(e.g. 'http://localhost:3000/').


The App's healthcheck: Located at the '/health' URI (e.g. 'http://localhost:3000/health') is a simple script that checks that basic App components are functioning such as DB & Disk connectivity. When one of the components is not functioning properly (For instance the App cannot connect to it's DB) the healthcheck URI will return a 500 status code.


You are requested to add a check at the end of the deployment flow that the App's healthcheck is OK (e.g. status 200) and if not fail the deployment flow.


## IMPORTANT NOTES:

 - The entire App including it's startup is already written. You are NOT required to write ANY Javascript code in this exercise.
 - For simplicity sake, it is sufficient for this exercise to have both the App & it's DB run on localhost and not on any other environment/cloud.


## Submission instructions:

Once done, please create a Github repo (Don't fork our repo) and send us a link to it. The repo should contain the following:

 - The deployment flow script.
 - The docker-compose.yml file.
 - Any additional files needed in order to run the app from it's root folder.
 - Proper documentation needed in order to fully run your exercise on our localhost.