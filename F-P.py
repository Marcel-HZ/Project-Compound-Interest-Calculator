import math


def get_value(name, description):
    """询问用户一个变量的值，返回 float 或 None（表示未知）"""
    while True:
        raw = input(f"请输入 {name}（{description}），如果未知请输入“未知”：").strip()
        if raw in ("未知", "未知数", "不知道", "unknown", "?", ""):
            return None
        try:
            return float(raw)
        except ValueError:
            print("输入无效，请输入一个数字或“未知”。")


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
#  EAR 模式：EAR = (1 + R/M)^M - 1
#             F = P × (1 + EAR)^t
# ============================================================

def compute_ear(R, M):
    """由名义年利率 R 和复利次数 M 计算 EAR"""
    return (1 + R / M) ** M - 1


def solve_ear_mode(F, P, R, M, EAR, t):
    """
    EAR 模式求解。变量：F, P, R, M, EAR, t
    关系：
        EAR = (1 + R/M)^M - 1
        F   = P × (1 + EAR)^t
        F   = P × (1 + R/M)^(M×t)
    只允许一个未知量。
    """
    variables = {
        "F": F, "P": P, "R": R, "M": M, "EAR": EAR, "t": t
    }
    unknowns = [name for name, val in variables.items() if val is None]

    if len(unknowns) == 0:
        return "所有变量均已知，无需计算。", True
    if len(unknowns) > 1:
        return f"未知变量过多（{', '.join(unknowns)}），无法计算。", False

    target = unknowns[0]
    lines = []

    try:
        # ---------- 1. 直接求 EAR ----------
        if target == "EAR":
            if M == 0:
                return "无法计算 EAR：M 不能为 0。", False
            ear = compute_ear(R, M)
            lines.append(f"EAR = (1 + R/M)^M - 1")
            lines.append(f"    = (1 + {R}/{M})^{M} - 1")
            lines.append(f"    = {ear:.6f}  （即 {ear * 100:.4f}%）")
            return "\n".join(lines), True

        # ---------- 2. 求 R ----------
        if target == "R":
            if M == 0:
                return "无法计算 R：M 不能为 0。", False
            if EAR <= -1:
                return "无法计算 R：EAR 必须大于 -100%。", False
            r = M * ((1 + EAR) ** (1 / M) - 1)
            lines.append(f"R = M × [(1 + EAR)^(1/M) - 1]")
            lines.append(f"  = {M} × [(1 + {EAR})^(1/{M}) - 1]")
            lines.append(f"  = {r:.6f}  （即 {r * 100:.4f}%）")
            return "\n".join(lines), True

        # ---------- 3. 求 M ----------
        if target == "M":
            if R == 0:
                return "无法计算 M：R = 0 时 EAR 恒为 0，M 无法确定。", False
            if EAR <= -1:
                return "无法计算 M：EAR 必须大于 -100%。", False
            # 解 (1 + R/M)^M = 1 + EAR，无解析解，用数值法
            target_val = 1 + EAR

            def f(m):
                return (1 + R / m) ** m - target_val

            # 在 [0.1, 10000] 区间内二分搜索（M 连续值，实际应为整数）
            lo, hi = 0.1, 100000.0
            if f(lo) * f(hi) > 0:
                return ("无法计算 M：在合理范围内找不到满足条件的 M。"
                        "请检查 R 与 EAR 是否矛盾。"), False
            for _ in range(200):
                mid = (lo + hi) / 2
                if f(lo) * f(mid) <= 0:
                    hi = mid
                else:
                    lo = mid
            m_val = (lo + hi) / 2
            lines.append(f"由 (1 + R/M)^M = 1 + EAR 数值求解：")
            lines.append(f"  M ≈ {m_val:.6f}")
            lines.append(f"  提示：实际中 M 通常取整数（1/2/4/12/365 等），")
            lines.append(f"        请根据业务场景选择最接近的整数。")
            return "\n".join(lines), True

        # ---------- 4. 求 F ----------
        if target == "F":
            if EAR is not None and t is not None:
                f_val = P * (1 + EAR) ** t
                lines.append(f"F = P × (1 + EAR)^t")
                lines.append(f"  = {P} × (1 + {EAR})^{t}")
                lines.append(f"  = {f_val:.6f}")
            elif R is not None and M is not None and t is not None:
                i = R / M
                n = M * t
                f_val = P * (1 + i) ** n
                lines.append(f"F = P × (1 + R/M)^(M×t)")
                lines.append(f"  = {P} × (1 + {R}/{M})^({M}×{t})")
                lines.append(f"  = {f_val:.6f}")
            else:
                return ("无法计算 F：需要 (EAR 和 t) 或 (R、M 和 t) "
                        "中的一组。"), False
            return "\n".join(lines), True

        # ---------- 5. 求 P ----------
        if target == "P":
            if EAR is not None and t is not None:
                if (1 + EAR) == 0:
                    return "无法计算 P：1 + EAR = 0，不能做分母。", False
                p_val = F / ((1 + EAR) ** t)
                lines.append(f"P = F / (1 + EAR)^t")
                lines.append(f"  = {F} / (1 + {EAR})^{t}")
                lines.append(f"  = {p_val:.6f}")
            elif R is not None and M is not None and t is not None:
                if (1 + R / M) == 0:
                    return "无法计算 P：1 + R/M = 0，不能做分母。", False
                i = R / M
                n = M * t
                p_val = F / ((1 + i) ** n)
                lines.append(f"P = F / (1 + R/M)^(M×t)")
                lines.append(f"  = {F} / (1 + {R}/{M})^({M}×{t})")
                lines.append(f"  = {p_val:.6f}")
            else:
                return ("无法计算 P：需要 (EAR 和 t) 或 (R、M 和 t) "
                        "中的一组。"), False
            return "\n".join(lines), True

        # ---------- 6. 求 t ----------
        if target == "t":
            if EAR is not None:
                if P == 0:
                    return "无法计算 t：P = 0，不能做分母。", False
                if F / P <= 0:
                    return "无法计算 t：F/P 必须为正数才能取对数。", False
                if (1 + EAR) <= 0:
                    return "无法计算 t：1 + EAR 必须为正数才能取对数。", False
                t_val = math.log(F / P) / math.log(1 + EAR)
                lines.append(f"t = ln(F/P) / ln(1 + EAR)")
                lines.append(f"  = ln({F}/{P}) / ln(1 + {EAR})")
                lines.append(f"  = {t_val:.6f} 年")
            elif R is not None and M is not None:
                if P == 0:
                    return "无法计算 t：P = 0，不能做分母。", False
                if F / P <= 0:
                    return "无法计算 t：F/P 必须为正数才能取对数。", False
                if (1 + R / M) <= 0:
                    return "无法计算 t：1 + R/M 必须为正数才能取对数。", False
                n_val = math.log(F / P) / math.log(1 + R / M)
                t_val = n_val / M
                lines.append(f"n = ln(F/P) / ln(1 + R/M) = "
                             f"{n_val:.6f}")
                lines.append(f"t = n / M = {n_val:.6f} / {M} = "
                             f"{t_val:.6f} 年")
            else:
                return ("无法计算 t：需要 EAR 或 (R 和 M) 中的一组。"), False
            return "\n".join(lines), True

    except Exception as e:
        return f"计算过程中出现错误：{e}", False


