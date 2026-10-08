import math


# ============================================================
#  输入函数
# ============================================================

def get_value(name, description, is_rate=False):
    """
    询问用户一个变量的值。
    - 输入“未知”返回 None
    - is_rate=True 时，允许输入如 5% / 12.5% / -3%，自动转成小数
    """
    while True:
        raw = input(f"请输入 {name}（{description}），如果未知请输入“未知”：").strip()

        if raw in ("未知", "未知数", "不知道", "unknown", "?", "x", ""):
            return None

        if raw.endswith("%"):
            if not is_rate:
                print(f"输入无效：{name} 不是利率，不能使用百分号。")
                continue
            num_str = raw[:-1].strip()
            try:
                return float(num_str) / 100.0
            except ValueError:
                print("输入无效，百分号前必须是数字，例如 5% 或 12.5%。")
                continue

        try:
            val = float(raw)
        except ValueError:
            if is_rate:
                print("输入无效，请输入一个数字、百分数（如 5%）或“未知”。")
            else:
                print("输入无效，请输入一个数字或“未知”。")
            continue

        return val


# ============================================================
#  基础模式：F = P × (1 + i)^n
# ============================================================

def solve_i(F, P, n):
    """解 i，方程为 (1+i)^n = F/P，正确处理偶次方的双根"""
    if P == 0:
        return "无法计算 i：因为 P = 0，不能做分母。"

    ratio = F / P
    solutions = []

    if n % 2 == 1:
        if ratio >= 0:
            x = ratio ** (1 / n)
        else:
            x = -((-ratio) ** (1 / n))
        solutions.append(x)
    else:
        if ratio < 0:
            return "无法计算 i：F/P 为负数且 n 为偶数，实数范围内无解。"
        x_pos = ratio ** (1 / n)
        x_neg = -x_pos
        solutions.append(x_pos)
        if x_neg != x_pos:
            solutions.append(x_neg)

    i_values = [x - 1 for x in solutions]

    lines = [f"方程：(1 + i)^{n} = F / P = {F} / {P} = {ratio}"]
    lines.append(f"求解：1 + i = ±({ratio})^(1/{n})")
    lines.append("结果：")
    for idx, iv in enumerate(i_values, 1):
        lines.append(f"  解 {idx}: i = {iv:.6f}  （即 {iv * 100:.4f}%）")

    if len(i_values) > 1:
        lines.append("")
        lines.append("说明：n 为偶数时，方程有两个数学解。")
        lines.append("      其中使 i < -100% 的解在金融上通常无意义。")

    valid = [iv for iv in i_values if iv > -1]
    if valid:
        lines.append("")
        lines.append("金融上有意义的解（i > -100%）：")
        for iv in valid:
            lines.append(f"  i = {iv:.6f}  （即 {iv * 100:.4f}%）")

    return "\n".join(lines)


def solve_basic(F, P, i, n):
    """基础模式求解，返回 (结果字符串, 是否成功)"""
    unknowns = [name for name, val in
                [("F", F), ("P", P), ("i", i), ("n", n)] if val is None]

    if len(unknowns) == 0:
        return "所有变量均已知，无需计算。", True
    if len(unknowns) > 1:
        return f"未知变量过多（{', '.join(unknowns)}），无法计算。", False

    target = unknowns[0]

    try:
        if target == "F":
            result = P * (1 + i) ** n
            return (f"F = P × (1 + i)^n = {P} × (1 + {i})^{n} "
                    f"= {result:.6f}", True)

        elif target == "P":
            if (1 + i) == 0:
                return "无法计算 P：因为 (1 + i) = 0，不能做分母。", False
            result = F / ((1 + i) ** n)
            return (f"P = F / (1 + i)^n = {F} / (1 + {i})^{n} "
                    f"= {result:.6f}", True)

        elif target == "i":
            return solve_i(F, P, n), True

        elif target == "n":
            if P == 0:
                return "无法计算 n：因为 P = 0，不能做分母。", False
            if F / P <= 0:
                return "无法计算 n：F/P 必须为正数才能取对数。", False
            if (1 + i) <= 0:
                return "无法计算 n：1 + i 必须为正数才能取对数。", False
            result = math.log(F / P) / math.log(1 + i)
            return (f"n = ln(F/P) / ln(1 + i) = "
                    f"ln({F}/{P}) / ln(1 + {i}) = {result:.6f}", True)

    except Exception as e:
        return f"计算过程中出现错误：{e}", False


