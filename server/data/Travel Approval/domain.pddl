(define (domain verdi-catalog)
    (:requirements :action-costs :typing)
    (:types
        generic - object
        agent - object
        mode - object
        type__of__origin - generic
        type__of__des - generic
        type__of__start_date - generic
        type__of__end_date - generic
        type__of__blanket_pre_approval - generic
        type__of__bis_trip - generic
        type__of__pre_approval_done - generic
        type__of__client_name - generic
        type__of__client_to_be_verified - generic
	    type__of__paper_to_be_verified - generic
        type__of__paper_title - generic
        type__of__flight_done - generic
        type__of__hotel_done - generic
        type__of__personal_trip  - generic
        type__of__original_error - generic
        type__of__list_of_signature_item_spec - generic
        type__of__slot_fill_form_title - generic
        type__of__data_objects - generic
        type__of__sf_context - generic
    )

    (:constants
        approval_blanket_pre_approval arranged_travel book_flight_bis book_flight_personal book_hotel_bis book_hotel_personal data-mapper error_handler fallback get_client_name get_paper_details get_trip_estimate get_trip_type_bis get_trip_type_personal pre_approval_client pre_approval_conference slot-filler slot_filler_for_planner slot_filler_form_agent - agent
        bis_trip - type__of__bis_trip
        blanket_pre_approval - type__of__blanket_pre_approval
        client_name - type__of__client_name
        client_to_be_verified - type__of__client_to_be_verified
	    paper_to_be_verified - type__of__paper_to_be_verified
        data_objects - type__of__data_objects
        des - type__of__des
        end_date - type__of__end_date
        flight_done - type__of__flight_done
        hotel_done - type__of__hotel_done
        list_of_signature_item_spec - type__of__list_of_signature_item_spec
        origin - type__of__origin
        original_error - type__of__original_error
        paper_title - type__of__paper_title
        personal_trip  - type__of__personal_trip 
        pre_approval_done - type__of__pre_approval_done
        sf_context - type__of__sf_context
        slot_fill_form_title - type__of__slot_fill_form_title
        start_date - type__of__start_date
    )

    (:predicates
        (goal-achieved)
	    (has_done ?x1 - agent)
        (failed ?x1 - agent)
        (known ?x1 - generic)
        (is_slotfillable ?x1 - generic)
        (is_mappable ?x1 - generic ?x2 - generic)
    )

    (:functions
        (total-cost ) - number
        (affinity ?x1 - generic ?x2 - generic) - number
    )

    (:action get_trip_estimate
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done get_trip_estimate)) (not (failed get_trip_estimate)) (known origin) (known des) (known start_date) (known end_date))
     :effect (and
        (has_done get_trip_estimate)
        (known blanket_pre_approval)
        (increase (total-cost ) 1))
    )


    (:action approval_blanket_pre_approval
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done approval_blanket_pre_approval)) (not (failed approval_blanket_pre_approval)) (known bis_trip) (known blanket_pre_approval))
     :effect (and
        (has_done approval_blanket_pre_approval)
        (known pre_approval_done)
        (increase (total-cost ) 1))
    )


    (:action pre_approval_client
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done pre_approval_client)) (not (failed pre_approval_client)) (known bis_trip) (known client_name) (known origin) (known des) (known start_date) (known end_date))
     :effect (and
        (has_done pre_approval_client)
        (known pre_approval_done)
        (increase (total-cost ) 1))
    )


    (:action get_client_name
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done get_client_name)) (not (failed get_client_name)) (known bis_trip) (known client_to_be_verified))
     :effect (and
        (has_done get_client_name)
        (known client_name)
        (increase (total-cost ) 1))
    )


    (:action pre_approval_conference
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done pre_approval_conference)) (not (failed pre_approval_conference)) (known bis_trip) (known paper_title) (known origin) (known des) (known start_date) (known end_date))
     :effect (and
        (has_done pre_approval_conference)
        (known pre_approval_done)
        (increase (total-cost ) 1))
    )


    (:action get_paper_details
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done get_paper_details)) (not (failed get_paper_details)) (known bis_trip) (known paper_to_be_verified))
     :effect (and
        (has_done get_paper_details)
        (known paper_title)
        (increase (total-cost ) 1))
    )


    (:action book_flight_bis
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done book_flight_bis)) (not (failed book_flight_bis)) (known pre_approval_done) (known bis_trip) (known origin) (known des) (known start_date) (known end_date))
     :effect (and
        (has_done book_flight_bis)
        (known flight_done)
        (increase (total-cost ) 1))
    )


    (:action book_hotel_bis
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done book_hotel_bis)) (not (failed book_hotel_bis)) (known pre_approval_done) (known bis_trip) (known origin) (known des) (known start_date) (known end_date))
     :effect (and
        (has_done book_hotel_bis)
        (known hotel_done)
        (increase (total-cost ) 1))
    )


    (:action book_flight_personal
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done book_flight_personal)) (not (failed book_flight_personal)) (known personal_trip ) (known origin) (known des) (known start_date) (known end_date))
     :effect (and
        (has_done book_flight_personal)
        (known flight_done)
        (increase (total-cost ) 1))
    )


    (:action book_hotel_personal
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done book_hotel_personal)) (not (failed book_hotel_personal)) (known personal_trip ) (known origin) (known des) (known start_date) (known end_date))
     :effect (and
        (has_done book_hotel_personal)
        (known hotel_done)
        (increase (total-cost ) 1))
    )


    (:action get_trip_type_personal
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done get_trip_type_personal)) (not (has_done get_trip_type_bis)) (not (failed get_trip_type_personal)))
     :effect (and
        (has_done get_trip_type_personal)
        (known personal_trip )
        (increase (total-cost ) 1))
    )


    (:action get_trip_type_bis
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done get_trip_type_bis)) (not (has_done get_trip_type_personal)) (not (failed get_trip_type_bis)))
     :effect (and
        (has_done get_trip_type_bis)
        (known bis_trip)
        (increase (total-cost ) 1))
    )


    (:action arranged_travel
     :parameters ()
     :precondition (and (not (has_done arranged_travel)) (not (failed arranged_travel)) (known flight_done) (known hotel_done))
     :effect (and
        (has_done arranged_travel) (goal-achieved)
        (increase (total-cost ) 1))
    )


    (:action error_handler
     :parameters ()
     :precondition (and (not (has_done error_handler)) (not (failed error_handler)) (known original_error))
     :effect (and
        (has_done error_handler)
        (increase (total-cost ) 1))
    )


    (:action slot_filler_for_planner
     :parameters ()
     :precondition (and (not (has_done slot_filler_for_planner)) (not (failed slot_filler_for_planner)) (known list_of_signature_item_spec))
     :effect (and
        (has_done slot_filler_for_planner)
        (known data_objects)
        (increase (total-cost ) 1))
    )


    (:action slot_filler_form_agent
     :parameters ()
     :precondition (and (not (has_done slot_filler_form_agent)) (not (failed slot_filler_form_agent)) (known sf_context))
     :effect (and
        (has_done slot_filler_form_agent)
        (increase (total-cost ) 1))
    )


    (:action fallback
     :parameters ()
     :precondition (and (not (has_done fallback)) (not (failed fallback)))
     :effect (and
        (has_done fallback)
        (increase (total-cost ) 1))
    )


    (:action data-mapper_type__of__pre_approval_done
     :parameters (?x - type__of__pre_approval_done ?y - type__of__pre_approval_done)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__list_of_signature_item_spec
     :parameters (?x - type__of__list_of_signature_item_spec ?y - type__of__list_of_signature_item_spec)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__sf_context
     :parameters (?x - type__of__sf_context ?y - type__of__sf_context)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__personal_trip 
     :parameters (?x - type__of__personal_trip  ?y - type__of__personal_trip )
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__client_to_be_verified
     :parameters (?x - type__of__client_to_be_verified ?y - type__of__client_to_be_verified)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )

    (:action data-mapper_type__of__paper_to_be_verified
     :parameters (?x - type__of__paper_to_be_verified ?y - type__of__paper_to_be_verified)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )



    (:action data-mapper_type__of__origin
     :parameters (?x - type__of__origin ?y - type__of__origin)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__bis_trip
     :parameters (?x - type__of__bis_trip ?y - type__of__bis_trip)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__paper_title
     :parameters (?x - type__of__paper_title ?y - type__of__paper_title)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__data_objects
     :parameters (?x - type__of__data_objects ?y - type__of__data_objects)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__hotel_done
     :parameters (?x - type__of__hotel_done ?y - type__of__hotel_done)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__original_error
     :parameters (?x - type__of__original_error ?y - type__of__original_error)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__flight_done
     :parameters (?x - type__of__flight_done ?y - type__of__flight_done)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__client_name
     :parameters (?x - type__of__client_name ?y - type__of__client_name)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__slot_fill_form_title
     :parameters (?x - type__of__slot_fill_form_title ?y - type__of__slot_fill_form_title)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__des
     :parameters (?x - type__of__des ?y - type__of__des)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__blanket_pre_approval
     :parameters (?x - type__of__blanket_pre_approval ?y - type__of__blanket_pre_approval)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__end_date
     :parameters (?x - type__of__end_date ?y - type__of__end_date)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action data-mapper_type__of__start_date
     :parameters (?x - type__of__start_date ?y - type__of__start_date)
     :precondition (and (known ?x) (not (known ?y)))
     :effect (and
        (known ?y)
        (increase (total-cost ) 3))
    )


    (:action slot-filler---start_date
     :parameters ()
     :precondition (not (known start_date))
     :effect (and
        (known start_date)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---personal_trip 
     :parameters ()
     :precondition (and (not (known personal_trip )) (has_done get_trip_type_personal))
     :effect (and
        (known personal_trip )
        (increase (total-cost ) 50))
    )


    (:action slot-filler---blanket_pre_approval
     :parameters ()
     :precondition (and (not (known blanket_pre_approval)) (has_done get_trip_estimate))
     :effect (and
        (known blanket_pre_approval)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---paper_title
     :parameters ()
     :precondition (and (not (known paper_title)) (has_done get_paper_details))
     :effect (and
        (known paper_title)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---pre_approval_done
     :parameters ()
     :precondition (and (not (known pre_approval_done)) (has_done approval_blanket_pre_approval) (has_done pre_approval_client) (has_done pre_approval_conference))
     :effect (and
        (known pre_approval_done)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---hotel_done
     :parameters ()
     :precondition (and (not (known hotel_done)) (has_done book_hotel_bis) (has_done book_hotel_personal))
     :effect (and
        (known hotel_done)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---client_name
     :parameters ()
     :precondition (and (not (known client_name)) (has_done get_client_name))
     :effect (and
        (known client_name)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---end_date
     :parameters ()
     :precondition (not (known end_date))
     :effect (and
        (known end_date)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---original_error
     :parameters ()
     :precondition (not (known original_error))
     :effect (and
        (known original_error)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---data_objects
     :parameters ()
     :precondition (and (not (known data_objects)) (has_done slot_filler_for_planner))
     :effect (and
        (known data_objects)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---bis_trip
     :parameters ()
     :precondition (and (not (known bis_trip)) (has_done get_trip_type_bis))
     :effect (and
        (known bis_trip)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---list_of_signature_item_spec
     :parameters ()
     :precondition (not (known list_of_signature_item_spec))
     :effect (and
        (known list_of_signature_item_spec)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---sf_context
     :parameters ()
     :precondition (not (known sf_context))
     :effect (and
        (known sf_context)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---origin
     :parameters ()
     :precondition (not (known origin))
     :effect (and
        (known origin)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---des
     :parameters ()
     :precondition (not (known des))
     :effect (and
        (known des)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---client_to_be_verified
     :parameters ()
     :precondition (not (known client_to_be_verified))
     :effect (and
        (known client_to_be_verified)
        (increase (total-cost ) 50))
    )

     (:action slot-filler---paper_to_be_verified
     :parameters ()
     :precondition (not (known paper_to_be_verified))
     :effect (and
        (known paper_to_be_verified)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---flight_done
     :parameters ()
     :precondition (and (not (known flight_done)) (has_done book_flight_bis) (has_done book_flight_personal))
     :effect (and
        (known flight_done)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---slot_fill_form_title
     :parameters ()
     :precondition (not (known slot_fill_form_title))
     :effect (and
        (known slot_fill_form_title)
        (increase (total-cost ) 50))
    )


   

)