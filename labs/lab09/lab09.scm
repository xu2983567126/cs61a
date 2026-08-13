(define (over-or-under num1 num2)
    (cond
        ((< num1 num2) -1)
        ((= num1 num2) 0)
        (else 1)))

(define (composed f g)
    (lambda (x) (f (g x))))

(define (repeat f n)
    (if (= n 0)
        (lambda (x) x)
        (composed f (repeat f (- n 1)))))

(define lst
    (cons   (cons 1 '())
            (cons   2
                    (cons   (cons   3
                                    (cons 4 '()))
                            (cons 5 '()))))
)

(define (without-duplicates lst) 
    (if (null? lst)
        lst
        (let ((h (car lst)))
            (cons   h
                (without-duplicates (filter (lambda (x) (not (= x h)))
                                            (cdr lst)
                                    )
                )
            )
        )
    )
)
