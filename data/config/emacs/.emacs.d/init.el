;; helm-gtags-fuzzy-match needs to be called before package-initialize
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(custom-enabled-themes (quote (tango-dark)))
 '(grep-command "grep --color -nHi -e ")
 '(grep-find-command
   (quote
    ("find . -type f -exec grep --color -nHi -e '' {} +" . 44)))
 '(grep-find-template "find <D> <X> -type f <F> -exec grep <C> -nHi -e <R> {} +")
 '(grep-highlight-matches (quote auto))
 '(grep-template "grep <X> <C> -nHi -e <R> <F>")
 '(grep-use-null-device nil)
 '(helm-gtags-auto-update t)
 '(helm-gtags-fuzzy-match t)
 '(helm-gtags-ignore-case t)
 '(helm-gtags-path-style (quote relative))
 '(helm-gtags-prefix-key "g")
 '(helm-gtags-pulse-at-cursor t)
 '(helm-gtags-suggested-key-mapping t)
 '(helm-gtags-use-input-at-cursor t)
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

(load "~/.emacs.d/config/package.el")
(load "~/.emacs.d/config/config.el")
(load "~/.emacs.d/config/functions.el")
(load "~/.emacs.d/config/keybindings.el")

(load "~/.emacs.d/helm-fzf/helm-fzf.el")
