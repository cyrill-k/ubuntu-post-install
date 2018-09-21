;; helm-gtags-fuzzy-match needs to be called before package-initialize
(custom-set-variables
 '(helm-gtags-ignore-case t)
 '(helm-gtags-auto-update t)
 '(helm-gtags-use-input-at-cursor t)
 '(helm-gtags-pulse-at-cursor t)
 '(helm-gtags-prefix-key "\C-cg")
 '(helm-gtags-suggested-key-mapping t)
 '(helm-gtags-fuzzy-match t)
 '(helm-gtags-path-style 'relative)
 '(grep-find-command
   (quote
    ("find . -type f -exec grep --color -nHi -e '' {} +" . 44)))
 '(inhibit-startup-screen t))

(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )

;; Added by Package.el.  This must come before configurations of
;; installed packages.  Don't delete this line.  If you don't want it,
;; just comment it out by adding a semicolon to the start of the line.
;; You may delete these explanatory comments.
(package-initialize)

(load "~/.emacs.d/config/package")
(load "~/.emacs.d/config/config")
(load "~/.emacs.d/config/functions")
(load "~/.emacs.d/config/keybindings")

(load "~/.emacs.d/helm-fzf/helm-fzf.el")
