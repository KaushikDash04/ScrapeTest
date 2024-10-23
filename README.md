# ScrapeTest

This Python script leverages web scraping and the Google Gemini Pro LLM (Large Language Model) to automatically attempt online tests. By integrating advanced scraping techniques with powerful AI, this tool aims to simplify the test-taking process.

**Disclaimer:** This project is for educational purposes only. Using it to cheat on real exams is unethical and may violate the terms of service of the testing platform.

## Features

- **Web Scraping**: Efficiently scrapes test questions and options from a specified target webpage using Selenium.
- **AI-Powered Answers**: Utilizes the Google Gemini Pro LLM to analyze questions and determine the most probable correct answers.
- **Automated Navigation**: Automates the entire process of selecting answers and submitting the test.
- **JSON Export**: Saves the extracted questions and options in a JSON file for further analysis or review.

## Requirements

- **Python 3.6+**
- **Google Chrome**: The script uses ChromeDriver for web automation.
- **Required Python Packages**: Install the necessary packages by running:
  ```bash
  pip install -r requirements.txt
  ```
- **Google Gemini Pro API Key**: Obtain an API key from Google to access the Gemini Pro model.

## Setup

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### 2. Create a Virtual Environment (Recommended)

It's recommended to use a virtual environment to isolate project dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Activate the environment
```

### 3. Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project's root directory and add the following lines, replacing the placeholders with your actual values:

```plaintext
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
TARGET_WEBPAGE="https://www.example.com/test-page"
```

### 5. Configure ChromeDriver

Download ChromeDriver from [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads) and ensure it is in your system's PATH or located in the project directory.

## Usage

### 1. Run the Script

Execute the script to start the automated test-taking process:

```bash
python main.py
```

### 2. Script Execution Details

- The script will open a Chrome browser window.
- It will navigate to the target webpage and fill in basic attendee information (customize the script as needed).
- It will scrape the questions and options, sending them to the Google Gemini Pro LLM for analysis.
- The LLM's responses will be used to select answers, and the script will automatically proceed through the test until submission.

## Web Scraping with Selenium

This project employs **Selenium**, a powerful tool for automating web browsers. Here’s how it contributes to the project's functionality:

### **What is Web Scraping?**

Web scraping is the process of automatically extracting information from websites. It involves making requests to web pages, retrieving HTML content, and parsing it to extract the desired data. In this project, web scraping is utilized to gather test questions and answer options from a designated online test platform.

### **Why Use Selenium?**

- **Browser Automation**: Selenium allows for the automation of browser actions like clicking buttons, filling out forms, and navigating through pages, which is essential for interacting with dynamic web applications.
- **Handling JavaScript**: Many modern web pages are dynamically generated using JavaScript. Selenium can execute JavaScript, making it capable of scraping content that traditional libraries like `BeautifulSoup` might miss.
- **Real User Simulation**: Selenium operates in a real browser environment, simulating human-like interactions, which helps in bypassing certain bot detection mechanisms used by websites.

### **Key Selenium Functions Used in the Project:**

- **`webdriver.Chrome()`**: Initializes a new Chrome browser instance.
- **`driver.get(webpage)`**: Navigates to the specified target webpage.
- **Element Selection**: Various methods (`find_element`, `find_elements`) are employed to locate HTML elements based on their attributes, such as IDs and class names.
- **Visibility Checks**: The script uses WebDriverWait and expected conditions (EC) to ensure elements are visible and ready for interaction, reducing the chances of encountering errors.
- **JavaScript Execution**: The script executes JavaScript commands to manipulate element styles and ensure they are visible when necessary.

## Test Cases

To ensure the script works correctly, you can create various test cases based on the structure of the questions on the target webpage. Some examples include:

### 1. Multiple Choice (Single Answer)

- Validate that the script can identify the question and all available options.
- Confirm it correctly parses the LLM's response to select the right answer.

### 2. True/False Questions

- Test if the script effectively handles binary questions where the options are "True" and "False."

### 3. Multiple Choice (Multiple Answers)

- Modify the script to handle scenarios where more than one answer choice can be correct.

### 4. Different Question Layouts

- Ensure the script can adapt to variations in how questions and options are structured on the target webpage.

### 5. Error Handling

- Validate the script's ability to manage scenarios where elements are not found or API requests fail.

## Important Notes

- **Ethical Use**: Remember that using this script to cheat on real exams is unethical and potentially illegal.
- **Website Changes**: Websites frequently update their structure. You might need to adjust the Selenium web scraping code in `main.py` if the target webpage changes.
- **Rate Limits**: Be mindful of rate limits when using the Google Gemini Pro API. Excessive requests in a short time frame might lead to temporary blocking of your API key.
- **Accuracy**: The LLM's accuracy depends on the quality of the questions, clarity of the language, and the model's training data. There is no guarantee of 100% accuracy.

## Further Development

This project can be further improved by adding features like:

- **Browser Support**: Extend support for different web browsers (e.g., Firefox, Edge).
- **Diverse Question Types**: Handle various question formats, including fill-in-the-blank and image-based questions.
- **User Interface**: Implement a more sophisticated user interface for better usability.
- **Logging and Reporting**: Add logging features to track the bot's actions and outcomes for analysis.
- **Dynamic Configuration**: Enable configuration through command-line arguments to make it easier to switch target webpages and settings without modifying the code.
