from utils.HeyGenClient import HeyGenClient
import os
import utils.script as script
from utils.uploadToYoutube.uploadToYoutube import upload_video
from dotenv import load_dotenv
import uuid
import time
# import utils.system_prompts as system_prompts
# from google import genai


load_dotenv()
# Load environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = HeyGenClient()

# def title_generation(topic):
#     """
#     Generate a title for the video based on the topic.
    
#     Args:
#         topic (str): The topic to generate a title for.
        
#     Returns:
#         str: The generated title.
#     """
#     PROMPT = f"""
#                 {system_prompts.TITLE_GENERATOR_MSG}
#                 USER TOPIC: {topic}
#             """
#     response = self.client.models.generate_content(
#         model="gemini-2.0-flash", contents=PROMPT,
#     )
#     return f"Video about {topic}"

# def description_generation(topic):
#     """
#     Generate a description for the video based on the topic.
    
#     Args:
#         topic (str): The topic to generate a description for.
        
#     Returns:
#         str: The generated description.
#     """
#     # Placeholder for description generation logic
#     return f"This is a video about {topic}"

# def tags_generation(topic):
#     """
#     Generate tags for the video based on the topic.
    
#     Args:
#         topic (str): The topic to generate tags for.
        
#     Returns:
#         list: The generated tags.
#     """
#     # Placeholder for tags generation logic
#     return [f"{topic} tag1", f"{topic} tag2"]

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
    
    print("Starting video generation process...")
    
    # Download the generated video
    client.generate_and_download_video(
        input_text=script_content,
        output_path=output_file,
        avatar_id="05ff47bf08f74d8d9161aae0c003f53b",
        voice_id="0d4d97379a6746baa5dfc692b37774d4",
        width=720,
        height=1280
    )
    print(f"Video downloaded successfully to {output_file}")
    
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