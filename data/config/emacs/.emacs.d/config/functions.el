(defun whack-whitespace (arg)
      "Delete all white space from point to the next word.  With prefix ARG
    delete across newlines as well.  The only danger in this is that you
    don't have to actually be at the end of a word to make it work.  It
    skips over to the next whitespace and then whacks it all to the next
    word."
      (interactive "P")
      (let ((regexp (if arg "[ \t]+" "[ \t\n]+")))
        (re-search-forward regexp nil t)
        (replace-match "" nil nil)))

(defun copy-buffer-file-name-into-clipboard (arg)
  "Copy current buffer's path into clipboard using x-set-selection"
  (interactive "P")
  (x-set-selection nil (file-truename buffer-file-name)))

(defun shell-execute (cmd buf)
  (interactive (let ((default-buffer "*make output*"))
                 (list
                  (read-string "Command: " "make")
                  (read-string (format "Output Buffer (%s): " default-buffer) nil nil default-buffer))))
  (with-output-to-temp-buffer buf
    (start-process-shell-command cmd
                                 (get-buffer-create buf)
                                 cmd)
    (pop-to-buffer buf)
    (special-mode)))

(defun async-make-with-args (cmd oBuffer vEnv)
  (let ((c cmd))
    (if vEnv
        (progn
          (message "execute within virtualenv './env'")
          (setq c (concatenate 'string "source env/bin/activate; " c))))
    (if oBuffer
        (progn
          (with-current-buffer (other-buffer (current-buffer) t)
            (shell-execute
             c
             (concatenate 'string "*" cmd " output*")
             )))
      (progn
        (shell-execute
         c
         (concatenate 'string "*" cmd " output*"))
        ))))

(defun global-s()
  (interactive)
  (if (eq (get major-mode 'mode-class) 'special)
      (call-interactively 'other-window)
    (call-interactively 'self-insert-command)))

(defun run-gnome-terminal-here ()
  (interactive "@")
  (shell-command
   (concat "gnome-terminal --working-directory="
           (file-truename default-directory)
           " > /dev/null 2>&1 & disown")
   nil nil))

(defun open-link-or-image-or-url ()
  "Opens the current link or image or current page's uri or any url-like text under cursor in firefox."
  (interactive)
    (browse-url-generic (car (browse-url-interactive-arg "URL: "))))

(defun update-yasnippets ()
  "Compile and load all yasnippets in yas-snippet-dirs."
  (interactive)
  (progn
    (yas-recompile-all)
    (yas-reload-all)))

(defun tramp-remove-gofmt-error-message ()
  (interactive)
  (setq gofmt-show-errors nil))

(defun tramp-remove-gofmt-before-save-hook ()
  (interactive)
  (remove-hook 'before-save-hook 'gofmt-before-save))


(defun toggle-window-split ()
  (interactive)
  (if (= (count-windows) 2)
      (let* ((this-win-buffer (window-buffer))
             (next-win-buffer (window-buffer (next-window)))
             (this-win-edges (window-edges (selected-window)))
             (next-win-edges (window-edges (next-window)))
             (this-win-2nd (not (and (<= (car this-win-edges)
                                         (car next-win-edges))
                                     (<= (cadr this-win-edges)
                                         (cadr next-win-edges)))))
             (splitter
              (if (= (car this-win-edges)
                     (car (window-edges (next-window))))
                  'split-window-horizontally
                'split-window-vertically)))
        (delete-other-windows)
        (let ((first-win (selected-window)))
          (funcall splitter)
          (if this-win-2nd (other-window 1))
          (set-window-buffer (selected-window) this-win-buffer)
          (set-window-buffer (next-window) next-win-buffer)
          (select-window first-win)
          (if this-win-2nd (other-window 1))))))


(defun rotate-windows (count)
  "Rotate your windows.
Dedicated windows are left untouched. Giving a negative prefix
argument makes the windows rotate backwards."
  (interactive "p")
  (let* ((non-dedicated-windows (remove-if 'window-dedicated-p (window-list)))
         (num-windows (length non-dedicated-windows))
         (i 0)
         (step (+ num-windows count)))
    (cond ((not (> num-windows 1))
           (message "You can't rotate a single window!"))
          (t
           (dotimes (counter (- num-windows 1))
             (let* ((next-i (% (+ step i) num-windows))

                    (w1 (elt non-dedicated-windows i))
                    (w2 (elt non-dedicated-windows next-i))

                    (b1 (window-buffer w1))
                    (b2 (window-buffer w2))

                    (s1 (window-start w1))
                    (s2 (window-start w2)))
               (set-window-buffer w1 b2)
               (set-window-buffer w2 b1)
               (set-window-start w1 s2)
               (set-window-start w2 s1)
               (setq i next-i)))))))
