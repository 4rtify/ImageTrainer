import torch
# add sys argument to load checkpoint path
import sys
if len(sys.argv) < 2:
    print("Usage: python convert_to_pt.py <checkpoint_path>")
    sys.exit(1)
checkpoint_path = sys.argv[1]
checkpoint_filename = checkpoint_path.split("/")[-1]

# Load the checkpoint
def convert_ckpt_to_pt(ckpt_path: str, output_path: str):
    # Load checkpoint
    checkpoint = torch.load(ckpt_path, map_location="cpu")

    # Extract model weights (assumes key is "state_dict")
    state_dict = checkpoint.get("state_dict", checkpoint)

    # Save as .pt file (weights only)
    torch.save(state_dict, output_path)
    print(f"Converted .ckpt to .pt: {output_path}")

# Call the function
ckpt_path = checkpoint_path
output_path = ckpt_path.replace(".ckpt", ".pt")
convert_ckpt_to_pt(ckpt_path, output_path)