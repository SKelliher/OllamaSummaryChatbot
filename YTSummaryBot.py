from SummaryBot import SummaryBot

# SummaryBot parameters
fileTag = ''
summaryCount = 8
temperature = 0
model = 'wizardlm2'
systemPrompt = 'You are reading a YouTube transcript and will provide a summary'
queryPrompt = 'Summarize just the text sequentially in ' + str(summaryCount) + ' detailed and numbered points. Include a short caption to begin each point '
outputHeader = ''

# open VideoIDList
readPath = './Summary/L_VideoIDList.txt'
readList = ''

inputText = ''
with open(readPath, 'r', encoding="utf-8", errors="replace") as f_in:
    inputText += f_in.read()

inputLines = inputText.split('\n')

# main loop to process each line in inputLines
# then call the summaryBot for each VideoID in the first element of the line

countTranscript = 0 # Count number of video transcripts processed for monitoring progress in the terminal
for line in inputLines:
    if len(line) > 1:
        lineData = line.split('#^#')
        fileTag = lineData[2] + '_' + lineData[4] + '_' + lineData[0]
        
        outputHeader = 'URL: ' + lineData[1] + '\n'
        outputHeader += 'Author: ' + lineData[2]+ '\n'
        outputHeader += 'Title: ' + lineData[3]+ '\n'
        outputHeader += 'Published: ' + lineData[4]+ '\n'
        outputHeader += 'Length(seconds): ' + lineData[5]+ '\n'
        bot = SummaryBot(fileTag, model, temperature, summaryCount, systemPrompt, queryPrompt,outputHeader)
        bot.run()
        countTranscript += 1
        print ('\n--------------------------------------------------')
        print (str(countTranscript) + ' ' + fileTag + '\n')
    else:
        pass