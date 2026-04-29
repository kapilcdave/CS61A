;;; Scheme Recursive Art Contest Entry
;;;
;;; Please do not include your name or personal info in this file.
;;;
;;; Title: The Golden Spin
;;;
;;; Description:
;;;   A geometric spin,
;;;   Squares and centers perfectly aligned,
;;;   Infinite power.

(define phi (/ (+ 1 (sqrt 5)) 2))

(define (fib-spiral-out size n colors)
  (if (> n 0)
      (begin
        ; Draw the square
        (color "darkgoldenrod")
        (pendown)
        (forward size) (left 90)
        (forward size) (left 90)
        (forward size) (left 90)
        (forward size) (left 90)
        
        (let ((start-x (xcor))
              (start-y (ycor))
              (start-h (heading)))
          (penup)
          (forward (/ size 2))
          (left 90)
          (forward (/ size 2))
          (let ((cx1 (xcor))
                (cy1 (ycor)))
            (goto start-x start-y)
            (setheading start-h)
            (penup)
            (forward size)
            (left 90)
            (forward size)
            (let ((next-start-x (xcor))
                  (next-start-y (ycor))
                  (next-h (heading))
                  (next-size (* size phi)))
              (forward (/ next-size 2))
              (left 90)
              (forward (/ next-size 2))
              (let ((cx2 (xcor))
                    (cy2 (ycor)))
                (penup)
                (goto cx1 cy1)
                (color (car colors))
                (pendown)
                (goto cx2 cy2)
                (penup)
                (goto next-start-x next-start-y)
                (setheading next-h)
                (fib-spiral-out next-size (- n 1) 
                                (append (cdr colors) (list (car colors)))))))))))

(define (draw)
  (bgcolor "black")
  (speed 0)
  
  (penup) (goto 0 0) (setheading 45) (pendown)
  (fib-spiral-out 2 13 '("cyan" "aqua" "springgreen" "yellow" "orange" "red" "magenta" "blueviolet"))
  
  (hideturtle)
  (exitonclick))

; Please leave this last line alone. You may add additional procedures above
; this line.
(draw)