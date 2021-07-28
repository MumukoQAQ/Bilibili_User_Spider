import random
def Generate(n=1000):
    print('正在生成uid...')
    uids = []
    while n !=0 :
        uid = random.randint(1,99999999)
        if str(uid)+',' not in uids:
            uids.append(str(uid)+',')
            n -= 1
    with open('./uid.txt','w') as f:
            f.writelines(uids)






