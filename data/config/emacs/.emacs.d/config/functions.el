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

(defun async-make (&optional arg)
  (if arg
      (progn
        (message "make within virtualenv 'ietf'")
        (shell-execute
         "source env/bin/activate; make"
         "*make output*")
        )
    (progn
      (message "make")
      (async-shell-to-temp-buffer
       "make"
       "*make output*")
      )))
