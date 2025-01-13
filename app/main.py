import modules

import requests
from bs4 import BeautifulSoup
import csv

import requests
from bs4 import BeautifulSoup
import csv

def crawl_blogspot(base_url, num_pages=5, output_file="blogspot_posts.csv"):
    posts = []
    current_url = base_url
    for _ in range(num_pages):
        try:
            # Fetch the page
            response = requests.get(current_url)
            if response.status_code != 200:
                print(f"Failed to fetch {current_url}. HTTP status: {response.status_code}")
                break
            
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract post elements
            post_elements = soup.find_all("div", class_="post") 
            for post in post_elements:
                try:
                    title_tag = post.find("h3", class_="post-title") 
                    title = title_tag.get_text(strip=True) if title_tag else "No title"
                    url = title_tag.a["href"] if title_tag and title_tag.a else "No URL"
                    content = post.find("div", class_="post-body")
                    content = content.get_text(strip=True)

                    date_tag = post.find("time", class_="date-header") 
                    publication_date = date_tag.get_text(strip=True) if date_tag else "Unknown date"

                    posts.append({"Title": title, "URL": url, "Post": content,"Publication Date": publication_date})
                except Exception as e:
                    print(f"Error extracting post: {e}")
            
            # Find the next page link
            next_page_tag = soup.find("a", class_="blog-pager-older-link") 
            if next_page_tag and "href" in next_page_tag.attrs:
                current_url = next_page_tag["href"]
            else:
                print("No more pages to crawl.")
                break

        except Exception as e:
            print(f"Error crawling {current_url}: {e}")
            break

    # Save results to a CSV file
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "URL", "Post", "Publication Date"])
        writer.writeheader()
        writer.writerows(posts)
    
    print(f"Crawling completed. {len(posts)} posts saved to {output_file}.")

# Usage
blogspot_url = "https://carlsonpessoa.blogspot.com"  # Replace with your Blogspot URL
crawl_blogspot(blogspot_url, num_pages=5)
