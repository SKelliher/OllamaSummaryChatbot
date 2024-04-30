# To Do List - Current
* Add a config file and Configuration Class for installation and run-time options

# To Do List - Backlog
* Add a simple database to track YouTube video data
    * Use database calls to find videos to be processed through the ChatBot
    * DB should allow searches based on incomplete status, by added date, created date, length and author

# To Do List - Complete
* Add program to read VideoIDList output from YTDownloadPlayList
    * parse it to extract VideoIDs
    * For each VideoID retrieve associated parsed Block File
    * Send to SummaryBot to create a summary file