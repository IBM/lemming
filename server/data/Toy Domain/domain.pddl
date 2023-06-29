(define (domain toy-lemming)
(:requirements :strips)
   (:predicates
        (start)
        (has_A)
        (hasDoneA)
        (has_B)
        (hasDoneBmain)
        (hasDoneBalt)
        (has_C)
        (hasDoneC)
        (has_D)
        (hasDoneD)
        (has_E)
        (hasDoneE)
        (has_F)
        (hasDoneF)
        (has_G)
        (hasDoneG)
        (food_for_B_main)
        (food_for_B_alt)
        (buffer)
        (hasDoneBuffer)
        (has_F)
        (has_G)
        (food_for_B_main)
        (food_for_B_alt)
        (buffer)
        (end)
        (hasDoneGoal)
    )

   (:action A
       :parameters  ()
       :precondition (and (start) (not (has_A)) (not (hasDoneA)) (not (end)))
       :effect (and (has_A) (hasDoneA) (food_for_B_main) (food_for_B_alt)))

   (:action B_main
       :parameters  ()
       :precondition (and (has_A) (food_for_B_main) (not (has_B)) (not (hasDoneBmain)) (not (end)))
       :effect (and (has_B) (hasDoneBmain) (buffer) (not (food_for_B_main))))

   (:action B_alt
       :parameters  ()
       :precondition (and (has_A) (food_for_B_alt) (not (has_B)) (not (hasDoneBalt)) (not (end)))
       :effect (and (has_B) (hasDoneBalt) (buffer) (not (food_for_B_alt))))

   (:action BUFFER
       :parameters  ()
       :precondition (and (buffer) (not (hasDoneBuffer)) (not (end)))
       :effect (and (not (buffer)) (hasDoneG) (not (food_for_B_alt))  (not (food_for_B_main))))

   (:action C
       :parameters  ()
       :precondition (and (has_B) (not (buffer)) (not (has_C)) (not (hasDoneC)) (not (end)))
       :effect (and  (has_C) (hasDoneC)))

   (:action D
       :parameters  ()
       :precondition (and (has_C) (not (has_D)) (not (hasDoneD)) (not (end)))
       :effect (and  (has_D) (hasDoneD)))

   (:action E
       :parameters  ()
       :precondition (and (has_C) (not (has_E)) (not (hasDoneE)) (not (end)))
       :effect (and  (has_E) (hasDoneE)))

   (:action F
       :parameters  ()
       :precondition (and (has_C) (not (has_E)) (not (hasDoneF)) (not (end)))
       :effect (and  (has_E) (hasDoneF) (buffer)))

   (:action G
       :parameters  ()
       :precondition (and  (not (has_G)) (not (hasDoneG)) (not (end)))
       :effect (and  (has_G) (hasDoneG)))

   (:action GOAL
       :parameters  ()
       :precondition (and (has_D) (has_E) (not (buffer)) (not (hasDoneGoal)) (not (end)))
       :effect (and (end)  (hasDoneGoal)))
)
