(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cadar x) (car (cdr (car x))))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

;; Problem 14
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 14
  (define (helper index lst)
    (if (null? lst)
          '()
          (cons (list index (car lst))
                (helper (+ index 1) (cdr lst)))))
  (helper 0 s)

  ; END PROBLEM 14
  )


;; Problem 15

;; Return the value for a key in a dictionary list
(define (get dict key)
  ; BEGIN PROBLEM 15
    (cond
    ((null? dict) #f)
    ((eq? (car (car dict)) key) (cadr (car dict)))
    (else (get (cdr dict) key)))
  ; END PROBLEM 15
  )

;; Return a dictionary list with a (key value) pair
(define (set dict key val)
  ; BEGIN PROBLEM 15
  (cond
    ((null? dict) (list (list key val)))
    ((eq? (car (car dict)) key)
     (cons (list key val) (cdr dict)))
    (else
      (cons (car dict) (set (cdr dict) key val))))
  ; END PROBLEM 15
  )

;; Problem 16

;; implement solution-code
(define (solution-code problem solution)
  ; BEGIN PROBLEM 16
  (cond
    ((null? problem) '())
    ((list? (car problem))
     (cons (solution-code (car problem) solution)
           (solution-code (cdr problem) solution)))
    ((equal? (car problem) '_____)
     (cons solution (solution-code (cdr problem) solution)))
    (else
      (cons (car problem) (solution-code (cdr problem) solution))))
  ; END PROBLEM 16
  )
