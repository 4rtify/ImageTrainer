python app/download_script.py crlab data/ YOLO/
python app/deletefiles.py
# python app/train.py task=train dataset=garment cpu_num=5 task.data.batch_size=8 model=v9-s use_wandb=False
python app/train.py task=train dataset=butt cpu_num=1 task.data.batch_size=8 model=v9-s weight=False use_wandb=True
python app/upload_weights.py crlab redi/ runs/