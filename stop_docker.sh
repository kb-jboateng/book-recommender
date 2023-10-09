#! /bin/bash 
# To stop the cluster, the date in the Docker volumes is preserved nad loaded when you restart.
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
