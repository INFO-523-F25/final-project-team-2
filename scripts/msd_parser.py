"""
The raw HDF5 files cannot be added to the codespace due to a nested folder structure.
This script allowed us to parse the data and save it in a .csv we were then able to add to our codespace.
This script extracts relevant audio features and metadata into a single tabular format suitable for analysis.
"""


import os
import h5py
import pandas as pd
import numpy as np
from pathlib import Path
from tqdm import tqdm

def extract_song_features(h5_file):
    """
    Extract ALL available features from a single h5 file.
    Returns a dictionary with comprehensive song attributes.
    """
    try:
        with h5py.File(h5_file, 'r') as f:
            song_data = {}
            
            # ===== METADATA =====
            song_data['song_id'] = f['metadata']['songs']['song_id'][0].decode('utf-8')
            song_data['title'] = f['metadata']['songs']['title'][0].decode('utf-8')
            song_data['artist_name'] = f['metadata']['songs']['artist_name'][0].decode('utf-8')
            song_data['artist_id'] = f['metadata']['songs']['artist_id'][0].decode('utf-8')
            song_data['release'] = f['metadata']['songs']['release'][0].decode('utf-8')
            song_data['artist_mbid'] = f['metadata']['songs']['artist_mbid'][0].decode('utf-8') if f['metadata']['songs']['artist_mbid'][0] else ''
            song_data['artist_playmeid'] = int(f['metadata']['songs']['artist_playmeid'][0])
            song_data['artist_7digitalid'] = int(f['metadata']['songs']['artist_7digitalid'][0])
            song_data['track_7digitalid'] = int(f['metadata']['songs']['track_7digitalid'][0])
            
            # ===== MUSICBRAINZ DATA =====
            song_data['year'] = int(f['musicbrainz']['songs']['year'][0])
            
            # ===== ANALYSIS FEATURES =====
            song_data['duration'] = float(f['analysis']['songs']['duration'][0])
            song_data['end_of_fade_in'] = float(f['analysis']['songs']['end_of_fade_in'][0])
            song_data['start_of_fade_out'] = float(f['analysis']['songs']['start_of_fade_out'][0])
            song_data['tempo'] = float(f['analysis']['songs']['tempo'][0])
            song_data['loudness'] = float(f['analysis']['songs']['loudness'][0])
            song_data['key'] = int(f['analysis']['songs']['key'][0])
            song_data['key_confidence'] = float(f['analysis']['songs']['key_confidence'][0])
            song_data['mode'] = int(f['analysis']['songs']['mode'][0])
            song_data['mode_confidence'] = float(f['analysis']['songs']['mode_confidence'][0])
            song_data['time_signature'] = int(f['analysis']['songs']['time_signature'][0])
            song_data['time_signature_confidence'] = float(f['analysis']['songs']['time_signature_confidence'][0])
            song_data['energy'] = float(f['analysis']['songs']['energy'][0])
            song_data['danceability'] = float(f['analysis']['songs']['danceability'][0])
            
            # ===== POPULARITY METRICS =====
            song_data['artist_hotttnesss'] = float(f['metadata']['songs']['artist_hotttnesss'][0]) if f['metadata']['songs']['artist_hotttnesss'][0] != b'' else np.nan
            song_data['song_hotttnesss'] = float(f['metadata']['songs']['song_hotttnesss'][0]) if f['metadata']['songs']['song_hotttnesss'][0] != b'' else np.nan
            song_data['artist_familiarity'] = float(f['metadata']['songs']['artist_familiarity'][0]) if f['metadata']['songs']['artist_familiarity'][0] != b'' else np.nan
            
            # ===== SEGMENT TIMBRE FEATURES (Averages) =====
            # Timbre describes the texture/color of sound - very useful for genre classification
            if 'segments_timbre' in f['analysis']:
                timbre_data = f['analysis']['segments_timbre'][:]
                if len(timbre_data) > 0:
                    timbre_avg = np.mean(timbre_data, axis=0)
                    timbre_std = np.std(timbre_data, axis=0)
                    for i in range(12):
                        song_data[f'timbre_avg_{i}'] = float(timbre_avg[i])
                        song_data[f'timbre_std_{i}'] = float(timbre_std[i])
                else:
                    for i in range(12):
                        song_data[f'timbre_avg_{i}'] = np.nan
                        song_data[f'timbre_std_{i}'] = np.nan
            else:
                for i in range(12):
                    song_data[f'timbre_avg_{i}'] = np.nan
                    song_data[f'timbre_std_{i}'] = np.nan
            
            # ===== SEGMENT PITCH/CHROMA FEATURES (Averages) =====
            # Pitch features represent the 12 chromatic pitches
            if 'segments_pitches' in f['analysis']:
                pitch_data = f['analysis']['segments_pitches'][:]
                if len(pitch_data) > 0:
                    pitch_avg = np.mean(pitch_data, axis=0)
                    pitch_std = np.std(pitch_data, axis=0)
                    for i in range(12):
                        song_data[f'pitch_avg_{i}'] = float(pitch_avg[i])
                        song_data[f'pitch_std_{i}'] = float(pitch_std[i])
                else:
                    for i in range(12):
                        song_data[f'pitch_avg_{i}'] = np.nan
                        song_data[f'pitch_std_{i}'] = np.nan
            else:
                for i in range(12):
                    song_data[f'pitch_avg_{i}'] = np.nan
                    song_data[f'pitch_std_{i}'] = np.nan
            
            # ===== STRUCTURAL COUNTS =====
            song_data['num_segments'] = len(f['analysis']['segments_start'][:]) if 'segments_start' in f['analysis'] else 0
            song_data['num_sections'] = len(f['analysis']['sections_start'][:]) if 'sections_start' in f['analysis'] else 0
            song_data['num_bars'] = len(f['analysis']['bars_start'][:]) if 'bars_start' in f['analysis'] else 0
            song_data['num_beats'] = len(f['analysis']['beats_start'][:]) if 'beats_start' in f['analysis'] else 0
            song_data['num_tatums'] = len(f['analysis']['tatums_start'][:]) if 'tatums_start' in f['analysis'] else 0
            
            # ===== SEGMENT STATISTICS =====
            if 'segments_start' in f['analysis'] and len(f['analysis']['segments_start'][:]) > 1:
                seg_starts = f['analysis']['segments_start'][:]
                seg_durations = np.diff(seg_starts)
                song_data['avg_segment_duration'] = float(np.mean(seg_durations))
                song_data['std_segment_duration'] = float(np.std(seg_durations))
            else:
                song_data['avg_segment_duration'] = np.nan
                song_data['std_segment_duration'] = np.nan
            
            # ===== SEGMENT LOUDNESS STATISTICS =====
            if 'segments_loudness_max' in f['analysis']:
                loudness_max = f['analysis']['segments_loudness_max'][:]
                if len(loudness_max) > 0:
                    song_data['avg_loudness_max'] = float(np.mean(loudness_max))
                    song_data['std_loudness_max'] = float(np.std(loudness_max))
                else:
                    song_data['avg_loudness_max'] = np.nan
                    song_data['std_loudness_max'] = np.nan
            else:
                song_data['avg_loudness_max'] = np.nan
                song_data['std_loudness_max'] = np.nan
            
            # ===== ARTIST TERMS (Genre-like tags) =====
            # These are crucial for classification!
            if 'artist_terms' in f['metadata']:
                terms = f['metadata']['artist_terms'][:]
                # Get up to top 5 terms
                terms_list = [term.decode('utf-8') if isinstance(term, bytes) else str(term) for term in terms[:5]]
                for i in range(5):
                    if i < len(terms_list):
                        song_data[f'artist_term_{i+1}'] = terms_list[i]
                    else:
                        song_data[f'artist_term_{i+1}'] = ''
                
                # Get term weights if available
                if 'artist_terms_weight' in f['metadata']:
                    weights = f['metadata']['artist_terms_weight'][:]
                    for i in range(5):
                        if i < len(weights):
                            song_data[f'artist_term_weight_{i+1}'] = float(weights[i])
                        else:
                            song_data[f'artist_term_weight_{i+1}'] = np.nan
                else:
                    for i in range(5):
                        song_data[f'artist_term_weight_{i+1}'] = np.nan
            else:
                for i in range(5):
                    song_data[f'artist_term_{i+1}'] = ''
                    song_data[f'artist_term_weight_{i+1}'] = np.nan
            
            # ===== SIMILAR ARTISTS =====
            if 'similar_artists' in f['metadata']:
                similar = f['metadata']['similar_artists'][:]
                similar_list = [s.decode('utf-8') if isinstance(s, bytes) else str(s) for s in similar[:3]]
                for i in range(3):
                    if i < len(similar_list):
                        song_data[f'similar_artist_{i+1}'] = similar_list[i]
                    else:
                        song_data[f'similar_artist_{i+1}'] = ''
            else:
                for i in range(3):
                    song_data[f'similar_artist_{i+1}'] = ''
            
            return song_data
            
    except Exception as e:
        print(f"Error processing {h5_file}: {e}")
        return None

