from utils.HeyGenClient import HeyGenClient
import os
import utils.script as script
from utils.uploadToYoutube.uploadToYoutube import upload_video

client = HeyGenClient()

def main():
    # Generate a script based on the topic
    topic = "Debate of GoAT of footbal" #automate this
    script_content = script.get_script(topic)
    
    # Download the generated video
    client.generate_and_download_video(
        input_text=script_content,
        output_path="output.mp4",
        avatar_id="05ff47bf08f74d8d9161aae0c003f53b",
        voice_id="0d4d97379a6746baa5dfc692b37774d4",
        width=720,
        height=1280
    )
    # Upload the video to YouTube
    upload_video(
        file_path="output.mp4",
        title="US China tarrif war", #automate this
        description="China attacks US Luxury brands by exposing their true manufacturing costs", #automate this
        tags=["Tarrif", "upload", "api"], #automate this
        privacy="unlisted"
    )
if __name__ == "__main__":
    main()