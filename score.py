import csv
from cost import fob_profit
header=['商品名', '采购价', 'FOB报价', '单件净利', '利润率(%)', '利润分', '需求分', '竞争分', '总分', '等级']


def export_csv(rows, filename):
    with open(filename, 'w',encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def profit_score(margin_pct):
    score = margin_pct / 25 * 45
    return round(min(score, 45), 1)
# print(profit_score(4.9))
# print(profit_score(24.6))
# print(profit_score(30))


def demand_score(deal_90d):
    score = deal_90d / 50 * 30
    return round(min(score, 30), 1)
# print(demand_score(10))
# print(demand_score(50))
# print(demand_score(80))



def compete_score(rivals):
    score = 25 - rivals / 40 * 25
    return round(max(score, 0), 1)

# print(compete_score(0))
# print(compete_score(20))
# print(compete_score(40))
# print(compete_score(60))



def score_one(name, cost_cny, fob_usd, qty, deal_90d, rivals):
    profit, margin = fob_profit(fob_usd, cost_cny, qty)   # ← 复用 M4 的成果
    p = profit_score(margin)
    d = demand_score(deal_90d)
    c = compete_score(rivals)
    total = p + d + c
    if total >= 70:
        grade = 'A'
    elif total >= 50:
        grade = 'B'
    else:
        grade = 'C'
    return [name, cost_cny, fob_usd, profit, margin, p, d, c, total, grade]

print(score_one('斗齿', 113, 20, 500, 30, 20))


rows = [
    score_one('斗齿', 113, 20, 500, 30, 20),
    score_one('滤芯', 45, 9, 300, 12, 35),
]
export_csv(rows, '选品评分.csv')


















