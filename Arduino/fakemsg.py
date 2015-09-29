carte = '1111111110000010100000000011000000000000000000011110000011001110'
out = []
for i in carte:
    if i == '0':
        out += [0,1]
    else :
        out += [1,0]
msg = ['h 240']
n = 1
while n < len(out)-1:
    mot = out[n:n+2]
    if mot == [0,0]:
        msg += ['l 480']
        n += 1
    elif mot == [1,1]:
        msg += ['h 480']
        n += 1
    elif mot[0] == 0:
        msg += ['l 240']
    else:
        msg += ['h 240']
    n += 1
    