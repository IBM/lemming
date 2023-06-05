(define (problem verdi-sequencer)
    (:domain verdi-catalog)

    (:objects
        
    )

    (:init
        (= (total-cost ) 0.0)
        (is_slotfillable data_objects)
        (is_slotfillable bis_trip)
        (is_slotfillable original_error)
        (is_slotfillable client_to_be_verified)
        (is_slotfillable origin)
        (is_slotfillable hotel_done)
        (is_slotfillable flight_done)
        (is_slotfillable personal_trip )
        (is_slotfillable paper_title)
        (is_slotfillable pre_approval_done)
        (is_slotfillable client_name)
        (is_slotfillable list_of_signature_item_spec)
        (is_slotfillable start_date)
        (is_slotfillable sf_context)
        (is_slotfillable blanket_pre_approval)
        (is_slotfillable des)
        (is_slotfillable slot_fill_form_title)
        (is_slotfillable end_date)
    )

    (:goal
        (has_done arranged_travel)
    )

    
    
    (:metric minimize (total-cost ))
)
