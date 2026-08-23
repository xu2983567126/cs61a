(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cadar x) (car (cdr (car x))))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

;; 问题 14
;; 返回一个由二元组构成的列表
(define (enumerate s)
  ; BEGIN PROBLEM 14
  (define (helper i s)
    (if (null? s)
      '()
      (cons (cons i
                  (cons (car s) '())) 
            (helper (+ i 1) (cdr s))))
    )
  (helper 0 s)
  ; END PROBLEM 14
  )


;; 问题 15

;; 在字典列表中查找某个键对应的值
(define (get dict key)
  ; BEGIN PROBLEM 15
  (cond 
    ((null? dict) #f)
    ((eq? (caar dict) key) (cadar dict))
    (else (get (cdr dict) key))
    )
  ; END PROBLEM 15
  )

;; 返回一个带有 (键 值) 对的字典列表
(define (set dict key val)
  ; BEGIN PROBLEM 15
  (cond 
    ((null? dict) (list (list key val)))
    ((eq? (caar dict) key) (cons (list key val) (cdr dict)))
    (else (cons (car dict) (set (cdr dict) key val)))
    )
  ; END PROBLEM 15
  )

;; 问题 16

;; 实现 solution-code
(define (solution-code problem solution)
  ; BEGIN PROBLEM 16
  (cond
    ((eq? problem '_____) solution)
    ((pair? problem)
      (cons
        (solution-code (car problem) solution)
        (solution-code (cdr problem) solution)))
    (else problem)
    )
  ; END PROBLEM 16
  )
