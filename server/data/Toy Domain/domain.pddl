(define (domain toy-lemming)
(:requirements :strips)
   (:predicates
        (start)
        (has_A)
        (has_B)
        (has_C)
        (has_D)
        (has_E)
        (end)
    )

   (:action START
       :parameters  ()
       :precondition (and)
       :effect (and  (start)))

   (:action get_A
       :parameters  ()
       :precondition (and (start))
       :effect (and (has_A)))

   (:action get_B
       :parameters  ()
       :precondition (and (has_A))
       :effect (and (has_B)))

   (:action get_C
       :parameters  ()
       :precondition (and (has_A))
       :effect (and (has_C)))

   (:action get_D_from_B
       :parameters  ()
       :precondition (and (has_B))
       :effect (and (has_D)))

   (:action get_D_from_C
       :parameters  ()
       :precondition (and (has_C))
       :effect (and (has_D)))

   (:action END
       :parameters  ()
       :precondition (and (has_D))
       :effect (and  (end)))
)
