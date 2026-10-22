Large-Scale Analysis of Heavy Rainfall Patterns Across the United States Using NASA GPM IMERG
Team Members
•	Akshitha Tolupunuri
•	Saksham Saxena
•	Harini Karnati
Course: EAS 587 - Data-Intensive Computing
University at Buffalo
Fall 2026
Project Overview
Heavy rainfall can cause flooding, road problems, travel issues, and damage to homes and public places. Rainfall is also not the same in every location or at every time.
The goal of this project is to study heavy rainfall patterns across the continental United States using NASA GPM IMERG Final Run V07 data.
The study period is from August 1, 2025 to September 14, 2025.
NASA IMERG provides precipitation estimates every 30 minutes for locations across the world.
Our main research question is:
How do the frequency, intensity, and geographic distribution of heavy rainfall vary across different regions of the United States from August 1 to September 14, 2025?
Dataset
Dataset: NASA GPM IMERG Final Run V07
Product: GPM_3IMERGHH_07
Source: NASA GES DISC / NASA Earthdata
File Format: HDF5
Time Resolution: 30 minutes
Spatial Resolution: About 0.1 degree by 0.1 degree
Raw Data Area: Global
Project Area: Continental United States
The full selected period normally contains:
•	45 days
•	48 half-hour files per day
•	2,160 expected HDF5 files
We downloaded:
•	2,067 HDF5 files
•	about 16 GB of raw data
The complete raw dataset is not stored in GitHub because it is too large.
Why This Is a Data-Intensive Project
Each global HDF5 file contains about:
•	3,600 longitude values
•	1,800 latitude values
•	about 6.48 million grid cells
The full dataset cannot be loaded into one normal Pandas DataFrame because it would require much more memory than the available 16 GB RAM.
Because of this, we process the files one at a time instead of loading everything into memory together.
This makes the processing more scalable and reduces memory usage.
Project Workflow
The main workflow of the project is:
NASA Earthdata
        ↓
Download HDF5 Files
        ↓
Inspect and Profile Raw Data
        ↓
Clean and Filter the Data
        ↓
Keep the U.S. Study Area
        ↓
Save Processed Data as Parquet
        ↓
Create Analytics Summaries
        ↓
Perform EDA
        ↓
Study Rainfall Frequency and Intensity
        ↓
Study Geographic Heavy Rainfall Patterns
        ↓
