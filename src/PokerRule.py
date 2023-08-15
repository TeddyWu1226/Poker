import random


class PokerDefinition:
    """
    撲克定義
    :param displacement: 位移權重(代表以哪個數值為起始，預設為8 => 梅花2為起點
    """

    def __init__(self, displacement=4):
        # 分類
        self._displacement = displacement
        self._type_limit = ['p', 'h', 'c', 't']
        self._type_img = ['♠', '♥', '♦', '♣']
        self._type_text = ['黑桃', '紅心', '方塊', '梅花']

    def poker_enum(self, _type, _return='img'):
        if _return == 'text':
            return self._type_text[self._type_limit.index(_type)]
        else:
            return self._type_img[self._type_limit.index(_type)]

    def random_poker_card(self):
        return f'{random.choice(self._type_limit)}{random.randint(1, 13)}'

    @staticmethod
    def help():
        print("""花色:
黑桃♠（p）、梅花♣（t）
紅心♥（h）、方塊♦（c)
數字: 1 ~ 13
        
ex: 'p5'、'c13'
        """)


class PokerCard(PokerDefinition):
    """
    撲克CLASS
    :param _type: 類型
    黑桃♠（p）、梅花♣（t）
    紅心♥（h）、方塊♦（c)
    :param _number: 數字(1~13)

    """

    def __init__(self, _type: str, _number: int):
        super().__init__()
        if _type not in self._type_limit:
            raise TypeError(f'類型錯誤，只能是這些字母{self._type_limit}類型，_type={_type}')
        if _number < 1 or _number > 13:
            raise TypeError(f'類型錯誤，數字大小必須介於1~13之間，_number={_number}')

        self._number = _number
        self._type = _type
        if _type == 'p' or _type == 't':
            self._color = 'black'
        else:
            self._color = 'red'

    @property
    def color(self):
        return self._color

    @property
    def number(self):
        return self._number

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        cal = self._number * 4 - self._type_limit.index(self._type) - self._displacement
        if cal <= 0:
            cal = cal + 48 + self._displacement
        return cal

    @property
    def text(self):
        return f'{self._type}{self._number}'

    @property
    def locale_text(self):
        return f'{super().poker_enum(self._type, "text")}{self._number}'

    @property
    def img(self):
        return f'{super().poker_enum(self._type, "img")}{self._number}'


class PokerGroup(PokerDefinition):
    def __init__(self, initial_card=None, quantity=52):
        super().__init__()
        if initial_card is None:
            initial_card = []
        self.card_list = initial_card
        self.quantity = quantity

    @staticmethod
    def check_poker_type(card):
        if isinstance(card, PokerCard):
            return card
        else:
            try:
                card = PokerCard(card[0], int(card[1:]))
                return card
            except Exception:
                ValueError('格式錯誤,請使用PokerCard class 或是 "p5","t3"寫法')

    def content(self, as_class=False):
        """
        回傳目前牌組情況
        :return:
        """
        if not self.card_list:
            return None
        if as_class:
            return self.card_list
        else:
            return list(map(lambda x: x.img, self.card_list))

    def fill_card_group(self, is_shuffle=True):
        for _type in self._type_limit:
            for num in range(1, 14):
                card = PokerCard(_type=_type, _number=num)
                self.card_list.append(card)
        if is_shuffle:
            for i in range(0, self.quantity):
                self.shuffle()

    def shuffle(self, is_show=False):
        random.shuffle(self.card_list)
        if is_show:
            self.show_all()

    def show_all(self):
        print(list(map(lambda x: x.img, self.card_list)))

    def specify_draw(self, draw_card: PokerCard, as_class=False):
        """
        抽牌(指定牌型)
        :param draw_card:指定的牌
        :param as_class:回傳class格式
        :return:
        """
        if isinstance(draw_card, PokerCard):
            draw_card = draw_card.text
        elif isinstance(draw_card, str):
            pass
        else:
            ValueError('格式錯誤,請使用PokerCard class 或是 "p5","t3"寫法')
        # 透過映射關係找到牌
        map_card_list = list(map(lambda x: x.text, self.card_list))
        if draw_card not in map_card_list:
            return None
        else:
            res = self.card_list.pop(map_card_list.index(draw_card))
        if as_class:
            return res
        else:
            return res.text

    def draw(self, number=1, _from='top', as_class=True):
        """
        抽牌(照順序抽數量)
        :param number: 張數
        :param _from: 從哪邊(top、bottom)
        :param as_class:回傳class格式
        :return:
        """
        res = []
        for i in range(0, number):
            if not self.card_list:
                break
            if _from == 'bottom':
                drew_card = self.card_list.pop()
            else:
                drew_card = self.card_list.pop(0)
            res.append(drew_card if as_class else drew_card.text)
        return res

    def add(self, poker_card_list, is_unique=True):
        for poker_card in poker_card_list:
            poker_card = self.check_poker_type(poker_card)
            # 透過映射關係找到牌
            map_card_list = list(map(lambda x: x.text, self.card_list))
            if is_unique:
                if poker_card.text in map_card_list:
                    print(f'{poker_card} 已存在在牌堆裡,略過添加')
                    continue
            self.card_list.append(poker_card)


def _convert_poker_type(card):
    """
    轉換為pokerCard class
    :param card:
    :return:
    """
    if isinstance(card, PokerCard):
        return card
    else:
        try:
            card = PokerCard(card[0], int(card[1:]))
            return card
        except Exception:
            ValueError('格式錯誤,請使用PokerCard class 或是 "p5","t3"寫法')