def parse_msd_subset(data_path, max_files=None):
    """
    Parse all h5 files in the Million Song Dataset subset.
    
    Parameters:
    -----------
    data_path : str or Path
        Path to the root directory of the MSD subset
    max_files : int, optional
        Maximum number of files to process (useful for testing)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame containing all song features
    """
    data_path = Path(data_path)
    
    # Find all h5 files
    h5_files = list(data_path.rglob('*.h5'))
    print(f"Found {len(h5_files)} h5 files")
    
    if max_files:
        h5_files = h5_files[:max_files]
        print(f"Processing first {max_files} files")
    
    # Extract features from all files
    songs_data = []
    for h5_file in tqdm(h5_files, desc="Processing songs"):
        song_features = extract_song_features(h5_file)
        if song_features:
            songs_data.append(song_features)
    
    # Create DataFrame
    df = pd.DataFrame(songs_data)
    print(f"\nSuccessfully processed {len(df)} songs")
    print(f"DataFrame shape: {df.shape}")
    print(f"Total columns: {len(df.columns)}")
    
    return df

# Example usage
if __name__ == "__main__":
    # Update this path to your MSD subset location
    DATA_PATH = "/Users/krosema@arizona.edu/Downloads/MillionSongSubset"
    
    # Process first 100 files as a test
    print("Testing with 100 files first...")
    df_test = parse_msd_subset(DATA_PATH, max_files=100)
    
    # Display basic info
    print("\nColumn names:")
    print(df_test.columns.tolist())
    
    print("\nFirst few rows (first 10 columns):")
    print(df_test.iloc[:, :10].head())
    
    print("\nDataFrame info:")
    print(df_test.info())
    
    # If test looks good, process all files
    response = input("\nTest successful! Process all files? (y/n): ")
    if response.lower() == 'y':
        print("\nProcessing all files...")
        df_full = parse_msd_subset(DATA_PATH)
        
        # Save to CSV
        output_file = '/Users/krosema@arizona.edu/Downloads/msd_subset_features.csv'
        df_full.to_csv(output_file, index=False)
        print(f"\nSaved complete dataset to {output_file}")
        print(f"Final shape: {df_full.shape}")
    else:
        print("\nTest data saved for inspection")
        df_test.to_csv('/Users/krosema@arizona.edu/Downloads/msd_subset_features.csv', index=False)