Create Figures and Results
Repository Structure
project-repo/
│
├── README.md
├── requirements.txt
├── research_plan.md
├── phase2_report.md
│
├── data/
│   ├── samples/
│   ├── raw/
│   ├── processed/
│   ├── analytics/
│   └── boundaries/
│
├── src/
│   ├── data_access.py
│   ├── data_sampling.py
│   ├── data_cleaning.py
│   ├── pipeline.py
│   └── analytics.py
│
├── notebooks/
│   └── phase2_analysis.ipynb
│
└── figures/
Main Source Files
src/data_access.py
This file was created in Phase 1 to help access and inspect the dataset.
src/data_sampling.py
This file was created in Phase 1 to work with smaller samples of the large dataset.
src/data_cleaning.py
This file contains the main cleaning steps.
The code:
•	reads one NASA IMERG HDF5 file
•	reads latitude, longitude, time, and precipitation
•	keeps the required geographic area
•	removes invalid fill values
•	removes negative precipitation values
•	keeps valid zero rainfall values
•	creates useful date and time columns
•	converts the result into a Pandas DataFrame
src/pipeline.py
This file is the main raw-to-processed pipeline.
It:
1.	finds the raw HDF5 files
2.	processes one file at a time
3.	applies the cleaning steps from data_cleaning.py
4.	saves the cleaned data as Parquet files
5.	continues until all available files are processed
Processing files one at a time prevents the full dataset from using all available memory.
src/analytics.py
This file creates smaller summary datasets from the processed Parquet files.
It creates:
•	half_hour_summary.parquet
•	daily_summary.parquet
•	hourly_summary.parquet
•	spatial_summary.parquet
•	eda_sample.parquet
These files are used for EDA and first analytics.
notebooks/phase2_analysis.ipynb
This notebook contains the Phase 2 EDA and first analytics.
It includes:
•	processed data checks
•	rainfall distribution
•	heavy rainfall definition
•	daily rainfall analysis
•	hourly rainfall analysis
•	rainfall frequency
•	rainfall intensity
•	heavy rainfall frequency
•	correlation analysis
•	spatial rainfall analysis
•	maps for the lower 48 states
•	key findings
•	design decisions
•	dead ends
Installation
Python is required for this project.
Install the required packages using:
pip install -r requirements.txt
How to Run the Phase 2 Workflow
Run the following commands from the main project folder.
Step 1: Process the Raw Data
python src/pipeline.py
This reads the HDF5 files, applies the cleaning steps, and saves the processed data as Parquet files.
Step 2: Create Analytics Summaries
python src/analytics.py
This creates the daily, hourly, half-hour, spatial, and EDA summary files.
Step 3: Run the Analysis Notebook
Open:
notebooks/phase2_analysis.ipynb
Run the notebook from top to bottom.
The notebook loads the summary files and performs the EDA and first analytics.
Data Cleaning
The main cleaning steps are:
•	extract latitude, longitude, time, and precipitation
•	keep the required U.S. geographic area
•	remove invalid fill values
•	remove negative precipitation values
•	keep valid zero rainfall values
•	create date, hour, and minute fields
•	save the cleaned data as Parquet files
Zero rainfall is kept because it is a valid observation showing that no rain occurred at that location and time.
Heavy Rainfall Definition
In Phase 1, the final heavy rainfall value had not yet been selected.
During Phase 2, we studied the distribution of positive rainfall values.
We defined heavy rainfall as:
Precipitation greater than or equal to 5.3 mm/hr
The value 5.3 mm/hr is the 95th percentile of positive rainfall observations in our processed EDA sample.
This threshold is used for this study period. It is not a general definition for all rainfall studies.
Data Coverage
The selected study period is August 1 to September 14, 2025.
However, the downloaded data is incomplete at the beginning of the period.
•	August 1 has no downloaded data.
•	August 2 contains only 3 of the expected 48 half-hour files.
•	August 3 to September 14 contains 43 complete days.
For this reason, daily comparisons use the 43 complete days.
Exploratory Data Analysis
The Phase 2 EDA studies rainfall using different views.
Rainfall Distribution
About 9.9% of observations in the EDA sample had precipitation greater than 0 mm/hr.
The positive rainfall distribution is strongly right-skewed.
Most rainfall values are small, while a smaller number of observations have much higher rainfall intensity.
We kept the high rainfall values because strong rainfall events are important for our research question.
Daily Rainfall
We studied:
•	daily rainfall frequency
•	average rainfall intensity
•	maximum rainfall intensity
•	heavy rainfall frequency
September 5 had the highest overall rainfall frequency among the complete days.
August 20 and August 21 had high rainfall intensity and high heavy rainfall activity.
Hourly Rainfall
The time values are studied in UTC.
Rainfall frequency was highest mainly around 21:00 to 23:00 UTC.
Average rainfall intensity was highest mainly around 14:00 to 18:00 UTC.
This shows that the time when rainfall happened most often was not always the same time when rainfall was strongest.
Spatial Rainfall
The original geographic subset was rectangular and included some ocean areas and locations outside the lower 48 states.
We used U.S. Census state boundary data to keep only spatial bins whose center points were inside the lower 48 states.
The spatial data was reduced from:
•	1,534 original spatial bins
•	to 851 lower-48 spatial bins
These 851 bins were used for the final spatial analysis.
Main Phase 2 Findings
Some of the main findings are:
•	About 9.9% of sampled observations had positive rainfall.
•	Heavy rainfall was defined as 5.3 mm/hr or higher.
•	September 5 had the highest overall rainfall frequency among the complete days.
•	August 20 and August 21 had high rainfall intensity and heavy rainfall activity.
•	Rainfall frequency and heavy rainfall frequency had a moderate positive correlation of about 0.54.
•	Rainfall frequency was highest mainly around 21:00 to 23:00 UTC.
•	Average rainfall intensity was highest mainly around 14:00 to 18:00 UTC.
•	Rainfall frequency was high mainly around Florida and parts of the southeastern United States.
•	Heavy rainfall frequency was also high mainly around Florida and nearby southeastern areas.
•	The highest spatial heavy rainfall frequency was about 1.87%.
•	The strongest individual rainfall events were found across different parts of the United States.
These results only describe the selected study period. They should not be treated as long-term climate results.
Design Decisions
Some important Phase 2 decisions were:
File-by-File Processing
We process one file at a time because the complete dataset is too large to load into memory at once.
Parquet Format
We save processed data in Parquet format because it is useful for large datasets and easier to use for later analysis than reading thousands of HDF5 files again.
Heavy Rainfall Threshold
We use the 95th percentile of positive rainfall values to define heavy rainfall instead of selecting a random value.
High Rainfall Values
We do not automatically remove high rainfall values as outliers because strong rainfall is important for our research question.
Incomplete Days
August 1 and August 2 are not used in daily comparisons because the data is incomplete.
U.S. Boundary Filtering
We use U.S. Census state boundaries for the final spatial analysis because a simple latitude and longitude box included ocean areas.
Dead Ends
Simple Latitude and Longitude Filtering
At first, we used simple latitude and longitude limits for the final spatial analysis.
This method still included some ocean areas. Some of the highest rainfall frequency locations appeared in the Atlantic Ocean.
Because of this, we did not use this method for the final spatial results.
GeoPandas and Shapely
We also tried GeoPandas and Shapely for U.S. state boundary filtering.
Some required library files were blocked in the Windows environment.
We later used pyshp with Matplotlib paths to perform the boundary filtering.
Limitations
There are some important limitations to the current analysis.
•	The study covers only a short 45-day period.
•	The beginning of the study period has missing files.
•	NASA IMERG precipitation values are satellite-based estimates and are not exact ground measurements.
•	The results should not be used as long-term climate conclusions.
•	We are studying rainfall patterns and are not directly predicting floods or weather.
Phase 3
Phase 2 prepares the cleaned data and first analytics needed for the next phase.
In Phase 3, we plan to continue using large-data tools such as Apache Spark and PySpark.
We can also study repeated heavy rainfall patterns, improve the scalable processing workflow, and decide whether a machine learning method is useful for the project.
References
1.	NASA Global Precipitation Measurement Mission, IMERG Version 07 Algorithm Theoretical Basis Document.
2.	NASA Global Precipitation Measurement Mission, IMERG Version 07 Technical Documentation.
3.	NASA GES DISC / NASA Earthdata.
4.	U.S. Census state boundary data.

