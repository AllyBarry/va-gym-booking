from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support.ui import WebDriverWait
import datetime as dt
import configparser

# Setup - ensure x server is running before starting

def get_date_picker(new_date):
    today = dt.datetime.now().date()
    num_days = (new_date - today).days
    if num_days > 7:
        raise Exception("Date too far in the future.")
    picker_num = "picker_%d" % num_days
    return picker_num

def init_session():
    opts = Options()
    #opts.add_argument("--headless")
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument("--remote-debugging-port=9222")  # this
    #opts.add_argument("window-size=1024,768")
    opts.add_experimental_option("detach", True)

    # Retrieve User Config
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'User' not in config:
        raise Exception('Config file does not contain user details.')
    user_id = config['User']['id_number']

    driver = Chrome(options = opts)
    driver.get("https://my.virginactive.co.za/bookings/")
    user_input = driver.find_element(By.CSS_SELECTOR, "#input_id")
    user_input.send_keys(user_id + Keys.ENTER)
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#make_a_booking')))
    button.click()
    return driver

def get_classes_by_date(driver, date):
    picker = get_date_picker(date)
    select_date = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#calendar div#date-picker a#%s' % picker)))
    select_date.click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#times div.slot')))
    slots = driver.find_elements(By.CSS_SELECTOR, "div#times div.slot")
    classes_dict = {}
    for slot in slots:
        details = slot.find_elements(By.CSS_SELECTOR, "div.timeelement")
        sl_time, sl_duration = details[0].text.split(" ")
        sl_class, sl_venue = details[1].text.split("\n")
        sl_instructor = details[2].text
        sl_status = details[3].text
        sl_book_btn = None
        if not sl_status == "FULLY BOOKED":
            sl_book_btn = details[4]
        classes_dict[sl_class+"-"+sl_time] = {
            "instructor": sl_instructor,
            "duration": sl_duration,
            "slots_free": sl_status,
            "venue": sl_venue,
            "book_btn": sl_book_btn
        }
    return classes_dict
    
def book_class(classes_dict, class_name, class_time, driver):
    class_selector = class_name+"-"+class_time
    if class_selector in classes_dict:
        class_sel = classes_dict[class_selector]
    else:
        raise Exception("Class not available at this time.")
    if class_sel["slots_free"] == "FULLY BOOKED":
        raise Exception("No slots available.")
    book_btn = class_sel["book_btn"].find_element(By.TAG_NAME, "a")
    book_btn.click()
    confirm_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.confirmbtncontainer a[href='javascript:confirmBooking()']")))
    confirm_btn.click()

def week_ahead_class_book(class_name, class_time):
    today = dt.datetime.now().date()
    week_ahead = today+dt.timedelta(days=7)
    driver = init_session()
    classes_dict = get_classes_by_date(driver, week_ahead)
    book_class(classes_dict, class_name, class_time, driver)
    driver.quit()

if __name__ == "__main__":
    # Eg book for Cycle at 6.15am:
    week_ahead_class_book("Cycle", "06:15")