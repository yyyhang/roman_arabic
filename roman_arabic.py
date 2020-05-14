import sys
'''
alp is the possible rule which is given by user, convert is the certain rule which is string. 
alpha is the certain rule which is dictionary
roman is the thing need to be converted
'''

command = input('How can I help you? ').split()
length = len(command)
cvert = 'MDCLXVI'

def no_repeat(alp):
    '''
    to check if the consequence the usr input can be a rule (whithout repeating)
    '''
    alp = list(alp)
    value = True
    for _ in alp:
        if alp.count(_) != 1:
            value = False
            break
    return value

def valid_input(roman,alp):
    '''
    To check if the thing need to be converted is valid or not
    (for question one and two)
    ''' 
    cnt = 0
    value = False
    if roman.isdigit():
        for digit in roman:    #To make sure there is no heading 0s
            if digit == '0':
                cnt += 1
            else:
                value = False
                break
        if cnt == 0:
            roman=int(roman)
            discard, maxum = arab (alp)
            if 0<roman<=maxum:    #To make sure the positive integer is less than maxum
                value = True
    elif roman.isalpha():   # To make sure all input in the convert
        for i in range(len(roman)):
            if roman[i] in alp:
                value = True
            else:
                value = False
                break
            if roman[i] in roman[slice(i+5,len(roman)+1)] or roman.count(roman[i]) > 4:
                #To make sure there is no wrong format like IIII or XXXIXIX
                value = False
                break
    return value

def possible_input(roman):
    '''
    to check whether the input can be changed
    '''
    value = False
    if roman.isalpha(): 
        for i in range(len(roman)):
            value = True
            if roman[i] in roman[slice(i+5,len(roman)+1)] or roman.count(roman[i]) > 4:
                value = False
                break
    return value


def arab(convert):
    '''
    To get special letter, like IV, IX, XL
    And get the biggest number this rule can represent
    '''
    mul = 1
    convert = convert[::-1]
    arab = {}
    temp = [1,4,5,9]
    k = 0
    limit = (len(convert)-1) * 2
    for i in range(limit + 1):
        if i > 0 and i % 4 == 0:
            mul = mul * 10
            k += 2
        number = temp[i%4] * mul
        if i % 4 == 0:
            arab[number] = convert[k]
        elif i % 4 == 1:
            arab[number] = convert[k] + convert[k+1]
        elif i % 4 == 2:
            arab[number] = convert[k+1]
        elif i % 4 == 3:
            arab[number] = convert[k] + convert[k+2]
    i += 1
    upper_bound = (temp[i % 4]) * mul - 1
    return arab,upper_bound

def roman_symbols(alp=cvert):
    '''
    To get what rule a consequence letters can represent, like {letter:value}
    '''
    # if alp.isalpha():
    alpha = {}
    temp = 1
    alp = alp[::-1]
    for i in range(len(alp)):
        if i == 0:
            alpha[alp[i]]=temp
        elif i % 2 == 0:
            temp = temp * 2
            alpha[alp[i]]=temp
        else:
            temp = temp * 5
            alpha[alp[i]]=temp
    return alpha
    #else:
        #return {}

def roman_digits(roman,alpha):
    '''
    To get value from Roman letter by a certain rule
    '''
    value=0
    for i in range(len(roman)-1):
        if alpha[roman[i]] < alpha[roman[i+1]]:
            value -= alpha[roman[i]]
        else:
            value += alpha[roman[i]]
    value += alpha[roman[-1]]
    return value

def check_roman(roman,alpha):
    '''
    Check if the letter input can be converted to value successfully by a certain convert rule (dic)
    '''
    roman = roman[::-1]
    pre_flag = 0
    value = 1
    old_flag = 0
    value2 = 0
    cnt = 1
    status = 0
    for i in roman:
        value1 = alpha[i]
        flag = len(str(value1))
        if status:
            if flag > old_flag:
                status = 0
            else:
                value = 0
                break
        if value1 == value2 and cnt <= 2 and flag >= pre_flag and str(value1)[0] != '5':
            cnt += 1
        elif value1 < value2 <= 10 * value1 and flag > pre_flag and str(value1)[0] != '5':
            status = 1
            cnt = 1
        elif value1 > value2 and flag >= pre_flag:
            cnt = 1
        else:
            value = 0
            break
        value2 = value1
        pre_flag = old_flag
        old_flag = flag
    return value