# ============================================================
#  EAR 模式：迭代求解
# ============================================================

def solve_ear_mode(F, P, R, M, EAR, t):
    """EAR 模式迭代求解。变量：F, P, R, M, EAR, t"""
    values = {"F": F, "P": P, "R": R, "M": M, "EAR": EAR, "t": t}
    steps = []

    MAX_ITER = 10
    for _ in range(MAX_ITER):
        progress = False

        if values["EAR"] is None and values["R"] is not None and values["M"] is not None:
            if values["M"] != 0:
                ear = (1 + values["R"] / values["M"]) ** values["M"] - 1
                values["EAR"] = ear
                steps.append(
                    f"EAR = (1 + R/M)^M - 1 = "
                    f"(1 + {values['R']}/{values['M']})^{values['M']} - 1 "
                    f"= {ear:.6f}  （即 {ear*100:.4f}%）"
                )
                progress = True

        if values["R"] is None and values["EAR"] is not None and values["M"] is not None:
            if values["M"] != 0 and values["EAR"] > -1:
                r = values["M"] * ((1 + values["EAR"]) ** (1 / values["M"]) - 1)
                values["R"] = r
                steps.append(
                    f"R = M × [(1+EAR)^(1/M) - 1] = "
                    f"{values['M']} × [(1+{values['EAR']})^(1/{values['M']}) - 1] "
                    f"= {r:.6f}  （即 {r*100:.4f}%）"
                )
                progress = True

        if values["F"] is None and values["P"] is not None:
            if values["EAR"] is not None and values["t"] is not None:
                f_val = values["P"] * (1 + values["EAR"]) ** values["t"]
                values["F"] = f_val
                steps.append(
                    f"F = P × (1+EAR)^t = {values['P']} × "
                    f"(1+{values['EAR']})^{values['t']} = {f_val:.6f}"
                )
                progress = True
            elif (values["R"] is not None and values["M"] is not None
                  and values["t"] is not None):
                i = values["R"] / values["M"]
                n = values["M"] * values["t"]
                f_val = values["P"] * (1 + i) ** n
                values["F"] = f_val
                steps.append(
                    f"F = P × (1+R/M)^(Mt) = {values['P']} × "
                    f"(1+{values['R']}/{values['M']})^"
                    f"({values['M']}×{values['t']}) = {f_val:.6f}"
                )
                progress = True

        if values["P"] is None and values["F"] is not None:
            if values["EAR"] is not None and values["t"] is not None:
                if (1 + values["EAR"]) != 0:
                    p_val = values["F"] / (1 + values["EAR"]) ** values["t"]
                    values["P"] = p_val
                    steps.append(
                        f"P = F / (1+EAR)^t = {values['F']} / "
                        f"(1+{values['EAR']})^{values['t']} = {p_val:.6f}"
                    )
                    progress = True
            elif (values["R"] is not None and values["M"] is not None
                  and values["t"] is not None):
                if (1 + values["R"] / values["M"]) != 0:
                    i = values["R"] / values["M"]
                    n = values["M"] * values["t"]
                    p_val = values["F"] / (1 + i) ** n
                    values["P"] = p_val
                    steps.append(
                        f"P = F / (1+R/M)^(Mt) = {values['F']} / "
                        f"(1+{values['R']}/{values['M']})^"
                        f"({values['M']}×{values['t']}) = {p_val:.6f}"
                    )
                    progress = True

        if values["t"] is None and values["F"] is not None and values["P"] is not None:
            if values["P"] != 0 and values["F"] / values["P"] > 0:
                if values["EAR"] is not None and (1 + values["EAR"]) > 0:
                    t_val = math.log(values["F"] / values["P"]) / math.log(1 + values["EAR"])
                    values["t"] = t_val
                    steps.append(
                        f"t = ln(F/P) / ln(1+EAR) = "
                        f"ln({values['F']}/{values['P']}) / "
                        f"ln(1+{values['EAR']}) = {t_val:.6f} 年"
                    )
                    progress = True
                elif (values["R"] is not None and values["M"] is not None
                      and (1 + values["R"] / values["M"]) > 0):
                    n_val = math.log(values["F"] / values["P"]) / math.log(1 + values["R"] / values["M"])
                    t_val = n_val / values["M"]
                    values["t"] = t_val
                    steps.append(
                        f"n = ln(F/P) / ln(1+R/M) = {n_val:.6f}，"
                        f"t = n / M = {n_val:.6f} / {values['M']} = {t_val:.6f} 年"
                    )
                    progress = True

        if not progress:
            break

    remaining = [k for k, v in values.items() if v is None]

    if remaining:
        msg = f"未知变量过多（{', '.join(remaining)}），无法计算。"
        if steps:
            msg += "\n\n已完成的步骤：\n" + "\n".join(f"  {s}" for s in steps)
        return msg, False

    output = "求解过程：\n" + "\n".join(f"  {s}" for s in steps)
    output += "\n\n最终结果：\n"
    for k, v in values.items():
        if k in ("R", "EAR"):
            output += f"  {k:4s} = {v:.6f}  （即 {v*100:.4f}%）\n"
        else:
            output += f"  {k:4s} = {v:.6f}\n"
    return output, True


