import requests
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_loading_time(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        load_time = end_time - start_time
        return url, load_time
    except requests.RequestException as e:
        return url, str(e)


def get_components(base_url):
    try:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        components = set()
        for tag in soup.find_all(['img', 'script', 'link']):
            if tag.name == 'img' and tag.get('src'):
                components.add(tag['src'])
            elif tag.name == 'script' and tag.get('src'):
                components.add(tag['src'])
            elif tag.name == 'link' and tag.get('href'):
                components.add(tag['href'])

        return [url if url.startswith('http') else base_url + url for url in components]

    except requests.RequestException as e:
        print(f"Error fetching base URL: {e}")
        return []

def analyse_website(base_url):
    components = get_components(base_url)
    print(f"Found {len(components)} components to analyse.")

    load_times = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(get_loading_time, url): url for url in components}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                load_times.append(data)
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")

    load_times.sort(key=lambda x: x[1] if x[1] is not None else float('inf'), reverse=True)

    return load_times

def main():
    base_url = "https://www.w3schools.com/"
    loading_times = analyse_website(base_url)

    print("\nComponent load times (in seconds):")
    for url, load_time in loading_times:
        print(f"{url}: {load_time:.2f} seconds")

if __name__ == "__main__":
    main()
