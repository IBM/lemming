(define (domain toy-lemming)
(:requirements :strips)
   (:predicates
        (start)
        (has_A)
        (has_done_A)
        (has_B)
        (has_done_B_main)
        (has_done_B_alt)
        (has_C)
        (has_done_C)
        (has_D)
        (has_done_D)
        (has_E)
        (has_done_E)
        (has_F)
        (has_done_F)
        (has_G)
        (has_done_G)
        (food_for_B_main)
        (food_for_B_alt)
        (buffer)
        (has_done_BUFFER)
        (end)
        (has_done_GOAL)
    )

   (:action A
       :parameters  ()
       :precondition (and (start) (not (has_A)) (not (has_done_A)) (not (end)))
       :effect (and (has_A) (has_done_A) (food_for_B_main) (food_for_B_alt)))

   (:action B_main
       :parameters  ()
       :precondition (and (has_A) (food_for_B_main) (not (has_B)) (not (has_done_B_main)) (not (end)))
       :effect (and (has_B) (has_done_B_main) (buffer) (not (food_for_B_main))))

   (:action B_alt
       :parameters  ()
       :precondition (and (has_A) (food_for_B_alt) (not (has_B)) (not (has_done_B_alt)) (not (end)))
       :effect (and (has_B) (has_done_B_alt) (buffer) (not (food_for_B_alt))))

   (:action BUFFER
       :parameters  ()
       :precondition (and (buffer) (not (has_done_BUFFER)) (not (end)))
       :effect (and (not (buffer)) (has_done_G) (not (food_for_B_alt))  (not (food_for_B_main))))

   (:action C
       :parameters  ()
       :precondition (and (has_B) (not (buffer)) (not (has_C)) (not (has_done_C)) (not (end)))
       :effect (and  (has_C) (has_done_C)))

   (:action D
       :parameters  ()
       :precondition (and (has_C) (not (has_D)) (not (has_done_D)) (not (end)))
       :effect (and  (has_D) (has_done_D)))

   (:action E
       :parameters  ()
       :precondition (and (has_C) (not (has_E)) (not (has_done_E)) (not (end)))
       :effect (and  (has_E) (has_done_E)))

   (:action F
       :parameters  ()
       :precondition (and (has_C) (not (has_E)) (not (has_done_F)) (not (end)))
       :effect (and  (has_E) (has_done_F) (buffer)))

   (:action G
       :parameters  ()
       :precondition (and  (not (has_G)) (not (has_done_G)) (not (end)))
       :effect (and  (has_G) (has_done_G)))

   (:action GOAL
       :parameters  ()
       :precondition (and (has_D) (has_E) (not (buffer)) (not (has_done_GOAL)) (not (end)))
       :effect (and (end)  (has_done_GOAL)))
)
