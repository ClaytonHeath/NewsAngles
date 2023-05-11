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
    url = f"https://gnews.io/api/v4/search?q={topic}&lang=en&country=us&max=05&apikey={gnewsapikey}"
    # Fetch the data from the API
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
    # Get the articles from the data
    articles = data["articles"]
    # Initialize an empty list to store the headlines
    headlines = []
    # Loop through the first 5 articles
    for i in range(5):
        # Get the title of the article
        title = articles[i]["title"]
        # Get the URL of the article
        url = articles[i]["url"]
        # Get the published date of the article
        published_at = articles[i]["publishedAt"]
        # Append it to the headlines list as a dictionary
        headlines.append({'title': title, 'url': url, 'published_at': published_at})
    # Return the headlines as a variable
    return headlines


# Ask the user for a topic
topic = input("Enter a topic: ")
# Call the function with the user input
headlines = get_news(topic)
# Print the headlines
print(headlines)


# Define the function to generate an article
def generate_editor(headlines):
    
    # Create a string that includes the headline, URL, and published date for each article
    headlines_str = "\n".join([f"Title: {headline['title']}\nURL: {headline['url']}\nPublished At: {headline['published_at']}" for headline in headlines])


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", ##choose "gpt-4" or "gpt-3.5-turbo'
        messages=[
            {"role": "system", "content": "You are an experienced senior news editor"},
            {"role": "user", "content": "Assess the following news headlines and, for each, make dot point notes on potential unique and engaging reporting angles that a journalist could follow up. Focus on new and different perspectives. Be specific: use prompts, examples and questions as a way of illustrating angles. Create a possible hypothesis for each. The headlines are:"},
            {"role": "user", "content": f"Headlines {headlines}"}
        ],
        max_tokens=3500  # Increase this value to generate a longer article
    )

    # Extract the generated text
    generated_text = response["choices"][0]["message"]["content"]
    # Return the generated text
    return generated_text



# Generate the article
article = generate_editor(headlines)

# Save the article as a markdown file
file_name = topic.replace(" ", "_") + ".md"
with open(file_name, "w") as f:
    f.write(f"# {topic}\n\n")
    f.write(article)
    f.write("\n\n--SOURCES--\n")
    # Write the headlines, URLs, and published dates to the file
    for headline in headlines:
        f.write(f"Title: {headline['title']}\nURL: {headline['url']}\nPublished At: {headline['published_at']}\n\n")
print(f"Your news angles has been saved as {file_name}, good luck out there - go get 'em")