# ============================================================
#  连续复利模式：F = P × e^(rt)
# ============================================================

def solve_continuous_mode(F, P, r, t):
    """连续复利模式迭代求解。变量：F, P, r, t"""
    values = {"F": F, "P": P, "r": r, "t": t}
    steps = []

    MAX_ITER = 10
    for _ in range(MAX_ITER):
        progress = False

        if values["F"] is None and values["P"] is not None \
                and values["r"] is not None and values["t"] is not None:
            f_val = values["P"] * math.exp(values["r"] * values["t"])
            values["F"] = f_val
            steps.append(
                f"F = P × e^(rt) = {values['P']} × "
                f"e^({values['r']}×{values['t']}) = {f_val:.6f}"
            )
            progress = True

        if values["P"] is None and values["F"] is not None \
                and values["r"] is not None and values["t"] is not None:
            p_val = values["F"] * math.exp(-values["r"] * values["t"])
            values["P"] = p_val
            steps.append(
                f"P = F × e^(-rt) = {values['F']} × "
                f"e^(-{values['r']}×{values['t']}) = {p_val:.6f}"
            )
            progress = True

        if values["r"] is None and values["F"] is not None \
                and values["P"] is not None and values["t"] is not None:
            if values["P"] != 0 and values["F"] / values["P"] > 0 and values["t"] != 0:
                r_val = math.log(values["F"] / values["P"]) / values["t"]
                values["r"] = r_val
                steps.append(
                    f"r = ln(F/P) / t = "
                    f"ln({values['F']}/{values['P']}) / {values['t']} "
                    f"= {r_val:.6f}  （即 {r_val*100:.4f}%）"
                )
                progress = True

        if values["t"] is None and values["F"] is not None \
                and values["P"] is not None and values["r"] is not None:
            if values["P"] != 0 and values["F"] / values["P"] > 0 and values["r"] != 0:
                t_val = math.log(values["F"] / values["P"]) / values["r"]
                values["t"] = t_val
                steps.append(
                    f"t = ln(F/P) / r = "
                    f"ln({values['F']}/{values['P']}) / {values['r']} "
                    f"= {t_val:.6f} 年"
                )
                progress = True

        if not progress:
            break

    remaining = [k for k, v in values.items() if v is None]

    if remaining:
        msg = f"未知变量过多（{', '.join(remaining)}），无法计算。"
        if steps:
            msg += "\n\n已完成的步骤：\n" + "\n".join(f"  {s}" for s in steps)
        return msg, False

    output = "求解过程：\n" + "\n".join(f"  {s}" for s in steps)
    output += "\n\n最终结果：\n"
    for k, v in values.items():
        if k == "r":
            output += f"  {k:4s} = {v:.6f}  （即 {v*100:.4f}%）\n"
        else:
            output += f"  {k:4s} = {v:.6f}\n"
    return output, True


# ============================================================
#  普通年金模式（后付年金）
# ============================================================

