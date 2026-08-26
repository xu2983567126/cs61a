(define (accumulate merger start n term)
  (if (= n 0)
    start
    (merger (term n) (accumulate merger start (- n 1) term)))
  )

(define (accumulate-tail merger start n term)
  (if (= n 0)
    start
    (accumulate-tail merger (merger (term n) start) (- n 1) term))
  )
