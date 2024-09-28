import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_stackoverflow_page(url, writer):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        questions = soup.find_all('div', class_='s-post-summary')  
        for question in questions:
            # Judul dan Link
            title_element = question.find('a', class_='s-link')
            if title_element:
                title = title_element.get_text(strip=True)
                link = 'https://stackoverflow.com' + title_element['href']
            else:
                title = 'N/A'
                link = 'N/A'
            
            # Tags
            tag_elements = question.find_all('a', class_='post-tag')
            tags = [tag.get_text(strip=True) for tag in tag_elements]
            
            # Votes
            votes_element = question.find('span', class_='s-post-summary--stats-item-number')
            votes = votes_element.get_text(strip=True) if votes_element else '0'
            
            # Views
            views_element = question.find('span', class_='s-post-summary--stats-item-unit')
            if views_element and 'view' in views_element.get_text().lower():
                views = views_element.find_previous_sibling('span').get_text(strip=True)
            else:
                views = '0'
            
            writer.writerow([title, link, ', '.join(tags), votes, views])
            
            print(f'Title: {title}')
            print(f'Link: {link}')
            print(f'Tags: {", ".join(tags)}')
            print(f'Votes: {votes}')
            print(f'Views: {views}')
            print('-' * 80)
    else:
        print(f"Gagal mengambil halaman {url}. Status code: {response.status_code}")

base_url = 'https://stackoverflow.com/questions'

with open('nala_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Link', 'Tags', 'Votes', 'Views'])
    
    # Contoh: Mengambil 20 halaman
    for page in range(1, 21):
        url = f'{base_url}?tab=Newest&page={page}'
        print(f"Scraping halaman: {url}")
        scrape_stackoverflow_page(url, writer)
        time.sleep(2)  

print('Data berhasil ditulis ke nala_data.csv')


