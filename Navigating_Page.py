from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import global_var
import html
import sys
import os
import ctypes
from Scraping_data import Scraping_data
from selenium.webdriver.chrome.options import Options
import wx
import re
app = wx.App()


def ChromeDriver():
    chrome_options = Options()
    chrome_options.add_extension('C:\\BrowsecVPN.crx')
    browser = webdriver.Chrome(executable_path=str(f"C:\\chromedriver.exe"),chrome_options=chrome_options)
    browser.maximize_window()
    # browser.get("""https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh%3Fhl%3Den&amp;ved=2ahUKEwivq8rjlcHmAhVtxzgGHZ-JBMgQFjAAegQIAhAB""")
    wx.MessageBox(' -_-  Add Extension and Select Proxy Between 10 SEC -_- ','Info', wx.OK | wx.ICON_WARNING)
    time.sleep(15)
    browser.get("https://ppms.pprasindh.gov.pk/PPMS/public/portal/notice-inviting-tender")
    wx.MessageBox(' -_- Change Some Setting Then Wait For Load Website Fully Then OK   -_- ','Info', wx.OK | wx.ICON_WARNING)
    time.sleep(5)
    clicking(browser)


def clicking(browser):
    for status in browser.find_elements_by_xpath('//*[@id="PostedNIT:statusSerach"]/div[3]'):
        status.click()
        for Active in browser.find_elements_by_xpath('//*[@id="PostedNIT:statusSerach_1"]'):
            Active.click()
            break
        break
    time.sleep(1)
    for From_date in browser.find_elements_by_xpath('//*[@id="PostedNIT:searchPanel"]/tbody/tr[5]/td[2]/span/input'):
        From_date.send_keys(str(global_var.From_Date))
        break
    time.sleep(1)
    for TO_date in browser.find_elements_by_xpath('//*[@id="PostedNIT:searchPanel"]/tbody/tr[5]/td[4]/span/input'):
        TO_date.send_keys(str(global_var.To_Date))
        break
    time.sleep(1)

    # Remove Calender and then Click on DropDown
    for JUST in browser.find_elements_by_xpath('//*[@id="PostedNIT:agencyId"]/div[3]/span'):
        JUST.click()
        break
    time.sleep(1)

    # Select DropDown
    # for DropDown in browser.find_elements_by_xpath('//*[@id="PostedNIT:datalist:j_id10"]'):
    #     DropDown.click()
    #     # Select 500 On DropDown
    #     for DropDown1 in browser.find_elements_by_xpath('//*[@id="PostedNIT:datalist:j_id10"]/option[11]'):
    #         DropDown1.click()
    #         break
    #     break
    # time.sleep(1)

    for Search in browser.find_elements_by_xpath('//*[@id="PostedNIT:btnSearch"]'):
        Search.click()
        break
    time.sleep(13)
    Click_On_Tender_Icon(browser)


