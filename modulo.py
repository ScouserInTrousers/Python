def modulo(dividend, divisor):
    """This function imitates the modulo operator, %, for learning purposes.
	
    :arguments: 
            dividend: integer to be divided
            divisor: integer by which the dividend will be divided
    :returns: 
            remainder of the division problem  dividend / divisor as long as divisor is non-zero 
    """

    if divisor == 0: 
        print 'Cannot divide by 0!'
    	return

    elif not (isinstance(dividend,int) & isinstance(divisor,int)): 
        print 'Dividend AND divisor must be integers.'
        return 

    while dividend >= divisor: 
        dividend -= divisor

    return dividend 
