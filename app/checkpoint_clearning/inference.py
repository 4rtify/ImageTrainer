import sys
from pathlib import Path

import torch
from hydra import compose, initialize
from PIL import Image 

project_root = Path().resolve()
sys.path.append(str(project_root))
print(project_root)

from yolo import (
    AugmentationComposer,
    Config,
    PostProcess,
    create_converter,
    create_model,
    draw_bboxes,
)

# Set the path to the folder containing the config files
CONFIG_PATH = "../../YOLO/yolo/config"
CONFIG_NAME = "config"
MODEL = "v9-s"
DEVICE = 'cpu'
CLASS_NUM = 1
IMAGE_PATH = '/home/user/ImageTrainer/YOLO/data/redi/cig_butts/images/train/00000005.jpg'
CUSTOM_MODEL_PATH = "/home/user/ImageTrainer/logs/weights/test_121_butts.ckpt"

device = torch.device(DEVICE)

with initialize(config_path=CONFIG_PATH, version_base=None, job_name="notebook_job"):
    cfg: Config = compose(config_name=CONFIG_NAME, overrides=["task=inference", f"task.data.source={IMAGE_PATH}", f"model={MODEL}", f"dataset=butt"])

    model = create_model(cfg.model, class_num=CLASS_NUM).to(device)
    cfg.task.nms.min_confidence = 0.05
    cfg.task.nms.min_iou = 0.1

    # Load the checkpoint
    state_dict = torch.load(CUSTOM_MODEL_PATH, map_location=device)["state_dict"]
    model.load_state_dict(state_dict)
    model.eval()

    # Debugging Step 1: Print model state_dict keys
    print("\nModel state_dict keys:")
    print(model.state_dict().keys())

    # Debugging Step 2: Print checkpoint state_dict keys
    print("\nCheckpoint state_dict keys:")
    print(state_dict.keys())

    transform = AugmentationComposer([], cfg.image_size)

    converter = create_converter(cfg.model.name, model, cfg.model.anchor, cfg.image_size, device)
    post_proccess = PostProcess(converter, cfg.task.nms)

pil_image = Image.open(IMAGE_PATH)
image, bbox, rev_tensor = transform(pil_image)

# Debugging Step 3: Print preprocessed image shape and values
print("\nPreprocessed image shape:", image.shape)
print("Preprocessed image values:", image)

image = image.to(device)[None]
rev_tensor = rev_tensor.to(device)[None]

with torch.no_grad():
    predict = model(image)

    # Debugging Step 4: Print raw predictions
    print("\nRaw predictions from the model:")
    print(predict)

    pred_bbox = post_proccess(predict, rev_tensor)

    # Debugging Step 5: Print processed bounding boxes
    print("\nProcessed bounding boxes:")
    print(pred_bbox)

# Debugging Step 6: Check bounding box coordinates
if pred_bbox:
    for bbox in pred_bbox:
        print("Bounding box coordinates:", bbox)
else:
    print("No bounding boxes detected.")

output_image = draw_bboxes(pil_image, pred_bbox, idx2label=cfg.dataset.class_list)

# Debugging Step 7: Display the output image with bounding boxes
output_image.show()

OUTPUT_PATH = 'output.jpg'  # Specify your output file path

# Save the image with the bounding boxes to the specified path
output_image.save(OUTPUT_PATH)
print("Class list:", cfg.dataset.class_list)
print(f"Output image saved at: {OUTPUT_PATH}")