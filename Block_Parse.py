import re
class Block_Parse:
    def __init__(self, readName, headerRows, blockLimit):
        self.readName = readName
        self.headerRows = headerRows
        self.readPath = r'./Output/P_'  + self.readName + '.txt'
        self.writePath = r'./Output/B_' + self.readName + '.txt'
        self.blockLimit = blockLimit

    def load_text(self):
        with open(self.readPath, 'r', encoding="utf-8", errors="replace") as file:
            self.text = file.read()
        lines = self.text.split('\n')
        self.headerLines = lines[:self.headerRows]
        self.blockLines = lines[self.headerRows:]        
    
        # Store header/block lines to header/block Text
        self.headerText = ''
        self.blockText= ''

        for line in self.headerLines:
            self.headerText += str(line) + ' '        

        for line in self.blockLines:
            self.blockText += str(line) + ' '      

    def wordBlock_write(self):
        self.outputText = ''
        headerSize = len(self.headerText.split())
        self.wordBlock = []
        outWord = ''
        for word in self.blockText.split():
            if len(outWord.split()) + len(word.split()) + headerSize + 2 > self.blockLimit:
                self.wordBlock.append(outWord)
                outWord = word
            else:
                outWord += ' ' + word
        self.wordBlock.append(outWord)
        self.wordBlock = [self.headerText + ' ' + block + '[B]' for block in self.wordBlock]
        with open(self.writePath, 'w', encoding="utf-8", errors="replace") as file:
            file.write('\n'.join(self.wordBlock))
