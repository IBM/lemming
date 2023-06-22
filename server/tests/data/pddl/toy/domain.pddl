(define (domain toy-lemming)
(:requirements :strips)
   (:predicates
        (start)
        (has_A)
        (has_B)
        (has_C)
        (has_D)
        (has_E)
        (has_F)
        (has_G)
        (food_for_B_main)
        (food_for_B_alt)
        (buffer)
        (end)
    )

   (:action A
       :parameters  ()
       :precondition (and (start) (not (has_A)) (not (end)))
       :effect (and (has_A) (food_for_B_main) (food_for_B_alt)))

   (:action B_main
       :parameters  ()
       :precondition (and (has_A) (food_for_B_main) (not (has_B)) (not (end)))
       :effect (and (has_B) (buffer) (not (food_for_B_main))))

   (:action B_alt
       :parameters  ()
       :precondition (and (has_A) (food_for_B_alt) (not (has_B)) (not (end)))
       :effect (and (has_B) (buffer) (not (food_for_B_alt))))

   (:action BUFFER
       :parameters  ()
       :precondition (and (buffer) (not (end)))
       :effect (and (not (buffer)) (not (food_for_B_alt))  (not (food_for_B_main))))

   (:action C
       :parameters  ()
       :precondition (and (has_B) (not (buffer)) (not (has_C)) (not (end)))
       :effect (and  (has_C)))

   (:action D
       :parameters  ()
       :precondition (and (has_C) (not (has_D)) (not (end)))
       :effect (and  (has_D)))

   (:action E
       :parameters  ()
       :precondition (and (has_C) (not (has_E)) (not (end)))
       :effect (and  (has_E)))

   (:action F
       :parameters  ()
       :precondition (and (has_C) (not (has_E)) (not (end)))
       :effect (and  (has_E) (buffer)))

   (:action G
       :parameters  ()
       :precondition (and  (not (has_G)) (not (end)))
       :effect (and  (has_G)))

   (:action GOAL
       :parameters  ()
       :precondition (and (has_D) (has_E) (not (buffer)) (not (end)))
       :effect (and (end)))
)
