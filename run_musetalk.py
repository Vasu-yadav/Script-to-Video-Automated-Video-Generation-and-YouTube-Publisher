from utils.script_generator.script_generator import ScriptGenerator
from utils.Musetalk import MuseTalk
import os
import time
from utils.uploadToYoutube.uploadToYoutube import upload_video
import uuid
import random
import json
from utils.video_metadata import VideoMetadata


script_generator = ScriptGenerator()
# Initialize the MuseTalk client
musetalk_client = MuseTalk(
    base_url="http://localhost:7860",
)
video_metadata = VideoMetadata()


def get_script(topic):
    """
    Generate a script based on the provided topic.
    
    Args:
        topic (str): The topic for which to generate the script.
        
    Returns:
        str: Generated script content.
    """
    # Generate a script based on the topic
    response = script_generator.process_query(topic)
    if response:
        return response.text
    return "Could not generate a response for your query."




if __name__ == "__main__":
    topic = "How to make a video"
    # output_script = script.get_script(topic)
    script_content = get_script(topic)
    
    print(f"Current UTC time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("Output script:", script_content)
    
    # Create an output folder if it doesn't exist
    output_folder = "outputs"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    speakers = musetalk_client.list_speakers()
    
    input_speaker = random.choice(speakers)
    print("Selected speaker:", input_speaker)
    
    unique_id = str(uuid.uuid4())
    output_file = os.path.join(output_folder, f"output_{unique_id}.mp4")
    
    # # Create a video
    musetalk_client.create_video(
        text=script_content,
        video_path=output_file,
        input_video_id = input_speaker['video_id'],
        gender=input_speaker['gender']
    )
    
    
    
    metadata_file = os.path.join(output_folder, f"metadata_{unique_id}.json")
    metadata = {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "topic": topic,
        "output_file": output_file
    }
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)
    
    # Upload the video to YouTube
    title = video_metadata.generate_video_title(script_content)
    description = video_metadata.generate_video_description(script_content)
    tags = video_metadata.generate_video_tags(script_content)
    upload_video(
        file_path=output_file,
        title=title, 
        description=description,  
        tags=tags, 
        privacy="unlisted"
    )