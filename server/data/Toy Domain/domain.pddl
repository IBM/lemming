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
       :precondition (and (start))
       :effect (and (has_A) (food_for_B_main) (food_for_B_alt)))

   (:action B_main
       :parameters  ()
       :precondition (and (has_A) (food_for_B_main))
       :effect (and (has_B) (buffer) (not (food_for_B_main))))

   (:action B_alt
       :parameters  ()
       :precondition (and (has_A) (food_for_B_alt))
       :effect (and (has_B) (buffer) (not (food_for_B_alt))))

   (:action BUFFER
       :parameters  ()
       :precondition (and (buffer))
       :effect (and (not (buffer)) (not (food_for_B_alt))  (not (food_for_B_main))))

   (:action C
       :parameters  ()
       :precondition (and (has_B) (not (buffer)))
       :effect (and  (has_C)))

   (:action D
       :parameters  ()
       :precondition (and (has_C))
       :effect (and  (has_D)))

   (:action E
       :parameters  ()
       :precondition (and (has_C))
       :effect (and  (has_E)))

   (:action G
       :parameters  ()
       :precondition (and )
       :effect (and  (has_G)))

   (:action GOAL
       :parameters  ()
       :precondition (and (has_D) (has_E))
       :effect (and (end)))
)
