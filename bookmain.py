import math
import sqlite3
import string
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

def username_creator(usernames, uname):
    if not 3 < len(uname) < 21:
        print('Username length must be between 4-21 characters long.')
        return username_creator(usernames,input('Username :'))
    for char in uname:
        if char in ['!', '^', '+', '%', '&', '/', '(', ')', '=', '?', '*', ',', ';', ':']:
            print('Username cannot contain punctuations!("_-" is allowed!)')
            continue
    if uname in usernames:
        print('Username already exists!')
        return username_creator(usernames, input('Username :'))
    return uname



def password_creator(pw):
    containlist = [False, False, False, False]
    if not 7 < len(pw) < 21:
        print('Password must be 8-20 characters long!')
        return password_creator(input('Password: '))

    for char in pw:
        if char in string.ascii_uppercase:
            containlist[0] = True
        if char in string.ascii_lowercase:
            containlist[1] = True
        if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            containlist[2] = True
        if char in ['!', '^', '+', '%', '&', '/', '(', ')', '=', '?', '*', ',', ';', ':', '_', '-', '.']:
            containlist[3] = True
    if all(containlist):
        return pw
    else:
        print('Your password must contain an uppercase and a lowercase letter, number and a punctuation.')
        return password_creator(input('Password: '))


def create_user(datas):
    con = sqlite3.connect('bookdbase.db')
    cursor = con.cursor()
    cursor.execute(
        f"insert into logindata VALUES (\"{len(datas) + 1}\",\"{username_creator([i[1] for i in datas], input('Username:'))}\",\"{password_creator(input('Password:'))}\")")
    con.commit()
    cursor.execute(
        f'CREATE TABLE records_{(len(datas) + 1)} (id INT,Name TEXT, Kind TEXT, Author TEXT,IsFiction INT, Page INT, Rating FLOAT,Note TEXT)')
    con.close()
    login_user()


def login_user():
    uname = str(input('Username: '))
    pw = str(input('Password: '))
    con = sqlite3.connect('bookdbase.db')
    cursor = con.cursor()
    cursor.execute('Select * from logindata')
    datas = cursor.fetchall()
    for data in datas:
        if uname == data[1]:
            if pw == data[2]:
                print('Success! Logging in...')
                menu(data[0], data[1], 'get_op')
                break
    if input('No records found with entered credintals.Enter q to quit, press any key but q to get redirected to main menu.').lower() == 'q': exit(0)
    else: entrance()


def entrance():
    con = sqlite3.connect('bookdbase.db')
    cursor = con.cursor()
    cursor.execute('Select * from logindata')
    datas = cursor.fetchall()
    con.close()
    while 1:
        operation = str(input('Welcome to Book app... enter || L to log in - R to register || ')).lower()
        if operation == 'l':
            login_user()
        elif operation == 'r':
            create_user(datas)
        elif operation == 'debug':
            menu(2, 'Print', 'get_op')
        else:
            print(f'Unsupported command: {operation}')
            continue
        break


def get_daytime(h):
    return 'Morning' if 5 < h < 12 else 'Afternoon' if 12 <= h < 17 else 'Evening' if 17 <= h < 19 else 'Night'

def menu(id, name, status):
    if status == 'get_op':
        menu(id, name, input(f'''Good {get_daytime(int(datetime.now().strftime('%H')))}, {name}\n-----Please choose an operation below:\n
            -------------------------
            | - Add Book Record     |
            | - Delete Book Record  |
            | - See your records    |
            | - Check your insights |
            | - See global insights |
            | - Get recommendations |
            | - type commands to    |
            |   see commands!       |
            -------------------------
            Type Here: ''').lower())
    elif status == 'add': add_record(id)
    elif status == 'del': del_record(id,name,input('Enter the name of the book that you wish to be deleted: '))
    elif status == 'see': see_record(id)
    elif status == 'my insights': my_insights(id)
    elif status == 'global insights': insights()
    elif status == 'get recs': recsystem(id)
    elif status == 'commands': print('*************************************************************************'
                                     '\n| add | del | see | my insights | global insights | get recs | commands |'
                                     '\n*************************************************************************')
    elif status == 'exit':
        print(f'See you again, {name}')
        exit(0)
    else: print(f'unsupported command: |{status}|')
    menu(id, name, 'get_op')


