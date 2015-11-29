from __future__ import unicode_literals

def format_quotes(string):
	if isinstance(string, str):
		string.replace('\"', r'\"')
		string.replace("\'", r"\'")
	return string

if __name__ == '__main__':
	
	foo = u'@cooijmanstim Thanks for picking this up.\r\n\r\n> we need to think about how to save/load the BN parameters. \r\n\r\nBy \\"saved\\" you mean serialized with a checkpoint? It seems like where to save that entire test-time graph is more the issue, isn\'t it? One would like to be able to get access to and evaluate it.\r\n\r\nOne thing I think we should leave up to the user is whether to adapt these via some additional squared error objective function passed as a term of the cost function to GradientDescent (which seems like a straightfoward and easy way to do it) or just via some simple moving average updates added with `add_updates`. In either case I don\'t think it\'s a problem to consider these quantities PARAMETERs as they don\'t appear in the train-time graph and therefore won\'t be adapted if you do gradient descent on the train-time graph\'s (single) output.\r\n\r\nThere\'s a larger arc to this story which is whether the graph substitution framework is really appropriate for this situation. Other frameworks are tackling this by adding a \\"Brick\\" equivalent into the original model object hierarchy, which makes it a little easier to figure out what\'s going on. In that kind of a setup, from a  Blocks perspective, we\'d essentially have two apply methods, one for train time and one for test time. In that situation, however, we\'d need some way of conveniently excluding the learned means and variances from gradient descent on the real objective function, which probably means a new parent role for PARAMETER, like ADAPTABLE or something.'

	try:
		print """ fail: "{}" """.format(foo)
	except Exception, e:
		print e

	foo = format_quotes(foo)	

	try:
		print """ succeed: "{}" """.format(foo)
	except Exception, e:
		print e
