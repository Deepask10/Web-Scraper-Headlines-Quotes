import requests
from bs4 import BeautifulSoup
import json


# Website URL
URL = "https://quotes.toscrape.com/"


def scrape_quotes():
    try:
        # Send HTTP request
        response = requests.get(URL, timeout=10)

        # Check for HTTP errors
        response.raise_for_status()

        print("Website connected successfully!")
        print("Status Code:", response.status_code)

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all quote containers
        quote_blocks = soup.find_all("div", class_="quote")

        quotes_data = []

        # Extract quote information
        for quote_block in quote_blocks:

            quote_text = quote_block.find(
                "span", class_="text"
            ).get_text(strip=True)

            author = quote_block.find(
                "small", class_="author"
            ).get_text(strip=True)

            tag_elements = quote_block.find_all(
                "a", class_="tag"
            )

            tags = [
                tag.get_text(strip=True)
                for tag in tag_elements
            ]

            quote_data = {
                "quote": quote_text,
                "author": author,
                "tags": tags
            }

            quotes_data.append(quote_data)

        return quotes_data

    except requests.exceptions.RequestException as error:
        print("Error while connecting to website:", error)
        return []


def save_to_json(quotes):
    with open("quotes.json", "w", encoding="utf-8") as file:
        json.dump(quotes, file, indent=4, ensure_ascii=False)

    print("Data saved to quotes.json")


def save_to_text(quotes):
    with open("quotes.txt", "w", encoding="utf-8") as file:

        for number, quote in enumerate(quotes, start=1):
            file.write(f"Quote {number}\n")
            file.write(f"Quote: {quote['quote']}\n")
            file.write(f"Author: {quote['author']}\n")
            file.write(f"Tags: {', '.join(quote['tags'])}\n")
            file.write("-" * 60 + "\n")

    print("Data saved to quotes.txt")


def display_quotes(quotes):
    print("\n" + "=" * 60)
    print("SCRAPED QUOTES")
    print("=" * 60)

    for number, quote in enumerate(quotes, start=1):
        print(f"\nQuote {number}")
        print(f"Quote: {quote['quote']}")
        print(f"Author: {quote['author']}")
        print(f"Tags: {', '.join(quote['tags'])}")
        print("-" * 60)


def main():
    print("Starting Web Scraper...")
    print("=" * 60)

    # Scrape website
    quotes = scrape_quotes()

    # Check whether data was collected
    if not quotes:
        print("No quotes were found.")
        return

    print(f"Successfully scraped {len(quotes)} quotes.")

    # Display scraped data
    display_quotes(quotes)

    # Save data
    save_to_json(quotes)
    save_to_text(quotes)

    print("\nScraping completed successfully!")


# Run the program
if __name__ == "__main__":
    main()