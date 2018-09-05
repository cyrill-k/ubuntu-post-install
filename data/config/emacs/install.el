(load "~/.emacs.d/config/package")

(mapcar (lambda (package)
          ; install package if not already installed
          (unless (package-installed-p package)
            (message "Installing %s" package)
            (package-install package)))

        ; list of packages to be installed
          '(helm
            wgrep
            wgrep-helm
            magit
            s))