def add_record(id):
    con = sqlite3.connect('bookdbase.db')
    cursor = con.cursor()
    while 1:
        kind = input('Kind of your book(e.g. Politics, History):').lower()
        if len(kind) == 0:
            print('Please enter kind again!')
            continue
        if kind not in ['adventure', 'classics', 'crime', 'fairy tales', 'fables',
                             'fantasy', 'historical fict.', 'horror', 'humour and satire', 'literary fiction',
                             'mystery', 'poetry', 'plays', 'romance', 'science fiction', 'short stories',
                             'thrillers', 'war', "women’s fiction",
                        'autobiography', 'biography', 'essays', 'history', 'politics',
                        'non-fiction novel', 'self-help']:
            print('This is not a valid kind.Please try again!')
            continue
        break

    def get_author(a):
        return a if  0 < len(a) < 17 else get_author(input("Author(max 18 chars long): "))
    def get_bookname(name):
        if 35 > len(name) > 0:
            return name
        else:
            get_bookname(input('Book Name(0-35 chars long): '))

    def get_fiction(kind):
        return 1 if kind in ['adventure', 'classics', 'crime', 'fairy tales', 'fables',
                             'fantasy', 'historical fict.', 'horror', 'humour and satire', 'literary fiction',
                             'mystery', 'poetry', 'plays', 'romance', 'science fiction', 'short stories',
                             'thrillers', 'war', "women’s fiction"] else 0

    def get_page(p):
        while 1:
            try:
                return int(p) if 6 > len(p) > 0 else get_page(input('0 to  6 chars available.\nPage Again:'))
            except:
                print('Only use numbers!')

    def get_rating(r):
        try: r = int(r)
        except: get_rating(input('Please only use integers!'))
        if 0 <= r <= 100:
            return r
        else:
            get_page(input('Rate the book from 0 to 100. Both limits are included: '))


    try:
        cursor.execute(
            f"insert into records_{id} VALUES(?,?,?,?,?,?,?,?)", (id,get_bookname(input('Book Name: ')), kind,get_author(input('Author(max 18 chars long): ')),get_fiction(kind),
                                                            get_page(input('Total pages (use integers): ')), get_rating(
                int(input('Rate the book over 100. Please only use numbers.')))/10,input('Add some notes about book(Leave blank if you wish): : ')))
        con.commit()
        print('Book successfully added!')

        con.close()
    except Exception as e:
        print(f'Error occurred while writing the data. Restart the app and try again!\nError is: {e}')


def del_record(id,name,bookname):
    with sqlite3.connect('bookdbase.db') as con:
        cursor = con.cursor()
        cursor.execute(f'Select * from records_{id}')
        if bookname not in [r[0] for r in cursor.fetchall()]:
            print(
                'This is not a valid bookname.Be aware of capitals and  miss-used spaces.Check your records below and try again!')
            see_record(id)
            del_record(id,name,input('Enter the name of the book that you wish to be deleted: '))
        elif bookname.lower() == 'exit':
            menu(id, name, 'get_op')
        else:
            cursor.execute(f"delete from records_{id} WHERE Name=? ", (bookname,))
            con.commit()
            print(f'--\nBook {bookname} , successfully deleted from your records!\n--')
    con.close()

def see_record(id):
    def print_data(totlen, data, i):
        if i >= 3: i-=1
        if int(34 / i) % 2 == 0:
            if totlen % 2 != 0:
                totlen += 1
                data += ' '
        else:
            if totlen % 2 == 0:
                totlen += 1
                data += ' '
        return ' ' * math.floor(((34 / i) - totlen) / 2) + data + ' ' * math.ceil(((34 / i) - totlen) / 2)

    con = sqlite3.connect('bookdbase.db')
    cursor = con.cursor()
    cursor.execute(f"Select * from records_{id}")
    print("""
------------------------------------------------------------------------------------------------------------
|           Name of Book           ||    Book Kind    ||      Author     || Is Fiction ||  Pages  || Score |""")
    for row in cursor.fetchall():
        for i, data in enumerate(row):
            if i == 0 or i == 7: continue
            print(f'|{print_data(len(str(data)), str(data), i)}|', end='')
        print()
    print('------------------------------------------------------------------------------------------------------------')

    con.close()

def create_df(is_global=False,id=0):
    with sqlite3.connect('bookdbase.db') as con:
        cursor = con.cursor()
        if is_global:
            cursor.execute('Select * from logindata')
            records = []
            for i in range(1, len(cursor.fetchall()) + 1):
                cursor.execute(f'Select * from records_{i}')
                for row in cursor.fetchall():
                    records.append(row)

        else:
            cursor.execute(f"Select * from records_{id}")
            records = cursor.fetchall()
    con.close()
    return pd.DataFrame({'id': [r[0] for r in records], 'Book Names': [r[1] for r in records],
                       'Kinds': [r[2] for r in records], 'Authors': [r[3] for r in records],
                       'Is Fiction': [r[4] for r in records],
                       'Pages': [r[5] for r in records],
                       'Ratings': [r[6] for r in records]})
