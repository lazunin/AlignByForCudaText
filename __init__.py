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
		#if row2 < 0: return None
		if any(x < 0 for x in (col1, row1, col2, row2)): return None
		col1 = 0 # the entire first line, including possibly missing leading spaces
		return col1, row1, col2, row2
	
	def run(self):
		sel = self.get_selection()
		if not sel: return
		s   = ed.get_text_substr(*sel)
		s   = align_by_symbol(s, '=')
		ed.replace(*sel, s)
	
	def align_selection_by(self, delimeter):
		sel = self.get_selection()
		s   = ed.get_text_substr(*sel)
		s   = align_by_symbol(s, delimeter)
		ed.replace(*sel, s)
	
	def callback_maindlg(self, id_dlg, id_ctl, data='', info=''):
		h = id_dlg
		n_edit = dlg_proc(h, DLG_CTL_FIND, prop='edit_delimeter')
		d = dlg_proc(h, DLG_CTL_PROP_GET, index=n_edit)
		delimeter = d['val']
		self.align_selection_by(delimeter)
	
	def run_with_dlg(self):
		h=dlg_proc(0, DLG_CREATE)
		dlg_proc(h, DLG_PROP_SET, prop={
			'cap'     : 'Align by',
			'x'       : 100,
			'y'       : 50,
			'w'       : 220,
			'h'       : 100,
			'w_min'   : 200,
			'h_min'   : 100,
			'border'  : DBORDER_SIZE,
			'topmost' : True,
			})
		
		n=dlg_proc(h, DLG_CTL_ADD, 'label')
		dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={
			'name' : 'label0',
			'cap'  : 'Delimeter: ',
			'x'    : 10,
			'y'    : 10,
			'w'    : 50,
			'tag'  : 'some_tag',
			})
		
		n=dlg_proc(h, DLG_CTL_ADD, 'edit')
		dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={
			'name' : 'edit_delimeter',
			'val'  :'',
			'x'    : 10,
			'y'    : 30,
			'w'    : 200,
			})
		
		n=dlg_proc(h, DLG_CTL_ADD, 'button')
		dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={
			'name'      : 'btn_align',
			'cap'       : 'Align',
			'x'         : 10,
			'y'         : 60,
			'w'         : 100,
			'on_change' : 'cuda_align_by.callback_maindlg'
			})
		
		dlg_proc(h, DLG_SHOW_NONMODAL)