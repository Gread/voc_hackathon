# -*- coding: utf-8 -*-
import json, pathlib

bundle = json.load(open("data/work/extract_bundles/bundle_103.json", encoding="utf-8"))
texts = {r["call_id"]: r["text"] for r in bundle["records"]}
keys = {r["call_id"]: r["cache_key"] for r in bundle["records"]}

records = {}

records["cfpb_14681712"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a bank account was fraudulently opened using the customer's identity without any knowledge or authorization", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": [], "customer_ask": "stop_or_block",
  "stated_reason": "requesting Chase investigate and permanently close a fraudulent bank account opened in his name without authorization",
  "underlying_driver": "identity theft resulted in an unauthorized account being opened at Chase using the customer's personal information",
  "reason_differs": False,
  "topics": [
    {"topic_label": "fraudulent account opened without authorization",
     "issue_statement": "A bank account was fraudulently opened at Chase using the customer's name, Social Security number, or other personal information, without his knowledge or consent.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "identity theft led to an unauthorized account opened under the customer's name and personal information",
     "outcome": "unknown",
     "evidence": [
       {"quote": "a bank account was fraudulently opened in my name at Chase Bank without my knowledge or authorization.", "speaker": "narrative"},
       {"quote": "This is a clear case of identity theft, and I am requesting that Chase Bank immediately investigate and permanently close any accounts that were opened using my name, Social Security number, or other personal information without my consent.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unknown", "positive_moments": [], "redaction_heavy": False,
  "summary": "The customer reports that a bank account was fraudulently opened at Chase using stolen personal information and requests investigation, closure, and written confirmation of removal."
}

records["cfpb_15332178"] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "branch refused a refinance payoff check for not matching the exact current balance, causing double interest", "is_primary": True}
  ],
  "products": ["credit_card"], "services": ["branch"], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants compensation for the extra interest incurred because the branch refused to accept a refinance payoff check that didn't match the exact current balance",
  "underlying_driver": "the branch would only accept a check for the exact balance amount, even though the balance had grown slightly due to a 3-month processing delay, so the payoff check was rejected and interest continued accruing on both loans",
  "reason_differs": False,
  "topics": [
    {"topic_label": "branch refused payoff check not matching exact balance",
     "issue_statement": "A refinance payoff check for about $11,000.00 was rejected because the current balance had grown slightly during a 3-month delay, and the branch would only accept a check for the exact amount, unlike online payments of varying amounts.",
     "product": "credit_card", "sentiment": -1, "driver_category": "policy_or_terms_change",
     "driver": "branch would only accept an exact-amount check for payoff, rejecting the refi check because it no longer matched to the penny after a 3-month delay, unlike online payments of varying amounts",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The local branch said they could only accept a check for the exact amount. Both the teller and manager confirmed.", "speaker": "narrative"},
       {"quote": "I said I make payments of different amounts all the time through online banking without issue. They had no explanation other than to say sorry, cant help you.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A refinance payoff check for about $11,000.00 was rejected at the branch because it no longer matched the balance to the penny after a processing delay, leaving the customer paying interest on the same amount to two lenders at once."
}

records["cfpb_15980098"] = {
  "contact_reasons": [
    {"reason": "terms_information_or_communication", "specific_reason": "branch requires a utility bill for proof of address that the wife cannot provide since only one name may appear on shared utility accounts", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["branch"], "customer_ask": "information_or_status",
  "stated_reason": "requesting to add his wife as a joint account holder, but the branch's utility-bill proof-of-address requirement can't be met since only one name may appear on their utility accounts",
  "underlying_driver": "the branch requires a utility bill for proof of address, but the wife cannot be listed on the shared utility account, so alternative documentation is needed",
  "reason_differs": False,
  "topics": [
    {"topic_label": "utility bill requirement blocks adding joint holder",
     "issue_statement": "The branch requires a utility bill to prove the wife's address, but utility companies only allow one account holder's name, so she cannot provide one to be added as a joint account holder.",
     "product": "checking_or_savings", "sentiment": 0, "driver_category": "policy_or_terms_change",
     "driver": "utility-bill-only proof-of-address policy blocks adding a joint holder whose name can't legally appear on the shared utility bill",
     "outcome": "unknown",
     "evidence": [
       {"quote": "The branch has requested a utility bill as proof of address. However, all utility accounts for our residence are solely under my name, and the utility companies do not allow more than XXXX account holders name to appear on the bills.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": 0, "resolution_status": "unknown", "positive_moments": [], "redaction_heavy": False,
  "summary": "A customer seeking to add his wife as a joint account holder is blocked by a utility-bill proof-of-address requirement she cannot meet, since only one name can appear on their shared utility bills."
}

records["cfpb_16693859"] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "account closed abruptly after a fraud report and unlock, with no information given", "is_primary": True},
    {"reason": "payment_or_transfer_problem", "specific_reason": "rent payments returned twice on a stop-payment the customer never requested", "is_primary": False}
  ],
  "products": ["checking_or_savings"], "services": ["branch", "phone_support"], "customer_ask": "fix_error",
  "stated_reason": "wants access to account funds to pay rent after the account was closed without warning or explanation",
  "underlying_driver": "after reporting fraud and having the account unlocked, a text warned the account could be closed, and it was closed before the customer could get an explanation; rent payments were also returned twice on a stop-payment she never requested",
  "reason_differs": False,
  "topics": [
    {"topic_label": "account closed abruptly after fraud report",
     "issue_statement": "After reporting fraud and having the account unlocked, the customer received a text warning of possible closure, then found the account already closed with no information given when she called.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "account closed right after a fraud unlock, with no information given when the customer called back",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I reported fraud on account and they unlocked my account, then I got another text saying if I didnt call my accould could be closed I called after receiving text and my account was already closed and no information could be given??", "speaker": "narrative"}
     ]},
    {"topic_label": "rent returned on unrequested stop-payment",
     "issue_statement": "Rent payments were returned twice, with Chase claiming someone told them to stop payment even though the customer never requested a stop-payment on either transaction.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "rent returned twice on a claimed stop-payment instruction the customer never gave",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Rent was returned and for two months first time they said XXXX had told them to stop payment, I did not stop rent payment twice and XXXX payments returned??", "speaker": "narrative"}
     ]},
    {"topic_label": "no check or balance letter received",
     "issue_statement": "The branch said a letter and the account balance would be sent as a check, but neither has arrived, and the customer urgently needs the funds to pay rent.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned",
     "driver": "promised letter and balance check never arrived, leaving funds needed for rent inaccessible",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I went into bank and they could not help me o tell me anything said a letter and my balance would be sent in the form of a check. No check or letter??", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "After reporting fraud and having her account unlocked, a 30-year Chase customer's account was closed with no explanation, rent payments were returned twice on a stop-payment she never gave, and a promised balance check never arrived."
}

records["cfpb_17278646"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a Social Security check deposit was garnished, causing automated payments to be declined with no legal notice provided", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": [], "customer_ask": "explanation",
  "stated_reason": "reporting that Social Security funds were garnished without the required legal notice, causing automated payments to fail",
  "underlying_driver": "the SSA check deposit, which should be protected from garnishment, was withheld or garnished without proper legal notice, causing automatic payments to be returned",
  "reason_differs": False,
  "topics": [
    {"topic_label": "SSA check garnished without legal notice",
     "issue_statement": "A federal SSA check deposit was apparently garnished with no legal notice provided, causing automated transactions to be returned negatively for 7 days.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned",
     "driver": "SSA check deposit garnished with no legal notice, and automated payments returned negatively for 7 days",
     "outcome": "unknown",
     "evidence": [
       {"quote": "After 7 days of non payment and no Legal letter support for the Federal SSA Check being Garnished, which according to Social Security was deposited ok.", "speaker": "narrative"},
       {"quote": "All of my automated transactions were presented against my Checking account as Negatively and a letter was only provided to all items paid Negatively.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unknown", "positive_moments": [], "redaction_heavy": False,
  "summary": "A Social Security check deposit at Chase was apparently garnished without legal notice, causing automated payments to be returned negatively for a week, which the customer suspects is not an isolated incident."
}

records["cfpb_18279062"] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "a newly approved credit card was closed about a week later, citing dispute activity tied to a different, unrelated Chase account", "is_primary": True},
    {"reason": "credit_reporting", "specific_reason": "requesting correction of credit bureau reporting that inaccurately suggests adverse behavior on the closed account", "is_primary": False}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "fix_error",
  "stated_reason": "requesting a formal review and correction of how the closed account is reported to credit bureaus",
  "underlying_driver": "Chase closed a newly approved card citing dispute activity from a different, older account that predated the approval, and this is now inaccurately reflected in credit reporting",
  "reason_differs": False,
  "topics": [
    {"topic_label": "new card closed over unrelated prior disputes",
     "issue_statement": "A credit card approved with a $25,000.00 limit was closed about a week later, with Chase citing dispute activity that actually belonged to a different, previously closed Chase account.",
     "product": "credit_card", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "account closed within a week of approval over dispute history from a separate, unrelated Chase account that Chase already knew about when it approved this card",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase stated that the closure was related to dispute activity. However, the disputes referenced occurred several months prior and were associated with a different Chase credit card account, not the XXXX XXXX credit card that was approved and subsequently closed.", "speaker": "narrative"}
     ]},
    {"topic_label": "inaccurate credit bureau reporting from closure",
     "issue_statement": "The closure is now reflected in credit bureau reporting in a way that inaccurately suggests adverse behavior that never occurred on this specific account.",
     "product": "credit_card", "sentiment": -1, "driver_category": "error_not_corrected",
     "driver": "credit bureau reporting suggests adverse behavior based on a closure reason unrelated to this account's actual payment history",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I am concerned that the current credit bureau reporting inaccurately suggests adverse consumer behavior that did not occur and compounds prior harm unrelated to this accounts actual history.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A newly approved $25,000.00 credit card was closed a week later over dispute activity that actually belonged to a separate, unrelated Chase account, and the closure is now inaccurately reflected in credit bureau reporting."
}

records["cfpb_18803575"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a wire to a company later revealed as running a Ponzi scheme was not stopped by the bank's due diligence", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"], "services": [], "customer_ask": "explanation",
  "stated_reason": "reporting that a wire transfer to a company later revealed to be a Ponzi scheme was not stopped by the bank, and repeated emails have gone unanswered",
  "underlying_driver": "the receiving company was later charged with running a Ponzi scheme, and the bank did not perform due diligence to stop or reject the transfer, then ignored the customer's follow-up emails",
  "reason_differs": False,
  "topics": [
    {"topic_label": "wire to a ponzi scheme not stopped",
     "issue_statement": "A wire transfer was sent to a company that later turned out to be running a Ponzi scheme and is now under administration, and the bank did not perform due diligence to stop or reject the transaction.",
     "product": "money_transfer_or_p2p", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "wire to a company later revealed as a Ponzi scheme under administration was not stopped or rejected by the bank's due diligence",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The Bank didn't do due diligence to stop and reject the transaction.", "speaker": "narrative"}
     ]},
    {"topic_label": "no response to repeated emails",
     "issue_statement": "The customer emailed the bank many times about the fraudulent transfer and received no reply.",
     "product": "money_transfer_or_p2p", "sentiment": -1, "driver_category": "no_response_or_follow_up",
     "driver": "multiple emails sent about the issue went entirely unanswered",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I emailed them many times about this fact and no one replied to me.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A wire transfer to a company later revealed as running a Ponzi scheme was not stopped by the bank's due diligence, and repeated follow-up emails have gone unanswered."
}

records["cfpb_20299031"] = {
  "contact_reasons": [
    {"reason": "loan_servicing", "specific_reason": "requested hardship assistance on a past-due auto loan due to increased childcare costs, and was denied", "is_primary": True}
  ],
  "products": ["auto_loan"], "services": ["phone_support"], "customer_ask": "other",
  "stated_reason": "requesting hardship assistance on an auto loan that is a couple of months past due due to increased childcare costs",
  "underlying_driver": "after explaining a temporary financial hardship and an upcoming move that would free up funds, the customer was placed on hold for a long time and then denied any hardship assistance, risking repossession",
  "reason_differs": False,
  "topics": [
    {"topic_label": "hardship assistance denied on past-due auto loan",
     "issue_statement": "After falling behind on the auto loan due to rising childcare costs and explaining plans to move and resume full payments, the customer was placed on hold for 35-45 minutes and then denied any hardship assistance, risking repossession.",
     "product": "auto_loan", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "after a 35-45 minute hold and detailed explanation of hardship and an upcoming income improvement, hardship assistance was denied, risking repossession with 52 payments already made",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I was placed on hold for approximately 3545 minutes. When the representative returned, I was informed that I was not approved for any hardship assistance.", "speaker": "narrative"},
       {"quote": "As a result, I am now two months behind and approaching a third month past due, putting me at risk of repossession of a vehicle I have paid significantly toward.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "After falling behind on an auto loan due to rising childcare costs, Chase denied hardship assistance following a 35-45 minute hold, putting the customer at risk of repossession despite 52 prior payments."
}

records["cfpb_21418641"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "12 unauthorized ATM withdrawals totaling $5,000.00 made with the correct PIN while the debit card was reported lost, claim denied twice", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["atm", "phone_support"], "customer_ask": "refund_or_reversal",
  "stated_reason": "disputing $5,000.00 in unauthorized ATM withdrawals made using the correct PIN during a period the card was reported lost",
  "underlying_driver": "Chase denied the fraud claim twice because the transactions used the correct PIN, refused to review its own ATM footage, and told the customer her only recourse is a police-subpoenaed video review",
  "reason_differs": False,
  "topics": [
    {"topic_label": "denied fraud claim for pin-based atm withdrawals",
     "issue_statement": "Twelve ATM withdrawals totaling $5,000.00 were made with the correct PIN during a period the debit card was reported lost, but Chase denied the fraud claim twice and refused to check its own ATM footage.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "$5,000.00 in ATM withdrawals with the correct PIN denied twice, with Chase refusing to review its own footage and telling the customer to get a police subpoena instead",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I have spoken to Chase several times, with my claim being denied twice and had a manager call me back and inform me myonly recourse is to file a police report and have the police subpoena the videos", "speaker": "narrative"},
       {"quote": "Chase said they will not reference any ATM footage to prove it was not me, or someone I gave my information to.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Twelve unauthorized ATM withdrawals totaling $5,000.00 were made with the correct PIN while the debit card was reported lost, but Chase denied the fraud claim twice and refused to review its own ATM footage, leaving the customer to pursue a police subpoena."
}

records["cfpb_22643248"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "8 months trying to get Chase to reverse fraudulent merchant charges despite zero-liability terms", "is_primary": True}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants Chase to reverse fraudulent charges to the merchant and credit the account, per its own zero-liability terms",
  "underlying_driver": "a merchant fraudulently charged the credit card, and despite 8 months of effort and the card's zero-liability terms, Chase has not reversed the charges",
  "reason_differs": False,
  "topics": [
    {"topic_label": "8 months without reversal of fraudulent charges",
     "issue_statement": "A merchant fraudulently charged the credit card for $740.00 and $120.00, and after 8 months Chase still has not reversed the charges despite its own zero-liability terms.",
     "product": "credit_card", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "8 months without reversal of fraudulent merchant charges despite the card's zero-liability policy",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "for the last 8 months I have tried to get Chase to reverse it.", "speaker": "narrative"},
       {"quote": "According to their own terms of service on the card, I am not liable for these fraudulent charges.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A merchant fraudulently charged the credit card $740.00 and $120.00, and despite 8 months of effort and the card's zero-liability terms, Chase has not reversed the charges."
}

records["cfpb_23433773"] = {
  "contact_reasons": [
    {"reason": "terms_information_or_communication", "specific_reason": "minor son's flight excluded from the Sapphire Reserve trip cancellation/interruption benefit after a medical emergency abroad", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "months of no response clarifying what the travel insurance benefit covers", "is_primary": False}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "seeking full reimbursement under the Sapphire Reserve trip cancellation/interruption benefit for a medical emergency abroad, including the minor son's flight",
  "underlying_driver": "after a medical emergency required an emergency evacuation, the insurer refused to cover the minor son's flight though the parents' tickets were covered, and gave no clear answer on what is covered despite the benefit's advertised terms",
  "reason_differs": False,
  "topics": [
    {"topic_label": "son's flight excluded from trip cancellation coverage",
     "issue_statement": "After a medical emergency abroad required emergency evacuation and trip cancellation, the parents' flights were covered under the Sapphire Reserve benefit but the minor son's flight was not.",
     "product": "credit_card", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "minor son's flight excluded from the covered trip cancellation/interruption benefit even though policy required him to travel with the family and his cost should have been reimbursed",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "My husband and my ticket was covered under Chase Sapphire Reserve XXXX XXXX XXXX and XXXX but they informed us that our sons flight we needed to pay upfront and that the Trip Cancellation and Interruption would cover the cost of his ticket.", "speaker": "narrative"},
       {"quote": "They will not cover my son 's flight when I had to emergency evacuated to come home.", "speaker": "narrative"}
     ]},
    {"topic_label": "months of unresponsive claims handling",
     "issue_statement": "After filing the claim, it took several months to recover only a small portion, and the credit card company and insurer refuse to respond to emails or clarify what is covered.",
     "product": "credit_card", "sentiment": -1, "driver_category": "no_response_or_follow_up",
     "driver": "months after filing, only a small portion was recovered and the insurer won't respond to emails or clarify coverage",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "We filed our claims in XX/XX/year> and after XXXX  months, we have only been able to recover only a small portion.", "speaker": "narrative"},
       {"quote": "The credit card company and insurance company that provides this service refuses to respond to emails or clarify what was covered versus not covered.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "partially_resolved", "positive_moments": [], "redaction_heavy": True,
  "summary": "A medical emergency abroad triggered a Sapphire Reserve trip cancellation claim; the parents' flights were covered but the minor son's flight was not, and months later the insurer still has not clarified coverage or paid the remainder."
}

records["cfpb_9562090"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "an unauthorized $500.00 transaction posted on a new credit card that had been locked and frozen", "is_primary": True}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "disputing an unauthorized $500.00 charge that posted despite the new card being locked and frozen",
  "underlying_driver": "even though the replacement card was locked and frozen after the original was stolen, a $500.00 unauthorized charge still posted",
  "reason_differs": False,
  "topics": [
    {"topic_label": "unauthorized charge despite locked card",
     "issue_statement": "Even though the new replacement card was locked and frozen after the original was stolen, an unauthorized $500.00 transaction still posted to the account.",
     "product": "credit_card", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "a $500.00 unauthorized transaction posted despite the card being locked and frozen",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I had the new card locked and frozen so no charges can be applied to the new or old card.", "speaker": "narrative"},
       {"quote": "I was notified of an unauthorized transaction of $500.00 on my card today", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Despite locking and freezing a replacement credit card after the original was stolen, an unauthorized $500.00 transaction still posted, and the customer has filed a fraud dispute."
}

records["cfpb_9849029"] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a wire sent to a Chase account was not returned after the account was closed just before the funds arrived", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the wired funds returned since the destination account was closed right before the transfer arrived",
  "underlying_driver": "the wire arrived at a Chase account that had just been closed, and the funds have still not been returned months later",
  "reason_differs": False,
  "topics": [
    {"topic_label": "wire not returned after account closed",
     "issue_statement": "A wire transfer was sent to a Chase account that was closed just before the funds arrived, and the money still has not been returned.",
     "product": "money_transfer_or_p2p", "sentiment": -1, "driver_category": "money_held_or_not_returned",
     "driver": "wire funds not returned since the receiving account was closed right before the transfer landed",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Account was closed just before the $ was sent It is now XX/XX/XXXX and they still have not returned the XXXX", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": True,
  "summary": "A wire transfer sent to a Chase account that had just been closed has still not been returned months later."
}

records["cfpb_10191236"] = {
  "contact_reasons": [
    {"reason": "loan_servicing", "specific_reason": "demanding disclosure of who owns the mortgage debt and an explanation of escrow payment discrepancies", "is_primary": True},
    {"reason": "balance_or_statement_error", "specific_reason": "escrow payments of $190.00 don't match the $130.00/$91.00 shown on billing and escrow review statements, with no refund of the overpayment", "is_primary": False}
  ],
  "products": ["mortgage"], "services": [], "customer_ask": "explanation",
  "stated_reason": "demanding TILA-required disclosure of the true creditor/owner of the mortgage debt and documentation authenticating all charges",
  "underlying_driver": "conflicting claims about who owns the mortgage note, combined with escrow payment amounts that don't match billing statements, have left the customer unable to verify what she owes or to whom",
  "reason_differs": False,
  "topics": [
    {"topic_label": "conflicting claims about who owns the mortgage debt",
     "issue_statement": "Conflicting statements from a creditor's lawyer about who owns the mortgage note, including an allegedly forged assignment, have left it unclear who the mortgage is actually owed to.",
     "product": "mortgage", "sentiment": -2, "driver_category": "incorrect_or_conflicting_information",
     "driver": "a lawyer's shifting statements about which entity owns the note, plus a disputed assignment of mortgage, leave the true creditor unverified",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "here are OTHER investors who own the Note XXXX owns part of the Note, JP Morgan Chase owns part of the Note", "speaker": "narrative"},
       {"quote": "attached forged, fabricated Assignment of Mortgage dated XX/XX/XXXX", "speaker": "narrative"}
     ]},
    {"topic_label": "escrow payments dont match billing statements",
     "issue_statement": "The customer has been paying $190.00 per month for escrow, but her billing statement shows $91.00 and a separate escrow review shows $130.00, with no refund of the resulting overpayment.",
     "product": "mortgage", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "escrow charged at $190.00/month while statements show $91.00 or $130.00, with no refund of the surplus despite RESPA requiring one",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "during all time in question [ including last month ] I paid $190.00 for escrow, not $130.00 as appear on billing statement and not $91.00 as stated in escrow review", "speaker": "narrative"},
       {"quote": "Pursuant to RESPA, all escrow surplus must be immediately returned to me. It never happened.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": True,
  "summary": "Conflicting claims about who actually owns the mortgage note, plus escrow payments of $190.00 that don't match billing statements showing $91.00 or $130.00, have left the customer demanding full documentation of the debt and a refund of the escrow overpayment."
}

records["cfpb_10503661"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "company continued honoring new charges on a voided, fraud-replaced card account and refused to guarantee against further charges", "is_primary": True}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "stop_or_block",
  "stated_reason": "wants the company to remove a charge made to the voided card account and guarantee no further charges will be honored on it",
  "underlying_driver": "after fraud voided the card and issued a new one, the company kept honoring new charges to the voided account, including one from a non-recurring merchant, and refused to stop or guarantee against future charges",
  "reason_differs": False,
  "topics": [
    {"topic_label": "charges still honored on voided fraud account",
     "issue_statement": "After the card was voided and reissued due to fraud, the company continued honoring new charges to the voided account, including one from a merchant with no recurring-charge setup, and refused to remove it or guarantee no further charges.",
     "product": "credit_card", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "a new charge was honored on a voided, fraud-replaced account from a non-recurring merchant, and the company refused to remove it or guarantee against future charges",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Subsequent to this, the company is honoring charges made to the voided account ending in XXXX.", "speaker": "narrative"},
       {"quote": "I called the company to get them to remove the charge under the voided account and guarantee to me that no further charges would be honored made to the voided account. they refused to do both of these things.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "After a card was voided and reissued due to fraud, the company kept honoring new charges on the voided account and refused to remove one or guarantee against further charges."
}

records["cfpb_10923071"] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "unable to access promised sign-up bonus points and a companion ticket despite meeting all the spending requirements", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "at least six calls with transfers, disconnections, and contradictory instructions between Chase and British Airways with no resolution", "is_primary": False}
  ],
  "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "fix_error",
  "stated_reason": "wants access to the promised sign-up bonus points and companion ticket after meeting all spending requirements on the British Airways Visa card",
  "underlying_driver": "Chase and British Airways could not link the accounts or resolve the discrepancy despite many calls, transfers, and supervisor escalations over several months, forcing the customer to pay for flights out of pocket",
  "reason_differs": False,
  "topics": [
    {"topic_label": "promised bonus points and companion ticket inaccessible",
     "issue_statement": "After spending over $30,000.00 on the card as required, the customer could not access the promised sign-up bonus points or the companion ticket despite meeting all advertised criteria.",
     "product": "credit_card", "sentiment": -2, "driver_category": "no_response_or_follow_up",
     "driver": "over $30,000.00 spent to earn the bonus points and companion ticket, but neither could be accessed despite meeting all criteria",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "IN BRIEF WE HAVE NOT BEEN ABLE TO ACCESS THESE POINTS WHATSOEVER DESPITE MEETING ALL ADVERTISED CRITERIA AND DESPITE MANY MANY EFFORTS AS DETAILED BELOW.", "speaker": "narrative"},
       {"quote": "We met all criteria to earn those XXXX points plus the companion ticket, having used the card for substantially more than $30000.00 and being up to date on all required payments throughout.", "speaker": "narrative"}
     ]},
    {"topic_label": "repeated calls and transfers with no resolution",
     "issue_statement": "Over roughly six calls to Chase and multiple calls to British Airways, involving long holds, disconnected calls, and contradictory instructions, no supervisor was able to resolve the account linking issue.",
     "product": "credit_card", "sentiment": -2, "driver_category": "no_response_or_follow_up",
     "driver": "six-plus calls with escalations, disconnections, and contradictory instructions between Chase and British Airways over months with no fix",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I call Chase again ( this is my 6th call to them ). Start from scratch with phone tree and explaining the situation.", "speaker": "narrative"},
       {"quote": "She then tries to connect me to someone at British Airways. The call then gets disconnected. She asks me to call them back. I ask if they can call me back and she says no, they can only receive and can not make calls.", "speaker": "narrative"}
     ]},
    {"topic_label": "paid out of pocket after unresolved reward issue",
     "issue_statement": "Unable to resolve the points issue in time, the customer ended up paying out of pocket for flights for his wife and daughter to join the trip.",
     "product": "credit_card", "sentiment": -1, "driver_category": "money_held_or_not_returned",
     "driver": "paid out of pocket for family flights because the promised points could not be resolved before the trip",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I ultimately paid out of pocket for my daughter and wife to join me on my trip to the XXXX. We flew XXXX XXXX and the tickets were about $1000.00 each", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Despite spending over $30,000.00 to meet the requirements for a British Airways Visa sign-up bonus and companion ticket, the customer could not access either after six-plus calls with Chase and British Airways full of disconnections and contradictory instructions, and ended up paying out of pocket for family flights."
}

records["cfpb_11222783"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "account hacked with multiple unauthorized transfers, and Chase would not close the account or release funds when asked in person twice", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["branch"], "customer_ask": "stop_or_block",
  "stated_reason": "trying to close the hacked joint account and release its funds after multiple unauthorized transfers",
  "underlying_driver": "after the account was hacked and money moved out multiple ways, Chase refused two in-person requests to close it and said nothing could be done until the following Monday",
  "reason_differs": False,
  "topics": [
    {"topic_label": "unable to close hacked account or release funds",
     "issue_statement": "After the account was hacked and money was transferred out multiple times, Chase refused two in-person requests to close the joint account and said nothing could be done until Monday.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "denied_or_declined_without_explanation",
     "driver": "two in-person requests to close the hacked account were denied, and Chase said nothing could be done until Monday while refusing to release funds",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "She went in face to face on Monday and Wednesday ( we both went Wednesday ) to try to close it and were still told no.", "speaker": "narrative"},
       {"quote": "They are now telling us they cant do anything until Monday.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "After a joint account was hacked and funds moved out multiple ways, Chase refused two in-person requests to close the account or release funds, saying nothing could be done until Monday."
}

records["cfpb_11549387"] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a $220.00 payment made to a closed account was never returned despite being told it would come back", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $220.00 payment returned after it was sent to a closed account",
  "underlying_driver": "Chase first said the payment to a closed account would be returned, but after waiting and following up, the customer was redirected to the other bank, which wouldn't provide information, and the funds were never received",
  "reason_differs": False,
  "topics": [
    {"topic_label": "$220 payment to closed account never returned",
     "issue_statement": "A payment sent to a closed account was initially said by Chase to be coming back, but after follow-up the customer was told to contact the other bank instead, and the $220.00 was never returned.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned",
     "driver": "Chase first promised the $220.00 payment would return, then redirected the customer to the other bank, which gave no information, and the funds were never received",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase first informed me that the charge would come back to my account. I waited a couple of days, and I never received the funds.", "speaker": "narrative"},
       {"quote": "I never received my funds of $220.00 back.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A $220.00 payment sent to a closed account was initially said to be returning to the customer, but after being redirected to the other bank for information, the funds were never received."
}

records["cfpb_12137512"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a $2,100.00 fraud claim was denied for months before finally being refunded", "is_primary": True},
    {"reason": "account_opening_or_closure", "specific_reason": "account closed after the customer was frustrated with employees and sent a demand letter threatening legal action", "is_primary": False}
  ],
  "products": ["checking_or_savings"], "services": ["branch", "phone_support"], "customer_ask": "explanation",
  "stated_reason": "disputing a $2,100.00 fraud claim that was denied for months before being refunded, and questioning why the account was then closed",
  "underlying_driver": "after finally getting the fraud claim paid, the account was closed citing rudeness to employees, which the customer believes was retaliation for sending a demand letter and threatening legal action",
  "reason_differs": True,
  "topics": [
    {"topic_label": "fraud claim denied for months before refund",
     "issue_statement": "A $2,100.00 fraud claim was denied for months before Chase finally returned the money, and the customer never received the legally required written explanation for the initial denial.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "long_wait_or_delay",
     "driver": "$2,100.00 fraud claim denied for months before being paid, with no written explanation for the denial as required by law",
     "outcome": "resolved",
     "evidence": [
       {"quote": "After XXXX XXXX months denying my fraud claim on my previous claim of $2100.00 and not returning our money, they did finally give the money back.", "speaker": "narrative"},
       {"quote": "other than the first claim denial NEVER got a written explanation of why it was denied as is required by law in state regulatory codes.", "speaker": "narrative"}
     ]},
    {"topic_label": "account closed after demand letter and frustration",
     "issue_statement": "The customer's account was closed for being 'rude to employees,' which she believes was retaliation for sending a demand letter to executives and threatening legal action after months of unhelpful, dismissive service.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "staff_attitude_or_competence",
     "driver": "account closed citing rudeness after the customer sent a demand letter and threatened legal action following months of dismissive, unhelpful service including a canceled in-person appointment",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I received a letter saying they were closing our account because I was rude to employees.", "speaker": "narrative"},
       {"quote": "I believe the real reason for closing my account was that I had the temerity to send a demand letter to XXXX executives with Chase and threaten further legal actions.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "partially_resolved",
  "positive_moments": [
    {"what": "the fraud claim money was eventually returned", "category": "fair_outcome",
     "quote": "they did finally give the money back.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A $2,100.00 fraud claim was denied for months before being refunded, and the customer's account was then closed for being 'rude,' which she believes was retaliation for threatening legal action over the bank's handling of the claim."
}

records["cfpb_12545281"] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "both new checking and safe banking accounts closed abruptly right after activating the second debit card, with no good reason given", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["mobile_app", "phone_support"], "customer_ask": "explanation",
  "stated_reason": "trying to find out why both newly opened accounts were suddenly closed and Chase said it would no longer do business with him",
  "underlying_driver": "shortly after activating the debit card for a newly opened safe banking account, the app logged the customer out for suspicious activity and both accounts were closed with no reason given",
  "reason_differs": False,
  "topics": [
    {"topic_label": "both new accounts closed without explanation",
     "issue_statement": "Shortly after activating the debit card for a newly opened safe banking account, the app flagged suspicious activity and logged the customer out, and both new accounts were closed with Chase saying only that it would no longer do business with him.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "both new accounts closed right after activating the second debit card, with Chase saying only that it would no longer do business with him and no real explanation given",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "my Chase app wasnt working and was logged out for suspicious activity and called to see what had happened for my accounts to be closed all I got was that they were closed and that chase will no longer do business with me", "speaker": "narrative"},
       {"quote": "still no good reason as to why they were closed.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Shortly after opening two new Chase accounts and activating the second debit card, the app flagged suspicious activity and both accounts were closed with no real explanation, other than Chase saying it would no longer do business with him."
}

records["cfpb_13037974"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "Chase ignored a court order to release garnished funds and instead transferred the entire balance to the garnishing party", "is_primary": True},
    {"reason": "fees_and_charges", "specific_reason": "an unauthorized $100.00 legal processing fee and multiple overdraft fees resulted from the mishandled garnishment, most never reversed", "is_primary": False}
  ],
  "products": ["checking_or_savings"], "services": ["phone_support", "branch"], "customer_ask": "refund_or_reversal",
  "stated_reason": "demanding Chase comply with the court order, reverse the resulting fees, and pay for the financial harm caused",
  "underlying_driver": "Chase transferred the entire garnished balance to the opposing party instead of following the court's order to release the remainder, then charged an unauthorized fee and multiple overdraft fees, and later closed the account",
  "reason_differs": False,
  "topics": [
    {"topic_label": "court order to release funds ignored",
     "issue_statement": "A court order instructed Chase to remit $250.00 to the plaintiff's counsel and release the remaining balance to the customer, but Chase instead transferred the entire balance to the garnishing party.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned",
     "driver": "entire garnished balance transferred to the opposing party despite a court order to release the remainder to the customer",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The court order instructed Chase Bank to ( 1 ) remit $250.00 to Plaintiff 's counsel and ( 2 ) immediately release the remaining balance to me. Instead, XXXX unlawfully transferred the entire balance to the garnishing party, ignoring the directive to release the remaining funds to me.", "speaker": "narrative"}
     ]},
    {"topic_label": "unauthorized fee and unreversed overdraft charges",
     "issue_statement": "Chase imposed an unauthorized $100.00 legal processing fee and multiple overdraft charges caused by its own mishandling of the garnishment, and only one overdraft charge was ever removed.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "unexpected_charge",
     "driver": "an unauthorized $100.00 legal processing fee plus overdraft charges from the bank's own garnishment mishandling, with only one overdraft fee removed",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "In addition to this unlawful transfer, XXXX imposed an unauthorized $100.00 legal processing fee despite the procedural failure.", "speaker": "narrative"},
       {"quote": "After finally reaching a XXXX representative, only XXXX overdraft charges were removed. However, the majority of overdraft charges were not addressed", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase ignored a court order to release garnished funds, transferring the entire balance to the opposing party, then charged an unauthorized $100.00 fee and multiple overdraft charges from its own mishandling, most of which were never reversed, before closing the account."
}

records["cfpb_13565373"] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "requesting the bank match a new, higher sign-up bonus offered on the same credit card product after an involuntary upgrade raised the annual fee", "is_primary": True}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "other",
  "stated_reason": "requesting Chase match the current, much higher opening bonus for the same card product he was automatically upgraded into at a higher annual fee",
  "underlying_driver": "after an involuntary product upgrade raised the annual fee, Chase began offering the identical card to new applicants with a much larger sign-up bonus at the same fee",
  "reason_differs": False,
  "topics": [
    {"topic_label": "requesting bonus match for identical upgraded product",
     "issue_statement": "After being automatically upgraded to a card with a higher annual fee, the customer discovered Chase now offers the identical product to new applicants with a much larger opening bonus at the same annual fee, and is requesting a match.",
     "product": "credit_card", "sentiment": 0, "driver_category": "other_or_unclear",
     "driver": "identical card now offered to new customers with a far larger sign-up bonus at the same annual fee as the customer's involuntarily upgraded card",
     "outcome": "unknown",
     "evidence": [
       {"quote": "It is absolutely not fair for certain customers to receive XXXX fewer miles at the same annual cost for the same credit card product.", "speaker": "narrative"},
       {"quote": "I would greatly appreciate it if you would consider matching your current promotion - an open bonus of XXXX miles, for my card.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": 0, "resolution_status": "unknown", "positive_moments": [], "redaction_heavy": True,
  "summary": "After an involuntary product upgrade raised his annual fee, the customer found Chase now offers the identical card to new applicants with a far larger sign-up bonus at the same fee, and is requesting a match."
}

records["cfpb_14088230"] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "account wrongfully closed over alleged 'abuse of disputes' while disputes were still unresolved", "is_primary": True},
    {"reason": "dispute_or_chargeback", "specific_reason": "disputes ignored or lost despite repeated documentation submissions, with contradictory statements about what was received", "is_primary": False},
    {"reason": "fees_and_charges", "specific_reason": "late fee and interest charge imposed as a result of the improper closure", "is_primary": False}
  ],
  "products": ["credit_card"], "services": ["online_banking", "phone_support", "chat_or_email"], "customer_ask": "refund_or_reversal",
  "stated_reason": "demanding disputes be reopened, fees reversed, a written explanation for the closure, and compliance with the Fair Credit Billing Act",
  "underlying_driver": "Chase repeatedly gave contradictory information about documentation and disputes, then closed the account for alleged dispute abuse, leaving the customer with unreversed late fees and interest",
  "reason_differs": False,
  "topics": [
    {"topic_label": "account closed over alleged dispute abuse",
     "issue_statement": "The account was closed for alleged 'abuse of the dispute process' while five disputes (two $100.00 and three $50.00) were still unresolved and Chase gave contradictory statements about receiving documentation.",
     "product": "credit_card", "sentiment": -2, "driver_category": "denied_or_declined_without_explanation",
     "driver": "account closed for alleged dispute abuse despite the customer submitting documentation multiple times and Chase's own contradictory claims about what it received",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "My account was closed prematurely for alleged \" abuse of disputes, '' though I acted in good faith with valid claims under the Fair Credit Billing Act.", "speaker": "narrative"},
       {"quote": "Chase has processed two $100.00 disputes but claims to have no record of the three $50.00 disputes, even though all disputes were listed in the same documentation submitted repeatedly.", "speaker": "narrative"}
     ]},
    {"topic_label": "documentation repeatedly lost or ignored",
     "issue_statement": "Chase claimed it never received documentation the customer uploaded multiple times, and agents hung up or gave contradictory reasons for the dispute status.",
     "product": "credit_card", "sentiment": -2, "driver_category": "incorrect_or_conflicting_information",
     "driver": "documentation uploaded three times was claimed as never received, and agents gave contradictory reasons including that disputes were never initiated and the account was closed for abuse",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I've had two agents hang up on me, and another tell me to call back despite having proper documentation for my dispute with them.", "speaker": "narrative"},
       {"quote": "Now thanks to these disputes, Chase has stated over the phone several things : 1 ) That they didn't even initiate the disputes 2 ) There was no documentation 3 ) That the account was closed due to activity indicating abuse", "speaker": "narrative"}
     ]},
    {"topic_label": "late fee and interest from improper closure",
     "issue_statement": "Because the account was closed, the customer was unable to make payments, resulting in a $28.00 late fee and a $2.00 interest charge that she says Chase caused and must reverse.",
     "product": "credit_card", "sentiment": -1, "driver_category": "unexpected_charge",
     "driver": "$28.00 late fee and $2.00 interest charge resulted from being unable to pay after the improper account closure",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Due to the closure, Ive been unable to make payments, resulting in : A $28.00 late fee ( XX/XX/year> ) $2.00 interest charge ( XX/XX/year> )", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase closed an account over alleged dispute abuse while five disputes were still unresolved and repeatedly gave contradictory statements about lost documentation, leaving a $28.00 late fee and $2.00 interest charge the customer says must be reversed."
}

records["cfpb_14682088"] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "auto pay to a merchant was rejected, blamed on a zip+4 mismatch, causing a delinquent utility bill", "is_primary": True}
  ],
  "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "explanation",
  "stated_reason": "wants to know why a long-standing auto pay was suddenly rejected, causing the utility bill to go delinquent",
  "underlying_driver": "after years of no issues, the same auto pay was rejected over a mismatched extended zip code, which the agent called a 'security enhancement' that customers were never notified about",
  "reason_differs": False,
  "topics": [
    {"topic_label": "auto pay rejected over unnotified zip+4 mismatch",
     "issue_statement": "An auto pay that had worked without issue for years was rejected, and after escalation the agent attributed it to a mismatched extended zip code called a 'security enhancement' that customers were never told about.",
     "product": "credit_card", "sentiment": -1, "driver_category": "policy_or_terms_change",
     "driver": "auto pay rejected over a zip+4 mismatch on an unannounced 'security enhancement,' despite years of the same card, merchant, and account working fine",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "She agreed that it was \" NOT due to insufficient funds ''.", "speaker": "narrative"},
       {"quote": "The Chase agent stated \" that it's a security enhancement ''.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A long-standing auto pay was suddenly rejected over a mismatched extended zip code that Chase called a 'security enhancement' never disclosed to customers, leaving a utility bill delinquent."
}

records["cfpb_15327644"] = {
  "contact_reasons": [
    {"reason": "credit_reporting", "specific_reason": "unauthorized accounts from identity theft that credit furnishers won't remove despite required documentation", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "unable to reach a live agent at the credit furnishers by phone", "is_primary": False}
  ],
  "products": ["credit_reporting_service"], "services": ["phone_support"], "customer_ask": "stop_or_block",
  "stated_reason": "requesting unauthorized accounts opened through identity theft be blocked or removed from her credit file",
  "underlying_driver": "credit furnishers make it impossible to reach a live person, and despite submitting required documentation to block the fraudulent accounts, they have not removed them",
  "reason_differs": False,
  "topics": [
    {"topic_label": "unauthorized accounts not removed despite documentation",
     "issue_statement": "Several accounts not authorized by the customer, the result of identity theft, have not been removed by the credit furnishers despite required blocking documentation being submitted.",
     "product": "credit_reporting_service", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "unauthorized accounts from identity theft remain on file even after submitting the required documentation to block them",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "These accounts listed are not authorized by me.", "speaker": "narrative"},
       {"quote": "Since these creditors would not remove the fraudulent accounts I have requested the XXXX files for these charged off accounts for tax purposes with the XXXX.", "speaker": "narrative"}
     ]},
    {"topic_label": "unable to reach a live agent",
     "issue_statement": "The phone numbers provided by the credit furnishers make it impossible to reach an actual live agent to discuss the disputed accounts.",
     "product": "credit_reporting_service", "sentiment": -1, "driver_category": "other_or_unclear",
     "driver": "no way to reach a live agent using the phone numbers listed on the furnishers' websites",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "You can not speak to a live agent with the phone number provided on their website.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Accounts opened through identity theft remain on the customer's credit file despite submitting required blocking documentation, and the credit furnishers' phone lines make it impossible to reach a live agent."
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
