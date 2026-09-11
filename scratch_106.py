# -*- coding: utf-8 -*-
import json, pathlib

bundle = json.load(open("data/work/extract_bundles/bundle_106.json", encoding="utf-8"))
texts = {r["call_id"]: r["text"] for r in bundle["records"]}
keys = {r["call_id"]: r["cache_key"] for r in bundle["records"]}

records = {}

records["cfpb_18815691"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "$700.00 withdrawn without notice as a 'double presentment' reversal, and Chase won't investigate a documentation mismatch", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["branch", "phone_support"], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants Chase to investigate and reverse a $700.00 withdrawal taken as an unexplained 'double presentment' reversal",
  "underlying_driver": "Chase withdrew $700.00 without notice claiming a double-presented check, but the check copy Chase provided doesn't match the original document the issuing bank confirmed and released, and Chase refuses to investigate the discrepancy",
  "reason_differs": False,
  "topics": [
    {"topic_label": "$700 withdrawn over unverified double presentment",
     "issue_statement": "Chase withdrew $700.00 without prior notice, claiming a 'double presentment' of a check, but the check copy Chase provided does not match the original document the issuing bank confirmed and released.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned",
     "driver": "$700.00 taken without notice over a 'double presentment' claim, backed by a check copy that doesn't match the issuing bank's original, verified document",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "On XX/XX/year> JPMC bank took $700.00 from my bank account without ever sending me an alert or notifying me.", "speaker": "narrative"},
       {"quote": "the copy of the check provided by XXXX  Chase bank did not match the original document cleared by XXXX XXXX XXXX  and XXXX", "speaker": "narrative"}
     ]},
    {"topic_label": "refused to investigate despite proof of release",
     "issue_statement": "Despite obtaining a formal letter and the original check copy from the issuing bank confirming the funds were cleared and released, Chase refuses to investigate the discrepancy and says it can no longer help.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "denied_or_declined_without_explanation",
     "driver": "proof of release from the issuing bank was presented, but Chase refuses to investigate the discrepancy and says it can no longer help",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Despite presenting this evidence to JPMC branch management and phone representatives, the bank refuses to investigate the discrepancy between their records and the issuing banks records.", "speaker": "narrative"},
       {"quote": "They have stated they \" can no longer help me, '' leaving me with a negative balance of $ XXXX and causing significant financial hardship.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase withdrew $700.00 without notice over an unverified 'double presentment' claim backed by a mismatched check copy, and refuses to investigate despite the customer obtaining proof of release from the issuing bank."
}

records["cfpb_20356796"] = {
  "contact_reasons": [
    {"reason": "fees_and_charges", "specific_reason": "Chase returned an unauthorized withdrawal's principal but refused to indemnify $250.00 in overdraft fees it caused", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting reimbursement of $250.00 in overdraft fees caused by an unauthorized withdrawal Chase already reversed",
  "underlying_driver": "Chase returned the $550.00 principal from an unauthorized withdrawal but denies any processing error occurred, despite the reversal itself proving the withdrawal was improper, and refuses to cover the resulting $250.00 in overdraft fees",
  "reason_differs": False,
  "topics": [
    {"topic_label": "overdraft fees from reversed withdrawal not covered",
     "issue_statement": "Chase returned the $550.00 principal from an unauthorized withdrawal but refused to indemnify $250.00 in seven $34.00 overdraft fees the withdrawal caused, despite claiming in writing that no processing error occurred.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "unexpected_charge",
     "driver": "$250.00 in seven $34.00 overdraft fees caused by an unauthorized withdrawal that Chase itself later reversed, while denying any processing error occurred",
     "outcome": "partially_resolved",
     "evidence": [
       {"quote": "While Chase returned the principal $550.00 on XX/XX/year>, they have refused to indemnify me for $250.00 in overdraft fees caused directly by their unauthorized withdrawal.", "speaker": "narrative"},
       {"quote": "In their response dated XX/XX/year>, Chase falsely claimed 'no processing errors ' occurred. However, their own action of reversing the payment proves the withdrawal was improper.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "partially_resolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase reversed an unauthorized $550.00 withdrawal but refused to cover the resulting $250.00 in seven overdraft fees, despite the reversal itself contradicting its claim that no processing error occurred."
}

records["cfpb_21424523"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "checking account closed for suspicious activity, withholding $1,400.00 in legitimate wages for over a month with a stated 12-year investigation timeline", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting immediate release of a $1,400.00 remaining balance or a clear written explanation and timeline for the hold",
  "underlying_driver": "the account was closed over suspicious activity even though the funds are entirely legitimate employer direct deposits, and Chase told the customer the investigation could take up to 12 years",
  "reason_differs": False,
  "topics": [
    {"topic_label": "wages withheld with 12-year investigation timeline",
     "issue_statement": "A checking account was closed for suspicious activity even though its funds are entirely legitimate employer direct deposits, and over a month later Chase says the investigation could take up to 12 years before the $1,400.00 balance is released.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned",
     "driver": "$1,400.00 in verified wages withheld over a month with Chase citing a possible 12-year investigation timeline and no written explanation",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "When I contacted the bank, I was told the investigation could take up to 12 years, which is unreasonable given that the funds are verified wages.", "speaker": "narrative"},
       {"quote": "I have requested clarification and a timeline, but have not received a clear explanation for the delay or any indication of when my funds will be released.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase closed a checking account over suspicious activity despite the funds being entirely legitimate wages, and after a month is withholding the $1,400.00 balance with a stated possible 12-year investigation timeline."
}

records["cfpb_22645275"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "$16,000.00 in unauthorized transfers after a stolen phone; Chase denied the remaining $3,700.00 claim without providing investigative documentation", "is_primary": True}
  ],
  "products": ["checking_or_savings", "money_transfer_or_p2p"], "services": ["mobile_app"], "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting reimbursement of the remaining $3,700.00 unauthorized transfer loss and the complete investigative file behind Chase's denial",
  "underlying_driver": "after the phone was lost or stolen, $16,000.00 in unauthorized transfers occurred; $12,000.00 was recovered from the receiving platform but Chase denied the remaining $3,700.00 claim, directing the customer back to the merchant without ever providing the records it relied on",
  "reason_differs": False,
  "topics": [
    {"topic_label": "remaining $3,700 claim denied without documentation",
     "issue_statement": "After $16,000.00 in unauthorized transfers followed a lost or stolen phone, and $12,000.00 was recovered from the receiving platform, Chase denied the remaining $3,700.00 claim and has never provided the investigative records or audit trail behind that decision.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "denied_or_declined_without_explanation",
     "driver": "$3,700.00 of a $16,000.00 unauthorized-transfer loss remains denied, with Chase directing the customer back to the merchant and never producing the records or audit trail it relied on despite repeated requests",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Despite that, Chase denied reimbursement of the remaining $3700.00. Chase stated only that it did not find evidence to support reimbursement and directed me to continue working directly with the merchant because the merchant initiated the transactions.", "speaker": "narrative"},
       {"quote": "Chase still has not provided the investigative documentation, records relied upon, or electronic audit trail needed to explain that denial.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "partially_resolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "After $16,000.00 in unauthorized transfers followed a lost or stolen phone, Chase denied reimbursement of the remaining $3,700.00 unrecovered loss and has never provided the investigative records or audit trail behind that decision, despite a related identity-theft matter being resolved in the customer's favor."
}

records["cfpb_23452025"] = {
  "contact_reasons": [
    {"reason": "credit_reporting", "specific_reason": "a business credit card is incorrectly reported on the customer's personal credit report as a personal card", "is_primary": True}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "fix_error",
  "stated_reason": "wants the business credit card corrected so it stops appearing on his personal credit report",
  "underlying_driver": "a Chase business credit card is incorrectly showing up on the personal credit report as though it were a personal card",
  "reason_differs": False,
  "topics": [
    {"topic_label": "business card misreported as personal",
     "issue_statement": "A Chase business credit card for the customer's own company is incorrectly showing up on his personal credit report as a personal card.",
     "product": "credit_card", "sentiment": -1, "driver_category": "other_or_unclear",
     "driver": "business credit card incorrectly reported on the personal credit file rather than as a business account",
     "outcome": "unknown",
     "evidence": [
       {"quote": "My Chase XXXX credit card is one of the business card for my own company, but it incorrectly showing up on my personal credit report showing as my personal card.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unknown", "positive_moments": [], "redaction_heavy": False,
  "summary": "A Chase business credit card is incorrectly appearing on the customer's personal credit report as a personal card."
}

records["cfpb_9560772"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "$330.00 sent by error or fraud to an unknown person was denied as authorized despite evidence the recipient denied knowing the customer", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $330.00 sent to an unknown person refunded after reporting it as fraud immediately",
  "underlying_driver": "Chase denied the fraud claim saying the customer authorized the payment, despite the recipient denying knowing the customer or the transfer, and Chase made no effort to contact the recipient or report the incident to authorities",
  "reason_differs": False,
  "topics": [
    {"topic_label": "denied claim despite recipient denying the transfer",
     "issue_statement": "A $330.00 transfer to an unknown person was reported as fraud within minutes, with the recipient denying knowing the customer or accepting any transfer, but Chase's investigation denied the claim saying the customer authorized the payment.",
     "product": "money_transfer_or_p2p", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "$330.00 claim denied as authorized despite the recipient denying the transfer and the customer providing text and phone records as evidence, with no effort by Chase to contact the recipient or report the incident",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The individual denied knowing me denied the tranfer and denied having a XXXX  acount.", "speaker": "narrative"},
       {"quote": "Chase Investigated and denied my claim they said I authorized payment from bank XXXX account.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A $330.00 transfer to an unknown person, whom the customer immediately reported and who denied knowing him or accepting the money, was still denied by Chase as an authorized payment, with no attempt made to contact the recipient or report the incident."
}

records["cfpb_9859904"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "unauthorized charges and a covertly issued replacement card sent to a different address, claim denied citing chip and correct PIN", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "transferred repeatedly between departments despite documented store security footage confirming she wasn't responsible", "is_primary": False}
  ],
  "products": ["checking_or_savings"], "services": ["phone_support", "branch", "mobile_app"], "customer_ask": "refund_or_reversal",
  "stated_reason": "trying to prove that unauthorized transactions were not made by her after a caller impersonating Chase fraud staff led to a covertly issued replacement card",
  "underlying_driver": "a caller who correctly authenticated as Chase led to a small card-replacement fee, then unauthorized ATM and store charges appeared, and Chase discovered a second replacement card had been issued to a different address, yet still denied the claim citing chip entry and correct PIN usage while store security confirmed she wasn't the one on camera",
  "reason_differs": False,
  "topics": [
    {"topic_label": "claim denied despite second card sent elsewhere",
     "issue_statement": "After a caller convincingly posing as Chase fraud staff triggered a card replacement, unauthorized charges of over $2,000.00 followed, and Chase later confirmed a second replacement card had been issued and mailed to an address that wasn't hers, yet still denied the claim citing chip entry and correct PIN usage.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "claim denied on chip-and-PIN grounds even after Chase confirmed a second replacement card was issued and mailed to an unfamiliar address, suggesting the account itself was compromised",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The representative told me XXXX cards had been issued, XXXX to my current address and XXXX to an address that was not mine.", "speaker": "narrative"},
       {"quote": "Over the phone, I was told that my card was used via chip entry. The representative on the phone told me that it is impossible to recreate a chip.", "speaker": "narrative"}
     ]},
    {"topic_label": "store footage confirmed fraud but chase kept transferring her",
     "issue_statement": "A store's security footage confirmed the customer was not the one who made the disputed purchases, but Chase kept transferring her between departments without helping her prove the fraud.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "repeated_contact_needed",
     "driver": "store security confirmed she wasn't on camera for the fraudulent purchases, yet Chase kept transferring her between fraud, technical, and branch staff with no one able to help",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "They were able to pull the footage and security confirmed it was not me.", "speaker": "narrative"},
       {"quote": "I've called Chase many times, having been transferred many times and to no avail.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "the store's head of security pulled footage and confirmed the customer was not the one who made the fraudulent purchases", "category": "helpful_staff",
     "quote": "They were able to pull the footage and security confirmed it was not me.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A caller convincingly posing as Chase fraud staff triggered a card replacement, after which unauthorized charges exceeding $2,000.00 appeared and a second replacement card was found mailed to an unfamiliar address, yet Chase denied the claim on chip-and-PIN grounds and kept transferring the customer despite store security footage confirming she wasn't responsible."
}

records["cfpb_10199260"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "identity theft with money stolen and wrong contact information on the account blocking online access", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["online_banking"], "customer_ask": "fix_error",
  "stated_reason": "wants the fraud resolved and the incorrect phone number on the account corrected so she can access her account and funds",
  "underlying_driver": "fraud and identity theft led to stolen funds and an incorrect phone number being attached to the account, which is now blocking online access",
  "reason_differs": False,
  "topics": [
    {"topic_label": "wrong phone number blocks account access after fraud",
     "issue_statement": "After experiencing fraud and identity theft with money stolen, the account now shows an incorrect phone number that is blocking the customer from accessing her account and funds online.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "system_or_app_failure",
     "driver": "an incorrect phone number attached to the account after a fraud incident is blocking online access to funds",
     "outcome": "unknown",
     "evidence": [
       {"quote": "The last numbers are XXXX and that is not my number.", "speaker": "narrative"},
       {"quote": "It's keeping me from accessing my account and funds", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unknown", "positive_moments": [], "redaction_heavy": True,
  "summary": "After a fraud and identity theft incident, an incorrect phone number attached to the account is blocking the customer from accessing her account and funds online."
}

records["cfpb_10510069"] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a payment misdirected due to a mistyped phone number was denied even after Chase initially assured a refund", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the money back after mistakenly reversing two digits of the recipient's phone number on a transfer",
  "underlying_driver": "the transfer went to the wrong phone number despite the correct name being displayed, and although Chase repeatedly said the claim would be expedited and the money returned, it was ultimately closed and denied",
  "reason_differs": False,
  "topics": [
    {"topic_label": "misdirected transfer denied despite assurances",
     "issue_statement": "A transfer sent to a mistyped phone number, though displaying the correct recipient name, was repeatedly said to be expedited with the money coming back, but the claim was ultimately closed and denied.",
     "product": "money_transfer_or_p2p", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "transfer sent to a mistyped phone number despite the correct name showing, and despite verbal assurances the claim would be expedited and refunded, it was closed and denied",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "they said that they can expedite the process and that I will get my money back becuase I reacted fast.", "speaker": "narrative"},
       {"quote": "When I called on XXXX they said that they close my claim and that I will not get my money back.this is after they told XXXX I will and that those money should be in my account in XXXX.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A transfer sent to a mistyped phone number but displaying the correct recipient name was repeatedly promised an expedited refund, only for the claim to be closed and denied."
}

records["cfpb_10929270"] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "a $300.00 checking bonus and a related $400.00 combined-account bonus were denied after Chase reclassified a same-day wire deposit as not qualifying as direct deposit", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the promised $300.00 checking bonus and additional $400.00 combined-account bonus paid after complying with revised instructions",
  "underlying_driver": "Chase said the first wired deposit didn't qualify as 'direct deposit,' the customer sent a second wire following Chase's own guidance which was still rejected as not an 'electronic deposit of a paycheck,' even though it was payment from his employer, so Chase never paid either bonus",
  "reason_differs": False,
  "topics": [
    {"topic_label": "checking bonus denied despite following chase's guidance",
     "issue_statement": "After a first wired deposit was rejected as not qualifying for a $300.00 checking bonus, Chase told the customer his employer payment still wasn't an acceptable 'direct deposit' even after he followed the bank's own guidance on how to send it correctly.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "$300.00 checking bonus denied after the customer's employer payment, following Chase's own revised guidance, was still rejected as not an acceptable direct deposit",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "despite numerous attempts on my part to obtain the \" $300.00 Bonus '' on the Checking Account Chase has refused to comply claiming that I failed to \" complete all requirement activities ''.", "speaker": "narrative"},
       {"quote": "received the enclosed letter which states that my \" direct deposit needed to be an electronic deposit of ( my ) paycheck ''", "speaker": "narrative"}
     ]},
    {"topic_label": "combined-account $400 bonus also withheld",
     "issue_statement": "Because the checking account bonus was never honored, Chase also refused to pay an additional $400.00 bonus promised for opening both a checking and savings account at the same time.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "$400.00 combined-account bonus withheld because the linked $300.00 checking bonus was never honored",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Because of their ongoing reluctance to accept my argument they have refused to send me the \" extra $400.00 bonus '' to which I was entitled when I decided to \" open both at the same time '' and I have been scammed out of a total of $700.00.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase denied a promotional $300.00 checking bonus even after the customer followed the bank's own revised instructions for sending a qualifying deposit, and also withheld a related $400.00 combined-account bonus, leaving him out $700.00."
}

records["cfpb_11228049"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a scam caller convincingly posing as Chase fraud staff walked the customer through wiring $15,000.00 that was never returned as promised", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "months of calls for updates produce no response on the remaining unrecovered funds", "is_primary": False}
  ],
  "products": ["money_transfer_or_p2p"], "services": ["phone_support", "online_banking"], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the remaining wired funds, beyond the $7,600.00 already recovered, returned after being scammed into a wire transfer by a caller posing as Chase fraud staff",
  "underlying_driver": "a scam caller passed Chase's own verification steps and walked the customer through wiring $15,000.00 to 'protect' it, the receiving bank recovered $7,600.00 after investigation, but months of calls for the rest have gone unanswered",
  "reason_differs": False,
  "topics": [
    {"topic_label": "wire scam claim denied as self-initiated",
     "issue_statement": "A caller convincingly posing as Chase fraud staff walked the customer through wiring $15,000.00 to 'protect' the funds, and when the money never returned as promised, Chase's claim was denied as a self-initiated transfer.",
     "product": "money_transfer_or_p2p", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "$15,000.00 wired under a scammer's step-by-step guidance during a call that passed Chase's own verification, then the claim was denied as self-initiated",
     "outcome": "partially_resolved",
     "evidence": [
       {"quote": "the person walked me through setting up a wire transfer to move my $15000.00 so when accounts were hit money wouldn't be in there and that the funds would be put back within XXXX hours.", "speaker": "narrative"},
       {"quote": "Claim was denied saying I initiated the transfer even though I tried to explain what happened.", "speaker": "narrative"}
     ]},
    {"topic_label": "no updates on remaining funds after partial recovery",
     "issue_statement": "After the receiving bank recovered $7,600.00 of the stolen wire, the customer has had to keep calling for updates on the rest, with no response, delaying her retirement plans.",
     "product": "money_transfer_or_p2p", "sentiment": -1, "driver_category": "no_response_or_follow_up",
     "driver": "after a $7,600.00 partial recovery, repeated calls for the remaining funds get no response, forcing the customer to delay retirement",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I have had to constantly call Chase XXXX XXXX XXXX for updates on the request for remaining funds and keep being told they are no longer getting a response from them?", "speaker": "narrative"},
       {"quote": "The plan was to retire this year which I had to put on hold.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "partially_resolved",
  "positive_moments": [
    {"what": "the receiving bank investigated and recovered $7,600.00 of the stolen funds", "category": "fast_resolution",
     "quote": "They filed a reclaim of funds with XXXX XXXX and I got back $7600.00.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A scam caller who passed Chase's own verification walked the customer through wiring $15,000.00 that was never returned, and while $7,600.00 was later recovered by the receiving bank, months of calls about the remaining funds have gone unanswered, delaying her retirement."
}

records["cfpb_11549582"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a chargeback for an airline's undisclosed baggage fee and delayed, missing-content luggage was denied despite documented proof of the airline's own error", "is_primary": True}
  ],
  "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the airline charge reversed after documented proof the airline overcharged, delayed the bag, and it arrived with missing contents",
  "underlying_driver": "despite the airline admitting fault in writing and Chase promising to follow up before deciding, Chase sided with the airline without ever reaching back out to the customer",
  "reason_differs": False,
  "topics": [
    {"topic_label": "chargeback denied despite airline's own admission",
     "issue_statement": "Chase denied a chargeback for an airline's undisclosed baggage fee and a delayed, missing-content bag, even after the customer provided statements from the airline admitting its own error, and despite promising to reach out before deciding.",
     "product": "credit_card", "sentiment": -2, "driver_category": "denied_or_declined_without_explanation",
     "driver": "chargeback denied in favor of the airline despite the airline's own written admission of error, and Chase never followed up as promised before its decision",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I told Chase I had ample proof, including statements from the airline admitting to their error. Chase said they would reach out to me. They never did.", "speaker": "narrative"},
       {"quote": "Just got a letter saying they sided with XXXX XXXX. They didnt do anything.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase denied a chargeback over an airline's undisclosed baggage fee and a delayed, missing-content bag, siding with the airline despite the airline's own written admission of error and never following up as promised."
}

records["cfpb_12140703"] = {
  "contact_reasons": [
    {"reason": "credit_reporting", "specific_reason": "a $6,500.00 fraudulent debt is repeatedly added and removed from the credit file despite multiple police reports", "is_primary": True}
  ],
  "products": ["credit_reporting_service"], "services": [], "customer_ask": "fix_error",
  "stated_reason": "wants the fraudulent $6,500.00 debt permanently removed from her credit file",
  "underlying_driver": "despite submitting police reports multiple times showing her information was stolen, the $6,500.00 fraudulent debt keeps being removed and then re-added to her credit file every other day",
  "reason_differs": False,
  "topics": [
    {"topic_label": "fraudulent debt repeatedly re-added to credit file",
     "issue_statement": "A $6,500.00 fraudulent debt has been added and removed from the credit file roughly a dozen times over two months, despite the customer submitting police reports multiple times showing her information was stolen.",
     "product": "credit_reporting_service", "sentiment": -2, "driver_category": "error_not_corrected",
     "driver": "$6,500.00 fraudulent debt keeps reappearing on the credit file every other day despite repeated police report submissions",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "JPMCB has added and removed the same fraudulent $6500.00 debt to my credit file about XXXX times in the past two months.", "speaker": "narrative"},
       {"quote": "I have already submitted my police report multiple times showing that all my information was stolen.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A $6,500.00 fraudulent debt keeps being removed and re-added to the customer's credit file roughly every other day for two months, despite her repeatedly submitting police reports proving her information was stolen."
}

records["cfpb_12531834"] = {
  "contact_reasons": [
    {"reason": "loan_servicing", "specific_reason": "Chase proceeded with a vehicle sale and loan despite allegedly knowing the manufacturer was going insolvent, and now offers a buyback well below the loan balance", "is_primary": True}
  ],
  "products": ["auto_loan"], "services": [], "customer_ask": "explanation",
  "stated_reason": "questioning why Chase proceeded with the loan despite reportedly knowing about the manufacturer's insolvency, and disputing an unfairly low buyback offer",
  "underlying_driver": "Chase allegedly knew the manufacturer would not remain solvent but still financed the purchase with false solvency assurances, and the resulting buyback offer is lower than comparable vehicles with fewer features, while unclear delivery timing forced selling the old car at a loss",
  "reason_differs": False,
  "topics": [
    {"topic_label": "buyback offer far below loan despite known insolvency risk",
     "issue_statement": "Chase allegedly knew the manufacturer would not remain solvent but still financed the vehicle purchase with false solvency assurances, and the resulting buyback offer is lower than what owners of lesser, similar vehicles are receiving.",
     "product": "auto_loan", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "buyback offer for the vehicle is lower than comparable vehicles with fewer features, despite Chase reportedly knowing about the manufacturer's insolvency risk when it financed the sale",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I am told that Chase was aware that XXXX was not going to be able to remain solvent, yet Chase and XXXX still went through with the sale of the vehicle including providing false information about the future solvency of XXXX.", "speaker": "narrative"},
       {"quote": "people with other XXXX vehicles, lesser models, are getting higher offers for their vehicles with less features than mine.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase allegedly knew the vehicle manufacturer would become insolvent but still financed the purchase with false solvency assurances, and the resulting buyback offer is lower than what similar, lesser vehicles are receiving; unclear delivery timing also forced selling the old car at a loss."
}

records["cfpb_13045275"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a $1,300.00 hotel-room fraud charge was denied and later reinstated, breaking Chase's advertised zero-liability protection", "is_primary": True}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $1,300.00 unauthorized hotel-room charge refunded under Chase's advertised zero-liability protection",
  "underlying_driver": "an unauthorized $1,300.00 charge was made in the customer's hotel room while he was out, and Chase denied the dispute because of one unrelated card-present transaction afterward, later reinstating the fraudulent charge despite its advertised zero-liability policy",
  "reason_differs": False,
  "topics": [
    {"topic_label": "zero-liability protection not honored for hotel fraud",
     "issue_statement": "An unauthorized $1,300.00 charge made in the customer's hotel room while he was out was denied by Chase because of one later card-present taxi transaction, and after weeks the charge was reinstated despite Chase's advertised zero-liability protection.",
     "product": "credit_card", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "$1,300.00 unauthorized hotel charge reinstated after weeks, breaking Chase's advertised zero-liability protection, based only on one unrelated later transaction",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "they said that they could not return the charges given that I used my credit card afterwards.", "speaker": "narrative"},
       {"quote": "they finally reinstated them and told me that they were unable to refund me for the unauthorized charges, breaking their agreement on the XXXX Liability Protection that is prominently touted on their website as one of their major benefits.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "An unauthorized $1,300.00 hotel-room charge was denied by Chase over one unrelated later transaction, and the charge was ultimately reinstated despite Chase's advertised zero-liability fraud protection."
}

records["cfpb_13582821"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "recurring charges after cancellation were credited then reversed as an 'installment loan,' leaving the account overdrawn", "is_primary": True}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the dispute reopened for recurring charges billed after cancellation, which Chase initially credited then reversed",
  "underlying_driver": "the customer canceled the service before ever using it, Chase initially credited the disputed recurring charges but then reversed the credit calling it an installment loan, leaving the account overdrawn $300.00",
  "reason_differs": False,
  "topics": [
    {"topic_label": "credit reversed for post-cancellation charges",
     "issue_statement": "Recurring charges billed after the customer canceled and never used the service were initially credited by Chase, then reversed as an 'installment loan,' leaving the account overdrawn $300.00.",
     "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "credit for post-cancellation charges was reversed by re-labeling them an 'installment loan,' despite the service being canceled before any use, leaving the account $300.00 overdrawn",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase initially gave me a credit, but then reversed it, saying it was an installment loan.", "speaker": "narrative"},
       {"quote": "I am now overdrawn $300.00.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Charges billed after the customer canceled a service he never used were initially credited by Chase, then reversed by relabeling them an 'installment loan,' leaving the account overdrawn $300.00."
}

records["cfpb_14091801"] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a repeat overpayment the receiver confessed to was closed by Chase without resolving the bank-to-bank dispute needed to return the funds", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants Chase to dispute and return $1,300.00 in repeat payments the receiver has confessed were an overpayment",
  "underlying_driver": "the customer never authorized a repeat payment, and although the receiver admitted it was an overpayment and said the resolution required a bank-to-bank dispute, Chase closed the dispute instead of pursuing it",
  "reason_differs": False,
  "topics": [
    {"topic_label": "confessed overpayment dispute closed by chase",
     "issue_statement": "The receiver of two $650.00 payments confessed it was an unauthorized overpayment requiring a bank-to-bank dispute, but Chase closed the dispute instead of pursuing recovery of the funds.",
     "product": "money_transfer_or_p2p", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "receiver confessed the $1,300.00 was an overpayment needing a bank-to-bank dispute, but Chase closed the dispute rather than pursuing the money back",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The receiver confessed it is the overpayment, but she need bank to bank dispute.", "speaker": "narrative"},
       {"quote": "Our Chase bank seems close the dispute", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "The recipient of two unauthorized $650.00 payments admitted it was an overpayment needing a bank-to-bank dispute, but Chase closed the dispute instead of pursuing the funds back."
}

records["cfpb_14686061"] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "long-standing account being closed with no explanation given despite a clean history", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["branch"], "customer_ask": "explanation",
  "stated_reason": "requesting a clear explanation, review, and chance to respond before the account is permanently closed",
  "underlying_driver": "Chase notified the customer his account will be permanently closed with no explanation, no prior warning, and branch representatives said no information could be shared, despite years of responsible use",
  "reason_differs": False,
  "topics": [
    {"topic_label": "account closure with no explanation given",
     "issue_statement": "A long-standing account is being permanently closed with no explanation, no prior warning, and branch staff saying no information could be shared, despite a history of no late payments and responsible use.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "account closure notice with no explanation or prior warning, and branch representatives unable to share any information despite a clean payment history",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase notified me that my account will be permanently closed on XX/XX/XXXX, without giving any explanation.", "speaker": "narrative"},
       {"quote": "I visited the bank several times and spoke with representatives, requesting a reason or any information that would allow me to clarify or prove myself. Unfortunately, I was told no information could be shared.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A long-time Chase customer's account is being closed with no explanation or prior warning, and branch staff said no information could be shared despite a clean, responsible account history."
}

records["cfpb_15340031"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a fraudulent withdrawal remains unresolved and unreimbursed despite immediate reporting and repeated follow-up", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["branch", "phone_support"], "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting the official fraud case number, a copy of the investigation decision, and reimbursement of the stolen funds",
  "underlying_driver": "a fraudulent transfer to an unrecognized, phishing-like account was reported the same day, but despite one follow-up call promising an update, no further communication or reimbursement has followed",
  "reason_differs": False,
  "topics": [
    {"topic_label": "fraud case unresolved despite immediate reporting",
     "issue_statement": "A fraudulent transfer to an unrecognized, phishing-like account was reported the same day it occurred, but despite phone and in-person follow-ups, Chase has not reimbursed the funds or provided a transparent investigation update.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "no_response_or_follow_up",
     "driver": "fraudulent transfer reported the same day, but repeated phone and in-person follow-ups have produced no reimbursement or transparent investigation update since one promised callback",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "He confirmed XXXX had received my case and stated I would be contacted again with an update. However, I have not received any further communication since that call.", "speaker": "narrative"},
       {"quote": "I have complied fully, reported the suspicious activity immediately on XX/XX/XXXX, and followed up multiple times, both by phone and in person at a branch. Yet, XXXX has failed to provide answers, accountability, or reimbursement.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A fraudulent transfer to an unrecognized, phishing-like account was reported the same day, but despite repeated phone and in-person follow-ups and one promised callback, the funds remain unreimbursed with no transparent investigation update."
}

records["cfpb_15994110"] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "a reopened account was restricted and closed the same day her first paycheck cleared, with no reason given", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "multiple branch visits and calls produced no help or explanation", "is_primary": False}
  ],
  "products": ["checking_or_savings"], "services": ["branch", "phone_support"], "customer_ask": "explanation",
  "stated_reason": "wants to know why the account was restricted and closed the same day her first paycheck became available, and to get her money back",
  "underlying_driver": "after being told the bank was no longer collecting on her old overdraft and reopening an account, her first paycheck's availability coincided with card declines, a call to 'refresh' something, and then the account being restricted and closed with no reason given",
  "reason_differs": False,
  "topics": [
    {"topic_label": "account restricted and closed the day paycheck cleared",
     "issue_statement": "After being told she could reopen an account since the bank was no longer collecting on an old overdraft, the customer's first paycheck became available, her card began declining, and the same day she called about it the account was restricted and closed with no reason given.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "account restricted and closed the same day the first paycheck cleared and the customer called about card declines, with no reason ever given",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "a lady said she would refresh something going on with my card and the same day my account was restricted and closed, with out any reason", "speaker": "narrative"},
       {"quote": "They are not giving me a reason why they closed my account and it will be almost a XXXX  that they held onto my money.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "After reopening an account once told an old overdraft debt was no longer being collected, the customer's account was restricted and closed the same day her first paycheck cleared, with no reason given and her money held for weeks."
}

records["cfpb_16726075"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a merchant keeps running canceled recurring charges early against prepaid accounts, repeatedly triggering overdraft fees that Chase won't reverse", "is_primary": True}
  ],
  "products": ["prepaid_card"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants Chase to stop the recurring charges from a canceled subscription and reverse the resulting overdraft fees",
  "underlying_driver": "a merchant keeps charging a canceled subscription early against multiple prepaid accounts, triggering repeated $34.00 overdraft fees, and even though the merchant confirmed the cancellation, Chase denies responsibility and won't release the charges",
  "reason_differs": False,
  "topics": [
    {"topic_label": "canceled subscription keeps triggering overdraft fees",
     "issue_statement": "A canceled online subscription keeps being charged early against multiple prepaid accounts, triggering repeated $34.00 overdraft fees, and even though the merchant confirms the cancellation, Chase denies it's their issue and won't release the fees.",
     "product": "prepaid_card", "sentiment": -2, "driver_category": "unexpected_charge",
     "driver": "canceled subscription repeatedly charged early against prepaid accounts causing recurring $34.00 overdraft fees, with the merchant confirming cancellation but Chase still refusing to release the charges",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I canceled out a online app account several months ago and they keep doing reoccurring payments on this causing me to overdraft", "speaker": "narrative"},
       {"quote": "XXXX has already confirmed that they canceled it they're not running it through Chase is and they are still denying that it's their issue and they are not releasing it again this month", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A canceled subscription keeps being charged early against multiple prepaid accounts, repeatedly triggering $34.00 overdraft fees, and even though the merchant confirms the cancellation, Chase denies responsibility and won't release the charges."
}

records["cfpb_17300419"] = {
  "contact_reasons": [
    {"reason": "loan_servicing", "specific_reason": "vehicle title not sent to the DMV despite over a month and 11 contacts, including the wrong title being sent", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "two calls were disconnected during attempts to resolve the title issue", "is_primary": False}
  ],
  "products": ["auto_loan"], "services": ["phone_support"], "customer_ask": "fix_error",
  "stated_reason": "wants the correct vehicle title sent to the DMV after over a month of delays and 11 contact attempts",
  "underlying_driver": "Chase repeatedly failed to send the correct vehicle title to the DMV, sending the wrong one and disconnecting two calls, leaving the customer unable to drive for over a month and incurring lost wages and transportation costs",
  "reason_differs": False,
  "topics": [
    {"topic_label": "wrong title sent after month of delays",
     "issue_statement": "Despite 11 contacts over more than a month requesting the vehicle title be sent to the DMV, Chase sent the wrong title, forcing a wasted day at the DMV and leaving the customer unable to drive.",
     "product": "auto_loan", "sentiment": -2, "driver_category": "error_not_corrected",
     "driver": "wrong vehicle title sent to the DMV after over a month and 11 contacts, forcing a wasted day at the DMV and leaving the customer unable to drive",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase sent the wrong title, forcing me to spend a full day at the DMV where they could not process the transaction.", "speaker": "narrative"},
       {"quote": "Because the correct title has still not been provided, I have been unable to drive my vehicle for over a month.", "speaker": "narrative"}
     ]},
    {"topic_label": "calls disconnected during title resolution",
     "issue_statement": "Two Chase representatives disconnected the call while the customer was trying to resolve the title delay.",
     "product": "auto_loan", "sentiment": -2, "driver_category": "staff_attitude_or_competence",
     "driver": "two representatives disconnected calls during attempts to resolve the ongoing title delay",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Two Chase representatives disconnected the call, which was unprofessional and obstructed resolution.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Despite 11 contacts and over a month of waiting, Chase sent the wrong vehicle title to the DMV and two representatives disconnected calls during the process, leaving the customer unable to drive and incurring lost wages and transportation costs."
}

records["cfpb_18289448"] = {
  "contact_reasons": [
    {"reason": "terms_information_or_communication", "specific_reason": "a written settlement offer paid in full was not honored, and the balance was not reduced to $0.00 as promised", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "phone representatives gave verbal explanations that directly contradict the written settlement terms", "is_primary": False}
  ],
  "products": ["credit_card"], "services": ["online_banking", "phone_support"], "customer_ask": "fix_error",
  "stated_reason": "requesting Chase honor its written settlement offer by reducing the balance to $0.00 and confirming the account is satisfied",
  "underlying_driver": "Chase issued a written settlement offer to satisfy the account for $280.00, the customer paid in full, but the balance still shows $740.00 outstanding, and phone reps gave contradictory verbal explanations instead of honoring the written terms",
  "reason_differs": False,
  "topics": [
    {"topic_label": "settlement paid in full but balance not reduced",
     "issue_statement": "After paying a written settlement offer of $280.00 in full to satisfy the account, the balance still shows $740.00 outstanding instead of being reduced to $0.00 as the offer stated.",
     "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "$280.00 settlement paid in full per a written offer, but the balance remains at $740.00 instead of the promised $0.00",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The offer stated that a one time payment of $280.00 would satisfy the account and that the account balance would be reduced to $0.00.", "speaker": "narrative"},
       {"quote": "The account continues to show an outstanding balance of $740.00 despite the settlement payment having been accepted and cleared.", "speaker": "narrative"}
     ]},
    {"topic_label": "phone reps contradict written settlement terms",
     "issue_statement": "Two Chase call center representatives said the remaining balance is supposed to stay on the account and simply won't be pursued, directly contradicting the written settlement terms that promised a $0.00 balance.",
     "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "phone representatives verbally contradicted the written settlement offer, saying the balance would remain rather than be reduced to $0.00",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Both representatives stated that the remaining balance is supposed to remain on the account and that Chase will simply not pursue collection of the remaining amount. This directly contradicts the written settlement offer, which stated that the settlement payment would satisfy the account and reduce the balance to $0.00.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase issued a written settlement offer of $280.00 to zero out a credit card balance, but after the customer paid in full the balance still shows $740.00 outstanding, and phone representatives gave verbal explanations directly contradicting the written terms."
}

records["cfpb_18816872"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a $4,000.00 wire for an apartment deposit and rent to a scammer went unrefunded despite a lease clause promising a full refund", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"], "services": ["branch"], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $4,000.00 wired for a deposit and first month's rent refunded after being unable to reach the landlord",
  "underlying_driver": "the customer wired $4,000.00 for an apartment deposit and rent under a lease that promised a full refund if unsatisfied, but could not reach the person afterward and has not been refunded",
  "reason_differs": False,
  "topics": [
    {"topic_label": "apartment deposit wire unrefunded",
     "issue_statement": "A $4,000.00 wire for an apartment deposit and first month's rent, sent under a lease promising a full refund if unsatisfied, went unrefunded after the customer could not reach the recipient again.",
     "product": "money_transfer_or_p2p", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "$4,000.00 wired for a deposit and rent under a full-refund lease clause was never refunded after the recipient became unreachable",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "In the leasing agreement, it says I can get full refund if I do not like the place. I did not get hold of the person at all and I could not get refund.", "speaker": "narrative"},
       {"quote": "I called Chase bank and completed IC3 complaint ( Submission ID : XXXX ) and completed FTC Report ( Number XXXX ).", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A $4,000.00 wire for an apartment deposit and rent, sent under a lease promising a full refund, went unrefunded after the recipient became unreachable, and the customer has filed IC3 and FTC reports."
}

records["cfpb_20360587"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a rental car damage charge was upheld without documentation, while the matching rental-protection benefit claim was denied for lacking that same documentation", "is_primary": True}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "explanation",
  "stated_reason": "requesting Chase resolve the contradiction between upholding a rental damage charge without documentation and denying the matching benefit claim for lacking that documentation",
  "underlying_driver": "the merchant never provided a repair estimate or invoice despite repeated requests, yet Chase upheld the disputed damage charge anyway, and then separately denied the rental-protection benefit claim specifically because that same documentation was missing",
  "reason_differs": False,
  "topics": [
    {"topic_label": "contradictory positions on missing repair documentation",
     "issue_statement": "Chase upheld a rental car damage charge based only on the rental contract despite no repair estimate ever being provided, then denied the matching rental-protection benefit claim specifically because that same repair documentation was missing.",
     "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "Chase upheld the damage charge without requiring repair documentation, then denied the rental-protection benefit claim for lacking that exact documentation, which the merchant never provided despite repeated requests",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase upheld the charge based solely on the contractual agreement.", "speaker": "narrative"},
       {"quote": "Chase Benefits has refused to process the claim without a repair estimate or invoice, even though the merchant has not provided one and Chase itself was unable to obtain one during the dispute process.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase upheld a rental car damage charge with no repair documentation, then denied the matching rental-protection benefit claim specifically for lacking that same documentation, which the merchant never provided despite repeated requests."
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
