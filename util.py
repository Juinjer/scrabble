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
    '\n': 0
}
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

def parse(path: str):
    with open(f'{path}.txt','r') as r:
        temp = r.readlines()
    wr = [f'{line.split()[0]}\n' for line in temp]
    with open(f'{path}Parsed.txt','w') as w:
        w.writelines(wr)

def getList(path: str):
    with open(f'{path}.txt','r') as f:
        wordlist = f.readlines()
    test = dict()
    for word in wordlist:
        worde, val = word.split(' ')
        test[worde.lower()] = int(val)
    return test

def permutations(s: str):
    a = set()
    for i in range(1,len(s)+1):
        b = [''.join(p) for p in itertools.permutations(s,i)]
        a = a.union(set(b))
    return a

if __name__ == '__main__':
    process('NWL2020Parsed')
    pass