#!/usr/bin/env python3
from cmd import Cmd
import os
import inspect
from pathlib import Path
from shutil import copyfile, copytree, rmtree
from distutils import dir_util
import subprocess
import re
import glob
import stat
import errno

run = subprocess.run
rm = os.remove
join = os.path.join
root = os.path.dirname(os.path.realpath(__file__))
home = Path.home()
dirname = os.path.dirname


def shellrun(cmd):
    return run(" ".join(cmd), shell=True)


class Helper:
    def apt_update(self):
        run(["sudo", "apt", "update"])

    def apt_install(self, package):
        run(["sudo", "apt", "-y", "install", package])

    def apt_remove(self, package):
        run(["sudo", "apt", "-y", "remove", package])

    def git_clone(self, remote, dst, options):
        """Clone `remote` into `dst` folder with git options as list (e.g., options =
        ['--depth','1'])"""
        if os.path.isdir(dst):
            rmtree(dst)
        cmd = ["git", "clone"]
        cmd.extend(options)
        cmd.append(remote)
        cmd.append(dst)
        print(f"Executing {cmd}")
        run(cmd)

    def binary_exists(self, binary):
        # this approach does not consider changes to the environment variable PATH
        # """check if binary exists using distutils.spawn.find_executable"""
        # return find_executable(binary) is not None
        bash_config_files = [join(home, ".bashrc"), join(home, ".bashrc_extended")]
        cmd = "; ".join([f"[ -f {x} ] && source {x}" for x in bash_config_files])
        cmd += f"; which {binary}"
        return run(["/bin/bash", "-c", cmd], stdout=subprocess.DEVNULL).returncode == 0

    def append_to_file(self, src, content):
        with open(src, "a+") as f:
            f.seek(0, os.SEEK_END)
            f.write(content)

    def pip_install(self, package):
        print("pip update --upgrade pip")
        print(f"pip install {package}")

    def venv_run(self, venv_folder, cmd):
        return run(
            ["/bin/bash", "-c", f'source {join(venv_folder, "bin", "activate")}; {cmd}']
        )


helper = Helper()


