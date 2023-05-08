-- Script ranks the origins of metal bands.
-- Output includes the origins name and the total number
-- of fans from that origins in descending order.

SELECT origin, SUM(fans) as nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
