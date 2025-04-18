from utils.HeyGenClient import HeyGenClient
import os
from utils.script_generator.script_generator import ScriptGenerator
from utils.uploadToYoutube.uploadToYoutube import upload_video
from utils.video_metadata import VideoMetadata
from dotenv import load_dotenv
import uuid
import time
import json
import random

load_dotenv()
# Load environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = HeyGenClient()
script_generator = ScriptGenerator()
script_generator.set_debug(True)
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

def load_topics():
    """
    Load topics from the JSON file.
    
    Returns:
        list: List containing topics.
    """
    topics_file = 'utils/video_topics.json'
    if os.path.exists(topics_file):
        with open(topics_file, 'r') as file:
            return json.load(file)
    else:
        print(f"Warning: Topics file not found at {topics_file}")
        return {"topics": ["Debate of GoAT of football"]}  # Default topic as fallback

def get_random_topic(topics_data):
    """
    Select a random topic from the available topics.
    
    Args:
        topics_data (dict): Dictionary containing topics list.
        
    Returns:
        str: Selected topic.
    """
    topics = topics_data.get("topics", [])
    if not topics:
        print("No topics available in the topics file.")
        return "Debate of GoAT of football"  # Default topic as fallback
    
    return random.choice(topics)

def remove_used_topic(topic, topics_data):
    """
    Remove a topic from the topics list after it has been used.
    
    Args:
        topic (str): The topic to remove.
        topics_data (dict): Dictionary containing topics list.
        
    Returns:
        dict: Updated topics data.
    """
    if "topics" in topics_data and topic in topics_data["topics"]:
        topics_data["topics"].remove(topic)
        # Save the updated topics list back to the file
        with open('utils/video_topics.json', 'w') as file:
            json.dump(topics_data, file, indent=4)
        print(f"Topic '{topic}' has been removed from the topics list.")
    return topics_data

def main():
    
    print(f"Current UTC time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load topics data
    topics_data = load_topics()
    
    # Try to generate a script with a valid topic
    max_attempts = 3
    attempts = 0
    script_content = None
    topic = None
    
    while attempts < max_attempts and script_content is None:
        # Select a random topic
        if not topics_data.get("topics", []):
            print("No more topics available in the topics list.")
            break
            
        topic = get_random_topic(topics_data)
        print(f"Attempt {attempts+1}: Selected topic: {topic}")
        
        # Generate a script based on the selected topic
        script_content = get_script(topic)
        
        # Check if script generation was successful
        if script_content == "Could not generate a response for your query.":
            print(f"Failed to generate script for topic: '{topic}'. Removing it and trying another topic.")
            remove_used_topic(topic, topics_data)
            script_content = None
            attempts += 1
        else:
            print(f"Successfully generated script for topic: '{topic}'")
            remove_used_topic(topic, topics_data)
    
    # If all attempts failed, exit the program
    if script_content is None or script_content == "Could not generate a response for your query.":
        print("Failed to generate a script after multiple attempts. Exiting program.")
        return
    
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

if __name__ == "__main__":
    main()