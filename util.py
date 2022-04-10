import itertools
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
    ' ': 0,
    '?': 0,
    '' : 0
}
alfabet = "abcdefghijklmnopqrstuvwxyz"
def process(path: str):
    with open(f'{path}.txt','r') as s:
        wordlist = s.readlines()
    res = []
    for word in wordlist:
        word = word.strip()
        temp = 0
        for letter in word:
            # print(letter)
            temp+= values.get(letter.lower())
        res.append(word + ' ' + str(temp) + '\n')

    with open(f'{path}res.txt','w') as f:
        f.writelines(res)

def getValue(s: str, wildcard: str):
    res = 0
    for letter in s:
        res += values.get(letter)
    for letter in wildcard:
        res -= values.get(letter)
    return res

def parse(path: str):
    with open(f'{path}.txt','r') as r:
        temp = r.readlines()
    wr = [f'{line.split()[0]}\n' for line in temp]
    with open(f'{path}Parsed.txt','w') as w:
        w.writelines(wr)

def getList(path: str) -> list[str]:
    with open(f'{path}.txt','r') as f:
        wordlist = f.readlines()
    return [word.strip('\n').lower() for word in wordlist]

def getWildcard(s: str) -> set[tuple[str,str]]:
    res = set()
    count = s.count('?')
    temp = s.strip('?')
    test = [''.join(p) for p in itertools.product(alfabet,repeat = count)]
    a = set(tuple(sorted(x)) for x in test)
    for elem in a:
        b = temp + ''.join(elem) 
        res.add(b)
    return res

def permutations(s: str, wordlist:set[str]) -> set:
    a = set()
    for i in range(1,len(s)+1):
        b = [''.join(p) for p in itertools.permutations(s,i)]
        a = a.union(set(b))
    return wordlist.intersection(a)

def disjoin(full: str, part: str):
    for letter in part:
        full = full.replace(letter,'',1)
    return full

if __name__ == '__main__':
    # print(getList('TWL06'))
    print(getValue('aaazzz'))
    pass