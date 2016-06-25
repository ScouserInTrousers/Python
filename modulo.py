def modulo(dividend, divisor):
	"""This function imitates the modulo operator, %, for learning purposes.
	
	:arguments: 
		dividend: integer to be divided
		divisor: integer by which the dividend will be divided
	:returns: 
		remainder of the division problem  dividend / divisor as long as divisor is non-zero 
	"""
	if not all([isinstanceof(dividend,int), isinstanceof(divisor,int)]):
		print 'arguments must be integers'
		break
		
	if divisor == 0:
		print 'cannot divide by 0'
		break
		
	#To be edited later	
	return dividend % divisor
