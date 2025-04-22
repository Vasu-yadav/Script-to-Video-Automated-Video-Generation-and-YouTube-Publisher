#!/bin/bash
# filepath: /ext_disk/videoGAN/Script_to_video/run_main.sh

# Activate the virtual environment
source /ext_disk/videoGAN/Script_to_video/.venv/bin/activate

# Run the Python script
python /ext_disk/videoGAN/Script_to_video/run_musetalk.py --upload >> /ext_disk/videoGAN/Script_to_video/cron.log 2>&1

echo  -e "\n\n\n" >> cron.log