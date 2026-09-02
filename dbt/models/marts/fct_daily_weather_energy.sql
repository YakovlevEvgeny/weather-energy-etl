WITH staging AS (
    SELECT * FROM {{ ref('stg_weather_hourly') }}
),

daily_aggregated AS (
    SELECT
        observed_at::date AS observation_date,
        city_name,
        COUNT(*) AS hourly_records_count,
        ROUND(AVG(temperature_c), 2) AS avg_temperature_c,
        ROUND(MIN(temperature_c), 2) AS min_temperature_c,
        ROUND(MAX(temperature_c), 2) AS max_temperature_c,
        ROUND(AVG(humidity_pct), 1) AS avg_humidity_pct,
        ROUND(AVG(wind_speed_ms), 2) AS avg_wind_speed_ms,
        ROUND(SUM(solar_irradiance_w_m2), 2) AS total_solar_radiation,
        ROUND(AVG(wind_energy_potential), 2) AS avg_wind_energy_potential
    FROM staging
    GROUP BY 1, 2
)

SELECT 
    MD5(observation_date::text || '-' || city_name) AS daily_summary_id,
    *
FROM daily_aggregated
