docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images)
docker volume prune
docker system prune