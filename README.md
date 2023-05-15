# NewsAngles - Your AI Editor-in-Chief

**Note:** A little heads-up: I'm not a coder, and I'm learning the ropes when it comes to the sacred art of crafting the README.md. But, hey, I've given it a good try, by stealing from the pros I've observed in the wilds of other repositories. If you spot something awry, or you've got a shiny new improvement, don't be shy - whip up a pull request (I think that's what it's called, right?) and make it better!

I've written about this project over at Medium: [Article Headline](URL to come). You can hit me up on Twitter [@claytonhm](https://twitter.com/claytonhm)

NewsAngles uses headlines from Gnews and GPT-4 from OpenAI API to give writers unique ideas and angles to write about.

Tech stack is Python, [OpenAI](https://platform.openai.com/docs/introduction) API and [GNews API](https://gnews.io/docs/v4#introduction).

## Setup Environment

1. Clone the repo or download the ZIP
2. Copy .env.example into .env 
```
cp .env.template .env
```

Your .env file should look like this:
```
# Add your API keys
OPENAI_API_KEY=
GNEWS_API_KEY=
LLM_MODEL=gpt-4 #gpt-4 or gpt-3.5-turbo
MAX_TOKENS=6000     #~3500 for GPT-3.5-turbo or ~7500 for gpt-4
```
3. Visit openai to retrieve API keys and insert into your .env file. Visit Gnews to retrieve API keys and insert into your .env file.
4. Choose which gpt model to use (as of 15th May 2023, not everyone has access to GPT-4). 
5. Use the guidance to enter the relevant Max Tokens based on the GPT model you're using

## Run NewsAngles
At the command line, run:
```python3 newsangles.py```

