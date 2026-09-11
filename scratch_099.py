import json, pathlib

bundle = json.load(open('data/work/extract_bundles/bundle_099.json', encoding='utf-8'))
texts = {r['call_id']: r['text'] for r in bundle['records']}
keys = {r['call_id']: r['cache_key'] for r in bundle['records']}

R = {}

R['cfpb_10911224'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "an account was hacked and unauthorized purchases were made; a temporary credit was issued and the customer worries it may be reversed", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants assurance the temporary credit for the hacked account will not be reversed",
  "underlying_driver": "unauthorized purchases were made after the account was hacked, and the customer fears the temporary credit issued will later be taken back",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "hacked account with unauthorized purchases",
      "issue_statement": "An account was hacked and unauthorized purchases were made that the customer cannot afford, and while a temporary credit was issued, there is concern it will be reversed.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "unauthorized purchases were made after a hack, and the temporary credit issued may still be reversed",
      "outcome": "unknown",
      "evidence": [
        {"quote": "My XXXX account got hacked over XXXX dollars was taken and I did not authorize these purchases", "speaker": "narrative"},
        {"quote": "My bank gave me a temporary credit but I want to make sure it doesnt get reversed.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unknown",
  "positive_moments": [
    {"what": "the bank issued a temporary credit for the unauthorized purchases", "category": "fast_resolution", "quote": "My bank gave me a temporary credit but I want to make sure it doesnt get reversed.", "speaker": "narrative"}
  ],
  "redaction_heavy": True,
  "summary": "An account was hacked and unauthorized purchases were made; Chase issued a temporary credit, but the customer is worried it will later be reversed."
}

R['cfpb_11205174'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a caller claiming to be from Chase's fraud department, who already had partial personal information, tried to get the customer transferred to file a fraud report despite having no Chase accounts", "is_primary": True}
  ],
  "products": ["other_or_unspecified"],
  "services": ["phone_support"],
  "customer_ask": "other",
  "stated_reason": "reporting a suspicious call claiming to be from Chase's fraud department",
  "underlying_driver": "a caller with a thick accent already had the customer's last four SSN digits and name, claimed someone tried to open a card in her name, and tried to transfer her to file a report, despite her having no Chase card or account",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "suspicious call impersonating chase fraud department",
      "issue_statement": "A caller claiming to be from Chase's fraud department already had the customer's name and partial social security number and tried to transfer her to file a report, though she has no Chase account.",
      "product": "other_or_unspecified",
      "sentiment": -1,
      "driver_category": "other_or_unclear",
      "driver": "the caller already possessed partial personal information and pushed toward a transfer and report despite the customer having no relationship with Chase",
      "outcome": "resolved",
      "evidence": [
        {"quote": "He had my last XXXX digits of my social security number and my name.", "speaker": "narrative"},
        {"quote": "I do not have a XXXX card or bank account", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "resolved",
  "positive_moments": [
    {"what": "the customer declined to give any information and hung up on the suspicious caller", "category": "fast_resolution", "quote": "I did not give him any info and hung up.", "speaker": "narrative"}
  ],
  "redaction_heavy": True,
  "summary": "A caller impersonating Chase's fraud department, who already had partial personal information, tried to get the customer to file a fraud report despite her having no Chase accounts, and she hung up without providing anything."
}

R['cfpb_11544905'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a $310.00 scam software charge was refunded by check and the account was closed, but the same charge later reappeared on the closed account", "is_primary": True},
    {"reason": "fees_and_charges", "specific_reason": "a $29.00 late fee and $5.00 interest charge were added to an account that had already been closed", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants the reappeared $310.00 charge and resulting fees removed from an account already closed and refunded",
  "underlying_driver": "the bank issued a refund check and confirmed account closure, but the same $310.00 charge then reappeared on the closed account along with a late fee and interest, and the dispute was ultimately resolved against the customer",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "refunded charge reappeared on closed account",
      "issue_statement": "A $310.00 scam software charge was refunded by check and the account confirmed closed, but the same charge reappeared on a statement for the closed account months later.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "the bank confirmed the account closed with a zero balance after refunding $310.00, but the same amount later reappeared, and the resulting dispute was resolved to keep it on the account",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I received Bank statement dated XX/XX/XXXX showing a charge of $310.00 had been made to my account that was closed on XX/XX/XXXX.", "speaker": "narrative"},
        {"quote": "stating the resolved the dispute saying the amount was to stay on the account to the account that was closed", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "late fee and interest on closed account",
      "issue_statement": "A $29.00 late fee and $5.00 interest charge were added to the same account that had already been confirmed closed.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "unexpected_charge",
      "driver": "a late fee and interest charge were applied to an account that had already been closed with a zero balance",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "showing a new balance in the amount of $350.00 which added a late fee of $29.00 and a interest charge of $5.00 to my account that was closed", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "the bank issued a refund check for the original scam charge", "category": "fair_outcome", "quote": "Bank issued me a check on XX/XX/XXXX in the amount of $310.00.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A $310.00 scam software charge was refunded and the account confirmed closed, but the same charge later reappeared along with a late fee and interest, and the resulting dispute was resolved to keep it on the closed account."
}

R['cfpb_12130884'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "fraudulent chip transactions were ruled valid because Chase says chips cannot be duplicated, despite known reports of similar hacks on other Chase accounts", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the disputed chip transactions overturned in his favor",
  "underlying_driver": "Chase ruled that chip transactions cannot be duplicated, so the charges must have been made by the customer, without acknowledging widely reported chip cloning affecting other Chase accounts",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "chip fraud dispute denied as impossible to duplicate",
      "issue_statement": "Fraudulent charges were ruled valid because Chase said the chip could not have been duplicated, despite widely reported chip cloning affecting thousands of other Chase debit accounts.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase overturned the dispute saying the chip cannot be duplicated, and could not explain how the customer could prove his innocence beyond that",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "They later overturned the dispute in the vendors favor saying that my chip was used and they cant be duplicated so it had to have been me.", "speaker": "narrative"},
        {"quote": "i was told \" prove it wasn't you who used the card in another dispute '' and when i asked how i would do that they told me they can not tell me", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Fraudulent chip transactions were ruled valid because Chase claims chips cannot be duplicated, leaving a decade-long customer with no way to prove his innocence despite widely reported chip cloning on other accounts."
}

R['cfpb_12533226'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a Holder in Due Course arbitration claim against Chase over a bankrupt auto manufacturer resulted in a settlement offer far below what other owners of the same trim received", "is_primary": True}
  ],
  "products": ["auto_loan"],
  "services": [],
  "customer_ask": "other",
  "stated_reason": "wants a fair settlement matching what other owners of the identical vehicle trim were offered",
  "underlying_driver": "Chase misclassified the vehicle as the lowest-priced model and offered $36000.00, far below the over $55000.00 offered to owners of the identical trim, and never filed arbitration as promised",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "settlement offer misclassifies vehicle trim",
      "issue_statement": "After the vehicle manufacturer went bankrupt, Chase offered a $36000.00 settlement that misclassified the vehicle as the lowest-priced model, while owners of the identical trim received over $55000.00.",
      "product": "auto_loan",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase's settlement offer misclassified the vehicle trim and undervalued it far below the amount offered to owners of the exact same trim",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase sends an offer for settlement which classified the XXXX XXXX XXXX as the lowest priced model, even though the vehicle was the highest priced", "speaker": "narrative"},
        {"quote": "I was only provided an offer of $36000.00", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "After the vehicle manufacturer's bankruptcy, Chase offered a $36000.00 Holder in Due Course settlement that misclassified the vehicle's trim, well below the over $55000.00 offered to owners of the identical model, and never filed the promised arbitration."
}

R['cfpb_13014395'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "fraudulent transactions were reported multiple times, the account was closed, but the customer was still held responsible for the disputed charges", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants to no longer be held responsible for charges from transactions reported as fraud",
  "underlying_driver": "Chase closed the account after repeated fraud reports but still held the customer liable for the charges, and monthly payments continue without resolution",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "held responsible for reported fraud charges",
      "issue_statement": "After multiple fraud reports, Chase closed the account but still held the customer responsible for the fraudulent charges, and monthly payments continue with no resolution.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase closed the account over repeated fraud reports but still held the customer liable for the charges, unresolved despite continued payments",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase closed my account but held me responsible for the charges.", "speaker": "narrative"},
        {"quote": "Ive continued to pay my monthly payments however weve not reached resolution.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase closed an account after repeated fraud reports but continues to hold the customer responsible for the disputed charges, which remain unresolved despite continued monthly payments."
}

R['cfpb_13560166'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a card was flagged as fraud and replaced without notice while the customer was traveling abroad, leaving them without card access for the entire trip", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "17 different representatives each promised to fix the card access problem during a 35-day overseas trip but none did", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wanted card access restored while stranded overseas without being able to buy food or lodging",
  "underlying_driver": "Chase flagged the card as fraud and mailed a replacement home without notifying the customer, who was then unable to use the card for 35 days abroad despite 17 representatives promising to fix it, and was ultimately only offered a costly wire transfer",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "card flagged and replaced without notice while abroad",
      "issue_statement": "Chase flagged the card as fraud and mailed a new one home without any notice, leaving the customer without a usable card for a full 35-day trip abroad.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "system_or_app_failure",
      "driver": "the card was flagged as fraud and replaced without phone, text or email notice, leaving no way to use it for the entire 35-day trip",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase placed our XXXX XXXX card as Fraud and did not notify up by us by phone, txt or email", "speaker": "narrative"},
        {"quote": "This left us in a significantly difficult situation overseas and unable to purchase food, lodging, etc.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "seventeen representatives failed to restore access",
      "issue_statement": "Seventeen different Chase representatives each promised to solve the card access problem during the trip, but none did, and the final solution offered was a costly wire transfer with fees and 29% interest.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "no_response_or_follow_up",
      "driver": "17 representatives promised solutions that never materialized, and the eventual offer was a fee-and-interest-laden wire transfer",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "After talking to 17 different Chase people ( I have names, dates and what was promised ) who each said they would solve our problem", "speaker": "narrative"},
        {"quote": "We feel this was a predatory action built on their employee incompetence and/or Chase 's systems.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase flagged a card as fraud and mailed a replacement home without notice, leaving the customer without card access for a full 35-day trip abroad despite 17 representatives promising to fix it, with the only offered solution being a costly high-interest wire transfer."
}

R['cfpb_14059866'] = {
  "contact_reasons": [
    {"reason": "fees_and_charges", "specific_reason": "monthly $12.00 fees continued to be charged on a dormant account with no activity or service provided", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the monthly fees refunded since there has been no account activity or service to justify them",
  "underlying_driver": "monthly $12.00 fees have continued to reduce the balance of a dormant account with no activity, and only one month's fee was refunded after calling",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "monthly fees on inactive account",
      "issue_statement": "Monthly $12.00 fees have continued to reduce the balance of an account with no activity, and Chase only refunded one month's fee after being contacted.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "unexpected_charge",
      "driver": "monthly $12.00 fees continued on a dormant account with no service provided, and only one month was refunded on request",
      "outcome": "partially_resolved",
      "evidence": [
        {"quote": "there is no service provided and thus the fee should be refunded", "speaker": "narrative"},
        {"quote": "only 1 monthly service of $12.00 being refunded", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "partially_resolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Monthly $12.00 fees continued to reduce the balance of a dormant account with no activity, and Chase refunded only one month's worth after being contacted."
}

R['cfpb_14674354'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a business account was repeatedly locked over a legitimately signed-over third-party check even after a supervisor verified and unlocked it", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "a representative was rude and unprofessional, refused to provide a supervisor's name, and would not confirm who re-locked the account", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support", "branch"],
  "customer_ask": "fix_error",
  "stated_reason": "wants the account unlocked and the funds released after already being verified once",
  "underlying_driver": "a supervisor verified the signed-over checks and unlocked the account, but it was locked again for the same reason two weeks later by someone who would not identify herself, and a rude representative refused to escalate",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "account relocked after prior verification",
      "issue_statement": "A business account was locked over a signed-over check even after a supervisor verified the transfer and unlocked it, only to be relocked two weeks later for the same reason.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "error_not_corrected",
      "driver": "the account was relocked for the same already-verified check, and staff would not identify who did it or provide a supervisor to escalate to",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "The rep identified herself as a supervisor and said she would release the hold and unlock my account which she did showing funds available.", "speaker": "narrative"},
        {"quote": "I am ready to take this to my attorneys", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "rude representative refused escalation",
      "issue_statement": "A representative was blunt and unprofessional, refused to identify the person who re-locked the account, and would not provide a supervisor for escalation.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "staff_attitude_or_competence",
      "driver": "the representative was blunt and unprofessional, told the customer to stop interrupting, and refused to provide a supervisor",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "he started getting blunt and unprofessional saying he didn't have to listen to me and to quit interrupting him and am I ready to listen like I was a child", "speaker": "narrative"},
        {"quote": "I asked for his supervisor he said he can not provide one", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "a branch manager gave her direct number and promised to look into the issue", "category": "helpful_staff", "quote": "spoke with XXXX XXXX  who gave me her direct number and said she would look into this and get back with me today", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A business account was locked over a legitimately signed-over check even after a supervisor verified and unlocked it, only to be relocked two weeks later by an unidentified employee, with a rude representative refusing to escalate."
}

R['cfpb_15314883'] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a $300.00 instant transfer was deducted immediately but marked delayed by the payee's bank, and neither bank will take responsibility for locating it", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants the $300.00 transfer delivered or a clear timeline for resolution",
  "underlying_driver": "Chase confirmed the $300.00 payment was sent but tells the customer to contact the recipient bank, while the recipient bank says it never arrived and points back to Chase",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "instant transfer stuck between two banks",
      "issue_statement": "A $300.00 instant transfer was deducted immediately but never arrived at the recipient's account, with both banks deflecting responsibility and neither providing a timeline.",
      "product": "money_transfer_or_p2p",
      "sentiment": -2,
      "driver_category": "money_held_or_not_returned",
      "driver": "Chase confirms the payment was sent while the recipient bank says it never received it, and neither institution will take ownership of resolving it",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Both institutions are deflecting responsibility, and no one has taken ownership of resolving this issue.", "speaker": "narrative"},
        {"quote": "This is an unacceptable delay for what should be an instant transfer service.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $300.00 instant transfer was deducted immediately but never arrived, with Chase and the recipient bank each deflecting responsibility and neither offering a resolution timeline."
}

R['cfpb_15963962'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a $26000.00 fraud claim was credited then reversed as an overdraft each time a legitimate transaction posted, requiring repeated calls", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the fraud credit to stay and not be reversed into an overdraft every time a real transaction posts",
  "underlying_driver": "each time the $26000.00 fraud credit is issued, a subsequent legitimate transaction triggers Chase to reverse it, turning it into an overdraft charge, requiring the customer to call back repeatedly",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "fraud credit repeatedly reversed into overdraft",
      "issue_statement": "A $26000.00 fraud credit was issued then reversed into an overdraft charge each time a legitimate transaction posted, requiring the customer to keep calling back to fix it.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "the fraud credit is reversed into an overdraft every time a real transaction comes through, and the customer has to keep calling to get it corrected again",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Two days later they gave credit but soon as another transaction with through they took back so making it overdraft charge.", "speaker": "narrative"},
        {"quote": "I believe I'm being singled out for whatever reason.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "A $26000.00 fraud credit keeps being reversed into an overdraft charge every time a legitimate transaction posts, requiring repeated calls to get it fixed again."
}

R['cfpb_16700238'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a warranty replacement phone that was never returned to the customer could not be disputed because Chase's system will not allow disputes past a three-month window", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants Chase to dispute the original purchase since the replacement phone was never received back",
  "underlying_driver": "a months-long manufacturer warranty replacement process ended with the seller never sending the replacement phone, but by the time this was clear, Chase's system could not open a dispute past the three-month window",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "dispute blocked by three-month window",
      "issue_statement": "After a lengthy manufacturer warranty process, the seller never sent back the replacement phone, but Chase's system could not open a dispute because it was past the three-month window.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "the seller kept the replacement phone without sending it back, but Chase's system constraints made it impossible to file any dispute past three months",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "the person told me that they can not even try to file anything, as it is past the 3 month window, no matter what they try to do with a long-term dispute", "speaker": "narrative"},
        {"quote": "It is impossible due to the system 's constraints to even allow for a longer dispute.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "After a months-long manufacturer warranty process ended with the seller never returning a replacement phone, Chase's system could not open a dispute because the original purchase was more than three months old."
}

R['cfpb_17281821'] = {
  "contact_reasons": [
    {"reason": "collections_or_debt", "specific_reason": "representatives keep visiting the customer's home at all hours, including at night, looking for a person who does not live there", "is_primary": True}
  ],
  "products": ["debt_collection"],
  "services": ["branch"],
  "customer_ask": "stop_or_block",
  "stated_reason": "wants Chase to stop sending people to her home looking for someone who does not live there",
  "underlying_driver": "despite repeated emails and in-person statements that the wanted person does not live there, Chase keeps sending representatives, including at night, and texting to sign documents meant for someone else",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "repeated home visits for the wrong person",
      "issue_statement": "Representatives keep coming to the customer's home, including at night, looking for a person who does not live there, despite repeated emails and in-person statements correcting them.",
      "product": "debt_collection",
      "sentiment": -2,
      "driver_category": "error_not_corrected",
      "driver": "despite repeated corrections by email and in person, representatives keep visiting the home, even at night, looking for someone unrelated to the customer",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase Bank continue to send people to my home, wanting a person who does not live in my home.", "speaker": "narrative"},
        {"quote": "They even come to my house at night. I am not opening any doors for them.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Despite repeated corrections by email and in person, Chase representatives keep coming to the customer's home, including at night, looking for a person who does not live there."
}

R['cfpb_18276213'] = {
  "contact_reasons": [
    {"reason": "terms_information_or_communication", "specific_reason": "Chase Travel said it would cancel a hotel reservation and follow up, but later claimed it was never canceled at all", "is_primary": True},
    {"reason": "dispute_or_chargeback", "specific_reason": "a travel insurance claim was denied for lack of proof of cancellation, which could not exist because Chase never processed the cancellation", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "requests reimbursement of about $340.00 for the penalty caused by Chase's failure to process the cancellation",
  "underlying_driver": "Chase Travel promised to cancel the reservation and follow up within hours after a health-related cancellation request, but later said it was never canceled, which also caused the resulting insurance claim to be denied for lack of cancellation proof",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "hotel cancellation never actually processed",
      "issue_statement": "Chase Travel said it would contact the hotel and confirm cancellation within hours, but weeks later claimed the reservation was never canceled at all.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "no_response_or_follow_up",
      "driver": "Chase Travel promised to process the cancellation and follow up within hours, then denied ever canceling it after repeated follow-ups",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "The representative said they would contact the hotel and update me within XXXX hours.", "speaker": "narrative"},
        {"quote": "On XX/XX/XXXX, Chase stated that the cancellation was denied and advised me to file an insurance claim.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "insurance claim denied for proof that could not exist",
      "issue_statement": "The travel insurance claim was denied for lacking proof of cancellation, which could never be produced because Chase Travel never actually processed the cancellation.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "the insurance claim required proof of cancellation that could not exist since Chase never canceled the reservation as promised",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "The claim was denied because the letter did not explicitly restrict travel, and I need a Proof of Cancellation.", "speaker": "narrative"},
        {"quote": "Since nobody at Chase Travel ever cancelled this hotel stay, proof of cancellation doesnt exist.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase Travel promised to process a hotel cancellation after a health emergency but later claimed it was never canceled, which also caused a travel insurance claim to be denied for lacking cancellation proof, leaving the customer seeking a $340.00 penalty reimbursement."
}

R['cfpb_18738820'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a $4500.00 deposit hold was not released on the availability date Chase itself provided, with conflicting information about a partial release", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "requests release of the full or partial funds by a set date and written clarification of the reason for the extended hold",
  "underlying_driver": "Chase told the customer funds would be available on a specific date, but the hold continued past it with representatives giving conflicting answers about whether even a partial release was possible",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "deposit hold past promised availability date",
      "issue_statement": "A $4500.00 check deposit hold was not released on the availability date Chase itself provided, and representatives gave conflicting answers about whether even a partial release was possible.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "Chase continues holding the full $4500.00 past its own stated availability date, with conflicting information on whether a partial release is possible, despite no indicated issue with the check",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I was explicitly told by Chase that the funds would be available on XXXX. That date passed and the funds were not released.", "speaker": "narrative"},
        {"quote": "I was told at XXXX point that a partial release was possible and later told that no release was possible at all.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $4500.00 check deposit hold was not released on the availability date Chase itself provided, and representatives gave conflicting information about whether even a partial release was possible."
}

R['cfpb_20283815'] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "a retroactive change to a transaction's posted date caused denial of an advertised 5 percent quarterly bonus reward on a tax payment", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants the 5 percent bonus reward honored based on the transaction date originally displayed at the time of purchase",
  "underlying_driver": "the issuer initially displayed the transaction with a date that qualified for a 5 percent bonus category, then later changed the posted date, causing the reward to be denied despite documentation of the original date",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "changed transaction date denied bonus reward",
      "issue_statement": "A tax payment transaction date shown at the time of purchase later changed in the issuer's system, causing denial of the advertised 5 percent bonus reward despite screenshots proving the original date.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "the issuer changed the recorded transaction date after the fact, denying the 5 percent bonus reward despite documented proof of the originally displayed date",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "The XXXX tax payment later posted as XX/XX/XXXX and the issuer denied the 5 percent reward.", "speaker": "narrative"},
        {"quote": "The issuer declined to adjust the reward and stated the purchase posted XX/XX/XXXX.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A tax payment's recorded transaction date was later changed in the issuer's system, causing denial of an advertised 5 percent bonus reward despite screenshots proving the originally displayed date."
}

R['cfpb_21388662'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a stolen phone's passcode let someone access a digital wallet and saved bank passwords, resulting in $1600.00 in unauthorized transfers and purchases, and the debit fraud claim was denied", "is_primary": True}
  ],
  "products": ["checking_or_savings", "credit_card"],
  "services": ["mobile_app"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $1600.00 in unauthorized debit transactions refunded",
  "underlying_driver": "a stolen phone's passcode gave access to the digital wallet and saved bank passwords, and although credit cards blocked most attempts, the debit fraud claim covering $1600.00 in losses was denied",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "debit fraud claim denied after phone theft",
      "issue_statement": "After a stolen phone's passcode was used to access a digital wallet and saved passwords, resulting in $1600.00 in unauthorized debit transactions and transfers, the fraud claim was denied.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "a debit fraud claim covering $1600.00 in transactions made using credentials stolen from a phone was denied even after a police report and credit bureau fraud alerts were filed",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I received a letter from Chase that my debit fraud claim was denied and I have now lost $1600.00 so far.", "speaker": "narrative"},
        {"quote": "I have already filed a police report with XXXX XXXX XXXX ( pending case number ) and reported it the identitytheft.gov.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "the credit cards were able to block most of the fraudulent transaction attempts", "category": "fast_resolution", "quote": "My credit cards were able to block most of these transactions", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A stolen phone's passcode was used to access a digital wallet and saved bank passwords, resulting in $1600.00 of unauthorized debit transactions and transfers, and the resulting fraud claim was denied despite a police report and credit freezes."
}

R['cfpb_22632419'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "Chase told the customer to file an identity theft claim so a legitimate account could be opened, then reversed course and said the situation was final and could not be undone", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wants the identity theft claim situation resolved as originally promised so a legitimate account can be opened",
  "underlying_driver": "the identity theft team first told the customer everything was fine and a legitimate account could be opened, then called back saying nothing could be reversed and the decision was final",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "identity theft resolution reversed as final",
      "issue_statement": "Chase's identity theft team first said a legitimate account could be opened after filing a claim, then reversed course, saying the situation was final and nothing could be undone.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "the identity theft team first confirmed the customer was good to open a legitimate account, then called back saying it was final and could not be reversed",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "now theyre saying nothing cant be reversed after I just got off the phone with the identity theft people for chase", "speaker": "narrative"},
        {"quote": "now theyre saying its final after they told me I was good", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase's identity theft team told the customer a legitimate account could be opened after filing a claim, then reversed course and said the decision was final and could not be undone."
}

R['cfpb_23345790'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a $590.00 cash co-payment demanded on top of surrendered airline miles was disputed twice as deceptive, self-contradicting pricing, and denied both times without examining the evidence", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $590.00 charge permanently credited and a written explanation of the specific reason for each denial",
  "underlying_driver": "the airline's own pricing was self-contradicting, since a comparable segment cost far fewer miles and no cash while this one demanded all the miles plus $590.00, and Chase denied the dispute twice without addressing that evidence",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "billing dispute denied without examining evidence",
      "issue_statement": "A $590.00 cash charge on top of surrendered miles for an award flight was disputed as self-contradicting, deceptive pricing, and Chase denied the dispute twice without ever addressing the documented inconsistency.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase denied the $590.00 dispute twice as generic cardholder dissatisfaction without addressing the documented pricing inconsistency, giving no substantive explanation either time",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "JP Morgan Chase has now denied a legitimate billing dispute twice without ever examining the actual substance of my claim, and I am frankly appalled at how this has been handled.", "speaker": "narrative"},
        {"quote": "That is not an investigation ; it is a rubber stamp, and it is unacceptable.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $590.00 cash charge added on top of surrendered airline miles, part of documented self-contradicting pricing by the merchant, was disputed twice and denied both times by Chase without addressing the evidence."
}

R['cfpb_9554112'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "fraudulent in-person chip transactions were first confirmed as fraud and removed, then reversed back onto the account since the card was still in the customer's possession", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the two fraudulent in-person transactions permanently removed from the account",
  "underlying_driver": "Chase first removed two fraudulent transactions after confirming fraud, but then reversed the removal because the transactions used the chip or tap and the customer still had physical possession of the card",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "confirmed fraud charges reinstated after removal",
      "issue_statement": "Two in-person chip transactions totaling $2300.00 were confirmed as fraud and removed, but then reinstated because Chase said card-present transactions couldn't be fraud if the card was still with the customer.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "Chase reinstated two removed fraud charges because they were done with the chip or tap while the card remained in the customer's possession, despite the customer denying making them",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I see those XXXX transaction backed into my account.", "speaker": "narrative"},
        {"quote": "Chase saying since the purchases are done in person charges are reversed.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "Chase initially removed the two fraudulent transactions after the customer reported them", "category": "fast_resolution", "quote": "A day later I checked my online statement and these XXXX transactions were removed.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "Two confirmed fraudulent in-person chip transactions totaling $2300.00 were removed and then reinstated because Chase said card-present charges could not be fraud while the customer still had the card, and the claim is now being reopened."
}

R['cfpb_9835862'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "someone impersonated the customer in a branch, opened a joint account, linked all accounts and transferred large sums out, despite a prior in-branch security safeguard that was not followed", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the transferred money back and stronger in-branch security going forward",
  "underlying_driver": "an oral-password safeguard put in place after a prior identity theft incident was not followed, allowing an impersonator to open a joint account, link all accounts and move large sums in a single day without triggering any fraud alerts",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "in-branch impersonation bypassed prior safeguard",
      "issue_statement": "An impersonator physically opened a joint account at a branch and transferred large sums out of linked accounts, even though a prior oral-password safeguard should have prevented it.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "error_not_corrected",
      "driver": "an oral-password safeguard set up after a prior identity theft was not followed, letting an impersonator open accounts and transfer large sums in-branch in a single day with no fraud alerts triggered",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "The bank said they put additional safeguards on my account, including an oral password needed for any in branch transaction. Apparently the process was not followed.", "speaker": "narrative"},
        {"quote": "I feel like I was physically assaulted. I feel like I was physically violated", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "An impersonator opened a joint account in a branch and transferred large sums out of multiple linked accounts in a single day, even though an oral-password safeguard from a prior identity theft incident should have stopped it, and no fraud alerts were triggered."
}

R['cfpb_10180655'] = {
  "contact_reasons": [
    {"reason": "loan_servicing", "specific_reason": "a Chase representative said paying $130.00 would apply $24000.00 of unapplied funds to fully pay off the mortgage, but the funds were never applied", "is_primary": True}
  ],
  "products": ["mortgage"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wants the mortgage paid off as promised or the unapplied funds returned with interest",
  "underlying_driver": "a Chase representative promised that paying $130.00 would apply $24000.00 in unapplied funds to fully pay off the mortgage, but another party confirmed the funds were never requested to be applied",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "promised mortgage payoff never applied",
      "issue_statement": "A Chase representative said paying $130.00 would apply $24000.00 of unapplied funds to pay off the mortgage in full, but another party confirmed the funds were never actually requested to be applied.",
      "product": "mortgage",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "a Chase representative promised a $130.00 payment would trigger full mortgage payoff from unapplied funds, but the funds were never applied and the mortgage remains unpaid",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "He also stated that once I paid this amount my account would be paid in full, but this did not happen.", "speaker": "narrative"},
        {"quote": "my mortgage is not paid in full nor have my funds been returned with interest", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A Chase representative promised that a $130.00 payment would apply $24000.00 of unapplied funds to fully pay off the mortgage, but the funds were never actually applied, leaving the mortgage unpaid."
}

R['cfpb_10488155'] = {
  "contact_reasons": [
    {"reason": "credit_reporting", "specific_reason": "a JPMCB account was disputed with the credit bureaus and no signed contract or requested information was ever provided to support it", "is_primary": True}
  ],
  "products": ["credit_reporting_service"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants the disputed JPMCB account removed from the credit report so a home purchase for the family can move forward",
  "underlying_driver": "despite multiple dispute attempts, no signed contract or requested documentation supporting the JPMCB account was ever provided, and it continues to hurt the credit needed for a home purchase",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "undocumented account blocking home purchase",
      "issue_statement": "A disputed JPMCB account was never supported with a signed contract or requested documentation, and it continues to hurt the credit needed to buy a home for the family.",
      "product": "credit_reporting_service",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "no signed contract or requested documentation for the disputed JPMCB account was ever provided across multiple dispute attempts, yet it remains on the credit report",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I have disputed JPMCB with the credit bureaus and I didnt receive any informations or contracts from signed as requested", "speaker": "narrative"},
        {"quote": "i am trying to buy a house for my XXXX kids and wife and this hurts my credit so bad", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "A disputed JPMCB account was never supported with a signed contract or requested documentation across multiple attempts, and it continues to damage the credit needed to buy a home for the family."
}

R['cfpb_10911703'] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "a $900.00 new-account bonus was not paid after meeting the terms because Chase could not locate the coupon code linked to the account", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $900.00 promotional bonus paid after satisfying all its terms",
  "underlying_driver": "the coupon code was provided to a representative and validated when the accounts were opened, but Chase now refuses to pay the bonus because it cannot locate that code linked to the account",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "promo bonus unpaid over lost coupon code",
      "issue_statement": "A $900.00 new-account bonus was not paid after 90 days of meeting all the terms, because Chase says it cannot locate the coupon code that was validated when the accounts were opened.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "the coupon code was provided and validated at account opening, but Chase now refuses to pay the $900.00 bonus because it cannot locate that code on its end",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "After not seeing the bonus hit my account after 90 days - i contacted Chase and they are refusing to pay due to unable to locate the coupon code linked to my account", "speaker": "narrative"},
        {"quote": "provided the coupon code to the rep helping me open accounts to validate that i would qualify for the $900.00 in bonus", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $900.00 new-account bonus was not paid despite the customer meeting all the terms, because Chase says it cannot locate the coupon code that was validated when the accounts were opened."
}

R['cfpb_11211172'] = {
  "contact_reasons": [
    {"reason": "fees_and_charges", "specific_reason": "no payment due reminders are sent, resulting in a $40.00 late fee, which the customer believes is intentional to collect fees", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants Chase to send payment due reminders to avoid late fees",
  "underlying_driver": "the customer receives no reminder on the day payment is due, resulting in a $40.00 fee the next day, which they believe is a deliberate way for Chase to collect fees",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "no payment reminders leading to late fee",
      "issue_statement": "No reminder is sent on the day a payment is due, resulting in a $40.00 late fee the following day, which the customer believes is intentional.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "unexpected_charge",
      "driver": "no payment due reminder is sent, resulting in a $40.00 fee the next day, which the customer believes is a deliberate way to collect fees",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I do not receive any reminders on the day my payment is due.", "speaker": "narrative"},
        {"quote": "Chase does not send payment reminders in order to collect fees.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "No reminder is sent on the day a credit card payment is due, resulting in a $40.00 late fee, which the customer believes is a deliberate tactic by Chase to collect fees."
}

# ---- verification ----
missing = set(texts) - set(R)
extra = set(R) - set(texts)
print("missing:", missing)
print("extra:", extra)

errors = []
for cid, resp in R.items():
    text = texts[cid]
    for t in resp["topics"]:
        for ev in t["evidence"]:
            if ev["quote"] not in text:
                errors.append((cid, "topic_evidence", ev["quote"]))
            if not (8 <= len(ev["quote"]) <= 300):
                errors.append((cid, "topic_evidence_len", ev["quote"]))
    for pm in resp["positive_moments"]:
        if pm["quote"] not in text:
            errors.append((cid, "pm_evidence", pm["quote"]))
        if not (8 <= len(pm["quote"]) <= 300):
            errors.append((cid, "pm_evidence_len", pm["quote"]))
    if not (1 <= len(resp["contact_reasons"]) <= 3):
        errors.append((cid, "contact_reasons_count", len(resp["contact_reasons"])))
    if sum(1 for cr in resp["contact_reasons"] if cr["is_primary"]) != 1:
        errors.append((cid, "primary_count", cid))
    if not (1 <= len(resp["topics"]) <= 5):
        errors.append((cid, "topics_count", len(resp["topics"])))
    if not (1 <= len(resp["products"]) <= 3):
        errors.append((cid, "products_count", len(resp["products"])))
    if not (0 <= len(resp["services"]) <= 3):
        errors.append((cid, "services_count", len(resp["services"])))
    if not (0 <= len(resp["positive_moments"]) <= 3):
        errors.append((cid, "pm_count", len(resp["positive_moments"])))
    if len(resp["summary"]) > 400:
        errors.append((cid, "summary_len", len(resp["summary"])))
    for t in resp["topics"]:
        if len(t["issue_statement"]) > 220:
            errors.append((cid, "issue_statement_len", len(t["issue_statement"])))
        if len(t["driver"]) > 200:
            errors.append((cid, "driver_len", len(t["driver"])))
        if not (1 <= len(t["evidence"]) <= 3):
            errors.append((cid, "evidence_count", len(t["evidence"])))

if errors:
    print("ERRORS:")
    for e in errors:
        print(e)
else:
    print("ALL OK")

out = pathlib.Path("data/cache/extract")
if not errors:
    for cid, resp in R.items():
        obj = {"key": keys[cid], "prompt_version": "ext-1.0", "schema_version": "1",
               "taxonomy_version": "1", "call_id": cid, "model": "claude-agent-build",
               "produced_by": "claude_agent", "created_at": "2026-09-11T12:00:00Z",
               "usage": None, "response": resp}
        (out / f"{cid}.json").write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
    print("wrote", len(R))
