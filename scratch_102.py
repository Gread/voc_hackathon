# -*- coding: utf-8 -*-
import json, pathlib

bundle = json.load(open("data/work/extract_bundles/bundle_102.json", encoding="utf-8"))
texts = {r["call_id"]: r["text"] for r in bundle["records"]}
keys = {r["call_id"]: r["cache_key"] for r in bundle["records"]}

records = {}

records["cfpb_13567527"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "business checking account and a CD frozen after an indemnification request tied to a $30,000.00 wire transfer, unresolved for 20 months", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "20 months of branch visits and calls met with 'still investigating' and no updates or resolution", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch", "phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "escalating a nearly two-year-old freeze on the business account and a CD, with no access to the funds",
  "underlying_driver": "Chase froze the account after an indemnification request tied to a disputed $30,000.00 wire transfer and has withheld the funds, plus a CD, for 20 months despite proof provided",
  "reason_differs": False,
  "topics": [
    {"topic_label": "account frozen after indemnification request",
     "issue_statement": "Chase froze the business checking account after receiving an indemnification request tied to a $30,000.00 wire transfer, and has refused to release the funds for nearly two years.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned",
     "driver": "account frozen after an indemnification request tied to a disputed $30,000.00 wire transfer; funds withheld ~20 months despite proof provided",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Still, Chase flagged the account as potentially fraudulent and has refused to release my funds.", "speaker": "narrative"},
       {"quote": "I immediately provided proof of the signed contract, communications, and documentation that verified the transaction was valid.", "speaker": "narrative"}
     ]},
    {"topic_label": "certificate of deposit also locked",
     "issue_statement": "A Certificate of Deposit was also locked even though Chase said CDs are not restricted under these circumstances, denying access to that money too.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned",
     "driver": "told Chase does not restrict CDs under these circumstances, yet the CD was locked too",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I was explicitly told that Chase does not restrict Certificates of Deposit ( CDs ) under these circumstancesyet mine has also been locked and I am being denied access to that money too.", "speaker": "narrative"}
     ]},
    {"topic_label": "no updates after 20 months of contact",
     "issue_statement": "Over 20 months of visiting branches and calling, customer service kept saying they were still investigating with no updates or resolution.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "no_response_or_follow_up",
     "driver": "20 months of visits and calls met with 'still investigating' and no updates, support, or resolution",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Ive visited multiple branches, presented legal documents, and have been ignored and dismissed repeatedly.", "speaker": "narrative"},
       {"quote": "Customer service continues to say, Were still investigating, with no updates, no support, and no resolution.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase froze a business account and a CD after an indemnification request tied to a $30,000.00 wire transfer, holding the funds for 20 months with no resolution despite documentation; the customer has retained an attorney."
}

records["cfpb_14060903"] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "credit card account closed without direct notice while enrolled in a hardship program", "is_primary": True},
    {"reason": "rewards_or_promotions", "specific_reason": "unclear status of over XXXX rewards miles accumulated over decades, after the account closure", "is_primary": False},
    {"reason": "other_or_unclear", "specific_reason": "hardship program payment amounts remained too high despite documented, federally-recognized financial hardship", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["chat_or_email"],
  "customer_ask": "explanation",
  "stated_reason": "concerned that the credit card account was closed without proper notice and unsure what happened to the accumulated rewards miles",
  "underlying_driver": "hardship program payments remained higher than affordable despite documented hardship, and the account was closed with no clear notification while the rewards status was left unresolved",
  "reason_differs": False,
  "topics": [
    {"topic_label": "account closed without proper notice",
     "issue_statement": "The Chase credit card account was closed without direct notice; the customer only learned of it from a brief note at the bottom of an email.",
     "product": "credit_card", "sentiment": -1, "driver_category": "other_or_unclear",
     "driver": "account closed while enrolled in a hardship program, with no direct notification other than a note buried in an email",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I was not properly notified of my account closure. I only discovered that Chase had closed my account when I noticed a brief note at the bottom of a recent email communication.", "speaker": "narrative"}
     ]},
    {"topic_label": "unclear status of rewards miles after closure",
     "issue_statement": "After the account closure, it is unclear what happened to over XXXX rewards miles accumulated through years of spending.",
     "product": "credit_card", "sentiment": -1, "driver_category": "other_or_unclear",
     "driver": "unclear whether accumulated rewards miles were forfeited after the account was closed",
     "outcome": "unknown",
     "evidence": [
       {"quote": "I am unclear about the status of these earned rewards.", "speaker": "narrative"}
     ]},
    {"topic_label": "hardship program payments too high",
     "issue_statement": "Despite enrolling in Chase's hardship program and explaining documented financial hardship, the reduced payment amounts still exceeded what the customer could afford.",
     "product": "credit_card", "sentiment": -1, "driver_category": "other_or_unclear",
     "driver": "hardship program payments remained above what income allowed even after explaining an IRS 'Currently Not Collectible' status",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "the payment amounts remained higher than my current financial capacity could support.", "speaker": "narrative"},
       {"quote": "I clearly communicated this limitation and explained that even the reduced payments exceeded what my hardship status would allow.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "Chase representatives were compassionate and understanding despite the situation", "category": "helpful_staff",
     "quote": "To Chase 's credit, their representatives were consistently compassionate and understanding of my situation.", "speaker": "narrative"}
  ],
  "redaction_heavy": True,
  "summary": "A long-time Chase credit card customer facing hardship after her special-needs daughter was abused had her account closed without direct notice while enrolled in a hardship program; the status of her rewards miles is unclear, though representatives were compassionate."
}

