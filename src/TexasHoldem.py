import copy
from collections import Counter
from enum import Enum

from PokerRule import PokerGroup, PokerDefinition, _convert_poker_type, poker_value_sum, filter_poker_list


class CardTypeEnum(Enum):
    RoyalFlush = 'RoyalFlush'
    StraightFlush = 'StraightFlush'
    FourKind = 'FourKind'
    FullHouse = 'FullHouse'
    Flush = 'Flush'
    Straight = 'Straight'
    ThreeKind = 'ThreeKind'
    TwoPair = 'TwoPair'
    OnePair = 'OnePair'
    HighCard = 'HighCard'


class CardTypeStageEnum(Enum):
    RoyalFlush = 100
    StraightFlush = 99
    FourKind = 98
    FullHouse = 97
    Flush = 96
    Straight = 95
    ThreeKind = 94
    TwoPair = 93
    OnePair = 92
    HighCard = 0


CardTypeEnumCn = {
    'RoyalFlush': '同花大順',
    'StraightFlush': '同花順',
    'FourKind': '鐵支',
    'FullHouse': '葫蘆',
    'Flush': '同花',
    'Straight': '順子',
    'ThreeKind': '三條',
    'TwoPair': '兩對',
    'OnePair': '一對',
    'HighCard': '雜牌'
}


