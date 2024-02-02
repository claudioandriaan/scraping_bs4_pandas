import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

# Function to scrape website and extract data
def scrape_website(url, max_pages):
    
    # Lists to store data
    link = []
    job_title = []
    company_name = []
    contrat = []
    desc = []
    
    # Iterate over pages
    for page in range(1, max_pages+1):
        url_next = f"{url}liste/page/{page}"
        response = requests.get(url_next)
        
        txt = BeautifulSoup(response.content, "html.parser")
        containers = txt.find_all('aside', class_='contenu_annonce')
        
        for container in containers: 
            link.append(container.find('a')['href'])
            job_title.append(container.find('strong').text.strip())
            company_name.append(container.find('h4').text.strip())
            contrat.append(container.find('h5').text.strip())
            desc.append(container.find(class_='description').text.strip())

    # Create a DataFrame to store the data
    data = pd.DataFrame({
        'Link': link,
        'Job Title': job_title,
        'Company': company_name,
        'Contract': contrat,
        'Description': desc,
        
    })
    
    return data


# Main function
def main():
    
    url = "https://www.portaljob-madagascar.com/emploi/"
    max_pages = 10
    
    data = scrape_website(url, max_pages)
    today = date.today().strftime("%Y-%m-%d")
    
    file_name = f'data_{today}.xlsx'

    data.to_excel(file_name, index=False)

    print("Data has been scraped and saved to", file_name)

if __name__ == "__main__":
    main()
