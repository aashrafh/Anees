import numpy as np
def accuracy_score(true, predicted):
    summation = 0
    for index in range(len(true)):
        if true[index] == predicted[index]:
            summation += 1
    return (summation/(len(true)))

def sigmoid(x):
    return (1/(1+np.exp2(-x)))

class LogisticRegression:
    def __init__(self, lr: int, epochs: int, probability_threshold: float = 0.5, random_state = None):
        self.lr = lr # The learning rate
        self.epochs = epochs # The number of training epochs
        self.probability_threshold = probability_threshold # If the output of the sigmoid function is > probability_threshold, the prediction is considered to be positive (True)
                                                           # otherwise, the prediction is considered to be negative (False)
        self.random_state = random_state # The random state will be used set the random seed for the sake of reproducability
    
    def _prepare_input(self, X):
        ones = np.ones((X.shape[0], 1), dtype=X.dtype)
        return np.concatenate((ones, X), axis=1)
    
    def _prepare_target(self, y):
        return np.where(y, 1, -1)

    def _initialize(self, num_weights: int, stdev: float = 0.01):
        self.w = np.random.randn(num_weights) * stdev

    def _gradient(self, X, y):
        y_x = np.matmul(y,X)
        y_w_x = np.matmul(y,np.dot(self.w,X.T))
        exp_y_w_x = np.exp2(y_w_x)+1
        result = np.divide((y_x),(exp_y_w_x))
        return (-1/len(y))*(result)

    def _update(self, X, y):
        gradient = self._gradient(X,y)
        self.w = self.w - self.lr*gradient

    def fit(self, X, y):
        np.random.seed(self.random_state) 
        X = self._prepare_input(X) 
        y = self._prepare_target(y)
        self._initialize(X.shape[1])
        for _ in range(self.epochs):
            self._update(X, y)
        return self 
    
    def predict(self, X):
        X = self._prepare_input(X)
        w_x = np.dot(self.w,X.T)
        predictions = sigmoid(w_x)
        classes = list()
        for prediction in predictions:
            if prediction > self.probability_threshold:
                classes.append(True)
            else:
                classes.append(False)
        return np.array(classes)
    
def validate(X_tr, X_val, y_tr, y_val, lr, epochs):
    model = LogisticRegression(lr=lr, epochs=epochs, random_state=0).fit(X_tr, y_tr)
    return accuracy_score(y_val, model.predict(X_val)) 