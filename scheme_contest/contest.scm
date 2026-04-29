;;; Scheme Recursive Art Contest Entry
;;;
;;; Please do not include your name or personal info in this file.
;;;
;;; Title: The Golden Spin
;;;
;;; Description:
;;;   A sphere takes flight now,
;;;   Golden rectangle in spin,
;;;   Infinite power.

(define phi 1.618033988749895)

(define (fib-spiral-out size n colors)
  (if (> n 0)
      (begin
        (color "darkgoldenrod")
        (pensize 2)
        (pendown)
        (forward size) (left 90)
        (forward size) (left 90)
        (forward size) (left 90)
        (forward size) (left 90)
        
        (color (car colors))
        (pensize 4)
        (circle size 90)
        
        (fib-spiral-out (* size phi) (- n 1) 
                        (append (cdr colors) (list (car colors)))))))

(define (draw-horse)
  (color "saddlebrown")
  (pensize 2)
  (penup) (goto -160 -120) (setheading 0) (pendown)
  (begin_fill)
  (forward 140) (left 90) (forward 60) (left 90) 
  (forward 140) (left 90) (forward 60) (left 90)
  (end_fill)
  
  (penup) (goto -20 -60) (setheading 45) (pendown)
  (begin_fill)
  (forward 60) (left 90) (forward 30) (left 90) 
  (forward 60) (left 90) (forward 30) (left 90)
  (end_fill)
  
  (pensize 8)
  (penup) (goto -140 -120) (setheading 250) (pendown) (forward 70)
  (penup) (goto -120 -120) (setheading 270) (pendown) (forward 70)
  (penup) (goto -60 -120) (setheading 260) (pendown) (forward 70)
  (penup) (goto -40 -120) (setheading 280) (pendown) (forward 70)
  
  (penup) (goto -160 -80) (setheading 190) (pendown)
  (pensize 5)
  (forward 50))

(define (draw-rider)
  (color "purple")
  (pensize 6)
  (penup) (goto -100 -60) (pendown)
  (goto -90 10) 
  
  (penup) (goto -90 25) (setheading 0) (pendown)
  (color "peachpuff")
  (begin_fill) (circle 15) (end_fill)
  
  (penup) (goto -115 40) (setheading 0) (pendown)
  (color "forestgreen")
  (begin_fill)
  (forward 50) (left 90) (forward 15) (left 90) 
  (forward 50) (left 90) (forward 15) (left 90)
  (end_fill)
  
  (penup) (goto -100 -20) (pendown)
  (color "magenta")
  (begin_fill)
  (goto -160 -30) (goto -150 -70) (goto -100 -60)
  (end_fill)
  
  (penup) (goto -95 0) (pendown)
  (color "purple")
  (pensize 5)
  (goto 0 0)
  
  (penup) (goto -90 5) (pendown)
  (color "white")
  (pensize 1)
  (goto -5 -40))

(define (draw-sphere)
  (penup) (goto 0 -12) (setheading 0) (pendown)
  (color "white")
  (begin_fill)
  (circle 12)
  (end_fill)
  
  (color "mediumseagreen")
  (begin_fill)
  (penup) (goto 0 -8) (pendown)
  (circle 8)
  (end_fill)
  
  (color "white")
  (pensize 2)
  (penup) (goto 0 -4) (pendown)
  (circle 4))

(define (draw)
  (bgcolor "black")
  (speed 0)
  
  (draw-horse)
  (draw-rider)
  
  (penup) (goto 0 0) (setheading 45) (pendown)
  (fib-spiral-out 2 13 '("cyan" "aqua" "springgreen" "yellow" "orange" "red"))
  
  (draw-sphere)
  
  (hideturtle)
  (exitonclick))

; Please leave this last line alone. You may add additional procedures above
; this line.
(draw)