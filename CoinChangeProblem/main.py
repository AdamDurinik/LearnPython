import sys

from CoinChangeProblem.CoinSimple import CoinSimple
from CoinChangeProblem.CoinAll import CoinAll
from CoinChangeProblem.CoinReal import CoinReal

def parse_coin_input(s):
    return list(map(int, s.strip().split()))

def part_one():
    coins = parse_coin_input(input("Enter coin denominations (space-separated): "))
    target = int(input("Enter target amount: "))
    solver = CoinSimple(coins)
    result = solver.min_coins(target)
    print(f"Minimum coins needed: {result}")

def part_two():
    coins = parse_coin_input(input("Enter coin denominations (space-separated): "))
    target = int(input("Enter target amount: "))
    solver = CoinAll(coins)
    combinations = solver.all_combinations(target)
    print("Possible combinations:")
    for combo in combinations:
        print(" + ".join(map(str, combo)))

def part_three():
    coins = parse_coin_input(input("Enter coin denominations (space-separated): "))
    counts = parse_coin_input(input("Enter available counts (space-separated): "))
    target = int(input("Enter target amount: "))
    solver = CoinReal(coins, counts)
    result = solver.limited_min_coins(target)
    if result is None:
        print("Not possible.")
    else:
        used, total = result
        print(f"Used coins: {' + '.join(map(str, used))}")
        print(f"Total coins used: {total}")

def main():
    print("Select problem part:")
    print("1 - Minimum coins needed")
    print("2 - All combinations")
    print("3 - Limited coins")
    print("0 - Exit")

    while True:
        choice = input("Choice: ").strip()
        if choice == "1":
            part_one()
        elif choice == "2":
            part_two()
        elif choice == "3":
            part_three()
        elif choice == "0":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()