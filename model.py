
import cv2
import numpy as np
import time
import math

# Define the sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def layer_sizes(X, Y):
    """
    Determines the size of the input layer, hidden layer(s), and output layer.

    Parameters:
    - X: Input data (features). Shape (n_x, m), where 'n_x' is the number of input features, 'm' is the number of examples.
    - Y: Output data (labels). Shape (1, m) for binary classification or (n_y, m) for multi-class.

    Returns:
    - sizes: A tuple containing (n_x, n_h, n_y).
    """

    # Number of input features
    n_x = X.shape[0]  # Input layer size

    # Number of hidden neurons (optional, can be predetermined, e.g., 4)
    n_h = 4  # Hardcoding a hidden layer size, typically set based on problem requirements

    # Number of outputs
    n_y = Y.shape[0]  # Output layer size (1 for binary classification)

    return (n_x, n_h, n_y)


def initialize_parameters(n_x, n_h, n_y):
    """
    Initialize the weights and biases for a simple neural network with one hidden layer.

    Parameters:
    - n_x: Number of input features.
    - n_h: Number of neurons in the hidden layer.
    - n_y: Number of output neurons (e.g., 1 for binary classification).

    Returns:
    - parameters: Dictionary containing the initialized weights and biases.
    """

    # Initialize weights with small random values (to avoid symmetry) and biases with zeros
    W1 = np.random.randn(n_h, n_x) * 0.01  # Weights for the hidden layer
    b1 = np.zeros((n_h, 1))  # Biases for the hidden layer

    W2 = np.random.randn(n_y, n_h) * 0.01  # Weights for the output layer
    b2 = np.zeros((n_y, 1))  # Biases for the output layer

    # Store in a dictionary
    parameters = {
        'W1': W1,
        'b1': b1,
        'W2': W2,
        'b2': b2
    }

    return parameters




def forward_propagation(X, parameters):
    """
    Perform forward propagation to compute the outputs of each layer.

    Parameters:
    - X: Input data. Shape (n_x, m).
    - parameters: Dictionary containing the model's parameters (W1, b1, W2, b2).

    Returns:
    - A2: Output predictions from the model. Shape (1, m).
    - cache: Dictionary containing intermediate computations (Z1, A1, Z2, A2) for later use in backpropagation.
    """

    # Retrieve values from parameters
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']

    # Implement forward propagation
    Z1 = np.dot(W1, X) + b1  # Compute linear activation at layer 1
    A1 = 1 / (1 + np.exp(-Z1))  # Apply sigmoid activation to layer 1
    Z2 = np.dot(W2, A1) + b2  # Compute linear activation at layer 2
    A2 = 1 / (1 + np.exp(-Z2))  # Apply sigmoid activation to layer 2 (output layer)

    # Store intermediate values in cache
    cache = {
        'Z1': Z1,
        'A1': A1,
        'Z2': Z2,
        'A2': A2
    }

    return A2, cache


def compute_cost(A2,y,parameters):
    m=y.shape[0]
    logprobs = np.multiply(np.log(A2), Y) + np.multiply(np.log(1 - A2), 1 - Y)
    cost = -np.sum(logprobs) / m  # Average cost across all examples
    # Ensures the cost is a scalar value
    cost = np.squeeze(cost)  # Remove unnecessary dimensions

    return cost





def backward_propagation(parameters, cache, X, Y):
    """
    Perform backward propagation to calculate gradients for updating the model's parameters.

    Parameters:
    - parameters: Dictionary containing the model's parameters (W1, b1, W2, b2).
    - cache: Dictionary containing intermediate computations (Z1, A1, Z2, A2) from the forward propagation.
    - X: Input data. Shape (n_x, m).
    - Y: True labels. Shape (1, m).

    Returns:
    - grads: Dictionary containing the gradients for each parameter (dW1, db1, dW2, db2).
    """

    # Retrieve values from parameters and cache
    W1 = parameters['W1']
    W2 = parameters['W2']
    b1 = parameters['b1']
    b2 = parameters['b2']
    A1 = cache['A1']
    A2 = cache['A2']
    Z1 = cache['Z1']
    Z2 = cache['Z2']

    # Number of training examples
    m = X.shape[1]

    # Calculate derivatives for output layer (layer 2)
    dZ2 = A2 - Y  # Derivative of cost with respect to Z2 (error at the output)
    dW2 = np.dot(dZ2, A1.T) / m  # Gradient of W2
    db2 = np.sum(dZ2, axis=1, keepdims=True) / m  # Gradient of b2

    # Calculate derivatives for hidden layer (layer 1)
    dA1 = np.dot(W2.T, dZ2)  # Backpropagate the error to the hidden layer
    dZ1 = dA1 * (1 - A1) * A1  # Derivative of cost with respect to Z1 (using sigmoid derivative)
    dW1 = np.dot(dZ1, X.T) / m  # Gradient of W1
    db1 = np.sum(dZ1, axis=1, keepdims=True) / m  # Gradient of b1

    # Store gradients in a dictionary
    grads = {
        'dW1': dW1,
        'db1': db1,
        'dW2': dW2,
        'db2': db2
    }

    return grads




