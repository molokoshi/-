"""Scraping program for app"""
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.utils.timezone import make_aware
import datetime


def main(value):
    from .models import DetailInfo, BaseInfo

    def count_scraping_ad(CSS_SELECTOR):
        """掲載されている広告数をカウント"""
        ad = 0
        for i in driver.find_elements_by_css_selector(CSS_SELECTOR):
            ad += 1
        return ad

    def To_advertise(i, CSS_SELECTOR):
        """各コンテンツへのパス"""
        way_to_advertise = "#content > div > div._7lca > div._7lcc > div._8n-_ > div._8n-x > div > div._7jjx > div._7jj- > div._7owt"
        on_ad_way = driver.find_elements_by_css_selector(way_to_advertise)[i].find_elements_by_css_selector(
            CSS_SELECTOR)
        return on_ad_way

    def turn_num_only(num):
        """スクレイピングしたテキストから数値を抜出"""
        escape = re.search(r'\d+', num)
        num = escape.group(0)
        return num

    # 各種設定
    op = Options()
    op.add_argument("--disable-gpu")
    op.add_argument("--disable-extensions")
    op.add_argument("--proxy-server='direct://'")
    op.add_argument("--proxy-bypass-list=*")
    op.add_argument("--start-maximized")
    op.add_argument("--headless")
    Chormedriverpath = "C:\\Program Files\\chromedriver_win32\\chromedriver"
    driver = webdriver.Chrome(Chormedriverpath)
    # chrome_options=op <--オプションを使う場合
    Check_flag = True
    try:
        # checker = 0
        for i in range(1):
            URL = "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=JP&impression_search_field=has_impressions_lifetime&view_all_page_id={}".format(
                value)
            driver.get(URL)
            # 一番下までスクロール
            first_html = driver.page_source
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                next_html = driver.page_source
                if first_html != next_html:
                    first_html = next_html
                else:
                    break
                # 広告主情報
            ad_boss = driver.find_element_by_css_selector("div._8tue").text
            ad_nice = driver.find_element_by_css_selector("div._8tuf > div >div:nth-of-type(2)").text
            ad_num = driver.find_element_by_css_selector("div._7gn2 > div").text
            print("広告主: " + ad_boss + " 広告件数: " + turn_num_only(ad_num) + "件" + " いいね！ " + ad_nice + "ID:" + value)
            BaseInfo.objects.create(base_id=value, master=ad_boss, nice=ad_nice)
            # 変数初期化
            ad_masters = []
            ad_dates = []
            ad_ids = []
            ad_maintexts = []
            ad_subtexts = []
            ad_imgs = []
            detail_ids = []

            # 広告情報
            for i in range(count_scraping_ad("div._7owt")):
                detail_ids.append(value)
                try:
                    # 確実に存在する要素
                    date_str = To_advertise(i, "div._7jwu > span")[0].text
                    ad_dates.append(DetailInfo(advertise_register=make_aware(datetime.datetime.strptime(date_str, "%Y/%m/%d"))))
                    ad_ids.append(DetailInfo(ad_id=int(turn_num_only(To_advertise(i, "div._8jox > div")[0].text))))
                    if To_advertise(i, "div._8nqr._3qn7._61-3._2fyi._3qng > span > a") == []:
                        ad_masters.append(DetailInfo(name=To_advertise(i, "div._8nqr._3qn7._61-3._2fyi._3qng > span")[0].text[:255]))
                    else:
                        ad_masters.append(DetailInfo(name=To_advertise(i, "div._8nqr._3qn7._61-3._2fyi._3qng > span > a")[0].text[:255]))
                except Exception:
                    print("error1")
                    Check_flag = False
                try:
                    # ない場合がある要素
                    if To_advertise(i, "div._7jyr div._4ik4._4ik5 > div") == []:
                        ad_maintexts.append(DetailInfo(main_text=""))
                    else:
                        ad_maintexts.append(DetailInfo(main_text=To_advertise(i, "div._7jyr div._4ik4._4ik5 > div")[0].text[:100]))

                    if To_advertise(i, "div._7jyg._7jyh > div._8jgz._8jg_ > div._8jh1") == []:
                        ad_subtexts.append(DetailInfo(sub_text=""))
                    else:
                        ad_subtexts.append(
                            DetailInfo(sub_text=To_advertise(i, "div._7jyg._7jyh > div._8jgz._8jg_ > div._8jh1")[0].text[:100]))
                    if To_advertise(i, "img._7jys") is To_advertise(i, "div._8o0a._8o0b video"):
                        ad_imgs.append("no_image")
                    else:
                        if To_advertise(i, "div._8o0a._8o0b video") != []:
                            ad_imgs.append(DetailInfo(sample_img=To_advertise(i, "div._8o0a._8o0b video")[0].get_attribute("src")[:255]))
                        else:
                            ad_imgs.append(DetailInfo(sample_img=To_advertise(i, "img._7jys")[0].get_attribute("src")[:255]))
                except Exception:
                    Check_flag = False
                    print("error2")
            DetailInfo.objects.bulk_update(ad_dates, fields=['advertise_register'])
            DetailInfo.objects.bulk_update(ad_masters, fields=['name'])
            DetailInfo.objects.bulk_update(ad_maintexts, fields=['main_text'])
            DetailInfo.objects.bulk_update(ad_subtexts, fields=['sub_text'])
            DetailInfo.objects.bulk_update(ad_ids, fields=['ad_id'])
            DetailInfo.objects.bulk_update(ad_imgs, fields=['sample_img'])

    except Exception:
        Check_flag = False
        pass
    print(Check_flag)
    driver.close()
    return Check_flag


if __name__ == '__main__':
    main()