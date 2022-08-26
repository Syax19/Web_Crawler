# Crawler for job104
# -Extract company_name, job_opening, content

import requests
from bs4 import BeautifulSoup
import os
import re

if not os.path.exists("./job_104"):
    os.mkdir("./job_104")

url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword={}&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=1&asc=0&page={}&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1'
job = '雲端工程師'  # 更改此處可更改搜尋職稱


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

page = 1
for i in range(1, 5+1):  # 更改此處可更改爬蟲頁數, 目前設定為爬5頁
    res = requests.get(url=url.format(job, page), headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    jobArticle_list = soup.select('article[class="b-block--top-bord job-list-item b-clearfix js-job-item"]')
    for jobArticle in jobArticle_list:
        data = []
        companyContents = jobArticle.select('a')  # <class 'bs4.element.ResultSet'>, list

        companyName = companyContents[1]['title'].split()[0].split("：")[1]
        print("公司名稱:", companyName)
        data.append(companyName)
        data.append("\n")

        jobTitles = jobArticle.select('a em[class="b-txt--highlight"]')
        print("應徵職稱: ", end="")
        for jobTitle in jobTitles:
            print(jobTitle.text, end="")
            data.append(jobTitle.text)

        expRequired_list = jobArticle.select('ul[class="b-list-inline b-clearfix job-list-intro b-content"]')
        for expRequired in expRequired_list:
            exp = expRequired.select('li')
            print("\n工作經歷:", exp[1].text, end="\t")
            print("學歷:", exp[2].text)
            data.append("\n")
            data.append(exp[1].text)
            data.append("\n")
            data.append(exp[2].text)

        jobContents = jobArticle.select('p[class="job-list-item__info b-clearfix b-content"]')
        for jobContent in jobContents:
            print(jobContent.text)

            # -----Regular Expression to sub \r\n and \n-----
            pattern = r"[(\r\n)\n]"
            pattern_var = re.compile(pattern)
            contentResult = pattern_var.sub("", jobContent.text)

            data.append("\n")
            data.append(contentResult)

        salary_list = jobArticle.select('div[class="job-list-tag b-content"]')
        for salary in salary_list:
            sal = salary.select_one('span[class="b-tag--default"]')
            print("\n待遇:", sal.text)
            data.append("\n")
            data.append(sal.text)

        jobContentUrl = 'https:' + companyContents[0]['href']
        print("\n職缺網頁:", jobContentUrl)
        data.append("\n")
        data.append(jobContentUrl)

        companyAddress = companyContents[1]['title'].split()[1]
        print(companyAddress)
        data.append("\n")
        data.append(companyAddress)

        companyUrl = 'https:' + companyContents[1]['href']
        print("公司網頁:", companyUrl)
        data.append("\n")
        data.append(companyUrl)

        print("-" * 30)
        with open("./job_104/{}_{}.txt".format(companyName, jobTitles[0].text), "w", encoding='utf-8') as f:
            f.writelines(data)

    print('-----Page', page, 'scraping finished-----')
    page += 1
