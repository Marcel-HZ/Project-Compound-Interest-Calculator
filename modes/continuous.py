"""模式 3：连续复利  F = P × e^(rt)"""
import math
from utils import get_value


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


def run():
    """交互式运行连续复利模式"""
    print("连续复利模式：F = P × e^(rt)")
    print("提示：")
    print("  r = 连续复利利率，可输入 0.05 或 5%")
    print("  t = 年数，例如 2 表示 2 年")
    print("  未知的请输入“未知”。\n")

    F = get_value("F", "终值/未来值")
    P = get_value("P", "现值/本金")
    r = get_value("r", "连续复利利率，可输入 0.05 或 5%", is_rate=True)
    t = get_value("t", "年数")
    print("\n" + "-" * 60)
    result, _ = solve_continuous_mode(F, P, r, t)
    print(result)
    print("-" * 60)