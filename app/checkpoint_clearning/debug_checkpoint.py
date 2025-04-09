import torch
from hydra import compose, initialize
from yolo import create_model

# Paths
CUSTOM_MODEL_PATH = "/home/user/ImageTrainer/logs/weights/cleaned_test_121_butts.pt"
CONFIG_PATH = "../../YOLO/yolo/config"
CONFIG_NAME = "config"
DEVICE = 'cpu'
CLASS_NUM = 1

# Initialize the device
device = torch.device(DEVICE)

# Step 1: Load the checkpoint
print(f"Loading checkpoint from: {CUSTOM_MODEL_PATH}")
try:
    checkpoint = torch.load(CUSTOM_MODEL_PATH, map_location=device)
    print("Checkpoint loaded successfully.")
except Exception as e:
    print(f"Error loading checkpoint: {e}")
    exit(1)

# Step 2: Inspect the checkpoint structure
print("\nInspecting checkpoint structure...")
if isinstance(checkpoint, dict):
    print(f"Checkpoint keys: {list(checkpoint.keys())}")
    if "state_dict" in checkpoint:
        state_dict = checkpoint["state_dict"]
    else:
        state_dict = checkpoint  # Assume weights are stored directly
else:
    print("Checkpoint is not a dictionary. Assuming it contains state_dict directly.")
    state_dict = checkpoint

# Check if the checkpoint is empty
if not state_dict:
    print("Error: The checkpoint is empty. Please verify the checkpoint file.")
    exit(1)

# Step 3: Initialize the model using Hydra configuration
print("\nInitializing the model...")
try:
    with initialize(config_path=CONFIG_PATH, version_base=None, job_name="debug_job"):
        cfg = compose(config_name=CONFIG_NAME, overrides=[f"model=v9-s", f"dataset=butt"])
        model = create_model(cfg.model, class_num=CLASS_NUM).to(device)
    print("Model initialized successfully.")
except Exception as e:
    print(f"Error initializing model: {e}")
    exit(1)

# Step 4: Compare state_dict keys
print("\nComparing state_dict keys...")
model_keys = set(model.state_dict().keys())
checkpoint_keys = set(state_dict.keys())

missing_keys = model_keys - checkpoint_keys
unexpected_keys = checkpoint_keys - model_keys

if missing_keys:
    print(f"\nMissing keys (present in the model but not in the checkpoint):")
    for key in missing_keys:
        print(key)
else:
    print("\nNo missing keys.")

if unexpected_keys:
    print(f"\nUnexpected keys (present in the checkpoint but not in the model):")
    for key in unexpected_keys:
        print(key)
else:
    print("\nNo unexpected keys.")

# Step 5: Attempt to load the state_dict
print("\nAttempting to load the state_dict into the model...")
try:
    model.load_state_dict(state_dict, strict=False)
    print("State_dict loaded successfully with strict=False.")
except Exception as e:
    print(f"Error loading state_dict: {e}")

# Step 6: Print final model state_dict keys
print("\nFinal model state_dict keys:")
print(model.state_dict().keys())