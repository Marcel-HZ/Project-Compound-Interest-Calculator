"""模式 1：基础复利  F = P × (1 + i)^n"""
import math
from utils import get_value


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


def run():
    """交互式运行基础模式"""
    print("基础复利模式：F = P × (1 + i)^n")
    F = get_value("F", "终值/未来值")
    P = get_value("P", "现值/本金")
    i = get_value("i", "每期利率，可输入 0.05 或 5%", is_rate=True)
    n = get_value("n", "期数")
    print("\n" + "-" * 60)
    result, _ = solve_basic(F, P, i, n)
    print(result)
    print("-" * 60)