# Web_Crawler
### 使用時須注意版權問題

* icook_scraper
>     擷取icook食譜網食譜及其內容
> 輸入欲搜尋食材或食譜名稱，爬取頁面數後即可擷取：
> 
> 食譜名稱json檔案：包含食譜名、食譜內容(食材名稱、用量、作法)\
> 食譜名稱jpg檔案：食譜照片\
> 擷取內容會保存在icook_scraper.py檔資料夾中的「icook」資料夾底下「蔬菜名稱」資料夾中
> 

* job_104_scraper
>     擷取104人力銀行職缺及職缺內容
> 更改以下參數可客製蒐尋職缺：
> 
> line 13  job = '雲端工程師'  # 更改此處可更改搜尋職稱\
> line 21  for i in range(1, 5+1):  # 更改5+1此處可更改爬蟲頁數, 預設為爬5頁\
> 預設存檔檔案為「公司名稱_職稱」.txt檔, 路徑為job_104_scraper.py檔資料夾中「job_104」資料夾
> 

* job_104_to_csv
>     將job_104_scraper爬取下內容整理成csv檔案
