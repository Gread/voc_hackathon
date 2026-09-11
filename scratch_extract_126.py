# -*- coding: utf-8 -*-
import json, pathlib

bundle = json.load(open('data/work/extract_bundles/bundle_126.json', encoding='utf-8'))
texts = {r['call_id']: r['text'] for r in bundle['records']}
keys = {r['call_id']: r['cache_key'] for r in bundle['records']}

R = {}

R["cfpb_18882181"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "business checking account with a $12,000.00 balance frozen for no given reason", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants the frozen $12,000.00 business checking account funds released",
  "underlying_driver": "the bank put a hold and froze the account for no stated reason, halting the business",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "business account frozen without reason",
      "issue_statement": "The business checking account with a $12,000.00 balance was frozen with no reason given and the funds have not been released, stopping the business from operating.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "money_held_or_not_returned",
      "driver": "no reason given for freezing a $12,000.00 business checking account; funds still not released and business stopped working",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "CHASE BANK DISCRIMINATED ME AND PUT HOLD ON MY FUNDS FOR NO REASON AND ALSO FREEZED MY CHASE BUSINESS CHECKING ACCOUNT WITH BALANCE OF $12000.00 AND IS NOT RELEASING MY FUNDS.", "speaker": "narrative"},
        {"quote": "BECAUSE OF THIS MY BUSINESS STOPED WORKING.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A business checking account holding $12,000.00 was frozen with no reason given, halting the business, and the customer calls it discriminatory."
}

