import bs4 as beautifulsoup
import requests
import trafilatura
from google import genai
import dotenv
import os
from . import system_prompts


class ScriptGenerator:
    def __init__(self, api_key=None):
        """
        Initialize the ScriptGenerator class with Google API key
        If no API key is provided, it will attempt to load from environment variables
        """
        dotenv.load_dotenv()
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("Google API key is required. Provide it as a parameter or set GOOGLE_API_KEY environment variable.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.debug = False  # Control debug printing
    
    def set_debug(self, debug=True):
        """Enable or disable debug printing"""
        self.debug = debug
    
    def _debug_print(self, message):
        """Print debug messages if debug mode is enabled"""
        if self.debug:
            print(message)
    
    def search_or_not(self, user_query):
        """Determine if the query requires web search"""
        PROMPT = f"""
            {system_prompts.SEARCH_OR_NOT_MSG}
            USER QUERY: {user_query}
        """

        response = self.client.models.generate_content(
            model="gemini-2.0-flash", contents=PROMPT,
        )

        content = response.text
        self._debug_print(f'SEARCH OR NOT: {content}')

        return 'yes' in content.lower()
    
    def query_generator(self, user_query):
        """Generate an optimized search query from user input"""
        PROMPT = f"""
        {system_prompts.QUERY_GENERATOR_MSG}
        USER QUERY: {user_query}
        """
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", contents=PROMPT,
        )

        content = response.text
        content = content.replace('"', '')
        self._debug_print(f'QUERY GENERATOR: {content}')

        return content

    def duckduckgo_search(self, query):
        """Perform a DuckDuckGo search and extract results"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.'
        }
        url = f'https://duckduckgo.com/html/?q={query}'
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = beautifulsoup.BeautifulSoup(response.text, 'html.parser')
        results = []
        for i, result in enumerate(soup.find_all('div', class_ = 'result'), start=1):
            if i > 5:
                break
            title = result.find('a', class_='result__a')
            if not title:
                continue

            link = title['href']
            snippet_tag = result.find('a', class_='result__snippet')
            snippet = snippet_tag.text.strip() if snippet_tag else 'No description available'

            results.append({
                'id': i,
                'link': link,
                'search_description': snippet
            })
        return results
    
    # def searxng_search(self,query):

    #     headers = {
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    #     }
    #     # Query the local searxng instance. Adjust parameters as needed.
    #     url = 'http://localhost:4000/search'
    #     params = {
    #     'q': query,
    #     'format': 'html'  # Explicitly request HTML format
    #     }
    #     proxies = {
    #         'http': None,
    #         'https': None
    #     }

    #     response = requests.get(url, headers=headers, params=params, proxies=proxies)
    #     response.raise_for_status()
        
    #     soup = beautifulsoup.BeautifulSoup(response.text, 'html.parser')
    #     results = []
        
    #     # Use a CSS selector to get all articles with class "result"
    #     articles = soup.select('article.result')
    #     for i, article in enumerate(articles, start=1):
    #         if i > 5:
    #             break
    #         # Get the URL from the <a> with class "url_header"
    #         link_tag = article.find('a', class_='url_header')
    #         if not link_tag:
    #             continue
    #         link = link_tag.get('href', 'No URL found')
            
    #         # Get the snippet from the <p> with class "content"
    #         snippet_tag = article.find('p', class_='content')
    #         snippet = snippet_tag.get_text(strip=True) if snippet_tag else 'No description available'
            
    #         results.append({
    #             'id': i,
    #             'link': link,
    #             'search_description': snippet
    #         })
        
    #     return results

    def best_search_results(self, s_results, query, user_prompt):
        """Determine the most relevant search result"""
        PROMPT = f"""
            {system_prompts.BEST_SEARCH_RESULT_MSG}
            SEARCH_RESULTS: {s_results} 
            USER_PROMPT: {user_prompt} 
            SEARCH_QUERY: {query}
        """
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", contents=PROMPT,
        )

        content = response.text
        self._debug_print(f'BEST SEARCH RESULT: {content}')

        return content

    def scrape_webpage(self, url):
        """Extract content from a webpage"""
        try:
            downloaded = trafilatura.fetch_url(url)
            return trafilatura.extract(downloaded, include_links=True, deduplicate=True)
        except Exception as e:
            self._debug_print(f"Error scraping webpage: {str(e)}")
            return None
        
    def contains_data_needed(self, search_content, query, user_prompt):
        """Check if the scraped content contains the information needed"""
        PROMPT = f"""
            {system_prompts.CONTAINS_DATA_NEEDED_MSG}
            PAGE_TEXT: {search_content}
            USER PROMPT: {user_prompt}
            SEARCH QUERY: {query}
        """
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", contents=PROMPT,
        )

        content = response.text
        self._debug_print(f'CONTAINS DATA NEEDED: {content}')

        return 'true' in content.lower()
        
    def ai_search(self, user_query):
        """Perform an AI-guided web search"""
        self._debug_print("GENERATING SEARCH QUERY...")
        search_query = self.query_generator(user_query)

        if search_query and search_query[0] == '"' and search_query[-1] == '"':
            search_query = search_query[1:-1]

        search_results = self.duckduckgo_search(search_query)
        self._debug_print(f"SEARCH RESULTS: {search_results}")
        context_found = False

        while not context_found and len(search_results) > 0:
            best_result = self.best_search_results(search_results, search_query, user_query)
            
            # Convert the result to an integer and handle invalid responses
            try:
                best_result = int(best_result)
            except ValueError:
                self._debug_print(f"Invalid result '{best_result}' returned. Removing the first result as fallback.")
                search_results.pop(0)  # Remove the first result as a fallback
                continue

            # Validate the index returned by best_search_results
            if not (0 <= best_result < len(search_results)):
                self._debug_print(f"Invalid index {best_result} returned. Removing the first result as fallback.")
                search_results.pop(0)  # Remove the first result as a fallback
                continue
            
            try:
                page_link = search_results[best_result]['link']
            except IndexError:
                self._debug_print('FAILED TO SELECT BEST SEARCH RESULT, TRYING AGAIN...')
                search_results.pop(best_result)  # Remove the invalid result
                continue
            
            page_content = self.scrape_webpage(page_link)
            
            if page_content and self.contains_data_needed(page_content, search_query, user_query):
                context_found = True
                return page_content
            else:   
                search_results.pop(best_result)  # Remove the result if it doesn't contain needed data
                continue

        return None

    def generate_response(self, user_query, context=None):
        """Generate a response to the user query, optionally with context"""
        if context:
            PROMPT = f"""
                {system_prompts.CONTENT_GENERATOR_WITH_CONTEXT_MSG}

                CONTEXT: {context}
                USER TOPIC: {user_query}
            """
            response = self.client.models.generate_content(
                model="gemini-2.0-flash", contents=PROMPT,
            )
        else:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash", contents=user_query,
            )

        self._debug_print(f"Response: {response.text}")
        return response
    
    def process_query(self, user_query):
        """
        Process a user query and return the generated response
        This is the main API method that handles the entire workflow
        """
        if self.search_or_not(user_query):
            context = self.ai_search(user_query)
            if context:
                return self.generate_response(user_query, context)
            else:
                self._debug_print("No relevant context found.")
                return None
        else:
            self._debug_print("No search needed for this query.")
            return self.generate_response(f"""
                {system_prompts.CONTENT_GENERATOR_WITHOUT_CONTEXT_MSG}
                                          {user_query}""")


def main():
    """Command line interface for ScriptGenerator"""
    generator = ScriptGenerator()
    generator.set_debug(True)
    
    while True: 
        user_query = input("Enter your query: ")
        if user_query.lower() == 'exit':
            break
        
        response = generator.process_query(user_query)
        if response:
            print(f"Response: {response.text}")
        else:
            print("Could not generate a response for your query.")


if __name__ == "__main__":
    main()