(load "~/.emacs.d/config/package")

(mapcar (lambda (package)
          ; install package if not already installed
          (unless (package-installed-p package)
            (message "Installing %s" package)
            (package-install package)))

        ; list of packages to be installed
        '(magit
          ; helm
          helm
          ; wgrep
          wgrep
          wgrep-helm
          ; necessary dependencies
          s
          ; coding: gtags, irony, company, flycheck
          helm-gtags
          company
          irony
          company-irony
          flycheck
          flycheck-irony
          helm-flycheck
          ; markdown
          markdown-mode))
