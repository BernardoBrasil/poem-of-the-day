import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

URL = 'https://www.poetryfoundation.org/poems/poem-of-the-day'


def app():
    try:
        response = requests.get(URL)
    except requests.ConnectionError:
        print("Connection error. \nTry again?(y/n)")
        retry = input('> ')

        if retry == 'y':
            app()
        elif retry == 'n':
            return
        else:
            print('Invalid choice, chosse y for yes or n for no.')
            retry = input('> ')

        print('Program finished.')
    else:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find('div', {'class': 'c-feature-hd'}).h1.text.strip()
        author_name = soup.find(
            'span', {'class': 'c-txt_attribution'}).a.text.strip()
        author_link = soup.find(
            'span', {'class': 'c-txt_attribution'}).a['href']
        poem = [line.text for line in soup.find('div', {'class': 'o-poem'}).find_all('div')]
        link = soup.find('a', {'class': 'c-txt_minimalCta'})['href']
        print(f'Poem {title} found.')

        write_md(title, author_name, author_link, poem, link)
        print('File saved to your desktop.')


def write_md(title, author_name, author_link, poem, link):
    now = datetime.now()
    today = now.strftime("%d-%m-%Y")
    home = os.environ['HOMEPATH']
    path = f'{home}/Desktop/Poem of the day'
    name = f'{title} - {today}'

    if not os.path.exists(path):
        os.makedirs(path)

    with open(f'{path}/{name}.md', 'w', encoding='utf-8') as f:
        f.write(f'# {title}\n')
        f.write(f'By [{author_name}]({author_link})\n')
        f.write('\n')
        for line in poem:
            f.write(f'{line}\n')
        f.write('\n***\n')
        f.write(f'\n[🪶 Read on Poetry Foundation]({link})\n')
        f.write(f"\n_⌛ Fetched on {now.strftime('%b %d %Y')}_")


if __name__ == "__main__":
    app()
