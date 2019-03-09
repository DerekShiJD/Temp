# version 2
test1 = ['2', 'B A C E D', 'A C', 'C B D']
test2 = ['2', 'data mining', 'frequent pattern mining',
         'mining frequent patterns from the transaction dataset',
         'closed and maximal pattern mining']
test3 = ['2', 'A B C D E', 'A B C D E', 'A B C D E']
test4 = ['2', 'A B C D', 'A B C D', 'A B C D']
scl = 30
a = ['.'] * scl
row_num = 0     #num of input rows

'''
try:
    while True:
        a[row_num] = input()
        row_num += 1
except EOFError:
    pass
'''
''' !!! delete the line below'''
a = test4
row_num = len(a)

b = [['.' for i in range(scl)]for i in range(scl)]      # 存放二维数组化后的a
b_num = [0 for i in range(scl)]     # 每一层有多少个对象

sop = int(a[0])     # support最小值

tempchar = ''
checklist = ['.']*scl*10   # 需要查找的对象，组合对象存放处，每层结束要初始化！！
checklist_len = 0       # 该层需要check的对象的个数，注意每层需要清零！！
checklist_tempcount = [0 for i in range(scl*10)] # 清零


Flist = [['.' for i in range(scl)]for i in range(scl)]      # 存放每一层符合条件的对象
Flist_anchor = [[0 for i in range(scl)]for i in range(scl)]     # 每一层每一个对象开始的坐标,对象长度为层数加1
count = [[0 for i in range(scl)]for i in range(scl)]        # 每一层每一个对象出现次数
Flist_num = [0 for i in range(scl)]         # 每一层有多少个符合条件的对象

# 第一层：字符串删除空格，变为数组，存进b
for i in range(1, row_num):
    for j in range(len(a[i])):
        if a[i][j] != ' ':
            tempchar = tempchar + a[i][j]
        else:
            b[i-1][b_num[i-1]] = tempchar
            b_num[i-1] += 1
            tempchar = ''
    b[i-1][b_num[i-1]] = tempchar
    b_num[i-1] += 1
    tempchar = ''

# 形成第一层checklist
for i in range(row_num-1):
    for j in range(b_num[i]):
        if b[i][j] not in checklist:
            checklist[checklist_len] = b[i][j]
            checklist_tempcount[checklist_len] += 1
            checklist_len += 1
        else:
            checklist_tempcount[checklist.index(b[i][j])] += 1

for i in range(checklist_len):
    if checklist_tempcount[i] >= sop:
        Flist[0][Flist_num[0]] = checklist[i]
        count[0][Flist_num[0]] = checklist_tempcount[i]
        Flist_anchor[0][Flist_num[0]] = Flist_num[0]
        Flist_num[0] += 1
Flist_anchor[0][Flist_num[0]] = Flist_num[0]

checklist = ['.'] * scl * 10  # 需要查找的对象，组合对象存放处，每层结束要初始化！！
checklist_anhor = [0 for i in range(scl * 10)]   # 清零
checklist_len = 0  # 该层需要check的对象的个数，注意每层需要清零！！
checklist_tempcount = [0 for i in range(scl * 10)]   # 清零

# 排列组合形成checklist
slot = ['.'] * scl * 10      # 形成组合并传入checklist，排序+查重，形成一个组合后清空!!!!!!
slot_len = 0            # 该组合slot的长度，形成一个组合后清零!!!!!!!!
Fcurrlayer = 0          # 目前的layer!!!!!

