# Data

## Dataset Source

- **Million Song Dataset Subset**: A collection of 10,000 songs with audio features and metadata extracted from the Echo Nest API. This is a manageable subset of the full Million Song Dataset which contains 1 million tracks.
- **Source URL**: http://millionsongdataset.com/pages/getting-dataset/#subset
- **Original Format**: HDF5 (.h5) files organized in nested directories
- **Processed Format**: Single CSV file with extracted and aggregated features

## Data Processing

The raw HDF5 files were processed using `scripts/parse_msd.py` to extract all available audio features, metadata, and artist information. Time-series data (segment-by-segment measurements) were aggregated into summary statistics to create a single-row-per-song tabular format suitable for machine learning analysis.

# Codebook for Million Song Dataset (Full Features)

## Variable Names and Descriptions:

### Identifiers
- **song_id**: Unique identifier for each song (Echo Nest ID)
- **artist_id**: Unique identifier for the artist (Echo Nest ID)
- **artist_mbid**: MusicBrainz artist ID (empty string if unavailable)
- **artist_playmeid**: 7digital artist ID for Playme service
- **artist_7digitalid**: 7digital artist ID
- **track_7digitalid**: 7digital track ID

### Metadata
- **title**: Song title
- **artist_name**: Name of the performing artist
- **release**: Album or release name
- **year**: Year of release (0 indicates unknown)

### Audio Features (Summary Statistics)
- **duration**: Length of the song in seconds
- **end_of_fade_in**: Time when fade-in ends in seconds
- **start_of_fade_out**: Time when fade-out begins in seconds
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
- **artist_hotttnesss**: Artist popularity measure (0.0 to 1.0)
- **song_hotttnesss**: Song popularity measure (0.0 to 1.0, may contain null values)
- **artist_familiarity**: How well-known the artist is (0.0 to 1.0)

### Timbre Features (Texture/Color of Sound)
Aggregated from segment-level timbre data. Timbre describes the quality or color of sound that distinguishes different types of sound production.

- **timbre_avg_0** through **timbre_avg_11**: Average values for 12 timbre dimensions across all segments
- **timbre_std_0** through **timbre_std_11**: Standard deviation of timbre values across all segments

### Pitch/Chroma Features
Aggregated from segment-level pitch data. Represents the 12 chromatic pitch classes (C, C#, D, etc.).

- **pitch_avg_0** through **pitch_avg_11**: Average pitch class values across all segments
- **pitch_std_0** through **pitch_std_11**: Standard deviation of pitch values across all segments

### Structural Information
- **num_segments**: Total number of segments in the song (typically 100-500 per song)
- **num_sections**: Total number of sections (verse, chorus, bridge, etc.)
- **num_bars**: Total number of musical bars
- **num_beats**: Total number of beats
- **num_tatums**: Total number of tatums (smallest rhythmic subdivision)

### Segment Statistics
- **avg_segment_duration**: Average length of segments in seconds
- **std_segment_duration**: Variability in segment length (standard deviation)
- **avg_loudness_max**: Average peak loudness across segments in dB
- **std_loudness_max**: Variability in peak loudness across segments

### Artist Terms/Tags (Genre Descriptors)
Echo Nest tags that describe artist style, genre, and characteristics. Terms are ordered by relevance/weight.

- **artist_term_1** through **artist_term_5**: Top 5 descriptive terms for the artist (e.g., "rock", "indie", "alternative")
- **artist_term_weight_1** through **artist_term_weight_5**: Weight/importance of each term (0.0 to 1.0)

### Similar Artists
- **similar_artist_1** through **similar_artist_3**: Artist IDs of top 3 similar artists

## Data Types:

### String Variables
- song_id, artist_id, artist_mbid, title, artist_name, release
- artist_term_1, artist_term_2, artist_term_3, artist_term_4, artist_term_5
- similar_artist_1, similar_artist_2, similar_artist_3

### Integer Variables
- year, artist_playmeid, artist_7digitalid, track_7digitalid
- key, mode, time_signature
- num_segments, num_sections, num_bars, num_beats, num_tatums

### Float Variables (nullable)
- duration, end_of_fade_in, start_of_fade_out, tempo, loudness
- key_confidence, mode_confidence, time_signature_confidence
- energy, danceability
- artist_hotttnesss, song_hotttnesss, artist_familiarity
- timbre_avg_0 through timbre_avg_11
- timbre_std_0 through timbre_std_11
- pitch_avg_0 through pitch_avg_11
- pitch_std_0 through pitch_std_11
- avg_segment_duration, std_segment_duration
- avg_loudness_max, std_loudness_max
- artist_term_weight_1 through artist_term_weight_5

## Notes

- **Missing Data**: 
  - Years are coded as 0 when unknown
  - Some songs may have null/NaN values for song_hotttnesss, artist_hotttnesss, or artist_familiarity
  - Artist terms and similar artists may be empty strings if unavailable
  - Timbre and pitch aggregations will be NaN if segment data is unavailable

- **Key Values**: Follow standard pitch class notation (C=0, C#=1, D=2, ..., B=11)

- **Confidence Scores**: Values closer to 1.0 indicate higher reliability of the estimation

- **Timbre Dimensions**: The 12 timbre dimensions represent different aspects of sound texture derived from MFCCs (Mel-frequency cepstral coefficients). Higher dimensions generally correspond to finer spectral details.

- **Pitch Classes**: The 12 pitch values represent the chromatic scale (C, C#, D, D#, E, F, F#, G, G#, A, A#, B)

- **Artist Terms**: These are the most valuable features for genre classification tasks, as they represent human-annotated style descriptors

- **Aggregation**: All segment-level time-series data (timbre, pitch, loudness) has been aggregated using mean and standard deviation to create summary features

## Total Columns

The processed dataset contains approximately **100+ columns** with comprehensive audio analysis, metadata, and artist information for each song.