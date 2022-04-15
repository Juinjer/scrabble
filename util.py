from typing import Tuple
values = {
    'a': 1,
    'b': 3,
    'c': 3,
    'd': 2,
    'e': 1,
    'f': 4,
    'g': 2,
    'h': 4,
    'i': 1,
    'j': 8,
    'k': 5,
    'l': 1,
    'm': 3,
    'n': 1,
    'o': 1,
    'p': 3,
    'q': 10,
    'r': 1,
    's': 1,
    't': 1,
    'u': 1,
    'v': 4,
    'w': 4,
    'x': 8,
    'y': 4,
    'z': 10,
    '  ': 0,
    '?': 0,
    '': 0
}
alfabet = "abcdefghijklmnopqrstuvwxyz"


def process(path: str):
    with open(f'{path}.txt', 'r') as s:
        wordlist = s.readlines()
    res = []
    for word in wordlist:
        word = word.strip()
        temp = 0
        for letter in word:
            # print(letter)
            temp += values.get(letter.lower())
        res.append(word + ' ' + str(temp) + '\n')

    with open(f'{path}res.txt', 'w') as f:
        f.writelines(res)


def getValue(s: str, wildcard: str):
    res = 0
    for letter in s:
        res += values.get(letter)
    for letter in wildcard:
        res -= values.get(letter)
    return res


def parse(path: str):
    with open(f'{path}.txt', 'r') as r:
        temp = r.readlines()
    wr = [f'{line.split()[0]}\n' for line in temp]
    with open(f'{path}Parsed.txt', 'w') as w:
        w.writelines(wr)


def getWordList(path: str) -> set[str]:
    with open(f'{path}.txt', 'r') as f:
        wordlist = f.readlines()
    return set([word.strip('\n').lower() for word in wordlist])

# def wildcarPerm(s: str, wordlist: set[str]) -> None:
#     res = set()
#     count = s.count('?')
#     temp = s.strip('?')
#     for word in wordlist:
#         if checkWord(word, temp, count):
#             res.add(word)
#     return res

# def getWildcard(s: str) -> set[tuple[str,str]]:
#     res = set()
#     count = s.count('?')
#     temp = s.strip('?')
#     test = [''.join(p) for p in itertools.product(alfabet,repeat = count)]
#     a = set(tuple(sorted(x)) for x in test)
#     for elem in a:
#         b = temp + ''.join(elem)
#         res.add(b)
#     return res


def permutations(s: str, wordlist: set[str], wildcard: bool = False) -> set:
    a = set()
    if wildcard:
        count = s.count('?')
        temp = s.strip('?')
        for word in wordlist:
            if checkWord(word, temp, count):
                a.add(word)
    else:
        for word in wordlist:
            if checkWord(word, s):
                a.add(word)
    return a


def checkWord(word: str, available: str, wildcards: int = 0) -> bool:
    # if word == 'bechalking':
    #     print(word)
    for x in word:
        if x not in available:
            if wildcards == 0:
                return False
            else:
                wildcards -= 1
        available = available.replace(x, '', 1)
    return True

# def permutations(s: str, wordlist:set[str]) -> set:
#     first = time.time()
#     a = set()
#     for i in range(1,len(s)+1):
#         b = [''.join(p) for p in itertools.permutations(s,i)]
#         a = a.union(set(b))
#         a = a.intersection(wordlist)
#         # print(len(a))
#     second = time.time()
#     print("1 " + str(second-first))
#     return wordlist.intersection(a)


def disjoin(full: str, part: str):
    for letter in part:
        full = full.replace(letter, '', 1)
    return full


def parsePos(s: str, dir: str, length: int) -> list[tuple[int, int]]:
    res: list[tuple[int, int]] = []
    posx, posy = s.split()
    first = (int(posx), int(posy))
    # second = (int(pos2[0]), int(pos2[1]))
    # diff = (abs(second[0]-first[0]),abs(second[1]-first[1]))
    if dir == 'r':
        for i in range(first[1], first[1] + length):
            res.append((first[0], i))
    else:
        for i in range(first[0], first[0] + length):
            res.append((i, first[1]))
    return res


def sortDict(dic: dict) -> dict:
    return dict(sorted(dic.items(), key=lambda item: item[1], reverse=True))


def sortList(lis: list[tuple[str, int]]) -> list[tuple[str, int]]:
    return sorted(lis, key=lambda tup: tup[1], reverse=True)


def getMapValue(maps: list[list[str]], oldmap: list[list[str]]) -> int:
    res = 0
    # for line in maps:
    #     res += sum(line)
    for word in getAllWords(maps):
        res += getValue(word, '')

    for word in getAllWords(oldmap):
        res -= getValue(word, '')
    return res


def getAllWords(stringmap: list[list[str]]) -> list[str]:
    words = []
    for line in stringmap:
        word = ''.join(line)
        words.extend([x for x in word.split('  ') if len(x) > 1])
    for i in range(len(stringmap[0])):
        word = ''.join([stringmap[j][i] for j in range(len(stringmap))])
        words.extend([x for x in word.split('  ') if len(x) > 1])
    return words


def updateValues(position: Tuple[int, int], value: int, map: list[list[str | int]]) -> None:
    map[position[0]][position[1]] = value


if __name__ == '__main__':
    print(permutations("abcdefghi", getWordList('NWL2020Parsed')))
    # print(permutations2("abcdefghi",getWordList('NWL2020Parsed')))
    pass
