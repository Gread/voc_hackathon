import json, pathlib

bundle = json.load(open('data/work/extract_bundles/bundle_100.json', encoding='utf-8'))
texts = {r['call_id']: r['text'] for r in bundle['records']}
keys = {r['call_id']: r['cache_key'] for r in bundle['records']}

R = {}

R['cfpb_11545747'] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "free hotel nights earned on one spouse's credit card were erroneously credited to the other spouse's Marriott account and never received by either", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants the free hotel nights earned through his own credit card purchases finally credited to his account",
  "underlying_driver": "a misspelled last name kept the credit card from linking to the correct Marriott account, so the earned free nights were misrouted to the spouse's account instead, and Chase keeps insisting the nights were already received",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "earned free nights misrouted between spouses' accounts",
      "issue_statement": "Free hotel nights earned through the husband's credit card spending were erroneously credited to his wife's Marriott account due to a name misspelling, and Chase insists he already received them.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "a misspelled last name prevented the credit card from linking to the correct Marriott account, causing the earned free nights to be misrouted and never actually delivered to either spouse",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "my Chase card never linked with my Marriott account due to a misspelling of my last name on my credit card", "speaker": "narrative"},
        {"quote": "Each time Chase sends a post-investigation letter explaining that I received my free nights, that the points were posted on my Marriott account, and used.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A misspelled last name kept a credit card from linking to the correct Marriott account, causing earned free hotel nights to be misrouted to the spouse's account, and after a year Chase still insists the nights were already received."
}

