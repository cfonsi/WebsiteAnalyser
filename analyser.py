import requests
import time

def get_loading_time(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    loading_time = end_time - start_time
    return loading_time

def main():
    url = "https://example.com"
    loading_time = get_loading_time(url)
    print(f"The loading time for {url} is {loading_time} seconds.")

if __name__ == "__main__":
    main()
