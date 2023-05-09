import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


# use selenium on tweeterid.com to get the twitter id from a twitter handle
def fromh(handle):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('http://tweeterid.com')
    driver.find_element('id','twitter').send_keys(handle)
    driver.find_element('id','twitterButton').click()
    id = WebDriverWait(driver,15).until(EC.visibility_of_element_located((By.ID,'oid-0'))).get_attribute('textContent')
    driver.quit()
    return id.split(' => ')[-1]


# take input file containig twitter handles one on each line
# output a file translating each line from handle to twitter ID
def get_ids(input_fle):
    print(f"Start processing intput: {input_fle} ...")
    ids = []
    with open(input_file, 'r') as i_file:
        handles = [line.strip() for line in i_file]
        for handle in handles:
            print(handle)
            id = fromh(handle)
            # if getting network error, wait and try later
            if id == "Error: Connection":
                print(f"Updating for user: {handle}")
                print("Sleep for 5 secs...")
                time.sleep(5)
                while True:
                    id = fromh(handle)
                    if res != "Error: Connection":
                        ids.append(id)
                        with open(output_file, 'w+') as o_file:
                            o_file.writelines('\n'.join(ids))
                            o_file.close()
                        break
                    else:
                        print("Sleep for 5 secs...")
                        time.sleep(5)
            # add the result otherwise
            else:
                ids.append(id)
                with open(output_file, 'w+') as o_file:
                    o_file.writelines('\n'.join(ids))
                    o_file.close()
        i_file.close()
    print(f"Finshed processing input: '{input_path}'")


# remote entries containig errors (user not found)
def clean_ids(output_file):
    # generate file name for the clean output
    n = output_file.index(".")
    clean_output_file = output_file[:n]+"clean"+output_file[n:]

    print(f"Cleaning up output, generate new file: {clean_output_file} ...")
    # read in raw output and exclude entries containing string "error"
    with open(output_file, 'r') as i_file:
        ids = [line.strip() for line in i_file]
        clean_ids = [id for id in ids if "error" not in id.lower()]
        with open(clean_output_file, 'w+') as o_file:
            o_file.writelines('\n'.join(clean_ids))
            o_file.close()
        i_file.close()
    print("Finshed cleaning output")


if __name__ == '__main__':
    # input and output file names
    input_file = 'valid_twitter_handles_2023-05-02.txt'
    output_file = 'twitter_ids_translated_2023-05-02.txt'

    # translate input twitter handles to twitter IDs
    get_ids(input_file)
    # remote entries containig errors (user not found)
    clean_ids(output_file)
