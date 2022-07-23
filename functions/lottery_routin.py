class LotRoutin():

    def lottery_message(self, lottery):
        prize_sp = lottery[3]
        prize = ""
        self.main_prize = ""
        for row in prize_sp:
            prize += f'🎁 {row}\n'
        self.main_prize = prize