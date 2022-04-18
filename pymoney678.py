import sys
'''
print("Check point 5")
balance=input("How much money do you have? ")
balance=int(balance)
txn=input("Add some expense or income records with description and amount: \n\
desc1 amt1, desc2 amt2, desc3 amt3, ...\n")
txn_amt=txn.split(', ') #txn_amt now is list of str
txn_list=[]
for i in range(0,len(txn_amt)):
    #txn_amt[i].strip()
    txn_amt[i]=txn_amt[i].split(' ')
    txn_list.append((txn_amt[i][0],txn_amt[i][1]))

print("Here's your expense and income records:")
for i in range(0, len(txn_list)):
    print(txn_list[i][0], txn_list[i][1])


money_list=[int(txn_list[i][1]) for i in range(0, len(txn_list))]
balance=balance+sum(money_list)
print(f"Now you have {balance} dollars.")
print('-'*30)
'''
op=''
balance_=0
txn_list_=[]

def initialize(balance, txn_list):
    ''' int balance_, list 
    return (balance, txn_list)'''
    mode=1
    try:
        with open('records.txt', 'r') as fin:
            content=fin.readlines()
            try:
                #print(len(content))
                if(len(content)<=0):
                    raise AssertionError
            except AssertionError:
                print("No content in records.txt")
                mode=0
            try:
                balance_=int(content[0])
            except ValueError as err:           
                sys.stderr.write(str(err)+'\n')
                print("Invalid value for initial balance.\nDeleting the contents.")
                mode=0
            else:
                for i in range(1, len(content)):
                    content[i]=content[i].split(' ')
                    try:
                        content[i][1]=int(content[i][1])
                    except IndexError as err:
                        sys.stderr.write(str(err)+'\n')
                        print("Invalid format in records.txt. Deleting the contents.")
                        mode =0
                        break
                    except ValueError as err:           
                        sys.stderr.write(str(err)+'\n')
                        print("Invalid value for money.\nFail to add a record.")
                        mode=0
                    
                    else:
                        txn_list.append(content[i])
                        balance_=balance_+content[i][1]

            if(mode ==1):
                print("Welcome back!")
    except FileNotFoundError:
        mode=0

    finally:
        if(mode==0):
            balance_=input("How much money do you have? ")
            try:
                balance_=int(balance_)
            except ValueError as err:           
                print("Invalid value for money. Set to 0 by default.")
                balance_=0
    return (balance, txn_list)

def add(txn_list):
    ''' list txn_list; return: list'''
    success=0
    while(success==0):
        try:
            txn_list.append(input("Add an expense or income record with description and amount:\n"))
        except EOFError as err:
            sys.stderr.write(str(err)+'\n')
            print("Invalid input, try again!")
        except KeyboardInterrupt as err:
            sys.stderr.write(str(err)+'\n')
            print("Invalid input, try again!")
        else:
            success=1

        txn_list[-1]=txn_list[-1].split(' ')
        try:
            txn_list[-1][1]=int(txn_list[-1][1])
        except ValueError as err:           
            sys.stderr.write(str(err)+'\n')
            print("Invalid value for money.\nFail to add a record.")
            txn_list.pop()
            success=0
        except IndexError as err:
            sys.stderr.write(str(err)+'\n')
            print("Invalid format.\nFail to add a record.")
            txn_list.pop()
            success=0


    return txn_list
    
def delete(txn_list):
    ''' arg: list; return list '''
    item_found=0
    amt_found=0
    success=0
    while(success==0):
        try:
            todel=input("Which record do you want to delete (item amt) ? ")
        except EOFError as err:
            sys.stderr.write(str(err)+'\n')
            print("Invalid input, try again!")
        except KeyboardInterrupt as err:
            sys.stderr.write(str(err)+'\n')
            print("Invalid input, try again!")
        else:
            success=1

    todel=todel.split(' ')
    try:
        todel[1]=int(todel[1])
    except IndexError as err:
        sys.stderr.write(str(err))
        print("Invalid format. Fail to delete a record.")
        success=0
    else:                
        for i in range(0, len(txn_list)):
            if(todel[0] == txn_list[i][0]):
                item_found=1
                if(todel[1]==txn_list[i][1]):
                    txn_list.pop(i)
                    amt_found=1
        try:
            if(item_found==0):
                raise NameError
        except NameError:
            print("Item not found!")
            success=0
        try:
            if(item_found==1 and amt_found==0):
                raise ValueError
        except ValueError:
            print("Value not match with item!")
            success=0
    return txn_list
    
def view(balance, txn_list):
    ''' int balance, list txn_list
    return: int balance'''
    for i in range(0, len(txn_list)):
        balance=balance+txn_list[i][1]
    print("Here's your expense and income records:")
    print("Description \t\t Amount")
    print("-"*30)
    for i  in range(0, len(txn_list)):
        print(f"{txn_list[i][0]}\t\t\t{txn_list[i][1]}")
    print("-"*30)
    print(f"Now you have {balance} dollars.")
    return balance

def save(balance, txn_list):
    '''int balance, list txn_list
    return void'''
    with open('records.txt','w') as fin:
        fin.write(f"{balance}\n")
        for i in range(0, len(txn_list)):
            fin.write(f"{txn_list[i][0]} {txn_list[i][1]}\n")
''' main '''

(balance_, txn_list_)=initialize(balance_, txn_list_)

while(op!='exit'):
    try:
        op=input("What do you want to do (add / view / delete / exit)? ")
    except EOFError as err:
        sys.stderr.write(str(err)+'\n')
        print("Invalid input, try again!")
    except KeyboardInterrupt as err:
        sys.stderr.write(str(err)+'\n')
        print("Invalid input, try again!")
    
    if(op=='add'):
        txn_list_=add(txn_list_)
    elif(op=='view'):
        balance_=view(balance_, txn_list_)
    elif(op=='delete'):
        txn_list_=delete(txn_list_)
    elif(op!='exit'):
        print("Invalid command. Try again.")

save(balance_, txn_list_)


