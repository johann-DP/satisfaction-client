commande pour tester le conteneur:

docker container run --rm\
 #-v ../../data:/scraping/data \
-v /home/ubuntu/projet_satisfaction/projet_DST_satisfaction_client/data:/scraping/data \
  --network my_network\
 --name my_scraping scraping:latest


docker container run --rm -v /home/ubuntu/projet_satisfaction/projet_DST_satisfaction_client/data:/scraping/data --network my_network -it --name my_scraping scraping:latest bash
