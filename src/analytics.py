import os
import time
import pandas as pd
import numpy as np


print("NASA GPM IMERG - Phase 2 Analytics")
print("----------------------------------")



processed_folder = "../data/processed"
results_folder = "../data/analytics"



os.makedirs(results_folder, exist_ok=True)



parquet_files = []

for file_name in os.listdir(processed_folder):

    if file_name.endswith(".parquet"):

        file_path = os.path.join(
            processed_folder,
            file_name
        )

        parquet_files.append(file_path)



parquet_files.sort()


print("\nTotal parquet files found:", len(parquet_files))


random_seed = 42



file_summaries = []

eda_samples = []

spatial_summaries = []



start_time = time.time()


for file_number, file_path in enumerate(parquet_files, start=1):

    print(
        "Analyzing file",
        file_number,
        "of",
        len(parquet_files)
    )


  
    df = pd.read_parquet(file_path)


   
    observation_time = df["datetime"].iloc[0]


    
    total_rows = len(df)

    rainy_rows = (df["precipitation_mm_per_hr"] > 0).sum()

    zero_rows = (df["precipitation_mm_per_hr"] == 0).sum()

    
    heavy_rain_rows = (
        df["precipitation_mm_per_hr"] >= 5.3
    ).sum()

    heavy_rain_percentage = (
        heavy_rain_rows / total_rows
    ) * 100


    
    rain_percentage = (
        rainy_rows / total_rows
    ) * 100


    
    rainy_data = df[
        df["precipitation_mm_per_hr"] > 0
    ]


    
    mean_precipitation = df[
        "precipitation_mm_per_hr"
    ].mean()

    median_precipitation = df[
        "precipitation_mm_per_hr"
    ].median()

    maximum_precipitation = df[
        "precipitation_mm_per_hr"
    ].max()


   
    if len(rainy_data) > 0:

        mean_rainy_precipitation = rainy_data[
            "precipitation_mm_per_hr"
        ].mean()

        median_rainy_precipitation = rainy_data[
            "precipitation_mm_per_hr"
        ].median()

        percentile_95 = rainy_data[
            "precipitation_mm_per_hr"
        ].quantile(0.95)

        percentile_99 = rainy_data[
            "precipitation_mm_per_hr"
        ].quantile(0.99)

    else:

        mean_rainy_precipitation = 0

        median_rainy_precipitation = 0

        percentile_95 = 0

        percentile_99 = 0


  
    file_summaries.append({
        "datetime": observation_time,
        "date": observation_time.date(),
        "hour": observation_time.hour,
        "minute": observation_time.minute,
        "total_rows": total_rows,
        "zero_rows": zero_rows,
        "rainy_rows": rainy_rows,
        "rain_percentage": rain_percentage,
        "heavy_rain_rows": heavy_rain_rows,
        "heavy_rain_percentage": heavy_rain_percentage,
        "mean_precipitation": mean_precipitation,
        "median_precipitation": median_precipitation,
        "mean_rainy_precipitation": mean_rainy_precipitation,
        "median_rainy_precipitation": median_rainy_precipitation,
        "maximum_precipitation": maximum_precipitation,
        "rainy_95th_percentile": percentile_95,
        "rainy_99th_percentile": percentile_99
    })


    
    sample_size = min(200, len(df))

    sample = df.sample(
        n=sample_size,
        random_state=random_seed
    )

    eda_samples.append(sample)


    
    df["latitude_bin"] = np.floor(
        df["latitude"]
    )

    df["longitude_bin"] = np.floor(
        df["longitude"]
    )


    
    df["rain_occurred"] = (
        df["precipitation_mm_per_hr"] > 0
    ).astype(int)

    df["heavy_rain_occurred"] = (
        df["precipitation_mm_per_hr"] >= 5.3
    ).astype(int)

    
    spatial = df.groupby(
        ["latitude_bin", "longitude_bin"]
    ).agg(
        total_observations=(
            "precipitation_mm_per_hr",
            "count"
        ),
        rainy_observations=(
            "rain_occurred",
            "sum"
        ),
        heavy_rain_observations=(
            "heavy_rain_occurred",
            "sum"
        ),
        precipitation_sum=(
            "precipitation_mm_per_hr",
            "sum"
        ),
        maximum_precipitation=(
            "precipitation_mm_per_hr",
            "max"
        )
    ).reset_index()


    spatial_summaries.append(spatial)



