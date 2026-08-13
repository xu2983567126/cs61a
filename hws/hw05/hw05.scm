(define (square n) (* n n))

(define (pow base exp)
  (cond ((= exp 0) 1)                              ; 基准
        ((= (modulo exp 2) 0)                     ; 偶数
         (let ((half (pow base (/ exp 2))))
           (* half half)))
        (else                                     ; 奇数
          (let ((half (pow base (/ (- exp 1) 2))))
            (* base half half)))))         ; 也可优化为 (square (pow base (/ (- exp 1) 2))) * base

(define (repeatedly-cube n x)
  (if (zero? n)
      x
      (begin 
        (define y (repeatedly-cube (- n 1) x))
        (* y y y))))

(define (cddr s) (cdr (cdr s)))

(define (cadr s) (car (cdr s)))

(define (caddr s) (car (cddr s)))
