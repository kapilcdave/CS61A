def strategy1(n):
    """Strategy for player 1 (computer)"""
    if n % 3 == 0:
        return 1
    else:
        return n % 3

def strategy2(n):
    """Strategy for player 2 (human)"""
    while True:
        choice = int(input(f"Player 2: {n} stones left. Take 1 or 2? "))
        if choice in [1, 2] and choice <= n:
            return choice
        print("Invalid choice. You must take 1 or 2 stones.")

def play(n):
    """Play the take 1 or 2 from ten game. Last player to take wins."""
    who = 1
    while n > 0:
        print(f"\nPlayer {who}'s turn. {n} stones left.")
        if who == 1:
            take = strategy1(n)
            print(f"Player 1 takes {take} stone(s).")
        elif who == 2:
            take = strategy2(n)
            print(f"Player 2 takes {take} stone(s).")
        else:
            print("Error in play")
            return
        n = n - take
    print(f"\nPlayer {who} wins!")
    return who

if __name__ == "__main__":
    play(10)
