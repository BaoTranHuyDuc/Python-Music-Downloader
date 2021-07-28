import os
from tinytag import TinyTag
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
song_list = os.listdir('D:\Desktop\Music')
# read_music_folder

for song in song_list:
    driver = webdriver.Chrome('D:\\Desktop\\chromedriver.exe')
    try:
        audio_file = TinyTag.get('D:\\\Desktop\\Music\\' + song)
        # read metadata

        #audio_athor and audio_title represents metadata in the original file
        audio_title = audio_file.title
        audio_author = audio_file.artist
        audio_title_split = audio_title.split() + audio_author.split(",")
        search_string = ""

        # search song name in URL
        for x in range(len(audio_title_split)):
            if x != len(audio_title_split) - 1:
                search_string += audio_title_split[x] + "+"
            else:
                search_string += audio_title_split[x]
        driver.get('https://chiasenhac.vn/tim-kiem?q=' + search_string)

        #log-in
        driver.execute_script("arguments[0].click();",  driver.find_element_by_link_text('Đăng nhập'))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form-login"]/div[1]/div/input[1]')))
        driver.find_element_by_xpath('//*[@id="form-login"]/div[1]/div/input[1]').send_keys('real_username')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form-login"]/div[1]/div/input[2]')))
        driver.find_element_by_xpath('//*[@id="form-login"]/div[1]/div/input[2]').send_keys('real_password')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form-login"]/div[1]/div/div/button')))
        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="form-login"]/div[1]/div/div/button'))

        #search song
        for x in range(7):
            if x == 6:
                print(song)
                driver.quit()
            else:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-all"]/ul/li[' + str(x+1) + ']/div[2]/div/h5/a')))
                song_title = driver.find_element_by_xpath('//*[@id="nav-all"]/ul/li[' + str(x+1) + ']/div[2]/div/h5/a').text
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-all"]/ul/li[' + str(x+1) + ']/div[2]/div/div')))
                song_author = driver.find_element_by_xpath('//*[@id="nav-all"]/ul/li[' + str(x+1) + ']/div[2]/div/div').text
                def replaceMultiple(mainString, toBeReplaces, newString):
                    for elem in toBeReplaces:
                        if elem in mainString:
                            mainString = mainString.replace(elem, newString)
                    return mainString
                if audio_author.split(",")[0].strip().lower() in replaceMultiple(song_author, ["'", ".", ",", "!", "?"], "").strip().lower() and replaceMultiple(song_title, ["'", ".", ",", "!", "?"], "").strip().lower() in replaceMultiple(audio_title, ["'", ".", ",", "!", "?"], "").strip().lower():
                    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="nav-all"]/ul/li[' + str(x + 1) + ']/div[2]/div/h5/a')))
                    time.sleep(5)
                    driver.execute_script('arguments[0].click();', driver.find_element_by_link_text(song_title))


                    #download songs
                    driver.execute_script('arguments[0].click();', driver.find_element_by_xpath('//*[@id="pills-download-tab"]'))
                    try:
                        driver.execute_script('arguments[0].click();',driver.find_element_by_xpath('// *[ @ id = "pills-download"] / div / div[2] / div / div[1] / ul / li[4] / a / span'))
                    except NoSuchElementException:
                        driver.execute_script('arguments[0].click();',driver.find_element_by_xpath('// *[ @ id = "pills-download"] / div / div[2] / div / div[1] / ul / li[3] / a / span'))


                    #check if download is finished
                    file_path_old = driver.find_element_by_xpath('/html/body/section/div[3]/div/div[1]/div[1]/h1').text.replace("; ", "_ ")
                    file_path_new = replaceMultiple(file_path_old, ["'", ".", ",", "!", "?"], "_")
                    seconds_until_termination = 0
                    if len(file_path_new) > 40:
                        reduced_file_path = file_path_new[:40] + ".flac"
                        reduced_file_path_m4a = file_path_new[:40] + ".m4a"
                        time.sleep(10)
                        while os.path.exists("D:\\Downloads\\" + reduced_file_path + ".crdownload") is True or os.path.exists("D:\\Downloads\\" + reduced_file_path_m4a + "cr.download") is True:
                            time.sleep(1)
                            seconds_until_termination += 1
                            if seconds_until_termination == 1800:
                                print(song)
                                driver.quit()
                                break
                            else:
                                pass
                        time.sleep(6)
                        if os.path.isfile("D:\\Downloads\\" + reduced_file_path + "cr.download") is False or os.path.isfile("D:\\Downloads\\" + reduced_file_path_m4a + "cr.download") is False:
                            driver.quit()
                            break
                    else:
                        reduced_file_path = file_path_new + ".flac"
                        reduced_file_path_m4a = file_path_new + ".m4a"
                        time.sleep(10)
                        while os.path.exists("D:\\Downloads\\" + reduced_file_path + ".crdownload") is True or os.path.exists("D:\\Downloads\\" + reduced_file_path_m4a + "cr.download") is True:
                            time.sleep(1)
                            seconds_until_termination += 1
                            if seconds_until_termination == 1800:
                                print(song)
                                driver.quit()
                                break
                            else:
                                pass
                        time.sleep(6)
                        if os.path.isfile("D:\\Downloads\\" + reduced_file_path + "cr.download") is False or os.path.isfile("D:\\Downloads\\" + reduced_file_path_m4a + "cr.download") is False:
                            driver.quit()
                            break
                else:
                    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="nav-all"]/ul/li[' + str(x + 1) + ']/div[2]/div/h5/a')))
                    time.sleep(10)
                    driver.execute_script("arguments[0].remove()", driver.find_element_by_xpath('//*[@id="nav-all"]/ul/li[' + str(x+1) + ']/div[2]/div/h5/a'))

    #exception checks
    except StaleElementReferenceException:
        print("Stale" + song)
        driver.quit()
    except NoSuchElementException():
        print("No Song" + song)
        driver.quit()
    except:
        print("Unknown Error" + song)
        driver.quit()


#driver.quit()