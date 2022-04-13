from operator import index
import util
from copy import deepcopy

class Scrabble:
    def __init__(self, field: int, list: str = 'TWL06') -> None:
        self.wordlist = util.getWordList(list)
        self.field = self.initfield(field, '  ')
        self.valuemap = self.initfield(field, 0)
        self.reprField(self.field)
        self.play()
        self.playplaces = set((field//2+1,field//2+1))

    def initfield(self, dim: int, fill: str|int) -> list[list[str | int]]:
        arr = [[fill for i in range(dim)] for j in range(dim)]
        return arr
    
    def reprField(self, field: list[list[str]]):
        print('   |',end='')
        for i in range(len(field)):
            print('{:2}'.format(i),end='|')
        print()
        for i in range(len(field)):
            print('{:2} |'.format(i), end='')
            for j in range(len(field[0])):
                print('{:2}'.format(field[i][j]),end='|')
            print()

    def play(self):
        finished = True
        while finished:
            choice = input('0 you\'re playing, 1 input: ')
            if '0' == choice:
                avail = input("Enter letters: ")
                boardletters = self.getBoardLetter()
                if boardletters:
                    a = dict()
                    for letter in boardletters:
                        a = a | self.checkBest(avail+letter)
                    res = util.sortDict(a)
                    self.displayOptions(res, avail)
                    self.tempFill(res,avail)
                else:
                    res = self.checkBest(avail)
                    sor = util.sortDict(res)
                    self.displayOptions(sor, '')
            elif '1' == choice:
                word = input("Word: ")
                pos = input("Position (fe. 00 00|25 25): ")
                dir = input("Direction (d|r): ")
                positions = util.parsePos(pos, dir, len(word))
                self.fillWord(positions,word)
                self.reprField(self.field)
            else:
                print("enter a valid option 0|1")
    
    def checkValidBoard(self, board: list[list[str]]) -> bool:
        for line in board:
            valid = self.checkLine(line)
            if not valid:
                return False
        for i in range(len(board[0])):
            temp = [board[j][i] for j in range(len(board))]
            valid = self.checkLine(temp)
            if not valid:
                return False
        return True

    def checkLine(self, line: list[str]) -> bool:
        linestr = ''.join(line)
        words = linestr.split('  ')
        for word in words:
            if len(word) > 1 and word not in self.wordlist:
                return False
        return True


    def getBoardLetter(self) -> set[str]:
        res = set()
        for line in self.field:
            for elem in line:
                res.add(elem)
        res.remove('  ')
        return res
    
    def checkBest(self, available: str):
        temp = dict()
        if '?' in available:
            avalist = util.getWildcard(available)
            variantions = set()
            for elem in avalist:
                x = util.permutations(elem, self.wordlist)
                variantions = variantions.union(x)
        else:
            variantions = util.permutations(available, self.wordlist)
        for var in variantions:
            # print(var)
            if var in self.wordlist:
                # print(var)
                wildcard = util.disjoin(var,available)
                temp[var] = util.getValue(var, wildcard)
        # print(util.sortDict(temp))
        return temp
    
    def fillWord(self, positions: list[tuple[int, int]], word: str) -> None:
        tempboard = deepcopy(self.field)
        tempvalues = deepcopy(self.valuemap)
        i = 0
        for elem in positions:
            if tempboard[elem[0]][elem[1]] == '  ':
                tempboard[elem[0]][elem[1]] = word[i]
                tempvalues[elem[0]][elem[1]] = util.values.get(word[i])
            i+=1
        if self.checkValidBoard(tempboard):
            self.field = tempboard
        else:
            print("not a valid word/position")

    def displayOptions(self, wordoptions: dict[str, int], available: str):
        i = 0
        for w in wordoptions:
            boardletter = util.disjoin(w, available)
            if available:
                print(f'Play {w}, value: {wordoptions[w]} through letter {boardletter}')
            else:
                print(f'Play {w}, value: {wordoptions[w]}')
            if i == 19:
                break
            i += 1
    
    def tempFill(self, wordoptions: dict[str, int], available: str) -> list[list[dict[str, int]]]:
        for w in wordoptions:
            boardletter = util.disjoin(w, available)
            index = w.find(boardletter)
            if boardletter:
                for (posy,posx) in self.getPositions(boardletter):
                    tempboard = deepcopy(self.field)
                    tempvalues = deepcopy(self.valuemap)
                    beginh = posx - index
                    endh = posx - index + len(w)
                    j = 0
                    valid = True
                    for i in range(beginh,endh):
                        if tempboard[posy][i] == '  ' or tempboard[posy][i] == boardletter:
                            tempboard[posy][i] = w[j]
                            tempvalues[posy][i] = util.values.get(w[j])
                        else:
                            valid = False
                        j +=1
                    if self.checkValidBoard(tempboard) and valid:
                        self.reprField(tempboard)
                        return tempboard
                    tempboard = deepcopy(self.field)
                    beginv = posy - index
                    endv = posy - index + len(w)
                    j = 0
                    valid = True
                    for i in range(beginv,endv):
                        if tempboard[i][posx] == '  ' or tempboard[i][posx] == boardletter:
                            tempboard[i][posx] = w[j]
                            tempvalues[i][posx] = util.values.get(w[j])
                        else:
                            valid = False
                        j +=1
                    if self.checkValidBoard(tempboard) and valid:
                        self.reprField(tempboard)
                        return tempboard
    
    def getPositions(self, letter: str)-> str:
        res = []
        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                if letter == self.field[i][j]:
                    res.append((i,j))
        return res
        
        
if __name__ == "__main__":
    Scrabble(30)