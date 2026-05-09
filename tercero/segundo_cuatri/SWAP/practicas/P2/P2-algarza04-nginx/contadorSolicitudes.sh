for i in {1..8}; do
  echo "web$i: $(docker exec web$i grep GET /var/log/apache2/access.log | wc -l)"
done

