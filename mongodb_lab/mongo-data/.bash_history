cd data/db/
cat dblp-nosql-1000.json | jq '.' | head
cat dblp-nosql-1000.json | jq '.result.hits.hit' > dblp-nosql-1000-results.json
mongoimport --collection='dblp_nosql' --file='dblp-nosql-1000-results.json' --jsonArray
exit
mongoimport --collection='dblp_nosql' --file='dblp-nosql-1000-results.json' --jsonArray
cd data/db/
ls
mongoimport --collection='dblp_nosql' --file='dblp-nosql-1000-results.json' --jsonArray
exit
cd data/db/
mongoimport --collection='dblp_nosql' --file='dblp-nosql-1000-results.json' --jsonArray
exit
