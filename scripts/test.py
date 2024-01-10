# from pyabsa import AspectPolarityClassification as APC
# from pyabsa import DatasetItem
# # config = APC.APCConfigManager.get_apc_config_glove()  # get pre-defined configuration for GloVe model, the default embed_dim=300
# # config = APC.APCConfigManager.get_apc_config_multilingual()  # this config contains 'pretrained_bert', it is based on pretrained models
# config = APC.APCConfigManager.get_apc_config_english()
#
# from pyabsa import ModelSaveOption, DeviceTypeOption
#
#
# config.num_epoch = 1
# config.model = APC.APCModelList.FAST_LSA_T_V2
# trainer = APC.APCTrainer(
#     config=config,
#     dataset='100.CustomDataset',
#     from_checkpoint="english",
#     # if you want to resume training from our pretrained checkpoints, you can pass the checkpoint name here
#     auto_device=DeviceTypeOption.AUTO,
#     path_to_save=None,  # set a path to save checkpoints, if it is None, save checkpoints at 'checkpoints' folder
#     checkpoint_save_mode=ModelSaveOption.SAVE_MODEL_STATE_DICT,
#     load_aug=False,
#     # there are some augmentation dataset for integrated datasets, you use them by setting load_aug=True to improve performance
# )

from pyabsa import ModelSaveOption, DeviceTypeOption
import warnings
from pyabsa import AspectTermExtraction as ATEPC
config = (
    ATEPC.ATEPCConfigManager.get_atepc_config_english()
)  # this config contains 'pretrained_bert', it is based on pretrained models
config.model = ATEPC.ATEPCModelList.FAST_LCF_ATEPC  # improved version of LCF-ATEPC

warnings.filterwarnings("ignore")

config.batch_size = 16
config.patience = 2
config.log_step = -1
config.seed = [1]
config.verbose = False  # If verbose == True, PyABSA will output the model strcture and seversal processed data examples
config.notice = (
    "This is an training example for aspect term extraction and modified"  # for memos usage
)

trainer = ATEPC.ATEPCTrainer(
    config=config,
    dataset='100.CustomDataset',
    # dataset='118.TShirt',
    from_checkpoint="",  # if you want to resume training from our pretrained checkpoints, you can pass the checkpoint name here
    auto_device=DeviceTypeOption.AUTO,  # use cuda if available
    checkpoint_save_mode=ModelSaveOption.SAVE_MODEL_STATE_DICT,  # save state dict only instead of the whole model
    #checkpoint_save_mode=0,
    load_aug=False,  # there are some augmentation dataset for integrated datasets, you use them by setting load_aug=True to improve performance
)