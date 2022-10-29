sudo docker volume prune -f
sudo docker volume rm $(docker volume ls -q)
sudo rm -rf mongo-volume app/__pycache__/ && mkdir mongo-volume
sudo docker system prune -a -f && docker builder prune -a -f