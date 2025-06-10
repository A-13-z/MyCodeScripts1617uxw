text = "I was lonely that it was difficult to even f@thom all the trouble $he went through*. Alas!!!"
hash = {'shift':0}
special_hash = {'~':'`','!':'1', '@':'2','#':'3','$':'4','%':'5','^':'6', '&':'7','*':'8','(':'9',')':'0','_':'-','+':'=','{':'[', '}':']', '|':"\\",':':';','\'':'"','<':',','>':'.','?':'/'}
for i in text:
    if i.islower() and i != ' ':
        if i in hash.keys():
            hash[i] += 1
        else:
            hash[i] = 1
    elif i.isupper() and i != ' ':
        if i in hash.keys():
            hash[i.lower()] += 1
        else:
            hash[i.lower()] = 1
        hash['shift'] += 1
    elif i.isnumeric() and i != ' ':
        if i in hash.keys():
            hash[i] += 1
        else:
            hash[i] = 1
    elif i.isalnum() == False and i != ' ':
        if i in special_hash.keys() and special_hash[i] in hash.keys():
            hash[special_hash[i]] += 1
            hash['shift'] += 1
        elif i in special_hash.keys() and special_hash[i] not in hash.keys():
            hash[special_hash[i]] = 1
            hash['shift'] += 1
        else:
            if i is hash.keys():
                hash[i] += 1
            else:
                hash[i] = 1

print(hash)