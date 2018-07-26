import random

deck = [1,2,3,
	    4,5,6,
	    7,8,9,
	    10,10,
	    10,10]

def drawCards(amount):
	hand = []
	for i in range(amount):
		hand.append(random.choice(deck))
	return hand

def randomAI(Game):
	options = ["hit", "stand"]
	return random.choice(options)

class Hand:
	def __init__(self):
		self.cards = drawCards(2)

	def usableAce(self):
		return 1 in self.cards and sum(self.cards)+10<=21

	def total(self):
		if self.usableAce():
			return sum(self.cards)+10
		else:
			return sum(self.cards)

	def draw(self, amount):
		self.cards.extend(drawCards(amount))

class Dealer:
	"""Dealer class, responds to game state according to dealer rues"""
	def __init__(self):
		self.hand = Hand()
		self.bust = False
		self.upcard = self.hand.cards[0]
		self.natural = self.hand.total() == 21

	def play(self, Game):
		if self.hand.total() >= 17:
			return "stand"
		return "hit"

class Player:
	"""Player class, responds with hit or stand based on AI/human input"""
	def __init__(self, player_AI):
		self.hand = Hand()
		self.bust = False
		self.ai = player_AI
		self.natural = self.hand.total() == 21

	def play(self, Game):
		return self.ai(Game)

class BlackJackGame:
	""""A game of blackjack."""
	def __init__(self, player_AI, bet, debug):
		self.player = Player(player_AI)
		self.dealer = Dealer()
		self.result = "Draw, Player's money was returned."
		self.active = True
		self.earnings = 0
		self.bet = bet
		self.debug = debug

	def log(self, text):
		if not self.debug:
			return
		print(text)

	def hit(self):
		self.player.hand.draw(1)
		self.log("Player's hand: "+str(self.player.hand.cards))
		self.player.bust = self.player.hand.total() > 21
		if self.player.bust:
			self.endGame()
		if self.player.hand.total() == 21:
			self.log("Player has blackjack.")
			self.endGame()

	def stand(self):
		self.endGame()

	def endGame(self):
		self.active = False
		p_sum  = self.player.hand.total()
		d_sum = self.dealer.hand.total()
		if self.player.natural and not self.dealer.natural:
			self.log("Player has natural blackjack.")
			self.result = "Player wins with natural."
		elif self.dealer.natural and not self.player.natural:
			self.log("Dealer has natural blackjack.")
			self.result = "House wins."
		elif self.dealer.natural and self.player.natural:
			self.log("Dealer and Player have natural blackjack.")
		elif self.player.bust:
			self.result = "House wins."
			self.log("Player busts!")
		elif self.dealer.bust:
			self.result = "Player wins."
			self.log("Dealer busts!")
		elif p_sum > d_sum:
			self.result = "Player wins."
		elif d_sum > p_sum:
			self.result = "House wins."

		self.log("\nPlayer: "+str(p_sum))
		self.log(self.player.hand.cards)
		self.log("Dealer: "+str(d_sum))
		self.log(self.dealer.hand.cards)
		if self.result == "House wins.":
			self.earnings -= self.bet
		elif self.result == "Player wins.":
			self.earnings += self.bet*2
		elif self.result == "Player wins with natural.":
			self.earnings += self.bet*3

	def nextRound(self):
		p_act = self.player.play(self)
		d_act = self.dealer.play(self)
		if d_act == "hit":
			self.dealer.hand.draw(1)

		self.log("Player chose to "+p_act)

		if p_act == "hit":
			self.hit()
		elif p_act == "stand":
			self.stand()

		if not self.active:
			return self.result
		self.nextRound()

	def simulate(self):
		self.log("Dealer's card: "+str(self.dealer.upcard))
		self.log("Player's hand: "+str(self.player.hand.cards))
		if self.player.natural or self.dealer.natural:
			self.endGame()
			return self.result
		return self.nextRound()

def goBankrupt(money):
	counter = 0
	peak = money
	def newGame():
		game = BlackJackGame(randomAI, 1, False)
		game.simulate()
		return game.earnings
	while money > 0:
		money += newGame()
		if money > peak:
			peak = money
		counter += 1
	print("Player went bankrupt after "+str(counter)+" games. At their peak, they owned "+str(peak)+" chips.")

goBankrupt(1000)

#achieved game functionality in 1hr 40m