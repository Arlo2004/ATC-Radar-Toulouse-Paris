java -jar trino_jar.jar --server https://trino.opensky-network.org --external-authentication --user arlo2004 --catalog minio --schema osky --execute "
SELECT time, lat, lon, velocity, geoaltitude, heading 
FROM state_vectors_data4 
WHERE icao24 = '3950cc' 
AND hour BETWEEN 1704067200 AND 1704153600 
ORDER BY time ASC" --output-format CSV > trayectoria_A320_AFR58XP.csv
