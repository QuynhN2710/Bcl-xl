import unittest
from unittest.mock import mock_open, patch
import pandas as pd
class FileReader:
    """Base class for reading files."""
    def __init__(self, filename) -> None:
        self.filename = filename
        self.data = None

    def open(self):
        """Open the file and call the read_data method"""
        try:
            with open(self.filename,'r') as file:
                self.read_data(file)
        except FileNotFoundError:
            print(f"File {self.filename} not found.")
        except Exception as e:
            print(f"An error occured: {e}")
    
    def read_data(self, file):
        """Method to be implemented by subclasses to read data from file."""
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_data(self):
        if self.data is not None:
            return self.data
        else:
            print("No data available")
            return None
    
class PSFReader(FileReader):
    '''Class to read PSF files and process atomic data.'''
    def read_data(self,file):
        self._find_start_marker(file)
        index, resid, resname = self._read_atom_data(file)
        df = self._create_data_frame(index, resid, resname)
        self.data = self._format_data_frame(df)

    def _find_start_marker(self, file):
        start_marker = "!NATOM"
        for line in file:
            if start_marker in line:
                break
    
    def _read_atom_data(self,file):
        index, resid, resname = [], [], []
        for line in file:
            if not line.strip():
                print("Reached the end of !NATOM")
                break
            parts = line.split()
            index.append(parts[0])
            resid.append(parts[2])
            resname.append(parts[3])
        return index, resid, resname
    
    def _create_data_frame(self, index, resid, resname):
        return pd.DataFrame({
            'index': index,
            'resid': resid,
            'resname': resname
        })
    
    def _format_data_frame(self,df):
        df['index'] = df['index'].astype(int)
        df['resid'] = df['resid'].astype(int)
        df['resname'] = df['resname'].astype(str)
        return df

class ContactFileReader(FileReader):
    def read_data(self,file):
        frames, index_1, index_2 = self._read_lines(file)
        df = self._create_data_frame(frames, index_1, index_2)
        self.data = self._format_data_frame(df)

    def _read_lines(self, file):
        frames, index_1, index_2 = [], [], []
        for line in file:
            parts = line.split()
            frame = parts[0]
            i = 2
            while i < len(parts):
                frames.append(frame)
                index_1.append(parts[i])
                index_2.append(parts[i+1])
                i = i+2
        return frames, index_1, index_2
    
    def _create_data_frame(self, frames, index_1, index_2):
        df = pd.DataFrame({
            'frame': frames,
            'Index 1': index_1,
            'Index 2': index_2
        })
        return df
    
    def _format_data_frame(self,df):
        df['frame'] = df['frame'].astype(int)
        df['Index 1'] = df['Index 1'].astype(int)
        df['Index 2'] = df['Index 2'].astype(int)
        return df
    
    


