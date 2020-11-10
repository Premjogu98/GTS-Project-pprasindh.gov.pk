# This Python file uses the following encoding: utf-8
import time
from datetime import datetime
import global_var
from Insert_On_Datbase import insert_in_Local
import sys
import os
import string
import time
from datetime import datetime
import html


def Scraping_data(get_htmlSource, browser, NIT_ID):
    a = 0
    while a == 0:
        try:
            SegField = []
            for data in range(45):
                SegField.append('')
                
            Submission_date = get_htmlSource.partition('id="DownloadNITForm:itemlist:0:j_idt203"')[2].partition("</td>")[0].strip()
            Submission_date = Submission_date.partition('">')[2].partition("</label>")[0].strip()
            if Submission_date != '':
                Submission_date = datetime.strptime(Submission_date, '%d-%m-%Y')  # 27-11-2019
                Submission_date = Submission_date.strftime("%Y-%m-%d")  # 2019-11-27
                SegField[24] = Submission_date
            if Submission_date == "":
                for Submission_date in browser.find_elements_by_xpath('//*[@id="DownloadNITForm:itemlist_data"]/tr[1]/td[6]'):
                    Submission_date = Submission_date.get_attribute('innerText').strip()
                    Submission_date = datetime.strptime(Submission_date, '%d-%m-%Y')  # 27-11-2019
                    Submission_date = Submission_date.strftime("%Y-%m-%d")  # 2019-11-27
                    SegField[24] = Submission_date
            # Tender ID
            SegField[13] = str(NIT_ID).replace("'", '').replace('[', '').replace(']', '')

            # Purchaser

            Purchaser = get_htmlSource.partition('id="DownloadNITForm:eoiCode"')[2].partition("</td>")[0].strip()
            Purchaser = Purchaser.partition('">')[2].partition("</label>")[0].strip()
            SegField[12] = Purchaser.upper()

            # Purchaser_Website = get_htmlSource.partition('id="DownloadNITForm:j_idt138"')[2].partition("</td>")[0].strip()
            # Purchaser_Website = Purchaser_Website.partition('">')[2].partition("</label>")[0].strip()
            # if Purchaser_Website != '-':
            #     SegField[8] = Purchaser_Website
            # else:
            #     SegField[8] = ''

            # Title
            Main_Title = get_htmlSource.partition('id="DownloadNITForm:j_idt126"')[2].partition("</td>")[0].strip()
            Main_Title = Main_Title.partition('">')[2].partition("</label>")[0].strip()
            Main_Title = string.capwords(str(Main_Title))
            if Main_Title == '':
                Main_Title = get_htmlSource.partition('id="DownloadNITForm:j_idt125"')[2].partition("</td>")[0].strip()
                Main_Title = Main_Title.partition('">')[2].partition("</label>")[0].strip()
                Main_Title = string.capwords(str(Main_Title))
            SegField[19] = Main_Title

            # Tender Description
            Reference_No = get_htmlSource.partition('id="DownloadNITForm:j_idt132"')[2].partition("</td>")[0].strip()
            Reference_No = Reference_No.partition('">')[2].partition("</label>")[0].strip()
            if Reference_No == '':
                Reference_No = get_htmlSource.partition('id="DownloadNITForm:j_idt131"')[2].partition("</td>")[0].strip()
                Reference_No = Reference_No.partition('">')[2].partition("</label>")[0].strip()

            Department_Name = get_htmlSource.partition('DownloadNITForm:j_idt130')[2].partition("</td>")[0].strip()
            Department_Name = Department_Name.partition('">')[2].partition("</label>")[0].strip()
            if Department_Name == '':
                Department_Name = get_htmlSource.partition('DownloadNITForm:j_idt129')[2].partition("</td>")[0].strip()
                Department_Name = Department_Name.partition('">')[2].partition("</label>")[0].strip()

            # Posting_date = ''
            # for Posting_date in browser.find_elements_by_xpath('//*[@id="DownloadNITForm:nitInfo"]/tbody/tr[4]/td[4]'):
            #     Posting_date = Posting_date.get_attribute('innerText')
            #     break

            Tender_Description = 'Title: '+str(SegField[19])+"<br>\n""Agency Name: "+str(SegField[12])+"<br>\n""Purchaser Website: "+str(SegField[8])+"<br>\n""Department Name: "+str(Department_Name)+"<br>\n""Reference No: "+str(Reference_No)
            Tender_Description = string.capwords(str(Tender_Description))
            SegField[18] = str(Tender_Description)

            SegField[7] = "PK"

            # notice type
            SegField[14] = "2"

            SegField[22] = "0"

            SegField[26] = "0.0"

            SegField[27] = "0"  # Financier

            SegField[2] = "Pakistan\n<br>[Disclaimer : For Exact Organization/Tendering Authority details, please refer the tender notice.]"
            # Source Name
            SegField[31] = "pprasindh.gov.pk"
            
            SegField[20] = ""
            SegField[21] = "" 
            SegField[42] = SegField[7]
            SegField[43] = "" 

            # Tender URl
            url = browser.current_url
            SegField[28] = str(url)

            for SegIndex in range(len(SegField)):
                print(SegIndex, end=' ')
                print(SegField[SegIndex])
                SegField[SegIndex] = html.unescape(str(SegField[SegIndex]))
                SegField[SegIndex] = str(SegField[SegIndex]).replace("'", "''")
            if len(SegField[19]) >= 200:
                SegField[19] = str(SegField[19])[:200]+'...'

            if len(SegField[18]) >= 1500:
                SegField[18] = str(SegField[18])[:1500]+'...'
            if len(SegField[19]) != 0 and SegField[24] != '' and len(SegField[18]) != '':
                Check_date(get_htmlSource, browser, SegField)
            a = 1
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " +str(e), "\n", exc_type, "\n", fname, "\n", exc_tb.tb_lineno)
            a = 0


def Check_date(get_htmlSource, browser, SegFeild):
    tender_date = str(SegFeild[24])
    nowdate = datetime.now()
    date2 = nowdate.strftime("%Y-%m-%d")
    try:
        if tender_date != '':
            deadline = time.strptime(tender_date, "%Y-%m-%d")
            currentdate = time.strptime(date2, "%Y-%m-%d")
            if deadline > currentdate:
                insert_in_Local(get_htmlSource, SegFeild)
            else:
                print("Expired")
                global_var.expired += 1
        else:
            print("Deadline was not given")
            global_var.deadline_Not_given += 1
            ctypes.windll.user32.MessageBoxW(0, "Deadline Not Found", "pprasindh.gov.pk", 1)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
