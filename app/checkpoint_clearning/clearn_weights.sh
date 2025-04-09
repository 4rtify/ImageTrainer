# Define paths for input and output files
WEIGHT_DIR_PATH="/home/user/ImageTrainer/logs/weights"
INPUT_CKPT="test_121_butts.ckpt"  # Replace with the actual checkpoint file path
CLEANED_CKPT="cleaned_${INPUT_CKPT}"  # Output path for the cleaned checkpoint
OUTPUT_PT="${CLEANED_CKPT%.ckpt}.pt"  # Output path for the converted .pt file

# Step 1: Clean the checkpoint using prepare_ckpt.py
echo "Cleaning the checkpoint..."
python /home/user/ImageTrainer/app/checkpoint_clearning/prepare_ckpt.py "$WEIGHT_DIR_PATH" "$INPUT_CKPT"

# Step 2: Convert the cleaned checkpoint to .pt format using convert_to_pt.py
echo "Converting the cleaned checkpoint to .pt format..."
python /home/user/ImageTrainer/app/checkpoint_clearning/convert_to_pt.py "${WEIGHT_DIR_PATH}/${CLEANED_CKPT}" "$OUTPUT_PT"

echo "✅ Checkpoint cleaning and conversion completed!"
echo "Cleaned checkpoint: $CLEANED_CKPT"
echo "Converted .pt file: $OUTPUT_PT"