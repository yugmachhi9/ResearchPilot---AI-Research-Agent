from langchain.tools import tool
import requests
from bs4 import BeautifulSoup #it is libraray for web scraping (web scraping means extracting data from websites)
from tavily import TavilyClient
import os
from rich import print
from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a given topic.returns Titles,URLs and snippets of the top 5 search results."""
    results = tavily.search(query= query, max_results=5)

    output = []

    for r in results['results']:
        title = r['title']
        url = r['url']
        snippet = r['content']
        output.append(f"Title: {title}\nURL: {url}\nSnippet: {snippet}\n")
    return "\n------\n".join(output)
    

# print(web_search("What is latest news in AI?"))

@tool
def web_scrape(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading and analysis."""
    try:
        response = requests.get(url,timeout=10,headers={'User-Agent': 'Mozilla/5.0'}) #to avoid being blocked by some websites that restrict automated requests so we set a user-agent header to mimic a regular browser request.
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style','nav','footer','header','aside']):
            tag.decompose() #to remove unwanted tags that do not contribute to the main content of the page, such as scripts, styles, navigation bars, footers, headers, and sidebars.
        return soup.get_text(separator='\n', strip=True)[:3000]
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "Failed to retrieve the web page content."

# print(web_scrape.invoke("https://techcrunch.com/2026/05/31/making-sense-of-the-debate-over-ai-psychosis/"))