while Flist_num[Fcurrlayer] > 0:
    # 从flist中的Fcurrlayer层读入，开始排列组合
    for i in range(Flist_num[Fcurrlayer] - 1):
        for j in range(i + 1, Flist_num[Fcurrlayer]):  # 放入slot的对象为Flist[Fcurr][i]与Flist[Fcurr][j]
            wordlen = Fcurrlayer + 1
            for k in range(wordlen):
                slot[k] = Flist[Fcurrlayer][Flist_anchor[Fcurrlayer][i] + k]
                slot_len += 1
            for k in range(wordlen):
                if Flist[Fcurrlayer][Flist_anchor[Fcurrlayer][j] + k] not in slot:
                    slot[slot_len] = Flist[Fcurrlayer][Flist_anchor[Fcurrlayer][j] + k]
                    slot_len += 1

            flag = True
            for m in range(checklist_len):
                ctemplen = checklist_anhor[m + 1] - checklist_anhor[m]
                ctempword = ''
                for p in range(ctemplen):
                    ctempword = ctempword + checklist[checklist_anhor[m] + p]
                if ctemplen != slot_len:
                    continue
                tempsame = 0
                for n in range(slot_len):
                    if slot[n] in ctempword:
                        tempsame += 1
                if tempsame == slot_len:
                    flag = False
                    break

            if flag:
                for k in range(slot_len):
                    checklist[checklist_anhor[checklist_len] + k] = slot[k]
                checklist_anhor[checklist_len + 1] = checklist_anhor[checklist_len] + slot_len
                checklist_len += 1

            slot = ['.'] * scl * 10 # 形成组合并传入checklist，排序+查重，形成一个组合后清空!!!!!!
            slot_len = 0  # 该组合slot的长度，形成一个组合后清零!!!!!!!!

    # 对checklist中的每一个对象，在原数据集中查找，计数
    for i in range(checklist_len):
        for k in range(row_num - 1):
            flag = True
            for j in range(Fcurrlayer + 2):
                if checklist[checklist_anhor[i] + j] not in b[k]:
                    flag = flag & False
                    break
            if flag:
                checklist_tempcount[i] += 1

    # 将符合条件的对象写入Flist
    Fcurrlayer += 1  # Fcurr = 1
    for i in range(checklist_len):
        if checklist_tempcount[i] >= sop:
            ctemplen = checklist_anhor[i + 1] - checklist_anhor[i]
            for j in range(Fcurrlayer + 1):
                Flist[Fcurrlayer][Flist_anchor[Fcurrlayer][Flist_num[Fcurrlayer]] + j] = checklist[
                    checklist_anhor[i] + j]
            count[Fcurrlayer][Flist_num[Fcurrlayer]] = checklist_tempcount[i]
            Flist_anchor[Fcurrlayer][Flist_num[Fcurrlayer] + 1] = Flist_anchor[Fcurrlayer][
                                                                      Flist_num[Fcurrlayer]] + ctemplen
            Flist_num[Fcurrlayer] += 1

    checklist = ['.'] * scl * 10 # 需要查找的对象，组合对象存放处，每层结束要初始化！！
    checklist_anhor = [0 for i in range(scl * 10)]  # 清零
    checklist_len = 0  # 该层需要check的对象的个数，注意每层需要清零！！
    checklist_tempcount = [0 for i in range(scl * 10)]  # 清零


# 排序输出
# flist 各对象内部排序 + 统计频次
layer = 0
reFlist = [['.' for i in range(scl)]for i in range(scl)]        # 存放每个对象排完序的flist

while Flist_num[layer] != 0:
    obnum = Flist_num[layer]
    for i in range(obnum):
        reFlist[layer][i] = sorted(Flist[layer][Flist_anchor[layer][i]:Flist_anchor[layer][i+1]])
    layer += 1

# Q1 顺序输出
casenum = 0     # 有多少种可能的频次
outputlistcount = [0 for i in range(scl)]      # 存放每个频次数下有多少个对象
outputlist = [['.' for i in range(scl)]for i in range(scl)]        # 存放准备输出的内容
caselist = ['.' for i in range(scl)]      # 存放出现过的频次数从大到小
outputorder = ['.' for i in range(scl)]

maxcount = max(max(count))

