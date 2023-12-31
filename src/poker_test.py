from enum import Enum
from time import sleep
from itertools import combinations
from PokerRule import PokerGroup, PokerCard
from TexasHoldem import TexasRule, CardTypeEnumCn, CardTypeEnum, CardTypeStageEnum, get_biggest_stack_type, judge_winner


class PlayerStatus(Enum):
    Alive = '1'
    Drop = '2'
    Allin = '3'
    Out = '4'


class Player:
    def __init__(self, account: str):
        self._account = account
        self._status = PlayerStatus.Alive
        self._hand_stack = PokerGroup()

    def get_card(self, card_list):
        self._hand_stack = PokerGroup(card_list)

    def set_drop(self):
        self._status = PlayerStatus.Drop

    def set_out(self):
        self._status = PlayerStatus.Out

    def set_allin(self):
        self._status = PlayerStatus.Allin

    def show_hand(self, as_class=False):
        return self._hand_stack.content(as_class)

    @property
    def name(self):
        return self._account

    @property
    def status(self):
        return self._status

    @property
    def win(self):
        print(f'{self._account} 獲勝')
        return self._account


class ClassicPokerGame:
    def __init__(self, _players: list, hand_number=5):
        self._players = _players
        self._player_num = 4
        self._hand_number = hand_number
        self._stage = 0
        self._dealer_stack = PokerGroup()
        self._appear_stack = PokerGroup()

    @property
    def dealer_stack(self):
        return self._dealer_stack.content()

    @property
    def appear_stack(self):
        return self._appear_stack.content()

    def next_stage(self):
        self._stage += 1
        self.swift_stage()

    def swift_stage(self):
        pass
        # if self._stage == 1:
        #     self.game_start()
        # elif self._stage == 2:
        #     self.deal_all()
        # elif self._stage == 3:
        #     self.add_appear_card(3)

    def game_start(self):
        """
        遊戲開始
        :return:
        """
        self._stage = 1
        # print('遊戲開始')
        self._player_num = len(self._players)
        # print(f'玩家人數: {self._player_num} 人')
        # for index, player in enumerate(self._players):
        # print(f'{index + 1} 號玩家: {player.name}')
        self._dealer_stack.fill_card_group(is_shuffle=True)
        # print('牌庫已重新整理')
        self.next_stage()

    def add_appear_round(self, add_num=1):
        """
        增加顯牌回合
        :param add_num:
        :return:
        """
        # print(f'--------增加 {add_num} 張顯牌--------')
        self.add_appear_card(add_num)
        # print(f'顯牌有: {self.appear_stack}')
        stronger = self.judge_player_winnable()
        # print(f'當前贏面大的是 {stronger.get("index")} 號玩家 {stronger.get("player").name}')
        return stronger

    def deal_specify(self, player_seat_num: int, deal_num=2):
        """
        指定發牌
        :param player_seat_num: 玩家座位號碼(1~X)
        :param deal_num: 發牌數量(預設2)
        :return:
        """
        specify_player = self.legal_number_player(player_seat_num)
        if not specify_player:
            return
        specify_player.get_card(self._dealer_stack.draw(deal_num))

    def legal_number_player(self, player_num) -> Player:
        """
        檢驗座位玩家的狀態
        :param player_num: 
        :return: 
        """
        if player_num > self._player_num or player_num < 1:
            print(f'{player_num} 號玩家不存在')
            return False
        specify_player = self._players[player_num - 1]
        if specify_player.status != PlayerStatus.Alive:
            reason = '棄牌' if specify_player.status == PlayerStatus.Drop else '出局' if \
                specify_player.status == PlayerStatus.Out else 'AllIn'
            print(f'{player_num} 號玩家已{reason} ,無法發牌')
            return False
        return specify_player

    def deal_all(self):
        """
        對在座存活玩家發牌
        :return:
        """
        for index, player in enumerate(self._players):
            if player.status == PlayerStatus.Alive:
                self.deal_specify(index + 1)
        self.next_stage()

    def add_appear_card(self, add_num=1):
        """
        增加顯牌
        :param add_num: 增加數量
        :return:
        """
        self._appear_stack.add(self._dealer_stack.draw(add_num))

    @staticmethod
    def C_function(original_list: list, sublist_length=5) -> list:
        """
        C函數 (CX取X)
        :param original_list: 總數
        :param sublist_length: 取數
        :return:
        """
        sub_lists = list(combinations(original_list, sublist_length))
        sub_lists = [list(sub_list) for sub_list in sub_lists]
        return sub_lists

    def card_check(self, player_num):
        """
        檢查手牌與顯牌的牌型，回傳最大組合
        :return:
        """
        specify_player = self.legal_number_player(player_num)
        if self._appear_stack.content():
            all_card_list = specify_player.show_hand(as_class=True) + self._appear_stack.content(as_class=True)
        else:
            all_card_list = specify_player.show_hand(as_class=True)
        sub_len = 5 if len(all_card_list) >= 5 else len(all_card_list)
        sub_card_lists = self.C_function(all_card_list, sub_len)
        return get_biggest_stack_type(sub_card_lists)

    def judge_player_winnable(self):
        """
        根據當前情況 判斷當前贏家
        :return:
        """
        player_hands = []
        for num in range(1, self._player_num + 1):
            player = self.legal_number_player(num)
            if player:
                card_list, hand_type, value = self.card_check(num)
                player_hand = {
                    "index": num,
                    "player": player,
                    "hand": player.show_hand(),
                    'win_list': card_list,
                    "hand_type": hand_type,
                    "value": value,
                }
                # print(f"{num} 號玩家 {player.name} 有 {card_list} 類型:{hand_type}")
                player_hands.append(player_hand)
        return judge_winner(player_hands)


if __name__ == '__main__':
    def one_game():
        # 牌局設定
        win_list = []
        game = ClassicPokerGame(_players=players)
        # 遊戲開始
        game.game_start()
        # sleep(1)
        # 發牌
        # print('發牌')
        game.deal_all()
        # for player in players:
        #     print(f'{player.name} 拿到 {player.show_hand()}')
        # sleep(1)
        stronger1 = game.judge_player_winnable()
        win_list.append(stronger1.get('player').name)
        # 增加顯牌
        stronger2 = game.add_appear_round(3)
        win_list.append(stronger2.get('player').name)
        stronger3 = game.add_appear_round(1)
        win_list.append(stronger3.get('player').name)
        _winner = game.add_appear_round(1)
        win_list.append(_winner.get('player').name)
        return win_list, _winner


    # 參數設定
    RUN_TIME_NUM = 100
    PLAYER_NUM = 10

    # 玩家設定
    players = []
    for time in range(1, PLAYER_NUM + 1):
        players.append(Player(f'Player_{time}'))

    total_list = []
    always_win_list = []
    for time in range(1, RUN_TIME_NUM + 1):
        print(f'---第 {time} 次測試---')
        win_list, winner = one_game()
        data_dict = {'win_list': win_list, "winner": winner}
        # total_list.append(data_dict)
        if win_list[0] == win_list[-1]:
            always_win_list.append(tuple(sorted(winner.get('hand'))))
            print('從頭贏到尾:', winner.get('hand'), '牌型:', winner.get('hand_type'))
        else:
            # print('贏:', winner.get('hand'), '牌型:', winner.get('hand_type'))
            pass

    print('拿到就要打到底的好牌')
    print(set(always_win_list))
