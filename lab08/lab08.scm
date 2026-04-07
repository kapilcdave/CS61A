(define (over-or-under num1 num2)
  (if (< num1 num2)
      -1
      (if (= num1 num2)
          0
          1)))

(define (over-or-under-cond num1 num2)
  (cond ((< num1 num2) -1)
        ((= num1 num2) 0)
        (else 1)))

(define (composed f g)
  (lambda (x)
    (f (g x))))

(define (repeat f n)
  (if (= n 1)
      (lambda (x) (f x))
      (composed f (repeat f (- n 1)))))

(define (max a b)
  (if (> a b)
      a
      b))

(define (min a b)
  (if (> a b)
      b
      a))

(define (gcd a b)
  (if (zero? (min a b))
      (max a b)
      (if (zero? (modulo (max a b) (min a b)))
          (min a b)
          (gcd (min a b)
               (modulo (max a b) (min a b))))))

(define (exp b n)
  (define (helper n so-far)
    (if (= n 0)
        so-far
        (helper (- n 1) (* so-far b))))
  (helper n 1))

(define (swap s)
  (define (swap-helper s result)
    (cond ((null? s) result)                   
          ((null? (cdr s)) (append result s))  
          (else 
            (swap-helper (cdr (cdr s)) 
                         (append result (list (car (cdr s)) (car s)))))))
  (swap-helper s nil))


(define (make-adder num)
  (lambda (x)
    (+ x num)))