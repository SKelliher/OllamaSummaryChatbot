from SummaryBot import SummaryBot
from datetime import datetime
import re

# Run-Time program to read YT Video meta-data from VideoIDList and process associated block files to create a summary. 

# SummaryBot parameters
fileTag = ''
summaryCount = 20
temperature = 0
model = 'Lydia'
systemPrompt = 'You are reading a YouTube transcript and will provide a summary'
queryPrompt = 'Please provide a detailed summary of the text in about ' 
queryPrompt += str(summaryCount) + ' detailed and numbered points. Do not add additional comments.'
# queryPrompt = 'Summarize just the text sequentially in ' + str(summaryCount) + ' detailed and numbered points. Include a short caption to begin each point '
outputHeader = ''

# open VideoIDList
readPath = './Summary/YL_VideoIDList.txt'
readList = ''

inputText = ''
with open(readPath, 'r', encoding="utf-8", errors="replace") as f_in:
    inputText += f_in.read()

inputLines = inputText.split('\n')

# main loop to process each line in inputLines
# then call the summaryBot for each VideoID in the first element of the line

# convert date from YYMMDD to MM/DD/YY
def convert_date(date_str):
    year = "20" + date_str[:2]
    month = date_str[2:4]
    day = date_str[4:6]
    dt = datetime(int(year), int(month), int(day))
    return dt.strftime("%m/%d/%Y")

# remove characters in title that are problematic in YAML front matter
def remove_problematic_chars(text):
    # Define the characters to remove
    chars_to_remove = r'[:#\-\\@\$!]'
    # Use regular expressions to replace these characters with an empty string
    clean_text = re.sub('[' + re.escape(chars_to_remove) + ']', '', text)
    return clean_text

countTranscript = 0 # Count number of video transcripts processed for monitoring progress in the terminal
for line in inputLines:
    if len(line) > 1:
        lineData = line.split('#^#')
        fileTitle = remove_problematic_chars(lineData[3])
        fileTag = lineData[2] + '_' + lineData[4] + '_' + lineData[0]
        
        outputHeader = '---' + '\n'
        outputHeader += 'tags: #document' + '\n'
        outputHeader += 'URL: ' + lineData[1] + '\n'
        outputHeader += 'Author: ' + lineData[2]+ '\n'
        outputHeader += 'Title: ' + fileTitle + '\n'
        outputHeader += 'Published: ' + convert_date(lineData[4])+ '\n'
        outputHeader += 'Seconds: ' + lineData[5]+ '\n'
        outputHeader += '---' + '\n'
        bot = SummaryBot(fileTag, model, temperature, summaryCount, systemPrompt, queryPrompt,outputHeader,True)
        bot.run()
        countTranscript += 1
        print ('\n--------------------------------------------------')
        print (str(countTranscript) + ' ' + fileTag + '\n')
    else:
        pass