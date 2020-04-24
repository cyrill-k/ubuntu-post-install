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
