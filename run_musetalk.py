import utils.script as script 
from utils.Musetalk import MuseTalk
import os
import time
from utils.uploadToYoutube.uploadToYoutube import upload_video
import uuid

# Initialize the MuseTalk client
musetalk_client = MuseTalk(
    base_url="http://localhost:7860",
)


if __name__ == "__main__":
    topic = "How to make a video"
    output_script = script.get_script(topic)
    
    print(f"Current UTC time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("Output script:", output_script)
    
    # Create an output folder if it doesn't exist
    output_folder = "outputs"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    
    unique_id = str(uuid.uuid4())
    output_file = os.path.join(output_folder, f"output_{unique_id}.mp4")
    
    # Create a video
    musetalk_client.create_video(
        text=output_script,
        video_path=output_file,
        gender="Male"
    )
    
    # Upload the video to YouTube
    upload_video(
        file_path=output_file,
        title=topic,  # automate this
        description="How to make a video",  # automate this
        tags=["Education", "upload", "api"],  # automate this
        privacy="unlisted"
    )