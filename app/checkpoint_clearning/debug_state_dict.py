import torch

# Path to the state_dict_keys.txt file
state_dict_keys_file = "/home/user/ImageTrainer/state_dict_keys.txt"

# Function to load keys from the text file
def load_keys_from_file(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    # Extract keys (ignoring lines that don't contain keys)
    keys = [line.strip() for line in lines if line.startswith("model.")]
    return keys

# Load keys from the text file
file_keys = load_keys_from_file(state_dict_keys_file)
print(f"Loaded {len(file_keys)} keys from the file.")

# Load your model and its state_dict
# Replace `YourModel` with your actual model class
model = torch.nn.Module()  # Replace with your model initialization
model_state_dict = model.state_dict()
model_keys = list(model_state_dict.keys())
print(f"Model has {len(model_keys)} keys in its state_dict.")

# Compare keys
missing_keys = [key for key in model_keys if key not in file_keys]
unexpected_keys = [key for key in file_keys if key not in model_keys]

# Print debugging information
if missing_keys:
    print("\nMissing keys (present in the model but not in the file):")
    for key in missing_keys:
        print(key)
else:
    print("\nNo missing keys.")

if unexpected_keys:
    print("\nUnexpected keys (present in the file but not in the model):")
    for key in unexpected_keys:
        print(key)
else:
    print("\nNo unexpected keys.")