import os
import pickle
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Step 1: Define scopes and file paths
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRET_FILE = "client_secret.json"
CREDENTIALS_PICKLE_FILE = "token.pickle"

def get_authenticated_service():
    credentials = None

    # Step 2: Load credentials if they exist
    if os.path.exists(CREDENTIALS_PICKLE_FILE):
        with open(CREDENTIALS_PICKLE_FILE, "rb") as token:
            credentials = pickle.load(token)

    # Step 3: If no valid credentials, perform login flow
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

        with open(CREDENTIALS_PICKLE_FILE, "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)

def upload_video(file_path, title, description, tags=None, category_id="22", privacy="public"):
    youtube = get_authenticated_service()

    # Step 4: Define request body
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy
        }
    }

    # Step 5: Upload the video
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype='video/*')

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    print("Uploading...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print("Upload complete!")
    print("Video ID:", response["id"])

# Example usage
if __name__ == "__main__":
    upload_video(
        file_path="/ext_disk/videoGAN/Script_to_video/output.mp4",
        title="US China tarrif war",
        description="China attacks US Luxury brands by exposing their true manufacturing costs",
        tags=["Tarrif", "upload", "api"],
        privacy="unlisted"
    )