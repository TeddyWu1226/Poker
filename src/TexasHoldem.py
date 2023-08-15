import copy
from collections import Counter
from enum import Enum

from PokerRule import PokerGroup, PokerDefinition, _convert_poker_type


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


class PokerCardType(PokerDefinition):
    def __init__(self, card_list, as_class=False):
        super().__init__()
        self.card_list = []
        for card in card_list:
            card = _convert_poker_type(card)
            self.card_list.append(card)
        self.as_class = as_class
        self.number_count = {}
        self.type_count = {}

    def list_sort(self, key, as_class=False):
        """

        :param key:number,value
        :param as_class:
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
    def judge_straight_by_number(self):
        """
        透過數字排列判斷順子
        :return:
        """
        base_list = self.list_sort('number', as_class=True)
        last_number = 0
        for index, card in enumerate(base_list):
            if not index:
                pass
            else:
                if card.number - last_number != 1:
                    return False
            last_number = card.number
        return True

    @property
    def judge_straight_by_value(self):
        """
        透過價值排列判斷順子
        :return:
        """
        base_list = self.list_sort('value', as_class=True)
        last_value = 0
        for index, card in enumerate(base_list):
            if not index:
                pass
            else:
                if card.value - last_value > 4:
                    return False
            last_value = card.value
        return True

    @property
    def is_straight(self):
        """
        是否為順子
        :return:
        """
        if len(self.card_list) < 5:
            return False
        # by number
        if self.judge_straight_by_number:
            return True
        # by value
        if self.judge_straight_by_value:
            return True
        return False

    @property
    def is_flush(self):
        """
        是否為同花
        :return: Bool
        """
        if len(self.card_list) < 5:
            return False
        type_list = self.get_count('type')
        if 5 in type_list.values():
            return True
        return False

    @property
    def judge_kinds(self):
        """
        是否為多對
        :return: String
        """
        if len(self.card_list) < 2:
            return False
        count_list = self.get_count('number').values()
        if 4 in count_list:
            return CardTypeEnum.FourKind.value
        elif 3 in count_list and 2 in count_list:
            return CardTypeEnum.FullHouse.value
        elif 3 in count_list:
            return CardTypeEnum.ThreeKind.value
        elif list(count_list).count(2) == 2:
            return CardTypeEnum.TwoPair.value
        elif 2 in count_list:
            return CardTypeEnum.OnePair.value
        else:
            return False

    @property
    def get_total_value(self):
        value_list = map(lambda x: x.value, self.card_list)
        return sum(value_list)

    @property
    def check(self):
        """
        檢查牌型
        :return:
        """
        is_flush = self.is_flush
        is_straight = self.is_straight
        total = self.get_total_value

        if is_flush and is_straight and total >= 205:
            ans = CardTypeEnum.RoyalFlush.value
        elif is_flush and is_straight:
            ans = CardTypeEnum.StraightFlush.value
        elif is_flush:
            ans = CardTypeEnum.Flush.value
        elif is_straight:
            ans = CardTypeEnum.Straight.value
        else:
            ans = self.judge_kinds
            if not ans:
                ans = CardTypeEnum.HighCard.value
        return ans
