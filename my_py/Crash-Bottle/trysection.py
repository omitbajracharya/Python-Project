with open('score.txt','r') as f:
    str1 = f.read()
    list1 = str1.split(',')
    print(list1)
    list2 = []
    for i in list1:
        list2.append(int(i))
# f = open("score.txt", "w")
# f.writelines(['10,','2,','3'])
# f.close()
score = 11
print(list2)
list2.append(score)
list2.sort()
list2.reverse()
print(list2)
# print(dir(list))
list2.pop(3)
print(list2)