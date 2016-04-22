# 6.00 Problem Set 2 - Successive Approximation
# Name: Matt Graffunder
# Collaborators: None 
# Time Spent: 0:30


def evaluate_poly(poly, x):
    """
    Computes the polynomial function for a given value x. Returns that value.

    Example:
    >>> poly = (0.0, 0.0, 5.0, 9.3, 7.0)    # f(x) = 7x^4 + 9.3x^3 + 5x^2
    >>> x = -13
    >>> print evaluate_poly(poly, x)  # f(-13) = 7(-13)^4 + 9.3(-13)^3 + 5(-13)^2
    180339.9

    poly: tuple of numbers, length > 0
    x: number
    returns: float
    """
    result = 0.0
	
    for n in range(0, len(poly)):
            termResult = poly[n] * (x**n)
            result += termResult #Raise x to the Nth power, and multiple by the coeffiecent in for the Nth power
    
    return result


def compute_deriv(poly):
    """
    Computes and returns the derivative of a polynomial function. If the
    derivative is 0, returns (0.0,).

    Example:
    >>> poly = (-13.39, 0.0, 17.5, 3.0, 1.0)    # x^4 + 3x^3 + 17.5x^2 - 13.39
    >>> print compute_deriv(poly)        # 4x^3 + 9x^2 + 35^x
    (0.0, 35.0, 9.0, 4.0)

    poly: tuple of numbers, length > 0
    returns: tuple of numbers
    """
    result = ()

    for n in range(1, len(poly)):
            result += (poly[n]*(n),)

    return result

def compute_root(poly, x_0, epsilon):
    """
    Uses Newton's method to find and return a root of a polynomial function.
    Returns a tuple containing the root and the number of iterations required
    to get to the root.

    Example:
    >>> poly = (-13.39, 0.0, 17.5, 3.0, 1.0)    #x^4 + 3x^3 + 17.5x^2 - 13.39
    >>> x_0 = 0.1
    >>> epsilon = .0001
    >>> print compute_root(poly, x_0, epsilon)
    (0.80679075379635201, 8.0)

    poly: tuple of numbers, length > 1.
         Represents a polynomial function containing at least one real root.
         The derivative of this polynomial function at x_0 is not 0.
    x_0: float
    epsilon: float > 0
    returns: tuple (float, int)
    """
    deriv = compute_deriv(poly) #Derivitive won't change, compute once outside loop
    root = x_0
    iterations = 1

    result = evaluate_poly(poly, root) #Evaluate outside loop and store to allow only one eval per iteration

    while abs(result) > epsilon:
        #New Guess Formula: x_n - (f(x_n)/f'(x_n))
        root = root -(result / evaluate_poly(deriv, root)) #Calc new guess

        result = evaluate_poly(poly, root) #Evaluate new guess
        
        iterations += 1

    return (root, iterations)

##test_poly = (0,0,5,9.3,7)	
##test_poly2 = (-13.39, 0, 17.5, 3, 1)
##
##print evaluate_poly(test_poly, -13)
##print compute_deriv(test_poly2)
##print compute_root(test_poly2, 0.1, 0.0001)
