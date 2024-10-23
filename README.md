# Boook Tracker App 
The project track the reading habits of the user and then give the user evaluation
of his habits on supposed time.
- What does it do?   
the user can add the book directly from 
the google book databse and then adding it to his list on the app. 
- What is the "new feature" which you have implemented that 
we haven't seen before?   
  - connecting to the public api.
  - using jason to read and write.
  - using the database.
  - authentication with jwt, http request and async and wait.
  - using boostrap.
## Prerequisites 
Did you add any additional modules that someone needs to 
install (for instance anything in Python that you `pip 
install-ed`)? 
- I wrote it in the requirements file in my code but to elaborate:
Flask>=2.3,<3.0
Flask-JWT-Extended>=4.4,<5.0
Flask-SQLAlchemy>=3.0,<4.0
Werkzeug>=2.3,<3.0
requests
Flask-Migrate 
python-dotenv
 
## Project Checklist 
- [x] It is available on GitHub. 
- [x] It uses the Flask web framework. 
- [x] It uses at least one module from the Python Standard 
Library other than the random module. 
  Please provide the name of the module you are using in your 
app. 
  - : 
- [x] It contains at least one class written by you that has 
both properties and methods. It uses `__init__()` to let the 
class initialize the object's attributes (note that  
`__init__()` doesn't count as a method). This includes 
instantiating the class and using the methods in your app. 
Please provide below the file name and the line number(s) of 
at least one example of a class definition in your code as 
well as the names of two properties and two methods. 
  - File name for the class definition: models.py
  - Line number(s) for the class definition: 11
  - Name of two properties: user_name, id
  - Name of two methods: set_password, check_password
  - File name and line numbers where the methods are used:app.py , 166, 142  
- [x] It makes use of JavaScript in the front end and uses the 
localStorage of the web browser. 
- [x] It uses modern JavaScript (for example, let and const 
rather than var). 
- [x] It makes use of the reading and writing to the same file 
feature. 
- [x] It contains conditional statements. Please provide below 
the file name and the line number(s) of at least one example of a conditional statement in your code. 
  - File name: login.js
  - Line number(s):24
- [x] It contains loops. Please provide below the file name 
and the line number(s) of at least 
  one example of a loop in your code. 
  - File name: book_list.html
  - Line number(s):  52
- [x] It lets the user enter a value in a text box at some 
point. This value is received and processed by your back end 
Python code. 
- [x] It doesn't generate any error message even if the user 
enters a wrong input. 
- [x] It is styled using your own CSS. 
- [x] The code follows the code and style conventions as 
introduced in the course, is fully documented using comments 
and doesn't contain unused or experimental code.  
  In particular, the code should not use `print()` or 
`console.log()` for any information the app user should see. 
Instead, all user feedback needs to be visible in the 
browser.   
- [x] All exercises have been completed as per the 
requirements and pushed to the respective GitHub repository. 
