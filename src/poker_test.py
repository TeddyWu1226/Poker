from Poker.PokerRule import PokerGroup

if __name__ == '__main__':
    stack = PokerGroup()
    stack.fill_card_group(is_shuffle=True)
    time = 1
    print('抽卡比大小實驗')
    while stack.content(as_class=True):
        print(f'第{time}次測試')
        draw_card = stack.draw(number=2, as_class=True)
        one, two = draw_card
        print(f'抽出{one.img}、{two.img}，玩家 {1 if one.value > two.value else 2} 獲勝')
        print('------')
        time += 1
