(write-region "" nil "/tmp/jarvis-chatgpt.txt")

(require 'filenotify)
(generate-new-buffer "CHATGPT")

(defun my-jarvis-callback (event)
  (with-current-buffer "CHATGPT"
    (erase-buffer)
    (insert-file-contents "/tmp/jarvis-chatgpt.txt" nil 0 5000)
    (goto-char (point-max))))

(file-notify-add-watch
  "/tmp/jarvis-chatgpt.txt" '(change) 'my-jarvis-callback)
      
(defun send-selection-to-jarvis ()
  (interactive)
  (write-region (buffer-substring (region-beginning) (region-end)) "/tmp/jarvis-chatgpt-input.txt" 0))
(global-set-key (kbd "<f12>") 'send-selection-to-jarvis)
