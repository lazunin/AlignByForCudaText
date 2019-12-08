import os
from cudatext import *
from .helper_fn import align_by_symbol

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_align_by.ini')

option_int = 100
option_bool = True

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s == '1'
			
class Command:
	
	def __init__(self):
		
		
		global option_int
		global option_bool

		option_int  = int(ini_read(fn_config, 'op', 'option_int', str(option_int)))
		option_bool = str_to_bool(ini_read(fn_config, 'op', 'option_bool', bool_to_str(option_bool)))

	def config(self):

		ini_write(fn_config, 'op', 'option_int', str(option_int))
		ini_write(fn_config, 'op', 'option_bool', bool_to_str(option_bool))
		file_open(fn_config)
	
	def get_selection(self):
		'''
		Selection (col1, row1, col2, row2), but col1 is set to 0,
		so that the entire first line is selected.
		'''
		col1, row1, col2, row2  = ed.get_carets()[0]
		if (row1, col1) > (row2, col2):
			col1, row1, col2, row2 = col2, row2, col1, row1
		if row2 < 0: return None
		col1 = 0 # the entire first line, including possibly missing leading spaces
		return col1, row1, col2, row2   
	
	def run(self):
		sel = self.get_selection()
		s   = ed.get_text_substr(*sel)
		s   = align_by_symbol(s, '=')
		ed.replace(*sel, s)
		