R["cfpb_20489349"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "check deposit frozen for verification for over 4 months even after the issuing bank confirmed the funds", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "multiple calls to resolve the frozen funds with no manager callback", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["mobile_app", "phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wants the frozen $6,300.00 check deposit released after it was already verified",
  "underlying_driver": "the deposited check needed verification, phone number mismatches delayed it, and the account stayed frozen even after the issuing bank confirmed the funds",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "check deposit held for verification",
      "issue_statement": "A $6,300.00 check deposit was frozen for verification, and even after the issuing bank verified the funds, the account remained frozen.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "check verified by the issuing bank yet the account stayed frozen for 4 months",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I checked the app a couple days later and it had said my money needed verified and should take a couple days.", "speaker": "narrative"},
        {"quote": "The money was resolved and verified by the issuing bank and Chase still refuses to give it to me.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "no callback despite manager request",
      "issue_statement": "Despite asking for a manager call back multiple times over four months, nobody has called to resolve the frozen account.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "no_response_or_follow_up",
      "driver": "asked for a manager call back repeatedly; none received in 4 months",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Ive asked for a manager call back and I have yet to recieve one.", "speaker": "narrative"},
        {"quote": "This has been an ongoing issue for 4 months.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "a customer service representative found the correct verification number and called it", "category": "helpful_staff", "quote": "One of their customer service guys found a different number and called that one.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A $6,300.00 check deposit was frozen for verification and stayed frozen for over four months despite being confirmed by the issuing bank, with no callback from a manager as promised."
}

R["cfpb_21468032"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "business account locked after Chase treated a retried $1,800.00 check deposit correction as fraudulent activity", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["mobile_app"],
  "customer_ask": "fix_error",
  "stated_reason": "disputes Chase's decision to freeze the business account after a technical error during a check deposit",
  "underlying_driver": "a rejected check scan was corrected and accepted, but the bank treated the retry as fraud and locked the account",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "business account locked after deposit retry",
      "issue_statement": "A retried check deposit of $1,800.00, submitted after the first scan was rejected, was treated as fraudulent and the entire business account was locked.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "app scan retry after a rejected first attempt was flagged as fraud and locked the entire business account",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase has characterized this correction of a failed technical scan as \" fraudulent activity '' and subsequently locked my entire business account.", "speaker": "narrative"},
        {"quote": "This unjustified freeze has caused significant harm to my trucking operations and forced me to file a tax extension.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A retried check deposit, resubmitted after an initial scan rejection, was wrongly flagged as fraud and led to a full business account lock causing significant business harm."
}

R["cfpb_23586039"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "settlement check of $3,100.00 was cashed then held for over a year despite a verification phone number printed on the check", "is_primary": True},
    {"reason": "account_opening_or_closure", "specific_reason": "account closed a few days after the hold with no notice or reason given", "is_primary": False},
    {"reason": "customer_service_experience", "specific_reason": "check department staff refused to call the verification number and were rude, implying the customer was a scammer", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wants Chase to release the $3,100.00 held from a deposited and already-cashed settlement check",
  "underlying_driver": "Chase would not call the verification number on the check, then closed the account without explanation and gave no resolution for over a year",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "settlement check held despite verification offer",
      "issue_statement": "A $3,100.00 settlement check that was deposited and already cashed was frozen because Chase said it could not be verified, even though a verification phone number was printed on the check.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "Chase refused to call the verification number printed on the check, citing an internal restriction, and never released the $3,100.00",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "but CHASE BANK holding my account & amount $3100.00 for some suspicious reason ... and they described can't verify the check.", "speaker": "narrative"},
        {"quote": "almost 1 and half year passed still I didn't get any solution from the CHASE BANK.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "account closed without notice",
      "issue_statement": "After a few days, the account was closed without any notice or explanation.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "account closed abruptly a few days after the hold, no reason ever given",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "after few day Bank closed my account without any noticed to me and they didn't showed any reason..", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "rude staff called customer a scammer",
      "issue_statement": "Check department staff were rude and indirectly implied the customer was a scammer while offering no solution.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "staff_attitude_or_competence",
      "driver": "check department staff rude and implied the customer was a scammer instead of resolving the hold",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "and some time they got rude to me from check department and indirectly they indicated I am like scammer.... and unable to provide any described and solution to me....", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $3,100.00 settlement check was deposited and cashed but then held indefinitely because Chase would not call the printed verification number; the account was later closed without notice, and after more than a year the funds remain unresolved."
}

R["cfpb_9597602"] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "personal credit card closed a few months after paying a $550.00 annual fee, with no reason given", "is_primary": True},
    {"reason": "fees_and_charges", "specific_reason": "$550.00 annual fee kept by Chase despite closing the account shortly after charging it", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants a partial refund of the $550.00 annual fee after the credit card was closed by the bank",
  "underlying_driver": "the bank closed the account months after charging the annual fee and gave no reason, keeping the full fee",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "credit card closed after fee charged",
      "issue_statement": "The personal credit card was closed a few months after a $550.00 annual fee was charged and paid in full, with no reason given other than 'bank policy.'",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "account closed months after the annual fee was paid, with the bank citing only 'bank policy' and refusing details",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "The Bank charged a $550.00 annual fee for this XXXX XXXX in XX/XX/2023 and XXXX months later closed this account without a reason ... and they kept the full fee!", "speaker": "narrative"},
        {"quote": "All they said was it is Bank Policy and we can not share any additional details.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "annual fee kept after account closure",
      "issue_statement": "Chase kept the full $550.00 annual fee even though the account was closed by the bank only months later.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "unexpected_charge",
      "driver": "$550.00 annual fee retained despite the bank closing the account shortly after collecting it",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Sounds like a dishonest business model.", "speaker": "narrative"},
        {"quote": "and keep the full annual fee?", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $550.00 annual credit card fee was charged and paid in full, then the bank closed the account a few months later without explanation and kept the entire fee."
}

R["cfpb_9903662"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "$7,000.00 wire transfer sent to a fraudulent account after scammers posing as Chase representatives convinced the customer to send it", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p", "checking_or_savings"],
  "services": ["phone_support", "branch"],
  "customer_ask": "stop_or_block",
  "stated_reason": "reporting a $7,000.00 wire sent to a fraudulent account after being tricked by scammers posing as Chase",
  "underlying_driver": "scammers convinced the customer their computer was compromised, then posed as Chase to get a fraudulent wire sent",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "wire transfer to scammer posing as chase",
      "issue_statement": "A scammer impersonating a Chase representative convinced the customer to wire $7,000.00 to a fraudulent account after a fake pending withdrawal alert.",
      "product": "money_transfer_or_p2p",
      "sentiment": -1,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "fraudsters posing as bank staff persuaded the customer to wire $7,000.00 to a fraudulent account at the bank",
      "outcome": "unknown",
      "evidence": [
        {"quote": "I wire transferred $7000.00 to this entity and then determined it was a fraud.", "speaker": "narrative"},
        {"quote": "They continued to call for days, every few hours.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A customer was tricked by scammers impersonating Chase representatives into wiring $7,000.00 to a fraudulent account, and continues seeking help to protect the account."
}

R["cfpb_10231915"] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a deposited check's funds were released then the check bounced, with no warning, leaving the account overdrawn", "is_primary": True},
    {"reason": "unauthorized_or_fraud", "specific_reason": "$2,000.00 Zelle transfer turned out to be fraudulent though the customer made it directly", "is_primary": False}
  ],
  "products": ["checking_or_savings", "money_transfer_or_p2p"],
  "services": ["mobile_app", "phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "reporting an overdraft caused by a bounced check deposit and a separate fraudulent $2,000.00 Zelle transfer",
  "underlying_driver": "funds were released on a check that later bounced without warning, and a Zelle transfer to what turned out to be a fraudulent recipient was never refunded",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "check deposit bounced without warning",
      "issue_statement": "A deposited check's funds were released but the check later bounced, leaving the account overdrawn after no warning it might bounce.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "other_or_unclear",
      "driver": "funds from a deposited check were released then the check bounced with no prior warning, causing an overdraft",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "the funds from a check I deposited earlier were released. However, the check bounced later on.", "speaker": "narrative"},
        {"quote": "I called them at least twice before the funds were released, but they didn't warn me about anything at all, and now my account is overdrawn.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "fraudulent zelle transfer to blocked recipient",
      "issue_statement": "A $2,000.00 Zelle transfer made by the customer turned out to be fraudulent, and the recipient blocked the customer after being asked for a refund.",
      "product": "money_transfer_or_p2p",
      "sentiment": -1,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "$2,000.00 Zelle payment to a fraudulent recipient who then blocked the customer; bank and Zelle uncooperative with the police investigation",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Another issue is with a $2000.00 XXXX transfer on the Chase mobile app, which turned out to be fraudulent, even though I made the transfer.", "speaker": "narrative"},
        {"quote": "I also requested a refund from the recipient 's XXXX account, but later found out that they blocked me.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "An unwarned check bounce left the account overdrawn, and separately a $2,000.00 Zelle transfer turned out to be fraudulent with no cooperation from the bank, Zelle, or police to recover it."
}

R["cfpb_10559810"] = {
  "contact_reasons": [
    {"reason": "credit_reporting", "specific_reason": "an unfamiliar credit card account appeared on the credit report and dropped the score, with no prior notice", "is_primary": True}
  ],
  "products": ["credit_card", "credit_reporting_service"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants an unfamiliar credit card account removed from the credit report and proof that the debt belongs to them",
  "underlying_driver": "an unrecognized account appeared on the credit profile without any prior notice of a debt",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "unknown credit card hurting credit score",
      "issue_statement": "An unfamiliar credit card account was reported on the credit profile without prior notice, dropping the credit score.",
      "product": "credit_reporting_service",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "an unrecognized credit card account was placed on the credit report with no prior notice, causing the score to drop",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "This account was just reported on my credit profile as a credit card belonging to me and caused my score to drop by XXXX points.", "speaker": "narrative"},
        {"quote": "I have also reported this to the credit bureau, but haven't heard back.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "An unfamiliar credit card account appeared on the customer's credit report without notice, lowering their score, and they are asking for proof of the debt and its removal."
}

R["cfpb_10972162"] = {
  "contact_reasons": [
    {"reason": "other_or_unclear", "specific_reason": "demands a settlement amount for an unspecified case with no details given", "is_primary": True}
  ],
  "products": ["other_or_unspecified"],
  "services": [],
  "customer_ask": "other",
  "stated_reason": "demands a settlement for an unspecified case",
  "underlying_driver": "unknown; no details of the underlying dispute are given",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "demand for case settlement",
      "issue_statement": "The customer demands a settlement of an unspecified amount for an unspecified case, without describing what happened.",
      "product": "other_or_unspecified",
      "sentiment": -1,
      "driver_category": "other_or_unclear",
      "driver": "insists on a settlement amount but provides no details of the underlying issue",
      "outcome": "unknown",
      "evidence": [
        {"quote": "CHASE bank I shall settle my case for the sum of XXXX XXXX XXXX dollars and not a penny less.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unknown",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "A heavily redacted complaint demands a settlement amount for an unspecified case against the bank, with no details of the underlying issue."
}

R["cfpb_11265236"] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a $1,700.00 Zelle payment showed as completed on the sender's app but was never received", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"],
  "services": ["mobile_app", "phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wants the missing $1,700.00 Zelle payment located and delivered",
  "underlying_driver": "the Zelle transfer completed on the sender's side but never posted to the recipient's account",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "zelle payment never received",
      "issue_statement": "A $1,700.00 Zelle payment from a friend showed as completed on the sender's app but never appeared on the recipient's account.",
      "product": "money_transfer_or_p2p",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "$1,700.00 Zelle payment marked complete by the sender's bank but never received by the recipient",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "On her mobile app side, it shows the transaction is completed and was accepted on XX/XX/2024 On my side however, the transaction does not show up and I have not recieved the money.", "speaker": "narrative"},
        {"quote": "We have both called customer service numerous of times however no solution/action item has been given.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $1,700.00 Zelle payment showed as sent and completed but was never received, and repeated calls to customer service produced no resolution."
}

R["cfpb_11579435"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a $590.00 dispute over a fraudulent merchant was closed after accepting falsified merchant documents, and the charge was re-billed with interest and late fees", "is_primary": True},
    {"reason": "unauthorized_or_fraud", "specific_reason": "merchant altered shipping information and delivered the package to someone else, confirmed fraudulent by USPS and Chase representatives", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["chat_or_email"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting reversal of a $590.00 fraudulent merchant charge along with related interest and late fees",
  "underlying_driver": "the fraud dispute was closed based on falsified merchant documents despite clear evidence, and the charge was then re-billed with fees",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "fraud dispute denied on falsified merchant documents",
      "issue_statement": "A $590.00 dispute over a merchant that altered shipping details and delivered the package to someone else was closed after Chase accepted the merchant's falsified documents.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "Chase closed the fraud dispute after accepting merchant documents that a Chase rep confirmed were falsified",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase initially closed the case after accepting the merchants falsified documents without properly reviewing the clear evidence I provided", "speaker": "narrative"},
        {"quote": "Verification from Chase representatives that the documents submitted by the merchant were falsified.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "recharged with interest and late fees",
      "issue_statement": "After the dispute was denied, Chase re-billed the $590.00 charge and added interest and late fees.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "unexpected_charge",
      "driver": "$590.00 charge re-billed plus interest and late fees after the fraud dispute was denied",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase has re-billed the $590.00 charge and imposed interest and late fees on my account.", "speaker": "narrative"},
        {"quote": "This has resulted in financial harm, loss of trust, and significant frustration as a consumer.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $590.00 dispute over a fraudulent merchant was closed after Chase accepted documents confirmed to be falsified, the charge was re-billed with interest and late fees, and multiple follow-ups produced no resolution."
}

R["cfpb_12186195"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "an ACH debit payment to a company that never delivered the purchased item, and Chase says it cannot file a claim for ACH debit payments", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants a refund for an ACH debit payment to a company that never delivered the item",
  "underlying_driver": "the bank says it cannot file a claim for ACH debit payments even with a police report and evidence of non-delivery",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "ACH payment to non-delivering merchant",
      "issue_statement": "An ACH debit payment made to a company that never delivered the purchased item was not refunded, and Chase said it cannot file a claim for ACH debit payments.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "Chase refused to open a claim for an ACH debit payment to a company that never delivered the item",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase Bank has failed to help me. This company is a scam company and they insist they delivered the item to me.", "speaker": "narrative"},
        {"quote": "the bank said since it is a ACH debit payment they can not file a claim for me.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "An ACH debit payment to a non-delivering company was never refunded, and the bank says it cannot file a claim for ACH debit transactions despite supporting evidence."
}

R["cfpb_12598165"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a $55,000.00 withdrawal from the account that the customer did not make, followed by account closure, tied to a disputed wire transfer", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "being hung up on twice, transferred repeatedly, and given conflicting information across many calls", "is_primary": False},
    {"reason": "account_opening_or_closure", "specific_reason": "account closed the same day as the unauthorized $55,000.00 withdrawal, described as irreversible", "is_primary": False}
  ],
  "products": ["checking_or_savings", "money_transfer_or_p2p"],
  "services": ["phone_support", "mobile_app"],
  "customer_ask": "explanation",
  "stated_reason": "asking why $55,000.00 was withdrawn from the account without permission and why the account was closed",
  "underlying_driver": "a family member falsely accused the customer of an unauthorized wire transfer, leading Chase to withdraw $55,000.00 and close the account without investigation",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "$55,000 withdrawal customer did not authorize",
      "issue_statement": "A $55,000.00 withdrawal that the customer did not make was taken from the account, and Chase gave several conflicting explanations for it.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "$55,000.00 withdrawn without authorization; Chase alternately said the customer withdrew it, then that Chase itself withdrew it, then that it was sent back",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase withdrew $55000.00 from my account then closed my account the same day without asking me a single question about the wire transfer.", "speaker": "narrative"},
        {"quote": "is unbelievable and unacceptable.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "repeated calls with hang ups and transfers",
      "issue_statement": "Across many calls the customer was repeatedly transferred, put on hold for hours, and hung up on twice by representatives.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "staff_attitude_or_competence",
      "driver": "hung up on twice by representatives and transferred repeatedly across hours of calls with no resolution",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I could not believe how incredibly unprofessional Chase was by hanging up on me 2 times!", "speaker": "narrative"},
        {"quote": "the last time she got back on the line she said, I know your time is valuable have a nice day and hung up on me!", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "account closed without explanation",
      "issue_statement": "The account was closed the same day as the disputed withdrawal, and Chase said the closure is irreversible.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "account closed the same day as the $55,000.00 withdrawal, described by Chase as irreversible with no real explanation",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase also let me know they have now closed my account and it is irreversible.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "An unauthorized $55,000.00 withdrawal tied to a disputed wire led Chase to close the account the same day, after weeks of contradictory answers, hang-ups and repeated transfers with no resolution."
}

R["cfpb_13072690"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a $220.00 Zelle payment intended for a sister was sent to a stranger and neither JPMorgan Chase nor Zelle would treat it as fraud", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"],
  "services": ["mobile_app"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $220.00 misrouted Zelle payment refunded as fraud",
  "underlying_driver": "no recipient verification step let the payment go to the wrong person, and neither the bank nor Zelle would call it fraud",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "zelle payment misrouted to stranger",
      "issue_statement": "A $220.00 Zelle payment meant for the customer's sister went to an unknown recipient because there was no confirmation step, and it was not treated as fraud.",
      "product": "money_transfer_or_p2p",
      "sentiment": -1,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "no verification of the receiving recipient before a $220.00 Zelle payment was misrouted to a stranger; Chase and Zelle both declined to treat it as fraud",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "When I pressed send, the transaction confirmation said sent to XXXX XXXX. I have no idea who this person is and it appears someone accessed my bank account fraudulently.", "speaker": "narrative"},
        {"quote": "They said it's not fraud and there is nothing they can do.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $220.00 Zelle payment intended for a family member was sent to an unknown recipient with no verification, and both the bank and Zelle declined to treat it as fraud or refund it."
}

R["cfpb_13642357"] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a $6,600.00 transfer was rejected because a required phone notification could not be received, even after other verification steps passed", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "felt harshly treated by a representative during an authentication call, describing years of negative treatment by the bank", "is_primary": False}
  ],
  "products": ["checking_or_savings", "money_transfer_or_p2p"],
  "services": ["phone_support"],
  "customer_ask": "escalation_or_complaint",
  "stated_reason": "trying to complete a $6,600.00 transfer that was rejected for lack of phone verification",
  "underlying_driver": "a phone notification needed for verification never arrived, and the customer feels she has been treated unfairly by the bank for years",
  "reason_differs": True,
  "topics": [
    {
      "topic_label": "transfer rejected over notification verification",
      "issue_statement": "A $6,600.00 transfer was rejected because the customer could not receive a required verification notification, despite completing other authentication steps.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "system_or_app_failure",
      "driver": "notification-based verification failed to reach the customer's phone, causing a $6,600.00 transfer to be rejected even after other checks passed",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I do not receive Chase notifications on my phone, she tried that option.", "speaker": "narrative"},
        {"quote": "we are unable to confirm your ownership of the external account with the external bank ''.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "felt harshly treated by representative",
      "issue_statement": "The customer felt treated harshly during the verification call and describes years of unkind treatment by the bank, including during a past mortgage application.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "staff_attitude_or_competence",
      "driver": "described being treated harshly on this call and unkindly during a mortgage application years earlier",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I am really frustrated with Chase Bank.", "speaker": "narrative"},
        {"quote": "I believe the treatment is deliberate at this point due to the defamation of character that has been placed in my file which is totally fabricated.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $6,600.00 transfer was rejected because a verification notification could not be received, and the customer describes feeling harshly and unfairly treated by the bank over several years."
}

R["cfpb_14163301"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a $3,100.00 cruise charge dispute resulted in only a $2,200.00 credit, and the cruise company is now threatening legal action and credit reporting", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "information_or_status",
  "stated_reason": "requesting a copy of Chase's communication with the cruise company to address ongoing collection threats",
  "underlying_driver": "the bank issued a partial credit for the disputed cruise charge, but the merchant is now threatening legal action and credit reporting despite that",
  "reason_differs": True,
  "topics": [
    {
      "topic_label": "partial refund credited for cancelled cruise",
      "issue_statement": "A $3,100.00 cruise charge dispute for a canceled trip due to sudden illness resulted in a $2,200.00 credit, which the customer accepted despite it being lower than the charge.",
      "product": "credit_card",
      "sentiment": 1,
      "driver_category": "fair_outcome",
      "driver": "Chase investigated the dispute and issued a $2,200.00 credit for the $3,100.00 cruise charge, which the customer accepted",
      "outcome": "resolved",
      "evidence": [
        {"quote": "This bank conducted an investigation, and based on their findings, both XXXX and Chase determined the claim was valid. As a result, they issued a credit of $2200.00 to my account.", "speaker": "narrative"},
        {"quote": "I want to establish that Chase handled my original claim promptly and professionally.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "cruise company threatening collection after credit",
      "issue_statement": "The cruise company is now threatening legal action and negative credit reporting despite the dispute credit already issued by Chase.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "other_or_unclear",
      "driver": "a letter threatening legal action and credit bureau reporting arrived from the cruise company after the dispute credit was issued",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I received a letter from XXXX XX/XX/XXXXthreatening legal action and negative reporting to credit bureaus.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": 0,
  "resolution_status": "partially_resolved",
  "positive_moments": [
    {"what": "Chase investigated the dispute and issued a partial credit, handling the claim promptly and professionally", "category": "fair_outcome", "quote": "I want to establish that Chase handled my original claim promptly and professionally.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A cruise cancellation dispute resulted in a $2,200.00 credit against a $3,100.00 charge, and although the customer praises Chase's handling, the cruise company is now threatening legal action and credit reporting."
}

R["cfpb_14757201"] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "checking account closed abruptly with no notice and conflicting explanations for why", "is_primary": True},
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a pending $500.00 check deposit and existing balance withheld after the account closure while stranded out of town", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch", "phone_support"],
  "customer_ask": "explanation",
  "stated_reason": "wants a written explanation for the account closure and the return of withheld funds",
  "underlying_driver": "the account was closed without notice and conflicting reasons were given, and the balance plus a pending $500.00 deposit remain withheld",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "account closed abruptly with conflicting reasons",
      "issue_statement": "The checking account was closed with no prior notice, and different agents gave conflicting stories about whether it was a fraud alert.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "agents gave conflicting explanations - one said no fraud alert, another blamed the fraud department - with no written explanation provided",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I was told verbally multiple stories and none are adding up one agent states it was closed but that there was no fraud alert, the next one said that the fraud department had closed it", "speaker": "narrative"},
        {"quote": "I am currently stranded out of town with my XXXX XXXX XXXX child without access to my own money, and this is causing extreme financial hardship.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "pending deposit and balance withheld",
      "issue_statement": "A pending $500.00 check deposit and the existing account balance are being withheld after the closure, with no timeline for return.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "money_held_or_not_returned",
      "driver": "$500.00 pending deposit and remaining balance withheld with no confirmed timeline to return the funds",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "At the time the account was closed, I had a pending check deposit of $500.00 and Chase is now withholding those funds along with my balance that was available.", "speaker": "narrative"},
        {"quote": "I have no funds for food, lodging, or transportation.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A checking account was closed without notice, agents gave conflicting explanations, and a pending $500.00 deposit plus the remaining balance are being withheld, leaving the customer stranded with a child and no funds."
}

R["cfpb_15401179"] = {
  "contact_reasons": [
    {"reason": "credit_decision_or_limit", "specific_reason": "repeated denial of credit line increases despite years of on-time payments and monthly deposits over $3,900.00", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "explanation",
  "stated_reason": "wants an explanation for repeated credit line increase denials and clarification on how deposits factor into decisions",
  "underlying_driver": "the bank appears not to factor monthly deposits into credit evaluations despite a long history of responsible use",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "credit line increase repeatedly denied",
      "issue_statement": "Credit line increase requests have been repeatedly denied despite six to seven years of timely payments and deposits often exceeding $3,900.00 monthly.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "credit line increases denied every eligible cycle despite a strong payment history and deposits regularly over $3,900.00",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Despite my responsible account management, I have repeatedly been denied credit line increases.", "speaker": "narrative"},
        {"quote": "my requests have not been approved.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A long-standing business credit card customer with a strong payment history has been repeatedly denied credit line increases and wants a clear explanation of how deposits are weighed in the decision."
}

R["cfpb_16078952"] = {
  "contact_reasons": [
    {"reason": "credit_reporting", "specific_reason": "a hard inquiry was placed on the non-owner spouse's credit despite being told there would be none", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "bank managers ignored repeated calls about the incorrect credit check", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["branch", "phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "disputing a hard credit inquiry run on the wrong spouse despite being told there would be no inquiry",
  "underlying_driver": "an employee ran credit on the non-owner spouse for a business card and bank managers ignored follow-up calls about it",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "unauthorized hard inquiry on spouse",
      "issue_statement": "An employee ran a credit check on the non-owner spouse instead of the actual business owner, causing a hard inquiry after being told there wouldn't be one.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "assured there would be no hard inquiry, then a hard inquiry appeared from a credit check run on the wrong person",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I asked before he ran my credit if there would be a hard inquiry and he said no and I checked and there's a hard Inquiry from chase bank.", "speaker": "narrative"},
        {"quote": "So the bank employee ran my credit for the business credit card, not my wife who is actually the owner.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "bank managers ignored complaint",
      "issue_statement": "Bank managers contacted about the incorrect credit check completely ignored the customers.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "no_response_or_follow_up",
      "driver": "all bank managers called about the wrongful credit check ignored the complaint",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "All of the bank managers we called completely ignored us.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "An employee incorrectly ran a hard credit inquiry on the non-owner spouse while opening a business account, contrary to what was promised, and bank managers ignored follow-up calls."
}

R["cfpb_16787202"] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "credit card account closed without notice while the customer was actively making agreed payment-plan payments", "is_primary": True},
    {"reason": "collections_or_debt", "specific_reason": "collections communications continuing despite the alleged breach of the payment plan agreement", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the account reopened or all payment-plan payments refunded after the account was closed without notice",
  "underlying_driver": "the account was closed mid-way through an agreed payment plan with no letter or warning, and collections continued afterward",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "account closed during agreed payment plan",
      "issue_statement": "While making agreed $250.00 biweekly payments under a payment plan, the account was closed without any letter or warning.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "policy_or_terms_change",
      "driver": "$250.00 biweekly payment plan was being honored, yet the account was closed with no notice partway through",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "they apparently closed my account without mu knowledge, no letter.", "speaker": "narrative"},
        {"quote": "I claim that there was a breach of contract and would like all payments I made back or my account reopened", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "collections continuing after closure",
      "issue_statement": "After discovering the closure, the customer ordered the collections department to cease all communications and warned of legal escalation.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "staff_attitude_or_competence",
      "driver": "collections continued to pursue the account after it was closed without notice, prompting a cease-and-desist demand",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I canceled the rest of my payments and ordered their collections department to CEASE AND DESIST all communications and warned them that if they decide to file a lawsuit, I will file complaints against their attorneys to the Indiana Supreme Court Judicial Disciplinary Commission and would go after their law licenses.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "Chase offered a payment plan to keep the account open during a period of lost income", "category": "fair_outcome", "quote": "they offered me a payment plan to pay them $250.00 every two weeks to keep the account open", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A credit card account was closed without notice while the customer was honoring an agreed payment plan after a wrongful arrest caused income loss, and the customer is now threatening legal escalation over the breach."
}

R["cfpb_17360856"] = {
  "contact_reasons": [
    {"reason": "credit_reporting", "specific_reason": "a hard inquiry appeared for a credit card the customer never applied for, and JP Morgan gave conflicting information about notifying credit bureaus", "is_primary": True}
  ],
  "products": ["credit_card", "credit_reporting_service"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wants the unauthorized credit inquiry corrected and the resulting credit score drop resolved",
  "underlying_driver": "JP Morgan did not properly notify the credit bureaus about the fraud after an inquiry the customer never made, dropping the credit score",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "unauthorized inquiry and conflicting bureau claims",
      "issue_statement": "A credit inquiry appeared for a card the customer never applied for, and JP Morgan claimed it notified the credit bureaus but the bureaus say they received nothing.",
      "product": "credit_reporting_service",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "JP Morgan said it sent fraud notices to the bureaus, but when contacted the bureaus said they received nothing, and score dropped as a result",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "immediately I call JP Morgan ( Chase bank ) and I told them that I never ask for any credit cards", "speaker": "narrative"},
        {"quote": "when I contacted these companies they told me that they do not receive nothing from JP Morgan", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "An unauthorized credit inquiry for a card the customer never applied for dropped their score, and JP Morgan's claim of notifying the credit bureaus turned out to be false, leaving the issue unresolved."
}

R["cfpb_18359253"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a $6,500.00 dispute over a moving company that never rendered services was denied despite evidence of merchant misrepresentation", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting a proper second-level review and credit for a $6,500.00 moving service dispute",
  "underlying_driver": "the moving company never rendered services or issued a Bill of Lading, and admitted internal misrepresentation, yet the dispute was denied",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "denied dispute over non-rendered moving services",
      "issue_statement": "A $6,500.00 dispute over a moving company that never issued a Bill of Lading or confirmed a carrier was denied despite evidence the merchant admitted internal misrepresentation.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "dispute denied even after new evidence showed the merchant admitted to suspending a coordinator for giving customers incorrect information and never issuing a Bill of Lading",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "My initial dispute was denied despite clear evidence of merchant misrepresentation.", "speaker": "narrative"},
        {"quote": "my credit card issuer initially denied the dispute without adequately addressing the evidence of misrepresentation and services not rendered.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $6,500.00 dispute over a moving company that never rendered services was denied twice despite new evidence of merchant misrepresentation, and the customer is requesting a proper second-level review."
}

R["cfpb_18889894"] = {
  "contact_reasons": [
    {"reason": "customer_service_experience", "specific_reason": "branch tellers refused a coin deposit and offered no alternative assistance beyond suggesting an outside machine", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch"],
  "customer_ask": "other",
  "stated_reason": "wanted to deposit coins along with cash at the branch",
  "underlying_driver": "the branch's coin machine was reportedly broken and coin deposits were limited to business customers, so the customer was turned away",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "coin deposit refused at branch",
      "issue_statement": "Branch tellers refused to accept a coin deposit unless the customer was a business client and said their coin counting machine was broken, offering no other help.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "other_or_unclear",
      "driver": "coin deposit refused because the branch's counting machine was broken and coin deposits are limited to business clients, with no alternative offered in-branch",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "The tellers claimed they do not accept coin deposits unless the customer is a business client, and they claimed their coin counting machine was broken.", "speaker": "narrative"},
        {"quote": "Then I was turned away with no further assistance.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A long-time customer was turned away at the branch when trying to deposit coins because the coin counting machine was reportedly broken and coin deposits were limited to business clients."
}

R["cfpb_20490470"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "an $870.00 charge for unauthorized tires was disputed as fraud but Chase rejected it saying the customer benefited from the service, then blocked further review", "is_primary": True},
    {"reason": "unauthorized_or_fraud", "specific_reason": "a mechanic added tires outside the approved insurance estimate without consent or prior invoice", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "disputing an $870.00 charge for unauthorized tires that Chase denied as fraud and then blocked from further billing dispute",
  "underlying_driver": "a repair shop added tires outside the approved estimate and billed for them nearly two years later, and Chase's fraud review blocked a proper billing dispute",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "unauthorized tire charge disputed and denied",
      "issue_statement": "An $870.00 charge for tires added without authorization or invoice was disputed as fraud, but Chase rejected it saying the customer 'received and benefited from the service,' then blocked a separate billing dispute.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "$870.00 unauthorized tire charge rejected as fraud dispute, then declared ineligible for a billing dispute despite being a distinct legal claim under the FCBA",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "When I called XXXX, their agent could not identify the source of the charge and advised me to dispute it as fraud.", "speaker": "narrative"},
        {"quote": "On XX/XX/XXXX, Chase rejected the dispute, stating I \" received and benefited from the service. ''", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "unauthorized tires added by repair shop",
      "issue_statement": "A repair shop added brand new tires without prior knowledge or consent outside the insurance-approved estimate, and charged $870.00 for them nearly two years later with no invoice or notice.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "unexpected_charge",
      "driver": "tires added outside the approved repair estimate and charged $870.00 almost two years later with no prior invoice, call, or email",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "XXXX added brand new tires without my prior knowledge or consent outside of the agreed scope of repairs.", "speaker": "narrative"},
        {"quote": "I received no prior invoice, no phone call, no email, and no letter before the charge was made.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "An $870.00 charge for tires added without authorization during a car repair was denied as a fraud dispute, and Chase then blocked a separate billing dispute despite it being a distinct legal claim."
}

R["cfpb_21470894"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a mailed tax check was stolen and used to write a fraudulent check, followed by numerous additional fraudulent ACH debits and checks draining the account", "is_primary": True},
    {"reason": "dispute_or_chargeback", "specific_reason": "Chase says only some of the fraudulent ACH debits may be recoverable while the fraudulent checks cashed will not be reimbursed", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "reporting extensive fraudulent ACH debits and checks that drained a rarely used checking account",
  "underlying_driver": "a stolen mailed check led to fraud that was initially resolved, but many more fraudulent transactions went unnoticed for months and some losses will not be recovered",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "stolen mailed check used for fraud",
      "issue_statement": "A check mailed to pay taxes was stolen and used to write a fraudulent check, which was refunded, but the customer later found many more fraudulent transactions had drained the account.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "a stolen mailed check led to a fraudulent check that was refunded, but additional fraudulent ACH debits and checks went unnoticed for months",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "The check was stolen from the mail and used to write a fraudulent check, which I noticed immediately and canceled with Chase.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "fraudulent checks cashed will not be recovered",
      "issue_statement": "Chase told the customer that while some fraudulent ACH debit losses may be recovered, none of the fraudulent checks that were cashed will be reimbursed.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "the check fraud department said none of the cashed fraudulent checks would be recovered, unlike some of the ACH debit losses",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "the check fraud department said I would not recover any of the fraudulent checks cashed out", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "Chase refunded the initial fraudulent check right away", "category": "fast_resolution", "quote": "They refunded me the initial lost check money and said the problem was solved, so I moved on.", "speaker": "narrative"}
  ],
  "redaction_heavy": True,
  "summary": "A stolen mailed check led to an initial fraud that Chase refunded, but months of additional fraudulent ACH debits and checks drained the account, with the bank saying not all losses, particularly the cashed checks, will be recovered."
}

# verify quotes and coverage
missing = set(texts) - set(R)
extra = set(R) - set(texts)
print("missing:", missing)
print("extra:", extra)

bad = []
for call_id, resp in R.items():
    text = texts[call_id]
    for t in resp["topics"]:
        for ev in t["evidence"]:
            if ev["quote"] not in text:
                bad.append((call_id, ev["quote"]))
    for pm in resp.get("positive_moments", []):
        if pm["quote"] not in text:
            bad.append((call_id, pm["quote"]))

if bad:
    print("BAD QUOTES:")
    for cid, q in bad:
        print(" ", cid, "::", repr(q))
else:
    print("ALL QUOTES OK")

out = pathlib.Path("data/cache/extract")
out.mkdir(parents=True, exist_ok=True)
count = 0
for call_id, resp in R.items():
    payload = {
        "key": keys[call_id], "prompt_version": "ext-1.0",
        "schema_version": "1", "taxonomy_version": "1", "call_id": call_id,
        "model": "claude-agent-build", "produced_by": "claude_agent",
        "created_at": "2026-09-11T12:00:00Z", "usage": None,
        "response": resp
    }
    (out / f"{call_id}.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    count += 1
print("wrote", count)