def Click_On_Tender_Icon(browser):
    a = False
    while a == False:
        try:
            page_End_count = ''
            for page_End_count in browser.find_elements_by_xpath('//*[@id="PostedNIT:datalist_paginator_top"]/span[1]'):
                page_End_count = page_End_count.get_attribute('innerText')  # eg: (1 OF 1)
                page_End_count = page_End_count.partition("OF")[2].partition(")")[0].strip()
                break
            for next_page in range(0, int(page_End_count)+1, 1):
                tr = 1
                for NIT_ID in browser.find_elements_by_xpath('/html/body/div[1]/div/div/div/form/div[2]/div[3]/table/tbody/tr/td[1]'):
                    browser.execute_script("arguments[0].scrollIntoView();", NIT_ID)
                    NIT_ID = NIT_ID.get_attribute('innerText').strip()
                    tender_Search_icon_error = True
                    while tender_Search_icon_error == True:
                        try:
                            for tender_Search_icon in browser.find_elements_by_xpath('/html/body/div[1]/div/div/div/form/div[2]/div[3]/table/tbody/tr['+str(tr)+']/td[9]/a[1]/img'):
                                browser.execute_script("arguments[0].scrollIntoView();", tender_Search_icon)
                                tender_Search_icon.click()
                                time.sleep(4)
                                break
                            tender_Search_icon_error = False
                        except:
                            print('Error When try to Click On Tender ICON')
                            wx.MessageBox(' -_- if there is a model opened Then close it and click on ok   -_- ','Info', wx.OK | wx.ICON_WARNING)
                            time.sleep(1)
                            tender_Search_icon_error = True
                    while True:
                        Model_Open_or_close = ''
                        for Model_Open_or_close in browser.find_elements_by_xpath('//*[@id="DownloadNITDlg"]'):
                            Model_Open_or_close = Model_Open_or_close.get_attribute('outerHTML').replace('\n','').strip()
                            break
                        Model_Open_or_close = re.sub('\s+', ' ', Model_Open_or_close)
                        Model_Open_or_close = Model_Open_or_close.partition('id="DownloadNITDlg"')[2].partition('"><div')[0].strip()
                        if 'display: block;' in Model_Open_or_close:
                            No_records_found = ''
                            for No_records_found in browser.find_elements_by_xpath('//*[@id="DownloadNITForm:itemlist1_data"]/tr/td'):
                                No_records_found = No_records_found.get_attribute('innerText').strip()
                                break
                            if No_records_found != 'No records found.':
                                get_htmlSource = ''
                                global_var.Total += 1
                                for get_htmlSource in browser.find_elements_by_xpath('//*[@id="DownloadNITDlg"]/div[2]'):
                                    get_htmlSource = get_htmlSource.get_attribute('outerHTML')
                                    get_htmlSource = html.unescape(str(get_htmlSource))
                                    break
                                time.sleep(2)
                                get_htmlSource = get_htmlSource.replace("""<input id="DownloadNITForm:corrigendumNo_focus" name="DownloadNITForm:corrigendumNo_focus" type="text" autocomplete="off" role="combobox" aria-haspopup="true" aria-expanded="false" aria-autocomplete="list" aria-owns="DownloadNITForm:corrigendumNo_items" aria-activedescendant="DownloadNITForm:corrigendumNo_0" aria-describedby="DownloadNITForm:corrigendumNo_0" aria-disabled="false">""", '')
                                get_htmlSource = get_htmlSource.replace('href="#', 'href="https://ppms.pprasindh.gov.pk/PPMS/public/portal/notice-inviting-tender#')
                                get_htmlSource = get_htmlSource.replace("""<select id="DownloadNITForm:corrigendumNo_input" name="DownloadNITForm:corrigendumNo_input" tabindex="-1" aria-hidden="true" onchange="PrimeFaces.ab({s:" downloadnitform:corrigendumno",e:"change",p:"downloadnitform:corrigendumno",u:"downloadnitform:tendergrid="" downloadnitform:nitinfo="" downloadnitform:nitgrid="" downloadnitform:sindhinews="" downloadnitform:urdunews="" downloadnitform:internationalengnew="" downloadnitform:suppengnews="" downloadnitform:engnews"});"=""><option value="0" selected="selected"></option></select>""", '')
                                Scraping_data(get_htmlSource, browser, NIT_ID)
                                print(" Total: " + str(global_var.Total) + " Duplicate: " + str(global_var.duplicate) + " Expired: " + str(global_var.expired) + " Inserted: " + str(global_var.inserted) +" Skipped: " + str(global_var.skipped) + " Deadline Not given: " + str(global_var.deadline_Not_given) + " QC Tenders: " + str(global_var.QC_Tender), "\n")
                                time.sleep(2)
                                error = True 
                                while error == True:
                                    try:
                                        for close_tab in browser.find_elements_by_xpath('//*[@id="DownloadNITDlg"]/div[1]/a/span'):
                                            browser.execute_script("arguments[0].scrollIntoView();", close_tab)
                                            close_tab.click()
                                            break
                                        error = False
                                    except:
                                        print('Error On Close Button')
                                        error = True
                                        time.sleep(1)
                                tr += 1
                            else:
                                browser.refresh()
                                ctypes.windll.user32.MessageBoxW(0, "No records found.", "pprasindh.gov.pk", 1)
                                clicking(browser)
                        break 
                error2 = True
                while error2 == True:
                    try:
                        for next_page in browser.find_elements_by_xpath('//*[@id="PostedNIT:datalist_paginator_bottom"]/a[3]'):
                            next_page.click()
                            time.sleep(5)
                            break
                        error2 = False
                    except:
                        print('Error On Next page button')
                        error2 = True
            a = True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " +str(e), "\n", exc_type, "\n", fname, "\n", exc_tb.tb_lineno)
            a = False

    ctypes.windll.user32.MessageBoxW(0, "Total: " + str(global_var.Total) + "\n""Duplicate: " + str(
        global_var.duplicate) + "\n""Expired: " + str(global_var.expired) + "\n""Inserted: " + str(
        global_var.inserted) + "\n""Skipped: " + str(global_var.skipped) + "\n""Deadline Not given: " + str(
        global_var.deadline_Not_given) + "\n""QC Tenders: " + str(
        global_var.QC_Tender) + "", "pprasindh.gov.pk", 1)
    browser.close()
    sys.exit()


ChromeDriver()