records["cfpb_14679512"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "Chase still holding all funds despite the state levy release being confirmed received", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "45 minutes on hold and the rep could not explain why the levy release was not processed", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wants the levy release processed so the held funds are released before payday and bill payments are due",
  "underlying_driver": "although the state levy release was confirmed received on the stated date, Chase has not processed it and cannot explain the delay",
  "reason_differs": False,
  "topics": [
    {"topic_label": "levy release not processed despite confirmation",
     "issue_statement": "Chase confirmed receiving the state levy release but is still holding all funds in the account and could not explain why it has not been processed.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned",
     "driver": "levy release confirmed received but funds remain held with no explanation for the delay",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase Bank is still holding all the funds in my account.", "speaker": "narrative"},
       {"quote": "he could not explain why the levy had not been processed or why my funds remained inaccessible.", "speaker": "narrative"}
     ]},
    {"topic_label": "long hold with no resolution timeline",
     "issue_statement": "After 45 minutes on hold, the representative said the issue would be escalated but that it could still take a few more days to release the funds, while a paycheck deposit and bill payments are at risk.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "long_wait_or_delay",
     "driver": "45 minutes on hold followed by an escalation that could still take a few more days, threatening an incoming paycheck and bill payments",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I contacted Chase after spending 45 minutes on hold.", "speaker": "narrative"},
       {"quote": "The representative stated that he would escalate the issue internally, but it could still take a few more days before the funds are released.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Despite Chase confirming receipt of a state levy release, the bank continues to hold all funds in the account with no explanation, risking a coming paycheck deposit and bill payments."
}

records["cfpb_15329715"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "dispute for an undelivered purchase denied despite documentation provided", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "trying to dispute a debit card transaction for an item that was never delivered",
  "underlying_driver": "the merchant and carrier claim delivery to a locker with no record of it, and Chase considers the transaction valid despite the dispute documentation",
  "reason_differs": False,
  "topics": [
    {"topic_label": "denied dispute for undelivered purchase",
     "issue_statement": "A purchase made with the debit card was never delivered - the locker system has no record and the front desk never received a package - but Chase says the transaction was valid despite supporting documents.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "dispute denied and transaction deemed valid despite the locker having no delivery record and no package received at the front desk",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The merchant and carrier said it was been placed into a locker but the locker system have no records of that.", "speaker": "narrative"},
       {"quote": "I am trying to claim that transaction with Chase and provide all documents which support it to them but they consist it was valid.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A debit card purchase was never delivered despite the merchant's locker claim, but Chase denied the dispute and considers the charge valid even with supporting documentation."
}

records["cfpb_15979946"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a $7,500.00 credit card reportedly opened in the customer's name without their knowledge", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "stop_or_block",
  "stated_reason": "reporting that a Chase credit card with a $7,500.00 limit was opened in their name without authorization",
  "underlying_driver": "received a call about an unauthorized credit card opened in their name and grew suspicious when asked to be transferred to continue resolving it",
  "reason_differs": False,
  "topics": [
    {"topic_label": "unauthorized credit card opened in customer's name",
     "issue_statement": "A caller claiming to be from Chase said a credit card with a $7,500.00 limit had been opened in the customer's name without authorization, and the customer hung up when asked to be transferred to continue resolving it.",
     "product": "credit_card", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "a $7,500.00 credit card reportedly opened without consent; the call's request to transfer to another number raised suspicion",
     "outcome": "unknown",
     "evidence": [
       {"quote": "stating a credit card was open with Chase Bank in my name- $7500.00 limit from XXXX TX, by XXXX XXXX.", "speaker": "narrative"},
       {"quote": "I hung up when he wanted to transfer me to some number to continue resolving this.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unknown",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A caller reported a $7,500.00 Chase credit card opened in the customer's name without authorization; the customer grew suspicious of the call's request to transfer and hung up."
}

records["cfpb_16711362"] = {
  "contact_reasons": [
    {"reason": "loan_servicing", "specific_reason": "auto loan paid off after a total-loss settlement but Chase has not sent the title or proof of payment", "is_primary": True}
  ],
  "products": ["auto_loan"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "trying to get the vehicle title and proof of payment after fully paying off the auto loan following a total loss",
  "underlying_driver": "the loan was paid in full through an insurance settlement plus the remainder, but Chase never sent the title or payment proof",
  "reason_differs": False,
  "topics": [
    {"topic_label": "title and proof of payment withheld after loan payoff",
     "issue_statement": "After the customer paid off the remaining auto loan balance following a total-loss insurance settlement, Chase did not send the vehicle title or any proof of payment.",
     "product": "auto_loan", "sentiment": -1, "driver_category": "no_response_or_follow_up",
     "driver": "loan paid in full through insurance settlement and personal payment, but no title or proof of payment received",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The debt was paid, but Chase did not send me the vehicle title. No proof of payment.", "speaker": "narrative"},
       {"quote": "I have been calling and trying to resolve this issue.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "After paying off an auto loan following a total-loss settlement, Chase has not sent the vehicle title or proof of payment despite repeated calls."
}

records["cfpb_17284518"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "fraud dispute denied solely for being filed more than 60 days after the first charge, with no investigation or documentation", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants Chase to reopen and properly investigate the denied unauthorized-charge dispute and reimburse the charges",
  "underlying_driver": "Chase denied the fraud claim solely for being filed more than 60 days after the first charge, in violation of Regulation E, without investigating or providing documentation",
  "reason_differs": False,
  "topics": [
    {"topic_label": "fraud dispute denied over 60-day timing",
     "issue_statement": "Chase denied the dispute for unauthorized charges starting XX/XX/XXXX solely because it was filed more than 60 days after the first charge, which the customer says violates Regulation E.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "claim denied solely for being filed more than 60 days out, without an investigation or documentation of the authorization determination",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "They denied my claim from XX/XX/XXXX solely because it was more than 60 days after the first charge, which violates Regulation E.", "speaker": "narrative"},
       {"quote": "The bank refused to perform a reasonable investigation and also refused to provide the required documentation showing how they concluded the transactions were authorized.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase denied a dispute over unauthorized charges solely due to a 60-day filing rule, without investigating or providing documentation, which the customer says violates Regulation E."
}

records["cfpb_18278820"] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "wire transfer submitted before the stated cutoff time was not completed until the next business day, causing a $2,600.00 rate-lock extension fee", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"],
  "services": ["branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants reimbursement for a $2,600.00 rate-lock extension fee caused by a delayed wire transfer",
  "underlying_driver": "a wire transfer submitted before the stated cutoff time was not completed until the next business day, triggering the fee from the refinance lender",
  "reason_differs": False,
  "topics": [
    {"topic_label": "wire completed late despite same-day promise",
     "issue_statement": "After a long wait at the branch to submit the wire before the cutoff, the clerk promised same-day completion, but the wire was not completed until Monday, causing a $2,600.00 rate-lock extension fee.",
     "product": "money_transfer_or_p2p", "sentiment": -1, "driver_category": "long_wait_or_delay",
     "driver": "wire submitted before cutoff after a long branch wait, but completed the next business day instead of same-day as promised, triggering a $2,600.00 fee",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "After dealing with high wait time, I was able to submit & sign the papers needed to do the wire transfer at around XXXX prior to the stated XXXX cutoff time for wire transfers.", "speaker": "narrative"},
       {"quote": "The Clerk said that wire would be completed on the same day. However, the wire was completed on Monday and due to this delay I was directly caused a $2600.00 rate-lock extension fee.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A Chase wire transfer submitted before cutoff was promised same-day completion but was not processed until Monday, causing a $2,600.00 rate-lock extension fee on a refinance; the customer wants reimbursement."
}

records["cfpb_18801663"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "induced by scammers to deposit and transfer funds into accounts they controlled at Chase", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "no clear written explanation of beneficiary account handling or recovery efforts despite full cooperation", "is_primary": False}
  ],
  "products": ["checking_or_savings", "money_transfer_or_p2p"],
  "services": ["branch"],
  "customer_ask": "explanation",
  "stated_reason": "reporting being defrauded into depositing cash and transferring funds into scammer-controlled Chase accounts",
  "underlying_driver": "scammers used fake promises to pay off the customer's mortgage/HELOC to induce cash deposits and transfers into their Chase accounts, and Chase has not clearly explained how it handled the beneficiary accounts or recovery",
  "reason_differs": False,
  "topics": [
    {"topic_label": "induced to deposit and transfer funds to scam accounts",
     "issue_statement": "Scammers posing as business representatives induced the customer to deposit and transfer large sums into accounts they controlled at Chase, after initially depositing money elsewhere to build trust.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "scammers used fabricated deposits to build trust, then induced a $20,000.00 deposit, and later withdrew a further $150,000.00 they had deposited despite a letter saying it would not be withdrawn",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I was told that I needed to deposit $20000.00 USD in advance into their JPMorgan Chase Bank business account, and that the remaining funds would later be repaid by me with very little interest.", "speaker": "narrative"},
       {"quote": "Despite this representation, the scammers later withdrew the entire $150000.00 USD.", "speaker": "narrative"}
     ]},
    {"topic_label": "no clear explanation after reporting fraud",
     "issue_statement": "Despite promptly reporting the fraud, filing a police report and cooperating fully, the customer did not receive clear written explanations about how the beneficiary accounts were handled or what recovery efforts were made.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "no_response_or_follow_up",
     "driver": "no clear or complete written explanation given about beneficiary account handling, recovery efforts, or fraud/KYC compliance despite full cooperation",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Despite prompt notification and full cooperation, I did not receive clear or complete written explanations regarding the handling of the beneficiary accounts, recovery efforts, or compliance with fraud monitoring, Know Your Customer ( KYC ), and XXXX XXXX XXXX XXXX XXXX  requirements.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A scam induced the customer to deposit and transfer large sums into scammer-controlled Chase accounts; despite reporting the fraud and filing a police report, Chase has not clearly explained how the accounts were handled or what recovery efforts occurred."
}

records["cfpb_20285286"] = {
  "contact_reasons": [
    {"reason": "access_or_digital_banking", "specific_reason": "locked out of the online credit card portal for over a year unless a mobile phone number is provided", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "escalation to a supervisor left on hold over an hour until disconnected", "is_primary": False},
    {"reason": "terms_information_or_communication", "specific_reason": "physical billing statements stopped despite requesting them, leaving no way to check for fraud", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["online_banking", "phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "unable to access credit card account information or make online payments for over a year",
  "underlying_driver": "Chase requires a mobile phone number to complete identity verification during login, which the customer does not have, and refuses to help without one",
  "reason_differs": False,
  "topics": [
    {"topic_label": "locked out of online account without a mobile number",
     "issue_statement": "The customer has been unable to access online credit card account information or pay bills, ultimately being told access requires a mobile phone number instead of the home number on file for over 15 years.",
     "product": "credit_card", "sentiment": -2, "driver_category": "denied_or_declined_without_explanation",
     "driver": "online access blocked and support says it can't help unless a mobile phone number is provided, despite 15+ years using a home number",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "BECAUSE I ONLY HAVE A HOME PHONE NUMBER AND NOT A MOBILE PHONE NUMBER THAT THEY CAN NOT HELP ME UNLESS I PROVIDE A MOBILE PHONE NUMBER.", "speaker": "narrative"},
       {"quote": "I have been prevented, with criminal intent, by Chase from accessing ANY of my CC Account information or from making an online payment through their online website portal.", "speaker": "narrative"}
     ]},
    {"topic_label": "no physical billing statements sent",
     "issue_statement": "Chase has failed to send any physical billing statements despite the customer's express wishes, leaving no way to check for fraudulent charges.",
     "product": "credit_card", "sentiment": -2, "driver_category": "other_or_unclear",
     "driver": "physical bill mailing stopped against the customer's express request, removing any way to review charges",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase has failed to provide me with ANY physical billing against my expressed wishes that I receive a physical bill by mail.", "speaker": "narrative"}
     ]},
    {"topic_label": "escalation call disconnected after an hour on hold",
     "issue_statement": "When the customer requested escalation to a supervisor, they were left on hold for over an hour until the customer service center closed and the call disconnected.",
     "product": "credit_card", "sentiment": -2, "driver_category": "long_wait_or_delay",
     "driver": "requested supervisor escalation resulted in over an hour on hold before the call was disconnected at close of business",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I was left on hold for over an hour until their customer service center closed and my call was disconnected.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "For over a year, the customer has been locked out of Chase's online credit card portal and denied help unless they provide a mobile phone number, physical billing statements stopped, and a supervisor escalation call was disconnected after an hour on hold."
}

records["cfpb_21399095"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "account closed 20 months ago over suspected check fraud and about $7,900.00 in funds still withheld", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "told to locate the check issuers herself rather than Chase investigating through banking channels", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting immediate release of approximately $7,900.00 withheld since the account was closed 20 months ago over suspected fraud",
  "underlying_driver": "the account was closed over suspected fraud tied to deposited checks, and Chase has provided no documentation, will not investigate the check issuers itself, and has given no valid legal justification for holding the funds this long",
  "reason_differs": False,
  "topics": [
    {"topic_label": "funds withheld 20 months after account closure",
     "issue_statement": "The account was closed roughly 20 months ago over suspected fraud involving deposited checks, and Chase continues to withhold approximately $7,900.00 with no documentation or valid legal justification.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned",
     "driver": "$7,900.00 withheld for 20 months since closure with no documentation or legal justification provided",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "My account was closed approximately 20 months ago due to alleged suspected fraud involving deposited checks.", "speaker": "narrative"},
       {"quote": "To date, I have not been given a valid legal justification for the continued withholding of my funds.", "speaker": "narrative"}
     ]},
    {"topic_label": "told to locate check issuers herself",
     "issue_statement": "Chase representatives said they could not contact the individuals who issued the checks and told the customer she must locate them herself.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "told to track down the check issuers personally instead of Chase investigating through its own banking channels",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase representatives have stated that they are unable to contact the individual ( s ) who issued the checks and have told me that I must locate these individuals myself.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase closed an account 20 months ago over suspected check fraud and continues to withhold about $7,900.00 with no documentation, telling the customer to locate the check issuers herself."
}

records["cfpb_22638837"] = {
  "contact_reasons": [
    {"reason": "fees_and_charges", "specific_reason": "$780.00 in overdraft fees charged across 7 waves over 58 days stemming from a single self-corrected overdraft", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "valid complaints marked 'duplicate' without review and contradictory explanations about the refund policy", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "disputing repeated overdraft fees charged after a single overdraft event that was self-corrected the same night",
  "underlying_driver": "Chase kept charging overdraft fees across multiple waves while complaints were pending, selectively refunding some fees, marking valid complaints as duplicates, and giving contradictory explanations about refund limits",
  "reason_differs": False,
  "topics": [
    {"topic_label": "repeated overdraft fees after single self-corrected event",
     "issue_statement": "A single overdraft of about $420.00 that was self-corrected the same night with a $620.00 deposit led to $780.00 in overdraft fees charged across seven separate waves over 58 days.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "unexpected_charge",
     "driver": "$780.00 in overdraft fees across 7 waves stemming from one self-corrected overdraft, while six CFPB complaints were pending",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase charged three overdraft fees totaling $100.00 on this single-night event, which was legitimate.", "speaker": "narrative"},
       {"quote": "Total charges : $780.00 across 7 separate waves over 58 days in response to one single-night event I had self-corrected.", "speaker": "narrative"}
     ]},
    {"topic_label": "selective refunds and contradictory refund policy",
     "issue_statement": "Chase reversed 68 overdraft fees on the account without any complaint, but denied refunds and gave only partial explanations when the customer complained in writing, and its stated 'three refund' policy contradicts its own data.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "incorrect_or_conflicting_information",
     "driver": "Chase's claim of a 3-refund-per-year limit is contradicted by 68 fee reversals in its own transaction data, and refunds were denied only when the customer complained",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase 's official account transaction export shows 68 overdraft fee reversals on THIS SAME ACCOUNT over the past 12 months.", "speaker": "narrative"},
       {"quote": "You can request up to three overdraft fee refunds in the current calendar year.", "speaker": "narrative"}
     ]},
    {"topic_label": "complaint marked duplicate without review",
     "issue_statement": "A valid complaint about $200.00 in fees was marked 'duplicate' and closed without review, and another investigation was closed the same day the customer's payroll posted.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "error_not_corrected",
     "driver": "a $200.00 fee complaint was marked duplicate without review, and another investigation was closed the same day payroll posted, followed by new fees the same day",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Marked valid complaint ( XX/XX/XXXX ) \" duplicate '' to avoid reviewing $200.00 in fees", "speaker": "narrative"},
       {"quote": "XX/XX/XXXX : Closed complaint # 4 investigation the same day my payroll ( $2600.00 ) posted", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A single self-corrected overdraft led to $780.00 in fees across seven waves over 58 days; Chase's own data shows 68 fee reversals contradicting its stated refund policy, and valid complaints were marked duplicate without review."
}

records["cfpb_23424549"] = {
  "contact_reasons": [
    {"reason": "access_or_digital_banking", "specific_reason": "locked in an endless verification loop unable to log into Chase.com for weeks, account said to be 'suspended' for an unknown reason", "is_primary": True},
    {"reason": "credit_decision_or_limit", "specific_reason": "new credit card application denied because Chase said it could not verify identity despite excellent credit", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["online_banking", "phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "unable to log into the Chase.com account for weeks due to a verification loop, and being told to call in each time",
  "underlying_driver": "the account was placed in an unexplained 'suspended' status and repeated calls to multiple reps did not resolve it; identity verification also blocked a new card application",
  "reason_differs": False,
  "topics": [
    {"topic_label": "login loop and unexplained account suspension",
     "issue_statement": "For weeks the customer has been stuck in a login verification loop on Chase.com, and after many calls was told the account is 'suspended' for an unknown reason that remains unresolved.",
     "product": "credit_card", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "account marked 'suspended' for an unspecified reason despite many calls and verification attempts",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Ultimately their reps tell me that my account is \" suspended '' for some unknown reason and that they will send my issue to a higher level person to have it resolved, but as of today it is still unresolved.", "speaker": "narrative"}
     ]},
    {"topic_label": "new card application denied for unverifiable identity",
     "issue_statement": "A new Chase Sapphire credit card application was denied because Chase said it could not verify the customer's identity, despite excellent credit and income.",
     "product": "credit_card", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "application denied for unverifiable identity with no explanation, despite excellent credit scores and income",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I also applied for a new Chase Sapphire credit card and my application was denied because they claimed they were unable to verify my identity.", "speaker": "narrative"},
       {"quote": "I have excellent credit scores and income, so there is no explanation for any of this.", "speaker": "narrative"}
     ]},
    {"topic_label": "repeated transfers and rude support",
     "issue_statement": "The customer was transferred and hung up on multiple times while being asked the same verification questions repeatedly by different representatives.",
     "product": "credit_card", "sentiment": -1, "driver_category": "staff_attitude_or_competence",
     "driver": "transferred and hung up on several times, repeating verification questions with each of many different reps described as rude and incompetent",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I have been transferred and hung up on several times.", "speaker": "narrative"},
       {"quote": "Their support reps are rude and incompetent.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A 20-year Chase customer has been stuck in a login verification loop for weeks with an unexplained account suspension, a new card application was denied for unverifiable identity despite excellent credit, and repeated calls led to transfers and rude service."
}

records["cfpb_9556021"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "Chase declined to open a dispute for a $2,000.00 Amazon order returned but only the cheaper order was refunded", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants Chase to start a dispute with Amazon for the unrefunded $2,000.00 order returned in the same package as the refunded one",
  "underlying_driver": "Amazon confirmed receiving the return package containing two orders but only refunded the cheaper one, and Chase declined to help after multiple attempts",
  "reason_differs": False,
  "topics": [
    {"topic_label": "declined dispute for partially refunded amazon return",
     "issue_statement": "Both Amazon orders were shipped back in one package, but Amazon only refunded the $1,000.00 order, and Chase declined to start a dispute for the missing $2,000.00 refund despite supporting documentation.",
     "product": "credit_card", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "Chase declined to dispute the $2,000.00 charge after numerous attempts, despite email proof that Amazon received both returned orders in one package",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Amazon notified me that they received the return but only refunded me for one of the order in the amount of $1000.00", "speaker": "narrative"},
       {"quote": "i was declined.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Two Amazon orders returned together were only partially refunded by Amazon, and Chase declined to open a dispute for the missing $2,000.00 refund despite supporting documentation."
}

records["cfpb_9850496"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "Chase froze checking and savings accounts and gave all the funds to a former business partner without any chance to respond", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "reporting that Chase gave all the funds in his checking and savings accounts to a former business partner without letting him respond",
  "underlying_driver": "after a bad-faith business breakup, the former partner went to Chase and had the accounts frozen and the funds released to her without due process",
  "reason_differs": False,
  "topics": [
    {"topic_label": "accounts frozen and funds given to ex-partner",
     "issue_statement": "After a business partnership ended badly, the former partner had the customer's checking ($15,000.00) and savings ($47,000.00) accounts frozen at Chase, and Chase gave her all the money without letting the customer respond.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned",
     "driver": "Chase froze and released $15,000.00 checking and $47,000.00 savings balances to a former business partner without allowing the customer to respond",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "She went to Chase Bank where I have my checking account ( balance $15000.00 ) and savings account ( balance $47000.00 ) frozen and they unlawfully gave her all my money.", "speaker": "narrative"},
       {"quote": "They did not give me a chance to respond.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "After a business partnership breakup, a former partner had the customer's Chase checking and savings accounts frozen and Chase released all the funds to her without letting the customer respond."
}

records["cfpb_10186492"] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "a $300.00 new-account coupon was not applied even though the banker confirmed and printed proof it was applied at account opening", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch", "phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the promised $300.00 new-account bonus credited after completing the direct deposit requirement",
  "underlying_driver": "the branch banker confirmed and printed proof the coupon was applied at account opening, but customer service later said it wasn't applied because it had expired, even though it wasn't expired at opening",
  "reason_differs": False,
  "topics": [
    {"topic_label": "$300 coupon not applied despite banker's confirmation",
     "issue_statement": "The banker who opened the account confirmed and printed proof that a $300.00 new-account coupon was applied, but after completing the direct deposit requirement, customer service said the coupon was not applied because it had expired.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "banker printed confirmation the $300.00 coupon was applied, but customer service later blamed expiration even though it had not expired when the account was opened",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The banker assured me that the code had already been successfully applied and provided a copy of their inner system which shows the applying of the coupon", "speaker": "narrative"},
       {"quote": "they told me the coupon was not applied successfully because it had expired.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "the branch banker was helpful and printed proof the coupon had been applied", "category": "helpful_staff",
     "quote": "The banker assured me that the code had already been successfully applied and provided a copy of their inner system which shows the applying of the coupon", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A branch banker confirmed and printed proof a $300.00 new-account coupon was applied, but after completing the requirements, Chase said it had expired even though it hadn't, and the coupon was never credited."
}

records["cfpb_10503646"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "Chase restricted and closed the checking account after depositing a death benefit check and is now holding the check", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "trying to deposit a death benefit check from her late fiance's mother and access the funds",
  "underlying_driver": "after following the agent's instructions and depositing the check, Chase restricted and closed the account, then required a POA, and is now holding the check until a future release date",
  "reason_differs": False,
  "topics": [
    {"topic_label": "account closed and check held after death benefit deposit",
     "issue_statement": "After depositing a death benefit check from her late fiance's mother following the bank's own instructions, Chase restricted then closed the account, required a POA, and is now holding the check until a specific date.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned",
     "driver": "account restricted and closed after the deposit, a POA was then required, and the check is now held until a stated future release date",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase then restricted my account closed it then told me I needed a POA.", "speaker": "narrative"},
       {"quote": "now theyre telling me they are going to hold on to the check until he gets released XX/XX/year>.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "After depositing a death benefit check from her late fiance's mother per the bank's instructions, Chase restricted and closed her checking account, required a POA, and is now holding the check until a future release date."
}

records["cfpb_10913023"] = {
  "contact_reasons": [
    {"reason": "access_or_digital_banking", "specific_reason": "credit repeatedly freezes after making a payment so the card declines in stores despite showing available credit", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wants Chase to stop freezing available credit after payments so the card doesn't decline in stores",
  "underlying_driver": "after each payment the account shows available credit but the card actually declines at checkout; this has happened three times and support could not guarantee it won't recur",
  "reason_differs": False,
  "topics": [
    {"topic_label": "available credit freezes and declines after payment",
     "issue_statement": "After each credit card payment, the account displays available credit but the card is declined in stores; this has happened three times and Chase cannot guarantee it will stop.",
     "product": "credit_card", "sentiment": -1, "driver_category": "system_or_app_failure",
     "driver": "credit shows available after payment but the card is declined at checkout, happening three times with no guarantee it will stop, and the third time took longer than usual to release",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "This happened 3 times each time I called them they released the funds.", "speaker": "narrative"},
       {"quote": "they said they cant guarantee it wont happen again and they will release funds again but it was taking so much longer than usual!!!!!", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "partially_resolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase's credit card repeatedly shows available credit after a payment posts but then declines in stores; this has happened three times, and support cannot guarantee it won't happen again."
}

records["cfpb_11221708"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "$1,200.00 debited from two failed ATM withdrawal attempts and the claim was denied", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["atm", "phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants $1,200.00 credited back after two failed ATM withdrawal attempts debited the account without dispensing cash",
  "underlying_driver": "the ATM displayed a daily-limit error and never dispensed cash on two attempts, yet $1,200.00 (more than double the daily limit) was debited, and Chase denied the claim citing an inability to track the transactions",
  "reason_differs": False,
  "topics": [
    {"topic_label": "atm debited without dispensing cash",
     "issue_statement": "Two ATM withdrawal attempts of $600.00 each showed a daily-limit error and dispensed no cash, yet $1,200.00 was debited from the account, exceeding the stated $500.00 daily limit.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned",
     "driver": "$1,200.00 debited from two failed ATM attempts with no cash dispensed, exceeding the $500.00 daily limit, and the casino's own receipt confirms both transactions failed",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I saw that a total of $1200.00 was debited from my account despite not receiving any money from the ATM.", "speaker": "narrative"},
       {"quote": "The casino provided me with a printed receipt showing that both transactions had failed and that no money was dispensed by the ATM.", "speaker": "narrative"}
     ]},
    {"topic_label": "claim denied despite evidence",
     "issue_statement": "Chase denied the claim for the $1,200.00 in failed ATM withdrawals, saying it could not track the transactions or recover the funds, despite the casino's receipt showing both transactions failed.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "denied_or_declined_without_explanation",
     "driver": "claim denied on the grounds Chase could not track the transactions, despite documentary proof of the failed withdrawals",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Subsequently, I filed a claim with Chase, but they denied it, stating that they could not track the transactions or recover the funds.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Two failed ATM withdrawal attempts dispensed no cash but debited $1,200.00, exceeding the $500.00 daily limit; Chase denied the claim citing an inability to track the transactions despite a casino receipt proving both failed."
}

records["cfpb_11548020"] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "account closed over alleged bank fraud with no explanation given, after depositing $831.00 in cash", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "promised $830.00 refund check not received, then barred from returning to the branch", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch", "phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the promised $830.00 check for the deposited cash after the account was closed",
  "underlying_driver": "the account was closed for alleged bank fraud with no explanation, the promised refund check was never received, and the customer was later told she could not return to the branch",
  "reason_differs": False,
  "topics": [
    {"topic_label": "account closed for unexplained fraud flag",
     "issue_statement": "After depositing $831.00 in cash, a bank manager said a paycheck could not be cashed because the customer was flagged for bank fraud, and Chase refused to explain why the account was closed.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "flagged for bank fraud and account closed with no reason given despite depositing $831.00 in cash",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I was told by a bank manager that they could not cash my check as I was caught for bank fraud. They did not give me any more details.", "speaker": "narrative"},
       {"quote": "they told me that they did not have to give me a reason for my bank account closure.", "speaker": "narrative"}
     ]},
    {"topic_label": "promised refund check never received",
     "issue_statement": "Chase confirmed it was mailing an $830.00 refund check within 10 business days, but the check never arrived, and the customer was later told she could not return to the branch to resolve it.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned",
     "driver": "promised $830.00 refund check within 10 days never arrived, and the customer was told her phone number didn't match security records, then barred from the branch",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "they were mailing me a check for $830.00 which was the money that I had deposited into my bank account.", "speaker": "narrative"},
       {"quote": "was informed that I was not allowed to come back on to the premises.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase closed a new checking account over an unexplained fraud flag after cash deposits, promised an $830.00 refund check that never arrived, and later barred the customer from the branch."
}

records["cfpb_12135833"] = {
  "contact_reasons": [
    {"reason": "fees_and_charges", "specific_reason": "a 3% foreign transaction fee of $180.00 was charged after downgrading cards, and the fee wasn't waived despite a request", "is_primary": True},
    {"reason": "terms_information_or_communication", "specific_reason": "the online account is still labeled 'Sapphire Reserve' after downgrading, and a travel-notice message misleadingly suggested no issues abroad", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["mobile_app", "phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting a one-time waiver of foreign transaction fees incurred abroad, including a $180.00 fee",
  "underlying_driver": "downgrading from Sapphire Reserve to Freedom Unlimited introduced an unexpected 3% foreign transaction fee that wasn't waived, compounded by the account still being labeled Sapphire Reserve and a misleading travel-notice message",
  "reason_differs": False,
  "topics": [
    {"topic_label": "foreign transaction fee not waived",
     "issue_statement": "After downgrading to avoid an annual fee, the customer was unaware of a 3% foreign transaction fee and incurred $180.00 on a large purchase abroad; Chase refunded smaller related fees but not the $180.00 fee despite a waiver request.",
     "product": "credit_card", "sentiment": -1, "driver_category": "unexpected_charge",
     "driver": "3% foreign transaction fee of $180.00 charged after downgrading cards, not waived despite a request escalated to a manager",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "For this transaction, I incurred a fee of $180.00 on XX/XX/XXXX.", "speaker": "narrative"},
       {"quote": "the fee for $180.00 would not be refunded/ waived.", "speaker": "narrative"}
     ]},
    {"topic_label": "account still labeled sapphire reserve after downgrade",
     "issue_statement": "Even after downgrading, the online banking profile and phone app still officially title the account as 'Sapphire Reserve,' creating confusion about which fees apply.",
     "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "account still displayed as 'Sapphire Reserve' online after downgrading to a card that does carry foreign transaction fees",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "on my Chase online banking profile and phone application, my account is still officially titled as \" Sapphire Reserve ( ... XXXX ) '' leading to confusion regarding applicable fees.", "speaker": "narrative"}
     ]},
    {"topic_label": "misleading travel notice message",
     "issue_statement": "The Chase app's travel notice screen said there was no need to notify the bank when traveling because of enhanced security, giving a false sense of security about purchases and fees abroad.",
     "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "app's travel-notice message claims no need to notify for travel due to security, misleadingly implying no issues with purchases abroad",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Good News, there's no need to notify us when you're traveling anymore.", "speaker": "narrative"},
       {"quote": "You can travel confidently knowing our enhanced security measures will recognize unusual behavior on your account.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "After downgrading credit cards to avoid an annual fee, the customer was hit with an unwaived $180.00 foreign transaction fee, compounded by the account still being labeled 'Sapphire Reserve' online and a misleading in-app travel notice."
}

records["cfpb_12542909"] = {
  "contact_reasons": [
    {"reason": "other_or_unclear", "specific_reason": "email linked to another platform was marked as fraud by Chase instead of reflecting that Chase had simply ended the relationship", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "multiple contact attempts led only to being transferred between departments", "is_primary": False}
  ],
  "products": ["other_or_unspecified"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants the fraud flag on his email removed so it stops restricting his use of another platform",
  "underlying_driver": "Chase previously ended its business relationship with the customer but mistakenly recorded or reported the reason as fraud, which is now restricting his email on another platform",
  "reason_differs": True,
  "topics": [
    {"topic_label": "email wrongly flagged as fraud",
     "issue_statement": "The customer's email linked to another platform was marked as fraud by Chase even though the real reason was that Chase had decided not to do business with him, and this now restricts his use of that platform.",
     "product": "other_or_unspecified", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "email was mistakenly marked fraud instead of reflecting that Chase had simply decided not to do business with the customer, and this restricts use of another platform",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I had my email that was linked to XXXX marked as fraud when it wasnt by chase.", "speaker": "narrative"},
       {"quote": "This hinders my ability to use XXXX other places.", "speaker": "narrative"}
     ]},
    {"topic_label": "transferred repeatedly without resolution",
     "issue_statement": "Multiple attempts to contact Chase about the mislabeled fraud flag resulted only in being transferred from department to department.",
     "product": "other_or_unspecified", "sentiment": -1, "driver_category": "repeated_contact_needed",
     "driver": "multiple contact attempts led only to being transferred department to department with no fix",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I tried contacting chase about this multiple times just to be transferred from department to department.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "Chase mistakenly marked the customer's email as fraud on another platform instead of noting it had simply ended its relationship with him, and repeated contact attempts only resulted in transfers between departments."
}

records["cfpb_13036394"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "reported a fraudulent charge that pushed the business account deeply negative", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "called a liar and treated like she did something wrong when following up on the promised credit timeline", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the promised provisional credit for a reported fraudulent charge issued as originally stated",
  "underlying_driver": "Chase promised a provisional credit within 4 days but later said it would take almost 2 weeks, leaving the account negative and unable to pay bills",
  "reason_differs": False,
  "topics": [
    {"topic_label": "provisional credit delayed from 4 days to nearly 2 weeks",
     "issue_statement": "After reporting a fraudulent charge that pushed the business account deeply negative, the customer was promised a provisional credit within 4 days but was later told it would take almost 2 weeks.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned",
     "driver": "promised a provisional credit within 4 days, later told nearly 2 weeks, leaving the account negative and unable to pay bills or buy food",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I was told that I would receive a a provisional credit within 4 days, and when I called to check on that, I was told that I wouldn't receive any credits until almost 2 weeks after I reported the fraudulent charge.", "speaker": "narrative"},
       {"quote": "This has caused me to be unable to work or pay bills or feed my family.", "speaker": "narrative"}
     ]},
    {"topic_label": "called a liar by customer service",
     "issue_statement": "When following up on the fraud claim, the customer was called a liar and treated like she had done something wrong.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "staff_attitude_or_competence",
     "driver": "called a liar and treated as if she had done something wrong while following up on a legitimate fraud report",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I was called a liar and treated like I did something wrong.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A promised 4-day provisional credit for a reported fraudulent charge stretched to nearly two weeks, leaving a business account deeply negative, and the customer was called a liar when following up."
}

records["cfpb_13572046"] = {
  "contact_reasons": [
    {"reason": "access_or_digital_banking", "specific_reason": "debit card blocked shortly after becoming a new customer, apparently due to a repeated charge", "is_primary": True},
    {"reason": "fees_and_charges", "specific_reason": "charged for a rushed replacement card delivery", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "debit card was blocked shortly after becoming a new customer and a rush-delivery fee for the replacement card was charged with nothing resolved",
  "underlying_driver": "the card was blocked over what seems to be a repeated charge, and after calling to rush a replacement card the customer was charged for that as well",
  "reason_differs": False,
  "topics": [
    {"topic_label": "debit card blocked shortly after becoming a customer",
     "issue_statement": "The customer's debit card was blocked shortly after becoming a new Chase customer, reportedly because of the same charge occurring again.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "system_or_app_failure",
     "driver": "debit card blocked as a new customer apparently due to a repeated charge",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I had my debit card blocked for chase Morgan what l just became new customer because same charge that l had", "speaker": "narrative"}
     ]},
    {"topic_label": "charged for rushed replacement card delivery",
     "issue_statement": "After calling customer service to rush delivery of a replacement card, the customer was charged for that service and nothing has been resolved.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "unexpected_charge",
     "driver": "charged for rushing the replacement card delivery after calling customer service, with nothing resolved since",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "called customer service to rushed on the delivery they charged my account for that and nothing has been resolved", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A new Chase customer's debit card was blocked over an apparent duplicate charge, and after calling to rush a replacement card, the customer was charged for that as well with nothing resolved."
}

records["cfpb_14080217"] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "two newly approved Chase credit card accounts were closed shortly after opening or application without notice or explanation", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "explanation",
  "stated_reason": "requesting reinstatement of the two closed credit card accounts or a clear explanation for the closures",
  "underlying_driver": "both credit card accounts were closed without any notice shortly after approval, with no stated reason despite acting in good faith",
  "reason_differs": False,
  "topics": [
    {"topic_label": "freedom unlimited account closed after approval",
     "issue_statement": "The Chase Freedom Unlimited credit card was approved, but the account was suddenly closed even though the customer's activity was authorized and responsible.",
     "product": "credit_card", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "account closed suddenly after approval despite authorized, responsible activity",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "However, to my surprise, the account was suddenly closed, even though the activity was authorized and I was acting responsibly.", "speaker": "narrative"}
     ]},
    {"topic_label": "second card account closed while awaiting delivery",
     "issue_statement": "A second Chase credit card application was placed under review and the account was closed without notice before the customer could even activate or use the card.",
     "product": "credit_card", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "second account closed without notice while still awaiting the physical card, before any use was possible",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "While awaiting the physical card, I was informed that my application was placed under review, and shortly thereafter, the account was closed without any notice or opportunity for me to activate or use the card.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Two newly approved Chase credit card accounts were closed shortly after opening or application, without notice or explanation, despite the customer acting in good faith."
}

# --- validation pass ---
missing = [cid for cid in texts if cid not in records]
extra = [cid for cid in records if cid not in texts]
if missing:
    raise SystemExit(f"MISSING extraction for: {missing}")
if extra:
    raise SystemExit(f"EXTRA extraction not in bundle: {extra}")

errors = []
for call_id, resp in records.items():
    text = texts[call_id]
    for t in resp["topics"]:
        for e in t["evidence"]:
            if e["quote"] not in text:
                errors.append((call_id, "topic_evidence", e["quote"]))
    for p in resp.get("positive_moments", []):
        if p["quote"] not in text:
            errors.append((call_id, "positive_moment", p["quote"]))

if errors:
    print(f"FOUND {len(errors)} QUOTE ERRORS:")
    for call_id, kind, q in errors:
        print(f"  [{call_id}] {kind}: {q!r}")
    raise SystemExit(1)

out = pathlib.Path("data/cache/extract")
for call_id, resp in records.items():
    payload = {"key": keys[call_id], "prompt_version": "ext-1.0", "schema_version": "1",
               "taxonomy_version": "1", "call_id": call_id, "model": "claude-agent-build",
               "produced_by": "claude_agent", "created_at": "2026-09-11T12:00:00Z", "usage": None,
               "response": resp}
    (out / f"{call_id}.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

print(f"OK: wrote {len(records)} records, all quotes verified as substrings.")
