(load "~/.emacs.d/config/package")

;; refresh package list if it is not already available
(when (not package-archive-contents) (package-refresh-contents))

(mapcar (lambda (package)
          ; install package if not already installed
          (unless (package-installed-p package)
            (message "Installing %s" package)
            (package-install package)))

        ; list of packages to be installed
        '(
          ; magit
          magit
          magit-svn
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
          markdown-mode
          ; go-lang
          go-mode
          company-go
          flycheck-gometalinter
          ; other stuff
          bind-key
          auctex
          ))
