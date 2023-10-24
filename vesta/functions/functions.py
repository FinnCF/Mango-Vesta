"""Functions - A library for common mathematical functions with constraints."""

import math
import numpy as np
from typing import Union, List
from ..exceptions.exceptions import NotInRangeError

class Functions:
    """
    A class contains 'factor' functions all co-domained to [0, 1].
    Any output not in [0, 1] will raise a NotInRangeError.
    """

    @staticmethod
    def _validate_output(value: float) -> float:
        """Validate that the output is in the range [0, 1].

        Args:
            value (float): The value to validate.

        Returns:
            float: The validated value.

        Raises:
            NotInRangeError: If the value is not in [0, 1].
        """
                
        if not 0 <= value <= 1:
            raise NotInRangeError(value)
        return value

    @staticmethod
    def invrational_1(x: float, a: float = 1, b: float = 1, c: float = 25) -> float:
        """Inverse rational function constrained to [0, 1].
        DESMOS: https://www.desmos.com/calculator/wdrcpucyye

        
        Args:
            x (float): Input value.
            a, b, c (float): Parameters of the function.

        Returns:
            float: Constrained output value.
        """
                
        output = a / (b + (x * (1 / c)))
        return  Functions._validate_output(output)
    

    @staticmethod
    def invrational_2(x: float, a: float = 1, b: float = 1, c: float = 25) -> float:
        """Inverse rational 2 function constrained to [0, 1].
        DESMOS: https://www.desmos.com/calculator/j2hodwrtem

        
        Args:
            x (float): Input value.
            a, b, c (float): Parameters of the function.

        Returns:
            float: Constrained output value.
        """
                
        output = -(a / (b + (x * c))) + 1
        return  Functions._validate_output(output)
        
    @staticmethod
    def genlogistic_1(x: float, a: float = 1, b: float = 1, c: float = 25, d: float = 1) -> float:
        """Generalized logistic 1 function constrained to [0, 1].
        DESMOS: https://www.desmos.com/calculator/cc7wisjl4u
        
        Args:
            x (float): Input value.
            a, b, c, d (float): Parameters of the function.

        Returns:
            float: Constrained output value.
        """
        if x > 1000000: return 1 # Prevent overflow
        output = -a / (b + (1/c) * np.exp((1/d) * x)) + 1
        return Functions._validate_output(output)

    @staticmethod
    def genlogistic_2(x: float, a: float = 1, b: float = 1, c: float = 25, d: float = 1) -> float:
        """Generalized logistic 2 function constrained to [0, 1].
        DESMOS: https://www.desmos.com/calculator/srettiqm4d
        
        Args:
            x (float): Input value.
            a, b, c, d (float): Parameters of the function.

        Returns:
            float: Constrained output value.
        """
                
        output = a / (b + (1/c) * np.exp((1/d) * x))
        return Functions._validate_output(output)

    
    @staticmethod
    def generalized_tanh(x: float, a: float, b: float, c: float, d: float) -> float:
        """
        Generalized hyperbolic tangent function with custom shaping parameters.
        
        This function generalizes the tanh function to allow for greater flexibility
        in shaping the curve. It is constrained to output values in [0, 1].

        Mathematical expression:
            \( \text{output} = a + b * \frac{e^{c * x} - e^{-d * x}}{e^{c * x} + e^{-d * x}} \)
        
        Args:
            x (float): The input value.
            a (float): Vertical shift parameter.
            b (float): Vertical scale parameter.
            c (float): Exponential growth rate for positive x.
            d (float): Exponential decay rate for negative x.

        Returns:
            float: The output value, constrained to [0, 1].

        Raises:
            NotInRangeError: If the output value is not in [0, 1].
        """

        numerator = np.exp(c * x) - np.exp(-d * x)
        denominator = np.exp(c * x) + np.exp(-d * x)
        output = a + b * (numerator / denominator)
        return Functions._validate_output(output)
    
    @staticmethod
    def generalized_relu(x: float, a: float = 1.0, b: float = 0.0) -> float:
        """
        Generalized Rectified Linear Unit (ReLU) function with scaling and shifting parameters.

        Mathematical expression:
            \( \text{output} = a \times \max(0, x) + b \)

        Args:
            x (float): The input value.
            a (float): Scaling parameter.
            b (float): Shifting parameter.

        Returns:
            float: The output value.

        Raises:
            NotInRangeError: If the output value is not in [0, 1].
        """
        output = a * max(0, x) + b
        return Functions._validate_output(output)
    
    @staticmethod
    def generalized_leaky_relu(x: float, alpha: float = 0.01, a: float = 1.0, b: float = 0.0) -> float:
        """
        Generalized Leaky Rectified Linear Unit (Leaky ReLU) function with scaling and shifting parameters.

        Mathematical expression:
            \( \text{output} = a \times \max(\alpha \times x, x) + b \)

        Args:
            x (float): The input value.
            alpha (float): The slope for the function when \( x < 0 \).
            a (float): Scaling parameter.
            b (float): Shifting parameter.

        Returns:
            float: The output value.

        Raises:
            NotInRangeError: If the output value is not in [0, 1].
        """
        output = a * max(alpha * x, x) + b
        return Functions._validate_output(output)
    
    @staticmethod
    def generalized_sigmoid(x: float, a: float = 0.0, b: float = 1.0, c: float = 1.0, d: float = 0.0) -> float:
        """
        Generalized Sigmoid function with scaling and shifting parameters.

        Mathematical expression:
            \( \text{output} = a + \frac{b}{1 + \exp(-c \times (x - d))} \)

        Args:
            x (float): The input value.
            a (float): Vertical shift parameter.
            b (float): Scaling parameter for the output.
            c (float): Scaling parameter for the input.
            d (float): Horizontal shift parameter for the input.

        Returns:
            float: The output value.

        Raises:
            NotInRangeError: If the output value is not in [0, 1].
        """
        output = a + b / (1 + np.exp(-c * (x - d)))
        return Functions._validate_output(output)

    @staticmethod
    def generalized_swish(x: float, a: float = 1.0, b: float = 1.0, beta: float = 1.0) -> float:
        """
        Generalized Swish function.
        
        Args:
            x (float): The input value.
            a (float): Vertical shift parameter.
            b (float): Scaling parameter for the output.
            beta (float): Beta parameter for sigmoid activation.

        Returns:
            float: The output value.

        Raises:
            NotInRangeError: If the output value is not in [0, 1].
        """
        sigmoid_output = Functions.generalized_sigmoid(beta * x)
        output = a + b * (x * sigmoid_output)
        return Functions._validate_output(output)
    
    @staticmethod
    def generalized_elu(x: float, a: float = 0.0, b: float = 1.0, alpha: float = 1.0) -> float:
        """
        Generalized Exponential Linear Unit (ELU) function.

        Args:
            x (float): The input value.
            a (float): Vertical shift parameter.
            b (float): Scaling parameter for the output.
            alpha (float): Alpha parameter for ELU activation.

        Returns:
            float: The output value.

        Raises:
            NotInRangeError: If the output value is not in [0, 1].
        """
        output = x if x > 0 else alpha * (math.exp(x) - 1)
        output = a + b * output
        return Functions._validate_output(output)
    
    @staticmethod
    def generalized_selu(x: float, a: float = 0.0, b: float = 1.0, alpha: float = 1.67326, scale: float = 1.0507) -> float:
        """
        Generalized Scaled Exponential Linear Unit (SELU) function.

        Args:
            x (float): The input value.
            a (float): Vertical shift parameter.
            b (float): Scaling parameter for the output.
            alpha (float): Alpha parameter for ELU activation.
            scale (float): Scaling parameter for the output.

        Returns:
            float: The output value.

        Raises:
            NotInRangeError: If the output value is not in [0, 1].
        """
        output = scale * Functions.generalized_elu(x, 0, 1, alpha)
        output = a + b * output
        return Functions._validate_output(output)
    
    @staticmethod
    def generalized_softplus(x: float, a: float = 0.0, b: float = 1.0) -> float:
        """
        Generalized Softplus function.

        Args:
            x (float): The input value.
            a (float): Vertical shift parameter.
            b (float): Scaling parameter for the output.

        Returns:
            float: The output value.

        Raises:
            NotInRangeError: If the output value is not in [0, 1].
        """
        output = math.log(1 + math.exp(x))
        output = a + b * output
        return Functions._validate_output(output)

