from SummaryBot import SummaryBot

# open VideoIDList
readPath = './Summary/L_VideoIDList.txt'
readList = ''

inputText = ''
with open(readPath, 'r', encoding="utf-8", errors="replace") as f_in:
    inputText += f_in.read()

inputLines = inputText.split('\n')

# main loop to process each line in inputLines
# then call the summaryBot for each VideoID in the first element of the line

for line in inputLines:
    lineData = line.split('#^#')
    print (lineData[0], lineData[2], lineData[3])

# bot = SummaryBot(fileTag, model, 1, summaryCount, systemPrompt, queryPrompt,outputHeader)
# bot.run()