class Install:
    def i3(self, inp):
        helper.apt_update()
        helper.apt_install("i3")

    def emacs(self, inp):
        helper.apt_update()
        if inp[0] == "apt":
            if not helper.binary_exists("emacs"):
                print("removing old emacs installations")
                helper.apt_remove("emacs*")
                print("installing emacs")
                helper.apt_install("emacs")
        elif inp[0] == "source":
            print("wget http://mirror.inode.at/gnu/emacs/emacs-26.3.tar.gz")
            print("tar -xzvf emacs-26.3.tar.gz")
            print("cd emacs-26.3")
            print("sudo apt-get install build-essential texinfo libx11-dev libxpm-dev libjpeg-dev libpng-dev libgif-dev libtiff-dev libgtk2.0-dev libncurses-dev libxpm-dev automake autoconf libgnutls28-dev")
            print("./configure --with-modules")
            print("make")
            print("sudo make install")
        if not helper.binary_exists("fzf"):
            self.fzf([])
        helper.apt_install("global")

    def emacs_args(self):
        return ["apt", "source"]

    def fzf(self, inp):
        helper.git_clone(
            "https://github.com/junegunn/fzf.git", join(home, ".fzf"), ["--depth", "1"]
        )
        print("installing fzf")
        run([join(home, ".fzf/install"), "--all"])

    def mysqlserver(self, inp):
        helper.apt_update()
        helper.apt_install("mysql-server")

    def ietftools(self, inp):
        helper.apt_update()
        helper.apt_install("enscript")
        helper.apt_install("gem")
        run(["sudo", "gem", "install", "kramdown-rfc2629"])
        helper.pip_install("xml2rfc")

    def japanese(self, inp):
        helper.apt_update()
        helper.apt_install("fcitx-mozc")

    def tmux(self, inp):
        helper.apt_update()
        helper.apt_install("tmux")

    def xkeysnail(self, inp):
        helper.pip_install("xkeysnail")
        print("xhost +SI:localuser:root")
        print(
            f"sudo xkeysnail {join(root, 'data', 'config', 'xkeysnail', 'config.py')}"
        )

    def localbin(self, inp):
        helper.apt_update()
        for p in ["maim"]:
            helper.apt_install(p)
        os.makedirs(join(home, ".local", "bin"), exist_ok=True)
        r = join(root, "data", "config", "local-bin")
        for src in next(os.walk(r))[2]:
            dst = join(home, ".local", "bin", os.path.basename(src))
            copyfile(join(r, src), dst)
            st = os.stat(dst)
            os.chmod(dst, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    def go(self, inp):
        tarFile = f'go{inp[0]}.linux-amd64.tar.gz'
        run(['wget', f'https://dl.google.com/go/{tarFile}'])
        try:
            run(['sudo', 'tar', '-C', '/usr/local', '-xzf', tarFile])
        finally:
            rm(tarFile)

    def go_args(self):
        return ['1.13.12']


class Configure:
    def __init__(self):
        self.i3path = join(root, "data", "config", "i3")
        self.i3statuspath = join(root, "data", "config", "i3status")
        self.emacspath = join(root, "data", "config", "emacs")

    def i3(self, inp):
        p_base = join(self.i3path, ".base")
        p = join(self.i3path, inp[0])
        c = join(home, ".config", "i3", "config")
        os.makedirs(dirname(c), exist_ok=True)
        copyfile(p_base, c)
        with open(p) as pf, open(c, "a") as cf:
            cf.write(pf.read())
        print(f"i3: wrote {c}")

        print("Adding Nautilus i3 fix")
        run(
            [
                "gsettings",
                "set",
                "org.gnome.desktop.background",
                "show-desktop-icons",
                "false",
            ]
        )

    def i3_args(self):
        return [
            p
            for p in os.listdir(self.i3path)
            if not p.startswith(".") and not p.endswith("~")
        ]

    def i3status(self, inp):
        p = join(self.i3statuspath, inp[0])
        c = join(home, ".config", "i3status", "config")
        os.makedirs(dirname(c), exist_ok=True)
        copyfile(p, c)
        print(f"i3status: wrote {c}")

    def i3status_args(self):
        return [
            p
            for p in os.listdir(self.i3statuspath)
            if not p.startswith(".") and not p.endswith("~")
        ]

    def emacs(self, inp):
        if inp[0] == "clean-install":
            print("removing existing config files")
            if os.path.isdir(join(home, ".emacs.d")):
                rmtree(join(home, ".emacs.d"))
            if os.path.isfile(join(home, ".emacs")):
                os.remove(join(home, ".emacs"))
            print("copying config files")
            copytree(join(self.emacspath, ".emacs.d"), join(home, ".emacs.d"))
        else:
            print("copying config files")
            dir_util.copy_tree(join(self.emacspath, ".emacs.d"), join(home, ".emacs.d"))
        helper.git_clone(
            "https://github.com/ibmandura/helm-fzf",
            join(home, ".emacs.d", "helm-fzf"),
            [],
        )
        print("running emacs install script")
        run(["emacs", "--script", join(self.emacspath, "install.el")])

    def emacs_args(self):
        return ["update-only", "clean-install"]

    def profile(self, inp):
        self._modify_option_wrapper(inp[0], "profile")

    def profile_args(self):
        return ["replace", "extend"]

    def bashrc(self, inp):
        self._modify_option_wrapper(inp[0], "bashrc")

    def bashrc_args(self):
        return ["replace", "extend"]

    def bashaliases(self, inp):
        self._modify_option_wrapper(inp[0], "bash_aliases")

    def bashaliases_args(self):
        return ["extend"]

    def sshd(self, inp):
        if not os.path.isfile(join(home, ".ssh", "id_ed25519_vm")):
            run(
                [
                    "ssh-keygen",
                    "-t",
                    "ed25519",
                    "-q",
                    "-N",
                    "",
                    "-f",
                    join(home, ".ssh", "id_ed25519_vm"),
                ]
            )
            with open(join(home, ".ssh", "id_ed25519_vm.pub"), "r") as private_key:
                helper.append_to_file(
                    join(home, ".ssh", "authorized_keys"), private_key.read()
                )
        helper.apt_install("openssh-server")

    def trillianmysql(self, inp):
        print(
            "# first command should be enough; kept remaining user commands for reference"
        )
        print(
            "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';"
        )
        print("FLUSH PRIVILEGES;")
        print()
        print(
            "CREATE USER 'test'@'localhost' IDENTIFIED WITH mysql_native_password BY 'zaphod';"
        )
        print(
            "GRANT ALL PRIVILEGES ON *.* TO 'test'@'localhost' "
            "IDENTIFIED WITH mysql_native_password BY 'zaphod';"
        )
        print()
        print("DROP USER 'root'@'localhost';")
        print("CREATE USER 'root'@'localhost' IDENTIFIED BY '';")
        print("GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY '';")
        print()
        print("CREATE USER 'cyrill'@'localhost' IDENTIFIED BY '';")
        print("GRANT ALL PRIVILEGES ON *.* TO 'cyrill'@'localhost' IDENTIFIED BY '';")
        print("FLUSH PRIVILEGES")
        print()
        # print("update user set authentication_string=password('') where user='root';")
        print("SET GLOBAL max_connections = 1000;")

    def elpy(self, inp):
        helper.apt_install("python-virtualenv")
        helper.apt_install("python3-venv")
        venvs = join(home, ".virtualenvs")
        if not os.path.exists(venvs):
            print(f"creating python virtualenv folder {venvs}")
            os.makedirs(venvs)
        venv_path = join(venvs, "elpy-python3")
        run(["python3", "-m", "venv", venv_path])
        helper.venv_run(venv_path, "pip install --upgrade pip")
        helper.venv_run(venv_path, "pip install rope jedi importmagic autopep8 flake8")

    def japanese(self, inp):
        xinputrcIn = join(root, "data", "config", "xinputrc.in")
        xinputrcOut = join(home, ".xinputrc")
        copyfile(xinputrcIn, xinputrcOut)

    def tmux(self, inp):
        copyfile(
            join(root, "data", "config", "tmux", ".tmux.conf"), join(home, ".tmux.conf")
        )

    def firefox(self, inp):
        self._add_firefox_user_pref('"browser.fullscreen.autohide"', "false")
        self._add_firefox_user_pref('"ui.key.menuAccessKeyFocuses"', "false")

    def xkeysnail(self, inp):
        configFile = join(home, ".config", "xkeysnail", "config.py")
        os.makedirs(dirname(configFile), exist_ok=True)
        copyfile(join(root, "data", "config", "xkeysnail", "config.py"), configFile)

    def docker(self, inp):
        shellrun(['sudo', 'groupadd', 'docker'])
        shellrun(['sudo', 'usermod', '-G', 'docker', '$USER'])
        print('# reboot system')
        print('sudo reboot')

    def aspell(self, inp):
        self._append_if_not_found("/etc/aspell.conf", r"^home-dir.*", "home-dir /home/cyrill/.emacs.d/config/aspell")

    # def elpy(self, inp):
    #     folder = join(home, '.emacs.d', 'elpy')
    #     if not os.path.isdir(folder):
    #         os.makedirs(folder)
    #     run(['python3', '-m', 'venv', join(folder, 'rpc-venv')])

    def _add_firefox_user_pref(self, key, val):
        try:
            firefoxDir = join(home, ".mozilla", "firefox")
            dirs = glob.glob(join(firefoxDir, "*.default"))
            dirs.extend(glob.glob(join(firefoxDir, "*.default-release")))
            for d in dirs:
                f = join(d, "user.js")
                p = f"user_pref({key},{val});\n"
                self._append_if_not_found(f, re.escape(key), p)
        except Exception as e:
            print(f"error while adding firefox user pref: {e}")

    def _add_shell_include(self, shell_include, base):
        self._append_if_not_found(
            base,
            rf"\. {shell_include}",
            f"""
if [ -f {shell_include} ]; then
    . {shell_include}
fi""",
        )

    #         with open(base, "a+") as origin_file:
    #             origin_file.seek(0, os.SEEK_SET)
    #             for line in origin_file:
    #                 if re.findall(rf'\. {shell_include}', line):
    #                     return
    #             print(f"Adding include statement to {base}")
    #             origin_file.seek(0, os.SEEK_END)
    #             origin_file.write(f'''
    # if [ -f {shell_include} ]; then
    #     . {shell_include}
    # fi''')

    def _append_if_not_found(self, f, searchRegex, append):
        try:
            with open(f, "a+") as origin_file:
                origin_file.seek(0, os.SEEK_SET)
                for line in origin_file:
                    if re.findall(searchRegex, line):
                        return
                print(f"Adding include statement to {f}")
                origin_file.seek(0, os.SEEK_END)
                origin_file.write(append)
        except IOError as e:
            if e.errno == errno.EACCES:
                print(f"not enough permissions to read and write {f}. Call run.py using sudo")
                exit(1)

    def _modify_option(
        self, basic_src, extended_src, basic_dst, extended_dst_shell_path
    ):
        """extended_dst_shell_path uses ~ to represent $HOME"""
        if basic_src:
            print(f"replacing {basic_dst}")
            copyfile(basic_src, basic_dst)
        if extended_src:
            print(f"replacing {extended_dst_shell_path}")
            copyfile(extended_src, os.path.expanduser(extended_dst_shell_path))
            self._add_shell_include(extended_dst_shell_path, basic_dst)

    def _modify_option_wrapper(self, cmd, filename):
        if cmd == "replace":
            basic_src = join(root, "data", "config", f"{filename}_basic.in")
        else:
            basic_src = None
        self._modify_option(
            basic_src,
            join(root, "data", "config", f"{filename}_extended.in"),
            join(home, f".{filename}"),
            f"~/.{filename}_extended",
        )


class MyPrompt(Cmd):
    prompt_map = {
        "default": "ubuntu config manager> ",
        "install": "install> ",
        "config": "configure> ",
    }
    prompt = prompt_map["default"]
    intro = "select which ubuntu configs to install"

    def do_exit(self, inp):
        print("Bye")
        return True

    def do_install(self, inp):
        # prompt = prompt_map['install']
        args = inp.split(" ")
        # argIndex = len(args) - 1
        getattr(Install(), args[0])(args[1:])

    def complete_install(self, text, line, begidx, endidx):
        args = line.split(" ")
        argIndex = len(args) - 1
        if argIndex == 1:
            return self.get_args(
                text,
                [
                    x[0]
                    for x in inspect.getmembers(Install, predicate=inspect.isfunction)
                    if not x[0].endswith("_args") and not x[0].startswith("_")
                ],
            )
        elif argIndex == 2:
            return self.get_args(text, getattr(Install(), args[1] + "_args")())

    # def complete_install(self, text, line, begidx, endidx):
    #     args = line.split(" ")
    #     argIndex = len(args) - 1
    #     if argIndex == 1:
    #         return self.get_args(
    #             text,
    #             [
    #                 x[0]
    #                 for x in inspect.getmembers(Install, predicate=inspect.isfunction)
    #                 if not x[0].startswith("_")
    #             ],
    #         )

    def do_configure(self, inp):
        # prompt = self.prompt_map['config']
        args = inp.split(" ")
        # argIndex = len(args) - 1
        getattr(Configure(), args[0])(args[1:])

    def complete_configure(self, text, line, begidx, endidx):
        args = line.split(" ")
        argIndex = len(args) - 1
        if argIndex == 1:
            return self.get_args(
                text,
                [
                    x[0]
                    for x in inspect.getmembers(Configure, predicate=inspect.isfunction)
                    if not x[0].endswith("_args") and not x[0].startswith("_")
                ],
            )
        elif argIndex == 2:
            return self.get_args(text, getattr(Configure(), args[1] + "_args")())

    def default(self, inp):
        if inp == "e" or inp == "q":
            return self.do_exit(inp)

        print("Default: {}".format(inp))

    def get_args(self, prefix, l):
        return [x for x in l if x.startswith(prefix)]

    do_EOF = do_exit


MyPrompt().cmdloop()
