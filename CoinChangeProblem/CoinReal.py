class CoinReal:
    def __init__(self, coins, counts):
        """
        :param coins: List of coin denominations (e.g. [1, 3, 4])
        :param counts: List of how many of each coin you have (e.g. [2, 1, 1])
        """
        self.coins = coins
        self.counts = counts

    def limited_min_coins(self, target):
        """
        Try to reach the target using only the limited number of coins available.
        :param target: Amount to make
        :return: Tuple (list of coins used, total coins used), or None if impossible
        """
        # TODO: implement bounded dynamic programming or DFS with pruning
        return None
