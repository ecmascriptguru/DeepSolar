""" Generate lists containing filepaths and labels for training, validation and evaluation. """
import pickle
import os.path
import random
import pandas as pd
from ..settings import Config


TRAIN_SET_DIR = os.path.join(Config.BASE_DIR, Config.TRAIN_SET_DIR_NAME)


class DataGenerator(object):
    """High Level Class to generate data to be used in validation & test
    """
    ##### generate training set #####
    train_set_list = []
    MAX_NEGATIVE_TRAIN_SAMPLE_COUNT = 320378
    MAX_POSSITIVE_TRAIN_SAMPLE_COUNT = 46091

    val_set_list = []
    test_set_list = []

    def __init__(self, **kwargs):
        self.MAX_POSSITIVE_TRAIN_SAMPLE_COUNT = kwargs.get(
            'max_possitive_train_sample_count', self.MAX_POSSITIVE_TRAIN_SAMPLE_COUNT)
        self.MAX_NEGATIVE_TRAIN_SAMPLE_COUNT = kwargs.get(
            'max_negative_train_sample_count', self.MAX_NEGATIVE_TRAIN_SAMPLE_COUNT)

    @property
    def property_name(self):
        return ''

    @property_name.setter
    def property_name(self, value):
        self.something = value

    def load_traning_datasets(self):
        pos_num = 0
        neg_num = 0
        # negative samples
        for i in range(1, self.MAX_NEGATIVE_TRAIN_SAMPLE_COUNT):
            img_path = os.path.join(TRAIN_SET_DIR, '0', str(i) + '.png')
            if not os.path.exists(img_path):
                continue
            self.train_set_list.append((img_path, [0]))
            neg_num += 1

        # positive samples
        for i in range(1, 46091):
            img_path = os.path.join(TRAIN_SET_DIR, '1', str(i)+'.png')
            if not os.path.exists(img_path):
                continue
            self.train_set_list.append((img_path, [1]))
            pos_num += 1

        random.shuffle(self.train_set_list)

        with open('train_set_list.pickle', 'wb') as f:
            pickle.dump(self.train_set_list, f)

        print ('Train set list done. # positive samples: ' + str(pos_num) + ' # negative samples: ' + str(neg_num))

    def load_validation_datasets(self):
        ##### generate validation set #####
        VAL_SET_DIR = 'SPI_val'
        
        pos_num = 0
        neg_num = 0
        # negative samples
        for i in range(1, 227):
            img_path = os.path.join(VAL_SET_DIR, '0', str(i)+'.png')
            if not os.path.exists(img_path):
                continue
            self.val_set_list.append((img_path, [0]))
            neg_num += 1

        # positive samples
        for i in range(1, 12761):
            img_path = os.path.join(VAL_SET_DIR, '1', str(i)+'.png')
            if not os.path.exists(img_path):
                continue
            self.val_set_list.append((img_path, [1]))
            pos_num += 1

        with open('val_set_list.pickle', 'wb') as f:
            pickle.dump(self.val_set_list, f)

        print ('Validation set list done. # positive samples: '+str(pos_num)+' # negative samples: '+str(neg_num))

    def load_test_datasets(self):
        ##### generate test set #####
        TEST_SET_DIR = 'SPI_eval'
        
        pos_num = 0
        neg_num = 0
        eval_set_meta = pd.read_csv(os.path.join(TEST_SET_DIR, 'eval_set_meta.csv')).values
        for index in range(1, 66):
            region_type = eval_set_meta[index-1, 5] # get the type of the regions
            region_dir = os.path.join(TEST_SET_DIR, str(index))

            # negative samples
            for i in range(1, 3001):
                img_path = os.path.join(region_dir, '0', str(i) + '.png')
                if not os.path.exists(img_path):
                    continue
                neg_num += 1
                self.test_set_list.append((img_path, [0], index, i, region_type))

            # positive samples
            for i in range(1, 3001):
                img_path = os.path.join(region_dir, '1', str(i) + '.png')
                if not os.path.exists(img_path):
                    continue
                pos_num += 1
                self.test_set_list.append((img_path, [1], index, i, region_type))

        with open('test_set_list.pickle', 'wb') as f:
            pickle.dump(self.test_set_list, f)

        print ('Test set list done. # positive samples: '+str(pos_num)+' # negative samples: '+str(neg_num))

    def run(self):
        self.load_traning_datasets()
        self.load_validation_datasets()
        self.load_test_datasets()


if __name__ == "__main__":
    print("Something went wrong. You can't execute this directly.")
