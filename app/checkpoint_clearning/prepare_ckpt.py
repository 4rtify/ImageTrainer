import torch
#add sys argument to load checkpoint path
import sys
if len(sys.argv) < 2:
    print("Usage: python prepare_ckpt.py <checkpoint_path> <checkpoint_filename>")
    sys.exit(1)
checkpoint_path = sys.argv[1]
checkpoint_filename = sys.argv[2]
# Load the checkpoint
checkpoint = torch.load(checkpoint_path+"/"+checkpoint_filename, map_location="cpu")  # Load on CPU for safety
state_dict = checkpoint["state_dict"]
# Create a new state_dict with only EMA weights (renaming them)
new_state_dict = {}

for key, value in state_dict.items():
    if key.startswith("ema.model"):  # Keep only EMA weights
        new_key = key.replace("ema.model", "model")  # Rename 'ema.model' → 'model'
        new_state_dict[new_key] = value
    # Skip "model.model" weights

# Create a new checkpoint dictionary with cleaned state_dict
cleaned_checkpoint = {
    "epoch": checkpoint["epoch"],  # Keep epoch info
    "global_step": checkpoint["global_step"],  # Keep global step info
    "pytorch-lightning_version": checkpoint["pytorch-lightning_version"],  # Keep version
    "state_dict": new_state_dict,  # Use the filtered EMA weights
    "loops": checkpoint.get("loops", None),  # Keep training loops if available
    "callbacks": checkpoint.get("callbacks", None),  # Keep callbacks
    "optimizer_states": checkpoint.get("optimizer_states", None),  # Keep optimizer state
    "lr_schedulers": checkpoint.get("lr_schedulers", None),  # Keep LR scheduler
    "MixedPrecision": checkpoint.get("MixedPrecision", None),  # Keep precision settings
}

# Save the cleaned checkpoint
total_path = checkpoint_path + "/" + checkpoint_filename
cleaned_checkpoint_path = total_path.replace(checkpoint_filename, "cleaned_" + checkpoint_filename)
torch.save(cleaned_checkpoint, cleaned_checkpoint_path)

print(f"✅ Cleaned checkpoint saved to: {cleaned_checkpoint_path}")