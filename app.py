from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import time
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
gemini_api_key = os.environ.get("GEMINI_API_KEY")
webpage = os.environ.get("TARGET_WEBPAGE")

# Initialize Google Gemini
genai.configure(api_key=gemini_api_key)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="Solve the question and return ONLY the option ID of the correct option in the format: optionD[24234]",  # Clearer instruction
)

chat_session = model.start_chat()

# --- Functions ---

def extract_question_data(driver, q_id):
    """Extracts question text and options from the webpage."""
    try:
        q_div = driver.find_element(By.ID, f"qsnId{q_id}")

        # Make question visible if hidden
        if q_div.get_attribute("style") == "display: none;":
            driver.execute_script("arguments[0].style.display = 'block';", q_div)

        driver.execute_script("arguments[0].scrollIntoView(true);", q_div)
        WebDriverWait(driver, 10).until(EC.visibility_of(q_div))

        que_div = q_div.find_element(By.ID, "testqsn")
        question_text = que_div.find_element(By.TAG_NAME, "p").text.strip()
        if not question_text:
            question_text = que_div.get_attribute("innerText").strip()

        question_data = {'id': q_id, 'question': question_text, 'options': {}}

        options = q_div.find_elements(By.CLASS_NAME, "form-check")
        for index, option in enumerate(options):
            try:
                radio_button = option.find_element(By.CSS_SELECTOR, "input[type='radio']")
                option_value = radio_button.get_attribute("value")
                label = option.find_element(By.XPATH, f".//label[@for='{radio_button.get_attribute('id')}']")
                label_text = label.text.strip()
                if ":" in label_text:
                    label_text = label_text.split(":")[1].strip()
                question_data['options'][f"option{option_value}[{q_id}]"] = label_text
            except NoSuchElementException as e:
                print(f"Error processing option for Question ID: {q_id}: {e}")

        return question_data

    except NoSuchElementException as e:
        print(f"Error processing question with ID {q_id}: {e}")
        return None

def get_correct_option_from_llm(question_text, options):
    """Gets the correct option from the Gemini LLM."""
    response = chat_session.send_message(f"{question_text} Options: {options}")
    print(f"LLM Response: {response.text}")
    return response.text

def select_option_and_proceed(driver, q_id, option_value):
    """Selects the given option and clicks 'Next'."""
    try:
        radio_button_container = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//input[@id='option{option_value}[{q_id}]']/parent::div"))
        )
        radio_button = radio_button_container.find_element(By.CSS_SELECTOR, f"input[type='radio'][value='{option_value}']")

        if not radio_button.is_enabled():
            print(f"Radio button for option {option_value} is disabled! (Question ID: {q_id})")
            return 

        try:
            radio_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", radio_button)

        time.sleep(1)  # Adjust wait time if needed

        try:
            next_bt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "next")))
            next_bt.click()
            print(f"Selected option {option_value} for Question ID {q_id}")
        except TimeoutException:
            print("No 'Next' button found. Assuming end of test.")
            return  

    except NoSuchElementException as e:
        print(f"Error selecting option for Question ID {q_id}: {e}")

# --- Main Execution ---

# Initialize Selenium WebDriver (replace with your browser and path)
driver = webdriver.Chrome()  

try:
    driver.get(webpage)
    time.sleep(2)

    # Close initial modal (if any)
    try:
        driver.find_element(By.CLASS_NAME, "btn-close").click()
    except NoSuchElementException:
        pass  

    driver.find_element(By.ID, "attndName").send_keys("YOUR NAME")
    driver.find_element(By.ID, "attndCred").send_keys("YOUR_CRED")
    driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "startTestBtn"))

    time.sleep(2) 

    questions_list = []
    for element in driver.find_elements(By.XPATH, "//input[@id='Qid']"):
        q_id = element.get_attribute("value")
        question_data = extract_question_data(driver, q_id)
        if question_data:
            questions_list.append(question_data)

    # Save and/or process the questions
    with open('questions.json', 'w') as json_file:
        json.dump(questions_list, json_file, indent=4)
    print("Questions have been saved to questions.json")

    # Answer questions using LLM
    for question in questions_list:
        correct_option_key = get_correct_option_from_llm(question['question'], question['options'])
        if correct_option_key:
            option_value = correct_option_key.split('[')[0][-1] 
            select_option_and_proceed(driver, question['id'], option_value)
        else:
            print(f"No correct option found for Question ID {question['id']}")

    # Submit the test
    try:
        driver.find_element(By.ID, "testSubmit").click()
        confirm_bt = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".swal2-actions button"))
        )
        confirm_bt.click()
        print("Test submitted successfully!")
    except Exception as e:
        print(f"Error submitting test: {e}")

finally:
    time.sleep(5)
    driver.quit()