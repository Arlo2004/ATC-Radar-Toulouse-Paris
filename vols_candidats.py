java -jar trino_jar.jar --server https://trino.opensky-network.org --external-authentication --user arlo2004 --catalog minio --schema osky --execute "
SELECT icao24, firstseen, lastseen 
FROM flights_data4 
WHERE estdepartureairport = 'LFBO' 
AND (estarrivalairport = 'LFPG' OR estarrivalairport = 'LFPO') 
AND day BETWEEN 1704067200 AND 1704153600 
LIMIT 10" --output-format CSV > lista_candidatos.csv
