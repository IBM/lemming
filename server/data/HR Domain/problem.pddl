(define (problem verdi-sequencer)
    (:domain verdi-catalog)
    (:objects
    )

    (:init
        (= (total-cost ) 0.0)
        (is_slotfillable original_error)
        (is_slotfillable HiringManager)
        (is_slotfillable slot_fill_form_title)
        (is_slotfillable response)
        (is_slotfillable data_objects)
        (is_slotfillable job_requisitions_filter_list)
        (is_slotfillable status_in_query_get_jrs)
        (is_slotfillable jobProfile_in_query_create_jr)
        (is_slotfillable Recruiter)
        (is_slotfillable status_in_query_create_jr)
        (is_slotfillable jobReqId_in_response_in_create_jr)
        (is_slotfillable list_of_signature_item_spec)
        (is_slotfillable channelName)
        (is_slotfillable location_in_query_create_jr)
        (is_slotfillable instances)
        (is_slotfillable job_requisitions)
        (is_slotfillable hiringManagerNote)
        (is_slotfillable sf_context)
    )

    (:goal
        (and (done) (has_done WO__postJobs))
    )

    (:metric minimize (total-cost ))
)