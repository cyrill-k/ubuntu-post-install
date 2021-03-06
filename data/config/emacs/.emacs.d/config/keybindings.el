(require 'bind-key)
;; unbind suspend-frame keybinding
(global-unset-key (kbd "C-x C-z"))

;; outline minor mode hack
(global-unset-key (kbd "C-o"))
(setq outline-minor-mode-prefix (kbd "C-o"))

;; en-us C-z yanking
;; (global-unset-key (kbd "C-z"))
(global-set-key (kbd "C-z") 'yank)
(global-set-key (kbd "M-z") 'yank-pop)

;; crux
(global-set-key (kbd "C-c D") #'crux-duplicate-current-line-or-region)
(global-set-key (kbd "C-c M-d") #'crux-duplicate-and-comment-current-line-or-region)

;; global keybindings
(global-set-key (kbd "C-c k") 'windmove-up)
(global-set-key (kbd "C-c j") 'windmove-down)
(global-set-key (kbd "C-c h") 'windmove-left)
(global-set-key (kbd "C-c l") 'windmove-right)
(global-set-key (kbd "C-c s") 'ff-find-other-file)
(global-set-key (kbd "M-SPC") 'hippie-expand)
(global-set-key (kbd "C-c d") 'whack-whitespace)
(global-set-key (kbd "C-c f") 'rgrep)
(global-set-key (kbd "C-c r") 'find-name-dired)
(global-set-key (kbd "C-x g") 'magit-status)
;; (global-set-key (kbd "C-c v") 'copy-buffer-file-name-into-clipboard)
(global-set-key (kbd "C-c m m") (lambda (&optional arg) (interactive "P") (async-make-with-args "make" nil arg)))
(global-set-key (kbd "C-c m c") (lambda (&optional arg) (interactive "P") (async-make-with-args "make clean" nil arg)))
(global-set-key (kbd "C-c m r") (lambda (&optional arg) (interactive "P") (async-make-with-args "make clean; make" nil arg)))
;; (global-set-key (kbd "C-c n m") (lambda (&optional arg) (interactive "P") (async-make-with-args "make" t arg)))
;; (global-set-key (kbd "C-c n c") (lambda (&optional arg) (interactive "P") (async-make-with-args "make clean" t arg)))
;; (global-set-key (kbd "C-c n r") (lambda (&optional arg) (interactive "P") (async-make-with-args "make clean; make" t arg)))
(global-set-key (kbd "C-c o") (lambda (x) (interactive "f") (i3wm-exec (concat "xdg-open \"" x "\""))))
(global-set-key (kbd "C-c t") 'run-gnome-terminal-here)
(global-set-key (kbd "C-c w") 'open-link-or-image-or-url)
(global-set-key (kbd "C-c i") 'toggle-input-method)

;; helm global overrides
(global-set-key (kbd "M-x") 'helm-M-x)
(global-set-key (kbd "C-x b") 'helm-mini)
(global-set-key (kbd "C-x C-f") 'helm-find-files)
;; (global-set-key (kbd "C-c l") 'helm-locate)
(global-set-key (kbd "M-s o") 'helm-occur)
(global-set-key [mouse-8] (kbd "C-u C-<SPC>"))
(global-set-key (kbd "M-y") 'helm-show-kill-ring)
(global-set-key (kbd "C-h a") 'helm-apropos)
(global-set-key (kbd "C-c b") 'helm-all-mark-rings)

;; helm internal keybindings
(with-eval-after-load "helm"
  (define-key helm-map (kbd "<tab>") 'helm-execute-persistent-action) ; rebind tab to do persistent action
  (define-key helm-map (kbd "C-i") 'helm-execute-persistent-action) ; make TAB works in terminal
  (define-key helm-map (kbd "C-<tab>")  'helm-select-action) ; list actions using C-z
  )

;; helm-gtags key bindings
(with-eval-after-load "helm-gtags"
  (define-key helm-gtags-mode-map (kbd "M-t") 'helm-gtags-find-tag)
  (define-key helm-gtags-mode-map (kbd "M-r") 'helm-gtags-find-rtag)
  (define-key helm-gtags-mode-map (kbd "M-s") 'helm-gtags-find-symbol)
  (define-key helm-gtags-mode-map (kbd "M-g M-p") 'helm-gtags-parse-file)
  (define-key helm-gtags-mode-map (kbd "C-c g a") 'helm-gtags-tags-in-this-function)
  (define-key helm-gtags-mode-map (kbd "C-j") 'helm-gtags-select)
  (define-key helm-gtags-mode-map (kbd "M-.") 'helm-gtags-dwim)
  (define-key helm-gtags-mode-map (kbd "M-,") 'helm-gtags-pop-stack)
  (define-key helm-gtags-mode-map (kbd "C-c <") 'helm-gtags-previous-history)
  (define-key helm-gtags-mode-map (kbd "C-c >") 'helm-gtags-next-history))

;; company-mode
(global-set-key (kbd "C-c c") 'company-complete)
(with-eval-after-load "cc-mode"
  (define-key c++-mode-map "§" 'company-complete))

;; helm-flyspell
(with-eval-after-load 'flyspell
  (define-key flyspell-mode-map (kbd "C-;") 'helm-flyspell-correct)
  (define-key flyspell-mode-map (kbd "C-.") nil)
  (define-key flyspell-mode-map (kbd "C-,") nil))

;; LaTeX (bind-keys)
(with-eval-after-load 'latex
            (bind-keys :map LaTeX-mode-map
                       ("C-c b" . LaTeX-save-and-compile)
                       ;; default C-c C-e rebound and cannot be rebound
                       ;; ("C-c C-x e" . LaTeX-environment)
                       ;; ("C-c C-x s" . LaTeX-section)
                       ;; ("C-c C-x m" . TeX-insert-macro)
                       ;; default C-c. not working and replaced by org-time-stamp
                       ;; ("C-c m" . LaTeX-mark-environment)
                       ;; ("<tab>" . TeX-complete-symbol)
                       ;; ("M-<return>" . LaTeX-insert-item)
                       ))

;; isearch
(define-key isearch-mode-map (kbd "C-S-w") 'isearch-yank-char)
(define-key isearch-mode-map (kbd "C-z") 'isearch-yank-kill)
(define-key isearch-mode-map (kbd "M-z") 'isearch-yank-pop)
(define-key isearch-mode-map (kbd "M-s o") 'helm-multi-occur-from-isearch)

;; move text
(global-set-key (kbd "C-c n n") (defrepeater #'move-text-down))
(global-set-key (kbd "C-c n p") (defrepeater #'move-text-up))

;; scrollers
(global-set-key (kbd "M-n") (kbd "C-u 1 C-v"))
(global-set-key (kbd "M-p") (kbd "C-u 1 M-v"))

;; goto-chg
(global-set-key (kbd "C-.") 'goto-last-change)
(global-set-key (kbd "C-,") 'goto-last-change-reverse)

;; yasnippet
(with-eval-after-load 'yasnippet
  (bind-keys :map yas-minor-mode-map
             ("C-c y" . yas-insert-snippet)))

;; org-mode global
(global-set-key (kbd "C-c a") 'org-agenda)
(global-set-key (kbd "C-c n") 'org-capture)

;; org-mode
;; (define-key org-mode-map (kbd "C-c a") 'org-agenda)
(define-key org-mode-map (kbd "C-c q") 'toggle-truncate-lines)

;; multi-term
(global-unset-key (kbd "<f1>"))
(global-set-key (kbd "<f1>") 'multi-term)
(add-hook 'term-mode-hook
          (lambda ()
            (add-to-list 'term-bind-key-alist '("M-[" . multi-term-prev))
            (add-to-list 'term-bind-key-alist '("M-]" . multi-term-next))
            (define-key term-raw-map (kbd "C-y") 'term-paste)))

;; special mode
(global-set-key "s" 'global-s)
