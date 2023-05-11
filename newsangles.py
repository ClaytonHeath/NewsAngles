# Import the libraries
import openai
import os
import json
import urllib.request
from dotenv import load_dotenv
from tqdm import tqdm  # Import the tqdm library
from urllib.parse import quote_plus
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Load the environment variables from the .env file
load_dotenv()

# Define the API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
gnewsapikey = os.getenv("GNEWS_API_KEY")

# Create a function that takes a topic as an argument and returns the top 5 news headlines
def get_news(topic):
    # URL encode the topic
    topic = quote_plus(topic)
    # Create the URL with the topic and your API key
    url = f"https://gnews.io/api/v4/search?q={topic}&lang=en&country=us&max=5&apikey={gnewsapikey}"
    # Fetch the data from the API
    return fetch_data(url)

# Create a function that takes a category as an argument and returns the top 5 news headlines
def get_top_headlines(category):
    # URL encode the category
    category = quote_plus(category)
    # Create the URL with the category and your API key
    url = f"https://gnews.io/api/v4/top-headlines?lang=en&country=us&category={category}&max=5&apikey={gnewsapikey}"
    # Fetch the data from the API
    return fetch_data(url)

# Create a function that fetches the data from the API
def fetch_data(url):
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
    # Get the articles from the data
    articles = data["articles"]
    # Initialize an empty list to store the headlines
    headlines = []
    # Loop through the first 5 articles
    for article in articles:
        # Get the title, url and published_at of the article
        headline = {
            "title": article["title"],
            "url": article["url"],
            "published_at": article["publishedAt"]
        }
        # Append it to the headlines list
        headlines.append(headline)
    # Return the headlines as a variable
    return headlines

# Ask the user for a choice
choice = input("Would you like to enter a topic or choose a Top News category? (topic/category): ")

if choice.lower() == "topic":
    # Ask the user for a topic
    topic = input("Enter a topic: ")
    # Call the function with the user input
    headlines = get_news(topic)
    file_name_base = topic
elif choice.lower() == "category":
    # Ask the user for a category
    category = input("Enter a category (general, world, nation, business, technology, entertainment, sports, science, health): ")
    # Call the function with the user input
    headlines = get_top_headlines(category)
    file_name_base = category
else:
    print("Invalid choice.")
    exit()

# Print the headlines
for headline in headlines:
    print(f"Title: {headline['title']}\nURL: {headline['url']}\nPublished At: {headline['published_at']}\n")

# Define the function to generate an article
def generate_editor(headline_strings):
    # Concatenate the headlines
    headlines_str = "\n".join(headline_strings)

    # Generate the text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an experienced senior news editor"},
            {"role": "user", "content": "Assess the following news headlines and, for each, make dot point notes on potential unique and engaging reporting angles that a journalist could follow up. Focus on new and different perspectives. Be specific: use prompts, examples and questions as a way of illustrating angles. Create a possible hypothesis for each. The headlines are:"},
            {"role": "user", "content": f"Headlines: {headlines_str}"}
        ],
        max_tokens=3500
    )

    # Extract the generated text
    generated_text = response["choices"][0]["message"]["content"]
    return generated_text

# Generate the article
headline_strings = [f"{headline['title']} (URL: {headline['url']}, Published At: {headline['published_at']})" for headline in headlines]
article = generate_editor(headline_strings)


# Save the article as a markdown file
file_name = file_name_base.replace(" ", "_") + ".md"
with open(file_name, "w") as f:
    f.write(f"# {file_name_base}\n\n")
    f.write(article)
    f.write("\n\n--SOURCES--\n")
    # Write the headlines, URLs, and published dates to the file
    for headline in headlines:
        f.write(f"Title: {headline['title']}\nURL: {headline['url']}\nPublished At: {headline['published_at']}\n\n")
print(f"Your news angles has been saved as {file_name}, good luck out there - go get 'em")


