# icook recipe scraper

import requests
from bs4 import BeautifulSoup
import os
import re
import json

vegetable = input("請輸入想查詢的蔬菜名稱:")

"""若儲存資料夾不存在，則創建新資料夾"""
# if not os.path.exists("./icook/"):
#     os.mkdir("./icook")
#
# if not os.path.exists("./icook/" + vegetable):
#     os.mkdir("./icook/" + vegetable)

if not os.path.exists("./icook/" + vegetable):
    os.makedirs("./icook/" + vegetable)

headers = {
    'content-type': 'text/html; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}



# url = 'https://icook.tw/search/%E9%A3%9F%E6%9D%90%EF%BC%9A%E7%AB%B9%E7%AD%8D/?page={}'

url = 'https://icook.tw/search/食材：{}/?page={}'

page_scraped = int(input("請問想爬幾頁食譜(請輸入阿拉伯數字):"))
page = 1
for i in range(0, page_scraped):
    res = requests.get(url=url.format(vegetable, page), headers=headers)
    html = res.content
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)

    recipe_ingredient = {}

    """取得食譜標題"""
    recipes_Obj = soup.select('li[class="browse-recipe-item"]')  # <class 'bs4.element.ResultSet'>
    for recipes in recipes_Obj:
        # print(recipes)
        try:
            titles = recipes.select('h2[class="browse-recipe-name"]')  # <class 'bs4.element.ResultSet'>
            for titleName in titles:
                recipeName = titleName.text.strip()
                pattern = r"[\\\\/:*?\"<>|]"
                pattern_var = re.compile(pattern)
                recipeName = pattern_var.sub("", recipeName)
                recipe_ingredient["RecipeName"] = recipeName
                # print(recipeName)
        except AttributeError as error:
            print(error)

        """取得食譜內文網址"""
        contents = recipes.select('a')  # <class 'bs4.element.ResultSet'>
        for content in contents:
            contentUrl = "https://icook.tw/" + content["href"]
            recipe_num = contentUrl.split("/")[5]
            # print(recipe_num)
            recipe_ingredient["Url"] = contentUrl
            # print(contentUrl)

            """取得食譜內文詳細內容"""
            content_res = requests.get(url=contentUrl, headers=headers)
            content_html = content_res.content
            content_soup = BeautifulSoup(content_html, 'html.parser')
            # print(content_soup)

            ingredients_Obj = content_soup.select('div[class="recipe-details-ingredients recipe-details-block"]')
            # print(ingredients_Obj)
            for ingredients in ingredients_Obj:
                ings = ingredients.select_one('h2[class="title"]').text
                recipe_ingredient["Ingredients"] = []
                # print(ings)  # 食材

                for ingredient in ingredients.select('div[class="ingredient"]'):
                    # print(ingredient)
                    ingredientName = ingredient.select_one('a').text  # 食材名稱
                    recipe_ingredient["Ingredients"].append(ingredientName)
                    # print(ingredientName)
                    ingredientUnit = ingredient.select_one('div.ingredient-unit').text  # 食材用量
                    recipe_ingredient["Ingredients"].append(ingredientUnit)
                    # print(ingredientUnit)

            """食譜作法"""
            recipe_details_Obj = content_soup.select('ul[class="recipe-details-steps"]')
            for detail in recipe_details_Obj:
                details = detail.select('p[class="recipe-step-description-content"]')
                detail_content = ''
                for detail_contents in details:
                    detail_content += (detail_contents.text.strip() + "\n")
                    # print(detail_content)
                recipe_ingredient["RecipeDetail"] = detail_content

            """食譜成品照片"""
            recipe_images = content_soup.select('a[class="glightbox ratio-container ratio-container-4-3"]')
            for img in recipe_images:
                recipe_images_url = img["href"]
                # print(recipe_images_url)
                res_img = requests.get(url=recipe_images_url, headers=headers)
                with open('./icook/{}/{}_{}.jpg'.format(vegetable, recipeName, recipe_num), 'wb') as f:
                    f.write(res_img.content)

            print("-" * 30)
            print(recipe_ingredient)
            with open('./icook/{}/{}_{}.json'.format(vegetable, recipeName, recipe_num), 'w', encoding='utf-8') as j:
                json.dump(recipe_ingredient, j, ensure_ascii=False)
                print("Writing complete!")
    print(f"-----Page {page:^6} complete!-----")
    page += 1



