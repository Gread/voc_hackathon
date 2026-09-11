import json, pathlib

bundle = json.load(open('data/work/extract_bundles/bundle_101.json', encoding='utf-8'))
texts = {r['call_id']: r['text'] for r in bundle['records']}
keys = {r['call_id']: r['cache_key'] for r in bundle['records']}

R = {}

R['cfpb_12537516'] = {
  "contact_reasons": [
    {"reason": "other_or_unclear", "specific_reason": "several credit card accounts were closed after instructions to debit a collateral deposit account were allegedly not carried out, framed through an unconventional legal theory of creditor status", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "other",
  "stated_reason": "claims to be the actual creditor who funded the accounts and accuses Chase of fraudulent misrepresentation and misappropriation",
  "underlying_driver": "instructions to offset an account balance from a named collateral deposit account were allegedly not carried out, leading to several credit card accounts being closed",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "credit card accounts closed after offset dispute",
      "issue_statement": "Several credit card accounts were closed after instructions to debit and offset a balance from a named collateral deposit account were allegedly not followed.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "other_or_unclear",
      "driver": "instructions to offset the balance from a named collateral account were allegedly not carried out, resulting in the closure of several credit card accounts",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "this was not done, causing a restraint of trade as each of the XXXX credit card accounts were closed", "speaker": "narrative"},
        {"quote": "Chase Bank has fraudulently misrepresented themselves as a lender and has breached a fiduciary duty", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "Several credit card accounts were closed after instructions to offset a balance from a named collateral deposit account were allegedly not followed, framed as fraudulent misrepresentation by the bank."
}

R['cfpb_13033931'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "fraudulent casino transactions overdrew the account, and Chase reversed the credited deposits from the scam but denied refunding the funds taken out", "is_primary": True},
    {"reason": "account_opening_or_closure", "specific_reason": "the account is being closed shortly after the customer filed a complaint, which feels retaliatory", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the funds taken from the account during the fraud refunded",
  "underlying_driver": "Chase reversed the fraudulent deposits, which put the account negative, but denied refunding the money that was actually withdrawn, and is now closing the account after a complaint was filed",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "account closed and fraud refund denied after complaint",
      "issue_statement": "After fraudulent casino transactions overdrew the account, Chase reversed the credited deposits but denied refunding the money taken out, and is now closing the account shortly after a complaint was filed.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "Chase reversed the fraudulent deposits, leaving the account negative, but denied refunding the funds that were actually withdrawn during the same fraud",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "NOW THEY ARE CLOSONG MY ACCOUNT BECAUSE I FILED A COMPLAINT AND NOT REFUNDING MY MONEY!!!!!", "speaker": "narrative"},
        {"quote": "Chase approved the credits that were deposited in my account so they saw it was fraud, this made my account go negative but they denied the funds that were taken out of my account?", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "After fraudulent casino transactions overdrew the account, Chase reversed the credited fraud deposits but denied refunding the money actually taken, and is now closing the account shortly after a complaint was filed."
}

R['cfpb_13566407'] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a $920.00 ATM cash deposit malfunctioned and never posted, and a temporary credit issued for it was later reversed and never restored despite months of escalation", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "multiple departments repeatedly said nothing could be found and passed the case around for months with no real investigation", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["atm", "branch", "phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $920.00 stuck in a malfunctioning ATM credited back",
  "underlying_driver": "an ATM malfunctioned mid-deposit and never returned the cash or posted the funds, a temporary credit was reversed a month later, and months of escalation across multiple departments produced no investigation or resolution",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "atm malfunction credit reversed with no resolution",
      "issue_statement": "A $920.00 ATM deposit malfunctioned mid-transaction and never posted or returned, and a temporary credit issued for it was reversed a month later with no further resolution after many months of escalation.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "money_held_or_not_returned",
      "driver": "the ATM malfunctioned and kept the cash, a temporary credit was reversed a month later, and months of repeated escalation across departments produced no investigation findings or resolution",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "this caused the ATM to give me a transaction error, then printed out a receipt which I have proof of and told me to make sure my deposit did go through which it did not and my money didn't come back out to me!", "speaker": "narrative"},
        {"quote": "this whole situation was taking a huge toll on my mental health and I all I could do when I thought of it was cry out of frustration", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "a branch manager returning from leave personally escalated the claim again after hearing the situation", "category": "helpful_staff", "quote": "she told me she had only been back in office for one month because she was on pregnancy leave and that she would help me try to get my money back", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A $920.00 ATM cash deposit malfunctioned and was never returned, a temporary credit issued for it was reversed a month later, and months of escalation across branches, claims and fraud departments produced no investigation results, taking a serious toll on the customer's wellbeing."
}

R['cfpb_14060033'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "Chase approved disputes for five months of an ongoing defective recruiting service but denied the first month's charge and setup fee solely due to a time-limit rule", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the initial $1400.00 charge and $1400.00 setup fee reversed as part of the same ongoing defective service already proven in later disputes",
  "underlying_driver": "Chase successfully refunded five months of charges proving the vendor's service failure, but mechanically applied a time-limit rule to deny the first month's charge from the same continuous defective service",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "first month's charge denied on a time-limit technicality",
      "issue_statement": "Chase refunded five months of charges for a defective recruiting service but denied the first month's $1400.00 charge and $1400.00 setup fee solely due to a mechanically applied time-limit rule.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "a time-limit rule was applied mechanically to deny the first month's charge, ignoring that it was part of the same continuous defective service already proven in five successfully disputed months",
      "outcome": "partially_resolved",
      "evidence": [
        {"quote": "the bank denied the first month 's charge of $1400.00 + $1400.00 setup fee, citing the 118-day rule", "speaker": "narrative"},
        {"quote": "The initial charge was part of the same faulty service as the later, successfully disputed charges.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "partially_resolved",
  "positive_moments": [
    {"what": "Chase successfully refunded five months of charges after the customer proved the vendor's ongoing failure", "category": "fair_outcome", "quote": "I successfully disputed 5 months of charges ( $5600.00 refunded ) proving the Vendor 's failure.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "Chase refunded five months of charges for a defective recruiting service but denied the first month's charge and setup fee, totaling $2800.00, solely because of a mechanically applied time-limit rule."
}

R['cfpb_14679444'] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "an unauthorized second points transfer was processed alongside the one authorized transfer, and a later separate error deduction left the rewards account negative for months", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wants the unauthorized transfer's points retrieved and the negative balance corrected",
  "underlying_driver": "Chase processed two transfers when only the third and final one was authorized, and then deducted additional points for an unrelated error, leaving the rewards account negative and unusable for months",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "unauthorized extra points transfer left balance negative",
      "issue_statement": "Chase processed both a second, unauthorized points transfer and the one authorized transfer, then deducted more points for an unrelated error, leaving the account negative and unusable for months.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "an unauthorized second transfer combined with a separate unexplained deduction left the points balance negative, and Chase has not resolved it despite admitting the investigation was incomplete",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "We later discovered that Chase had processed both the second and third transferstotaling XXXX pointseven though only XXXX transfer was intended and authorized.", "speaker": "narrative"},
        {"quote": "Chase now claims they are waiting to retrieve points from the airline, despite the fact that both transfers were initiated by Chase, and only XXXX was authorized.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "Chase processed an unauthorized second points transfer alongside the authorized one, then deducted more points for an unrelated error, leaving the rewards account negative and unusable for months without resolution."
}

R['cfpb_15328434'] = {
  "contact_reasons": [
    {"reason": "customer_service_experience", "specific_reason": "a promised $410.00 baggage fee reimbursement has repeatedly missed multiple committed delivery dates despite documentation and a formal complaint already filed", "is_primary": True},
    {"reason": "rewards_or_promotions", "specific_reason": "referral bonus points for two approved friend referrals were never credited despite the advertised program terms", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the promised $410.00 baggage reimbursement issued and the missing referral bonus points credited",
  "underlying_driver": "after its own booking mistake caused extra baggage costs, Chase promised reimbursement and then missed three separate committed delivery dates, while a separately promised referral bonus for two approved referrals was also never paid",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "baggage reimbursement missed three promised dates",
      "issue_statement": "After a booking mistake forced extra baggage fees, a promised $410.00 reimbursement check has missed three separate committed delivery dates despite documentation and a formal complaint.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "no_response_or_follow_up",
      "driver": "reimbursement for a booking mistake was promised by three separate dates, none of which were met, despite clear documentation and an already-filed complaint",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase XXXX has repeatedly promised delivery of a reimbursement check ( first by XX/XX/XXXX, then XX/XX/XXXX, then XX/XX/XXXX ), but I still have not received the payment.", "speaker": "narrative"},
        {"quote": "Chase XXXX has failed to provide the promised reimbursement despite clear documentation, repeated assurances, and a formal complaint already filed.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "referral bonus points never credited",
      "issue_statement": "Referral bonus points for two approved friend referrals through the customer's link were never credited despite the advertised program terms.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "two approved referrals should have earned the advertised bonus points, but they were never credited despite contacting Chase",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase advertises a referral bonus of XXXX points per approved referral. However, I never received the XXXX points that I am entitled to.", "speaker": "narrative"},
        {"quote": "Despite contacting Chase XXXX, the issue remains unresolved.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $410.00 baggage fee reimbursement caused by Chase's own booking mistake has missed three separate promised delivery dates, and referral bonus points for two approved referrals were also never credited."
}

R['cfpb_15979032'] = {
  "contact_reasons": [
    {"reason": "access_or_digital_banking", "specific_reason": "a transaction to the wrong person went through automatically while the debit card was locked, and Chase said it processed based on prior transaction history", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["mobile_app"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the misdirected transaction refunded since it should have been declined while the card was locked",
  "underlying_driver": "a transaction sent to the wrong person by mistake went through despite the debit card being locked, because Chase says it automatically approved based on previous transactions",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "misdirected transaction processed despite locked card",
      "issue_statement": "A transaction sent to the wrong person went through automatically even though the debit card was locked, because Chase said it processed based on previous transaction patterns.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "system_or_app_failure",
      "driver": "a transaction was allowed through automatically based on prior transaction history even though the card was locked and should have blocked it",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I was told due to previous transactions it automatically went through.", "speaker": "narrative"},
        {"quote": "That is unacceptable and should not have taken place while my card was locked", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A misdirected payment went through automatically despite the debit card being locked, because Chase says it approved the transaction based on prior transaction history."
}

R['cfpb_16708722'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a scammer convinced the customer to send $4000.00 in daily transfers, and Chase refused to help beyond confirming the customer authorized the transfers themselves", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"],
  "services": ["mobile_app"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants help recovering the $4000.00 sent to the scammer",
  "underlying_driver": "a scammer had the customer send $4000.00 in daily transfers to an account with traceable real-name information, but Chase refused to take further action beyond confirming the transfers were self-authorized, and sent no fraud alerts despite the unusual daily pattern",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "scam transfers dismissed as self-authorized",
      "issue_statement": "A scammer had the customer send $4000.00 in daily transfers to a traceable account, and Chase refused to take further action beyond confirming the transfers were self-authorized, without sending any fraud alerts.",
      "product": "money_transfer_or_p2p",
      "sentiment": -1,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "Chase refused to act further after verifying the transfers were self-authorized, and sent no alerts despite the daily pattern, though other suspicious activity had previously been blocked",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "They initially told me that I had authorized the transfer myself and therefore couldn't process it.", "speaker": "narrative"},
        {"quote": "Other suspected fraudulent activity during my time using this account was blocked by Chase.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A scammer had the customer send $4000.00 in daily transfers to a traceable account, and Chase refused further action beyond confirming the transfers were self-authorized, despite sending no fraud alerts even though it had blocked other suspicious activity before."
}

R['cfpb_17283857'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "Chase took back a $42.00 goodwill credit from a rental company and denied the overbilling dispute using documentation the customer says was fabricated by the merchant", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $42.00 credit restored and the overbilling dispute resolved in his favor",
  "underlying_driver": "the rental company admitted its billing mistakes and issued a $42.00 credit, but after it stopped responding, Chase took that credit back and denied the dispute using billing figures the customer says are inconsistent with the original quote",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "goodwill credit reclaimed using disputed documentation",
      "issue_statement": "After the rental company admitted its billing mistakes and credited $42.00, Chase took that credit back and denied the overbilling dispute using documentation the customer says was fabricated after the fact.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase reclaimed a merchant-issued goodwill credit and denied the dispute using billing figures the customer says are inconsistent with the originally agreed quote and receipts",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase took the $42.00 credit that I had received from XXXX without any explanation. This was clearly a theft of funds by Chase.", "speaker": "narrative"},
        {"quote": "Chase has clearly engaged in criminal acts of fraud to aid the business with the billing dispute and theft of funds in taking the original credit to my account.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "the rental company itself admitted its mistakes and issued a $42.00 credit before going unresponsive", "category": "fair_outcome", "quote": "XXXX admitted in writing that they made multiple mistakes, credited $42.00 to my Chase credit card account", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "After a rental company admitted billing mistakes and credited $42.00, Chase reclaimed that credit and denied the overbilling dispute using documentation the customer says was fabricated after the fact."
}

R['cfpb_18277565'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "an earlier counterfeit check attempt was misclassified as a system glitch instead of fraud, letting two more counterfeit checks totaling $1200.00 post the next day", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "overnight fraud phone lines and the chatbot's suggested numbers were all closed, preventing a timely warning before the counterfeit checks posted", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support", "branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants immediate provisional credit for the $1200.00 in counterfeit checks while the investigation continues",
  "underlying_driver": "an initial counterfeit check attempt was misclassified as a glitch rather than fraud, so no protective action was taken, and two more counterfeit checks then posted the next day while overnight support lines were unreachable",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "counterfeit checks followed misclassified glitch",
      "issue_statement": "An earlier counterfeit check attempt was misclassified as a system glitch instead of fraud, so no protective action was taken, allowing two more counterfeit checks totaling $1200.00 to post the next day.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "the first counterfeit attempt was treated as a glitch rather than fraud, so no check block or account protection was applied before two more counterfeit checks posted",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "The agent told us it was only an algorithm/system error and reversed it as a glitch rather than treating it as check fraud.", "speaker": "narrative"},
        {"quote": "The supervisor refused, stating Chase does not provide provisional credit for check fraud.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "overnight fraud lines unreachable",
      "issue_statement": "The debit card's stated after-hours fraud number and the chatbot's suggested alternatives were all closed overnight, preventing a timely warning before the counterfeit checks posted.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "system_or_app_failure",
      "driver": "the stated after-hours fraud assistance number and the chatbot's alternative numbers were all closed, preventing any timely report before the checks posted",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "when we attempted to call during the overnight period to prevent posting, the phone lines were closed", "speaker": "narrative"},
        {"quote": "We also used the Chase chatbot, which directed us to call multiple numbers presented as XXXX assistance ; those numbers were also closed.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "the branch helped open a new account and file the fraud disputes", "category": "helpful_staff", "quote": "The branch helped open a new account and file disputes", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "An initial counterfeit check attempt was misclassified as a system glitch instead of fraud, allowing two more counterfeit checks totaling $1200.00 to post the next day, and overnight fraud phone lines were entirely unreachable to give timely warning."
}

R['cfpb_18742949'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "over $4300.00 in ATM withdrawals made while the customer's debit card remained in her possession and she was far away were denied as familiar, self-authorized activity", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["atm"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $4300.00 in fraudulent ATM withdrawals reversed",
  "underlying_driver": "Chase denied the fraud claim saying the transactions looked familiar and someone with PIN knowledge may have made them, despite the customer's card never leaving her possession and being far from the withdrawal locations",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "fraud claim denied as familiar activity",
      "issue_statement": "Over $4300.00 in ATM withdrawals made while the debit card was in the customer's possession and she was far from the locations were denied as familiar, self-authorized activity.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "the claim was denied as familiar or PIN-known activity despite the card never leaving the customer's possession and her being far from the withdrawal locations",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "My claim was denied on the basis that the transactions appeared familiar and that I or someone with knowledge of my PIN may have made them.", "speaker": "narrative"},
        {"quote": "I did not authorize these withdrawals, did not share my PIN with anyone, and was not physically present in the area where the transactions took place.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Over $4300.00 in ATM withdrawals made while the debit card was in the customer's possession and she was far from the location were denied as familiar, self-authorized activity."
}

R['cfpb_20284740'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "$1000.00 in unauthorized Apple Pay debit transactions reported immediately have still not been credited back", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["mobile_app"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "requests reopening the investigation and issuing a provisional credit for the $1000.00 while it is completed",
  "underlying_driver": "despite immediately reporting the unauthorized Apple Pay transactions and getting a replacement card, the $1000.00 has not been credited back under Regulation E protections",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "unreimbursed unauthorized apple pay charges",
      "issue_statement": "$1000.00 in unauthorized Apple Pay debit transactions were reported immediately, and Chase confirmed the card was compromised, but the funds have still not been credited back.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "money_held_or_not_returned",
      "driver": "despite prompt reporting and confirmation the transactions went through an unauthorized Apple Pay wallet, the $1000.00 has not been credited back under Regulation E",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "despite reporting the fraud promptly, the $1000.00 has not been credited back to my account", "speaker": "narrative"},
        {"quote": "i this matter can not be resolved promptly, I will pursue further action through the Consumer Financia rotection Bureau and other regulatory authorities", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "Chase canceled the debit card and issued a replacement after the fraud was reported", "category": "fast_resolution", "quote": "Chase canceled m lebit card and issued a replacement card, confirming that the transactions were conducted throug Apple Pay.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "$1000.00 in unauthorized Apple Pay debit transactions were reported immediately and the card replaced, but the funds have still not been credited back, prompting a threat to escalate to regulators."
}

R['cfpb_21395694'] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "an advertised miles redemption benefit for eligible airline ticket purchases was refused even though multiple representatives confirmed the purchase met every eligibility criterion", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wants the advertised miles redemption applied to the eligible ticket purchase as confirmed by multiple representatives",
  "underlying_driver": "multiple Chase representatives and a supervisor confirmed the purchase met every criterion for the advertised miles redemption, and the airline confirmed the ticket coded correctly, yet Chase ultimately closed the case and refused to apply the miles",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "confirmed-eligible miles redemption still refused",
      "issue_statement": "Multiple Chase representatives and a supervisor confirmed the ticket purchase met every criterion for the advertised miles redemption benefit, yet the case was closed and the miles were never applied.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "representatives and a supervisor agreed the charges were eligible and the airline confirmed correct ticket coding, but Chase still closed the case and refused to apply the advertised miles benefit",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "The supervisor I spoke with agreed that these are eligible charges and the issue may be on XXXXXX/XX/XXXX side.", "speaker": "narrative"},
        {"quote": "I received a response that unfortunately Chase was not going to apply my miles as advertised.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Multiple Chase representatives and a supervisor confirmed an airline ticket purchase met every criterion for an advertised miles redemption benefit, yet Chase closed the case and refused to apply the miles anyway."
}

R['cfpb_22637530'] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "a business account was closed without a clear explanation, and the linked phone number remains restricted from being used with a similar service at another bank", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "stop_or_block",
  "stated_reason": "requests review and release of the phone number restriction so it can be used at another institution",
  "underlying_driver": "after closing the business account without explanation, Chase continues restricting the customer's phone number in a shared verification system, blocking its use at another bank",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "phone number restricted after unexplained closure",
      "issue_statement": "After closing the business account without a clear explanation, Chase's continued restriction of the customer's phone number is preventing its use with a similar payment service at another bank.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "the phone number restriction tied to the closed Chase account was never lifted, blocking its use with a similar service elsewhere",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase closed my business account without providing a clear explanation, and now my personal phone number remains restricted from being used with XXXX at another institution.", "speaker": "narrative"},
        {"quote": "continuing to restrict my phone number after account closure is causing financial inconvenience", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "After closing a business account without a clear explanation, Chase's continued restriction of the customer's phone number is blocking its use with a similar payment service at another bank."
}

R['cfpb_23354026'] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "was told she is ineligible to open a new account after previously holding a $250000.00 business savings balance with Chase, following unresolved employee theft and identity theft reports", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch"],
  "customer_ask": "explanation",
  "stated_reason": "wants to know if negative reporting from unresolved identity theft or account misuse claims is affecting the bank's decision not to do business with her",
  "underlying_driver": "despite previously holding hundreds of thousands of dollars with Chase, being told she is now ineligible after reporting employee theft and dealing with ongoing identity theft leaves her wanting disclosure of what information is being used against her",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "denied new account after unresolved theft reports",
      "issue_statement": "After previously holding a $250000.00 business savings balance and reporting employee theft, the customer was told she is no longer eligible to bank with Chase, without disclosure of the reason.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "no explanation was given for the ineligibility determination despite a prior high-value relationship and multiple police reports filed over employee theft and identity theft",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "she told me I was not eligible to bank with XXXX. Advised the bank no longer wanted to do business with me.", "speaker": "narrative"},
        {"quote": "I also have the right to full disclosure to know if any information out there is being reported negatively against me", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "After previously holding a $250000.00 business savings balance and reporting employee theft, the customer was told she is no longer eligible to bank with Chase, with no disclosure of the reason despite ongoing identity theft issues."
}

R['cfpb_9550543'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a fraudulent credit card and checking account were discovered open in the customer's name at the same branch where a legitimate account was being opened", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "the same branch representative repeatedly gave false information, including an undisclosed 24-48 hour account hold after renumbering the account", "is_primary": False}
  ],
  "products": ["checking_or_savings", "credit_card"],
  "services": ["branch", "phone_support"],
  "customer_ask": "escalation_or_complaint",
  "stated_reason": "wants the repeated misinformation from a specific branch representative addressed and formally complains about it",
  "underlying_driver": "the same branch representative who discovered a fraudulent card and account also gave false promises about card expediting and digital wallet access, and failed to disclose that renumbering the account would trigger a 24-48 hour hold on funds",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "fraudulent card and account discovered at branch",
      "issue_statement": "While opening a new account, the customer discovered a fraudulent credit card and checking account already open in her name, which the branch was able to resolve with the credit card department.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "a fraudulent credit card and checking account were found open in the customer's name at the same branch she was visiting to open a legitimate account",
      "outcome": "resolved",
      "evidence": [
        {"quote": "I discovered there was already a fraudulent credit card opened in my name! As well as another checking account.", "speaker": "narrative"},
        {"quote": "Called in with this rep to the CHASE CREDIT CARD department and was able to get that situation resolved.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "undisclosed hold after unexplained renumbering",
      "issue_statement": "After the same representative helped renumber the account, every transaction was declined because of an undisclosed 24-48 hour hold, on top of previous false promises from the same person.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "the representative never disclosed that renumbering the account would trigger a 24-48 hour hold, and had previously given false promises about card expediting and digital wallet access",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I WAS NOT INFORMED THAT THERE WOULD BE A HOLD ON MY ACCOUNT.", "speaker": "narrative"},
        {"quote": "Its too many incidents of NOT telling the truth with this person.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "partially_resolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A fraudulent credit card and checking account were discovered open in the customer's name at a branch, and the same representative who helped resolve it also failed to disclose that renumbering the account would trigger a 24-48 hour hold, on top of prior false promises."
}

R['cfpb_9838716'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "six fraudulent $200.00 charges overdrew the account, and some reversed credits were later revoked when the charges were reclassified as not fraud based on unverifiable device evidence", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "nearly a month of calls and branch visits produced inconsistent claim statuses and little clarity on the remaining disputed charges", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support", "branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants all six fraudulent $200.00 charges permanently reversed and the overdrawn balance corrected",
  "underlying_driver": "six identical fraudulent charges were made through a digital wallet, but Chase reversed only some credits, reclassified others as not fraud citing unverifiable device evidence, and left the customer overdrawn after nearly a month of inconsistent handling",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "identical fraud charges treated inconsistently",
      "issue_statement": "Six identical $200.00 fraudulent digital wallet charges were treated inconsistently, with some credited permanently, others reversed back, and two never explained at all.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "charges made the same way through the same digital wallet were ruled fraud in some cases and not fraud in others based on device evidence the phone carrier says the bank could not actually have",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "they could not consider these charges fraud, and the $600.00 I got back would be taken away from me once again", "speaker": "narrative"},
        {"quote": "it is EXTREMELY frustrating that I have received no help", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "partially_resolved",
  "positive_moments": [
    {"what": "a branch banker was helpful and personally contacted the fraud department on the customer's behalf", "category": "helpful_staff", "quote": "He was very helpful and contacted the fraud department as well", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "Six identical $200.00 fraudulent digital wallet charges were handled inconsistently, with some permanently credited and others reversed back as not-fraud based on unverifiable device evidence, leaving the account overdrawn after nearly a month of confusing back-and-forth."
}

R['cfpb_10182707'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a card was locked for 24 hours over a legitimate transfer attempt to a previously used recipient, blocking use of paid card benefits", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "the agent handling the fraud lock hung up before the customer could ask further questions", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "explanation",
  "stated_reason": "wants the card unlocked since the transaction was to a previously used, legitimate recipient",
  "underlying_driver": "the card was locked over a large transfer to a recipient the customer had transacted with before, and after full authentication the agent still refused to unlock it and hung up before further discussion",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "card locked over legitimate repeat transfer",
      "issue_statement": "A card was locked for 24 hours over a $5500.00 transfer attempt to a previously used, legitimate recipient, and the agent refused to unlock it after full authentication and then hung up.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "the card remained locked despite full authentication and a prior transaction history with the same recipient, and the agent hung up before further questions could be asked",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase refused, claiming that this was fraudulent activity, and said they will keep my card locked for XXXX hours while they investigate.", "speaker": "narrative"},
        {"quote": "The agent then immediately hung up on me before I could ask questions", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A card was locked for 24 hours over a $5500.00 transfer to a previously used, legitimate recipient, and after full authentication the agent still refused to unlock it and hung up before further discussion, blocking access to paid card benefits."
}

R['cfpb_10502702'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a fraud claim from a stolen wallet was closed the same day it was filed, and staff could not explain how they concluded there was no fraud", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the money from the fraudulent transactions returned",
  "underlying_driver": "after a stolen wallet led to fraudulent charges at stores and an ATM, the claim was closed the same day, and a representative could not give a valid explanation for concluding there was no fraud",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "fraud claim closed same day without explanation",
      "issue_statement": "A fraud claim over transactions made with cards from a stolen wallet was closed the same day it was filed, and a representative could not explain how they concluded there was no fraud.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "the claim was closed the same day it was filed, and the representative could not give a valid explanation for the no-fraud conclusion",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "A representative talked around in circles basically saying there was no evidence of fraud when there was in fact fraud.", "speaker": "narrative"},
        {"quote": "I asked her to explain to me how they came to that conclusion but she couldnt give me a valid answer and was non-chalant about it.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A fraud claim over charges made with cards from a stolen wallet was closed the same day it was filed, with a dismissive representative unable to explain how the no-fraud conclusion was reached."
}

R['cfpb_10908266'] = {
  "contact_reasons": [
    {"reason": "customer_service_experience", "specific_reason": "a teller refused to let the customer make a payment on an auto loan or credit card, saying the bank decided never to do business with him for life", "is_primary": True}
  ],
  "products": ["auto_loan", "credit_card"],
  "services": ["branch"],
  "customer_ask": "escalation_or_complaint",
  "stated_reason": "seeks to hold Chase accountable for refusing to accept his loan and credit card payments in branch",
  "underlying_driver": "despite years of on-time payments and no prior incidents of profanity or threats, a teller refused to let him make an auto loan and credit card payment and said he was permanently banned from the branch",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "banned from branch and denied payment",
      "issue_statement": "A teller refused to let a longtime customer with a perfect payment history make an auto loan and credit card payment, saying the bank decided never to do business with him for life.",
      "product": "auto_loan",
      "sentiment": -2,
      "driver_category": "staff_attitude_or_competence",
      "driver": "a teller refused to accept a legitimate loan and credit card payment and declared a lifetime ban with no cited misconduct despite years of on-time payments",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "she said the bank made a decision to not do business with me for life and I'm banned from their branch.", "speaker": "narrative"},
        {"quote": "This was egregious.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A teller refused to accept a longtime customer's auto loan and credit card payment, declaring a lifetime branch ban with no cited misconduct despite years of on-time payments."
}

R['cfpb_11221621'] = {
  "contact_reasons": [
    {"reason": "terms_information_or_communication", "specific_reason": "conflicting and arbitrary branch rules about adding a remote account holder led to being told he must be physically present, after being told the opposite when the account was opened", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch", "phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "just wants the remote account holder added to the already-opened account",
  "underlying_driver": "a branch representative first said a remote account holder could be added later, then admitted that was a mistake and said he must be physically present, and a case manager refused to explain the policy or provide an escalation contact",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "conflicting rules on adding remote account holder",
      "issue_statement": "After being told a remote account holder could be added later, the branch reversed course, insisting he must be physically present, and a case manager refused to explain the policy or provide an escalation contact.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "the branch first said the account holder could be added remotely, then reversed course requiring physical presence, and refused to provide any escalation contact when challenged",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "someone like XXXX who can not be present with us must be added to the account when the account is opened -- but there is no way to add him later unless he is physically present", "speaker": "narrative"},
        {"quote": "I asked for the name of his boss so I could escalate -- but he refused saying this is the final decision.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A branch representative first said a remote co-account holder could be added later, then reversed course requiring physical presence, and a case manager refused to explain the policy or allow escalation."
}

R['cfpb_11547967'] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a Zelle payment shown as received was later canceled or retracted with no explanation, and Chase could not help recover it", "is_primary": True},
    {"reason": "payment_or_transfer_problem", "specific_reason": "a separate $100.00 payment sent to a mistyped recipient number could not be retrieved by the bank", "is_primary": False}
  ],
  "products": ["money_transfer_or_p2p"],
  "services": ["mobile_app"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants help recovering money from a payment that was retracted and a separate payment sent to the wrong number",
  "underlying_driver": "a Zelle-type payment initially confirmed as received later disappeared as canceled or retracted, and a separate payment mistakenly sent to a mistyped number could not be recovered either",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "confirmed payment later retracted unexplained",
      "issue_statement": "A payment confirmed as received by text message later showed as canceled or retracted the next day, and Chase was not able to help recover the money.",
      "product": "money_transfer_or_p2p",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "a payment confirmed as received disappeared the next day as canceled or retracted, and Chase could not help recover it",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "the following day it show that the money was ether canceled or re tracked so I never received my money.", "speaker": "narrative"},
        {"quote": "Chase was not able to help with this.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "misdirected payment to wrong number unrecoverable",
      "issue_statement": "A separate $100.00 payment sent to a mistyped phone number could not be retrieved when the customer contacted the bank.",
      "product": "money_transfer_or_p2p",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "a $100.00 payment sent to a mistyped number could not be retrieved through the bank",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I accidentally typed one number wrong or off and when I contacted the bank I was not able to retrieve it", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A payment confirmed as received later showed as canceled or retracted with no help from the bank, and a separate $100.00 payment sent to a mistyped number could not be recovered either."
}

R['cfpb_12133332'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a third-party check deposit was held and the account closed while Chase tries unsuccessfully to verify the payee by phone, leaving the customer without funds and rejecting a routine SSI deposit", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "needs the money released, warning she is on the verge of becoming homeless",
  "underlying_driver": "Chase closed the account while still holding a legitimately deposited third-party check, rejected a routine SSI direct deposit, and refused an offer to bring the payee into a branch in person",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "check held and account closed with routine deposit rejected",
      "issue_statement": "A third-party check deposit remains held and the account has been closed, while Chase also rejected a routine SSI direct deposit and refused an offer to bring the payee into a branch to verify in person.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "money_held_or_not_returned",
      "driver": "the check remains held on a closed account, a routine SSI deposit was also rejected, and Chase refused an in-person verification offer, leaving the customer without any funds",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "They are still holding but have closed my acct. The funds are not available to me.", "speaker": "narrative"},
        {"quote": "I have never committed any fraud I am in the verge of becoming homeless", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A third-party check deposit remains held on a now-closed account, a routine SSI direct deposit was also rejected, and Chase refused an in-person verification offer, leaving the customer without funds and near homelessness."
}

R['cfpb_12540088'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a $50000.00 employer check was held for close to two months after the account was closed because Chase could not verify LLC ownership information on the state website", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $50000.00 check released or at least canceled so a new one can be issued",
  "underlying_driver": "Chase insists on verifying ownership through a state website that legally does not show the customer's personal information due to a registered-agent privacy protection, despite a certified state document already proving ownership, and refuses to cancel the check to let a new one be issued",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "employer check held over unverifiable ownership website",
      "issue_statement": "A $50000.00 employer check has been held for close to two months because Chase insists on verifying LLC ownership on a state website that legally shows only registered-agent information.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "policy_or_terms_change",
      "driver": "Chase's internal policy requires state-website verification that legally cannot show ownership information, and refuses a certified document or canceling the check for reissuance",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase bank has been holding my $50000.00 check for close to 2 months only because of their internal process, which is not even a federal or state regulation.", "speaker": "narrative"},
        {"quote": "Chase bank rejected this request and insisted that they need to verify the information via state website and until this is done they should keep my check.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $50000.00 employer check has been held for close to two months because Chase insists on verifying ownership through a state website that legally cannot show personal information, refusing to accept a certified state document or even cancel the check for reissuance."
}

R['cfpb_13034737'] = {
  "contact_reasons": [
    {"reason": "terms_information_or_communication", "specific_reason": "a card advertised as interest free is charging interest and increasingly high monthly fees regardless of usage, unlike the customer's other cards", "is_primary": True},
    {"reason": "fees_and_charges", "specific_reason": "a minimum monthly charge of hundreds of dollars keeps increasing every month whether or not the card is used", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "explanation",
  "stated_reason": "wants to understand why a card advertised as interest free carries growing interest and fees he cannot keep up with",
  "underlying_driver": "the card was opened expecting an interest-free arrangement, but interest and an undisclosed Interest Saving Balance concept resulted in monthly minimums of hundreds of dollars that keep rising regardless of use",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "interest-free card carrying rising fees",
      "issue_statement": "A card advertised as interest free is instead charging interest and a monthly minimum of hundreds of dollars that keeps increasing regardless of whether the card is used.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "unexpected_charge",
      "driver": "interest and fees appeared on a card advertised as interest free, with an undisclosed Interest Saving Balance concept driving monthly minimums into the hundreds and rising",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Advertised as interest free. Not the case I have interest added & fees.", "speaker": "narrative"},
        {"quote": "Predartory lending, my other credit cards don't have these excessely high monthly charges of hundreds of dollars a month.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A card advertised as interest free is instead charging interest and rising monthly minimums of hundreds of dollars regardless of usage, which the customer calls predatory lending compared to his other cards."
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
