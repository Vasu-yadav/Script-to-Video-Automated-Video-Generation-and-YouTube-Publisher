from google import genai
import dotenv
import os

class VideoMetadata:
    """
    Class to generate video metadata including title and description.
    """
    def __init__(self, api_key=None):
        dotenv.load_dotenv()
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("Google API key is required. Provide it as a parameter or set GOOGLE_API_KEY environment variable.")
        self.client = genai.Client(api_key=self.api_key)


    def generate_video_title(self, description):

        PROMPT = f"""
        You are a YouTube video title generator.
        Generate a catchy title for the following video description:
        {description}
        The title should be less than 60 characters.
        Rules:
            - Respond ONLY with the title string
            - Do not include explanations or additional text
            - Remove unnecessary words (articles, pronouns, etc.)

        Examples:
        Input: "Is Messi or Ronaldo the GOAT? The debate rages on, but Guinness World Records has tallied the score! It's a neck-and-neck race with both football icons holding numerous records. From domestic leagues to the Champions League and international play, they dominate. But in the end, Messi edges out Ronaldo 41 Guinness World Records to 40! But with Ronaldo continuing to play, the game isn't over"
        Output: "Messi vs Ronaldo: The GOAT Debate Continues! Guinness World Records Showdown"

        Do not provide any commentary - output only the title.
        """
        response = self.client.models.generate_content(
                model="gemini-2.0-flash", contents=PROMPT,
            )
        if response:
            print(f"video_title: {response.text}")
            return response.text
        else:
            print("Could not generate a video_title for your query.")
            return "Could not generate a video_title for your query."

    def generate_video_description(self, description):
        PROMPT = f"""
        You are a YouTube video description generator.
        Generate a detailed description for the following video:
        {description}
        The description should be less than 150 characters.
        Rules:
            - Respond ONLY with the description string
            - Do not include explanations or additional text
            - Remove unnecessary words (articles, pronouns, etc.)

        Examples:
        Input: "Is Messi or Ronaldo the GOAT? The debate rages on, but Guinness World Records has tallied the score! It's a neck-and-neck race with both football icons holding numerous records. From domestic leagues to the Champions League and international play, they dominate. But in the end, Messi edges out Ronaldo 41 Guinness World Records to 40! But with Ronaldo continuing to play, the game isn't over"
        Output: "Messi vs Ronaldo: The GOAT debate continues! Guinness World Records reveal Messi leads with 41 records, Ronaldo close behind with 40. Who's next?"
        Do not provide any commentary - output only the description.
        """
        response = self.client.models.generate_content(
                model="gemini-2.0-flash", contents=PROMPT,
            )
        if response:
            print(f"video_description: {response.text}")
            return response.text
        else:
            print("Could not generate a video_description for your query.")
            return "Could not generate a video_description for your query."
    
    def generate_video_tags(self, description):
        PROMPT = f"""
        You are a YouTube video tag generator.
        Generate relevant tags for the following video description:
        {description}
        The tags should be keywords related to given description.
        Rules:
            - Respond ONLY with the comma separated tags string
            - Do not include explanations or additional text
            - Remove unnecessary words (articles, pronouns, etc.)

        Examples:
        Input: "Is Messi or Ronaldo the GOAT? The debate rages on, but Guinness World Records has tallied the score! It's a neck-and-neck race with both football icons holding numerous records. From domestic leagues to the Champions League and international play, they dominate. But in the end, Messi edges out Ronaldo 41 Guinness World Records to 40! But with Ronaldo continuing to play, the game isn't over"
        Output: "Messi, Ronaldo, GOAT, Guinness World Records, football, debate, Champions League, international play"
        Do not provide any commentary - output only the tags.
        """
        response = self.client.models.generate_content(
                model="gemini-2.0-flash", contents=PROMPT,
            )
        if response:
            print(f"video_tags: {response.text}")
            tags = response.text.split(", ")
            return tags
        else:
            print("Could not generate a video_tags for your query.")
            return "Could not generate a video_tags for your query."


def main():
    video_metadata = VideoMetadata()
    description = "Generative AI tools like ChatGPT have revolutionized natural language processing, enabling applications across content creation, customer service, and predictive analytics. AI democratization is accelerating, with 50% of organizations adopting AI for at least one business function. Open-source frameworks and cost-effective solutions are empowering smaller enterprises to leverage AI for tasks like fraud detection and personalized healthcare."
    title = video_metadata.generate_video_title(description)
    description = video_metadata.generate_video_description(description)
    tags = video_metadata.generate_video_tags(description)
    print(f"Title: {title}")
    print(f"Description: {description}")
    print(f"Tags: {tags}")
if __name__ == "__main__":
    main()