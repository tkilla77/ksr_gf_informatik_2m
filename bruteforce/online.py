### requires: `pip install selenium`
 
### DON'T CHANGE CODE FROM HERE ...
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
 
# url to website
url_website = "https://bottom.ch/ksr/hackme/"
 
# Open the webpage
options = webdriver.ChromeOptions()
#options.add_argument("--headless=new")  # enable to make Chrome a bit faster
driver = webdriver.Chrome(options=options)
driver.get(url_website)
 
# Find buttons
input_field = driver.find_element(By.ID,"textInput") # find the input box ...
code_field = driver.find_element(By.ID, "responseCode") # find the response code box ...
decrypted_field = driver.find_element(By.ID, "encryptedTextArea") # find the encrypted text box ...
button = driver.find_element(By.ID,"btnSend") # find the button ...
 
def try_with_clicking(pw):
    """Enters password and clicks the button, performs 10-20 clicks per second."""
    # 1) Enter text in the input field
    input_field.clear()
    input_field.send_keys(pw)
    # 2) Click the button
    button.click()
    # 3) Read response and output
    code = code_field.get_attribute("value")
    message = decrypted_field.get_attribute("value")
    return code, message
 
def try_with_js(pw):
    """Tests a password by executing the relevant JS function, performs around 500 attempts per second."""
    return driver.execute_script(f'return check_pw("{pw}")')
 
### ... UNTIL HERE
### WRITE YOUR CODE BETWEEN HERE ...
def hack_single(pw):
    pw = ''.join(pw)
    code, message = try_with_js(pw)
    if int(code) < 400:
        return code, message, pw


from multiprocessing import Pool
from tqdm.auto import tqdm

def hack_password():
    import string, itertools
    
    alphabet = string.ascii_uppercase

    with Pool(processes=4) as pool:
        for l in range(3, 6):
            yield from (response for response in tqdm(pool.imap_unordered(hack_single, itertools.product(alphabet, repeat=l), chunksize=1000), total=len(alphabet)**l) if response)

def hack_password2():
    import string, itertools
    with open('woerter_top10000de_upper.txt') as f:
        words = [line.strip() for line in f]
        with Pool(processes=4) as pool:
            yield from (response for response in tqdm(pool.imap_unordered(hack_single, itertools.product(words, repeat=2), chunksize=1000), total=len(words)**2) if response)

if __name__ == '__main__':
    start = time.time()
    code, message, pw = next(hack_password2())
    elapsed = time.time() - start
    print(f"Code: {code}, Message: {message}, Password: {pw}, Elapsed: {elapsed:.1f}s")
    
    ### ... AND HERE. DON'T CHANGE LAST LINE:
    driver.quit() # Close the browser