def digits_roman(roman,convert):
    '''
    Convert number to Roman Letter by a str (will be changed to dic whinin function)
    '''
    roman = int(roman)
    value=''
    digit_to_letter,maxum = arab(convert)
    key_value = sorted(list(digit_to_letter.keys()),reverse=True)
    for i in key_value:
        while roman >= i:
            roman = roman - i
            value = value + digit_to_letter[i]
    return value

def get_alp(roman):
    hold = ''
    for i in roman:
        if i not in hold:
            hold += i
    return hold

def first_input(roman,convert):
    value = 0
    result= valid_input(roman,convert)
    if result:
        if roman.isdigit():
            value = digits_roman(roman,convert)
        else:
            alpha = roman_symbols()
            if check_roman(roman,alpha):
                value = roman_digits(roman,alpha)
    return value

def second_input(roman,alp):
    value = 0
    if no_repeat(alp):
        result = valid_input(roman,alp)
        if result:
            convert = roman_symbols(alp)
            if roman.isalpha() and convert and check_roman(roman,convert):
                value = roman_digits(roman,convert)
            elif roman.isdigit() and convert:
                value = digits_roman(roman,alp)
    return value

def not_five(roman):
    '''
    To find all elements can not be 5,50,500...
    '''
    notFive = [i for i in roman if roman.count(i) > 1] # AA can not be 5
    for i in range(len(roman)-2):
        if roman[i+1] != roman[i] and roman[i+2] == roman[i]:    # ABA can not be 5
            notFive.append(roman[i])
            notFive.append(roman[i+1])
    return notFive

