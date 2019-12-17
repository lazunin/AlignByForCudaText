
# TODO: maybe later
#import string
#special = list(string.punctuation)
multi = set(["**", "//", "==", "!=", "<>", ">=", "<=", "+=", "-=", "*=", "/=", "%=", "**=", "//=", "<<", ">>"])

def is_op(left, right, sep):
    '''
    Check if it was split inside a multi-character operator.
    '''
    if len(left.strip()) == 0: return False
    return ((left[-1:] + sep) in multi) or ((left[-2:] + sep) in multi) or ((left[-1:] + sep + right[:1]) in multi) or ((sep + right[:1]) in multi) or ((sep + right[:2]) in multi)
    
    
def tabbed_length(s):
	'''
	Length of the string if the tabs were expanded into 4 spaces.
	'''
	TAB_SIZE = 4
	filler   = '*'*TAB_SIZE
	s2       = s.replace("\t", filler)
	return len(s2)

def special_split(s, sep):
	'''
	Split string once, starting from the left, trying to avoid splitting
	in the middle of multi-character operators, e. g. !=, /=, +=, == etc.
	'''
	lr = s.split(sep, 1)
	if len(lr) != 2: return lr
	l, r = lr
	#if not (l[-1].isalnum() or l[-1].isspace()): return (s,) # no splitting in the middle of !=, += etc.?
	if is_op(l, r, sep): return (s, )
	l = l.rstrip() + " "
	return l, r    
	
def align_by_symbol(text, sep):
	'''
	Modyfy text, so that first occurences of `sep`
	are vertically aligned.
	'''
	lines        = text.splitlines(True)
	lines        = [special_split(s, sep) for s in lines]
	left_max_len = max([tabbed_length(s[0]) if len(s) == 2 else 0 for s in lines])
	lines2       = []
	for line in lines:
		if len(line) != 2:
			result = line[0]
		else:
			result = line[0] + ' '*(left_max_len - tabbed_length(line[0])) + sep + line[1]
		lines2.append(result)
	return "".join(lines2)