import sys
from pathlib import Path

import hydra
from lightning import Trainer

sys.path.append("/home/user/ImageTrainer/YOLO")

from yolo.config.config import Config
from yolo.tools.solver import InferenceModel, TrainModel, ValidateModel
from yolo.utils.logging_utils import setup
import torch


@hydra.main(config_path="../YOLO/yolo/config", config_name="config", version_base=None)
def main(cfg: Config):
    callbacks, loggers, save_path = setup(cfg)

    # if not loggers:
    #     loggers = TensorBoardLogger("logs", name="my_model")
    
    trainer = Trainer(
        accelerator="auto",
        max_epochs=getattr(cfg.task, "epoch", None),
        precision="16-mixed",
        callbacks=callbacks,
        logger=loggers,
        log_every_n_steps=1,
        gradient_clip_val=10,
        gradient_clip_algorithm="value",
        deterministic=True,
        enable_progress_bar=not getattr(cfg, "quite", False),
        default_root_dir=save_path,
    )
    if cfg.task.task == "train":
        model = TrainModel(cfg)
        trainer.fit(model)
    if cfg.task.task == "validation":
        model = ValidateModel(cfg)
        trainer.validate(model)
    if cfg.task.task == "inference":
        model = InferenceModel(cfg) 
        trainer.predict(model)         

if __name__ == "__main__":
    main()