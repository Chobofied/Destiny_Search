#https://realpython.com/python-sql-libraries/#creating-tables


import SQL_DB
import sqlite3
from sqlite3 import Error

class sqllite_db():

  #Establishes a connection to the SQLite DB
  def __init__(self,path):
    self.connection = None
    try:
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
  
  # Posts data to the Database
  def execute_query(self, query):
    try:
        self.cursor.execute(query)
        self.connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

  # Reads (Fetches) Data from the database
  def execute_read_query(self, query):
    result = None
    try:
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")



def example_routine():
  '''
  Example Routine that creates an SQLlite Database, 
  posts, reads, appends, deletes data with user inputs allowed
  
  Call from Shell Command below
  python
  from sqllite_create import example_routine
  example_routine
  '''
 
  path="C://Users//Taylo//OneDrive//Python//Functions//SQL//SQLLite//sqllite_test.db"

  #Creates an instance of the SQLlite Database
  test_sql=sqllite_db(path)

  #Creates lists of the Tables and Data to added to the SQLlite Database
  Tables=(SQL_DB.Create.create_users_table,
          SQL_DB.Create.create_posts_table,
          SQL_DB.Create.create_comments_table,
          SQL_DB.Create.create_likes_table)

  Tables_Data=(SQL_DB.Create.create_users,
              SQL_DB.Create.create_posts,
              SQL_DB.Create.create_comments,
              SQL_DB.Create.create_likes)

  #Creates the Tables and fills them with data
  for Table in Tables:
    test_sql.execute_query(Table)

  for Table_Data in Tables_Data:
    test_sql.execute_query(Table_Data)


  #Reads Specific Data from the Database and printes them
  results=test_sql.execute_read_query(SQL_DB.Select.select_users_posts)

  for result in results:
        print(result)


  #Inserts Records Into Table (User)
  User_Append = """
  INSERT INTO
    users (name, age, gender, nationality)
  VALUES
    ('Taylor', 30, 'male', 'USA');
  """

  test_sql.execute_query(User_Append)
  #test_sql.execute_query(SQL_DB.Create.create_users_table)


  #User Input Data, SQL injection protection

  # See https://docs.python.org/3/library/sqlite3.html
  # Set up for users to input data

  The_Name='RealSlimShady'
  test_sql.cursor.execute("INSERT INTO users (name, age, gender, nationality) VALUES (?,?,?,?)",(The_Name, 21, "female", "Canada"))
  test_sql.connection.commit()

  #Delete Example
  delete_comment = "DELETE FROM users WHERE id = 5"
  test_sql.execute_query(delete_comment)

  delete_comment = "DELETE FROM users WHERE name = 'Taylor'"
  test_sql.execute_query(delete_comment)

  #User Delete Example

  Delete_Name='Brigitte'
  test_sql.cursor.execute("DELETE FROM users WHERE name = (?)",(Delete_Name,))
  test_sql.connection.commit()


if __name__ == '__main__':

    example_routine()
    








 