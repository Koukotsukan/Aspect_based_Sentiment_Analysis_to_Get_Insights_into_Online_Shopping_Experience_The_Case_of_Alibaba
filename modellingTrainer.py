from pyabsa import AspectTermExtraction as ATEPC
config = (
    ATEPC.ATEPCConfigManager.get_atepc_config_english()
)  # this config contains 'pretrained_bert', it is based on pretrained models
config.model = ATEPC.ATEPCModelList.FAST_LCF_ATEPC  # improved version of LCF-ATEPC

from pyabsa import ModelSaveOption, DeviceTypeOption
import warnings

warnings.filterwarnings("ignore")

config.batch_size = 16
config.patience = 2
config.log_step = -1
config.seed = [1]
config.verbose = False  # If verbose == True, PyABSA will output the model strcture and seversal processed data examples
config.notice = (
    "This is an training example for aspect term extraction"  # for memos usage
)

dataset = '100.CustomDataset'

trainer = ATEPC.ATEPCTrainer(
    config=config,
    dataset=dataset,
    from_checkpoint="english",  # if you want to resume training from our pretrained checkpoints, you can pass the checkpoint name here
    auto_device=DeviceTypeOption.AUTO,  # use cuda if available
    checkpoint_save_mode=ModelSaveOption.SAVE_MODEL_STATE_DICT,  # save state dict only instead of the whole model
    load_aug=False,  # there are some augmentation dataset for integrated datasets, you use them by setting load_aug=True to improve performance
)



aspect_extractor = trainer.load_trained_model()
assert isinstance(aspect_extractor, ATEPC.AspectExtractor)
