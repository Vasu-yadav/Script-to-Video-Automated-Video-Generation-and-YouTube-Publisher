# Script-to-Video: Automated Video Generation & YouTube Publisher

A comprehensive tool for generating engaging short-form video content from topics, powered by AI, and automatically uploading to YouTube.

## 🌟 Overview

Script-to-Video automates the entire pipeline from topic research to YouTube publication:

1. **Topic Research & Script Generation** - Generate news-like scripts from topics using Google's Gemini API
2. **Video Generation** - Convert scripts into realistic avatar videos using HeyGen's API
3. **Metadata Generation** - Create SEO-optimized titles, descriptions, and tags
4. **YouTube Upload** - Automatically publish generated videos to YouTube

## ✨ Features

- **Topic-driven Content** - Generate engaging scripts from any topic
- **AI Avatar Generation** - Create realistic videos with virtual presenters
- **Multiple Avatars** - Choose from various predefined avatars
- **SEO Optimization** - Generate YouTube-optimized metadata
- **Batch Processing** - Process multiple videos in sequence
- **Metadata Storage** - Track all generated content

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Google API credentials (for Gemini and YouTube)
- HeyGen API credentials

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Vasu-yadav/Script-to-Video-Automated-Video-Generation-and-YouTube-Publisher.git
cd Script-to-Video-Automated-Video-Generation-and-YouTube-Publisher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following variables:
```
GOOGLE_API_KEY=your_google_api_key
HEYGEN_API_KEY=your_heygen_api_key
```

4. For YouTube uploads, place your `client_secret.json` file in the project root.

## 🚀 Usage

### Basic Usage

Run the main script to generate and upload a video:

```bash
python main.py
```

This will:
1. Select a random topic from `topics.json`
2. Generate a script
3. Create a video with a random avatar
4. Generate metadata
5. Upload to YouTube as unlisted

### Development Mode

For testing without YouTube upload:

```bash
python main_dev.py
```

### Custom Topics

Update the `data/topics.json` file with your own topics:

```json
[
  "AI advancements in healthcare",
  "Climate change solutions",
  "Future of remote work"
]
```

### Custom Avatars

Update the `data/avatars.json` file to configure avatars:

```json
[
  {
    "name": "Presenter Name",
    "avater_id": "avatar_id_from_heygen",
    "voide_id": "voice_id_from_heygen"
  }
]
```

## 📂 Project Structure

```
Script_to_Video/
├── main.py                 # Main production script
├── main_dev.py             # Development version
├── data/
│   ├── HeyGenAvaters.json        # Avatar configurations
│   └── video_topics.json         # Content topics
├── output/                 # Generated videos directory
└── utils/
    ├── HeyGenClient.py     # HeyGen API interface
    ├── script_generator/   # Script generation modules
    ├── uploadToYoutube/    # YouTube upload functionality
    └── video_metadata.py   # Title/description generation
```

## 🔧 Configuration

### Avatar Configuration
Each avatar in `HeyGenAvatars.json` requires:
- `name`: Friendly name for the avatar
- `avater_id`: HeyGen avatar ID
- `voide_id`: HeyGen voice ID

## 👥 Contributors
[Vasu Yadav](https://github.com/Vasu-yadav)  
[Krishan Mehra](https://github.com/krishankantmehra)  

## 🙏 Acknowledgments

- [HeyGen](https://www.heygen.com/) for video avatar generation
- [Google Gemini](https://ai.google.dev) for AI text generation