# ============================================================
#  主程序
# ============================================================

def main():
    print("=" * 55)
    print("  复利计算器")
    print("  基础模式：F = P × (1 + i)^n")
    print("  EAR 模式：EAR = (1 + R/M)^M - 1，F = P × (1 + EAR)^t")
    print("=" * 55)
    print("请选择模式：")
    print("  1 - 基础模式（F, P, i, n）")
    print("  2 - EAR 模式（F, P, R, M, EAR, t）")

    while True:
        mode = input("请输入 1 或 2：").strip()
        if mode in ("1", "2"):
            break
        print("输入无效，请输入 1 或 2。")

    print()
    if mode == "1":
        F = get_value("F", "终值/未来值")
        P = get_value("P", "现值/本金")
        i = get_value("i", "每期利率，例如 0.05 表示 5%")
        n = get_value("n", "期数")
        print("\n" + "-" * 55)
        result, ok = solve_basic(F, P, i, n)
    else:
        print("提示：")
        print("  R   = 名义年利率，例如 0.12 表示 12%")
        print("  M   = 每年复利次数，例如 12 表示按月复利")
        print("  EAR = 有效年利率，例如 0.1268 表示 12.68%")
        print("  t   = 年数，例如 2 表示 2 年")
        print("  未知的请输入“未知”。\n")

        F   = get_value("F",   "终值/未来值")
        P   = get_value("P",   "现值/本金")
        R   = get_value("R",   "名义年利率")
        M   = get_value("M",   "每年复利次数")
        EAR = get_value("EAR", "有效年利率")
        t   = get_value("t",   "年数")
        print("\n" + "-" * 55)
        result, ok = solve_ear_mode(F, P, R, M, EAR, t)

    print(result)
    print("-" * 55)


if __name__ == "__main__":
    main()