def annuity_fv(A, i, n):
    """普通年金终值：F = A × [((1+i)^n - 1) / i]"""
    if i == 0:
        return A * n
    return A * ((1 + i) ** n - 1) / i


def annuity_pv(A, i, n):
    """普通年金现值：P = A × [1 - (1+i)^(-n)] / i"""
    if i == 0:
        return A * n
    return A * (1 - (1 + i) ** (-n)) / i


def solve_annuity_i(target, known, fixed_value):
    """
    数值求解普通年金的利率 i。
    - target: 'F' 表示用终值公式，'P' 表示用现值公式
    - known: 已知的 A 和 n
    - fixed_value: 已知的 F 或 P
    用二分法在 (-0.9999, 10) 区间内搜索。
    """
    A = known["A"]
    n = known["n"]

    def func(i):
        if target == "F":
            return annuity_fv(A, i, n) - fixed_value
        else:
            return annuity_pv(A, i, n) - fixed_value

    # 搜索区间：i ∈ (-0.9999, 10)
    lo, hi = -0.9999, 10.0
    f_lo, f_hi = func(lo), func(hi)

    if f_lo * f_hi > 0:
        return None, "在合理利率范围内找不到满足条件的 i。"

    for _ in range(200):
        mid = (lo + hi) / 2
        f_mid = func(mid)
        if f_lo * f_mid <= 0:
            hi = mid
            f_hi = f_mid
        else:
            lo = mid
            f_lo = f_mid

    return (lo + hi) / 2, None


