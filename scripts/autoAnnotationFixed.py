from pyabsa import make_ABSA_dataset
from pyabsa.utils import convert_apc_set_to_atepc_set
from pyabsa import ABSADatasetList

# from apc to apetc
convert_apc_set_to_atepc_set(
    "100.CustomDataset"
)  # for custom datasets, absolute path recommended for this function

# make ABSA dataset annotation
make_ABSA_dataset(dataset_name_or_path='../Dataset/ali-train.csv', checkpoint='english')
make_ABSA_dataset(dataset_name_or_path='../Dataset/ali-test.csv', checkpoint='english')