for j in range(maxcount, 0, -1):
    flag = False
    for i in range(layer):
        for k in range(Flist_num[i]):
            if count[i][k] == j:
                flag = True
                outputlist[casenum][outputlistcount[casenum]] = reFlist[i][k]
                outputlistcount[casenum] += 1
    if flag:
        caselist[casenum] = str(j)
        casenum += 1

for i in range(casenum):
    outputorder[i] = sorted(outputlist[i][0:outputlistcount[i]])

for i in range(casenum):
    for j in range(outputlistcount[i]):
        print(caselist[i] + ' [', end='')
        for k in range(len(outputorder[i][j])):
            print(outputorder[i][j][k], end='')
            if k < len(outputorder[i][j]) - 1:
                print(' ', end='')
        print(']')

print()

# Q2

q2flag = False

q2list = ['.' for i in range(scl)]
q2listcount = [0 for i in range(scl)]
q2listnum = 0

# 顶层最长的肯定是
maxlen = 0
for i in range(Flist_num[Fcurrlayer-1]):
    if len(reFlist[Fcurrlayer-1][i]) > maxlen:
        maxlen = len(reFlist[Fcurrlayer-1][i])
        q2list[q2listnum] = reFlist[Fcurrlayer-1][i]
        q2listcount[q2listnum] = count[Fcurrlayer-1][i]
q2listnum += 1

for i in range(Fcurrlayer-1, -1, -1):
    for j in range(Flist_num[i]):
        pflag = True
        for p in range(q2listnum):
            flaglen = 0
            for k in range(len(reFlist[i][j])):
                if reFlist[i][j][k] in q2list[p]:
                    flaglen += 1
                else:
                    break
            if flaglen == len(reFlist[i][j]):
                if count[i][j] <= q2listcount[p]:
                    pflag = False
                    break
        if pflag:
            q2list[q2listnum] = reFlist[i][j]
            q2listcount[q2listnum] = count[i][j]
            q2listnum += 1

#q2flagmap = [[0 for i in range(scl)]for i in range(scl)]


for i in range(casenum):
    for j in range(outputlistcount[i]):
        if outputorder[i][j] in q2list:
            print(caselist[i] + ' [', end='')
            for k in range(len(outputorder[i][j])):
                print(outputorder[i][j][k], end='')
                if k < len(outputorder[i][j]) - 1:
                    print(' ', end='')
            print(']')

print()

# Q3-------------------------------------------------------

q2flag = False

q2list = ['.' for i in range(scl)]
q2listcount = [0 for i in range(scl)]
q2listnum = 0

# 顶层最长的肯定是
maxlen = 0
for i in range(Flist_num[Fcurrlayer-1]):
    if len(reFlist[Fcurrlayer-1][i]) > maxlen:
        maxlen = len(reFlist[Fcurrlayer-1][i])
        q2list[q2listnum] = reFlist[Fcurrlayer-1][i]
        q2listcount[q2listnum] = count[Fcurrlayer-1][i]
q2listnum += 1

for i in range(Fcurrlayer-1, -1, -1):
    for j in range(Flist_num[i]):
        pflag = True
        for p in range(q2listnum):
            flaglen = 0
            for k in range(len(reFlist[i][j])):
                if reFlist[i][j][k] in q2list[p]:
                    flaglen += 1
                else:
                    break
            if flaglen == len(reFlist[i][j]):
                pflag = False
                break
        if pflag:
            q2list[q2listnum] = reFlist[i][j]
            q2listcount[q2listnum] = count[i][j]
            q2listnum += 1

#q2flagmap = [[0 for i in range(scl)]for i in range(scl)]


for i in range(casenum):
    for j in range(outputlistcount[i]):
        if outputorder[i][j] in q2list:
            print(caselist[i] + ' [', end='')
            for k in range(len(outputorder[i][j])):
                print(outputorder[i][j][k], end='')
                if k < len(outputorder[i][j]) - 1:
                    print(' ', end='')
            print(']')

