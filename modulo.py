def modulo(dividend, divisor):
    """This function imitates the modulo operator, %, for learning purposes.
	
    :arguments: 
            dividend: integer to be divided
            divisor: integer by which the dividend will be divided
    :returns: 
            remainder of dividend / divisor as long as divisor is non-zero 
    """

    if divisor == 0: 
        print 'Cannot divide by 0.'
    	return

    while dividend >= divisor: 
        try:
            dividend -= divisor
        except TypeError:
            print 'Dividend and divisor must be integers.'
            return

    return dividend 
