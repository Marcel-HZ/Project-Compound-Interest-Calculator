"""复利、年金与投资项目评价计算器 —— 统一入口"""
from modes import basic, ear, continuous, annuity, investment


def print_menu():
    print("=" * 60)
    print("  复利、年金与投资项目评价计算器")
    print("  模式 1（基础）：    F = P × (1 + i)^n")
    print("  模式 2（EAR）：     EAR = (1 + R/M)^M - 1")
    print("  模式 3（连续复利）：F = P × e^(rt)")
    print("  模式 4（普通年金）：F = A × [((1+i)^n - 1) / i]")
    print("  模式 5（投资项目）：NPV、IRR、PI、回收期等")
    print("=" * 60)
    print("请选择模式：")
    print("  1 - 基础模式（F, P, i, n）")
    print("  2 - EAR 模式（F, P, R, M, EAR, t）")
    print("  3 - 连续复利模式（F, P, r, t）")
    print("  4 - 普通年金模式（A, i, n, F 或 P）")
    print("  5 - 投资项目评价（NPV、IRR、PI、回收期等）")
    print("  0 - 退出")
    print()
    print("提示：利率类变量可以直接输入百分数，例如 5% 或 12.5%")


def main():
    while True:
        print_menu()
        mode = input("请输入 0-5：").strip()

        if mode == "0":
            print("再见！")
            break

        print()
        if mode == "1":
            basic.run()
        elif mode == "2":
            ear.run()
        elif mode == "3":
            continuous.run()
        elif mode == "4":
            annuity.run()
        elif mode == "5":
            investment.run()
        else:
            print("输入无效，请输入 0-5。")

        print()  # 空行分隔，便于下一轮


if __name__ == "__main__":
    main()