file_summary_df = pd.DataFrame(file_summaries)



eda_sample_df = pd.concat(
    eda_samples,
    ignore_index=True
)



spatial_all = pd.concat(
    spatial_summaries,
    ignore_index=True
)



spatial_summary_df = spatial_all.groupby(
    ["latitude_bin", "longitude_bin"]
).agg(
    total_observations=(
        "total_observations",
        "sum"
    ),
    rainy_observations=(
        "rainy_observations",
        "sum"
    ),
    heavy_rain_observations=(
        "heavy_rain_observations",
        "sum"
    ),
    precipitation_sum=(
        "precipitation_sum",
        "sum"
    ),
    maximum_precipitation=(
        "maximum_precipitation",
        "max"
    )
).reset_index()



spatial_summary_df["rain_frequency_percent"] = (
    spatial_summary_df["rainy_observations"]
    /
    spatial_summary_df["total_observations"]
) * 100

spatial_summary_df["heavy_rain_frequency_percent"] = (
    spatial_summary_df["heavy_rain_observations"]
    /
    spatial_summary_df["total_observations"]
) * 100



spatial_summary_df["average_precipitation"] = (
    spatial_summary_df["precipitation_sum"]
    /
    spatial_summary_df["total_observations"]
)



daily_summary_df = file_summary_df.groupby(
    "date"
).agg(
    total_rows=(
        "total_rows",
        "sum"
    ),
    rainy_rows=(
    "rainy_rows",
    "sum"
    ),
    heavy_rain_rows=(
        "heavy_rain_rows",
        "sum"
    ),
    average_precipitation=(
        "mean_precipitation",
        "mean"
    ),
    average_rainy_precipitation=(
        "mean_rainy_precipitation",
        "mean"
    ),
    maximum_precipitation=(
        "maximum_precipitation",
        "max"
    )
).reset_index()



daily_summary_df["rain_percentage"] = (
    daily_summary_df["rainy_rows"]
    /
    daily_summary_df["total_rows"]
) * 100


daily_summary_df["heavy_rain_percentage"] = (
    daily_summary_df["heavy_rain_rows"]
    /
    daily_summary_df["total_rows"]
) * 100



hourly_summary_df = file_summary_df.groupby(
    "hour"
).agg(
    average_rain_percentage=(
        "rain_percentage",
        "mean"
    ),
    average_precipitation=(
        "mean_precipitation",
        "mean"
    ),
    average_rainy_precipitation=(
        "mean_rainy_precipitation",
        "mean"
    ),
    maximum_precipitation=(
        "maximum_precipitation",
        "max"
    )
).reset_index()



file_summary_df.to_parquet(
    os.path.join(
        results_folder,
        "half_hour_summary.parquet"
    ),
    index=False
)


daily_summary_df.to_parquet(
    os.path.join(
        results_folder,
        "daily_summary.parquet"
    ),
    index=False
)


hourly_summary_df.to_parquet(
    os.path.join(
        results_folder,
        "hourly_summary.parquet"
    ),
    index=False
)


spatial_summary_df.to_parquet(
    os.path.join(
        results_folder,
        "spatial_summary.parquet"
    ),
    index=False
)


eda_sample_df.to_parquet(
    os.path.join(
        results_folder,
        "eda_sample.parquet"
    ),
    index=False
)



end_time = time.time()

runtime_minutes = (
    end_time - start_time
) / 60



print("\nANALYTICS SUMMARY")

print(
    "Half-hour summaries:",
    len(file_summary_df)
)

print(
    "Daily summaries:",
    len(daily_summary_df)
)

print(
    "Hourly groups:",
    len(hourly_summary_df)
)

print(
    "Spatial groups:",
    len(spatial_summary_df)
)

print(
    "EDA sample rows:",
    len(eda_sample_df)
)

print(
    "Runtime in minutes:",
    round(runtime_minutes, 2)
)

print("\nAnalytics processing complete!")