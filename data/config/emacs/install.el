(load "~/.emacs.d/config/package.el")

;; refresh package list if it is not already available
(when (not package-archive-contents) (package-refresh-contents))

(mapcar (lambda (package)
          ; install package if not already installed
          (unless (package-installed-p package)
            (message "Installing %s" package)
            (package-install package)))

        ; list of packages to be installed
        '(use-package))
