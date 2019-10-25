(setq-default indent-tabs-mode nil)
(set-face-attribute 'default nil :height 150)
(setq-default fill-column 80)
(setq browse-url-generic-program (executable-find "firefox"))
(tool-bar-mode -1)

;; isearch wraps over new lines
(setq isearch-lax-whitespace t)
(setq isearch-regexp-lax-whitespace t)
(setq search-whitespace-regexp "[ \t\r\n]+")

;; tex
;; clean without confirmation
(setq TeX-clean-confirm nil)
(setq-default TeX-master 'shared)
;; save latex file and invoke latexmk on master tex file
(defun LaTeX-save-and-compile ()
  "Save and compile the tex project using latexmk.
If compilation fails, split the current window and open error-buffer
then jump to the error line, if errors corrected, close the error-buffer
window and close the *TeX help* buffer."
  (interactive)
  (progn
    (let ((TeX-save-query nil)
          (TeX-process-asynchronous nil)
          (master-file (TeX-master-file)))
      (TeX-save-document "")
      ;; clean all generated files before compile
      ;; DO NOT do it when up-to-date, remove this line in proper time
      (TeX-clean t)
      (TeX-run-TeX "latexmk"
                   (TeX-command-expand "latexmk -pdflatex='pdflatex -file-line-error -synctex=1' -pdf %s" 'TeX-master-file)
                   master-file)
      (if (plist-get TeX-error-report-switches (intern master-file))
          ;; avoid creating multiple windows to show the *TeX Help* error buffer
          (if (get-buffer-window (get-buffer "*TeX Help*"))
              (TeX-next-error)
            (progn
              (split-window-vertically -10)
              (TeX-next-error)))
        ;; if no errors, delete *TeX Help* window and buffer
        (if (get-buffer "*TeX Help*")
            (progn
              (if (get-buffer-window (get-buffer "*TeX Help*"))
                  (delete-windows-on "*TeX Help*"))
              (kill-buffer "*TeX Help*")))))))
(with-eval-after-load 'latex
  ;; TeX commands
  (add-to-list 'TeX-command-list
               '("latexmk" "latexmk -pdflatex='pdflatex -file-line-error -synctex=1' -pdf %s" TeX-run-command nil t :help "Run latexmk") t)
  (add-to-list 'TeX-command-list
               '("makeclean" "make clean" TeX-run-command t t :help "make clean") t)
  (add-to-list 'TeX-command-list
               '("make" "make" TeX-run-command t t :help "make") t)
  (setq TeX-command-default "make")

  ;; pdf view commands
  (push '("%(masterdir)" (lambda nil (file-truename (TeX-master-directory)))) TeX-expand-list)
  (add-to-list 'TeX-view-program-list
               '("okular" "/usr/bin/okular %o#src:%n%(masterdir)./%b"))
  (setcdr (assq 'output-pdf TeX-view-program-selection) '("okular"))

  ;; TeX-fold-mode customization
  (add-to-list 'LaTeX-fold-macro-spec-list
               '("{1}||*" ("item")))
  )
(add-hook 'LaTeX-mode-hook
          (lambda ()
            (TeX-fold-mode)
            (reftex-mode)
            (outline-minor-mode)
            (flyspell-mode)
            (flyspell-buffer)))

(add-hook 'doc-view-mode-hook
          'auto-revert-mode)

;; helm
(with-eval-after-load 'helm
  (setq helm-autoresize-max-height 50)
;;  (setq helm-autoresize-min-height 20)
  (helm-autoresize-mode 0)
  (setq helm-case-fold-search t)
  (helm-mode)
  )

;; fix dead_tilde issue due to fcitx
(require 'iso-transl)

;; gtags
(add-hook 'c++-mode-hook 'helm-gtags-mode)
(with-eval-after-load 'cc-mode
  (add-to-list 'company-backends 'company-gtags))

;; cc-mode
;; (require 'cc-mode)

;; company
(global-company-mode)

;; irony
(add-hook 'c++-mode-hook 'irony-mode)
;; removed, slows down ff-find-other-file
; (add-hook 'irony-mode-hook 'irony-cdb-autosetup-compile-options)

;; flycheck-irony
(with-eval-after-load 'flycheck
  (add-hook 'flycheck-mode-hook #'flycheck-irony-setup))

;; company-irony
(with-eval-after-load 'company
  (add-to-list 'company-backends 'company-irony))

;; company-go
(with-eval-after-load 'company
  (add-to-list 'company-backends 'company-go))

;; go
(add-hook 'go-mode-hook
          (lambda ()
            (add-hook 'before-save-hook 'gofmt-before-save)
            (setq-default)
            (setq tab-width 4)
            (setq standard-indent 4)
            (setq indent-tabs-mode t)))

;; markdown
(add-hook 'markdown-mode-hook
          (lambda ()
            (outline-minor-mode)
            (flyspell-mode)
            (flyspell-buffer)))

;; emacs lisp
(add-hook 'emacs-lisp-mode-hook
          (lambda ()
            (outline-minor-mode)))

;; ;; semantic
;; (require 'cc-mode)
;; (require 'semantic)

;; (global-semanticdb-minor-mode 1)
;; (global-semantic-idle-scheduler-mode 1)

;; (semantic-mode 1)

;; (require 'company)
;; (add-hook 'after-init-hook 'global-company-mode)

;; (setq company-backends (delete 'company-semantic company-backends))
;; (define-key c-mode-map  [(tab)] 'company-complete)
;; (define-key c++-mode-map  [(tab)] 'company-complete)
;; (setq company-clang-executable "~/scioncpp/build-tools/clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04/bin/clang++")

;; (require 'company-c-headers)
;; (add-to-list 'company-backends 'company-c-headers)
;; (add-to-list 'company-c-headers-path-system "~/scioncpp/build-tools/clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04/include/c++/v1")

;; (require 'cc-mode)
;; (require 'company)
;; (add-hook 'after-init-hook 'global-company-mode)
;; (define-key c-mode-map  [(tab)] 'company-complete)
;; (define-key c++-mode-map  [(tab)] 'company-complete)

;; ; irony
;; (add-hook 'c++-mode-hook 'irony-mode)

;; ; (add-hook 'irony-mode-hook 'irony-cdb-autosetup-compile-options)
;; (eval-after-load 'flycheck
;;   '(add-hook 'flycheck-mode-hook #'flycheck-irony-setup))
;; (eval-after-load 'company
;;   '(add-to-list 'company-backends 'company-irony))

(add-hook 'magit-mode-hook 'magit-svn-mode)
;; (magit-define-popup-option 'magit-diff-popup
;;   ?F "Filter by file status" "--diff-filter=" #'read-from-minibuffer)
;; todo: fix reading input from minibuffer
(transient-append-suffix 'magit-diff
                         "-w"
                         '("-F" "Filter by file status" "--diff-filter="'read-from-minibuffer))

;; i3
(load "~/.emacs.d/config/lib/i3wm-config-mode.el")
(load "~/.emacs.d/config/lib/i3wm.el")
(defun xdg (x)
  (interactive "f")
  (i3wm-exec (concat "xdg-open " x)))

;; tamarin
(load "~/.emacs.d/config/lib/spthy.el")

;; delight
(delight 'helm-mode)
;; somehow not working
;; (delight 'outline-minor-mode)

;; other useful stuff

;; ;; C-x C-s to use save-buffer for regular files and use sudo to prompt passwd to
;; ;; save file need root permission, C-x C-q to edit the root file first
;; ;; Note that this C-x C-s will fail if the buffer is not a file, in this case,
;; ;; use C-x C-w instead
;; (bind-keys* ("C-x C-s" .
;; 			 (lambda ()
;; 			   (interactive)
;; 			   (progn
;; 				 (if (file-writable-p buffer-file-name) (save-buffer)
;; (write-file (concat "/sudo:root@localhost:" buffer-file-name)))))))

;; org-mode
(setq org-latex-pdf-process (list "latexmk -xelatex -quiet -shell-escape -f %f"))

;; Org-Babel
(org-babel-do-load-languages
 'org-babel-load-languages
 '((ipython . t)))

(setq org-confirm-babel-evaluate nil)   ;don't prompt me to confirm everytime I want to evaluate a block

;; display/update images in the buffer after I evaluate
(add-hook 'org-babel-after-execute-hook 'org-display-inline-images 'append)

;; Org file directory
(setq org-agenda-files '("~/org"))

;; yasnippet
(setq yas-snippet-dirs
      '("~/.emacs.d/config/yasnippet/snippets"
        ))

(yas-global-mode 1) ;; or M-x yas-reload-all if you've started YASnippet already.

;; multi-term fix colors
(set-face-attribute 'term-color-blue nil :foreground "#5555FF")
(set-face-attribute 'term-color-green nil :foreground "#55FF55")
(set-face-attribute 'term-color-red nil :foreground "#FF5555")
(set-face-attribute 'term-color-magenta nil :foreground "#FF55FF")
(set-face-attribute 'term-color-cyan nil :foreground "#FF55FF")
(set-face-attribute 'term-color-yellow nil :foreground "#FFFF55")
(add-hook 'term-mode-hook
          (lambda ()
            (setq term-buffer-maximum-size 0)))
