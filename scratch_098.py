import json, pathlib

bundle = json.load(open('data/work/extract_bundles/bundle_098.json', encoding='utf-8'))
texts = {r['call_id']: r['text'] for r in bundle['records']}
keys = {r['call_id']: r['cache_key'] for r in bundle['records']}

R = {}

R['cfpb_10173757'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a $3500.00 billboard advertising charge was disputed twice and denied both times although the merchant never delivered a signed contract or the promised services", "is_primary": True},
    {"reason": "unauthorized_or_fraud", "specific_reason": "the merchant sent falsified documents bearing the husband's forged initials and signature, and images claiming he was involved in a project he never participated in", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $3500.00 charge refunded since the billboard services were never delivered as agreed",
  "underlying_driver": "the merchant repeatedly promised a refund that never came, then submitted forged documents with the husband's fabricated signature and unrelated billboard images to fight the dispute, which the credit card company accepted",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "billboard charge disputed twice and denied",
      "issue_statement": "A $3500.00 billboard advertising charge was disputed twice, but Chase denied both disputes based on the merchant's false documentation despite no signed contract ever existing.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "the merchant's contract was voided and inaccessible, yet Chase denied the dispute based on the merchant's own unsupported claims of valid service",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I have opened a dispute with Chase Business Credit Card twice now and been denied both times.", "speaker": "narrative"},
        {"quote": "they then sent new billboard images with my name and company", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "forged signature used to fight the dispute",
      "issue_statement": "The merchant submitted documents with the customer's husband's forged initials and signature, and images falsely depicting him as involved in a project he never took part in.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "forged initials and signature of the husband, who was never part of the conversation, were used on documents the merchant submitted to fight the dispute",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "they have my husbands initials and signature were on the form and he was never even involved in this conversation or phone call", "speaker": "narrative"},
        {"quote": "His initials and signatures have been forged.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $3500.00 billboard advertising charge for undelivered services was disputed twice and denied both times after the merchant submitted forged signatures and false documents, which Chase accepted over the customer's evidence."
}

R['cfpb_10485929'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a $180.00 ATM withdrawal the customer says she never made was ruled authorized because the correct card and code were used", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["atm", "branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $180.00 withdrawal refunded since she was not at the ATM",
  "underlying_driver": "Chase concluded the withdrawal was authorized solely because the card chip and code were used, despite the customer having sole possession of the card and witnesses placing her 20 miles away at the time",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "atm withdrawal ruled authorized despite alibi",
      "issue_statement": "A $180.00 ATM withdrawal was ruled authorized because the correct card and code were used, even though the customer has sole possession of her card and witnesses confirming she was 20 miles away at the time.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "the investigation relied solely on correct chip and code use, without reviewing ATM footage the branch manager admitted he could not access himself",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "It was declared by them that whoever was at the ATM had my card and code information and so I must have given them the authorization to use my card.", "speaker": "narrative"},
        {"quote": "I informed that I have witnesses that will verify I was home 20 miles away when the ATM was accessed.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $180.00 ATM withdrawal was ruled authorized based solely on correct chip and code use, despite the customer's sole possession of her card and witnesses placing her 20 miles away at the time."
}

R['cfpb_10909894'] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "funds sent to the wrong account were located at JPMorgan Chase, but Chase denied the sending bank's recall request and will not process reimbursement", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "demands JPMorgan Chase return the funds since their location is confirmed",
  "underlying_driver": "the sending bank located the misdirected funds at JPMorgan Chase and confirmed it has done everything required, but Chase denied the recall request and redirects the customer back to the sending bank instead of processing reimbursement",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "recall denied despite confirmed fund location",
      "issue_statement": "The sending bank located misdirected funds at JPMorgan Chase and confirmed it met every requirement, but Chase denied the recall request and refuses to process reimbursement.",
      "product": "money_transfer_or_p2p",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "Chase denied the recall request and redirects the customer back to the sending bank even though the funds' location is no longer in question",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "the recall request was denied", "speaker": "narrative"},
        {"quote": "JP Morgan Chase Bank has the funds but is refusing to process the reimbursement", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A misdirected transfer was traced to JPMorgan Chase, which denied the sending bank's recall request and refuses to process reimbursement even though the funds' location is confirmed."
}

R['cfpb_11203222'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "two mailed checks were stolen, had their payee altered, and were cashed by Chase, which now claims one check bears a forged signature that is actually the customer's own", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants Chase to reimburse the remaining $3900.00 check the same way it already reimbursed the $2400.00 check",
  "underlying_driver": "Chase cashed two stolen checks with altered payees, reimbursed one, but claims the customer's own signature on the second is forged when only the payee line was actually altered",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "altered-payee check reimbursement denied",
      "issue_statement": "Chase reimbursed a $2400.00 stolen and altered check but denies reimbursing a $3900.00 one, claiming the signature is forged when the payee, not the signature, was what was altered.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase reimbursed one altered check but is denying the second, incorrectly claiming the customer's own signature is forged rather than the altered payee",
      "outcome": "partially_resolved",
      "evidence": [
        {"quote": "Chase is now saying the check for $3900.00 has my forged signature when it is clear from both checks that my signature is identical.", "speaker": "narrative"},
        {"quote": "It is the Payee that was altered, not my signature", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "partially_resolved",
  "positive_moments": [
    {"what": "Chase already reimbursed the $2400.00 check after repeated requests", "category": "fair_outcome", "quote": "Finally, they received reimbursement for the $2400.00 check.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "Chase reimbursed one of two stolen, altered-payee checks but is denying the second, incorrectly claiming the customer's own matching signature is forged rather than the altered payee line."
}

R['cfpb_11520804'] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a $2100.00 final paycheck deposited at an ATM was rejected due to an ATM error and the funds were removed from the account", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "requests for a photo of the rejected check were never fulfilled despite being confirmed available", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["atm", "phone_support", "branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "needs the final paycheck funds restored since she will not be paid again for nearly a month",
  "underlying_driver": "an ATM error caused a $2100.00 final paycheck deposit to be rejected and removed from the account, and Chase would not provide the check image or any option besides waiting over a week or getting the issuer to reissue it",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "final paycheck deposit rejected by faulty atm",
      "issue_statement": "A $2100.00 final paycheck deposited at an ATM was rejected due to a confirmed ATM error, and the funds were removed from the account, leaving only a 7-10 day wait or reissue as options.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "system_or_app_failure",
      "driver": "an ATM error rejected a $2100.00 final paycheck deposit and removed the funds, with only a slow replacement-check process offered as a fix",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I discovered the check for $2100.00 was rejected altogether and the funds were removed from my account.", "speaker": "narrative"},
        {"quote": "they informed me they have it and confirmed that it was an error with the ATM to begin with", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A faulty ATM rejected a $2100.00 final paycheck deposit and removed the funds, leaving the customer only the option of a 7-10 day wait or a reissued check, despite urgently needing the money for rent."
}

R['cfpb_12126201'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a $730.00 hotel charge for a misrepresented, unsafe and still-under-construction property was disputed under the Fair Credit Billing Act and denied because the guest stayed the entire time", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants a full refund of the $730.00 booking since the hotel was not as advertised and unsafe",
  "underlying_driver": "Chase denied the dispute solely because the customer stayed the whole time, without accounting for having no reasonable alternative after discovering unsafe, misrepresented conditions post check-in",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "misrepresented hotel dispute denied",
      "issue_statement": "A $730.00 hotel booking turned out to be an unsafe, under-construction property lacking promised amenities, and Chase denied the FCBA dispute solely because the guest stayed the entire booked period.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase denied the dispute because the stay was completed, without considering there was no safe alternative after check-in revealed unsafe, unadvertised conditions",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase declined the dispute, stating that I stayed the entire time and therefore received services.", "speaker": "narrative"},
        {"quote": "I had already paid for my stay, and the hotels unsafe, misrepresented conditions were only discovered after check-in.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $730.00 hotel booking turned out to be an unsafe, under-construction property, and Chase denied the Fair Credit Billing Act dispute solely because the guest completed the stay, with no safe alternative available after check-in."
}

R['cfpb_12523442'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a $3000.00 property payment made through Chase after a prior payment pause was rejected, and the building company refuses to return it while closing the account", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the recent $3000.00 payment returned since the company will not continue the contract",
  "underlying_driver": "after honoring a payment pause and resuming with a $3000.00 payment, the building company said it would close the account and keep the money, and Chase did not help even after documents were sent",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "recent payment kept after account closure",
      "issue_statement": "After resuming payments with $3000.00 following an agreed pause, the building company said it would close the account and not honor or return that payment, and Chase did not help resolve it.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "a $3000.00 payment made after an agreed pause was kept by the company when it closed the account, and Chase provided little help despite submitted documentation",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "we received a letter stating that they will be closing our account and will not honor the payment we made", "speaker": "narrative"},
        {"quote": "Chase didnt really help even if I sent the documents.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $3000.00 property payment made after an agreed pause was kept by the building company when it closed the account, and Chase did little to help recover the money despite submitted documentation."
}

R['cfpb_13027719'] = {
  "contact_reasons": [
    {"reason": "balance_or_statement_error", "specific_reason": "a $140.00 pending refund credit shown as available balance disappeared the next day, leaving the account negative after it was relied on for a purchase", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants the account balance corrected since a purchase was made relying on the displayed pending refund",
  "underlying_driver": "a $140.00 merchant refund appeared as a pending credit and was used to justify a new purchase, but it was never finalized, leaving the account negative",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "pending refund vanished after being relied on",
      "issue_statement": "A $140.00 pending refund credit was shown as part of the available balance, but disappeared the next day without posting, leaving the account negative after a purchase was made relying on it.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "the account displayed a $140.00 pending refund as available, but Chase says pending transactions are not guaranteed and the refund was never posted",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "the next day the pending refund disappeared and was never finalized. My account then went negative by $140.00.", "speaker": "narrative"},
        {"quote": "I made the second purchase based on what Chase displayed as available funds.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $140.00 merchant refund displayed as available balance vanished the next day without posting, leaving the account negative after the customer relied on it to make another purchase."
}

R['cfpb_13560062'] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "an international payment blocked under sanctions rules remains stuck even after a license authorizing JPMorgan Chase to return the funds was obtained", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants the funds returned now that a license authorizing the return has been obtained",
  "underlying_driver": "a payment for imported goods was blocked under sanctions rules, and even after obtaining a license authorizing JPMorgan Chase to return the funds, the release was rejected and Chase has not responded to follow-up contact",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "sanctions-blocked payment stuck despite license",
      "issue_statement": "A payment for imported goods was blocked under sanctions rules, and even after obtaining a license authorizing the funds' return, the release was rejected and JPMorgan Chase has not responded.",
      "product": "money_transfer_or_p2p",
      "sentiment": -1,
      "driver_category": "no_response_or_follow_up",
      "driver": "a license authorizing return of the blocked funds was obtained and the transfer was released, but it was rejected and Chase never responded to follow-up outreach",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Transfer was releasedbank under XXXX license no. XXXX XXXX XXXXXXXX but was rejected by the XXXX XXXX", "speaker": "narrative"},
        {"quote": "JP Morgan Chase Bank did not respond. So, I can not get my money, even with a license that allows it", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "A sanctions-blocked international payment remained stuck even after obtaining a license authorizing JPMorgan Chase to return the funds, and Chase has not responded to follow-up requests."
}

R['cfpb_14058302'] = {
  "contact_reasons": [
    {"reason": "fees_and_charges", "specific_reason": "a savings account was changed to a fee-charging checking account without consent, resulting in over $880.00 in fees over several years", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "a representative was dismissive about the unauthorized account change and refused to escalate to a manager or provide documentation", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch", "phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the original account terms restored and all resulting fees reimbursed",
  "underlying_driver": "Chase changed a no-fee savings account into a fee-charging checking account without notice after a bank acquisition, and only partial fee refunds were given after the customer had to push for them",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "account type changed without consent, generating fees",
      "issue_statement": "A no-fee savings account was silently converted to a fee-charging checking account after a bank acquisition, generating over $880.00 in fees, of which only 17 months were eventually refunded.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "unexpected_charge",
      "driver": "the account type was changed without notice, generating over $880.00 in fees during a period of unemployment, with only partial fees refunded so far",
      "outcome": "partially_resolved",
      "evidence": [
        {"quote": "Chase changed my account types between XXXX and XXXX of XXXX, transitioning my savings account into a checking account which carries monthly fees", "speaker": "narrative"},
        {"quote": "I was charged over $880.00 in fees over the years", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "dismissive follow-up refused documentation",
      "issue_statement": "A phone representative added some fee compensation but was dismissive about the unauthorized account change, refused to provide documentation of any notice, and denied escalation to a manager.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "staff_attitude_or_competence",
      "driver": "the representative was dismissive, told the customer to get proof of notice at the branch instead of providing it, and refused to escalate to a manager",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "he was dismissive and made no effort to address the core issuethat my account was changed without my knowledge or consent", "speaker": "narrative"},
        {"quote": "I asked to speak with a manager but was refused a proper escalation path.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "partially_resolved",
  "positive_moments": [
    {"what": "a branch representative reviewed the account history, acknowledged the issue, and secured a refund of 5 months of fees", "category": "helpful_staff", "quote": "He reviewed my account history and acknowledged the issue.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A no-fee savings account was silently converted to a fee-charging checking account after a bank acquisition, generating over $880.00 in fees, and while a branch representative secured a partial refund, a later phone representative was dismissive and refused escalation or documentation."
}

R['cfpb_14662610'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "six unauthorized electronic withdrawals totaling $26000.00 by an unknown merchant were reported in time but denied without proof of authorization", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting reimbursement of the $26000.00 in unauthorized transactions as required under the Electronic Fund Transfer Act",
  "underlying_driver": "Chase denied the fraud claim saying the transactions processed correctly, without providing valid proof of authorization despite a timely report",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "unauthorized withdrawals denied without proof",
      "issue_statement": "Six unauthorized electronic withdrawals totaling $26000.00 by an unrecognized merchant were denied by Chase, which stated the transactions processed correctly without providing proof of authorization.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase denied a timely-reported $26000.00 fraud claim citing correct processing, without producing any valid proof of authorization",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase denied my claim, stating that the transactions were processed correctly, without providing any valid proof of authorization", "speaker": "narrative"},
        {"quote": "I never authorized any transaction, transfer, or business relationship with XXXX.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Six unauthorized electronic withdrawals totaling $26000.00 to an unrecognized merchant were denied by Chase, which cited correct processing without providing any proof of authorization."
}

R['cfpb_15312656'] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "a sign-up bonus was denied despite meeting the eligibility terms stated on Chase's own offer page, which staff said was simply incorrect", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wants an exception to receive the sign-up bonus since the denial is based on Chase's own incorrect website information",
  "underlying_driver": "Chase's Offer Details page said the bonus was available under the customer's exact circumstances, but a representative and supervisor said the website was wrong and refused to make an exception",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "bonus denied despite meeting stated website terms",
      "issue_statement": "A sign-up bonus was denied even though the customer met every eligibility condition listed on Chase's own Offer Details page, which staff admitted was simply incorrect.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "Chase's own published offer terms said the bonus applied, but staff said the website was wrong and refused an exception for their own error",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I am being simply told that the Offer Details information on their website is incorrect", "speaker": "narrative"},
        {"quote": "I asked for review for exception in this case as the incorrect information in the Offer Details page is at their fault but they refused.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A credit card sign-up bonus was denied even though the customer met every eligibility condition on Chase's own offer page, which staff admitted was wrong, and Chase refused to make an exception for its own error."
}

R['cfpb_15963003'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a $1600.00 dispute over undelivered merchandise was denied without provisional credit, documentation, or a substantive explanation", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants Chase to credit the $1600.00 for merchandise that was never delivered",
  "underlying_driver": "the merchant confirmed it would not help further, and Chase denied the billing-error dispute without issuing provisional credit or explaining the denial, leaving the customer with neither the goods nor the money",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "undelivered merchandise dispute denied without explanation",
      "issue_statement": "A $1600.00 dispute for merchandise that was never delivered was denied by Chase without provisional credit, supporting documentation, or a substantive explanation for the closure.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase closed the billing-error dispute with only a statement that it was resolved, providing no documentation, provisional credit, or explanation",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase denied my claim ( Claim # XXXX ) without issuing provisional credit and without providing any documentation or evidence supporting its denial.", "speaker": "narrative"},
        {"quote": "Chase left me with neither my merchandise nor my money, forcing me into a stalemate", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $1600.00 dispute over undelivered merchandise was denied by Chase without provisional credit, documentation, or explanation, leaving the customer with neither the goods nor the money."
}

R['cfpb_16698345'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a verified check deposit has been held for about a year, with Chase repeatedly re-verifying the already-confirmed check maker and giving no updates", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the held balance released since the check has already been verified",
  "underlying_driver": "Chase's fraud department keeps re-verifying an already-confirmed check maker on every call for about a year without releasing the funds or providing updates",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "year-long hold despite verified check",
      "issue_statement": "A checked deposit has been held for about a year even though the check maker has already been verified, and every call requires re-verifying the same information with no updates.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "the fraud department re-verifies the already-confirmed check maker on every call and provides no further update after about a year",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "every time I call Chase bank want to verify again", "speaker": "narrative"},
        {"quote": "its been a year they dont call and no further update", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "A verified check deposit has been held for about a year, with the fraud department re-verifying the already-confirmed check maker on every call and giving no further updates."
}

R['cfpb_17268363'] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "a checking account holding over $1,000,000 in legitimate stock-sale proceeds was closed for fraud concerns with no explanation", "is_primary": True},
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "promised return of the full balance within days has stretched to a month with conflicting status updates", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support", "branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "requests the full balance be returned as soon as possible",
  "underlying_driver": "Chase closed the account over unexplained fraud concerns and promised the funds back within days, but a month later the customer still has not received them and gets conflicting updates each time",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "account closed over unexplained fraud concerns",
      "issue_statement": "Chase closed a checking account holding over $1,000,000 in legitimate stock-sale proceeds, citing fraud concerns, without giving any explanation.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "the account was closed for fraud concerns with no explanation given despite the funds representing legitimate stock-sale proceeds",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I was informed by Chasewithout any explanationthat my checking account would be closed due to fraud concerns.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "promised return delayed a month with conflicting updates",
      "issue_statement": "Multiple representatives promised the full balance would be returned within days, but a month later it has not arrived, and each call brings conflicting information about its status.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "representatives promised return of the funds within days, but a month later they remain unreturned with conflicting status information each time",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I was told by multiple Chase representatives, both in person and over the phone, that the funds would be returned to me within XXXX business days.", "speaker": "narrative"},
        {"quote": "Each time I contact Chase customer support, I am given conflicting information about the status of the return of my money.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase closed an account holding over $1,000,000 in legitimate stock-sale proceeds over unexplained fraud concerns, and a promised return of the funds within days has stretched to a month with conflicting status updates."
}

R['cfpb_18275247'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "four ATM withdrawals totaling $1600.00 made after the customer was drugged and robbed abroad were denied solely because the correct PIN was used", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["atm"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "requests reversal of the $1600.00 in withdrawals made while incapacitated and robbed",
  "underlying_driver": "Chase treats correct PIN usage as proof of authorization regardless of coercion or incapacitation, even though other transactions from the same incident were already ruled in the customer's favor",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "fraud denied over correct pin despite robbery",
      "issue_statement": "Four ATM withdrawals totaling $1600.00 made while the customer was drugged, robbed and unconscious abroad were denied reversal solely because the correct PIN was used.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase policy treats correct PIN use as dispositive of authorization and does not account for coercion, incapacitation or criminal extraction of the PIN",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "XXXX XXXX stated that Chase policy treats correct PIN usage as dispositive and does not consider such transactions unauthorized.", "speaker": "narrative"},
        {"quote": "I regained consciousness the following morning and did not have possession of my debit card or phone when the disputed ATM withdrawals occurred.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "partially_resolved",
  "positive_moments": [
    {"what": "Chase ruled other disputed transactions from the same incident in the customer's favor", "category": "fair_outcome", "quote": "Chase initially issued provisional credit.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "Four ATM withdrawals made while the customer was drugged and robbed abroad were denied reversal solely because the correct PIN was used, even though other disputed transactions from the same incident were ruled in her favor."
}

R['cfpb_18737447'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "several fraudulent checks were flagged and the account was closed, but conflicting statements followed about a balance being paid off by an unknown party", "is_primary": True},
    {"reason": "fees_and_charges", "specific_reason": "a $34.00 charge posted to the account after it was closed, with no explanation of how a closed account could generate new charges", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support", "branch"],
  "customer_ask": "explanation",
  "stated_reason": "wants a written explanation of how the closed account was paid off and why the closure letter cannot be reproduced",
  "underlying_driver": "after the account was closed following fraud, Chase gave contradictory statements about who paid off the remaining balance and could not explain a new $34.00 charge on a closed account or reproduce the original closure letter",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "closed account paid off by unexplained party",
      "issue_statement": "After closing the account due to fraudulent checks, Chase cannot reproduce the original closure letter and gives contradictory explanations for how the account balance was later paid off by an unknown party.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "Chase gave contradictory statements about the account address, the closure letter, and who paid the balance, without a consistent explanation",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase has refused or failed to explain how a closed account could receive a payment, who made the payment, or why the closure letter can not be reproduced.", "speaker": "narrative"},
        {"quote": "Chase representatives provided multiple contradictory statements", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "unexplained charge on closed account",
      "issue_statement": "A $34.00 charge posted to the account after it was already closed, with no explanation of how a closed account could generate new charges.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "unexpected_charge",
      "driver": "a $34.00 charge appeared on a closed account with no explanation given despite repeated requests",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase also posted additional charges, including $34.00, to the closed account.", "speaker": "narrative"},
        {"quote": "No explanation for the $34.00 charge", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "After closing an account over fraudulent checks, Chase gave contradictory explanations for how the balance was later paid off, could not reproduce the closure letter, and could not explain a new $34.00 charge on the closed account."
}

R['cfpb_20283503'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a Washington Mutual credit card the customer never opened was fraudulently opened in their name and is now the subject of a collections lawsuit and wage garnishment", "is_primary": True},
    {"reason": "collections_or_debt", "specific_reason": "a debt collector sued over the fraudulent account and garnished the bank account without the customer ever receiving prior notice", "is_primary": False}
  ],
  "products": ["debt_collection", "credit_card"],
  "services": [],
  "customer_ask": "stop_or_block",
  "stated_reason": "only just learned of the case after the bank account was already garnished for a debt from an account never opened",
  "underlying_driver": "a Washington Mutual credit card was fraudulently opened in the customer's name years ago, and a lawsuit and garnishment proceeded with no documents ever reaching the customer beforehand",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "garnished over a fraudulently opened account",
      "issue_statement": "A Washington Mutual credit card fraudulently opened in the customer's name led to a collections lawsuit and bank account garnishment, with no prior notice ever received.",
      "product": "debt_collection",
      "sentiment": -2,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "the bank account was garnished for a fraudulently opened account the customer never had, and no documents about the case were ever received beforehand",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "COMITTED FRAUD IN OPENING SAID ACCOUNT IN MY NAME AND NOW XXXX XXXX IS GOING AFTER ME", "speaker": "narrative"},
        {"quote": "I NEVER RECIEVED ANY DOCUMENTS ON THIS MATTER TILL NOW AFTER MY BANK ACCOUNT WAS GARNISHED", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "A Washington Mutual credit card fraudulently opened in the customer's name led to a collections lawsuit and bank account garnishment, with the customer only learning of the case after the money was already taken."
}

R['cfpb_21385270'] = {
  "contact_reasons": [
    {"reason": "loan_servicing", "specific_reason": "a mortgage loan assumption application by a confirmed successor in interest has dragged on for about nine months with shifting, factually incorrect denial reasons", "is_primary": True}
  ],
  "products": ["mortgage"],
  "services": [],
  "customer_ask": "explanation",
  "stated_reason": "wants a clear, accurate written decision on the loan assumption application and, if denied, a specific accurate explanation",
  "underlying_driver": "despite being a confirmed successor in interest and repeatedly submitting every requested document, Chase issued denials based on factually incorrect information and has now gone silent past its own promised deadline for a valid reason",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "loan assumption stalled with shifting denial reasons",
      "issue_statement": "A mortgage loan assumption application by a confirmed successor in interest has dragged on for nine months, with Chase issuing denials based on factually incorrect information each resubmission.",
      "product": "mortgage",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "Chase repeatedly issued denials based on factually incorrect reasons despite full document compliance, and has now missed its own three-day promise to provide a valid reason",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase has issued denials based on information that was factually incorrect.", "speaker": "narrative"},
        {"quote": "I was informed that Chase would need more time to find a reason.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A financially well-qualified mortgage loan assumption application by a confirmed successor in interest has dragged on for about nine months, with Chase repeatedly issuing denials based on factually incorrect reasons."
}

R['cfpb_22629768'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "roughly $5200.00 in a savings account has been on an unexplained hold for over two years, with Chase saying it cannot determine the hold's nature due to the passage of time", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support", "branch"],
  "customer_ask": "explanation",
  "stated_reason": "wants to know what the hold is for and what is required to release it",
  "underlying_driver": "a hold placed shortly after the account was opened has continued for over two years with no reason given, and Chase says it cannot determine the hold's nature despite it being actively displayed in its current systems",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "unexplained multi-year hold blocking closure",
      "issue_statement": "About $5200.00 has been on an unexplained hold for over two years, currently shown in Chase's online portal as active until a set date, and it also prevents the account from being closed.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "money_held_or_not_returned",
      "driver": "Chase says it cannot determine the hold's nature due to the passage of time, even though the hold is presently displayed and active in its own current systems",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase is unable to determine the nature of the hold due to the passage of time.", "speaker": "narrative"},
        {"quote": "I am also filing parallel complaints with the Office of the Comptroller of the Currency and the New York Attorney General 's Office.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "About $5200.00 has sat under an unexplained hold in an active Chase savings account for over two years, blocking closure, and after exhausting phone, branch and executive-office contacts, the customer is filing parallel complaints with the OCC and the New York Attorney General."
}

R['cfpb_23345107'] = {
  "contact_reasons": [
    {"reason": "terms_information_or_communication", "specific_reason": "two branch visits were told that downgrading a credit card or modifying a Pay Over Time loan can only be done by phone, and one visit was refused a banker before even being asked for identification", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": ["branch"],
  "customer_ask": "information_or_status",
  "stated_reason": "asked whether a credit card can be downgraded and a Pay Over Time loan modified in branch",
  "underlying_driver": "branch staff said card downgrades and loan modifications require phone-only disclosures, and one branch declined to let the customer speak to a banker at all, raising concern about whether an aging parent could manage this alone",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "branch cannot process card downgrade or loan changes",
      "issue_statement": "Two Chase branches said credit card downgrades and Pay Over Time loan modifications can only be handled by phone, and one branch declined to let the customer speak to a banker at all.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "policy_or_terms_change",
      "driver": "branch staff say required disclosures for downgrading a card or modifying a loan can only be read over the phone, not in person",
      "outcome": "unknown",
      "evidence": [
        {"quote": "at Chase bank branch locations bankers were not authorized to downgrade or cancel credit cards because the disclosures could only be read over the phone", "speaker": "narrative"},
        {"quote": "I was also denied the opportunity to speak to a banker.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unknown",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Two Chase branches said credit card downgrades and Pay Over Time loan modifications require a phone call and cannot be handled in person, raising concern about whether an aging parent could manage the process alone."
}

R['cfpb_9554111'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a fake ticket seller on social media took a $200.00 Zelle payment and disappeared, and Chase said it could not help since the customer sent the money herself", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants help recovering the $200.00 sent to a scammer impersonating a ticket seller",
  "underlying_driver": "a person impersonating a ticket seller who does not actually exist took a $200.00 Zelle payment and vanished, and Chase said it could not help because the transfer was self-initiated",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "impersonation scam payment not covered",
      "issue_statement": "A fake ticket seller impersonating someone who does not exist took a $200.00 Zelle payment and disappeared, and Chase said it could not help since the customer sent the money herself.",
      "product": "money_transfer_or_p2p",
      "sentiment": -1,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "Chase declined to help recover a $200.00 payment sent to a scammer, citing that the transfer was self-initiated",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I contacted my bank Chase and they said they couldnt help because I sent the money myself.", "speaker": "narrative"},
        {"quote": "this was a fake person impersonating someone on XXXX that doesnt exist, and I was scammed out of my money", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A fake ticket seller impersonating a nonexistent person took a $200.00 Zelle payment and disappeared, and Chase declined to help since the transfer was self-initiated."
}

R['cfpb_9835043'] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "closing deceased parents' joint accounts and disbursing the funds has dragged on for over two months despite submitting every requested document", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "the case has been passed between the branch, back office and legal department with no resolution or proactive updates", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch"],
  "customer_ask": "close_or_cancel",
  "stated_reason": "wants the deceased parents' accounts closed and the funds disbursed after submitting all required documents",
  "underlying_driver": "documents required to close the accounts and disburse funds were submitted months ago, but the branch, back office and legal department keep passing the case between each other with no resolution",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "account closure stalled between departments",
      "issue_statement": "Closing deceased parents' joint accounts and disbursing the funds has stalled for over two months after all documents were submitted, with the branch, back office and legal department passing the case around.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "no_response_or_follow_up",
      "driver": "the required document was delivered over two months ago, but the branch, back office and legal department keep saying they are waiting on each other with no resolution",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "We are just the middle man between the back office and the legal department and youand we are still waiting for a response from the back office or legal.", "speaker": "narrative"},
        {"quote": "As of XX/XX/year> I had received no communication at all from Chase Bank.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Closing deceased parents' joint accounts and disbursing the funds has stalled for over two months after all required documents were submitted, with the branch, back office and legal department each pointing to the other."
}

R['cfpb_10178540'] = {
  "contact_reasons": [
    {"reason": "other_or_unclear", "specific_reason": "a formal notice opting out of all authorizations previously given to JPMCB Card, with no specific incident described", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "other",
  "stated_reason": "formally opting out of any authorizations previously given, citing the Fair Credit Reporting Act",
  "underlying_driver": "no specific incident or dispute is described; the text is a formal legal notice revoking any prior authorizations",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "formal opt-out notice to card issuer",
      "issue_statement": "The customer sent JPMCB Card a formal notice opting out of any and all prior authorizations, citing federal consumer protection law, without describing a specific incident.",
      "product": "credit_card",
      "sentiment": 0,
      "driver_category": "other_or_unclear",
      "driver": "no specific incident is described; the notice is a general legal opt-out of prior authorizations",
      "outcome": "unknown",
      "evidence": [
        {"quote": "I am now opting out of any and all authorizations that I may have given you written, unwritten, oral, verbal or nonverbal", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": 0,
  "resolution_status": "unknown",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "A formal notice was sent to JPMCB Card opting out of any and all prior authorizations under federal consumer protection law, without describing any specific incident."
}

R['cfpb_10488135'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "roughly $2600.00 from two employer checks has been held with no valid reason given, and Chase refuses alternative verification or to return the checks", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants access to the roughly $2600.00 held from two employer checks",
  "underlying_driver": "Chase insists on reaching a phone number that only goes to voicemail for verification, refuses HR's offer to verify by phone or email, and also refuses to return the checks to the employer or the customer",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "employer check hold with no verification path",
      "issue_statement": "About $2600.00 from two employer checks is held with no valid reason given, and Chase will only accept verification through a phone number that only reaches voicemail, refusing email or a stop payment alternative.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "Chase insists on a voicemail-only verification number and refuses alternative verification, while also declining to return the checks to the employer or the customer",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase insists on contacting a phone number that only goes to voicemail, and they have refused to leave a message.", "speaker": "narrative"},
        {"quote": "I have requested that the checks be returned to either the maker or myself, but this request has also been denied.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "About $2600.00 from two employer checks is held with no valid reason given, and Chase will only accept verification through a phone number that only reaches voicemail, refusing email verification or return of the checks."
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
