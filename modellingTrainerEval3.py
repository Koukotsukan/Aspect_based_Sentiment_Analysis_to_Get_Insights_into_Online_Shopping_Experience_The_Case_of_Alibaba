from pyabsa import AspectTermExtraction as ATEPC
from pyabsa import ModelSaveOption, DeviceTypeOption
import warnings

# 获取英文的 ATEPC 配置
config = ATEPC.ATEPCConfigManager.get_atepc_config_english()

# 设置为纯 BERT 模型
config.model = ATEPC.ATEPCModelList.BERT_BASE_ATEPC

# 其他配置
import warnings
warnings.filterwarnings("ignore")

config.batch_size = 16
config.patience = 2
config.log_step = -1
config.seed = [1]
config.verbose = False  # 如果 verbose == True，PyABSA 将输出模型结构和一些处理过的数据示例
config.notice = "This is a training example for aspect term extraction"  # 备注信息

dataset = '100.CustomDataset'

trainer = ATEPC.ATEPCTrainer(
    config=config,
    dataset=dataset,
    from_checkpoint=None,  # 如果你想从我们预训练的检查点继续训练，可以在这里传入检查点名称
    auto_device=DeviceTypeOption.AUTO,  # 如果可用使用 CUDA
    checkpoint_save_mode=ModelSaveOption.SAVE_MODEL_STATE_DICT,  # 只保存状态字典而不是整个模型
    load_aug=False  # 如果设置 load_aug=True，可以使用一些集成数据集的增强数据集来提高性能
)

aspect_extractor = trainer.load_trained_model()
assert isinstance(aspect_extractor, ATEPC.AspectExtractor)
