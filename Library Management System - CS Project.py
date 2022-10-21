import mysql.connector as sqltor

print('Hi! Welcome to the Library Management System','\n')

#Connecting to MySQL

print('To use the application, please provide the necessary information to connect to MySQL')
print('If the application ends abruptly, then either the password given is incorrect or the database does not exist')
print('Before using the application, please make sure that the following tables do not exist on your database: books, bookscopy, students')
print('If the program ends abruptly, either of these tables exist in your database. Delete the tables and then rerun the program') 
print('\n')
pass_word=input('Enter password for root user:')
database_name=input('Enter database to be used:')
mycon=sqltor.connect(host='localhost',user='root',passwd=pass_word,database=database_name)
if mycon.is_connected()==True:
    print('Connection to MySQL is successful!!')
print('\n')

#Creating tables in MySQL

print('Please wait till pre-requisite tables are made')

cursor=mycon.cursor()
create_table1="create table students ( AdmNo integer(4), Name varchar(20), BookNo integer(2), DueDate integer(2))"
cursor.execute(create_table1)
mycon.commit()

create_table2="create table books ( BookNo integer(2), BookName varchar(30))"
cursor.execute(create_table2)
mycon.commit()

create_table3="create table bookscopy ( BookNo integer(2), BookName varchar(30))"
cursor.execute(create_table3)
mycon.commit()

print('Tables made successfully!!')
print('You can now use the application')
print('\n')

#Functions to be used in the program

print('Please note the following commands to use the application:-') 
def instructions():
    print('Please note that all the commands are case sensitive')
    print('\n')
    print('To carry out a function, type the name of the function mentioned in double quotes(" ") in lowercase')
    print('To enter a new book, type "add"')
    print('To check the list of books available for issue in library, type "books"')
    print('To issue a book, type "enter"')
    print('To check the list of books issued, type "students"')
    print('For a new day, type "new"')
    print('To return a book issued, type "return"')
    print('To close the program, type "quit"')
    print('\n')

instructions()

books={}
books_copy={}
issue={} 
stu_name=[]
stu_adm_no=[]
book_due_date=[]

n=1
count=0

while n > 0:
    l1=list(issue.keys())
    l2=list(issue.values())
    dec=input('What do you want to do?')
    
#Set of instructions of how to run the program

    if dec == 'inst':
        print('Please note that all the commands are case sensitive')
        print('\n')
        print('To carry out a function, type the name of the function mentioned in double quotes(" ") in lowercase')
        print('To enter a new book, type "add"')
        print('To check the list of books available for issue in library, type "books"')
        print('To issue a book, type "enter"')
        print('To check the list of books issued, type "students"')
        print('For a new day, type "new"')
        print('To return a book issued, type "return"')
        print('To close the program, type "quit"')
        print('\n')

#Adding new books into the library database

    elif dec == 'add':
        print('Warning! Book number should be unique')
        book_no=int(input('Enter book number:'))
        book_name=input('Enter book name:')

        if book_no in books_copy.keys():
            print('Error! Book number already exists')
            print('Aborting the sequence of adding new books! Please enter a valid input')
            print('\n')
            continue

        else :
            books[book_no]=book_name
            books_copy[book_no]=book_name
            books_add='insert into books values({},"{}")'.format(book_no,book_name)
            cursor.execute(books_add)
            mycon.commit()
            books_copy_add='insert into bookscopy values({},"{}")'.format(book_no,book_name)
            cursor.execute(books_copy_add)
            mycon.commit()
            
            print('Book added to database')
            print('\n')

#List of available books for issue in the library

    elif dec =='books':
        print('The list of books available to issue is as follows',)
        print('Column 1 represents book number, column 2 represents book name')
        cursor.execute('select * from books order by BookNo')
        data1=cursor.fetchall()
        for row1 in data1:
            print(row1)
        print('\n')
        print('The total list of books in the library is as follows')
        print('Column 1 represents book number, column 2 represents book name.')
        cursor.execute('select *from bookscopy')
        data2=cursor.fetchall()
        for row2 in data2:
            print(row2)
        print('\n')

#Issuing an available book

    elif dec == 'enter':
        adm_no=int(input('Enter the admission number of student(Max length = 4):'))
        name=input("Enter student's name(Max length = 30):")
        select_book_no=int(input('Enter the book number:'))
        due_date=int(input('Enter number of days for which the book is issued(Max length = 2):'))

        if select_book_no not in books.keys():
            print('Book not found in library')
            print('Aborting sequence for issuing a book. Please enter a valid book number')
            print('\n')
            continue

        else :          
            issue[select_book_no]=books.get(select_book_no)
            del books[select_book_no]
            stu_name.append(name)
            stu_adm_no.append(adm_no)
            book_due_date.append(due_date)
            count+=1
            books_issue='insert into students values ({},"{}",{},{})'.format(adm_no,name,select_book_no,due_date)
            cursor.execute(books_issue)
            mycon.commit()
            books_issue2='delete from books where BookNo = {}'.format(select_book_no,)
            cursor.execute(books_issue2)
            mycon.commit()
            print('Book has been issued')
            print('\n')

#Viewing the books issued to students

    elif dec == 'students':
        print('List of books issued is as follows:')
        print('Column 1 represents Admission Number of student, Column 2 represents Name of student')
        print('Column 3 represents Book Number issued, Column 4 represents Due Date')
        cursor.execute('select * from students')
        data3=cursor.fetchall()
        for row3 in data3:
            print(row3)
        print('\n')

#Beginning a new day and checking books due for returning

    elif dec =='new':
        print('Welcome back')
        for date in range(len(book_due_date)):
            book_due_date[date]-=1
            if book_due_date[date]<=0:
                index=book_due_date.index(book_due_date[date])
                print('Submission of book number',l1[index],'titled',l2[index],'issued by',stu_name[index],'(adm no.',stu_adm_no[index],') is due')
        new_day='update students set DueDate = DueDate - 1'
        cursor.execute(new_day)
        mycon.commit()
        print('\n') 

#Returning a book

    elif dec == 'return':
        ret=int(input("Enter book number which is being returned:"))

        if ret not in l1:
            print('This book has not been issued')
            print('Aborting the sequence for returning of books. Enter a valid input')
            print('\n')

        elif ret in l1:         
            index2=l1.index(ret)
            stu_name.pop(index2)
            stu_adm_no.pop(index2)
            book_due_date.pop(index2)
            ele1=l1.pop(index2)
            ele2=l2.pop(index2)
            books[ele1]=ele2
            del issue[ret]
            ret_book='delete from students where BookNo={}'.format(ret,)
            cursor.execute(ret_book)
            mycon.commit()
            add_book='insert into books values ({},"{}")'.format(ret,ele2)
            cursor.execute(add_book)
            mycon.commit()
            print('Book has been returned')
            print('\n')
            count-=1
            print('Updated list of available books in libary is as follows')
            print('Column 1 represents book number. Column 2 represents book name.')
            print('\n')
            show_books='select * from books order by BookNo'
            cursor.execute(show_books)
            data4=cursor.fetchall()
            for row4 in data4:
                print(row4)
            print('\n')
            
#Quitting the program

    elif dec == 'quit':
        print('Do you really want to the program? :( ')
        ques=input('All your data will be lost! (y/n)')        
        if ques == 'y' :
            print('Thank you for using library management system :)')
            n-=1
        else:
            print('Welcome back :)')
            print('\n')
            print('Here is a recap of all functions')
            print('\n')
            instructions()
                
#Invalid input
    else:
        print('Please enter a valid command')
        instructions()