class TexasRule(PokerDefinition):
    def __init__(self, card_list, as_class=False):
        super().__init__()
        self.card_list = []
        for card in card_list:
            card = _convert_poker_type(card)
            self.card_list.append(card)
        self.as_class = as_class
        self.number_count = {}
        self.type_count = {}

    def list_sort(self, key, as_class=False, is_number=False):
        """
        排序(由大到小)
        :param key:number,value
        :param as_class:
        :param is_number:
        :return:
        """
        sorted_list = copy.deepcopy(self.card_list)

        if key not in ['number', 'value']:
            key = 'value'

        limit = len(self.card_list)
        for _first in range(limit):
            for _second in range(0, limit - _first - 1):
                first_value = getattr(sorted_list[_second], key)
                second_value = getattr(sorted_list[_second + 1], key)
                if first_value > second_value:
                    sorted_list[_second], sorted_list[_second + 1] = sorted_list[_second + 1], sorted_list[_second]

        if as_class:
            return sorted_list
        else:
            if is_number:
                return list(map(lambda x: x.number, sorted_list))
            else:
                return list(map(lambda x: x.img, sorted_list))

    @property
    def number_sorted(self):
        return self.list_sort('number', as_class=self.as_class)

    @property
    def value_sorted(self):
        return self.list_sort('value', as_class=self.as_class)

    def get_count(self, _type='number'):
        if _type == 'number':
            return self.number_count or self.calculate_number_count
        else:
            return self.type_count or self.calculate_type_count

    @property
    def calculate_number_count(self):
        base_list = map(lambda x: x.number, self.card_list)
        self.number_count = dict(Counter(base_list))
        return self.number_count

    @property
    def calculate_type_count(self):
        base_list = map(lambda x: x.type, self.card_list)
        self.type_count = dict(Counter(base_list))
        return self.type_count

    # 牌型判斷(基本型)
    @property
    def judge_straight_by_number(self) -> (bool, int):
        """
        透過數字排列判斷順子
        :return: Bool , total_value(int)
        """
        base_list = self.list_sort('number', as_class=True)
        last_number = 0
        if base_list[0].number == 1:
            total_value = poker_value_sum(base_list) - 48
        else:
            total_value = poker_value_sum(base_list)
        is_straight = True
        for index, card in enumerate(base_list):
            if not index:
                pass
            else:
                if card.number - last_number != 1:
                    is_straight = False
                    break
            last_number = card.number
        if not is_straight:
            is_straight, total_value = self.judge_biggest_straight
        return is_straight, total_value

    @property
    def judge_biggest_straight(self) -> (bool, int):
        """
        判斷大順
        :return: Bool , total_value(int)
        """
        base_list = self.list_sort('number', as_class=True)
        base_num_list = self.list_sort('number', as_class=False, is_number=True)
        total_value = poker_value_sum(base_list)
        if {10, 11, 12, 13, 1} - set(base_num_list):
            return False, 0
        return True, total_value

    @property
    def is_straight(self) -> (bool, int):
        """
        是否為順子
        :return: Bool,int
        """
        if len(self.card_list) < 5:
            return False, 0
        return self.judge_straight_by_number

    @property
    def is_flush(self) -> (bool, int):
        """
        是否為同花
        :return: Bool , total_value(int)
        """
        if len(self.card_list) < 5:
            return False
        type_list = self.get_count('type')
        has_flush = False
        for _type_count in type_list.values():
            if _type_count >= 5:
                has_flush = True
                break
        total_value = poker_value_sum(self.card_list)
        return has_flush, total_value

    @property
    def judge_kinds(self) -> (bool, int):
        """
        是否為多對
        :return: String,total_value(int)
        """
        if len(self.card_list) < 2:
            return False, 0

        count_list = list(self.get_count('number').values())
        num_list = list(self.get_count('number').keys())
        if 4 in count_list:
            _return_type = CardTypeEnum.FourKind.value
            total_value = poker_value_sum(self.card_list)
        elif 3 in count_list and 2 in count_list:
            _return_type = CardTypeEnum.FullHouse.value
            total_value = poker_value_sum(self.card_list)
        elif 3 in count_list:
            # 找到數量有3張的牌數字是多少
            three_kind_num = num_list[count_list.index(3)]
            # 找到三條的牌列
            filter_three_kind = filter_poker_list(self.card_list, number=three_kind_num)
            other_cards = list(set(self.card_list) - set(filter_three_kind))
            _return_type = CardTypeEnum.ThreeKind.value
            total_value = poker_value_sum(filter_three_kind) * 1000 + poker_value_sum(other_cards)
        elif count_list.count(2) == 2:
            total_value = 0
            count_dict = self.get_count('number')
            copy_card_list = copy.deepcopy(self.card_list)
            for num in count_dict:
                if count_dict[num] == 2:
                    _filter_pair = filter_poker_list(self.card_list, number=num)
                    copy_card_list = list(set(self.card_list) - set(_filter_pair))
                    total_value += poker_value_sum(_filter_pair) * 1000
            total_value += poker_value_sum(copy_card_list)
            _return_type = CardTypeEnum.TwoPair.value

        elif 2 in count_list:
            # 找到數量有2張的牌數字是多少
            pair_num = num_list[count_list.index(2)]
            # 找到三條的牌列
            filter_pair = filter_poker_list(self.card_list, number=pair_num)
            other_cards = list(set(self.card_list) - set(filter_pair))
            _return_type = CardTypeEnum.OnePair.value
            total_value = poker_value_sum(filter_pair) * 1000 + poker_value_sum(other_cards)
        else:
            _return_type = CardTypeEnum.HighCard.value
            total_value = poker_value_sum(self.card_list)

        return _return_type, total_value

    @property
    def get_total_value(self):
        value_list = map(lambda x: x.value, self.card_list)
        return sum(value_list)

    @property
    def check(self) -> (bool, int):
        """
        檢查牌型
        :return: 牌型、
        """
        is_flush, flush_value = self.is_flush
        is_straight, straight_value = self.is_straight
        if is_flush and is_straight and straight_value >= 205:
            ans = CardTypeEnum.RoyalFlush.value
            return_value = straight_value
        elif is_flush and is_straight:
            ans = CardTypeEnum.StraightFlush.value
            return_value = straight_value
        elif is_flush:
            ans = CardTypeEnum.Flush.value
            return_value = flush_value
        elif is_straight:
            ans = CardTypeEnum.Straight.value
            return_value = straight_value
        else:
            ans, return_value = self.judge_kinds
        return ans, return_value
