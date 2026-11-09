from DrissionPage import ChromiumPage
import random, time
import csv

page = ChromiumPage()
page.get('https://www.alibaba.com/trade/search?SearchText=1U3352')
page.wait(3)

rows = []
for p in range(3):
    cards = page.eles('css:.fy26-product-card')
    print(f'第 {p+1} 页卡片数: {len(cards)}')

    for card in cards:
        try:
            offer = card.attr('data-aplus-auto-offer') or ''
            if 'is_ad=true' in offer:        # 跳过广告位
                continue
            title = card.ele('css:.searchx-product-e-title').text

            price = card.ele('css:.searchx-product-price-price-main').text
            moq_text = card.ele('css:.searchx-moq').text
            rows.append((title, price, moq_text))
        except Exception:
            pass

    nav = page.ele('css:.searchx-pagination')
    links = nav.eles('tag:a')
    if links:
        links[-1].click()
    time.sleep(random.uniform(4, 8))

print('有效条数:', len(rows))

with open('阿里原始.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['标题', '价格', '起订量'])
    for r in rows:
        w.writerow(r)























