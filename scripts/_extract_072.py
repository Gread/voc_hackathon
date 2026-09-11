import json, pathlib
out = pathlib.Path(r"C:/Users/RicardsonAlbuquerque/repos/Hack/data/cache/extract")

records = {}

records["cfpb_9500796"] = {"key": "d75a96fed6a901797368f8157c2fe7f8b692a8938a9d32da851c3fba6f4a274c", "response": {
    "contact_reasons": [
        {"reason": "unauthorized_or_fraud", "specific_reason": "sent funds after a caller impersonating Chase's Fraud Department claimed a transfer needed reversing; the $750.00 never came back and the claim was denied", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "told 'too bad for your bad luck you were scammed and nothing we can do' despite staff being aware of the scam pattern", "is_primary": False}
    ],
    "products": ["checking_or_savings", "money_transfer_or_p2p"],
    "services": ["phone_support"],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "was tricked by a caller posing as Chase's Fraud Department into sending a transfer to 'reverse' a supposed unauthorized transaction, losing $750.00",
    "underlying_driver": "the fraud claim was denied because the transaction was made from the customer's own phone, and staff admitted they knew of the scam but offered no help",
    "reason_differs": False,
    "topics": [
        {"topic_label": "fraud claim denied after impersonation scam", "issue_statement": "A caller posing as Chase's Fraud Department convinced the customer to send a transfer to 'reverse' a supposed unauthorized transaction, and the $750.00 never came back.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "claim declined because the transaction was made from the customer's own phone, despite being induced by a scammer posing as Chase Fraud", "outcome": "unresolved", "evidence": [
            {"quote": "They had me send a XXXX to reverse the attempt and that my funds would be back in my accountt in 24 hours - and all funds were gone and no return of monies.", "speaker": "narrative"},
            {"quote": "I received an email stating my claim was declined as the transaction was done ferom my phone.", "speaker": "narrative"}
        ]},
        {"topic_label": "dismissive response after reporting scam", "issue_statement": "After reporting the scam, representatives told the customer it was 'too bad for your bad luck' and that nothing could be done.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "staff_attitude_or_competence", "driver": "told 'too bad for your bad luck you were scammed and nothing we can do' despite being aware of the scam", "outcome": "unresolved", "evidence": [
            {"quote": "They said too bad for your bad luck you were scammed and nothing we can do.", "speaker": "narrative"},
            {"quote": "This needs to stop- if they are aware of the scam should they not have notified their customers?", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Customer lost $750.00 to a scammer impersonating Chase's Fraud Department; the fraud claim was denied because the transfer came from the customer's own phone, and staff gave a dismissive response."
}}

records["cfpb_9800159"] = {"key": "f985138bd47940ad8170b38183867488bc8f76656e428170e17f9234d25de319", "response": {
    "contact_reasons": [
        {"reason": "unauthorized_or_fraud", "specific_reason": "checking account and credit cards compromised by a scam, and the bank took all the money from the savings account", "is_primary": True},
        {"reason": "collections_or_debt", "specific_reason": "the bank is now demanding $1,700.00 be repaid despite the unresolved fraud claim", "is_primary": False}
    ],
    "products": ["checking_or_savings", "credit_card"],
    "services": [],
    "customer_ask": "stop_or_block",
    "stated_reason": "was a victim of a scam that compromised the checking account and credit cards, and the bank took all the money from the savings account",
    "underlying_driver": "the fraud investigation with the bank's fraud department went nowhere, and the bank is now demanding $1,700.00 be repaid",
    "reason_differs": False,
    "topics": [
        {"topic_label": "scam compromised accounts and drained savings", "issue_statement": "A scam compromised the checking account and credit cards, and the bank took all the money from the savings account.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "the bank took all the money from the savings account after the scam compromised the checking account and credit cards", "outcome": "unresolved", "evidence": [
            {"quote": "My checking account and some credit cards were compromised. The bank took all my money from my savings account.", "speaker": "narrative"},
            {"quote": "I almost lost my car, and I had to put some credit cards with a debt consolidation program because I couldn't make the delinquent payments.", "speaker": "narrative"}
        ]},
        {"topic_label": "fraud department made no progress", "issue_statement": "After filing a police report, working with the bank's fraud department went nowhere.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "no_response_or_follow_up", "driver": "the fraud department made no progress despite a filed police report", "outcome": "unresolved", "evidence": [
            {"quote": "I filed a police report and tried to work with the fraud department of the bank, but went no where.", "speaker": "narrative"}
        ]},
        {"topic_label": "bank now billing $1,700", "issue_statement": "After the unresolved fraud case, the bank is now demanding $1,700.00 be paid back.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "unexpected_charge", "driver": "the bank is demanding $1,700.00 be repaid despite the unresolved fraud claim", "outcome": "unresolved", "evidence": [
            {"quote": "now they want me to pay them $1700.00. NO WAY", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A scam compromised the customer's checking account and credit cards, the bank drained the savings account, the fraud department made no progress, and the bank is now demanding $1,700.00 be repaid."
}}

records["cfpb_10126239"] = {"key": "c52310caf813f7071eb30fcbf58ee3e8ba4779ee3baa707064f3b87ea03eb9a6", "response": {
    "contact_reasons": [
        {"reason": "unauthorized_or_fraud", "specific_reason": "two credit cards fraudulently opened in the husband's name using an old address and SSN, with over $43,000.00 and $3,000.00 in cash advances", "is_primary": True},
        {"reason": "collections_or_debt", "specific_reason": "a collection agency is now demanding payment for the fraudulent credit card debt", "is_primary": False}
    ],
    "products": ["credit_card", "debt_collection"],
    "services": ["phone_support"],
    "customer_ask": "fix_error",
    "stated_reason": "discovered two credit cards were fraudulently opened in the husband's name using an old address and Social Security number",
    "underlying_driver": "the fraudulent accounts accrued over $43,000.00 and $3,000.00 in cash advances, a police report has been pending for months, and a collection agency is now demanding payment",
    "reason_differs": False,
    "topics": [
        {"topic_label": "fraudulent credit cards opened in husband's name", "issue_statement": "Two credit cards were fraudulently opened in the husband's name using an old address and Social Security number, incurring over $43,000.00 and $3,000.00 in cash advances.", "product": "credit_card", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "over $43,000.00 and $3,000.00 of cash advances made on two credit cards fraudulently opened in the husband's name", "outcome": "unresolved", "evidence": [
            {"quote": "there were 2 credit cards fraudulently taken out in his name in XXXX using a previous address and his SS # where we have not lived at since XXXX", "speaker": "narrative"},
            {"quote": "He was told that on the 1st credit card there were numerous charges made at XXXX for cash advances totaling over $43000.00 in XXXX, PA.", "speaker": "narrative"}
        ]},
        {"topic_label": "collection notice for fraudulent debt", "issue_statement": "A collection agency is now demanding payment for the fraudulent credit card debt while the police report is still pending.", "product": "debt_collection", "sentiment": -1, "driver_category": "error_not_corrected", "driver": "a collection agency is demanding payment for the fraudulent debt although a police report is still pending and unresolved", "outcome": "unresolved", "evidence": [
            {"quote": "We now received a statement from a XXXX XXXX XXXX for collection of the money.", "speaker": "narrative"},
            {"quote": "We have not payed any money yet and will be disputing all of the debt with the collection agency.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved",
    "positive_moments": [{"what": "JPMorgan Chase updated the address and sent copies of the statements after multiple calls", "category": "helpful_staff", "quote": "After talking to several people at JPMorgan they were able to change the address on the credit cards to our current address and then sent us copies of the statements.", "speaker": "narrative"}],
    "redaction_heavy": False,
    "summary": "Two credit cards were fraudulently opened in the husband's name using an old address and SSN, running up over $46,000.00 combined in cash advances; a police report is still pending and a collection agency now wants payment."
}}

records["cfpb_10414743"] = {"key": "2f3b16eb37c7c23b0d45a7b9c703ebec7f21c96ac2136ce21dc07a80204b92be", "response": {
    "contact_reasons": [
        {"reason": "dispute_or_chargeback", "specific_reason": "the customer's own bank denied a dispute over an ATM withdrawal that never dispensed cash, with no evidence provided", "is_primary": True},
        {"reason": "fees_and_charges", "specific_reason": "$300.00 withdrawal plus $3.00 ATM fee charged even though the ATM never dispensed cash", "is_primary": False}
    ],
    "products": ["checking_or_savings"],
    "services": ["atm", "branch"],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "an ATM at a Chase branch failed to dispense a $300.00 cash withdrawal or a receipt, but the withdrawal and a $3.00 fee were still charged",
    "underlying_driver": "the dispute filed with the customer's own bank was denied with only generic transaction code and no proof cash was dispensed",
    "reason_differs": False,
    "topics": [
        {"topic_label": "ATM failed to dispense cash but charge posted", "issue_statement": "The ATM took a $300.00 withdrawal request and displayed a message to remove the card but never dispensed cash or a receipt, yet the $300.00 plus a $3.00 fee was charged.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "unexpected_charge", "driver": "$300.00 withdrawal plus $3.00 ATM fee charged despite the ATM never dispensing cash", "outcome": "unresolved", "evidence": [
            {"quote": "After several minutes of the machine counting, I received a message to remove my card. The machine didn't dispense any cash nor did it dispense a receipt.", "speaker": "narrative"},
            {"quote": "The $300.00 charge has been applied to my account. $300.00 withdrawl and $3.00 ATM fee.", "speaker": "narrative"}
        ]},
        {"topic_label": "dispute denied without evidence", "issue_statement": "The customer's bank denied the dispute over the failed ATM withdrawal and provided pages of transaction code but no evidence cash was dispensed.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "dispute denied with only generic transaction code, no video or proof of cash dispensed", "outcome": "unresolved", "evidence": [
            {"quote": "I received a notice from XXXX stating that my dispute was closed, and they had refused my dispute.", "speaker": "narrative"},
            {"quote": "They sent me XXXX paragraphs of code describing the transaction but no evidence of cash being dispensed.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "partially_resolved",
    "positive_moments": [{"what": "eventually received cash from a teller at the bank", "category": "helpful_staff", "quote": "I eventually went to the teller at the bank and successfully received cash.", "speaker": "narrative"}],
    "redaction_heavy": False,
    "summary": "A Chase ATM failed to dispense a $300.00 withdrawal, yet the charge posted; the customer's own bank denied the dispute with no proof, though a teller later provided the cash."
}}

records["cfpb_10834556"] = {"key": "9792441e664870835b8f3326c25b2c505900a1b86cdab1ec206ed807c02da007", "response": {
    "contact_reasons": [
        {"reason": "fees_and_charges", "specific_reason": "charged for a cash withdrawal the ATM company confirmed was denied", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "called the bank many times with proof from the ATM company and was still refused a refund", "is_primary": False}
    ],
    "products": ["checking_or_savings"],
    "services": ["atm", "phone_support"],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "was charged for a cash withdrawal that was denied at the ATM, despite the ATM company confirming the denial",
    "underlying_driver": "the bank ignored proof from the ATM company and refused to refund the charge after repeated calls",
    "reason_differs": False,
    "topics": [
        {"topic_label": "charged for a denied ATM withdrawal despite proof", "issue_statement": "A cash withdrawal was denied at the ATM, confirmed by the ATM company's proof, but the bank still charged for it and refused to reimburse.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "error_not_corrected", "driver": "charged for a withdrawal the ATM company confirmed was denied, and the bank ignored the proof provided", "outcome": "unresolved", "evidence": [
            {"quote": "cash withdrawal was denied XXXX and this was confirmed by the ATM company and provided me the proof of denied transactions, however the Chase bank still charged me and ignore the proof of denied transactions from the ATM company.", "speaker": "narrative"},
            {"quote": "Called the bank many times, provided them the information from the ATM company and yet they refused to pay me back.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "The customer was charged for a cash withdrawal that the ATM company confirmed was denied, and the bank has refused to refund it despite repeated calls with proof."
}}

records["cfpb_11155723"] = {"key": "5c5a1000b34f6a36f1a5277384368795e5429f1c5d95c465bb15b6fb7ceebba4", "response": {
    "contact_reasons": [
        {"reason": "payment_or_transfer_problem", "specific_reason": "a $600.00 transfer from an external account never posted despite a notice it would be available", "is_primary": True},
        {"reason": "terms_information_or_communication", "specific_reason": "the bank deleted the external account link without notice, which the disclosures do not clearly warn about", "is_primary": False}
    ],
    "products": ["checking_or_savings", "money_transfer_or_p2p", "credit_card"],
    "services": ["online_banking", "phone_support"],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "a $600.00 transfer from an external credit union account never appeared in the Chase checking account despite a notice it would be available",
    "underlying_driver": "the fraud department could not verify the external account, deleted it without notice, and the missing transfer caused a credit card payment to be missed and incur fees",
    "reason_differs": True,
    "topics": [
        {"topic_label": "external transfer never posted", "issue_statement": "A $600.00 transfer from an external credit union account never appeared in the checking account despite a notice that it would be available.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "$600.00 transfer confirmed as remitted never showed up as pending or available in the account", "outcome": "unresolved", "evidence": [
            {"quote": "I received a notice that the transfer would be remitted and available on XX/XX/year>. However, when viewing my balance on XX/XX/year>, I noticed that there was no hold pending or funds in my account from the transfer.", "speaker": "narrative"}
        ]},
        {"topic_label": "external account deleted without notice causing late fees", "issue_statement": "Chase deleted the external account link without notice after failing to verify it, causing a credit card payment to be missed and resulting in delinquency and interest fees.", "product": "credit_card", "sentiment": -2, "driver_category": "policy_or_terms_change", "driver": "external account was deleted without notice after a failed verification, causing a missed credit card payment, delinquency and interest fees", "outcome": "unresolved", "evidence": [
            {"quote": "In addition, Chase Bank decided to delete the account from my list of external accounts, again. Lastly, Chase failed to inform me, in any manner, that the transaction of $600.00 was in question by the bank.", "speaker": "narrative"},
            {"quote": "I stated that the act of the bank is unfair, deceptive, and abusive, and has resulted, at least in my case, monetary harm.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A $600.00 external transfer never posted after the bank's fraud department could not verify the account and deleted it without notice, causing a missed credit card payment and fees."
}}

records["cfpb_11477667"] = {"key": "e1ff6affd94003b8e26541ebfb2da603c3aaec0edb32333cd0461a05faa6cc88", "response": {
    "contact_reasons": [
        {"reason": "unauthorized_or_fraud", "specific_reason": "a $4,700.00 fraud claim for an ATM withdrawal was denied despite alibi evidence", "is_primary": True}
    ],
    "products": ["checking_or_savings"],
    "services": ["atm"],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "filed a fraud complaint about a $4,700.00 ATM withdrawal that was denied by the bank",
    "underlying_driver": "the bank denied the fraud claim without reviewing ATM camera footage despite alibi evidence like home camera footage and not owning a car",
    "reason_differs": False,
    "topics": [
        {"topic_label": "fraud claim denied without reviewing evidence", "issue_statement": "A $4,700.00 fraud claim for an ATM withdrawal was denied even though the customer has home camera footage proving they were home and does not drive.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "denied the fraud claim without checking ATM camera footage despite alibi evidence like home camera footage and not owning a car", "outcome": "unresolved", "evidence": [
            {"quote": "I files a fraud complain and CHASE bank denied, I recently got a copy of the police report which I will attach to this form, I'm requesting for CHASE to at least check the ATM camera, that will prove XXXX I was not the one that withdrew the money", "speaker": "narrative"},
            {"quote": "i know lots only $4700.00 but its all I have", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A $4,700.00 fraud claim for an unauthorized ATM withdrawal was denied even though the customer has home camera footage and a police report supporting they were not the one who withdrew the money."
}}

records["cfpb_12073317"] = {"key": "700641f6f49a262634e817450ebdb6ca8ff97ef09093ce2f545875aba78069f8", "response": {
    "contact_reasons": [
        {"reason": "unauthorized_or_fraud", "specific_reason": "a $660.00 purchase posted on a newly opened credit card before the physical card even arrived", "is_primary": True}
    ],
    "products": ["credit_card"],
    "services": [],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "a $660.00 unauthorized purchase posted on a newly opened credit card before the physical card even arrived",
    "underlying_driver": "a fraud dispute was filed but no response has been received and the balance still shows on the statement",
    "reason_differs": False,
    "topics": [
        {"topic_label": "unauthorized charge before card arrived", "issue_statement": "A $660.00 purchase posted on a newly opened credit card before the physical card even arrived, and the customer never made the purchase or had an account with the merchant.", "product": "credit_card", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "$660.00 charge from a merchant account the customer never created, posted before receiving the physical card", "outcome": "unresolved", "evidence": [
            {"quote": "I did not make this purchase and I didn't even have a XXXX account ( I did create one after to check if there was any order history under my email, which there was not ).", "speaker": "narrative"},
            {"quote": "I have received no word on this matter, the balance still shows in my account, and I would like this matter to be resolved and the charge cleared from my statement balance.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A $660.00 unauthorized charge posted on a newly opened credit card before the physical card even arrived, and the fraud dispute has gone unanswered."
}}

records["cfpb_12468314"] = {"key": "75a44c10b1150d52784595b1c1a74836739bb374c7ab939f67acdec18db44205", "response": {
    "contact_reasons": [
        {"reason": "payment_or_transfer_problem", "specific_reason": "an ATM deposit of $3,400.00 jammed and only $200.00 has been located so far", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "feels the bank is not taking the missing $3,400.00 seriously despite an urgent housing need", "is_primary": False}
    ],
    "products": ["checking_or_savings"],
    "services": ["atm", "branch", "phone_support"],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "an ATM deposit of $3,400.00 jammed and the bank says it can only find $200.00 of it so far",
    "underlying_driver": "the investigation is slow and the customer believes the bank is not taking it seriously while urgently needing the funds to avoid homelessness",
    "reason_differs": False,
    "topics": [
        {"topic_label": "ATM deposit malfunction, only part of funds found", "issue_statement": "An ATM deposit of $3,400.00 jammed and ejected the money with an error message, and after an investigation the bank says it can only find $200.00 of it.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned", "driver": "$3,400.00 ATM deposit jammed and ejected with an error, and the bank has only located $200.00 so far while still investigating", "outcome": "unresolved", "evidence": [
            {"quote": "As soon as I attempted to make the deposit the ATM jammed and tried to eject my money stating that the machine can no longer take deposits and a 1800 number appeared on the screen. My money is stuck in the machine.", "speaker": "narrative"},
            {"quote": "I deposited everything I had into that ATM and now they are claiming they can only find $200.00 but are still investigating.", "speaker": "narrative"}
        ]},
        {"topic_label": "investigation not taken seriously amid housing crisis", "issue_statement": "The customer says the bank is not taking the missing $3,400.00 seriously even though the money is needed urgently to secure housing and avoid homelessness.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "staff_attitude_or_competence", "driver": "customer believes the bank is not taking the missing $3,400.00 seriously despite urgent need to pay rent and avoid homelessness", "outcome": "unresolved", "evidence": [
            {"quote": "I do not believe they are taking it seriously because a simple audit would should the amount I deposited or even a service tech but the bank continued to let people use the ATM and basically ignored me.", "speaker": "narrative"},
            {"quote": "my children and I are homeless waiting for the bank to handle this investigation.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "An ATM deposit of $3,400.00 jammed and the bank has only located $200.00 so far, leaving the customer's family homeless while waiting on an investigation they feel is not being taken seriously."
}}

records["cfpb_12951516"] = {"key": "c89749b5486ac0fee2dbcc891b6a9ed4925fbdc73de113473f480154a1d185b8", "response": {
    "contact_reasons": [
        {"reason": "dispute_or_chargeback", "specific_reason": "Chase reversed a chargeback in the merchant's favor despite USPS proof the returned dress was delivered", "is_primary": True}
    ],
    "products": ["credit_card"],
    "services": [],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "Chase reversed a chargeback in the merchant's favor despite evidence the $110.00 dress was returned",
    "underlying_driver": "Chase closed the dispute after initially favoring the customer and refuses to reconsider despite additional documentation submitted",
    "reason_differs": False,
    "topics": [
        {"topic_label": "chargeback reversed despite return evidence", "issue_statement": "Chase initially reversed a $110.00 charge in the customer's favor but later reversed the chargeback back to the merchant despite USPS proof the dress was returned.", "product": "credit_card", "sentiment": -1, "driver_category": "error_not_corrected", "driver": "chargeback reversed in the merchant's favor despite a USPS return receipt and tracking number provided as evidence", "outcome": "unresolved", "evidence": [
            {"quote": "Initially, Chase reversed the charge in my favor. However, on XX/XX/2024, I was notified by Chase that they had decided to reverse the chargeback in favor of the merchant and closed the dispute.", "speaker": "narrative"},
            {"quote": "Despite this evidence, Chase has refused to reconsider or reopen the case.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Chase reversed a chargeback in the merchant's favor for a $110.00 returned dress despite USPS proof of the return, and refuses to reopen the dispute."
}}

records["cfpb_13453747"] = {"key": "1bb068c04d44686e58cc656f7870ee3c0a08bde0a50ffee8f2199b8240c984fb", "response": {
    "contact_reasons": [
        {"reason": "account_opening_or_closure", "specific_reason": "the account was closed with no explanation, which the customer believes followed from filing several disputes", "is_primary": True},
        {"reason": "dispute_or_chargeback", "specific_reason": "a merchant's technical checkout error caused multiple charges requiring several separate disputes", "is_primary": False}
    ],
    "products": ["other_or_unspecified"],
    "services": [],
    "customer_ask": "explanation",
    "stated_reason": "had to file numerous disputes because a merchant's technical checkout error caused repeated charges to post",
    "underlying_driver": "Chase closed the account, which the customer believes was caused by the number of disputes filed, without ever providing an explanation",
    "reason_differs": True,
    "topics": [
        {"topic_label": "repeated charges from checkout technical error", "issue_statement": "A recurring technical error during checkout caused numerous charges to post at different times, forcing the customer to file several separate disputes.", "product": "other_or_unspecified", "sentiment": -1, "driver_category": "system_or_app_failure", "driver": "a merchant checkout technical error caused multiple charges to post separately, requiring several separate disputes since each could only be disputed once posted", "outcome": "unknown", "evidence": [
            {"quote": "I had an issue with a merchant when attempting to make a purchase on their website due to a technical error that kept happening during the checkout process and due to the error it seemed as though the transactions were never processed however numerous charges ended up posting in my Chase account at various different times.", "speaker": "narrative"}
        ]},
        {"topic_label": "account closed without explanation", "issue_statement": "Chase closed the account, which the customer believes was caused by the number of disputes filed, without ever providing an explanation.", "product": "other_or_unspecified", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "account closed with no explanation, which the customer believes followed from filing several disputes over the technical-error charges", "outcome": "unresolved", "evidence": [
            {"quote": "It is the number of disputes that I had to file that I believe caused Chase to decide to close my account because there is nothing else related to my account that could possibly have contributed to the account closure but Chase would not provide me with an explanation", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A merchant's checkout technical error forced the customer to file multiple disputes, after which Chase closed the account without ever explaining why."
}}

records["cfpb_14007734"] = {"key": "8720b160854aac204f9b56ab04d6c76f4705827c2cb5c934adadf3ea4e249892", "response": {
    "contact_reasons": [
        {"reason": "dispute_or_chargeback", "specific_reason": "a dispute for an undelivered food order has not resulted in a refund", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "the bank said it would just let the account overdraw more instead of resolving the dispute", "is_primary": False}
    ],
    "products": ["checking_or_savings"],
    "services": [],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "filed a dispute because a food delivery order never arrived and wants the refund credited",
    "underlying_driver": "the bank treated the customer as if they were fabricating the claim and offered to let the account overdraw further instead of resolving it",
    "reason_differs": False,
    "topics": [
        {"topic_label": "undelivered food order dispute unresolved", "issue_statement": "A food delivery order never arrived, but the customer has not received the refund and feels treated as if they were lying about it.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "dispute for a non-delivered food order not refunded; customer feels disbelieved despite providing proof", "outcome": "unresolved", "evidence": [
            {"quote": "I had filed a complaint because XXXX  XXXX  didnt deliver my food to my address. I gave them the correct information and proved that my food didnt show up.", "speaker": "narrative"},
            {"quote": "I prodded that I did not get the refund from the company and they still treated me like I was making this up.", "speaker": "narrative"}
        ]},
        {"topic_label": "bank offers more overdraft instead of help", "issue_statement": "Instead of resolving the dispute, the bank said it would just let the account overdraw more, which the customer calls the worst customer service.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "staff_attitude_or_competence", "driver": "told the bank would let the account overdraw more instead of resolving the disputed charge", "outcome": "unresolved", "evidence": [
            {"quote": "The bank just said they will overdraw my account more.", "speaker": "narrative"},
            {"quote": "Worst customer service", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A dispute for an undelivered food order has not been refunded, and the bank offered to let the account overdraw further instead of resolving it, which the customer calls the worst customer service."
}}

records["cfpb_14566353"] = {"key": "f19d0b574948596c5c350258856dd6b87f128763f8210e3887d63ee5c6e4e371", "response": {
    "contact_reasons": [
        {"reason": "funds_hold_or_account_restriction", "specific_reason": "a legal hold was placed on a custodial account to satisfy a parent's legal fees without notice", "is_primary": True}
    ],
    "products": ["checking_or_savings"],
    "services": [],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "a legal hold was placed on the customer's own custodial account to satisfy the parent's legal fees, without notice",
    "underlying_driver": "the held funds were the customer's own employment earnings and they were not the defendant in the case",
    "reason_differs": False,
    "topics": [
        {"topic_label": "legal hold on custodial account without notice", "issue_statement": "Chase allowed a legal hold on the customer's custodial account to satisfy the parent's legal fees, even though the funds were the customer's own money from employment and they were never notified or a defendant.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "own employment earnings held to satisfy a parent's legal fees, with no notice given despite not being a party to the case", "outcome": "unresolved", "evidence": [
            {"quote": "Chase allowed a legal hold to be placed on a custodial account belonging to me, a XXXX  at the time, to satisfy legal fees tied to my parent.", "speaker": "narrative"},
            {"quote": "I was never notified, the funds were my own from employment, and I was not the defendant in the case.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A legal hold tied to a parent's legal fees was placed without notice on the customer's own custodial account funded by their employment earnings."
}}

records["cfpb_15233039"] = {"key": "f5d09ed26bcc13459f70c242ad794c6010b4389667685bc575754e6d1547358f", "response": {
    "contact_reasons": [
        {"reason": "funds_hold_or_account_restriction", "specific_reason": "the account was restricted within two days of opening and access was blocked until a new debit card arrived", "is_primary": True},
        {"reason": "terms_information_or_communication", "specific_reason": "multiple representatives gave conflicting information about a replacement card fee and how funds would be returned", "is_primary": False}
    ],
    "products": ["checking_or_savings"],
    "services": ["branch", "phone_support"],
    "customer_ask": "fix_error",
    "stated_reason": "the account was restricted within two days of opening it in person and access was blocked pending a new debit card",
    "underlying_driver": "multiple representatives gave conflicting information about fees, card replacement and refunds, and the branch could not fulfill what phone reps promised",
    "reason_differs": True,
    "topics": [
        {"topic_label": "account restricted right after opening", "issue_statement": "The account was restricted within two days of opening it at a branch, and access was blocked until a replacement debit card arrived by mail.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "system_or_app_failure", "driver": "account restricted two days after opening and access blocked until a new card arrived, blamed on a system error", "outcome": "unresolved", "evidence": [
            {"quote": "Within two days, my account was restricted, and I was told I could not access it until my new debit card arrived in the mail.", "speaker": "narrative"},
            {"quote": "I called Chase and was told they could not lift the restriction due to a system error and to call back on Monday.", "speaker": "narrative"}
        ]},
        {"topic_label": "conflicting information on fees and fund return", "issue_statement": "Multiple representatives gave conflicting answers about a $15.00 replacement card fee, whether it was waived, and how the funds would be returned.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information", "driver": "told conflicting things by different representatives about a $15.00 replacement card fee and different methods and timelines for returning funds", "outcome": "unresolved", "evidence": [
            {"quote": "I would need to pay $15.00 to express a replacement card.", "speaker": "narrative"},
            {"quote": "Another representative told me my new card was being courtesy expressed and that the $15.00 fee had been waived.", "speaker": "narrative"},
            {"quote": "The branch told me it is impossible to receive a check there.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A newly opened account was restricted within two days, and representatives gave conflicting answers about the replacement card fee and how the funds would be returned."
}}

records["cfpb_15852410"] = {"key": "cf252f520c94f22c45a62c38ac1e7c0ceb068481dd76da1460062f92e43bb56a", "response": {
    "contact_reasons": [
        {"reason": "unauthorized_or_fraud", "specific_reason": "sent money for fake work-from-home equipment after a school's job posting system was hacked, and the bank refused to refund it", "is_primary": True}
    ],
    "products": ["checking_or_savings"],
    "services": [],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "sent money for a work-from-home job scam after the school's system was hacked; the bank refused to refund it",
    "underlying_driver": "police said the bank was supposed to refund the money but the bank never did, causing financial strain",
    "reason_differs": False,
    "topics": [
        {"topic_label": "scam refund refused despite police report", "issue_statement": "Money sent for fake work-from-home equipment through a hacked school job posting was never refunded by the bank even though police said it should be.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "bank refused to refund the scam payment even though police said the bank was supposed to refund it", "outcome": "unresolved", "evidence": [
            {"quote": "I explained to my bank chase at the time what happened they refused to refund my money, I also called police and filed a police report.", "speaker": "narrative"},
            {"quote": "Police said the bank was supposed to refund me but that didnt happen caused a financial strain on me as I was to get a job to help my mom with bills", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Money sent for a fake work-from-home job after a school's system was hacked was never refunded, even though police said the bank should refund it."
}}

records["cfpb_16605361"] = {"key": "ee5f40fc3a6a7f566884ec2ba2a1d11d720a73abd7d16f4875b307957764bc0d", "response": {
    "contact_reasons": [
        {"reason": "account_opening_or_closure", "specific_reason": "account closed for alleged suspicious activity with no explanation or notice", "is_primary": True},
        {"reason": "credit_reporting", "specific_reason": "wants any negative reporting shared with a reporting agency removed", "is_primary": False}
    ],
    "products": ["checking_or_savings"],
    "services": [],
    "customer_ask": "explanation",
    "stated_reason": "Chase closed the account for alleged suspicious activity with no explanation or notice",
    "underlying_driver": "the customer denies any involvement in fraud and wants documentation of the decision and removal of any negative reporting",
    "reason_differs": False,
    "topics": [
        {"topic_label": "account closed without explanation", "issue_statement": "Chase closed the account for alleged suspicious activity without explanation, and the customer wants documentation of the decision and removal of any negative reporting shared with a reporting agency.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "account closed for alleged suspicious activity with no reason given and refusal to reopen or explain", "outcome": "unresolved", "evidence": [
            {"quote": "Chase closed my account for alleged suspicious activity without explanation or notice.", "speaker": "narrative"},
            {"quote": "I was not involved in any fraud, and they refuse to provide a reason or reopen my account.", "speaker": "narrative"},
            {"quote": "Im requesting documentation of the decision and removal of any negative reporting shared with XXXX XXXX XXXX.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Chase closed the account for alleged suspicious activity without any explanation, and the customer wants documentation of the decision and removal of any negative reporting."
}}

records["cfpb_17185734"] = {"key": "9dca2ceedcea9d5ec65772f1158a000968cf96657944ed66ce3e3fddc355161b", "response": {
    "contact_reasons": [
        {"reason": "unauthorized_or_fraud", "specific_reason": "paid money under duress in a jury-duty bail scam; the bank refunded it then reversed the claim", "is_primary": True}
    ],
    "products": ["checking_or_savings"],
    "services": ["mobile_app", "phone_support"],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "fell victim to a jury-duty bail scam and paid money under threat of arrest; the bank initially refunded then reversed the claim",
    "underlying_driver": "the bank determined the transaction was authorized because it was made in person, despite being coerced by the scam",
    "reason_differs": False,
    "topics": [
        {"topic_label": "bail scam payment claim reversed", "issue_statement": "After being coerced by a fake jury-duty bail scam into paying under threat of arrest, the bank refunded the payment but later reversed the claim because the transaction was made in person.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "claim reversed because the payment was physically made, even though it was induced by a scam threatening arrest", "outcome": "unresolved", "evidence": [
            {"quote": "I have now filed a police report ( they wouldn't take XXXX previously because I had gotten my money back ) and I'm trying to get my claim accepted.", "speaker": "narrative"},
            {"quote": "Cut to today, I see they reversed my claim because while being scammed and under the impression I would be arrested if I didn't send money, I still physically made the transaction.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved",
    "positive_moments": [
        {"what": "the bank refunded the payment after the customer reported the scam", "category": "fast_resolution", "quote": "I called and talked to XXXX, told them everything, and they were able to refund me.", "speaker": "narrative"},
        {"what": "store staff were sympathetic when told about the scam", "category": "helpful_staff", "quote": "They were very nice, said they'd keep an eye out for this scam.", "speaker": "narrative"}
    ],
    "redaction_heavy": False,
    "summary": "A jury-duty bail scam coerced a payment that the bank first refunded, then reversed on the grounds the transaction was made in person; the customer is trying to get the claim reinstated."
}}

records["cfpb_18221818"] = {"key": "46df7c063628ba2c310fd83c04765128df82938a9e4e93cf53d299318672bd7e", "response": {
    "contact_reasons": [
        {"reason": "credit_decision_or_limit", "specific_reason": "credit card shut down and limit set to $0.00 after the first late payment in 10 years", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "three representatives, one rude, could not explain the shutdown after 1.5 hours on the phone", "is_primary": False}
    ],
    "products": ["credit_card"],
    "services": ["phone_support"],
    "customer_ask": "explanation",
    "stated_reason": "the credit card was shut down and the limit set to $0.00 after the first late payment in 10 years, despite a stated grace period",
    "underlying_driver": "three representatives could not explain the shutdown and one was rude, and the terms do not mention this consequence for a late payment",
    "reason_differs": False,
    "topics": [
        {"topic_label": "card shut down after first late payment", "issue_statement": "The credit card was shut down and the credit limit set to $0.00 after the first late payment in 10 years, despite a stated 21-day grace period.", "product": "credit_card", "sentiment": -1, "driver_category": "policy_or_terms_change", "driver": "credit limit dropped to $0.00 and card shut down after one late payment even though the terms show a 21-day grace period", "outcome": "unresolved", "evidence": [
            {"quote": "I went to use my card today and it shows I have $0.00 credit balance, which is not true.", "speaker": "narrative"},
            {"quote": "No where in the terms in conditions does it say they can shut a credit limit down, due to a late pay. In fact they show a grace period of 21 days.", "speaker": "narrative"}
        ]},
        {"topic_label": "unhelpful and rude support", "issue_statement": "Three different representatives, including one described as rude, could not explain why the account was shut down after 1.5 hours on the phone.", "product": "credit_card", "sentiment": -1, "driver_category": "staff_attitude_or_competence", "driver": "spent an hour and a half on the phone with three representatives, one rude, none able to explain the shutdown", "outcome": "unresolved", "evidence": [
            {"quote": "I spent about an hour and a half on the phone with Chase Bank. I spoke to 3 different people who could not give me an answer as to why this has happened.", "speaker": "narrative"},
            {"quote": "The so called XXXX argued with me over the situation and was the most rude of the three people I talked to and still could not offer an explanation.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A credit card was shut down and its limit set to $0.00 after the first late payment in 10 years, and three representatives, one rude, could not explain why."
}}

records["cfpb_18636324"] = {"key": "ac6079bc84eff596b8219d53f5e849dcff5a0e4c43f85223e58519c238378741", "response": {
    "contact_reasons": [
        {"reason": "payment_or_transfer_problem", "specific_reason": "$160.00 withdrawn via autopay from a closed account before the bill even arrived", "is_primary": True},
        {"reason": "fees_and_charges", "specific_reason": "a $49.00 refund owed was applied to a different charge instead of being returned", "is_primary": False}
    ],
    "products": ["checking_or_savings"],
    "services": [],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "an unauthorized $160.00 withdrawal was taken via autopay from a closed account before the bill was even received",
    "underlying_driver": "the company failed to send required return materials, withheld a $49.00 refund, and applied it to a different charge",
    "reason_differs": False,
    "topics": [
        {"topic_label": "unauthorized withdrawal after account closure", "issue_statement": "The company withdrew $160.00 through autopay from the bank account after the account was closed and before the bill even arrived, leaving no chance to review or dispute the charge.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "unexpected_charge", "driver": "$160.00 autopay withdrawal taken from the account for a closed service before the bill arrived, with no opportunity to dispute first", "outcome": "unresolved", "evidence": [
            {"quote": "Despite the account being closed, XXXX withdrew $160.00 from my Chase bank account through autopay before I even received the bill, and after failing to send the prepaid return box they told me was required to avoid equipment charges.", "speaker": "narrative"},
            {"quote": "By the time this bill arrived in the mail, XXXX had already withdrawn the $160.00, giving me no opportunity to review or dispute the charge before the money was taken.", "speaker": "narrative"}
        ]},
        {"topic_label": "refund withheld and applied elsewhere", "issue_statement": "A $49.00 refund shown as a balance forward credit was never returned; instead it was applied toward a charge caused by the company's own failure to send return materials.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "$49.00 refund owed was applied to an equipment charge instead of being returned", "outcome": "unresolved", "evidence": [
            {"quote": "XXXX also failed to issue the $49.00 refund that appears on the bill as Balance Forward : - $49.00. Instead of returning this money to my bank account, XXXX applied it toward a charge caused by their failure to provide return materials.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A $160.00 autopay withdrawal was taken from a closed account before the bill arrived, and a separate $49.00 refund owed was applied to another charge instead of being returned."
}}

records["cfpb_19671617"] = {"key": "ddb2ad5bcb41bc25d6759c33787f4ed75dbd6298b4ffb6c7d47155196a602ec9", "response": {
    "contact_reasons": [
        {"reason": "customer_service_experience", "specific_reason": "a restrictive note was placed on the account right after the customer corrected the bank's inaccurate refund statements", "is_primary": True},
        {"reason": "fees_and_charges", "specific_reason": "multiple NSF fees charged after the debit card was disabled following a fraud dispute", "is_primary": False},
        {"reason": "terms_information_or_communication", "specific_reason": "Chase's CFPB response contains inaccurate statements about the disputed charge", "is_primary": False}
    ],
    "products": ["checking_or_savings"],
    "services": ["phone_support"],
    "customer_ask": "escalation_or_complaint",
    "stated_reason": "Chase placed a restrictive internal note on the account immediately after the customer corrected the bank's inaccurate statements about NSF fee refunds",
    "underlying_driver": "disabling the debit card after a fraud dispute caused reliance on slow ACH transfers and multiple NSF fees, and escalation staff gave inaccurate information and interrupted the customer before imposing a punitive note",
    "reason_differs": True,
    "topics": [
        {"topic_label": "NSF fees from disabled debit card", "issue_statement": "After marking a disputed $1,700.00 charge as unauthorized, Chase disabled the debit card, forcing reliance on slow ACH transfers and causing multiple NSF fees.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "unexpected_charge", "driver": "multiple NSF fees charged after the debit card was disabled following a fraud dispute, forcing reliance on slow ACH transfers", "outcome": "resolved", "evidence": [
            {"quote": "I correctly marked the charge as unauthorized in response to Chases fraud alert, which caused Chase to disable my debit card. This removed my only ability to immediately deposit funds into my account, forcing me to rely on slow ACH transfers. During this time, multiple NSF fees were charged.", "speaker": "narrative"}
        ]},
        {"topic_label": "escalation staff gave inaccurate information", "issue_statement": "An escalation representative spoke rapidly and repeatedly interrupted the customer, and Executive Support insisted all NSF fees were already refunded when they were not.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information", "driver": "Executive Support representative repeatedly claimed all NSF fees were refunded when they were not, and interrupted the customer instead of reviewing the statement", "outcome": "resolved", "evidence": [
            {"quote": "the representative spoke extremely rapidly while reading transactions and repeatedly told me let me finish, but would interrupt me whenever I attempted to ask questions or explain discrepancies.", "speaker": "narrative"},
            {"quote": "the representative initially insisted that all NSF fees had already been refunded. I checked my statement and repeatedly told her that they were not all refunded.", "speaker": "narrative"}
        ]},
        {"topic_label": "punitive note after correcting the error", "issue_statement": "After finally acknowledging and refunding the remaining NSF fees, the representative placed a note on the account blocking future courtesy fee refunds, right after the customer corrected the bank's error.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "staff_attitude_or_competence", "driver": "a note was placed on the account blocking future courtesy fee refunds immediately after the customer corrected the representative's inaccurate refund claims", "outcome": "unresolved", "evidence": [
            {"quote": "she refunded the remaining fees but explicitly said she was placing a note on my account to prevent any future \" courtesy '' fee refunds unless caused by bank error.", "speaker": "narrative"},
            {"quote": "This restriction appears to be punitive and directly related to my disputes and escalation.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "partially_resolved",
    "positive_moments": [{"what": "standard customer service handled the matter professionally, unlike escalation and executive support", "category": "helpful_staff", "quote": "The only department that handled this matter professionally was standard customer service.", "speaker": "narrative"}],
    "redaction_heavy": False,
    "summary": "After a fraud dispute led to a disabled debit card and NSF fees, escalation and Executive Support staff gave inaccurate information and interrupted the customer, then placed a punitive note on the account right after being corrected."
}}

records["cfpb_20153672"] = {"key": "d7ea90257c84edf3bb937b065cfa56d21f313e519f8e2439a8d2d9e0b276180d", "response": {
    "contact_reasons": [
        {"reason": "unauthorized_or_fraud", "specific_reason": "four unauthorized ATM withdrawals totaling $1,700.00 while the card and phone were at home; only $1,400.00 was refunded", "is_primary": True}
    ],
    "products": ["checking_or_savings"],
    "services": ["atm", "phone_support"],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "four ATM withdrawals totaling $1,700.00 occurred while the customer's card and phone were at home and were reported as fraud",
    "underlying_driver": "the bank credited $1,400.00 but refuses to refund the remaining $290.00 without explaining the discrepancy",
    "reason_differs": False,
    "topics": [
        {"topic_label": "unauthorized ATM withdrawals partially reimbursed", "issue_statement": "Four ATM withdrawals totaling $1,700.00 occurred at a branch 35 minutes away while the card and phone were at home, and only $1,400.00 has been refunded.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "$290.00 of the $1,700.00 in unauthorized ATM withdrawals remains unrefunded, with no explanation for the difference", "outcome": "unresolved", "evidence": [
            {"quote": "On XX/XX/year>, four ATM withdrawals totaling $1700.00 occurred at a Chase branch approximately 35 minutes from my home. At the time of the withdrawals, my debit card and phone were in my possession and I was at my residence.", "speaker": "narrative"},
            {"quote": "Chase credited $1400.00 but refused to refund the remaining $290.00, stating it was the difference between the amount debited and the amount recorded.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "partially_resolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Four unauthorized ATM withdrawals totaling $1,700.00 occurred while the card and phone were at home; the bank refunded $1,400.00 but withholds the remaining $290.00 without explanation."
}}

records["cfpb_21213380"] = {"key": "85ae503cc3e686c00b773bdbb8b09d0cfce56cee25192cdd2397957c3163f3bb", "response": {
    "contact_reasons": [
        {"reason": "unauthorized_or_fraud", "specific_reason": "$1,100.00 moved through a fake job platform's task-based employment scam, classified by the bank as authorized", "is_primary": True}
    ],
    "products": ["checking_or_savings", "money_transfer_or_p2p"],
    "services": [],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "$1,100.00 was transferred out due to a task-based employment scam that manipulated the customer into moving money to a cash app and then crypto",
    "underlying_driver": "the bank classified the transactions as authorized rather than fraud by deception and denied or did not fully resolve the dispute",
    "reason_differs": False,
    "topics": [
        {"topic_label": "scam-induced transfers classified as authorized", "issue_statement": "$1,100.00 was moved through a fake job platform that induced transfers to a cash app and then bitcoin, and the bank denied the fraud dispute by classifying the transactions as authorized.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "transactions classified as authorized despite being induced through a fake job platform's deceptive scheme", "outcome": "unresolved", "evidence": [
            {"quote": "My bank has denied or not fully resolved my dispute by classifying these transactions as authorized.", "speaker": "narrative"},
            {"quote": "If you deny I will file a complaint with Consumer Financial Protection Bureau and Better Business Bureau and XXXX XXXXl Office.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A task-based employment scam induced $1,100.00 in transfers to a cash app and crypto wallet, and the bank classified the transactions as authorized rather than fraud by deception, prompting a threat to escalate to regulators."
}}

records["cfpb_22423299"] = {"key": "575f39f83fb9b55c7950f12105a4f65d6ddcaf91e44a6cc4467dc1bf44ad21cd", "response": {
    "contact_reasons": [
        {"reason": "funds_hold_or_account_restriction", "specific_reason": "credit limit set to $0.00 for days despite a $4,000.00 payment posting to the account", "is_primary": True}
    ],
    "products": ["credit_card"],
    "services": ["online_banking", "phone_support"],
    "customer_ask": "fix_error",
    "stated_reason": "a $4,000.00 credit card payment posted to the account, but the credit limit was set to $0.00 and remains unavailable",
    "underlying_driver": "the bank holds newly posted payments before making credit available, with delays extending days without explanation while the customer is traveling abroad",
    "reason_differs": False,
    "topics": [
        {"topic_label": "credit limit zeroed despite posted payment", "issue_statement": "A $4,000.00 payment posted to the credit card account, yet the credit limit was set to $0.00, leaving no usable credit while traveling abroad.", "product": "credit_card", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "credit limit set to $0.00 for days after a $4,000.00 payment posted, with no access to the resulting credit or overpayment", "outcome": "unresolved", "evidence": [
            {"quote": "Later that day, my card was declined. Looking at the portal, my current balance was reflected as XXXX, meaning based on the current balance Chase technically owed me $850.00. I had $660.00 left in pending transactions. My credit limit was set to $0.00.", "speaker": "narrative"},
            {"quote": "I have not been given a reason for why there will be this delay, other than it is still \" processing '' even though it is reflected as posted in my account portal.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A $4,000.00 credit card payment posted, but the credit limit was set to $0.00 for days with no explanation, leaving the customer unable to access credit while traveling abroad."
}}

records["cfpb_23215773"] = {"key": "137ebfc7c931ed1d01dc0903f4ffa786f2a9f7a56de1dab598360ac34c09e752", "response": {
    "contact_reasons": [
        {"reason": "payment_or_transfer_problem", "specific_reason": "checks over $110,000.00 belonging to the customer and brother were deposited into someone else's Chase account", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "the Executive office called twice but never sent the promised email with account details", "is_primary": False}
    ],
    "products": ["checking_or_savings", "money_transfer_or_p2p"],
    "services": ["phone_support"],
    "customer_ask": "explanation",
    "stated_reason": "checks worth over $110,000.00 belonging to the customer and their brother were deposited into someone else's Chase account instead of the intended investment house",
    "underlying_driver": "despite two calls from Chase's Executive office, they never followed through with sending the requested account and check information",
    "reason_differs": False,
    "topics": [
        {"topic_label": "misdirected checks deposited into wrong account", "issue_statement": "Investment checks for over $110,000.00, made out to the customer and their brother, were deposited into a Chase account that is not theirs instead of the intended investment house.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "checks worth over $110,000.00 not made out to the account holder were deposited without the identification checks normally required at a branch", "outcome": "unresolved", "evidence": [
            {"quote": "The checks that were for over $110000.00 and in my and my brothers names were deposited in to their account. JP MORGAN Chase Account number XXXX.", "speaker": "narrative"},
            {"quote": "How is it legal to deposit checks that are neither made out to them, or have anything to do with them? If I went to deposit a check at the bank, I need to have identification and it is confirmed.", "speaker": "narrative"}
        ]},
        {"topic_label": "executive office failed to follow through", "issue_statement": "The Executive office called twice but never sent the promised email with the account numbers and cancelled checks needed to resolve the misdirected deposit.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "no_response_or_follow_up", "driver": "Executive office called twice but never sent the promised follow-up email with account details", "outcome": "unresolved", "evidence": [
            {"quote": "I have had 2 calls from the \" Executive office '' for JP Morgan. Both times I asked them to send me an email with the information they are question ( Account numbers and cancelled checks ) which I am happy to provide to them BOTH TIMEs, they have failed to follow through with sending me a simple email that I can send them this information they need.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Investment checks worth over $110,000.00 meant for the customer and their brother were deposited into someone else's Chase account, and the Executive office has twice failed to follow through on sending requested details."
}}

records["cfpb_9501120"] = {"key": "dcf9c73d986e1a5410c8161c7ed77774ce1b2c7a83eb274b63a99e163aa3331b", "response": {
    "contact_reasons": [
        {"reason": "unauthorized_or_fraud", "specific_reason": "credited fraud charges on a Chase Sapphire credit card were later reversed, with the bank claiming the card was never reported stolen", "is_primary": True}
    ],
    "products": ["credit_card"],
    "services": ["phone_support"],
    "customer_ask": "refund_or_reversal",
    "stated_reason": "unauthorized charges appeared on the Chase Sapphire credit card after realizing a phone was missing; the charges were credited and then reversed",
    "underlying_driver": "the bank now disputes that the fraud report was made and is withholding the credited amount, demanding a police report it originally said it did not need",
    "reason_differs": False,
    "topics": [
        {"topic_label": "fraud claim reversed despite prior credit", "issue_statement": "Unauthorized charges appeared on the Chase Sapphire credit card, were reported stolen and credited, but months later the bank reversed the credit, claiming the card was never reported stolen and now wants the police report it originally declined.", "product": "credit_card", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "credited fraud charges were reversed months later on the claim the card was never reported stolen, though it had been, and the bank now demands a police report it earlier said it did not need", "outcome": "unresolved", "evidence": [
            {"quote": "I called chase reported it stolen and was credited the amounts back after a XXXX. XXXX  XXXX later they are saying I made the purchases and that I never reported the card stolen and I did which is why a new card was given to me.", "speaker": "narrative"},
            {"quote": "I even offered the police report the XXXX and they said they didn't need it and today XX/XX/XXXX they are asking for it but won't refund me the total amount they are charging me.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved",
    "positive_moments": [{"what": "was issued a credit and a new card right after reporting the shared card stolen", "category": "fast_resolution", "quote": "I reported the card stolen to XXXX  XXXX and was issued a credit and a new card was given to me.", "speaker": "narrative"}],
    "redaction_heavy": False,
    "summary": "Unauthorized charges on a Chase Sapphire credit card were credited after a fraud report but later reversed, with the bank now claiming the card was never reported stolen and demanding a police report it earlier declined."
}}

for call_id, rec in records.items():
    (out / f"{call_id}.json").write_text(json.dumps({"key": rec["key"], "prompt_version": "ext-1.0",
        "schema_version": "1", "taxonomy_version": "1", "call_id": call_id, "model": "claude-agent-build",
        "produced_by": "claude_agent", "created_at": "2026-09-11T12:00:00Z", "usage": None,
        "response": rec["response"]}, ensure_ascii=False), encoding="utf-8")
print("wrote", len(records))
