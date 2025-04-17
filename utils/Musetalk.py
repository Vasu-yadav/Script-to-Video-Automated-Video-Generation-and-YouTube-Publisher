import requests
import json
import os
import time


class MuseTalk:
    def __init__(self, base_url, proxies=None, headers=None):
        """
        Initialize the MuseTalk client.

        Args:
            base_url (str): The base URL of the API.
            proxies (dict): Proxy settings for requests.
            headers (dict): Headers for API requests.
        """
        self.base_url = base_url
        self.proxies = proxies or {'http': None, 'https': None}
        self.headers = headers or {"Content-Type": "application/json"}

    def list_speakers(self):
        """
        List available speakers from the API.

        Returns:
            list: A list of speakers if successful, None otherwise.
        """
        try:
            response = requests.get(f"{self.base_url}/speakers", headers=self.headers, proxies=self.proxies)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            return None
        
    def create_video(self, text, video_path, gender):
        """
        Create a video using the API and download it upon success.

        Args:
            text (str): The text for the video.
            video_path (str): Path to save the downloaded video.
            gender (str): Gender for the video generation.

        Returns:
            bool: True if the video was successfully downloaded, False otherwise.
        """
        create_endpoint = f"{self.base_url}/generate_video"
        status_endpoint = f"{self.base_url}/job-status"
        gender = gender.capitalize()  # Ensure
        payload = {
            "text": text,
            "gender": gender,
            "video_path": 'f1bbee75-460c-45e5-b42d-f1394da66fb9.mp4'
        }
        
        try:
            # Step 1: Call the create-video API
            print(self.headers)
            response = requests.post(create_endpoint, data=json.dumps(payload), headers=self.headers,proxies=self.proxies)
            response.raise_for_status()
            job_id = response.json().get("job_id")
            print(job_id)

            if not job_id:
                print("Failed to retrieve job_id from the response.")
                return False

            # Step 2: Poll the status endpoint
            while True:
                status_response = requests.get(f"{status_endpoint}/{job_id}", headers=self.headers, proxies=self.proxies)
                status_response.raise_for_status()
                status_data = status_response.json()
                print(status_data)

                if status_data.get("status") == "success":
                    # Step 3: Download the video
                    return self.download_video(job_id, video_path)
                elif status_data.get("status") == "failed":
                    print("Video creation failed.")
                    return False

                print("Video is still processing. Retrying in 5 seconds...")
                time.sleep(5)

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            return False

    def download_video(self, job_id, save_path):
        """
        Download a video file from the API response.

        Args:
            job_id (str): The job ID for the video.
            save_path (str): Path to save the downloaded video.

        Returns:
            bool: True if the video was successfully downloaded, False otherwise.
        """
        try:
            # Ensure the directory for save_path exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            url = f'{self.base_url}/download-video/{job_id}'
            response = requests.get(url, proxies=self.proxies, stream=True)
            response.raise_for_status()  # Raise an error for bad status codes

            # Save the file from the response
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # Filter out keep-alive chunks
                        f.write(chunk)

            print(f"Video successfully downloaded to {save_path}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Failed to download video: {str(e)}")
            return False