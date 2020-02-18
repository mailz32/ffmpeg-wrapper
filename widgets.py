from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pathlib

class FilesList(Frame):
    ''' A widget to select and display multiple files sorted

    It has a title, a button and a listbox to view files.
    Clicking "Open files" button will pop up file selection dialog.
    If choosen a file or any files, they will be sorted and placed in
    listbox replacing existing contents.
    '''

    OPEN_TEXT = 'Open files'

    def __init__(self, master, title, **options):

        #options['padx'] = 2
        #options['pady'] = 2
        super().__init__(master, **options)

        self._files = StringVar()
        self._ComposeWidgets(title)

    def _ComposeWidgets(self, title):
        # - Title
        if title:
            Label(self, text=title).grid(columnspan=2, sticky='we')

        # - Frame with controls
        fr_controls = Frame(self)
        fr_controls.grid(row=1, columnspan=2, sticky='we')

        # -- 'Open files' button
        btn_open = Button(fr_controls)
        btn_open['text']=self.OPEN_TEXT
        btn_open['command']=self._AddFilesToList
        btn_open.pack(side=LEFT)

        # - List
        lst_files = Listbox(self)
        #lst_files['width'] = 80
        #lst_files['height'] = 8
        lst_files['listvariable'] = self._files
        lst_files.grid(sticky='nswe')

        # - Vertical scrollbar
        sbv_lst_files = ttk.Scrollbar(self)
        sbv_lst_files['orient'] = VERTICAL
        sbv_lst_files['command'] = lst_files.yview
        lst_files['yscrollcommand'] = sbv_lst_files.set
        sbv_lst_files.grid(row=2, column=1, sticky='ns')

        # - Horisontal scrollbar
        sbh_lst_files = ttk.Scrollbar(self)
        sbh_lst_files['orient'] = HORIZONTAL
        sbh_lst_files['command'] = lst_files.xview
        lst_files['xscrollcommand'] = sbh_lst_files.set
        sbh_lst_files.grid(row=3, column=0, sticky='we')

        # Make first column and 2nd row expandable
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

    def _AddFilesToList(self):
        tk_file_paths = filedialog.askopenfilenames()
        file_paths = [str(pathlib.Path(path)) for path in tk_file_paths]
        self._files.set(sorted(file_paths, key=str.lower))

    def GetList(self) -> list:
        '''Returns a list of file paths which are present inside widget'''
        return list( eval(self._files.get()) ) # i hope that's save to eval

class DirPath(Frame):
    def __init__(self, master, **options):
        super().__init__(master, **options)

        self._dirpath = StringVar()
        self._ComposeWidgets()

    def _ComposeWidgets(self):
        # - Edit with dir path
        ent_path = Entry(self, state='readonly')
        ent_path['textvariable'] = self._dirpath
        ent_path.grid(sticky='we')

        # - 'Open' button
        btn_select_dir = Button(self)
        btn_select_dir['text'] = 'Open'
        btn_select_dir['command'] = self._SelectDirectory
        btn_select_dir.grid(row=0, column=1)

        # Make first column expandable
        self.columnconfigure(0, weight=1)

    def _SelectDirectory(self):
        tk_path = filedialog.askdirectory()
        self._dirpath.set(str(pathlib.Path(tk_path)))

    def GetPath(self) -> str:
        '''Returns a selected dir path'''
        return self._dirpath.get()
