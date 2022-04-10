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
        wilds = dict()
        wordlist = util.getList('NWL2020Parsed')
        if '?' in available:
            avalist = util.getWildcard(available)
            variantions = set()
            for elem in avalist:
                x = util.permutations(elem, set(wordlist))
                variantions = variantions.union(x)
        else:
            variantions = util.permutations(available, set(wordlist))
        for var in variantions:
            if var in wordlist:
                # print(var)
                wildcard = util.disjoin(var,available)
                temp[var] = util.getValue(var, wildcard)
        print(sorted(temp.items(), key=lambda item: item[1], reverse=True)[:20])
        return sorted(temp.items(), key=lambda item: item[1], reverse=True)
        
        
if __name__ == "__main__":
    Scrabble(10)