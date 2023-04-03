import os
import pickle

class DatasetLoader:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def load_dataset(self, dataset_name):
        dataset_path = os.path.join(self.folder_path, dataset_name)
        with open(dataset_path, 'rb') as f:
            dataset = pickle.load(f)
        return dataset
