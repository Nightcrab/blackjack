import numpy as np

def sigmoid(x, deriv=False):
	if(deriv==True):
		return x*(1-x)
	return 1/(1+np.exp(-x))

class TwoLayerNN:
	"""Neural Network with no hidden layers."""
	def __init__(self,t_in,t_out):
		self.I = t_in
		self.O = t_out.T
		self.syn0 = 2*np.random.random((3,1)) - 1 #randomly initialise weights with mean 0
	def train(self):
		for iter in range(10000):
			l0 = self.I #input layer is same as input training matrix
			l1 = sigmoid(np.dot(l0, self.syn0)) #dotproduct (multiplication) of all inputs with corresponding weights, as a probability (between 0 and 1)
			l1error = self.O - l1 #error or difference between expected output and what was generated
			l1delta = l1error * sigmoid(l1, True) #weighting the error measure of outputs to be higher for outputs closer to 0.5 (on the fence) in order to push them one way or another
			self.syn0 += np.dot(l0.T, l1delta) #increase or decrease weights by the dotproduct of input and weighted errors
			self.prediction = l1

X = np.array([[0, 0, 1],
			  [1, 0, 1],
			  [0, 1, 0],
			  [1, 1, 1],
			  [0, 1, 0],
			  [1, 1, 0]])
Y = np.array([[1,1,0,1,0,0]])

nn = TwoLayerNN(X, Y)
nn.train()
print(nn.prediction)