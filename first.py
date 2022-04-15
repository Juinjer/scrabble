import util
from copy import deepcopy


class Scrabble:
    def __init__(self, field: int, list: str = 'TWL06') -> None:
        self.wordlist = util.getWordList(list)
        self.field = self.initfield(field, '  ')
        self.valuemap = self.initfield(field, 0)
        self.updateMultipliers(self.valuemap)
        self.reprField(self.field)
        self.play()

    def initfield(self, dim: int, fill: str | int) -> list[list[str | int]]:
        arr = [[fill for i in range(dim)] for j in range(dim)]
        return arr

    def reprField(self, field: list[list[str]]):
        print('   |', end='')
        for i in range(len(field)):
            print('{:2}'.format(i), end='|')
        print()
        for i in range(len(field)):
            print('{:2} |'.format(i), end='')
            for j in range(len(field[0])):
                print('{:2}'.format(field[i][j]), end='|')
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
                        a = a | self.checkBest(avail + letter)
                    res = util.sortDict(a)
                    # self.displayOptions(res, avail)
                    tempboard = self.tempFill(res, avail)
                    fill = input('Want to fill? [y/n]: ')
                    if fill == 'y':
                        self.field = tempboard[0]
                        self.valuemap = tempboard[1]
                else:
                    res = self.checkBest(avail)
                    sor = util.sortDict(res)
                    self.displayOptions(sor, '')
            elif '1' == choice:
                word = input("Word: ")
                pos = input("Position (fe. 00 00|25 25): ")
                dir = input("Direction (d|r): ")
                positions = util.parsePos(pos, dir, len(word))
                self.fillWord(positions, word)
                self.reprField(self.field)
            elif 'q' == choice:
                finished = False
            else:
                print("enter a valid option 0|1")

    # def updateMultipliers(self) -> None:
    #     width = len(self.valuemap)  # TODO make dynamic
    #     w2 = [(1, 5), (1, 9), (1, 17), (1, 21), (3, 1), (3, 14), (3, 25), (5, 5), (5, 9), (5, 17), (5, 21), (7, 4), (7, 10), (7, 16), (7, 22)]
    #     pass

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
            variantions = util.permutations(available, self.wordlist, True)
        else:
            variantions = util.permutations(available, self.wordlist, False)
        for var in variantions:
            if var in self.wordlist:
                wildcard = util.disjoin(var, available)
                temp[var] = util.getValue(var, wildcard)
        # print(util.sortDict(temp))
        return temp

    def fillWord(self, positions: list[tuple[int, int]], word: str) -> None:
        tempboard = deepcopy(self.field)
        tempvalues = deepcopy(self.valuemap)
        for char, elem in zip(word, positions):
            if tempboard[elem[0]][elem[1]] == '  ':
                tempboard[elem[0]][elem[1]] = char
                tempvalues[elem[0]][elem[1]] = util.updateValues((elem[0], elem[1]), util.values.get(char), self.valuemap)
        if self.checkValidBoard(tempboard):
            self.field = tempboard
            self.valuemap = tempvalues
        else:
            print("not a valid word/position")

    def displayOptions(self, wordoptions: dict[str, int], available: str):
        for i, w in enumerate(wordoptions):
            boardletter = util.disjoin(w, available)
            if available:
                print(f'Play {w}, value: {wordoptions[w]} through letter {boardletter}')
            else:
                print(f'Play {w}, value: {wordoptions[w]}')
            if i == 20:
                break

    def tempFill(self, wordoptions: dict[str, int], available: str):
        bestvalue = 0
        best = (self.field, self.valuemap)
        for word in wordoptions:
            boardletter = util.disjoin(word, available)
            index = word.find(boardletter)
            if boardletter:  # TODO: implement without boardletter fe at edge of word
                for (posy, posx) in self.getPositions(boardletter):
                    tempboard = deepcopy(self.field)
                    tempvalues = deepcopy(self.valuemap)
                    beginh = posx - index
                    endh = posx - index + len(word)
                    valid = True
                    for char, i in zip(word, range(beginh, endh)):
                        if tempboard[posy][i] == '  ' or tempboard[posy][i] == boardletter:
                            tempboard[posy][i] = char
                            tempvalues[posy][i] = util.updateValues((posy, i), util.values.get(char), self.valuemap)
                        else:
                            valid = False
                    newval = util.getMapValue(tempboard, self.field)
                    if self.checkValidBoard(tempboard) and valid and newval > bestvalue:
                        bestvalue = newval
                        best = (tempboard, tempvalues)
                        # self.reprField(tempboard)
                        # return tempboard
                    tempboard = deepcopy(self.field)
                    beginv = posy - index
                    endv = posy - index + len(word)
                    valid = True
                    for char, i in zip(word, range(beginv, endv)):
                        if tempboard[i][posx] == '  ' or tempboard[i][posx] == boardletter:
                            tempboard[i][posx] = char
                            tempvalues[i][posx] = util.updateValues((i, posx), util.values.get(char), self.valuemap)
                        else:
                            valid = False
                    newval = util.getMapValue(tempboard, self.field)
                    if self.checkValidBoard(tempboard) and valid and newval > bestvalue:
                        bestvalue = newval
                        best = (tempboard, tempvalues)
                        # self.reprField(tempboard)
                        # return tempboard
        self.reprField(best[0])
        return best

    def getPositions(self, letter: str) -> str:
        res = []
        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                if letter == self.field[i][j]:
                    res.append((i, j))
        return res


if __name__ == "__main__":
    Scrabble(27)
