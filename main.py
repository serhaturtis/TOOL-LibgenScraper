import os
import libgen_scraper as lg
import requests
from tqdm import tqdm

LIBGEN_MIRROR= "http://libgen.rs"

def ensure_directory_exists(directory_name):
    current_directory = os.getcwd()
    directory_path = os.path.join(current_directory, directory_name)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    return directory_path

def search_nonfiction(topic, count_limit):
    non_fiction = lg.search_non_fiction(
    topic,
    search_in_fields=lg.NonFictionSearchField.TITLE,
    #filter={
    #    lg.NonFictionColumns.LANGUAGE: r'English',
    #},
    limit=count_limit,
    libgen_mirror=LIBGEN_MIRROR,
    )
    return non_fiction

def search_articles(topic, count_limit):
    articles = lg.search_articles(
    topic,
    filter={
        lg.ArticlesColumns.LANGUAGE: r'English',
    },
    limit=count_limit,
    libgen_mirror=LIBGEN_MIRROR,
)
    return articles

def download_nonfiction(topic, search_results:lg.NonFictionResults):
    save_directory = ensure_directory_exists(f'./downloads/{topic}/nonfiction')

    for i in range(len(search_results)):
        download_links = search_results.download_links(i, limit_mirrors=2)
        print("Downloading:" , search_results.id(i), " From: ", download_links[0])
        download_file(download_links[0], save_directory, search_results.title(i))

def download_article(topic, search_results:lg.ArticlesResults):
    save_directory = ensure_directory_exists(f'./downloads/{topic}/article')

    for i in range(len(search_results)):
        download_links = search_results.download_links(i, limit_mirrors=2)
        print("Downloading:" , search_results.article(i), " From: ", download_links[0])
        download_file(download_links[0], save_directory, search_results.article(i))


def download_file(url, directory, filename=None):
    if not filename:
        filename = url.split("/")[-1]

    file_path = os.path.join(directory, filename)

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(file_path, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

    print(f"Downloaded file saved to {file_path}")

def main():
    search_topic = input("Topic:")
    book_limit = int(input("Book Count:"))
    article_limit = int(input("Article Count:"))
    nonfiction_results = search_nonfiction(search_topic, book_limit)
    articles_results = search_articles(search_topic, article_limit)
    
    download_nonfiction(search_topic, nonfiction_results)
    download_article(search_topic, articles_results)

    
if __name__ == '__main__':
    main()