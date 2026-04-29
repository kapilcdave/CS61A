(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cadar x) (car (cdr (car x))))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

;; Problem 14
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 14
  ; Helper function to keep track of the current index and the remaining list
  (define (helper index lst)
    ; Base case: if the list is empty, return an empty list
    (if (null? lst)
          '()
          ; Recursive case: create a list of (index current_element)
          ; and add it to the front of the result of recursively processing the rest of the list with index + 1
          (cons (list index (car lst))
                (helper (+ index 1) (cdr lst)))))
  ; Start the recursion with index 0
  (helper 0 s)
  ; END PROBLEM 14
  )


;; Problem 15

;; Return the value for a key in a dictionary list
(define (get dict key)
  ; BEGIN PROBLEM 15
    (cond
    ; If the dictionary is empty, the key wasn't found, return #f
    ((null? dict) #f)
    ; If the first element of the first pair (the key) matches our target key, return the second element (the value)
    ((eq? (car (car dict)) key) (cadr (car dict)))
    ; Otherwise, recursively search for the key in the rest of the dictionary
    (else (get (cdr dict) key)))
  ; END PROBLEM 15
  )

;; Return a dictionary list with a (key value) pair
(define (set dict key val)
  ; BEGIN PROBLEM 15
  (cond
    ; If we reach the end of the dictionary and haven't found the key, add a new (key val) pair at the end
    ((null? dict) (list (list key val)))
    ; If we find the key, replace its pair with a new (key val) pair, and keep the rest of the dictionary the same
    ((eq? (car (car dict)) key)
     (cons (list key val) (cdr dict)))
    ; Otherwise, keep the current pair and recursively search/update the rest of the dictionary
    (else
      (cons (car dict) (set (cdr dict) key val))))
  ; END PROBLEM 15
  )

;; Problem 16

;; implement solution-code
(define (solution-code problem solution)
  ; BEGIN PROBLEM 16
  (cond
    ; Base case: if the problem expression is empty, return empty list
    ((null? problem) '())
    ; If the current element of the problem is itself a list, recursively process it as a sub-problem
    ((list? (car problem))
     (cons (solution-code (car problem) solution)
           (solution-code (cdr problem) solution)))
    ; If the current element is exactly the five-underscore blank, replace it with the solution
    ((equal? (car problem) '_____)
     (cons solution (solution-code (cdr problem) solution)))
    ; Otherwise, it's just a normal element, keep it and process the rest of the list
    (else
      (cons (car problem) (solution-code (cdr problem) solution))))
  ; END PROBLEM 16
  )
