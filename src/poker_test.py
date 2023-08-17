from PokerRule import PokerGroup, PokerCard
from TexasHoldem import PokerCardType


class Player:
    def __init__(self, account: str, hand_stack: list):
        self._account = account
        self._hand_stack = PokerGroup(hand_stack)

    def show_hand(self, as_class=False):
        return self._hand_stack.content(as_class)

    @property
    def win(self):
        print(f'{self._account} 獲勝')
        return self._account


class ClassicPokerGame:
    def __init__(self, players: list, hand_number=5):
        self.players = players
        self.player_num = 4
        self.hand_number = hand_number
        self.stage = 0
        self.dealer_stack = PokerGroup()

    def next_stage(self):
        self.stage += 1
        self.swift_stage()

    def swift_stage(self):
        if self.stage == 1:
            self.game_start()

    def game_start(self):
        """
        遊戲開始
        :return:
        """
        print('遊戲開始')
        self.player_num = len(self.players)
        print(f'玩家人數: {self.player_num} 人')
        self.dealer_stack.fill_card_group(is_shuffle=True)


if __name__ == '__main__':
    # 荷官生成牌
    dealer_stack = PokerGroup()
    dealer_stack.fill_card_group(is_shuffle=True)
    player1 = Player(account='player1', hand_stack=dealer_stack.draw(5))
    player2 = Player(account='player2', hand_stack=dealer_stack.draw(5))
    print(player1.show_hand())
    sort_list = PokerCardType(player1.show_hand(as_class=True), as_class=False)
    print(sort_list.check)
