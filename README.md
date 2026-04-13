# alfred-ai-agent
A simple AI agent, written in Python, powered by Gemini.

This is a hobby project. USE AT YOUR OWN RISK

## Setup:
Create a file in the root directory named '.env'. In it, put the following line:
```
GEMINI_API_KEY='your-gemini-api-key'
```

In the constants.py file, set your working directory. The agent will not have access outside this folder (probably):
```
WORKING_DIR = "YOUR_WORKING_DIRECTORY_HERE"
```
## Basic Usage:
```
python3 main.py "your-prompt-here"
```
### Additional options:
```
--verbose: Outputs token consumption and user input prompt in addition to the models response.
```