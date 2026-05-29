import sqlite3

# connect to sqlite3
connection = sqlite3.connect("student_batch_221.db")

# create cursor
cursor = connection.cursor()

# create table

table_info = """
CREATE TABLE students_information(ID VARCHAR(12), NAME VARCHAR(25), SECTION VARCHAR(5), DEPT VARCHAR(15), CGPA VARCHAR(5))

"""

# create table
cursor.execute(table_info)


# insert values into table
cursor.execute("""Insert Into students_information values('221-15-04','Naruto','61_G','CSE','3.50')""")
cursor.execute("""Insert Into students_information values('221-15-05','Sauske','61_A','CSE','3.96')""")
cursor.execute("""Insert Into students_information values('221-15-06','Sakura','61_G','SWE','3.70')""")
cursor.execute("""Insert Into students_information values('221-15-07','Minato','61_A','CSE','3.99')""")
cursor.execute("""Insert Into students_information values('221-15-08','Obito', '61_G','CSE','3.60')""")
cursor.execute("""Insert Into students_information values('221-15-09','Jiraiya','61_A','CSE','3.96')""")
cursor.execute("""Insert Into students_information values('221-15-10','Pain','61_B','SWE','3.80')""")
cursor.execute("""Insert Into students_information values('221-15-11','Itachi','61_G','CSE','4.00')""")
cursor.execute("""Insert Into students_information values('221-15-12','Orochimaru','61_A','CSE','3.95')""")
cursor.execute("""Insert Into students_information values('221-15-13','Kakashi','61_B','SWE','3.98')""")
cursor.execute("""Insert Into students_information values('221-15-14','Gaara','61_C','CSE','3.94')""")


# show data

data = cursor.execute("""Select * from students_information""")

# display data
print("The inserted records are: ")
for row in data:
    print(row)

connection.commit()
connection.close()