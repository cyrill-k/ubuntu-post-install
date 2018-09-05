(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
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

(load "~/.emacs.d/config/package")
(load "~/.emacs.d/config/config")
(load "~/.emacs.d/config/functions")
(load "~/.emacs.d/config/keybindings")

(load "~/.emacs.d/helm-fzf/helm-fzf.el")
