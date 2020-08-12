import random
import sqlite3

myDB = sqlite3.connect('card.s3db')
cursor = myDB.cursor()
cursor.execute('create table if not exists card('
               'id   integer,'
               'number TEXT ,'
               'pin TEXT ,'
               'balance INTEGER)'
               )


class account:
    account_db = []

    def __init__(self, Balance):
        self.cardnumber = self.card()
        print("Your card has been created\nYour card number:")
        print(self.cardnumber)
        print("Your card PIN")
        self.PIN = self.createpin()
        self.Balance = Balance
        account.account_db.append(self)
        cursor.execute('SELECT id FROM card WHERE id=(SELECT max(id) FROM card);')
        id = cursor.fetchone()
        if id is None: newid = 1
        else:  newid = int(id[0]) + 1

        fucking_sql = [newid, int(self.cardnumber), self.PIN, self.Balance]
        cursor.execute('insert into card (id,number,pin,balance)'
                       'values(?,?,?,?)', fucking_sql)
        myDB.commit()

    def card(self):
        save = list(str(random.randint(400000000000000, 400000999999999)))
        first = save[:]
        last_digit = luhn(first)
        save.append(last_digit)
        s = [str(i) for i in save]
        res = int("".join(s))
        return res

    def createpin(self):
        a = random.randint(0, 9999)
        a = f'{a:04}'
        print(a)
        return int(a)


def check_card(card, sender):
    if int(sender) == int(card):
        print("“You can't transfer money to the same account!”")
        return 'samesies'
    db = syncdb()
    for row in db:
        if int(row[1]) == int(card):
            return int(row[0])
    card = list(card)
    last_digit = card.pop(len(card)-1)
    if int(last_digit) != int(luhn(card)):
        print("Probably you made mistake in the card number. Please try again!")
        return 'bad'
    else:
        print("Such a card does not exist.")
        return 'null'


def luhn(first):
    total = 0
    first.insert(0, 0)
    for i in range(len(first)):
        if i % 2 == 1:
            first[i] = int(first[i]) * 2
            if int(first[i]) > 9:
                first[i] -= 9

    for i in range(len(first)):
        total += int(first[i])
    del first[0]
    mod = total % 10
    last_digit = 10 - mod
    if last_digit == 10: last_digit = 0
    return last_digit
def changemoney(amount,id):
    db = syncdb()
    income = int(amount) + int(db[id - 1][3])
    fck_sql = [income, id]
    cursor.execute('update card set balance = ? where id = ?', fck_sql)
    myDB.commit()


def menu():
    print("Enter your card number:")
    x = input()
    print("Enter your PIN:")
    y = input()
    db = syncdb()
    for row in db:
        if int(row[1]) == int(x) and int(row[2]) == int(y):
            current_id = int(row[0])
            print("You have successfully logged in!")
            while True:
                db = syncdb()
                print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
                s1 = input()
                if s1 == '1':
                    print(db[current_id - 1][3])
                if s1 == '2':
                    print("Enter income:")
                    changemoney(input(),db[current_id-1][0])
                    print("Income was added!")
                if s1 == '3':
                    print("Enter card number:")
                    a = check_card(input(), row[1])
                    if a == 'bad':
                        continue
                    if a == 'null':
                        continue
                    if a == 'samesies':
                        continue
                    print("Enter how much money you want to transfer:")
                    money = int(input())
                    if money > int(db[current_id - 1][3]):
                        print("Not enough money!")
                        continue
                    changemoney(-money,current_id)
                    changemoney(money,a)
                    print("Success!")
                if s1 == '4':
                    sg = [current_id]
                    cursor.execute("delete from card where id = ?",sg)
                    myDB.commit()
                    print("The account has been closed!")
                    break
                if s1 == '5':
                    print("You have successfully logged out!")
                    break
                if s1 == '0':
                    print("Bye!")
                    exit()
    else:
        print("Wrong card number or PIN!")


def syncdb():
    cursor.execute('select * from card')
    db = cursor.fetchall()
    return db


while True:
    syncdb()
    print("1. Create an account\n2. Log into account\n0. Exit")
    s = input()
    if s == '1':
        a = account(0)
    if s == '2':
        menu()
    if s == '0':
        exit()
