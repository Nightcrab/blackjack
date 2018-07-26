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
	def __init__(self, player_AI):
		self.player = Player(player_AI)
		self.dealer = Dealer()
		self.result = "Draw, Player's money was returned."
		self.active = True

	def hit(self):
		self.player.hand.draw(1)
		print("Player's hand: "+str(self.player.hand.cards))
		self.player.bust = self.player.hand.total() > 21
		if self.player.bust:
			self.endGame()
		if self.player.hand.total() == 21:
			print("Player has blackjack.")
			self.endGame()

	def stand(self):
		self.endGame()

	def endGame(self):
		self.active = False
		p_sum  = self.player.hand.total()
		d_sum = self.dealer.hand.total()
		if self.player.natural and not self.dealer.natural:
			print("Player has natural blackjack.")
			self.result = "Player wins."
		elif self.dealer.natural and not self.player.natural:
			print("Dealer has natural blackjack.")
			self.result = "House wins."
		elif self.dealer.natural and self.player.natural:
			print("Dealer and Player and natural blackjack.")
		elif self.player.bust:
			self.result = "House wins."
			print("Player busts!")
		elif self.dealer.bust:
			self.result = "Player wins."
			print("Dealer busts!")
		elif p_sum > d_sum:
			self.result = "Player wins."
		elif d_sum > p_sum:
			self.result = "House wins."

		print("\nPlayer: "+str(p_sum))
		print(self.player.hand.cards)
		print("Dealer: "+str(d_sum))
		print(self.dealer.hand.cards)

	def nextRound(self):
		p_act = self.player.play(self)
		d_act = self.dealer.play(self)
		if d_act == "hit":
			self.dealer.hand.draw(1)

		print("Player chose to "+p_act)

		if p_act == "hit":
			self.hit()
		elif p_act == "stand":
			self.stand()

		if not self.active:
			return print(self.result)
		self.nextRound()

	def simulate(self):
		print("Dealer's card: "+str(self.dealer.upcard))
		print("Player's hand: "+str(self.player.hand.cards))
		if self.player.natural or self.dealer.natural:
			self.endGame()
			return print(self.result)
		return self.nextRound()

game = BlackJackGame(randomAI)
game.simulate()

#achieved game functionality in 1hr 40m