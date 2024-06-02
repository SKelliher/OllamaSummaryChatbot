# OllamaSummaryChatbot
This is a Python project for personal information management. The goal is to take a source file (e.g. PDF, YouTube transcript or Web Page), parse the source file into blocks (eg of 1000 words), and then pass the parsed text sequentially to a local-instance LLM ChatBot running under Ollama to create a summary of the original text.

# venv
For execution, this is running in a virtualenv .\venv subdirectory with 

## libraries
* re - installed globally
* datetime - installed globally
* pytube - installed locally using pip
* youtube_transcript_api - installed locally using pip
* llamabot - installed locally using pip - large dependency install

## sub-directories
Create subdirectories ./venv/Summary and ./venv/Output for holding processing files
