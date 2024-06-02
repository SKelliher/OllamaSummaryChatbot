import llamabot
import datetime
from llamabot import SimpleBot

"""
[+] Amend output file name to Author-Published-# format. May use Mins-Secs for # to distinguish files. 
"""
class SummaryBot:
    def __init__(self, inputTag, outputTag, model, temperature, summaryCount, systemPrompt, queryPrompt, outputHeader,textAppend):
        self.inputTag = inputTag # input filename reference
        self.outputTag = outputTag # output filename reference
        self.model = model # ollama model parameter reference
        self.temperature = temperature
        self.summaryCount = str(summaryCount)
        self.systemPrompt = systemPrompt
        self.queryPrompt = queryPrompt
        self.ollamaModel = 'ollama/' + model
        self.outputHeader = outputHeader
        self.textAppend = textAppend # True or False

    """Generates an ID based on minutes and seconds for output file"""
    def time_mmss(self):

        # Get the current time.
        now = datetime.datetime.now()

        # Get the minutes and seconds.
        minutes = now.minute
        seconds = now.second

        # Convert the minutes and seconds to strings.
        minutes_str = str(minutes)
        seconds_str = str(seconds)

        # Pad the minutes and seconds with zeros if necessary.
        if len(minutes_str) == 1:
            minutes_str = "0" + minutes_str
        if len(seconds_str) == 1:
            seconds_str = "0" + seconds_str

        # Return the time in the form mmss.
        return minutes_str + seconds_str

    def process_input(self):
        inputPath = './Output/YB_' + self.inputTag + '.txt'
        outputPath = './Summary/' + self.outputTag + '_' + self.time_mmss() + '.md'

        inputText = ''
        with open(inputPath, 'r', encoding="utf-8", errors="replace") as f_in:
            inputText += f_in.read()

        with open(outputPath, 'w', encoding="utf-8", errors="replace") as f_out:
            f_out.write(self.outputHeader)
            f_out.write('\n')

        blocks = []
        blocks = inputText.split('[B]')

        bot = SimpleBot(self.systemPrompt, temperature=self.temperature, json_mode=False, model_name=self.ollamaModel)

        for i in range(len(blocks)):
            bot = SimpleBot(self.systemPrompt, temperature=self.temperature, json_mode=False, model_name=self.ollamaModel)
            if len(blocks[i].split()) > 10:  # Check there's text to summarize
                outputText = str(bot(blocks[i] + ' Instructions: ' + self.queryPrompt)) 
                endText = outputText.lstrip('content="').rstrip('" role=\'assistant\' ')

                with open(outputPath, "a", encoding="utf-8", errors="replace") as f_out:
                    for text in endText.split('\\n'):
                        f_out.write(text)
                        f_out.write('\n')
                    f_out.write('***')
                    f_out.write('\n')
        if self.textAppend:
            with open(outputPath, 'a', encoding="utf-8", errors="replace") as f_out:
                f_out.write("# Text" + '\n')
                f_out.write(inputText)
                f_out.write('***')
                f_out.write('\n')

    def run(self):
        self.process_input()
