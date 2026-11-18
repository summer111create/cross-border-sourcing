from DrissionPage import ChromiumPage
import random, time
import csv

# ============================================================
# 换品类只改下面 3 个变量，其余不用动
# ============================================================
KEYWORD = '1U3352'          # 搜索词。阿里国际站建议用英文，多词用 + 连接，
                            # 如 'excavator+filter'（挖掘机滤芯）、'hydraulic+motor'（液压马达）
PAGES = 3                   # 要爬的页数。页数越多数据越多，但翻页间隔（下方 4–8 秒）别调短
OUT_FILE = '阿里原始.csv'    # 输出文件名。⚠️ 换品类必须换文件名（如 '滤芯原始.csv'），否则覆盖旧数据
# ============================================================

page = ChromiumPage()
page.get(f'https://www.alibaba.com/trade/search?SearchText={KEYWORD}')
page.wait(3)

rows = []
for p in range(PAGES):
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

with open(OUT_FILE, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['标题', '价格', '起订量'])
    for r in rows:
        w.writerow(r)