def solve_annuity_mode(mode, A, i, n, F, P):
    """
    普通年金模式迭代求解。
    - mode: 'FV' 表示用终值公式 F = A × [((1+i)^n - 1) / i]
            'PV' 表示用现值公式 P = A × [1 - (1+i)^(-n)] / i
    - 变量：A, i, n, F（或 P）
    """
    if mode == "FV":
        values = {"A": A, "i": i, "n": n, "F": F}
        target_name = "F"
    else:
        values = {"A": A, "i": i, "n": n, "P": P}
        target_name = "P"

    steps = []

    MAX_ITER = 10
    for _ in range(MAX_ITER):
        progress = False

        # ---------- 求终值 F 或现值 P ----------
        if mode == "FV" and values["F"] is None:
            if values["A"] is not None and values["i"] is not None and values["n"] is not None:
                f_val = annuity_fv(values["A"], values["i"], values["n"])
                values["F"] = f_val
                if values["i"] == 0:
                    steps.append(
                        f"F = A × n = {values['A']} × {values['n']} = {f_val:.6f}（i = 0 特例）"
                    )
                else:
                    steps.append(
                        f"F = A × [((1+i)^n - 1) / i] = {values['A']} × "
                        f"[((1+{values['i']})^{values['n']} - 1) / {values['i']}] "
                        f"= {f_val:.6f}"
                    )
                progress = True

        if mode == "PV" and values["P"] is None:
            if values["A"] is not None and values["i"] is not None and values["n"] is not None:
                p_val = annuity_pv(values["A"], values["i"], values["n"])
                values["P"] = p_val
                if values["i"] == 0:
                    steps.append(
                        f"P = A × n = {values['A']} × {values['n']} = {p_val:.6f}（i = 0 特例）"
                    )
                else:
                    steps.append(
                        f"P = A × [1 - (1+i)^(-n)] / i = {values['A']} × "
                        f"[1 - (1+{values['i']})^(-{values['n']})] / {values['i']} "
                        f"= {p_val:.6f}"
                    )
                progress = True

        # ---------- 求年金 A ----------
        if values["A"] is None:
            if mode == "FV" and values["F"] is not None \
                    and values["i"] is not None and values["n"] is not None:
                if values["i"] == 0:
                    a_val = values["F"] / values["n"]
                    values["A"] = a_val
                    steps.append(
                        f"A = F / n = {values['F']} / {values['n']} = {a_val:.6f}（i = 0 特例）"
                    )
                    progress = True
                else:
                    denom = (1 + values["i"]) ** values["n"] - 1
                    if denom != 0:
                        a_val = values["F"] * values["i"] / denom
                        values["A"] = a_val
                        steps.append(
                            f"A = F × i / [(1+i)^n - 1] = {values['F']} × {values['i']} / "
                            f"[(1+{values['i']})^{values['n']} - 1] = {a_val:.6f}"
                        )
                        progress = True

            if mode == "PV" and values["P"] is not None \
                    and values["i"] is not None and values["n"] is not None:
                if values["i"] == 0:
                    a_val = values["P"] / values["n"]
                    values["A"] = a_val
                    steps.append(
                        f"A = P / n = {values['P']} / {values['n']} = {a_val:.6f}（i = 0 特例）"
                    )
                    progress = True
                else:
                    denom = 1 - (1 + values["i"]) ** (-values["n"])
                    if denom != 0:
                        a_val = values["P"] * values["i"] / denom
                        values["A"] = a_val
                        steps.append(
                            f"A = P × i / [1 - (1+i)^(-n)] = {values['P']} × {values['i']} / "
                            f"[1 - (1+{values['i']})^(-{values['n']})] = {a_val:.6f}"
                        )
                        progress = True

        # ---------- 求期数 n ----------
        if values["n"] is None and values["A"] is not None and values["i"] is not None:
            if values["i"] == 0:
                # i = 0 时，F = A×n 或 P = A×n
                if mode == "FV" and values["F"] is not None:
                    n_val = values["F"] / values["A"]
                    values["n"] = n_val
                    steps.append(
                        f"n = F / A = {values['F']} / {values['A']} = {n_val:.6f}（i = 0 特例）"
                    )
                    progress = True
                elif mode == "PV" and values["P"] is not None:
                    n_val = values["P"] / values["A"]
                    values["n"] = n_val
                    steps.append(
                        f"n = P / A = {values['P']} / {values['A']} = {n_val:.6f}（i = 0 特例）"
                    )
                    progress = True
            else:
                if mode == "FV" and values["F"] is not None:
                    inner = 1 + values["F"] * values["i"] / values["A"]
                    if inner > 0 and (1 + values["i"]) > 0:
                        n_val = math.log(inner) / math.log(1 + values["i"])
                        values["n"] = n_val
                        steps.append(
                            f"n = ln(1 + F·i/A) / ln(1+i) = "
                            f"ln(1 + {values['F']}×{values['i']}/{values['A']}) / "
                            f"ln(1+{values['i']}) = {n_val:.6f}"
                        )
                        progress = True
                elif mode == "PV" and values["P"] is not None:
                    inner = 1 - values["P"] * values["i"] / values["A"]
                    if inner > 0 and (1 + values["i"]) > 0:
                        n_val = -math.log(inner) / math.log(1 + values["i"])
                        values["n"] = n_val
                        steps.append(
                            f"n = -ln(1 - P·i/A) / ln(1+i) = "
                            f"-ln(1 - {values['P']}×{values['i']}/{values['A']}) / "
                            f"ln(1+{values['i']}) = {n_val:.6f}"
                        )
                        progress = True

        # ---------- 求利率 i（数值法） ----------
        if values["i"] is None and values["A"] is not None and values["n"] is not None:
            fixed_value = values["F"] if mode == "FV" else values["P"]
            if fixed_value is not None:
                i_val, err = solve_annuity_i(
                    "F" if mode == "FV" else "P",
                    {"A": values["A"], "n": values["n"]},
                    fixed_value
                )
                if i_val is not None:
                    values["i"] = i_val
                    steps.append(
                        f"i 由数值法求解（二分法）：i = {i_val:.6f}  "
                        f"（即 {i_val*100:.4f}%）"
                    )
                    progress = True
                else:
                    steps.append(f"i 求解失败：{err}")
                    # 标记为特殊值，避免无限循环
                    values["i"] = float("nan")
                    progress = True

        if not progress:
            break

    remaining = [k for k, v in values.items() if v is None]

    if remaining:
        msg = f"未知变量过多（{', '.join(remaining)}），无法计算。"
        if steps:
            msg += "\n\n已完成的步骤：\n" + "\n".join(f"  {s}" for s in steps)
        return msg, False

    output = "求解过程：\n" + "\n".join(f"  {s}" for s in steps)
    output += "\n\n最终结果：\n"
    for k, v in values.items():
        if k == "i":
            output += f"  {k:4s} = {v:.6f}  （即 {v*100:.4f}%）\n"
        else:
            output += f"  {k:4s} = {v:.6f}\n"
    return output, True


