import pathlib
import re

def ffmpeg_command(in_path_s, subsfile='', extra='', outdir='', *,
                   outfmt='mp4', binary='ffmpeg'):

    cmd_format = '{binary} -hide_banner -i "{in_path}" {extra} {subs} "{out}"'

    in_path = pathlib.Path(in_path_s)
    out_file_name = in_path.name.rstrip(in_path.suffix) + '.' + outfmt
    out_path = pathlib.Path(outdir).joinpath(out_file_name)
    subs_path = pathlib.Path(subsfile)
    if subs_path.suffix == '.ass':
        subs_filter = '-vf "ass={}"'.format(vf_quote(subsfile))
    else:
        subs_filter = '-vf "subtitles={}"'.format(vf_quote(subsfile))

    cmd = cmd_format.format(binary=binary, in_path=str(in_path), extra=extra,
                            subs=subs_filter, out=str(out_path))
    return cmd

def vf_quote(path):
    '''Quotes escape-sequences in subtitle path.
    Cursed videofilters string magic...
    '''
    path = path.replace('\\', '\\'*4)
    path = path.replace(':', r'\\:')    
    path = re.sub(r'([\[\]])', r'\\\1', path)
    return path
