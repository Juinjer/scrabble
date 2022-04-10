import util

class Scrabble:
    def __init__(self, field) -> None:
        self.field = self.initfield(field)
        self.play()

    def initfield(self, dim: int):
        arr = [[[] for i in range(dim)] for j in range(dim)]
        return arr

    def play(self):
        finished = True
        while finished:
            avail = input("Enter letters: ")
            self.checkBest(avail)
    
    def checkBest(self, available: str):
        temp = dict()
        wordlist = util.getList('NWL2020Parsedres')
        variantions = util.permutations(available)
        for var in variantions:
            if var in wordlist:
                temp[var] = wordlist.get(var)
        # print(temp)
        print(sorted(temp.items(), key=lambda item: item[1], reverse=True))
        return sorted(temp.items(), key=lambda item: item[1], reverse=True)
        
        
if __name__ == "__main__":
    Scrabble(10)