# ============================================================
#  主程序
# ============================================================

def main():
    print("=" * 60)
    print("  复利与年金计算器")
    print("  模式 1（基础）：    F = P × (1 + i)^n")
    print("  模式 2（EAR）：     EAR = (1 + R/M)^M - 1，F = P × (1 + EAR)^t")
    print("  模式 3（连续复利）：F = P × e^(rt)")
    print("  模式 4（普通年金）：F = A × [((1+i)^n - 1) / i]")
    print("                      P = A × [1 - (1+i)^(-n)] / i")
    print("=" * 60)
    print("请选择模式：")
    print("  1 - 基础模式（F, P, i, n）")
    print("  2 - EAR 模式（F, P, R, M, EAR, t）")
    print("  3 - 连续复利模式（F, P, r, t）")
    print("  4 - 普通年金模式（A, i, n, F 或 P）")
    print()
    print("提示：利率类变量可以直接输入百分数，例如 5% 或 12.5%")

    while True:
        mode = input("请输入 1、2、3 或 4：").strip()
        if mode in ("1", "2", "3", "4"):
            break
        print("输入无效，请输入 1、2、3 或 4。")

    print()
    if mode == "1":
        F = get_value("F", "终值/未来值")
        P = get_value("P", "现值/本金")
        i = get_value("i", "每期利率，可输入 0.05 或 5%", is_rate=True)
        n = get_value("n", "期数")
        print("\n" + "-" * 60)
        result, ok = solve_basic(F, P, i, n)

    elif mode == "2":
        print("提示：")
        print("  R   = 名义年利率，可输入 0.12 或 12%")
        print("  M   = 每年复利次数，例如 12 表示按月复利")
        print("  EAR = 有效年利率，可输入 0.1268 或 12.68%")
        print("  t   = 年数，例如 2 表示 2 年")
        print("  未知的请输入“未知”。\n")

        F   = get_value("F",   "终值/未来值")
        P   = get_value("P",   "现值/本金")
        R   = get_value("R",   "名义年利率，可输入 0.12 或 12%", is_rate=True)
        M   = get_value("M",   "每年复利次数")
        EAR = get_value("EAR", "有效年利率，可输入 0.1268 或 12.68%", is_rate=True)
        t   = get_value("t",   "年数")
        print("\n" + "-" * 60)
        result, ok = solve_ear_mode(F, P, R, M, EAR, t)

    elif mode == "3":
        print("提示：")
        print("  r = 连续复利利率，可输入 0.05 或 5%")
        print("  t = 年数，例如 2 表示 2 年")
        print("  未知的请输入“未知”。\n")

        F = get_value("F", "终值/未来值")
        P = get_value("P", "现值/本金")
        r = get_value("r", "连续复利利率，可输入 0.05 或 5%", is_rate=True)
        t = get_value("t", "年数")
        print("\n" + "-" * 60)
        result, ok = solve_continuous_mode(F, P, r, t)

    else:
        print("请选择年金计算类型：")
        print("  1 - 终值型：F = A × [((1+i)^n - 1) / i]")
        print("  2 - 现值型：P = A × [1 - (1+i)^(-n)] / i")
        while True:
            sub = input("请输入 1 或 2：").strip()
            if sub in ("1", "2"):
                break
            print("输入无效，请输入 1 或 2。")

        print("\n提示：")
        print("  A = 年金（每期期末等额收付的金额）")
        print("  i = 每期利率，可输入 0.05 或 5%")
        print("  n = 期数")
        print("  未知的请输入“未知”。\n")

        A = get_value("A", "年金（每期金额）")
        i = get_value("i", "每期利率，可输入 0.05 或 5%", is_rate=True)
        n = get_value("n", "期数")

        if sub == "1":
            F = get_value("F", "年金终值")
            P = None
            mode_str = "FV"
        else:
            P = get_value("P", "年金现值")
            F = None
            mode_str = "PV"

        print("\n" + "-" * 60)
        result, ok = solve_annuity_mode(mode_str, A, i, n, F, P)

    print(result)
    print("-" * 60)


if __name__ == "__main__":
    main()