def get_list(alp):
    limit = len(alp) * 2
    listFive = [5*10**(i//2) for i in range(limit) if i % 2 == 0]
    listOne = [10**(i//2) for i in range(limit) if i % 2 == 0]
    return listOne, listFive

def get_final(pos_convert,roman):
    roman = roman[::-1]
    value = 0
    if check_roman(roman,pos_convert):
        value = roman_digits(roman,pos_convert)
    if value:
        reverse_dic = {value:key for key, value in pos_convert.items()} # get dic as value:keys 
        final_list = list_1 +list_5
        for i in final_list:
            if int(i) < max(reverse_dic) and (i not in reverse_dic):
                reverse_dic[i] = '_'
        reverse_list = sorted(reverse_dic.items(), key=lambda item:item[0],reverse=True)
        #Print(reverse_list)
        cor_cvr = ''.join([i[1] for i in reverse_list]) # to convert the keys in dic to string 
        final[value] = cor_cvr #add result to another dictionary
    return final

def check(value1,value2,pre_flag,flag,letter):
    value = 0
    if ((value1 < value2 and flag > pre_flag and str(value1)[0] != '5') or
        (value1 >= value2 and flag >= pre_flag)):
        value = 1
        pos_convert[letter] = value1
    return value

def induction(lat_letter,rest,pre_flag,flag,record,roman):
    letter = rest[0]
    rest = rest[slice(1,len(rest))]
    value = 0

    if letter in notFive:
        new_list = list_1.copy()
    else:
        new_list = sorted(list_1+list_5)   
    new_list = sorted(list(set(new_list)-set(record)))  # get pool

    if letter in pos_convert and str(pos_convert[letter])[0] == '5': # letter is 5
        return
    elif letter in pos_convert:    # if =, no need to loop 
        i = pos_convert[letter]
        new_flag = len(str(i))
        if check(i,pos_convert[lat_letter],pre_flag,new_flag,letter):
            if rest:
                new_pre_flag = flag
                induction(letter,rest,new_pre_flag,new_flag,record,roman)
            else:
                get_final(pos_convert,roman)
        return
    for i in [j for j in new_list if j <= 100 * pos_convert[lat_letter]]:
        new_flag = len(str(i))
        result = check(i,pos_convert[lat_letter],pre_flag,new_flag,letter)
        if result and not rest:
            get_final(pos_convert,roman)
            pos_convert.pop(letter)
            return #No need to loop for larger correct number if it is the last element
        elif result:
            record.append(i)
            new_pre_flag = flag
            induction(letter,rest,new_pre_flag,new_flag,record,roman)
            record.pop()
            pos_convert.pop(letter)
    return

def divid(roman):
    divid_hold =[]
    cnt = 0
    while len(roman) > 10 and cnt < len(roman):
        cnt += 1
        for i in range(5,len(roman)-3):
            if roman[i] not in roman[i+1:len(roman)] and roman[i] in roman[0:i]:
                emm = 1
                for k in roman[0:i]:
                    if k in roman[i+1:len(roman)]:
                        emm = 0
                        break
                if emm:
                    divid_hold.append(''.join([i for i in roman[0:i+1]]))
                    roman = roman[i+1:len(roman)]
                    break
            elif roman[i-5] == roman[i-4] and roman[i-5] not in roman[i-3:len(roman)]:
                divid_hold.append(''.join([i for i in roman[0:i-3]]))
                roman = roman[i-3:len(roman)]
                break
    divid_hold.append(roman)
    return divid_hold

def result(combination):
    first = combination.pop(0)
    pos = [first]
    for i in combination:
        a = '_' + i
        b = i
        j = 0
        lenth = len(pos)
        while j < lenth:
            pre = pos.pop(0)
            pos.append(pre+a)
            pos.append(pre+b)
            j += 1
    return pos

def minimum(pos,roman):
    last = {}
    display = last
    for i in pos:
        rule = roman_symbols(i)
        if check_roman(roman,rule):
            value = roman_digits(roman,rule)
            last[value] = i
    if last:
        mini = min(last.keys())
        display = [mini,last[mini]]
    return display

def third_input(roman,alp):
    record = []
    combination = []
    result = possible_input(roman) 
    if result:
        divid_hold = divid(roman)
        for roman in divid_hold:
            roman = roman[::-1]    #reverse input
            rest = roman
            pos_convert[roman[0]] = 1
            letter = roman[0]
            rest = rest[slice(1,len(rest))]
            if letter in notFive:
                new_list = list_1.copy()
            else:
                new_list = sorted(list_1+list_5)
            while pos_convert[letter] <= 10 and new_list:
                #pos_convert[roman[0]] = new_list[0]
                pre_flag = 0
                flag = len(str(new_list[0]))
                record.append(new_list.pop(0))
                if rest:
                    induction(roman[0],rest,pre_flag,flag,record,roman)
                else:
                    get_final(pos_convert, roman)
                record.pop()
                pos_convert.pop(letter)
                if new_list:
                    pos_convert[letter] = new_list[0]
                else:
                    pos_convert[letter] = 0
            if final:
                minim = min(final.keys())
                combination.append(final[minim])
                final.clear()
                pos_convert.clear()
            else:
                combination.clear()
                return
    return combination # like ['aaa','sed','rty'], witch for the min for each part
if len(command) < 3:
    print("I don't get what you want, sorry mate!")
elif not (command[0]=='Please' and command[1]== 'convert'):       #To check the form
    print("I don't get what you want, sorry mate!")
    sys.exit()
else:
    if length == 3:
        value = first_input(command[2],cvert)
        if value:
            print('Sure! It is',value)
        else:
            print("Hey, ask me something that's not impossible to do!")

    elif length == 4 and command[3] == 'minimally':
        Roman = command[2]
        final = {}
        pos_convert = {}
        alp = get_alp(Roman)
        list_1,list_5 = get_list(alp)
        notFive = not_five(Roman)
        combination = third_input(Roman,alp)
        if combination:
            pos = result(combination)
            display = minimum(pos,Roman)
        else:
            display = []
        if display:
            print('Sure! It is',display[0],'using',display[1])
        else:
            print("Hey, ask me something that's not impossible to do!")

    elif length == 5 and command[3] == 'using':
        value=second_input(command[2],command[4])
        if value:
            print('Sure! It is',value)
        else:
            print("Hey, ask me something that's not impossible to do!")

    else:
        print("I don't get what you want, sorry mate!")
        sys.exit()