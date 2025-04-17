import requests
import dotenv
import os
import time
import json
from typing import Dict, Any, Optional

# Load environment variables
dotenv.load_dotenv()

class HeyGenClient:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the HeyGen API client.
        
        Args:
            api_key: Optional API key. If not provided, will try to get it from environment variable.
        """
        self.api_key = api_key or os.getenv("HEY_GEN_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set HEYGEN_API_KEY environment variable or pass it directly.")
        
        self.base_url = "https://api.heygen.com"
    
    def generate_video(self, input_text: str, avatar_id: str = "05ff47bf08f74d8d9161aae0c003f53b", 
                      voice_id: str = "0d4d97379a6746baa5dfc692b37774d4", 
                      bg_color: str = "#000000",
                      width: int = 720, height: int = 1280) -> str:
        """
        Generate a video using the HeyGen API.
        
        Args:
            input_text: The text for the avatar to speak
            avatar_id: ID of the avatar to use
            voice_id: ID of the voice to use
            bg_color: Background color in hex
            width: Video width in pixels
            height: Video height in pixels
            
        Returns:
            video_id: The ID of the generated video
        """
        url = f"{self.base_url}/v2/video/generate"
        
        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": avatar_id,
                        "avatar_style": "normal"
                    },
                    "voice": {
                        "type": "text",
                        "input_text": input_text,
                        "voice_id": voice_id
                    },
                    "background": {
                        "type": "color",
                        "value": bg_color
                    }
                }
            ],
            "dimension": {
                "width": width,
                "height": height
            }
        }
        
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Error generating video: {response.text}")
        
        response_data = response.json()
        
        if response_data.get("error"):
            raise Exception(f"API error: {response_data['error']}")
            
        return response_data["data"]["video_id"]
    
    def check_video_status(self, video_id: str) -> Dict[str, Any]:
        """
        Check the status of a video.
        
        Args:
            video_id: ID of the video to check
            
        Returns:
            Video status information
        """
        url = f"{self.base_url}/v1/video_status.get"
        
        headers = {
            "X-Api-Key": self.api_key
        }
        
        params = {
            "video_id": video_id
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Error checking video status: {response.text}")
        
        return response.json()
    
    def wait_for_video_completion(self, video_id: str, poll_interval: int = 5, 
                                 timeout: int = 300) -> Dict[str, Any]:
        """
        Poll the video status until it's completed or an error occurs.
        
        Args:
            video_id: ID of the video to check
            poll_interval: Seconds to wait between status checks
            timeout: Max seconds to wait for completion
            
        Returns:
            Final video status data
        """
        start_time = time.time()
        while True:
            status_data = self.check_video_status(video_id)
            
            if status_data["code"] != 100:
                raise Exception(f"API error: {status_data.get('message', 'Unknown error')}")
                
            video_status = status_data["data"]["status"]
            
            if video_status == "completed":
                return status_data["data"]
                
            if video_status == "failed" or status_data["data"].get("error"):
                error_msg = status_data["data"].get("error", "Unknown error")
                raise Exception(f"Video generation failed: {error_msg}")
                
                
            print(f"Video status: {video_status}. Checking again in {poll_interval} seconds...")
            time.sleep(poll_interval)
    
    def download_video(self, video_url: str, output_path: str) -> str:
        """
        Download a video from a URL and save it to disk.
        
        Args:
            video_url: URL of the video to download
            output_path: Path where the video will be saved
            
        Returns:
            Path to the saved video file
        """
        response = requests.get(video_url, stream=True)
        
        if response.status_code != 200:
            raise Exception(f"Error downloading video: {response.status_code}")
            
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"Video downloaded successfully to {output_path}")
        return output_path
    
    def generate_and_download_video(self, input_text: str, output_path: str, 
                                   avatar_id: str = "Daisy-inskirt-20220818",
                                   voice_id: str = "2d5b0e6cf36f460aa7fc47e3eee4ba54",
                                    width: int = 720, height: int = 1280) -> str:
        """
        Complete workflow: generate video, wait for completion, and download it.
        
        Args:
            input_text: The text for the avatar to speak
            output_path: Path where to save the video
            avatar_id: ID of the avatar to use
            voice_id: ID of the voice to use
            
        Returns:
            Path to the downloaded video file
        """
        print(f"Generating video with text: '{input_text}'")
        video_id = self.generate_video(input_text=input_text, avatar_id=avatar_id, voice_id=voice_id, width=width, height=height)
        
        print(f"Video generation started with ID: {video_id}")
        print("Waiting for video to complete...")
        
        video_data = self.wait_for_video_completion(video_id)
        
        video_url = video_data.get("video_url")
        if not video_url:
            raise Exception("Video URL not found in the response")
            
        print(f"Video is ready. Downloading from {video_url}")
        return self.download_video(video_url, output_path)

