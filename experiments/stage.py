def aaaa(x,v,D):
    #tv + x = Dn

    if int(x/D) == int((v+x)/D):
        return None

    #キャラが存在しうる格子の範囲を求める
    if v >= 0:
        minX, maxX = int(x/D), int((v + x)/D)
    else:
        minX, maxX = int((v + x)/D), int(x/D)

    t_list = []
    for n in range(minX, maxX+1):
        t = (D*n - x) / v
        if t < 0 or t > 1:
            continue
        else:
            t_list.append(t) 

    return ((minX, maxX), t_list)

print(aaaa(32*15+23, -32*8+4, 32))
print(aaaa(32*15+13, 32*3+4, 32))