R['cfpb_12130940'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a $90.00 charge made without consent was temporarily credited then reversed back to the merchant after the customer missed a callback window, and the merchant keeps billing monthly", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $90.00 unauthorized charge permanently reversed and the recurring merchant billing stopped",
  "underlying_driver": "a temporary credit for an unauthorized $90.00 charge was reversed because the customer did not respond in time to a phone call, and the same merchant continues charging monthly without approval",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "unauthorized charge credit reversed over missed callback",
      "issue_statement": "A $90.00 charge made without consent was temporarily credited, then reversed back to the merchant because the customer did not respond to a phone call in time, and the merchant keeps billing monthly.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "the claim was closed and the temporary credit reversed solely because a callback was missed, and the same merchant continues charging monthly without approval",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "chase credited the amount was back to the merchant claiming they tried making a phone call to me for more info and I didnt respond on time so they closed the claim!", "speaker": "narrative"},
        {"quote": "this merchant is going to keep charging me every month for something I m not approving!", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $90.00 unauthorized charge was temporarily credited then reversed back to the merchant after the customer missed a callback window, and the merchant continues billing monthly without approval."
}

R['cfpb_12537248'] = {
  "contact_reasons": [
    {"reason": "credit_decision_or_limit", "specific_reason": "a credit limit was decreased shortly after leaving a negative review, which the customer believes was retaliation", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "explanation",
  "stated_reason": "questioning why the credit limit was decreased right after submitting a negative review",
  "underlying_driver": "the timing of a credit limit decrease immediately following a requested review makes the customer suspect retaliation",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "credit limit cut after negative review",
      "issue_statement": "Shortly after submitting a negative review, the customer's account limit was decreased, which feels like retaliation for the review.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "other_or_unclear",
      "driver": "the credit limit was lowered immediately after a negative review was submitted, with no other explanation given",
      "outcome": "unknown",
      "evidence": [
        {"quote": "shortly after on XX/XX/year> I receivde an email from my credit monitoring account with XXXX XXXX I received an email that they decreased my account limit", "speaker": "narrative"},
        {"quote": "I feel like they are retaliating against me for the bad review.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unknown",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A credit limit decrease that followed shortly after a negative review left the customer suspecting retaliation."
}

R['cfpb_13014399'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a promised permanent $550.00 credit from a claim resolution was never applied, and Chase refused to share the documentation used or any employee accountability outcome", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "demands the promised $550.00 permanent credit finally be applied to the checking account",
  "underlying_driver": "incorrect information given during the claims process led the customer to believe the account would be permanently credited $550.00, but Chase has not applied it, shared the claim documentation, or explained any accountability for the employees involved",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "promised permanent credit never applied",
      "issue_statement": "Incorrect information during a claims process led the customer to expect a permanent $550.00 credit, which Chase has still not applied, while also refusing to share the claim documentation.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "error_not_corrected",
      "driver": "incorrect information during the claims process promised a permanent $550.00 credit that Chase never applied, and it refuses to provide the documentation used in the investigation",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase bank has not provided me the permanent credit of $550.00 posted to my checking account.", "speaker": "narrative"},
        {"quote": "This unethical and incompetence needs to be corrected by Chase.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Incorrect information given during a claims process led the customer to expect a permanent $550.00 credit that Chase never applied, and it has refused to share the investigation documentation or any accountability outcome for the employees involved."
}

R['cfpb_13548761'] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "both business and personal Chase accounts were closed without prior notice or justification", "is_primary": True},
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "release of a $14000.00 remaining balance has been stalled for over three weeks despite providing all requested check-verification information", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the remaining $14000.00 balance released after providing all requested verification information",
  "underlying_driver": "both accounts were closed without notice, and although the customer fully provided the names and verification contacts for all six checks requested, Chase has neither verified them nor given a timeline for releasing the funds",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "abrupt closure with unreleased balance",
      "issue_statement": "Business and personal accounts were closed without prior notice, and a $14000.00 remaining balance has not been released despite fully providing all six requested check verifications.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "all requested verification for six checks was provided, but Chase has neither verified them nor given any timeline for releasing the $14000.00 balance",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Both my business and personal accounts were closed without prior notice or clear justification.", "speaker": "narrative"},
        {"quote": "Despite these efforts, Chase has neither verified the checks nor provided any clear path forward.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Business and personal accounts were closed without notice, and a $14000.00 remaining balance has not been released for over three weeks despite fully providing all requested check verification information."
}

R['cfpb_14059889'] = {
  "contact_reasons": [
    {"reason": "fees_and_charges", "specific_reason": "monthly service and overdraft fee refund requests were rejected because an annual $180.00 refund cap had been reached, with $71.00 still owed", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the remaining $71.00 in monthly service and overdraft fees refunded",
  "underlying_driver": "Chase applies an annual $180.00 cap on fee refunds, and only $97.00 has been refunded so far, leaving $71.00 in requested refunds unpaid",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "fee refunds capped below amount owed",
      "issue_statement": "Requests to refund monthly service and overdraft fees were rejected because an annual $180.00 refund cap was reached, leaving $71.00 of the requested refunds unpaid.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "unexpected_charge",
      "driver": "an annual $180.00 refund cap left $71.00 of requested monthly service and overdraft fee refunds unpaid",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "they were rejected due to the maximum amount of refund reached for the year", "speaker": "narrative"},
        {"quote": "There is still room to be refunded for the above-mentioned fees totaling to $71.00.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "partially_resolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Requests to refund monthly service and overdraft fees were rejected once an annual $180.00 refund cap was reached, leaving $71.00 of the requested fees unpaid."
}

R['cfpb_14676449'] = {
  "contact_reasons": [
    {"reason": "credit_reporting", "specific_reason": "a formal dispute letter demands investigation and removal of inaccurate information from the credit report, citing an FTC and police report", "is_primary": True}
  ],
  "products": ["credit_reporting_service"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "requests investigation and correction or removal of inaccurate information from the credit report",
  "underlying_driver": "a formal dispute citing legal authority and an enclosed FTC and police report asks for prompt investigation and removal of inaccurate credit report entries",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "formal dispute demanding credit report correction",
      "issue_statement": "A formal legal dispute letter, citing an enclosed FTC report and police report, demands investigation and removal of inaccurate information from the credit report.",
      "product": "credit_reporting_service",
      "sentiment": 0,
      "driver_category": "other_or_unclear",
      "driver": "no specific inaccurate item is described beyond a general demand for investigation and removal, supported by an enclosed FTC and police report",
      "outcome": "unknown",
      "evidence": [
        {"quote": "Iam requesting you investigate the matter and correct and remove allinaccurate imformation from my credit report.", "speaker": "narrative"},
        {"quote": "i have inclosed relevant documents to support my dispute-ftc report , plice report case", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": 0,
  "resolution_status": "unknown",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "A formal dispute letter citing an FTC report and a police report demands investigation and removal of unspecified inaccurate information from the credit report."
}

R['cfpb_15317461'] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "Chase closed the accounts and returned only a small secondary balance, withholding over $3400.00 from the primary account for over a year", "is_primary": True},
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "release of the withheld balance is conditioned on a three-way call with a client the customer can no longer reach", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch", "phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the over $3400.00 primary account balance released",
  "underlying_driver": "after closing the accounts, Chase sent only a small check for the secondary account, and continues withholding the primary balance unless a three-way call with a client who hired the customer can be arranged, which has not been possible for over a year",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "primary balance withheld over unreachable client verification",
      "issue_statement": "After closing the accounts, Chase sent only a small check for the secondary account and continues withholding over $3400.00 from the primary account unless a three-way call with an unreachable client is arranged.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "release of over $3400.00 is conditioned on a three-way call with a client the customer has not been able to reach, despite already providing contract documentation",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "they still wouldn't release my funds unless I got the sender on a three way call", "speaker": "narrative"},
        {"quote": "Chase doesn't care and still refuses to release my money. It's been well over a year now.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "After closing the accounts and returning only a small secondary balance, Chase has withheld over $3400.00 from the primary account for over a year, conditioning release on a three-way call with a client the customer cannot reach."
}

R['cfpb_15966930'] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "a newly opened account was closed with no cause, seizing over $500.00, and years later no explanation or statements could be obtained", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "explanation",
  "stated_reason": "wants to recover the seized funds and get statements explaining the account opening and closure",
  "underlying_driver": "a newly opened account requiring a minimum deposit was closed with no stated cause, seizing over $500.00, and years later Chase would not provide any explanation or the requested statements",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "funds seized on closure with no explanation",
      "issue_statement": "A newly opened account was closed with no stated cause, seizing over $500.00, and years later Chase still would not explain the closure or provide the requested account statements.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "over $500.00 was seized when the account was closed with no cause given, and years later no explanation or statements were provided",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I was notified of account closure from Chase Bank with no cause in XX/XX/XXXX.", "speaker": "narrative"},
        {"quote": "I was not provided further information and was told I could not receive requested statements of opening and closing amounts", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A newly opened account was closed with no stated cause, seizing over $500.00, and years later Chase still refused to explain the closure or provide the requested statements."
}

R['cfpb_16705944'] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "a checking account was closed without warning, and months of calls, including to corporate, never produced a reason for the closure", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "a promised explanatory letter arrived weeks late and explained nothing, and the customer was told he could never open another account with the bank", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "explanation",
  "stated_reason": "wants to know why the checking account was closed",
  "underlying_driver": "the account was closed with no warning, a promised explanatory letter took weeks to arrive and explained nothing, and both a phone representative and a corporate contact refused to say why, only warning the customer could never bank there again",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "closure never explained despite months of calls",
      "issue_statement": "A checking account was closed without warning, and despite months of calls, including to corporate, and a promised explanatory letter, no reason for the closure was ever given.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "corporate refused to explain the closure even after a promised letter arrived weeks late explaining nothing, only warning the account could never be reopened",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "The letter finally came maybe a week and a half after our conversation, and it explained absolutely nothing.", "speaker": "narrative"},
        {"quote": "he precedes to tell me he can not tell me why and that I should be aware that they can close my account upon their discretion", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A checking account was closed without warning, and months of calls, including to corporate, along with a delayed explanatory letter, never produced any reason for the closure."
}

R['cfpb_17282850'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a JPMCB credit card account was opened without authorization or application", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "reporting an unauthorized credit card account for investigation and correction",
  "underlying_driver": "an account was opened in the customer's name without any application or approval on their part",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "credit card opened without authorization",
      "issue_statement": "A JPMCB credit card account was opened without the customer ever applying for it or approving it, discovered through a credit report or notice.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "other_or_unclear",
      "driver": "the account was opened with no application or approval from the customer",
      "outcome": "unknown",
      "evidence": [
        {"quote": "JPMCB Card allowed someone to open a credit card account in my name without my authorization.", "speaker": "narrative"},
        {"quote": "I did * * not * * apply for this credit card, and I did * * not * * give permission for anyone to open it.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unknown",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A JPMCB credit card account was opened without the customer's application or authorization, and they are requesting an investigation and correction."
}

R['cfpb_18277086'] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "Chase charged the wrong, insufficient-funds bank account for a credit card payment despite adding a new account with enough funds", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "asked Chase to stop charging the previous insufficient-funds account and to waive any resulting fees or interest",
  "underlying_driver": "after being told not to repeat the error and not to apply fees, Chase charged the same insufficient-funds account again and applied fees and interest anyway",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "payment charged to wrong account twice",
      "issue_statement": "Despite adding a new bank account with sufficient funds, Chase charged the old insufficient-funds account for the credit card payment, and after being told not to repeat this, did it again and applied fees and interest.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "Chase repeated the same wrong-account charge after being explicitly told to stop and not apply fees, then applied fees and interest anyway",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase instead charged the previous account I had been using which had insufficient funds to cover this month 's balance.", "speaker": "narrative"},
        {"quote": "then attempted to charge the same account that had insufficient funds and applied fees and interest to my credit card account", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Despite adding a bank account with sufficient funds and explicitly telling Chase not to repeat the error, Chase again charged the old insufficient-funds account for a credit card payment and applied fees and interest anyway."
}

R['cfpb_18739103'] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "a duplicate cash-back offer flag caused by a hotel's shared billing system was never corrected despite a supervisor's promise and submitted receipts proving two separate stays", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants both cash-back offers honored since receipts prove two separate stays at properties sharing a front desk",
  "underlying_driver": "a supervisor promised to fix a duplicate-offer flag caused by two hotels sharing one billing system, but despite receipts proving separate stays, Chase never corrected it and denied the offers anyway",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "duplicate offer flag never corrected despite proof",
      "issue_statement": "A supervisor promised to fix a duplicate cash-back offer flag caused by two hotels sharing a billing system, but despite submitted receipts proving two separate stays, Chase never corrected it and denied the offers.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "error_not_corrected",
      "driver": "a supervisor promised to fix the duplicate flag after seeing receipts proving two separate hotel stays, but never did, and Chase kept denying the offers",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Upon writing again and again and again I learned the supervisor did NOTHING and ultimately just lied", "speaker": "narrative"},
        {"quote": "I am livid more than anything at the misleading supervisor and the lies.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A duplicate cash-back offer flag caused by two hotels sharing a billing system was never corrected despite a supervisor's promise and receipts proving two separate stays, leaving both offers denied."
}

R['cfpb_20283958'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a $500.00 ATM withdrawal and two large check withdrawals totaling $16100.00 were fraudulent, and the funds have still not been reimbursed", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["atm", "branch", "phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the fraudulent $500.00, $7400.00 and $8700.00 withdrawals reimbursed",
  "underlying_driver": "after reporting the fraud, filing a police report and having the branch close and reopen the accounts, the customer has still not received reimbursement for any of the three fraudulent withdrawals",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "fraudulent withdrawals still not reimbursed",
      "issue_statement": "A $500.00 fraudulent ATM withdrawal and two fraudulent check withdrawals totaling $16100.00 from savings have still not been reimbursed despite prompt reporting and a police report.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "despite prompt fraud reports, a police report, and account closures, none of the $500.00, $7400.00 or $8700.00 fraudulent withdrawals have been reimbursed",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "someone withdrew XXXX large checks from my savings account -- one for $7400.00 and XXXX for $8700.00", "speaker": "narrative"},
        {"quote": "I have still not received money from Chase for the $500.00, $7400.00, and $8700.00 fraudulent withdrawals.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "a branch representative promptly closed the compromised accounts, opened new ones, and issued a cashier's check for the remaining balance", "category": "fast_resolution", "quote": "The bank representative I met with closed my checking and savings accounts, and opened two new accounts for me.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "Fraudulent ATM and check withdrawals totaling $16600.00 were reported promptly with a police report and the accounts were closed and reopened, but none of the money has been reimbursed."
}

R['cfpb_21393643'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "checking and savings accounts were flagged and restricted, blocking nearly $20000.00, based on a fraud determination the customer calls a false flag", "is_primary": True},
    {"reason": "account_opening_or_closure", "specific_reason": "Chase determined the customer is not eligible to use its checking and savings accounts, pending a review of up to several business days before a refund check is sent", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "explanation",
  "stated_reason": "wants access restored to nearly $20000.00 in primary funds being withheld over a fraud flag",
  "underlying_driver": "Chase determined the customer is ineligible to keep the accounts and is withholding nearly $20000.00 pending a review, and the resulting fraud report to EWS is also restricting other financial accounts and damaging the credit history",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "false fraud flag blocks funds and other accounts",
      "issue_statement": "A fraud determination that Chase calls ineligibility is blocking nearly $20000.00 in funds pending a review of several business days, and the resulting report to EWS is restricting other financial accounts too.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "a fraud flag the customer disputes led Chase to withhold nearly $20000.00 pending review and report a false fraud record to EWS, damaging other accounts",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "This is a false flag that is causing financial hardship because the bank is currently preventing me from accessing nearly $20000.00 of my primary funds.", "speaker": "narrative"},
        {"quote": "their false fraud flag has also caused my XXXX to be restricted and due to them reporting this to EWS my financial history now has a false fraud report on it", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A fraud determination the customer disputes is blocking nearly $20000.00 in account funds pending review, and the resulting report to EWS is also restricting other financial accounts and damaging the customer's financial history."
}

R['cfpb_22633794'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a $350.00 dispute over a moving company's failed and damaging pickup was closed without contacting the customer, and later closed again over a technicality after an escalation letter to the CEO's office went unanswered", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "escalation_or_complaint",
  "stated_reason": "wants the investigation into the $350.00 dispute to continue rather than be closed",
  "underlying_driver": "Chase closed the dispute without contacting the customer, closed it again citing a wrong dispute reason after a broken promise of a three-way call, and a formal escalation letter to the Office of the CEO received no response",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "dispute closed twice without real investigation",
      "issue_statement": "A $350.00 dispute over a moving company's failed pickup and damaged bag was closed without contacting the customer, then closed again over a technical dispute-reason issue after a promised three-way call fell through.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "the dispute was closed twice, once without contact and again over a dispute-reason technicality after a broken three-way call promise; a $100.00 offer was declined",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase closed the case after speaking with XXXX, without ever contacting me.", "speaker": "narrative"},
        {"quote": "closed the case citing that I had selected the wrong dispute reason on Chase 's platform", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "formal escalation to ceo office ignored",
      "issue_statement": "A formal escalation letter sent to Chase's Office of the CEO with return receipt requested has received no response at all.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "no_response_or_follow_up",
      "driver": "a certified escalation letter to the Office of the CEO went entirely unanswered",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I sent a formal escalation letter to Chase 's Office of the CEO. Delivered via USPS with return receipt.", "speaker": "narrative"},
        {"quote": "No response whatsoever from Chase 's Office of the CEO.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $350.00 dispute over a moving company's failed pickup was closed twice without real investigation, and a formal escalation letter to Chase's Office of the CEO went entirely unanswered."
}

R['cfpb_23346124'] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "a $300.00 new-account bonus coupon kept by a branch employee was never entered into the account, and after many months of escalation the bank denied it citing the time lapse its own error caused", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $300.00 promotional bonus credited after meeting the deposit and balance requirements for months",
  "underlying_driver": "the coupon for the $300.00 bonus was given to a branch employee at account opening but never entered into the system, and months of following up with the banker, a branch manager and corporate ended with the bonus denied for a time lapse caused entirely by the bank's own failure to enter the code",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "bonus denied over bank's own coupon error",
      "issue_statement": "A $300.00 new-account bonus coupon given to a branch employee at opening was never entered into the account, and after months of escalation, the bank denied the bonus for a time lapse its own error caused.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "the bonus coupon was never entered into the account by the employee who received it, and months of escalation ended with denial for a time lapse the bank itself caused",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "she had escalated the report but it is being denied because of the time lapse of the request", "speaker": "narrative"},
        {"quote": "The time lapse is due to the bank not imputing the code into the account upon opening and then failing to follow up on my requests for the credit due to their employee error.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $300.00 new-account bonus coupon given to a branch employee was never entered into the account, and after months of escalating through the branch and corporate, the bonus was ultimately denied for a time lapse the bank's own error caused."
}

R['cfpb_9554727'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a $1200.00 fraudulent charge confirmed by Chase's own fraud department was later denied for lack of documentation the customer could not possibly provide", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "faxed evidence including a merchant chat transcript confirming the fraud was never received across three attempts at two branches", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support", "branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $1200.00 fraudulent charge reversed after already being confirmed as fraud once",
  "underlying_driver": "Chase's own fraud department initially confirmed multiple suspicious purchase attempts on the card, but the claim was later denied for lack of documentation, and repeated faxed proof from the merchant confirming the fraud was never received",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "confirmed fraud denied for undeliverable documentation",
      "issue_statement": "A $1200.00 charge that Chase's own fraud department initially flagged after multiple suspicious attempts was later denied for lack of documentation, even after the merchant confirmed the fraud and a refund.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "the claim was denied for lack of documentation despite the fraud department's own prior confirmation of suspicious activity, and staff could not say what documentation would be acceptable",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "The operator pulled up the charge, noting that there had been several attempts at purchases for much larger amounts, declining until one went through successfully.", "speaker": "narrative"},
        {"quote": "This is now theft on the part of Chase bank.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "faxed proof never received across three attempts",
      "issue_statement": "A faxed transcript and paperwork from the merchant confirming the fraud and refund was never received by Chase across three attempts at two different branches.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "no_response_or_follow_up",
      "driver": "faxed proof of the confirmed fraud and refund was sent three times from two branches and never received, with representatives at a loss each time",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "The fax was never received. I have tried three times, most recently XX/XX/XXXX, at two different branches", "speaker": "narrative"},
        {"quote": "any time I call, they are at a complete loss of what to do", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $1200.00 charge that Chase's own fraud department initially flagged as suspicious was later denied for undeliverable documentation, even after the merchant confirmed the fraud and refunded it, with faxed proof failing to arrive across three attempts at two branches."
}

R['cfpb_9835966'] = {
  "contact_reasons": [
    {"reason": "loan_servicing", "specific_reason": "a demand for disclosure of who actually received a $1100.00 home insurance premium paid from an escrow account, after a form response the customer calls false", "is_primary": True}
  ],
  "products": ["mortgage"],
  "services": [],
  "customer_ask": "explanation",
  "stated_reason": "demands documentation and disclosure of who received the $1100.00 escrow payment for home insurance and under what authority",
  "underlying_driver": "a form letter claimed the insurance premium was paid through the escrow account by another entity, which the customer disputes, demanding proof of the wire or check and the authority for JP Morgan Chase to make and receive the payment",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "disputed escrow payment disclosure demand",
      "issue_statement": "A form letter claimed a $1100.00 home insurance premium was paid through escrow by another entity, which the customer disputes, demanding proof of payment and disclosure of who actually received the money.",
      "product": "mortgage",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "a form response attributes the $1100.00 escrow payment to another entity, which the customer says is false based on records showing JP Morgan Chase itself received the funds",
      "outcome": "unknown",
      "evidence": [
        {"quote": "This is a lie. ALL payments for my home insurance policy are made by JP Morgan Chase", "speaker": "narrative"},
        {"quote": "I demand to disclose the source of authority who authorized JP Morgan to make payments for my home insurance", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unknown",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "A form letter attributed a $1100.00 escrow-paid home insurance premium to another entity, which the customer disputes based on records showing JP Morgan Chase itself received the funds, and is demanding full disclosure of the payment."
}

R['cfpb_10181970'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a $17000.00 check deposit was held 14 days, the account was then closed, and the promised 6-8 week refund has not arrived after 10 months despite extensive documentation", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $17000.00 released after 10 months of providing documentation proving ownership of the source account",
  "underlying_driver": "a check deposit was held, the account was closed, and despite branch managers repeatedly helping submit tax returns, operating agreements and financial statements to the verification department, the check still has not been verified or released after 10 months",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "check still unverified after 10 months",
      "issue_statement": "A $17000.00 check deposit held for 14 days led to the account being closed and a promised 6-8 week refund, but 10 months later the check still has not been verified or released despite extensive documentation.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "despite submitting tax returns, operating agreements and financial statements repeatedly through local branch managers, verification still has not released the $17000.00 after 10 months",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase held the check for 14 days, and after the 14th day sent me a letter stating my account had been closed and my money would be refunded to me within 6-8 weeks.", "speaker": "narrative"},
        {"quote": "Check still needs to be verified to be released please help me", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "local branch managers repeatedly helped submit documents to the verification department", "category": "helpful_staff", "quote": "The managers of local chase bank have helped me send documents then have me call in a few days to the verification dept", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A $17000.00 check deposit hold led to account closure and a promised 6-8 week refund, but 10 months later the check still has not been verified or released despite extensive documentation submitted through helpful branch managers."
}

R['cfpb_10492849'] = {
  "contact_reasons": [
    {"reason": "credit_decision_or_limit", "specific_reason": "an LLC business credit card's limit was lowered from a much higher amount to $3000.00 without warning, apparently based on the personal signer rather than the business", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "explanation",
  "stated_reason": "questioning why the LLC's credit limit was lowered without warning based on personal rather than business creditworthiness",
  "underlying_driver": "the business credit card limit was cut to $3000.00 with no warning, and nothing in the disclosures mentioned that personal information would be used against the LLC's credit limit",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "business card limit cut using personal information",
      "issue_statement": "An LLC business credit card's limit was lowered to $3000.00 without warning, apparently based on the personal signer's information rather than the business, which was never disclosed.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "policy_or_terms_change",
      "driver": "the business credit limit was cut without warning, mixing personal signer information with the LLC's creditworthiness in a way never mentioned in the disclosures",
      "outcome": "unknown",
      "evidence": [
        {"quote": "in late XXXX without any warning the Credit Limit for the LLC  credit card was lowered to $3000.00 USD!", "speaker": "narrative"},
        {"quote": "Noowhere in the disclosure it is mentionned that personal information will be used against Credit Limit of LLC!", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unknown",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "An LLC's business credit card limit was cut to $3000.00 without warning, apparently based on the personal signer's information, which was never disclosed as a factor."
}

R['cfpb_10907990'] = {
  "contact_reasons": [
    {"reason": "fees_and_charges", "specific_reason": "a $95.00 annual fee began being charged on a card that had never carried one, with no prior notice, and Chase refused to refund the earlier years", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the previous years' annual fees refunded since they were never disclosed",
  "underlying_driver": "a card that had never carried an annual fee suddenly began being billed $95.00 with no notice of the change, and Chase refused to refund the fees already charged",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "undisclosed new annual fee not refunded",
      "issue_statement": "A card that had never carried an annual fee began being billed $95.00 with no prior notification, and Chase refused to refund the fees already charged with no explanation.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "unexpected_charge",
      "driver": "a new $95.00 annual fee appeared with no prior notice on a card that never had one, and Chase refused to refund the fees already charged",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I did not receive any prior notification to any such change.", "speaker": "narrative"},
        {"quote": "Chase refused to refund the previous years ' fees with no explanation.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A card that had never carried an annual fee suddenly began being billed $95.00 with no prior notice, and Chase refused to refund the fees already charged."
}

R['cfpb_11213188'] = {
  "contact_reasons": [
    {"reason": "other_or_unclear", "specific_reason": "the contents of a safe deposit box, including family heirloom watches, were shipped to a warehouse without any notice, and one watch was found damaged", "is_primary": True}
  ],
  "products": ["other_or_unspecified"],
  "services": ["branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants compensation for the damaged heirloom watch caused by the bank's mishandling",
  "underlying_driver": "the safe deposit box contents were removed and shipped to a Texas warehouse without any attempt to contact the customer, and a family heirloom watch's crystal was broken in the process, with no offer of compensation",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "safe deposit contents shipped away and damaged",
      "issue_statement": "The contents of a safe deposit box, including family heirloom watches, were removed and shipped to a warehouse without any notice, and one watch's crystal was found broken, with no offer of compensation.",
      "product": "other_or_unspecified",
      "sentiment": -2,
      "driver_category": "error_not_corrected",
      "driver": "valuable safe deposit contents were shipped to a warehouse without contacting the customer, and the bank showed no interest in compensating for a heirloom watch damaged in the process",
      "outcome": "partially_resolved",
      "evidence": [
        {"quote": "the contents had been \" put in a bag '' and sent to a warehouse in Texas", "speaker": "narrative"},
        {"quote": "The larger issue is the brazen and irresponsible way in which the bank handled our valuable possessions, making no effotr to content us about the mistake they made.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "partially_resolved",
  "positive_moments": [
    {"what": "the branch manager helped track down and recover the shipped contents", "category": "helpful_staff", "quote": "The branch manager then started to help, and determined that the contents had been \" put in a bag '' and sent to a warehouse in Texas.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "Safe deposit box contents including family heirloom watches were shipped to a warehouse without any notice, and a watch was damaged in the process, with the bank showing no interest in compensating for it despite the branch manager's help recovering the items."
}

R['cfpb_11546575'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a $650.00 undelivered sofa dispute was denied after the merchant sent the bank incorrect refund information for an unrelated item", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "a rude supervisor refused to help even after being shown documentation, and the bank opened a second $100.00 dispute without the customer's knowledge", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $640.00 for the undelivered sofa refunded after providing correct purchase documentation",
  "underlying_driver": "the merchant sent the bank incorrect refund information tied to a different, unrelated item, and despite providing correct documentation, a rude supervisor refused to help and the bank opened an unauthorized second dispute that took additional money",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "dispute denied over mismatched refund information",
      "issue_statement": "A $650.00 sofa that never arrived was disputed, but the claim was denied because the merchant sent the bank incorrect refund information belonging to a completely different item.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "the merchant's refund information referred to an unrelated item, and despite correct documentation being provided, the bank sided with the merchant's incorrect data",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "XXXX sent wrong refund information to my bank, I followed up with the bank to correct this", "speaker": "narrative"},
        {"quote": "as all claims were denied by Chase bank due to XXXX providing wrong information order numbers are incorrect etc", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "rude supervisor and unauthorized second dispute",
      "issue_statement": "A supervisor was rude and unhelpful even after seeing purchase documentation, and the bank opened a second $100.00 dispute without the customer's knowledge, taking additional money from the account.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "staff_attitude_or_competence",
      "driver": "a supervisor said there was nothing that could be done despite documentation being shown, and a second dispute was opened without the customer's knowledge or consent",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "spoke to a supervisor who was very rude to me and stated \" there is nothing I can do ''", "speaker": "narrative"},
        {"quote": "the bank opened another dispute with out my knowledge for $100.00", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $650.00 undelivered sofa dispute was denied after the merchant sent incorrect refund information for a different item, a supervisor was rude despite documentation being provided, and the bank opened a second dispute without the customer's knowledge, taking $640.00 total from the account."
}

R['cfpb_12131331'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "Chase denied a dispute over a merchant's broken price-match promise without giving a valid reason for deeming the charge legitimate", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $160.00 price difference refunded as the merchant's chat agent had agreed in writing",
  "underlying_driver": "a merchant's cancellation forced a repurchase at a higher price after a chat agent promised the original price would be honored, and Chase denied the dispute without a valid reason after the merchant stalled past its promised response time",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "price-match promise dispute denied",
      "issue_statement": "After a merchant's own cancellation forced a repurchase at a higher price, a chat agent promised in writing to honor the original price, but Chase denied the dispute without a valid reason.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase denied the price-difference dispute as legitimate without giving a valid reason, despite a written chat agreement to honor the original price",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Attempted to dispute transaction with Chase credit card, was denied and not given a valid reason why they deemed it legitimate.", "speaker": "narrative"},
        {"quote": "I am requesting the $160.00 be refunded as stated.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "After a merchant's own cancellation forced a higher-priced repurchase despite a written chat promise to honor the original price, Chase denied the resulting $160.00 dispute without giving a valid reason."
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
