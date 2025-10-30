# Data

## Dataset Source

- **Million Song Dataset Subset**: A collection of 10,000 songs with audio features and metadata extracted from the Echo Nest API. This is a manageable subset of the full Million Song Dataset which contains 1 million tracks.
- **Source URL**: http://millionsongdataset.com/pages/getting-dataset/#subset
- **Original Format**: HDF5 (.h5) files organized in nested directories
- **Processed Format**: Single CSV file with extracted features

## Data Processing

The raw HDF5 files were processed using `scripts/parse_msd.py` to extract relevant audio features and metadata into a single tabular format suitable for analysis.

# Codebook for Million Song Dataset Subset

## Variable Names and Descriptions:

### Identifiers
- **song_id**: Unique identifier for each song (Echo Nest ID)
- **artist_id**: Unique identifier for the artist (Echo Nest ID)

### Metadata
- **title**: Song title
- **artist_name**: Name of the performing artist
- **release**: Album or release name
- **year**: Year of release (0 indicates unknown)

### Audio Features
- **duration**: Length of the song in seconds
- **tempo**: Estimated tempo in beats per minute (BPM)
- **loudness**: Overall loudness in decibels (dB)
- **key**: Estimated key the song is in (0 = C, 1 = C#, 2 = D, ..., 11 = B)
- **key_confidence**: Confidence level for key estimation (0.0 to 1.0)
- **mode**: Modality (0 = minor, 1 = major)
- **mode_confidence**: Confidence level for mode estimation (0.0 to 1.0)
- **time_signature**: Estimated time signature (e.g., 4 for 4/4 time)
- **time_signature_confidence**: Confidence level for time signature estimation (0.0 to 1.0)
- **energy**: Overall energy of the song (0.0 to 1.0)
- **danceability**: Measure of how suitable a track is for dancing (0.0 to 1.0)

### Popularity Metrics
- **artist_hotttnesss**: Artist popularity measure (0.0 to 1.0, with more t's indicating hotness!)
- **song_hotttnesss**: Song popularity measure (0.0 to 1.0, may contain null values)

## Data Types:

- **song_id**: string
- **artist_id**: string
- **title**: string
- **artist_name**: string
- **release**: string
- **year**: integer
- **duration**: float
- **tempo**: float
- **loudness**: float
- **key**: integer
- **key_confidence**: float
- **mode**: integer
- **mode_confidence**: float
- **time_signature**: integer
- **time_signature_confidence**: float
- **energy**: float
- **danceability**: float
- **artist_hotttnesss**: float
- **song_hotttnesss**: float (nullable)

## Notes

- Missing years are coded as 0
- Some songs may have null values for `song_hotttnesss`
- Key values follow standard pitch class notation (C=0, C#=1, etc.)
- Confidence values closer to 1.0 indicate higher reliability of the estimation
- All audio features are computed using the Echo Nest analyzer