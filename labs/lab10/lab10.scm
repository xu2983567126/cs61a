(define-macro (repeat n expr)
  `(repeated-call ,n (lambda () ,expr)))

; Call zero-argument procedure f n times and return the final result.
(define (repeated-call n f)
  (if (= n 1)
      (f)
      (begin (f) (repeated-call (- n 1) f))))

(define (concatenate s)
  (define (helper concatenated rest)
    (if (null? rest)
      concatenated
      (helper (append concatenated (car rest)) (cdr rest)))
  )
  (helper () s)
)
