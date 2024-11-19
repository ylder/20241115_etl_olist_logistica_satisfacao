SELECT DISTINCT
    (geolocation_zip_code_prefix || geolocation_state) AS id_geolocation,
    geolocation_state

FROM geolocation