from langchain_core.documents import Document
from langchain_community.document_loaders.url_selenium import SeleniumURLLoader
from typing import List, Tuple
import logging
import time
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class SeleniumURLLoaderWithWait(SeleniumURLLoader):
    def load(self, wait_time: int = 3, recursive: bool = False, paths: List =[]) -> List[Document]:

        from unstructured.partition.html import partition_html

        docs: List[Document] = list()
        driver = self._get_driver()
        child_links = set()
        visited_urls = set()


        def scrape_recursive(url):
            try:
                driver.get(url)
                visited_urls.add(url)
                time.sleep(wait_time)
                
                page_content = driver.page_source

                elements = partition_html(text=page_content)
                text = "\n\n".join([str(el) for el in elements])
                metadata = self._build_metadata(url, driver)
                docs.append(Document(page_content=text, metadata=metadata))
                print(url)

                # Get links
                base_url = urlparse(url)
                soup = BeautifulSoup(page_content, 'html.parser')
                links = [link.get('href') for link in soup.find_all('a')]
                if '/curso/' in base_url.path: 
                    course_id = base_url.path.split('/')[-1]
                    plan = f"/pt/c/{course_id}/p"
                    links.append(f"{base_url.scheme}://{base_url.netloc}{plan}")

                for link in links:
                    if link:
                        absolute_link = urljoin(base_url.geturl(), link)
                        #print(absolute_link)#.split('/'))
                        if urlparse(absolute_link).netloc == base_url.netloc and any(p in absolute_link.split('/') for p in paths):
                            child_links.add(absolute_link)
                            if recursive and absolute_link not in visited_urls:
                                #visited_urls.add(absolute_link)
                                scrape_recursive(absolute_link)
                #Get buttons

            except Exception as e:
                if self.continue_on_failure:
                    logger.error(f"Error fetching or processing {url}, exception: {e}")
                else:
                    raise e


        for url in self.urls:
            scrape_recursive(url)
   
        driver.close()
        return docs
