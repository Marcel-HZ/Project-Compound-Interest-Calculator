from modes import investment

cashflows = [5, 15, 30, 30, 30, 15, 10]
init = 100
r = 0.075

# 1. 回收期
pb, _ = investment.calc_payback(cashflows, init)
print(f"回收期 = {pb:.6f} 年")          # 期望 4.666667

# 2. 贴现回收期
dpb, _ = investment.calc_discounted_payback(cashflows, init, r)
print(f"贴现回收期 = {dpb:.6f} 年")      # 期望 6.8526

# 3. NPV
npv, pv = investment.calc_npv(cashflows, init, r)
print(f"PV = {pv:.6f}")                  # 期望 100.8883
print(f"NPV = {npv:.6f}")                # 期望 0.8883

# 4. IRR
irr, _ = investment.calc_irr(cashflows, init)
print(f"IRR = {irr:.6f} ({irr*100:.4f}%)")  # 期望 0.0774

# 5. 等额现金流 NPV（年金现值 - 初始投资）
A = 20
n = 7
pv_annuity = A * (1 - (1 + r) ** (-n)) / r
npv_level = pv_annuity - init
print(f"标准金流量 NPV = {npv_level:.6f}")  # 期望 5.9320

# 6. XNPV
from datetime import datetime
dates = [
    datetime(2002, 12, 31),
    datetime(2003, 12, 31),
    datetime(2004, 6, 30),
    datetime(2004, 12, 31),
    datetime(2005, 3, 31),
    datetime(2005, 6, 30),
    datetime(2005, 9, 30),
    datetime(2005, 12, 31),
]
cashflows_x = [-100, 5, 15, 30, 30, 30, 15, 10]
xnpv, _ = investment.calc_xnpv(cashflows_x, dates, r)
print(f"XNPV = {xnpv:.6f}")              # 期望约 14.97

# 7. AAR（用净利润，不是现金流）
# 如果表格 5% 对应某个净利润序列，需要用户提供
# 例如若每年净利润都是 5，则 AAR = 5/100 = 5%
profits = [5, 5, 5, 5, 5, 5, 5]
aar, _ = investment.calc_aar(profits, init)
print(f"AAR = {aar:.6f} ({aar*100:.4f}%)")  # 期望 0.050000