# Import the libraries
import openai
import os
from dotenv import load_dotenv
from tqdm import tqdm  # Import the tqdm library

# Load the environment variables from the .env file
load_dotenv()

# Define the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the function to generate an article
def generate_article(title, keywords):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", ##choose "gpt-4" or "gpt-3.5-turbo'
        messages=[
            {"role": "system", "content": "You are a masterful business copywriter with 10 years professional experience."},
            {"role": "user", "content": "write a 1200 to 1500 word blog post based on the following topic and key words. Write in a tone and style described as engaging, conversational, and informative, to capture the reader's attention. Vary  paragraph and sentence length to keep the article interesting. Here are the topic and keywords:"},
            {"role": "user", "content": f"Topic: {title}\nKeywords: {keywords}\nArticle:\n"}
        ],
        max_tokens=2000  # Increase this value to generate a longer article
    )

    # Extract the generated text
    generated_text = response["choices"][0]["message"]["content"]
    # Return the generated text
    return generated_text

def get_editor_feedback(title, generated_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", ##choose "gpt-4" or "gpt-3.5-turbo'
        messages=[
            {"role": "system", "content": "You are an expert blog post article editor with 10 years of experience."},
            {"role": "user", "content": f"Please provide detailed dot point notes on improving the following article on the topic '{title}' by reviewing the draft and provide a critique and use specific examples from the text on what should be done to improve the draft. Optimise for engaging and informative content. Ensure one point of recommendation is to 'write 2 to 4 paragraphs per subheading'. Here is the draft:"},
            {"role": "user", "content": generated_text},
        ],
    )

    editor_feedback = response["choices"][0]["message"]["content"]
    return editor_feedback


def get_seo_feedback(title, generated_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", ##choose "gpt-4" or "gpt-3.5-turbo'
        messages=[
            {"role": "system", "content": "You are an SEO expert with 10 years experience in online SEO optimisation."},
            {"role": "user", "content": f"Review the following article on the topic '{title}' and provide dot point notes with specific examples from the text on how to optimize its SEO content. Recommend SEO-friendly titles and subtitles that could be used. Ensure one point of recommendation is to 'write 2 to 4 paragraphs per subheading'. Here is the article:"},
            {"role": "user", "content": generated_text},
        ],
    )

    seo_feedback = response["choices"][0]["message"]["content"]
    return seo_feedback


def rewrite_article(title, generated_text, editor_feedback, seo_feedback):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", ##choose "gpt-4" or "gpt-3.5-turbo'
        messages=[
            {"role": "system", "content": "You are a masterful business copywriter with 10 years of professional experience."},
            {"role": "user", "content": f"Take note of the feedback given by the article editor and the SEO expert, and use that information to expand on the following article on the topic '{title}':"},
            {"role": "user", "content": f"Article:{generated_text}"},
            {"role": "user", "content": f"Article Editor Feedback:\n{editor_feedback}\n\nSEO Expert Feedback:\n{seo_feedback}\n"},
        ],
        max_tokens=2000  # Increase this value to generate a longer article
    )

    revised_article = response["choices"][0]["message"]["content"]
    return revised_article

# Create a wrapper function for the progress bar
def generate_and_rewrite_article_with_progress(title, keywords):
    with tqdm(total=4) as pbar:
        # Generate the article
        pbar.set_description("Generating article")
        article = generate_article(title, keywords)
        pbar.update(1)

        # Get editor feedback
        pbar.set_description("Getting editor feedback")
        editor_feedback = get_editor_feedback(title, article)
        pbar.update(1)

        # Get SEO feedback
        pbar.set_description("Getting SEO feedback")
        seo_feedback = get_seo_feedback(title, article)
        pbar.update(1)

        # Rewrite the article based on feedback
        pbar.set_description("Revising article")
        revised_article = rewrite_article(title, article, editor_feedback, seo_feedback)
        pbar.update(1)

    return article, revised_article, editor_feedback, seo_feedback


# Get the input from the user
title = input("Enter the title or topic of the article: ")
keywords = input("Enter the keywords for the article (separated by commas): ")

# Call the wrapper function
article, revised_article, editor_feedback, seo_feedback = generate_and_rewrite_article_with_progress(title, keywords)

# Generate the article
article = generate_article(title, keywords)

# Get editor feedback
editor_feedback = get_editor_feedback(title, article)

# Save the editor notes as a markdown file
editor_notes_file_name = title.replace(" ", "_") + "_editor_notes.md"
with open(editor_notes_file_name, "w") as f:
    f.write(f"# Editor Notes for {title}\n\n{editor_feedback}")
print(f"Your editor notes have been saved as {editor_notes_file_name}")

# Get SEO feedback
seo_feedback = get_seo_feedback(title, article)

# Save the SEO notes as a markdown file
seo_notes_file_name = title.replace(" ", "_") + "_seo_notes.md"
with open(seo_notes_file_name, "w") as f:
    f.write(f"# SEO Notes for {title}\n\n{seo_feedback}")
print(f"Your SEO notes have been saved as {seo_notes_file_name}")

# Rewrite the article based on feedback
revised_article = rewrite_article(title, article, editor_feedback, seo_feedback)

# Print the article to the user
#print(f"Here is your article:\n{article}")

# Save the article as a markdown file
file_name = title.replace(" ", "_") + ".md"
with open(file_name, "w") as f:
    f.write(f"# {title}\n\n{article}")
print(f"Your article has been saved as {file_name}")

# Print the revised article
#print(f"Here is the revised article:\n{revised_article}")

# Save the revised article as a markdown file
revised_file_name = title.replace(" ", "_") + "_revised.md"
with open(revised_file_name, "w") as f:
    f.write(f"# {title}\n\n{revised_article}")
print(f"Your revised article has been saved as {revised_file_name}")
