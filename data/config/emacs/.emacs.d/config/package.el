;; melpa for magit
(require 'package)
(add-to-list 'package-archives
             '("melpa" . "http://melpa.org/packages/") t)
(package-initialize)
(package-refresh-contents)

(setq package-archive-priorities
      '(("gnu" . 0)
        ("melpa" . 10)))

(unless (require 'use-package nil 'noerror)
  (package-install 'use-package)
  (require 'use-package))

;; always install packages
(require 'use-package-ensure)
(setq use-package-always-ensure t)

;; auto update packages
;; (use-package auto-package-update
;;   :config
;;   (setq auto-package-update-delete-old-versions t)
;;   (setq auto-package-update-hide-results t)
;;   (auto-package-update-maybe))

;; delight
;; if gnu repository is not loaded because gpg key is expired, download
;; https://elpa.gnu.org/packages/gnu-elpa-keyring-update-2019.3.tar and install using
;; M-x package-install-file
(use-package delight)

;; emacs config management
(use-package bind-key)

;; general
(use-package goto-chg)
(use-package fcitx)

;; magit
(use-package magit)
(use-package magit-svn
             :after magit)

;; fixes
(use-package s)

;; helm
(use-package helm)
(use-package wgrep-helm
             :after helm)
(use-package helm-ispell
             :after helm)
(use-package helm-gtags
             :after helm)
(use-package helm-flyspell
             :after helm)
(use-package helm-flycheck
             :after (helm elpy)
             :config
             (setq elpy-modules (delq 'elpy-module-flymake elpy-modules))
             (add-hook 'elpy-mode-hook 'flycheck-mode)
             (setq-default flycheck-flake8-maximum-line-length 99)
             :init (global-flycheck-mode))

;; company
(use-package company
             :delight company-mode)

;; golang
(use-package flycheck-gometalinter)
;; (use-package company-go)
(use-package go-eldoc)
(setq lsp-keymap-prefix (kbd "C-c q"))
(use-package lsp-mode
  :commands (lsp lsp-deferred)
  :hook (go-mode . lsp-deferred))

;; (use-package lsp-ui
;;   :commands lsp-ui-mode
;;   :hook
;;   (lsp-mode . lsp-ui-mode))

(use-package helm-lsp
  :commands helm-lsp-workspace-symbol)

;; (use-package company-lsp
;;   :commands company-lsp
;;   :config (push 'company-lsp company-backends))

;; irony
(use-package flycheck-irony)
(use-package company-irony)

;; markdown
(use-package markdown-mode)

;; LaTeX
(use-package auctex
             :defer t)
(use-package auto-complete-auctex
             :defer t)

;; org
(use-package org)

;; ob-ipython (emacs jupyter support)
(use-package ob-ipython
             :after org)

;; yasnippet
(use-package yasnippet)
(use-package yasnippet-snippets
             :after yasnippet)

;; multi-term
(use-package multi-term)

;; elpy (python ide)
(use-package elpy
             :config
             (elpy-enable)
             (defalias 'workon 'pyvenv-workon))

;; docker
(use-package dockerfile-mode)

;; yml
(use-package yaml-mode)

;; crux
(use-package crux)

;; ;; emacs-jupyter (depends on zmq)
;; (require 'zmq)
;; (use-package jupyter)

;; json
(use-package json-mode)

;; php
(use-package php-mode)
(use-package php-eldoc)
(use-package flymake-php)

;; undo-tree
(use-package undo-tree
             :bind (
               :map undo-tree-map
                 ("C-x u" . undo-tree-undo)
                 ("C-c u" . undo-tree-visualize))
             :config (global-undo-tree-mode))

(use-package highlight-symbol
             :bind ("M-s h k" . highlight-symbol-remove-all))

(use-package docker-tramp)
(use-package helm-tramp)

(use-package projectile
  :bind (
         :map projectile-mode-map
              ("C-c p" . 'projectile-command-map)))

(use-package helm-projectile
  :after helm)

(use-package move-text)

(use-package defrepeater)
