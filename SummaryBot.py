import llamabot
from llamabot import SimpleBot

class SummaryBot:
    def __init__(self, fileTag, model, temperature, summaryCount, systemPrompt, queryPrompt, outputHeader,textAppend):
        self.fileTag = fileTag
        self.model = model
        self.temperature = temperature
        self.summaryCount = str(summaryCount)
        self.systemPrompt = systemPrompt
        self.queryPrompt = queryPrompt
        self.ollamaModel = 'ollama/' + model
        self.outputHeader = outputHeader
        self.textAppend = textAppend # True or False

    def process_input(self):
        inputPath = './Output/YB_' + self.fileTag + '.txt'
        outputPath = './Summary/YS_' + self.fileTag + '_' + self.model + '_' + self.summaryCount + '.md'

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
