#!/usr/bin/env python

from tkinter import *
from tkinter import messagebox
import pathlib
import json
import re

from widgets import *
from ffmpeg import *

class FfmpegWrapper(Tk):
    '''Main GUI class of application'''

    PROGRAM_TITLE='A GUI wrapper to ffmpeg'
    def __init__(self):
        super().__init__()

        self._extraopts = StringVar()
        self._ComposeWidgets()

        self.protocol('WM_DELETE_WINDOW', self._on_close)

        self.update() # Force window to place it's elements
        # Get size dimensions from geometry
        _self_x, _self_y, *_ = [int(i) for i in re.split('[x+]', self.geometry())]
        self.minsize(_self_x, _self_y)

    def _ComposeWidgets(self):
        self.title(self.PROGRAM_TITLE)
        self['padx'] = 2
        self['pady'] = 2

        # - Media files list
        fl_media = FilesList(self, 'Select media files:')
        fl_media.grid(row=0, column=0, sticky='nswe', padx=2, pady=2)
        self._media = fl_media

        # - Subtitles list
        fl_subtitles = FilesList(self, 'Select subtitles:')
        fl_subtitles.grid(row=0, column=1, sticky='nswe', padx=2, pady=2)
        self._subtitles = fl_subtitles

        # - Options frame
        fr_options = Frame(self)
        fr_options.grid(columnspan=2, sticky='we', padx=2, pady=2)

        fr_options.columnconfigure(0, weight=1)

        # -- Options label
        Label(fr_options, text='Other options').grid(sticky='w')

        # -- Output dir label
        Label(fr_options, text='Output dir:').grid(sticky='w')

        # -- Output dir selector
        dp_outdir = DirPath(fr_options)
        dp_outdir.grid(sticky='we')
        self._outdir = dp_outdir

        # -- Extra options label
        Label(fr_options, text='Extra options:').grid(sticky='w')

        # -- Extra options entry
        ent_extraopts = Entry(fr_options)
        ent_extraopts['textvariable'] = self._extraopts
        ent_extraopts.grid(sticky='we')

        # -- Export .bat button
        btn_exportbat = Button(fr_options)
        btn_exportbat['text'] = 'Export .bat'
        btn_exportbat['command'] = self._ExportBat
        btn_exportbat.grid(sticky='e')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def _ExportBat(self):
        ftypes = [('Batch script', '.bat')]
        bat_file = filedialog.asksaveasfile(filetypes=ftypes,
                                            defaultextension='.bat')

        extra = self._extraopts.get()
        outdir = self._outdir.GetPath()
        media_with_subs = zip(self._media.GetList(), self._subtitles.GetList())

        for m, s in media_with_subs:
            cmd =ffmpeg_command(m, s, extra, outdir)
            print(cmd, file=bat_file)

        bat_file.close()

        messagebox.showinfo(self.PROGRAM_TITLE, 'Success.')

    def save(self, path='.ffmpegwrapper'):
        options = {
            'extra': self._extraopts.get()
            }

        with open(path, mode='w') as file:
            json.dump(options, file)

    def load(self, path='.ffmpegwrapper'):
        if not pathlib.Path(path).exists():
            return

        with open(path) as file:
            options = json.load(file)
            self._extraopts.set(options.get('extra', ''))

    def _on_close(self):
        self.save()
        self.destroy()

if __name__ == '__main__':
    root = FfmpegWrapper()
    root.load()
    root.mainloop()
