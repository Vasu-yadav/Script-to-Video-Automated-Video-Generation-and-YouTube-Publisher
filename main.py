from utils.HeyGenClient import HeyGenClient
import os
import utils.script as script
from utils.uploadToYoutube.uploadToYoutube import upload_video
from dotenv import load_dotenv
import uuid
import time
import json
import random

load_dotenv()
# Load environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = HeyGenClient()

def load_avatars():
    """
    Load avatars from the JSON file.
    
    Returns:
        dict: Dictionary containing avatar information.
    """
    with open('utils/HeyGenAvaters.json', 'r') as file:
        return json.load(file)

def get_random_avatar(avatars):
    """
    Select a random avatar from the available avatars.
    
    Args:
        avatars (dict): Dictionary containing avatar information.
        
    Returns:
        tuple: Name of the selected avatar and its data.
    """
    avatar_name = random.choice(list(avatars.keys()))
    return avatar_name, avatars[avatar_name]

def main():
    
    print(f"Current UTC time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    # Generate a script based on the topic
    
    
    topic = "Debate of GoAT of footbal"  # automate this
    script_content = script.get_script(topic)
    
    # Create an output folder if it doesn't exist
    output_folder = "outputs"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Generate a unique file name using UUID and save it in the output folder
    unique_id = str(uuid.uuid4())
    output_file = os.path.join(output_folder, f"output_{unique_id}.mp4")
    
    # Select a random avatar
    avatars = load_avatars()
    avatar_name, avatar_data = get_random_avatar(avatars)
    
    print(f"Selected avatar: {avatar_name}")
    print("Starting video generation process...")
    
    # Download the generated video using the selected avatar
    client.generate_and_download_video(
        input_text=script_content,
        output_path=output_file,
        avatar_id=avatar_data["avater_id"],
        voice_id=avatar_data["voide_id"],
        width=720,
        height=1280
    )
    print(f"Video downloaded successfully to {output_file}")
    
    # Save metadata about the generation
    metadata_file = os.path.join(output_folder, f"metadata_{unique_id}.json")
    metadata = {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "topic": topic,
        "avatar_used": avatar_name,
        "output_file": output_file
    }
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)
    
    # Upload the video to YouTube
    upload_video(
        file_path=output_file,
        title="US China tarrif war",  # automate this
        description="China attacks US Luxury brands by exposing their true manufacturing costs",  # automate this
        tags=["Tarrif", "upload", "api"],  # automate this
        privacy="unlisted"
    )

if __name__ == "__main__":
    main()