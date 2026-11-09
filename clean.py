import csv
def prece(text):#a = "$8.00 + $9.50 / piece",这是B2B的报价区间
    a=text.split('/')[0]
    a=a.replace('$','')
    a=a.split('+')
    number1=float(a[0].strip())
    number2=float(a[1].strip())
    return (number1+number2)/2
#print(prece("$10.00 + $11.50 / piece")) # 输出：取平均作为代表单价
                                      # 注意：初筛阶段建议改取最高价，避免高估利润

def orders(text):#清洗销量 "2500+ orders" → 2500
    b=text.split('+')[0]
    b=int(b)
    return b
#print(orders("500+ orders"))

def moq(text):  # "最低起订量：1 set"
    c = text.split('：')[1]
    c = c.strip()
    parts = c.split(' ')
    return int(parts[0].replace(',', '')), parts[1]


USD_CNY_ALI = 6.68
def parse_price_cny(text):#¥19.03-32.38
    text = text.replace('¥', '').replace(',', '')
    parts = text.split('-')
    if len(parts) == 1:
        low = float(parts[0])
        high =  float(parts[0])
    else:
        low = float(parts[0])
        high = float(parts[1])

    return low, high

def to_usd(price_cny):
    price_usd = price_cny / USD_CNY_ALI
    return round(price_usd, 2)

def read_prices(filename):
    with open(filename, encoding='utf-8-sig', newline='') as f:
        rows = list(csv.reader(f))
    for row in rows[1:]:
        if len(row)<2:
            continue
        title = row[0]
        price_text = row[1]
        low_cny, high_cny = parse_price_cny(price_text)
        low_usd = to_usd(low_cny)
        print(title[:20],low_usd)
def clean_all(src, dst):
    with open(src,'r',encoding='utf-8-sig') as f:
        rows = list(csv.reader(f))
        rows_out = []
        seen = set()
    for row in rows[1:]:
        title = row[0]
        if len(row)<3:
            continue

        if title in seen:
            continue
        seen.add(title)
        low_cny, high_cny = parse_price_cny(row[1])
        qty, unit = moq(row[2])
        low_piece_cny = to_per_piece(low_cny, unit)
        high_piece_cny = to_per_piece(high_cny, unit)
        if low_piece_cny is None:
            continue
        if not is_price_reasonable(low_piece_cny):  # ← 新增第 71 行
            continue
        rows_out.append([title, to_usd(low_piece_cny), to_usd(high_piece_cny), unit])

    with open(dst, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['标题', '最低价USD', '最高价USD', '计价单位'])
        for r in rows_out:
            w.writerow(r)

TOOTH_WEIGHT_KG = 6.0

def to_per_piece(price_cny, unit):
    if unit.startswith('kilogram'):
        return round(price_cny * TOOTH_WEIGHT_KG, 2)
    if unit.startswith('piece'):
        return round(price_cny, 2)
    return None

STEEL_PRICE_CNY_PER_KG = 4.0      # 钢材地板单价，2026-10 钢价区间取保守值
def is_price_reasonable(price_piece_cny):
    floor_cny = TOOTH_WEIGHT_KG * STEEL_PRICE_CNY_PER_KG

    return price_piece_cny >= floor_cny

if __name__ == '__main__':
    print(prece()
    print(is_price_reasonable(254.7))
    print(is_price_reasonable(59.7))
    print(is_price_reasonable(24.0))
    print(is_price_reasonable(23.99))
    print(is_price_reasonable(4.01))
    clean_all('阿里原始.csv', '阿里清洗.csv')












