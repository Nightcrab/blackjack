import numpy as np

def sigmoid(x, deriv=False):
	if(deriv==True):
		return x*(1-x)
	return 1/(1+np.exp(-x))

np.random.seed(1)

class TwoLayerNN:
	"""Neural Network with no hidden layers."""
	def __init__(self):
		self.syn0 = 2*np.random.random((3,1)) - 1 #randomly initialise weights with mean 0

	def train(self, t_in, t_out):
		I = t_in
		O = t_out.T
		for iter in range(10000):
			l0 = I #input layer is same as input training matrix
			l1 = sigmoid(np.dot(l0, self.syn0)) #dotproduct (multiplication) of all inputs with corresponding weights, as a probability (between 0 and 1)
			l1error = O - l1 #error or difference between expected output and what was generated
			l1delta = l1error * sigmoid(l1, True) #weighting the error measure of outputs to be higher for outputs closer to 0.5 (on the fence) in order to push them one way or another
			self.syn0 += np.dot(l0.T, l1delta) #increase or decrease weights by the dotproduct of input and weighted errors
			self.prediction = l1

class ThreeLayerNN:
	"""Neural Network with one hidden layer."""
	def __init__(self):
		self.syn0 = 2*np.random.random((3,6)) - 1
		self.syn1 = 2*np.random.random((6,1)) - 1 #to turn the 6x6 from the hidden layer into a 6x1 array of outputs

	def train(self, t_in, t_out):
		I = t_in
		O = t_out.T
		for iter in range(10000):
			l0 = I #input (6x3)
			l1 = sigmoid(np.dot(l0, self.syn0)) #dotproduct of input (6x3) with weights (3x6) should create 6 outputs per input (for each neuron in l1), a (6x6) matrix
			l2 = sigmoid(np.dot(l1, self.syn1)) #output (6x1)
			l2error = O - l2
			l2delta = l2error * sigmoid(l2, True) #l2 weighted error
			l1error = l2delta.dot(self.syn1.T) #the error of the first set of weights is the second set of weights multiplied by the second layer's error, which reverses the
			                              #"extra" error created by the second set of weights
			l1delta = l1error * sigmoid(l1, True) #l1 weighted error
			self.syn0 += np.dot(l0.T, l1delta)
			self.syn1 += np.dot(l1.T, l2delta)
			self.prediction = l2

X = np.array([[0, 0, 1],
			  [1, 0, 1],
			  [0, 1, 0],
			  [1, 1, 1],
			  [0, 1, 0],
			  [1, 1, 0]])
Y = np.array([[1,1,0,1,0,0]])

nn = TwoLayerNN()
nn.train(X, Y)
print(nn.prediction)

print("\n")

nn1 = ThreeLayerNN()
nn1.train(X, Y)
print(nn1.prediction)