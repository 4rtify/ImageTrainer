python app/download_script.py crlab redi/ YOLO/data/
/bin/bash -c "cd /home/user/ImageTrainer/YOLO/ && python yolo/lazy.py task=train dataset=butt cpu_num=1 task.data.batch_size=8 model=v9-s use_wandb=True"
# python YOLO/yolo/lazy.py task=train dataset=butt cpu_num=5 task.data.batch_size=8 model=v9-s weight=False use_wandb=True
python app/upload_weights.py crlab redi YOLO/weights 