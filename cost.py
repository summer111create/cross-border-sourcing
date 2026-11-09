USD_CNY = 7.10       #汇率   美元换成元                                      #注释按照  [含义] _ [量级] _ [单位]
                                                               #cost_cny  人民币 单件
VAT_IN = 0.13          # 进项税率：采购价里已经含的税                #fob_usd     # 美元，单件
REBATE_RATE = 0.13     # 出口退税率 🔴 待你查 HS 编码核实           #qty         # 件数
                                                               #unit_cbm    # 立方米，单件
INLAND_FEE = 2000.0    # 济宁→青岛拖车，RMB/单                    #inland_fee  # 人民币，整单 
CUSTOMS_FEE = 500.0    # 报关+单证，RMB/单
PORT_FEE = 800.0       # 港杂+装船，RMB/单
BANK_FEE = 200.0       # T/T 电汇，RMB/笔

def rebate(cost_cny, qty):
    cost_total_cny = cost_cny * qty
    cost_tax_free_cny = cost_total_cny / (1+VAT_IN )#
    cost_refund_cny=cost_tax_free_cny * REBATE_RATE
    return round(cost_refund_cny, 2)
#print(rebate(226, 50))                       #rebate  退税的钱


def fob_profit(fob_usd, cost_cny, qty):
    income = fob_usd * qty * USD_CNY                              #美元数 *数量 *汇率    人民币
    total_amount = cost_cny * qty                                 #采购消费 = 人民币 * 数量
    refund_amount = rebate(cost_cny, qty)                         #退税 = rebate 函数
    up_amount= INLAND_FEE + CUSTOMS_FEE + PORT_FEE + BANK_FEE     #国内杂费 = 内地 人工 发货 电汇
    all_amount = total_amount - refund_amount + up_amount         #全部费用

    profit =  income - all_amount                             #利润
    profit_single_amount=profit / qty                         #单件商品利润
    rate_of_profit=profit_single_amount / (fob_usd * USD_CNY)
    return round(profit_single_amount, 2), round(rate_of_profit * 100, 1)
profit, margin = fob_profit(20, 113, 500)




if __name__ == '__main__':
    print(rebate(226, 50))
    profit, margin = fob_profit(20, 113, 500)
    print(profit, margin)














