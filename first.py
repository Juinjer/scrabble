import util

class Scrabble:
    def __init__(self, field: int) -> None:
        self.field = self.initfield(field)
        self.reprField()
        self.play()
        self.playplaces = [(field//2+1,field//2+1)]

    def initfield(self, dim: int):
        arr = [[' ' for i in range(dim)] for j in range(dim)]
        return arr
    
    def reprField(self):
        print('---------')
        for sublist in self.field:
            for elem in sublist:
                print(elem,end=' ')
            print()
        print('---------')

    def play(self):
        finished = True
        while finished:
            choice = input('0 you\'re playing, 1 input: ')
            if '0' == choice:
                avail = input("Enter letters: ")
                boardletters = self.getBoardLetter()
                if boardletters:
                    a: list[tuple[str,int]] = list()
                    for letter in boardletters:
                        a.extend(self.checkBest(avail+letter))
                    #todo need to know what letter was in field
                    res = util.sortList(a)
                    print(res)
                else:
                    print(self.checkBest(avail))
            elif '1' == choice:
                word = input("Word: ")
                pos = input("Position (fe. 00 00|25 25): ")
                dir = input("Direction (d|r): ")
                positions = util.parsePos(pos, dir, len(word))
                self.fillWord(positions,word)
                self.reprField()
            else:
                print("enter a valid option 0|1")
    
    def getBoardLetter(self) -> set[str]:
        res = set()
        for line in self.field:
            for elem in line:
                res.add(elem)
        res.remove(' ')
        return res
    
    def checkBest(self, available: str):
        temp = dict()
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
        # print(util.sortDict(temp))
        return util.sortDict(temp)[:10]
    
    def fillWord(self, positions: list[tuple[int, int]], word: str) -> None:
        i = 0
        for elem in positions:
            self.field[elem[0]][elem[1]] = word[i]
            i+=1
        
        
if __name__ == "__main__":
    Scrabble(25)