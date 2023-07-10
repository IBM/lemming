(define (domain verdi-catalog)
    (:requirements :action-costs :typing)
    (:types
        generic - object
        agent - object
        mode - object
        get_jrs_job_requisitions_list - generic
        get_jrs_job_requisitions - generic
        type__of__jobReqId - generic
        type__of__jobStartDate - generic
        type__of__department - generic
        type__of__division - generic
        type__of__location - generic
        type__of__costOfHire - generic
        type__of__country - generic
        type__of__createdDateTime - generic
        type__of__currency - generic
        type__of__salRateType - generic
        type__of__salaryBase - generic
        type__of__candidateProgress - generic
        type__of__city - generic
        type__of__state - generic
        type__of__closedDateTime - generic
        type__of__jobDescription - generic
        type__of__jobProfile - generic
        type__of__workExperience - generic
        type__of__recruiter - generic
        type__of__competency_type - generic
        type__of__competency_description - generic
        type__of__competency_id - generic
        type__of__status - generic
        get_jrs_job_requisitions_filter_list - generic
        type__of__status_in_query_get_jrs - generic
        type__of__instances - generic
        type__of__hiringManagerNote - generic
        type__of__location_in_query_create_jr - generic
        type__of__jobProfile_in_query_create_jr - generic
        type__of__status_in_query_create_jr - generic
        type__of__jobReqId_in_response_in_create_jr - generic
        type__of__channelName - generic
        type__of__response - generic
        type__of__HiringManager - generic
        type__of__original_error - generic
        type__of__list_of_signature_item_spec - generic
        type__of__slot_fill_form_title - generic
        type__of__data_objects - generic
        type__of__sf_context - generic
    )

    (:constants
        WO__postJobsLinkedIn WO__postJobsIndeed WO__showApprovedJRs WO__Update_JR_Details WO__approve_jrs_approve_jrs_post WO__createNewJobRequisitionExisting WO__getJobRequisitions WO__getJobRequisitions_selector WO__getJobRequisitions_selector_multi WO__postJobs data-mapper error_handler fallback slot-filler slot_filler_for_planner slot_filler_form_agent - agent
        job_requisitions - get_jrs_job_requisitions
        job_requisitions_filter_list - get_jrs_job_requisitions_filter_list
        job_requisitions_list - get_jrs_job_requisitions_list
        HiringManager - type__of__HiringManager
        candidateProgress - type__of__candidateProgress
        channelName - type__of__channelName
        city - type__of__city
        closedDateTime - type__of__closedDateTime
        competency_description - type__of__competency_description
        competency_id - type__of__competency_id
        competency_type - type__of__competency_type
        costOfHire - type__of__costOfHire
        country - type__of__country
        createdDateTime - type__of__createdDateTime
        currency - type__of__currency
        data_objects - type__of__data_objects
        department - type__of__department
        division - type__of__division
        hiringManagerNote - type__of__hiringManagerNote
        instances - type__of__instances
        jobDescription - type__of__jobDescription
        jobProfile - type__of__jobProfile
        jobProfile_in_query_create_jr - type__of__jobProfile_in_query_create_jr
        jobReqId - type__of__jobReqId
        jobReqId_in_response_in_create_jr - type__of__jobReqId_in_response_in_create_jr
        jobStartDate - type__of__jobStartDate
        list_of_signature_item_spec - type__of__list_of_signature_item_spec
        location - type__of__location
        location_in_query_create_jr - type__of__location_in_query_create_jr
        original_error - type__of__original_error
        recruiter - type__of__recruiter
        response - type__of__response
        salRateType - type__of__salRateType
        salaryBase - type__of__salaryBase
        sf_context - type__of__sf_context
        slot_fill_form_title - type__of__slot_fill_form_title
        state - type__of__state
        status - type__of__status
        status_in_query_create_jr - type__of__status_in_query_create_jr
        status_in_query_get_jrs - type__of__status_in_query_get_jrs
        workExperience - type__of__workExperience
    )

    (:predicates
        (has_done ?x1 - agent)
	(goal-achieved)
	(done)
        (failed ?x1 - agent)
        (known ?x1 - generic)
        (is_slotfillable ?x1 - generic)
        (is_mappable ?x1 - generic ?x2 - generic)
    )

    (:functions
        (total-cost ) - number
        (affinity ?x1 - generic ?x2 - generic) - number
    )


    (:action WO__showApprovedJRs
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done WO__getJobRequisitions)) (not (has_done WO__showApprovedJRs)) (not (failed WO__showApprovedJRs)) (known status_in_query_get_jrs))
     :effect (and
        (has_done WO__showApprovedJRs)
        (known instances)
        (known job_requisitions_list)
	(done)
        (increase (total-cost ) 1))
    )



    (:action WO__getJobRequisitions_selector
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done WO__getJobRequisitions_selector)) (not (failed WO__getJobRequisitions_selector)) (known job_requisitions_list))
     :effect (and
        (has_done WO__getJobRequisitions_selector)
        (known job_requisitions)
        (known jobReqId)
        (known jobStartDate)
        (known department)
        (known division)
        (known location)
        (known costOfHire)
        (known country)
        (known createdDateTime)
        (known currency)
        (known salRateType)
        (known salaryBase)
        (known candidateProgress)
        (known city)
        (known state)
        (known closedDateTime)
        (known jobDescription)
        (known hiringManager)
        (known jobProfile)
        (known workExperience)
        (known recruiter)
        (known competency_type)
        (known competency_description)
        (known competency_id)
        (known status)
        (increase (total-cost ) 1))
    )


    (:action WO__getJobRequisitions_selector_multi
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done WO__getJobRequisitions_selector_multi)) (not (failed WO__getJobRequisitions_selector_multi)) (known job_requisitions_list))
     :effect (and
        (has_done WO__getJobRequisitions_selector_multi)
        (known job_requisitions_filter_list)
        (increase (total-cost ) 1))
    )


    (:action WO__getJobRequisitions
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done WO__getJobRequisitions)) (not (failed WO__getJobRequisitions)) (known status_in_query_get_jrs))
     :effect (and
        (has_done WO__getJobRequisitions)
        (known instances)
        (known job_requisitions_list)
	(done)
        (increase (total-cost ) 1))
    )


    (:action WO__approve_jrs_approve_jrs_post
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done WO__approve_jrs_approve_jrs_post)) (not (failed WO__approve_jrs_approve_jrs_post))  (known jobReqId) (known hiringManagerNote) (known jobProfile) (known hiringManager))
     :effect (and
        (has_done WO__approve_jrs_approve_jrs_post)
        (known jobReqId)
        (known jobProfile)
        (known jobStartDate)
        (known department)
        (known country)
        (known status)
        (known candidateProgress)
	(done)
        (increase (total-cost ) 1))
    )


    (:action WO__createNewJobRequisitionExisting
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done WO__createNewJobRequisitionExisting)) (not (failed WO__createNewJobRequisitionExisting)) (known status_in_query_create_jr) (known jobReqId) (known jobStartDate) (known department) (known division) (known location) (known costOfHire) (known country) (known createdDateTime) (known currency) (known salRateType) (known salaryBase) (known candidateProgress) (known city) (known state) (known closedDateTime) (known jobDescription) (known hiringManager) (known jobProfile) (known workExperience) (known recruiter) (known competency_type) (known competency_description) (known competency_id) (known status))
     :effect (and
        (has_done WO__createNewJobRequisitionExisting)
        (known jobReqId_in_response_in_create_jr)
        (known jobReqId)
        (known jobStartDate)
        (known department)
        (known division)
        (known location)
        (known costOfHire)
        (known country)
        (known createdDateTime)
        (known currency)
        (known salRateType)
        (known salaryBase)
        (known candidateProgress)
        (known city)
        (known state)
        (known closedDateTime)
        (known jobDescription)
        (known hiringManager)
        (known jobProfile)
        (known workExperience)
        (known recruiter)
        (known competency_type)
        (known competency_description)
        (known competency_id)
        (known status)
	(done)
        (increase (total-cost ) 1))
    )


    (:action WO__postJobsIndeed
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done WO__postJobsIndeed)) (not (failed WO__postJobsIndeed)) (known jobReqId) (known jobProfile) (known channelName))
     :effect (and
        (has_done WO__postJobs)
	(has_done WO__postJobsIndeed)
        (known response)
	(done) (goal-achieved)
        (increase (total-cost ) 1))
    )


   (:action WO__postJobsLinkedIn
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done WO__postJobsLinkedIn)) (not (failed WO__postJobsLinkedIn)) (known jobReqId) (known jobProfile) (known channelName))
     :effect (and
        (has_done WO__postJobsLinkedIn)
	(has_done WO__postJobs)
        (known response)
	(done) (goal-achieved)
        (increase (total-cost ) 1))
    )



    (:action WO__Update_JR_Details
     :parameters ()
     :precondition (and (not (goal-achieved)) (not (has_done WO__Update_JR_Details)) (not (failed WO__Update_JR_Details)) (known jobReqId) (known jobStartDate) (known department) (known division) (known location) (known costOfHire) (known country) (known createdDateTime) (known currency) (known salRateType) (known salaryBase) (known candidateProgress) (known city) (known state) (known closedDateTime) (known jobDescription) (known hiringManager) (known jobProfile) (known workExperience) (known recruiter) (known competency_type) (known competency_description) (known competency_id) (known status))
     :effect (and
        (has_done WO__Update_JR_Details)
	(has_done WO__createNewJobRequisitionExisting)
        (known jobReqId)
        (known jobStartDate)
        (known department)
        (known division)
        (known location)
        (known costOfHire)
        (known country)
        (known createdDateTime)
        (known currency)
        (known salRateType)
        (known salaryBase)
        (known candidateProgress)
        (known city)
        (known state)
        (known closedDateTime)
        (known jobDescription)
        (known hiringManager)
        (known jobProfile)
        (known workExperience)
        (known recruiter)
        (known competency_type)
        (known competency_description)
        (known competency_id)
        (known status)
	(done)
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



    (:action slot-filler---slot_fill_form_title
     :parameters ()
     :precondition (not (known slot_fill_form_title))
     :effect (and
        (known slot_fill_form_title)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---hiringManagerNote
     :parameters ()
     :precondition (not (known hiringManagerNote))
     :effect (and
        (known hiringManagerNote)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---data_objects
     :parameters ()
     :precondition (and (not (known data_objects)) (has_done slot_filler_for_planner))
     :effect (and
        (known data_objects)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---response
     :parameters ()
     :precondition (and (not (known response)) (has_done WO__postJobs))
     :effect (and
        (known response)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---job_requisitions
     :parameters ()
     :precondition (and (not (known job_requisitions)) (has_done WO__getJobRequisitions_selector))
     :effect (and
        (known job_requisitions)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---channelName
     :parameters ()
     :precondition (not (known channelName))
     :effect (and
        (known channelName)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---jobProfile_in_query_create_jr
     :parameters ()
     :precondition (not (known jobProfile_in_query_create_jr))
     :effect (and
        (known jobProfile_in_query_create_jr)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---Recruiter
     :parameters ()
     :precondition (not (known Recruiter))
     :effect (and
        (known Recruiter)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---original_error
     :parameters ()
     :precondition (not (known original_error))
     :effect (and
        (known original_error)
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


    (:action slot-filler---instances
     :parameters ()
     :precondition (and (not (known instances)) (has_done WO__getJobRequisitions))
     :effect (and
        (known instances)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---status_in_query_create_jr
     :parameters ()
     :precondition (not (known status_in_query_create_jr))
     :effect (and
        (known status_in_query_create_jr)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---jobReqId_in_response_in_create_jr
     :parameters ()
     :precondition (and (not (known jobReqId_in_response_in_create_jr)) (has_done WO__createNewJobRequisitionExisting))
     :effect (and
        (known jobReqId_in_response_in_create_jr)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---job_requisitions_filter_list
     :parameters ()
     :precondition (and (not (known job_requisitions_filter_list)) (has_done WO__getJobRequisitions_selector_multi))
     :effect (and
        (known job_requisitions_filter_list)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---status_in_query_get_jrs
     :parameters ()
     :precondition (not (known status_in_query_get_jrs))
     :effect (and
        (known status_in_query_get_jrs)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---HiringManager
     :parameters ()
     :precondition (not (known HiringManager))
     :effect (and
        (known HiringManager)
        (increase (total-cost ) 50))
    )


    (:action slot-filler---location_in_query_create_jr
     :parameters ()
     :precondition (not (known location_in_query_create_jr))
     :effect (and
        (known location_in_query_create_jr)
        (increase (total-cost ) 50))
    )



)
