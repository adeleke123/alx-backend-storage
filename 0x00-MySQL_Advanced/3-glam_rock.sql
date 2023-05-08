-- Script lists all bands with Glam rock as their main style,
-- ranked by their longevity (in years).
-- Output displays only the 'band_name' and 'lifespan' columns.

SELECT band_name, (IFNULL(split, 2022) - formed) as lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
