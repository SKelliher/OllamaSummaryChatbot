# To Do List - Current
* Add a Conda wrapper for the Project

# To Do List - Backlog
* Add a config file and Configuration Class for installation and run-time options
* Add a simple database to track YouTube video data
    * Use database calls to find videos to be processed through the ChatBot
    * DB should allow searches based on incomplete status, by added date, created date, length and author
* Set up PDF Reader Class and Run-Time Program
* Set up Webpage Reader and Run-Time Program

# To Do List - Complete
* Add program to read VideoIDList output from YTDownloadPlayList
    * parse it to extract VideoIDs
    * For each VideoID retrieve associated parsed Block File
    * Send to SummaryBot to create a summary file

# YTSummaryBot Prompts/Models/SummaryCount to Try
* queryPrompt = 'Provide a brief overall summary of the text. Also provide a detailed  summary of the text in ' + str(summaryCount) + ' detailed and numbered points. Do not add additional comments.' ; Llama3 ; 8
* queryPrompt = 'Summarize just the text sequentially in ' + str(summaryCount) + ' detailed and numbered points. Include a short caption to begin each point ' ;  wizardLM2 ; 8

