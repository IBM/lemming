(define (domain toy-lemming)
(:requirements :strips)
   (:predicates
        (start)
        (has_A)
        (has_done_a)
        (has_B)
        (has_done_b_main)
        (has_done_b_alt)
        (has_C)
        (has_done_c)
        (has_D)
        (has_done_d)
        (has_E)
        (has_done_e)
        (has_F)
        (has_done_f)
        (has_G)
        (has_done_g)
        (food_for_B_main)
        (food_for_B_alt)
        (buffer)
        (has_done_buffer)
        (has_F)
        (has_G)
        (food_for_B_main)
        (food_for_B_alt)
        (buffer)
        (end)
        (has_done_goal)
    )

   (:action A
       :parameters  ()
       :precondition (and (start) (not (has_A)) (not (has_done_a)) (not (end)))
       :effect (and (has_A) (has_done_a) (food_for_B_main) (food_for_B_alt)))

   (:action B_main
       :parameters  ()
       :precondition (and (has_A) (food_for_B_main) (not (has_B)) (not (has_done_b_main)) (not (end)))
       :effect (and (has_B) (has_done_b_main) (buffer) (not (food_for_B_main))))

   (:action B_alt
       :parameters  ()
       :precondition (and (has_A) (food_for_B_alt) (not (has_B)) (not (has_done_b_alt)) (not (end)))
       :effect (and (has_B) (has_done_b_alt) (buffer) (not (food_for_B_alt))))

   (:action BUFFER
       :parameters  ()
       :precondition (and (buffer) (not (has_done_buffer)) (not (end)))
       :effect (and (not (buffer)) (has_done_g) (not (food_for_B_alt))  (not (food_for_B_main))))

   (:action C
       :parameters  ()
       :precondition (and (has_B) (not (buffer)) (not (has_C)) (not (has_done_c)) (not (end)))
       :effect (and  (has_C) (has_done_c)))

   (:action D
       :parameters  ()
       :precondition (and (has_C) (not (has_D)) (not (has_done_d)) (not (end)))
       :effect (and  (has_D) (has_done_d)))

   (:action E
       :parameters  ()
       :precondition (and (has_C) (not (has_E)) (not (has_done_e)) (not (end)))
       :effect (and  (has_E) (has_done_e)))

   (:action F
       :parameters  ()
       :precondition (and (has_C) (not (has_E)) (not (has_done_f)) (not (end)))
       :effect (and  (has_E) (has_done_f) (buffer)))

   (:action G
       :parameters  ()
       :precondition (and  (not (has_G)) (not (has_done_g)) (not (end)))
       :effect (and  (has_G) (has_done_g)))

   (:action GOAL
       :parameters  ()
       :precondition (and (has_D) (has_E) (not (buffer)) (not (has_done_goal)) (not (end)))
       :effect (and (end)  (has_done_goal)))
)
