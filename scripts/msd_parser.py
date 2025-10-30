"""
The raw HDF5 files cannot be added to the codespace due to a nested folder structure.
This script allowed us to parse the data and save it in a .csv we were then able to add to our codespace.
This script extracts relevant audio features and metadata into a single tabular format suitable for analysis.
"""


import os
import h5py
import pandas as pd
from pathlib import Path
from tqdm import tqdm

def extract_song_features(h5_file):
    """
    Extract features from a single h5 file.
    Returns a dictionary with song attributes.
    """
    try:
        with h5py.File(h5_file, 'r') as f:
            # Metadata features
            song_data = {
                'song_id': f['metadata']['songs']['song_id'][0].decode('utf-8'),
                'title': f['metadata']['songs']['title'][0].decode('utf-8'),
                'artist_name': f['metadata']['songs']['artist_name'][0].decode('utf-8'),
                'artist_id': f['metadata']['songs']['artist_id'][0].decode('utf-8'),
                'release': f['metadata']['songs']['release'][0].decode('utf-8'),
                'year': int(f['musicbrainz']['songs']['year'][0]),
                
                # Audio analysis features
                'duration': float(f['analysis']['songs']['duration'][0]),
                'tempo': float(f['analysis']['songs']['tempo'][0]),
                'loudness': float(f['analysis']['songs']['loudness'][0]),
                'key': int(f['analysis']['songs']['key'][0]),
                'key_confidence': float(f['analysis']['songs']['key_confidence'][0]),
                'mode': int(f['analysis']['songs']['mode'][0]),
                'mode_confidence': float(f['analysis']['songs']['mode_confidence'][0]),
                'time_signature': int(f['analysis']['songs']['time_signature'][0]),
                'time_signature_confidence': float(f['analysis']['songs']['time_signature_confidence'][0]),
                
                # Additional features
                'artist_hotttnesss': float(f['metadata']['songs']['artist_hotttnesss'][0]),
                'song_hotttnesss': float(f['metadata']['songs']['song_hotttnesss'][0]) if f['metadata']['songs']['song_hotttnesss'][0] != b'' else None,
                'energy': float(f['analysis']['songs']['energy'][0]),
                'danceability': float(f['analysis']['songs']['danceability'][0]),
            }
            
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
    
    return df

# Example usage
if __name__ == "__main__":
    # Update this path to your MSD subset location
    DATA_PATH = "/Users/krosema@arizona.edu/Downloads/MillionSongSubset"
    
    # Save as df
    df = parse_msd_subset(DATA_PATH)

    # Save full df to CSV for easier future access
    df.to_csv('msd_subset_features.csv', index=False)
    print("\nSaved to msd_subset_features.csv")
    
    # Process first 100 files as a test
    df100 = parse_msd_subset(DATA_PATH, max_files=100)
    
    # Display basic info
    print("\nFirst few rows:")
    print(df100.head())
    
    print("\nDataFrame info:")
    print(df100.info())
    
    print("\nBasic statistics:")
    print(df100.describe())    
