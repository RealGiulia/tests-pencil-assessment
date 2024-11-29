# Pencil Handler Automation
This project is designed to automate the process of interacting with the Pencil App website using Selenium WebDriver. The script logs into the website, performs various actions like validating components on the page, manipulating a canvas, and ensuring that all functionalities work correctly.

The technologies used are Python, Selenium and unittest library.

## Prerequisites
 - Python: Make sure you have Python installed (Python 3.10+ is recommended).

 - Virtual Environment: Create a virtual environment to manage dependencies.

## Setup Instructions
### 1. Create a Virtual Environment

``` bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate` 
```
### 2. Install Dependencies

Install the required dependencies using the requirements.txt file:

``` bash
    pip install -r requirements.txt
```

### 3. Configure config.ini

Create and set up the config.ini file within the folder "data", inserting  your Pencil website's credentials  and log folder path. The file should look like this:

```
    [INPUT]
    EMAIL = your_email@example.com
    SECRET = your_password
    LOG_FOLDER = path_to_log_folder
```

Replace your_email@example.com, your_password, and path_to_log_folder with your actual email, password, and desired log folder path.


## Components of this project:

    - This project consists in 5 python files, a requirements.txt file and a config.ini. Below, you will find more about the role of each file:

| File             | Role                                                                 |
|------------------|----------------------------------------------------------------------|
| `logger.py`      | Handles logging of errors and information throughout the script.     |
| `tester.py`      | Contains the test cases to verify the functionality of `PencilHandler`. |
| `user_input.py`  | Manages user input and configuration settings for the script.        |
| `web_handler.py` | Main script that performs the automation tasks on the Pencil website.|
| `bonus_tester.py`| Contains the test cases for the `bonus_assignment` function.         |





## Running the Automation Script

The main script to run the automation is web_handler.py. This script handles:

Login: Logs into the Pencil website using provided credentials.

Check Load Time: Verifies that the page loads within the specified time.

Validate Home Format: Validates various elements on the home page such as space title, navigation options, 'Create Space' button, and profile picture.

Enter First Space: Enters the first listed space.

Manipulate Canvas: Draws a vertical line on the canvas, moves it, and inserts text.

Logout: Logs out from the website and verifies redirection to the login page.

## How to run the tests scripts:

- The file responsible to execute the tests is **tester.py**. To execute tests, run:

```bash
python -m tester.py
```

## About the Logging:
Logs are generated in the folder specified in the config.ini file. This helps in tracking the errors performed by the script and identifying any issues that occur.

# ----------------------------- Bonus assignment -----------------------------------------

 - Bonus Assignment: Creates a new space, adds a text box, types text, italicizes it, and confirms the changes.

 - The steps tested are: Login into webpage, create a new Space and manipulate canvas to generate a text box,
 insert the word "test", select "Italicize" option, and setup textbox clicking outside it.

 - A test file was created to test the functionalities of the bonus assessment. You can find the tests at file 
 **bonus_tester.py**

 - A function named *_bonus_assignment_* to execute the steps indicated at bonus assessment was implemented at _web_handler.py_ file.