import os
import json
import logging
import sys
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from llama_index.core import VectorStoreIndex, Document
from llama_index.tools.brave_search import BraveSearchToolSpec
from llama_index.readers.web import SimpleWebPageReader

# Constants
USER_AGENT = 'Mozilla/5.0 (compatible; YourBot/1.0; +http://yourwebsite.com/bot.html)'
HEADERS = {'User-Agent': USER_AGENT}
RETRIES = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])

def setup_logging():
    """
    Initialize logging configuration to output logs to stdout.
    """
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

def load_environment_variables():
    """
    Load environment variables from the .env file.
    :return: The Brave API key.
    """
    load_dotenv()
    return os.getenv('BRAVE_API_KEY')

def perform_search(query, api_key):
    """
    Perform a search using the Brave Search API.
    :param query: The search query.
    :param api_key: The Brave API key.
    :return: The search response.
    """
    tool_spec = BraveSearchToolSpec(api_key=api_key)
    return tool_spec.brave_search(query=query)

def extract_search_results(response):
    """
    Extract search results from the Brave Search API response.
    :param response: The search response.
    :return: A list of search results.
    """
    documents = [doc.text for doc in response]
    search_results = []
    for document in documents:
        response_data = json.loads(document)
        search_results.extend(response_data.get('web', {}).get('results', []))
    return search_results

def scrape_web_pages(search_results):
    """
    Scrape web pages from the URLs obtained from the search results.
    :param search_results: The list of search results.
    :return: A list of scraped documents.
    """
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=RETRIES))
    session.mount('https://', HTTPAdapter(max_retries=RETRIES))
    all_documents = []

    for result in search_results:
        url = result.get('url')
        try:
            response = session.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            doc = Document(text=response.text, url=url)
            all_documents.append(doc)
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to scrape {url}: {e}")

    return all_documents

def main():
    """
    Main function to orchestrate the search, scraping, and querying process.
    """
    setup_logging()
    api_key = load_environment_variables()
    my_query = "What is the latest news about llamaindex?"
    response = perform_search(my_query, api_key)
    search_results = extract_search_results(response)
    all_documents = scrape_web_pages(search_results)
    
    # Load all the scraped documents into the vector store
    index = VectorStoreIndex.from_documents(all_documents)
    
    # Use the index to query with the language model
    query_engine = index.as_query_engine()
    response = query_engine.query(my_query)
    print(response)

if __name__ == "__main__":
    main()