def my_insights(id):
    df = create_df(id=id)
    if len(df) > 0:

        print(f'You read {sum(df["Pages"])} pages total.\n------------------')
        print(f'You rated your books in average of: {round(sum(df["Ratings"]) / len(df),3)}\n--------------')
        if sum(df['Is Fiction']) / len(df) >= 0.5:
            print('You are into fiction books more than non-fictions.\n-----')
        else:
            print("You're a realistic person.You read non-fiction books more than fictions.\n---------")
        print(f'You most read the books of {df["Authors"].mode().iloc[0]}! What an author to explore.')

    else:
        print('You have no records to get an insight.Type add to add a book!')

def get_uname(id):
    with sqlite3.connect('bookdbase.db') as con:
        cursor = con.cursor()
        cursor.execute('Select * from logindata where id=?',(int(id),))
        uname = cursor.fetchall()[0][1]
    con.close()
    return uname


def insights():
    df = create_df(is_global=True) #create df
    if sum(df['Is Fiction'])/len(df['Is Fiction']) >= 0.5: print('People prefers fiction books over realistic books.')
    else: print('People loves realistic books more than fictions.')

    print(f'--\nPeople read total of {sum(df["Pages"])} pages. Amazing!\n--\nAverage page per book is '
          f'{round(sum(df["Pages"])/len(df["Pages"]),2)}!')

    if len(df['Authors'].mode()) == len(df['Authors']): print("---\nAll authors has read equally!")
    else: print(f'---\nMost read author is {df["Authors"].mode().iloc[0]}')

    if len(df['Book Names'].mode()) == len(df['Book Names']): print('---\nAll books has read equally!')
    else: print(f'---\nMost read books by our community is {df["Book Names"].mode().iloc[0]}')

    print(f"---\nMost books read by bookworm user {get_uname(df.groupby('id')['Book Names'].count().index[0])} !")
    author_grouped = df.groupby('Authors').agg('mean').reset_index()
    print(f'{author_grouped[author_grouped["Ratings"]==author_grouped["Ratings"].max()].iloc[0]["Authors"]} holds the'
          f' crown for maximum avg rating by author!')

    plt.scatter(df['Book Names'],df['Pages'])
    plt.xlabel('Book Names')
    plt.ylabel('Pages Count')
    plt.title('Page distribution by book')
    plt.show()

    print('Although we keep improving the insights, we still need new recommendations to display to our users.Please '
          ' send us a feedback!')

def calc_recs(namelist,rec_df):
    userdict = {}
    for name in namelist:
        namedict = get_recs(name,rec_df)
        if not namedict: continue
        for key in namedict.keys():
            if key in namelist:
                continue
            if key not in userdict.keys():
                userdict[key] = [namedict[key] * 10]
            else:
                userdict[key].append(namedict[key] * 10)
    for key in userdict.keys():
        userdict[key] = sum(userdict[key]) / len(userdict[key]) * 10
    return userdict
def get_recs(name,rec_df):
    try: return dict(rec_df.corrwith(rec_df[name]).sort_values(ascending=False)[1:6])
    except: return False


def recsystem(id):
    df =create_df(is_global=True)
    rec_df = df.pivot_table(index='id', values='Ratings', columns='Book Names')
    ratings = pd.DataFrame(df.groupby('Book Names')['Ratings'].mean())
    ratings['num of ratings'] = df.groupby('Book Names')['Ratings'].count()
    ratings.reset_index(inplace=True)
    with sqlite3.connect('bookdbase.db') as con:
        cursor = con.cursor()
        cursor.execute(f'Select Name from records_{id}')
        booklist = cursor.fetchall()
        if len(booklist) == len(rec_df.columns):
            print('You have read all books in our system. wow!')
        elif len(booklist) < 1:
            print("We seem that you haven't added any book to your records.Here are some reccomendations for you to begin with!\n"
                  "| TOP 8 Recommendations based on what people liked |\n|                        --                        |")
            for i, name in enumerate(all_calc(rec_df, len(rec_df) / 48,ratings).keys()):
                print(f'|{i + 1}| {name}{(47 - len(name)) * " "}|\n----------------------------------------------------')

        else:
            print(
                '-----------------------------------------------\n| TOP 5 Recommendations based on your readings |\n|                    ----                      |')
            for i, name in enumerate(pd.Series(
                    calc_recs([tup[0] for tup in booklist], rec_df)).sort_values(
                ascending=False)[:5].keys()):
                if not name: continue
                print(f'|{i + 1}| {name}{(43 - len(name)) * " "}|\n-----------------------------------------------')
    con.close()

def all_calc(rec_df,lencol,ratings):
    for col in rec_df.columns:
        if ratings[ratings['Book Names']==col]['num of ratings'].iloc[0]< lencol:
            rec_df = rec_df.drop(col,axis=1)
    return dict(rec_df.agg('mean').sort_values(ascending=False)[1:8])
entrance()