def update_parameters(parameters, grads, learning_rate):
    """
    Updates the weights and biases of a simple neural network using gradient descent.

    Parameters:
    - parameters: Dictionary containing the network's current parameters (W1, b1, W2, b2).
    - grads: Dictionary containing the gradients of the parameters (dW1, db1, dW2, db2).
    - learning_rate: The step size for gradient descent (determines the magnitude of parameter updates).

    Returns:
    - parameters: Dictionary containing the updated parameters.
    """

    # Retrieve current parameters and gradients
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']

    dW1 = grads['dW1']
    db1 = grads['db1']
    dW2 = grads['dW2']
    db2 = grads['db2']

    # Update weights and biases using gradient descent
    W1 -= learning_rate * dW1  # Update weights for the first layer
    b1 -= learning_rate * db1  # Update biases for the first layer

    W2 -= learning_rate * dW2  # Update weights for the second layer
    b2 -= learning_rate * db2  # Update biases for the second layer

    # Store updated parameters in a dictionary
    parameters = {
        'W1': W1,
        'b1': b1,
        'W2': W2,
        'b2': b2
    }

    return parameters





def nn_model(X, Y, n_h, num_iterations, learning_rate=0.01, print_cost=False):
    """
    Builds a simple neural network model with one hidden layer.

    Parameters:
    - X: Input data (features). Shape (n_x, m), where 'n_x' is the number of features, and 'm' is the number of examples.
    - Y: Output data (labels). Shape (1, m) for binary classification.
    - n_h: Number of neurons in the hidden layer.
    - num_iterations: Number of iterations for training.
    - learning_rate: Learning rate for gradient descent.
    - print_cost: Whether to print the cost every 100 iterations.

    Returns:
    - parameters: Dictionary containing the final parameters (W1, b1, W2, b2) after training.
    """

    # Get the sizes of the layers
    n_x = X.shape[0]
    n_y = Y.shape[0]

    # Initialize the parameters
    parameters = initialize_parameters(n_x, n_h, n_y)

    # Training loop
    for i in range(1, num_iterations + 1):
        # Forward propagation
        A2, cache = forward_propagation(X, parameters)

        # Compute the cost
        cost = compute_cost(A2, Y)

        # Backward propagation
        grads = backward_propagation(parameters, cache, X, Y)

        # Update the parameters
        parameters = update_parameters(parameters, grads, learning_rate)

        # Print the cost every 100 iterations to track training progress
        if print_cost and i % 100 == 0:
            print(f"Cost after iteration {i}: {cost:.6f}")

    return parameters


def predict(X, parameters):
    """
    Predicts the output for the given input data using the trained parameters.

    Parameters:
    - X: Input data to make predictions on. Shape (n_x, m), where 'n_x' is the number of input features and 'm' is the number of examples.
    - parameters: Dictionary containing the trained parameters of the neural network (W1, b1, W2, b2).

    Returns:
    - predictions: Array containing the predicted class (0 or 1) for each example in 'X'.
    """

    # Perform forward propagation with the given input data and parameters
    _, cache = forward_propagation(X, parameters)

    # Get the output from the last layer (after sigmoid activation)
    A2 = cache['A2']

    # Apply a threshold to classify outputs
    predictions = (A2 > 0.5).astype(int)  # Predictions: 1 if A2 > 0.5, otherwise 0

    return predictions


