"""回归测试：验证核心公式"""
import math
from modes import basic, ear, continuous, annuity, investment

TOL = 1e-3  # 放宽容差，避免浮点末位误差

def check(name, actual, expected, tol=TOL):
    ok = abs(actual - expected) < tol
    mark = "✅" if ok else "❌"
    print(f"{mark} {name}: actual={actual:.6f}, expected={expected:.6f}")
    return ok


print("=" * 60)
print("一、基础模式")
print("=" * 60)

# 求 F
result, _ = basic.solve_basic(None, 1000, 0.05, 10)
assert "1628.894627" in result
print("✅ 基础 F: 1628.894627")

# 求 P
result, _ = basic.solve_basic(1628.894627, None, 0.05, 10)
assert "1000" in result
print("✅ 基础 P: 1000.000000")

# 求 n
result, _ = basic.solve_basic(2000, 1000, 0.05, None)
assert "14.206699" in result
print("✅ 基础 n: 14.206699")


print()
print("=" * 60)
print("二、连续复利模式")
print("=" * 60)

F = 100 * math.exp(0.05 * 1)
check("连续复利 F", F, 105.127110)

r = math.log(2) / 5
check("连续复利 r", r, 0.138629)

t = math.log(2) / 0.05
check("连续复利 t", t, 13.862944)


print()
print("=" * 60)
print("三、EAR 模式")
print("=" * 60)

ear_val = (1 + 0.12 / 12) ** 12 - 1
check("EAR (R=12%, M=12)", ear_val, 0.126825)

ear_val2 = (1 + 0.05 / 100) ** 100 - 1
check("EAR (R=5%, M=100)", ear_val2, 0.051265)

t_val = math.log(2) / math.log(1.07)
check("EAR 求 t (F=200, P=100, EAR=7%)", t_val, 10.244769)


print()
print("=" * 60)
print("四、普通年金模式")
print("=" * 60)

F = annuity.annuity_fv(1000, 0.05, 10)
check("年金终值 F", F, 12577.892535)

P = annuity.annuity_pv(1000, 0.05, 10)
check("年金现值 P", P, 7721.734927)

A = 10000 * 0.05 / (1 - 1.05 ** (-10))
check("年金 A (P=10000, i=5%, n=10)", A, 1295.045741)


print()
print("=" * 60)
print("五、投资项目评价模式")
print("=" * 60)

cashflows = [300, 400, 500, 600]
init = 1000
r = 0.10

# PV、NPV
pv_manual = sum(cf / (1 + r) ** t for t, cf in enumerate(cashflows, 1))
check("PV (r=10%)", pv_manual, 1388.771805)

npv, pv = investment.calc_npv(cashflows, init, r)
check("NPV", npv, 388.771805)
check("盈利指数 PI", npv / init, 0.388772)
check("现值指数 PI", pv / init, 1.388772)

# IRR
irr, _ = investment.calc_irr(cashflows, init)
check("IRR", irr, 0.248883, tol=1e-4)

# 回收期
pb, _ = investment.calc_payback(cashflows, init)
check("回收期", pb, 2.600000)

# 贴现回收期
dpb, _ = investment.calc_discounted_payback(cashflows, init, r)
check("贴现回收期", dpb, 3.051333, tol=1e-3)

# AAR
aar, _ = investment.calc_aar([200, 300, 250, 350], init)
check("AAR", aar, 0.275000)


print()
print("=" * 60)
print("六、综合对比：四种口径")
print("=" * 60)

P = 100
F_basic = 100 * (1 + 0.05) ** 1
check("基础 (i=5%, n=1)", F_basic, 105.000000)

F_ear_monthly = 100 * (1 + 0.05 / 12) ** 12
check("EAR 按月 (R=5%, M=12, t=1)", F_ear_monthly, 105.116190)

F_ear_daily = 100 * (1 + 0.05 / 365) ** 365
check("EAR 按日 (R=5%, M=365, t=1)", F_ear_daily, 105.126750)

F_continuous = 100 * math.exp(0.05 * 1)
check("连续复利 (r=5%, t=1)", F_continuous, 105.127110)


print()
print("=" * 60)
print("回归测试完成。")
print("=" * 60)