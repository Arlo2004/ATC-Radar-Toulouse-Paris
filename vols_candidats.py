--SQL 1: IDENTIFICATION DES CANDIDATS
SELECT 
    icao24 AS id_avion, 
    callsign AS matricula,
    firstseen AS hora_despegue
FROM flights_data4 
WHERE estdepartureairport = 'LFBO' 
  AND (estarrivalairport = 'LFPG' OR estarrivalairport = 'LFPO')
  AND day BETWEEN 1704067200 AND 1704153600 
  --Filtro de jours
ORDER BY firstseen ASC
LIMIT 10;
