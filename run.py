#!/usr/bin/env python
from cmd import Cmd
import os
import inspect
from pathlib import Path
from shutil import copyfile, copytree, rmtree
from subprocess import run

join = os.path.join
class Install:
    def __init__(self):
        run(['sudo', 'apt', 'update'])

    def _apt_install(self, package):
        run(['sudo', 'apt', '-y', 'install', package])

    def _apt_remove(self, package):
        run(['sudo', 'apt', '-y', 'remove', package])

    def i3(self, inp):
        self._apt_install('i3')

    def emacs(self, inp):
        print('removing old emacs installations')
        self._apt_remove('emacs*')
        print('installing emacs25')
        self._apt_install('emacs25')

class Configure:
    def __init__(self):
        self.i3path = join(os.getcwd(),'data','config','i3')
        self.i3configpath = join(Path.home(), '.config','i3')
        self.i3statuspath = join(os.getcwd(),'data','config','i3status')
        self.i3statusconfigpath = join(Path.home(),'.config','i3status')
        self.emacspath = join(Path.home(),'data','config','emacs')
        self.emacshomeconfigfolder = join(Path.home(),'.emacs.d')
        self.emacshomeconfigfile = join(Path.home(),'.emacs')

    def i3(self, inp):
        p_base = join(self.i3path, '.base')
        p = join(self.i3path, inp[0])
        c = join(self.i3configpath,'config')
        if not os.path.isdir(self.i3configpath):
            os.makedirs(self.i3configpath)
        copyfile(p_base, c)
        with open(p) as pf, open(c,'a') as cf:
            cf.write(pf.read())
        print(f"i3: wrote {c}")

        print("Adding Nautilus i3 fix")
        run(['gsettings', 'set', 'org.gnome.desktop.background', 'show-desktop-icons', 'false'])

    def i3_args(self):
        return [p for p in os.listdir(self.i3path) if not p.startswith(".") and not p.endswith("~")]

    def i3status(self, inp):
        p = join(self.i3statuspath, inp[0])
        c = join(self.i3statusconfigpath,'config')
        if not os.path.isdir(self.i3statusconfigpath):
            os.makedirs(self.i3statusconfigpath)
        copyfile(p, c)
        print(f"i3status: wrote {c}")

    def i3status_args(self):
        return [p for p in os.listdir(self.i3statuspath) if not p.startswith(".") and not p.endswith("~")]

    def emacs(self, inp):
        print('removing existing config files')
        rmtree(join(Path.home(),'.emacs.d'))
        os.remove(join(Path.home(),'.emacs'))
        print('copying config files')
        copytree(join(self.emacspath, '.emacs.d'), join(Path.home(), '.emacs.d'))
        print('running emacs install script')
        run(['emacs', '--script', join(self.emacspath,'install.el')])

class MyPrompt(Cmd):
    prompt_map = {'default': 'ubuntu config manager> ',
                  'install': 'install> ',
                  'config': 'configure> '}
    prompt = prompt_map['default']
    intro = 'select which ubuntu configs to install'
    
    def do_exit(self, inp):
        print("Bye")
        return True
 
    def do_install(self, inp):
        #prompt = prompt_map['install']
        args = inp.split(" ")
        argIndex = len(args)-1
        getattr(Install(), args[0])(args[1:])

    def complete_install(self, text, line, begidx, endidx):
        args = line.split(" ")
        argIndex = len(args)-1
        if argIndex == 1:
            return self.get_args(text, [x[0] for x in inspect.getmembers(Install, predicate=inspect.isfunction) if not x[0].startswith('_')])

    def do_configure(self, inp):
        #prompt = self.prompt_map['config']
        args = inp.split(" ")
        argIndex = len(args)-1
        getattr(Configure(), args[0])(args[1:])

    def complete_configure(self, text, line, begidx, endidx):
        args = line.split(" ")
        argIndex = len(args)-1
        if argIndex == 1:
            return self.get_args(text, [x[0] for x in inspect.getmembers(Configure, predicate=inspect.isfunction) if not x[0].endswith('_args') and not x[0].startswith('__')])
        elif argIndex == 2:
            return self.get_args(text,getattr(Configure(), args[1]+'_args')())
    
    def default(self, inp):
        if inp == 'e' or inp == 'q':
            return self.do_exit(inp)
 
        print("Default: {}".format(inp))

    def get_args(self, prefix, l):
        return [x for x in l if x.startswith(prefix)]

    do_EOF = do_exit

MyPrompt().cmdloop()
