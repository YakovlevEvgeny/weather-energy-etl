WITH source AS (
    SELECT * FROM {{ source('raw_data', 'weather_hourly') }}
),

transformed AS (
    SELECT
        timestamp AS observed_at,
        latitude,
        longitude,
        CASE
            WHEN latitude BETWEEN 55.70 AND 55.80 AND longitude BETWEEN 37.50 AND 37.70 THEN 'Moscow'
            WHEN latitude BETWEEN 52.40 AND 52.60 AND longitude BETWEEN 13.30 AND 13.50 THEN 'Berlin'
            ELSE 'Unknown'
        END AS city_name,
        temperature_2m AS temperature_c,
        relative_humidity_2m AS humidity_pct,
        wind_speed_10m AS wind_speed_ms,
        direct_normal_irradiance AS solar_irradiance_w_m2,
        -- Оценка ветрового потенциала (куб скорости ветра)
        ROUND(POWER(wind_speed_10m, 3)::numeric, 2) AS wind_energy_potential,
        extracted_at
    FROM source
)

SELECT * FROM transformed
