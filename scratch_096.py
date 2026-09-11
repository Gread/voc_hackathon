import json, pathlib

bundle = json.load(open('data/work/extract_bundles/bundle_096.json', encoding='utf-8'))
texts = {r['call_id']: r['text'] for r in bundle['records']}
keys = {r['call_id']: r['cache_key'] for r in bundle['records']}

R = {}

R['cfpb_9551725'] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "advertised sign-up bonus points fell short of the amount promised after qualifying spend was confirmed", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "had to give address, birthdate, another card's name and its CVV before being transferred and put on a 20-minute hold", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "calling about remaining bonus points that never posted after qualifying spend was met",
  "underlying_driver": "the bonus points balance is short of what was advertised, and getting an answer required extensive unrelated personal verification, a transfer, and a hold",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "signup bonus points short of advertised amount",
      "issue_statement": "Chase advertised a sign-up bonus for spending a set amount in three months, but months later the posted bonus points are short of what was advertised.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "a supervisor confirmed the qualifying spend was met but the missing points were only promised a possible fix after two statement cycles",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase is XXXX short of what was advertised.", "speaker": "narrative"},
        {"quote": "confirmed that I, indeed, did spend over XXXX XXXXXXXX within the three months period, as stated in the terms and agreement", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "excessive verification before addressing points issue",
      "issue_statement": "Before looking into the missing points, a representative required address verification, a birthdate, the name of another Chase card and its CVV, then transferred the call to a 20-minute hold.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "long_wait_or_delay",
      "driver": "required unrelated personal and other-card verification, then a 20-minute hold before a supervisor addressed the issue",
      "outcome": "resolved",
      "evidence": [
        {"quote": "she requested the three digit CVV number on the back of the Slate card", "speaker": "narrative"},
        {"quote": "The phone system put my back in the queue for another 20 minute hold for the next representative.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "the supervisor stopped requiring further security verification and addressed the points issue directly", "category": "helpful_staff", "quote": "without any further security inquiries, he delve into the situation at hand", "speaker": "narrative"}
  ],
  "redaction_heavy": True,
  "summary": "A promised credit card sign-up bonus fell short after qualifying spend was confirmed, and reaching a resolution required extensive personal verification and a hold before a supervisor promised a possible fix in two statement cycles."
}

R['cfpb_9832614'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "scammers posing as a fraud department walked the customer through wiring two payments framed as reversing fraudulent wires; the money was never returned", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the bank to return the money lost to the scam",
  "underlying_driver": "a caller impersonating a fraud department walked the customer through the app to wire two payments framed as reversing fraud, and the funds were never returned",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "scam wires framed as fraud reversal",
      "issue_statement": "Callers impersonating a fraud department walked the customer through wiring two payments in the app, framed as reversing fraudulent wires, and the money never came back.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "two wires sent under instructions from scammers posing as the fraud department; Chase would not return the money",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I DID NOT RECEIVE MY MONEY IN RETURN.", "speaker": "narrative"},
        {"quote": "I am one of thousands who this happens to on the daily", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A scammer impersonating a Chase fraud department walked the customer through wiring two payments framed as reversing fraud, and the bank has not returned the money."
}

R['cfpb_10173504'] = {
  "contact_reasons": [
    {"reason": "terms_information_or_communication", "specific_reason": "a Chase Travel agent said any trip cancellation would be fully covered by the credit card, then the claim was denied for a reason the customer was never warned about", "is_primary": True},
    {"reason": "dispute_or_chargeback", "specific_reason": "trip cancellation claim for $2900.00 was denied because it does not cover cancellations for passport issues", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants a full refund of the $2900.00 trip because Chase told her the trip would be fully covered",
  "underlying_driver": "a Chase Travel agent told the customer she did not need separate trip insurance because the card fully covered cancellations, but the claim was denied for a passport-related cancellation",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "trip protection claim denied after agent promised full coverage",
      "issue_statement": "A Chase Travel agent said any trip cancellation would be fully covered by the card, but after cancelling due to a passport problem, Chase denied the $2900.00 claim, saying passport-related cancellations are not covered.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "a Chase Travel agent said cancellation would be fully covered, but the $2900.00 claim was denied for a passport-related cancellation with no such exclusion mentioned beforehand",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "He told me that ANY TRIP CANCELLATION WOULD BE FULLY COVERED because I was using my CHASE VISA to pay for the trip!", "speaker": "narrative"},
        {"quote": "they don't reimburse for trips cancelled due to passport issues", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A Chase Travel agent promised full trip cancellation coverage, but Chase denied the $2900.00 claim after a passport problem forced the cancellation, leaving the customer without a refund."
}

R['cfpb_10485330'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "identity theft let someone print a check off the account at a branch with only one form of ID, overdrawing the account", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "was blamed for the fraud, denied a letter for merchants, and was told rudely that accounts could not be closed while still standing in the branch", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch", "phone_support"],
  "customer_ask": "explanation",
  "stated_reason": "wants to know how a check could be printed off the account by someone else and why a promised account alert was never placed",
  "underlying_driver": "a fraudulent check was printed at a branch using one form of ID, alerts the branch promised after a prior incident were never placed, and the branch blamed the customer instead",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "fraudulent check printed at branch",
      "issue_statement": "The account was overdrawn by a check the customer never wrote, which someone printed at a branch using only a single form of ID, and a Counter Fee was charged for it.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "a check was printed at a branch by someone presenting a single ID, causing an overdraft, and the customer was charged a Counter Fee for it",
      "outcome": "resolved",
      "evidence": [
        {"quote": "I was informed that the check was printed at a branch and that I was a victim of identity theft.", "speaker": "narrative"},
        {"quote": "I was notified that the claim had been approved but as of XX/XX/XXXX, I still do not have funds returned to my account", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "promised account alerts never placed",
      "issue_statement": "After the same type of fraud happened once before, the customer asked for alerts on the account, but the branch never placed them and instead blamed the customer for the new fraud.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "alerts requested after an earlier identical incident were never placed, so the same fraud happened again",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I asked for alerts to be placed on my account and I was assured that all transactions would be scrutinized moving forward", "speaker": "narrative"},
        {"quote": "I found out that an alert had never been placed on my account and instead, I was being blamed for the fraud", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "rude branch staff when asking to close account",
      "issue_statement": "When the customer asked to close the accounts because the branch was not helping, staff was condescending and rude and offered no support.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "staff_attitude_or_competence",
      "driver": "staff was condescending and rude and refused to close the account while the customer was still in the branch",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Instead of being helpful, they was condescending and rude and offered no support.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "partially_resolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A fraudulently printed check overdrew the account and the claim was eventually approved, but promised fraud alerts were never placed, the promised letter never arrived, and branch staff were rude when the customer tried to close the account."
}

R['cfpb_10903527'] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "a $250.00 sign-up bonus promised when opening a Chase Freedom Unlimited card was never paid after qualifying spend was met", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "Chase accused the customer of trying to get a richer offer instead of honoring the bonus promised at sign-up", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["online_banking"],
  "customer_ask": "fix_error",
  "stated_reason": "wants the $250.00 sign-up bonus that was promised when the card was opened",
  "underlying_driver": "Chase now says the only offer was the 1.5% earnings rate, but screenshots show a $250.00 bonus was promised in addition, and Chase accused the customer of misrepresenting the offer",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "sign-up bonus never paid",
      "issue_statement": "A $250.00 sign-up bonus promised after spending $500.00 in three months on a new Chase Freedom Unlimited card was never received as a statement credit or points.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "screenshots show a $250.00 bonus was promised at sign-up in addition to a 1.5% earnings rate, but Chase says only the 1.5% offer applies",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "We have spent well over $500.00 and have never seen the expected $250.00 bonus", "speaker": "narrative"},
        {"quote": "They replied again today accusing me of trying to get a \" richer offer ''", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $250.00 credit card sign-up bonus promised at account opening was never paid, and Chase accused the customer of misrepresenting the offer instead of honoring it, prompting a CFPB complaint."
}

R['cfpb_11198352'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a foreign debit charge and fee the customer never made was investigated and found to be authorized by the bank, which the customer disputes", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "reported a fraudulent foreign debit charge and fee on an account with no debit card",
  "underlying_driver": "Chase's investigation concluded the customer authorized the charge, which the customer says is false since there is no debit card on the account and no other activity since a much earlier date",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "fraud claim denied despite no debit card on account",
      "issue_statement": "An $83.00 foreign debit charge plus a $2.00 fee was reported as fraud, but Chase's letter said it was authorized even though the customer has no debit card and no activity on the account since months earlier.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase found the customer authorized a debit charge although she has no debit card for the account and was elsewhere when it posted",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I just received letter XX/XX/XXXX that they researched this & found that I did authorize this debit which is false.", "speaker": "narrative"},
        {"quote": "I do not have a debit card for this account, nor do I use XXXX", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase denied a fraud claim for a foreign debit charge and fee, saying it was authorized, even though the customer has no debit card on the account and was not near the transaction location."
}

R['cfpb_11519339'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a spoofed call from a real Chase number convinced the customer to move $1500.00 to a new account during a claimed hack, and the money was never returned", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $1500.00 lost to the scam returned",
  "underlying_driver": "a call spoofing Chase's real number convinced the customer her account was hacked and to move money, and Chase said it could only help if the recipient returned the funds",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "spoofed call scam moved money out of account",
      "issue_statement": "A call that appeared to come from an actual Chase number told the customer her account was hacked and had her move $1500.00 to a new account, which turned out to be a scam.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "Chase said it could not help unless the person who took the $1500.00 returned it, so the money was never refunded",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "they said they couldnt do anything for me unless the person that took the money returned it", "speaker": "narrative"},
        {"quote": "my money was never returned", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "Chase closed the old account and issued a new one after the scam", "category": "fast_resolution", "quote": "My old account was closed and I was given a whole new account", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A call spoofing Chase's real number tricked the customer into wiring $1500.00 during a claimed account hack, and Chase said it could not refund the money unless the recipient returned it."
}

R['cfpb_12117268'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "funds from a check endorsed over from a relative were held on suspicion of fraud and all accounts were closed", "is_primary": True},
    {"reason": "account_opening_or_closure", "specific_reason": "being placed in a check-clearing system that prevents opening a new account at any bank to deposit the mailed check", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "explanation",
  "stated_reason": "asked what to do with a large mailed check when no bank will let him open an account because of Chase's reporting",
  "underlying_driver": "Chase held and eventually verified the deposited funds but closed all accounts, and being flagged in a check-verification system now blocks opening accounts anywhere to deposit the resulting check",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "funds held then accounts closed on suspected fraud",
      "issue_statement": "Chase suspended and held funds from a check endorsed over by a relative on suspicion of fraud, verified it months later, but closed all of the customer's accounts in the meantime.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "money_held_or_not_returned",
      "driver": "funds were held for months on suspicion before Chase verified the check, while all accounts were closed and other banks refused new accounts",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase suspended my funds of XXXX dollars and have been holding on to them since XXXX", "speaker": "narrative"},
        {"quote": "Since all of this has happened I have had all of my accounts closed out by multiple banks I have defaulted on my house and my credit score has dropped over XXXX points.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "Chase held funds from an endorsed-over check for months on suspicion of fraud, then closed all the customer's accounts, leaving him unable to open an account anywhere to deposit the resulting check while his credit score and mortgage suffered."
}

R['cfpb_12516972'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a caller posing as Chase fraud department tried to get a login passcode after a fake suspicious-payment text alert", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["mobile_app"],
  "customer_ask": "stop_or_block",
  "stated_reason": "reporting an attempted scam that used real-looking Chase fraud alert texts to try to get account access",
  "underlying_driver": "a caller impersonating Chase's fraud department asked for a login passcode after sending realistic fraud alert texts, and threatened the customer's husband when confronted",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "phishing call attempted to steal login passcode",
      "issue_statement": "After realistic-looking Chase fraud alert texts, a caller claiming to be from the fraud department asked for a passcode that the texts themselves warned Chase would never request.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "system_or_app_failure",
      "driver": "the scam texts looked identical to genuine Chase security messages, making the fraudulent call convincing until the passcode was requested",
      "outcome": "resolved",
      "evidence": [
        {"quote": "The second text msg clearly stated that Chase would NEVER call and ask for that code.", "speaker": "narrative"},
        {"quote": "the individual then claimed to have all of my information and verbally threatened us", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "resolved",
  "positive_moments": [
    {"what": "the customer avoided giving up the passcode and locked the account before any loss occurred", "category": "fast_resolution", "quote": "I immediately changed the login information on my banking accounts while my husband was on the phone with the individual", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A scammer used realistic Chase fraud alert texts to try to obtain a login passcode; the customer refused, locked the account, and got new cards issued, though the convincing scam remains a concern."
}

R['cfpb_13025278'] = {
  "contact_reasons": [
    {"reason": "terms_information_or_communication", "specific_reason": "expected the credit card's travel insurance to cover lost luggage worth over $4000.00 but the process has dragged on for months with repeated requests for documents that cannot be produced", "is_primary": True},
    {"reason": "no_response_or_follow_up" if False else "customer_service_experience", "specific_reason": "Chase promised to contact the airline directly but never confirmed doing so, and only sends repeated copy-paste emails asking for more documents", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["chat_or_email"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants Chase Card Benefit Services to reimburse the value of lost luggage using the card's travel insurance",
  "underlying_driver": "the airline lost the luggage and stopped communicating, and Chase Card Benefit Services keeps asking for proof the customer cannot produce instead of reaching out to the airline as promised",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "travel insurance claim stalled for months",
      "issue_statement": "After the airline lost luggage worth over $4000.00, Chase Card Benefit Services has spent almost a year asking for documents the customer cannot produce instead of reimbursing the claim.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "no_response_or_follow_up",
      "driver": "Chase promised to contact the airline directly about the claim but never confirmed doing so, sending only repeated copy-and-paste requests for documents instead",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase also promised to reach out to the airline directly. If they did, they havent told me or made any progress.", "speaker": "narrative"},
        {"quote": "instead I get the same copy-and-paste emails asking for more documents I cant produce", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "An airline lost luggage worth over $4000.00 and stopped responding, and the credit card's travel insurance claim has stalled for nearly a year with repeated requests for documents the customer cannot produce."
}

R['cfpb_13551423'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "large amounts of money left the account in a short period during a scam without Chase freezing payments or reaching out", "is_primary": True},
    {"reason": "account_opening_or_closure", "specific_reason": "Chase closed the accounts instead of reimbursing the money lost to the scam", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants to be reimbursed for the money lost to the scam",
  "underlying_driver": "Chase did not freeze or question large amounts of money leaving the account in a short period and then closed the accounts instead of refunding the loss",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "large scam withdrawals not flagged",
      "issue_statement": "A financial scam caused severe losses because Chase did not attempt to freeze or stop payments or reach out about large amounts of money leaving the account in a short period.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "Chase made no attempt to freeze or stop the payments or contact the customer as large sums left the account quickly, and refused to reimburse the loss",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "They did not make any attempts to freeze or stop payments on my account and reach out to me to inquire about the large amounts of money leaving my account in a short period of time.", "speaker": "narrative"},
        {"quote": "Instead they wrongfully closed my accounts.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "Large scam-related withdrawals were not flagged or stopped by Chase, which then closed the customer's accounts instead of refunding the losses."
}

R['cfpb_14073982'] = {
  "contact_reasons": [
    {"reason": "collections_or_debt", "specific_reason": "Chase sued and won a judgment on a debt that credit reports show was already charged off and sold as a profit-and-loss write-off", "is_primary": True}
  ],
  "products": ["debt_collection"],
  "services": [],
  "customer_ask": "other",
  "stated_reason": "asking the CFPB to investigate whether Chase misrepresented its legal right to sue on a debt it no longer owned",
  "underlying_driver": "the credit report shows the account was charged off and closed as a profit-and-loss write-off, which usually means it was sold, yet Chase still sued and obtained a judgment",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "judgment obtained on a debt reported as sold",
      "issue_statement": "Chase obtained a $5500.00 judgment on a debt that the customer's credit report shows was charged off and closed as a profit-and-loss write-off, suggesting it no longer owned the debt.",
      "product": "debt_collection",
      "sentiment": -2,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "a $5500.00 judgment was obtained despite credit report evidence the debt was already charged off and sold to a third party",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "My credit report shows the account was charged off and closed in XX/XX/XXXX as a profit and loss write-off.", "speaker": "narrative"},
        {"quote": "the court issued a Final Judgment on XX/XX/XXXX, without acknowledging my filing or giving me a fair hearing", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase obtained a $5500.00 court judgment on a debt that credit report records suggest was already charged off and sold, and the customer's court filing objecting to the claim was not acknowledged."
}

R['cfpb_14655447'] = {
  "contact_reasons": [
    {"reason": "fees_and_charges", "specific_reason": "an interest charge of over $260.00 appeared despite the statement balance being paid to $0.00 before the due date", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "a representative was hostile and rude and refused to explain the charge, saying the customer should calculate it herself", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "explanation",
  "stated_reason": "wants to know why an interest charge appeared after paying the statement balance to $0.00",
  "underlying_driver": "a representative refused to explain a $260.00 interest charge on a paid-off balance and was rude when asked how to check for such charges",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "interest charge despite zero balance",
      "issue_statement": "An interest charge of over $260.00 appeared even though the statement balance was paid to $0.00 before the closing and due dates.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "unexpected_charge",
      "driver": "an interest charge of over $260.00 posted despite the portal showing payments fully paid",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "All statement balances paid down to $0.00 before the closing date and statement due date. Suddenly theres an interest charge of over $260.00.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "rude representative refused to explain charge",
      "issue_statement": "A Chase Card Services representative was extremely hostile and rude and told the customer to calculate the interest charge herself, saying everyone knows how.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "staff_attitude_or_competence",
      "driver": "representative was hostile and rude and refused to explain the charge, saying \"everyone knows this\"",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "who was extremely hostile and rude when asked where XXXX able to check on this constant incurring charge", "speaker": "narrative"},
        {"quote": "She said I need to do the calculations to work it out myself and I quote everyone knows this.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "An interest charge of over $260.00 appeared despite a $0.00 paid balance, and a Chase Card Services representative was rude and refused to explain how to check for such charges."
}

R['cfpb_15310816'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a business account was locked over an inability to verify the employer's phone number after a legitimate work-payment check was deposited", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "explanation",
  "stated_reason": "wants the funds released or a lawful explanation for why they are being withheld",
  "underlying_driver": "Chase locked the account because the employer's phone number could not be verified since he is not a Chase customer, despite the customer providing all requested identity documentation",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "business account locked over unverifiable employer phone number",
      "issue_statement": "Chase locked the business checking account and withheld a legitimately earned check deposit because the employer's phone number could not be verified, since the employer is not a Chase customer.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "funds from a valid work-payment check are withheld solely because the employer's phone number is not in Chase's system",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase has locked my account and is refusing to release my funds due to an inability to verify my employers phone number.", "speaker": "narrative"},
        {"quote": "Chase has not provided a clear or reasonable explanation or timeline for when the issue will be resolved", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A business checking account was locked and a legitimately earned check deposit withheld because the employer's phone number, who is not a Chase customer, could not be verified, with no timeline for resolution."
}

R['cfpb_15935149'] = {
  "contact_reasons": [
    {"reason": "balance_or_statement_error", "specific_reason": "funds from two deposited checks were made available and spent, then withdrawn a second time from the account without explanation", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "was told incorrectly that no double withdrawal occurred, then blamed for using personal checks after already being told the funds were available", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support", "branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the money that was withdrawn a second time, plus any overdraft fees, returned",
  "underlying_driver": "Chase told the customer the deposited funds were available and usable, then withdrew the same amount again days later because personal checks are no longer accepted, without apology or explanation",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "deposited funds withdrawn twice",
      "issue_statement": "After Chase confirmed two deposited checks were available and the customer used the funds, Chase withdrew the same amount from the account a second time with no explanation at first.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "unexpected_charge",
      "driver": "funds already confirmed available and spent were withdrawn a second time because Chase no longer accepts personal checks, which was not disclosed beforehand",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "A couple days later Chase then took the funds from my account a second time with no explanation why.", "speaker": "narrative"},
        {"quote": "Chase made these funds available to me but then took my money from my account TWICE after I ALREADY USED THOSE FUNDS", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "conflicting and dismissive explanations from staff",
      "issue_statement": "A phone representative first insisted the funds were not deducted twice, and after finally admitting it, blamed the customer for having friends who write invalid checks.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "staff_attitude_or_competence",
      "driver": "representative denied the double withdrawal happened, then blamed the customer for needing better friends who write valid checks",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I need to find better friends who will write me valid checks", "speaker": "narrative"},
        {"quote": "he too was reluctant to offer me any valid explanation why Chase made these funds available to me but then took my money", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "Chase confirmed two deposited checks were available and let the customer use the funds, then withdrew the same amount again days later with a dismissive explanation, and staff blamed the customer instead of apologizing."
}

R['cfpb_16696294'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a Chase account was opened without consent and is appearing on credit reports as a result of identity theft", "is_primary": True},
    {"reason": "credit_reporting", "specific_reason": "requesting the inaccurate accounts resulting from identity theft be blocked and removed from credit reports within four business days under FCRA Section 605C", "is_primary": False}
  ],
  "products": ["credit_reporting_service"],
  "services": [],
  "customer_ask": "other",
  "stated_reason": "requesting investigation and permanent removal of accounts opened through identity theft from the credit file",
  "underlying_driver": "accounts including one at Chase were opened without consent and the customer is formally disputing them as fraudulent under FCRA Section 605C",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "chase account opened without consent",
      "issue_statement": "A Chase Bank account was opened without the customer's consent and is showing on credit reports as a fraudulent or inaccurate account.",
      "product": "credit_reporting_service",
      "sentiment": -1,
      "driver_category": "other_or_unclear",
      "driver": "an account opened without consent is appearing on the credit report and has not yet been blocked or removed",
      "outcome": "unknown",
      "evidence": [
        {"quote": "Chase Bank Accounts was opened without my consent", "speaker": "narrative"},
        {"quote": "I am requesting that you block and permanently remove any information resulting from identity theft or inaccurate reporting", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unknown",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "The customer sent formal FCRA dispute letters to credit bureaus and furnishers, including Chase, requesting removal of a bank account opened without consent as a result of identity theft."
}

R['cfpb_17273367'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "several unauthorized credit inquiries appeared on credit reports, including from JPMCB Card and JPMorgan Chase Bank", "is_primary": True}
  ],
  "products": ["credit_reporting_service"],
  "services": [],
  "customer_ask": "other",
  "stated_reason": "reporting unauthorized credit inquiries appearing on the credit report",
  "underlying_driver": "multiple hard inquiries the customer did not authorize, including two from JPMCB Card and one from JPMorgan Chase Bank, appeared on the credit report",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "unauthorized credit inquiries on report",
      "issue_statement": "Several credit inquiries the customer did not authorize appeared on the credit report, including two from JPMCB Card and one from JPMorgan Chase Bank NA.",
      "product": "credit_reporting_service",
      "sentiment": -1,
      "driver_category": "other_or_unclear",
      "driver": "unauthorized inquiries from JPMCB Card and JPMorgan Chase Bank NA appear on the credit report",
      "outcome": "unknown",
      "evidence": [
        {"quote": "I have received unauthorized inquiries on my credit reports", "speaker": "narrative"},
        {"quote": "JPMORGAN CHASE BANK NA Inquiry date XX/XX/year>", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unknown",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "The customer lists several unauthorized hard inquiries on their credit report, including entries from JPMCB Card and JPMorgan Chase Bank."
}

R['cfpb_18273738'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a court order against the customer's mother-in-law, who has no connection to the account, was used to freeze first $1300.00 and then $27000.00 in the customer's own account", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "repeated faxed proof of the identity mismatch and a bankruptcy stay was reported as never received, and a call about it was not documented", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch", "phone_support"],
  "customer_ask": "stop_or_block",
  "stated_reason": "wants immediate release of the frozen funds and confirmation no further restraints will be placed based on a judgment against someone else",
  "underlying_driver": "a restraining notice against the customer's mother-in-law, who is not connected to the account, was repeatedly misapplied despite an identity mismatch, an automatic bankruptcy stay, and a written withdrawal from the creditor's attorney",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "account frozen on someone else's court order",
      "issue_statement": "Chase froze $1300.00 and then $27000.00 in the customer's account based on a court order against the mother-in-law, who is not an owner, signer or beneficiary on the account.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "money_held_or_not_returned",
      "driver": "a court order against an unrelated person was used to freeze first $1300.00 then $27000.00, despite repeated notice of the identity mismatch",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "the freeze was based on a court order issued against my mother-in-law", "speaker": "narrative"},
        {"quote": "Chase lifted the initial $1300.00 freeze, but on the same day immediately re-froze $27000.00 in my accountagain based on the same legal document and the same identity mismatch", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "bankruptcy stay and withdrawal notice repeatedly lost",
      "issue_statement": "Faxed proof of the actual debtor's bankruptcy filing and a written withdrawal of the restraining notice from the creditor's attorney were repeatedly reported as not received by Chase.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "no_response_or_follow_up",
      "driver": "documents including the bankruptcy filing and the attorney's withdrawal letter were faxed with confirmation multiple times but Chase kept saying it could not locate them",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase repeatedly stated that it could not locate the faxed documents, despite them being sent correctly and with confirmation", "speaker": "narrative"},
        {"quote": "Chase notified me that this call was not properly documented and there were no notes of my XX/XX/XXXX call", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase repeatedly froze the customer's own account based on a court order against an unrelated relative, and kept losing faxed proof of the identity mismatch, a bankruptcy stay, and the creditor's own withdrawal of the notice, leaving the account still restricted."
}

R['cfpb_18723965'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "requested a $1000.00 refund from an online cosmetology training academy for poor-quality, disorganized and misleadingly licensed instruction, and the academy refused", "is_primary": True}
  ],
  "products": ["other_or_unspecified"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting a $1000.00 refund because the training does not match what was promised",
  "underlying_driver": "the academy's offer terms say payments after training starts are non-refundable, and it denies the quality complaints amount to improper service, so it refuses the refund",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "training academy refund refused",
      "issue_statement": "The academy refused to refund $1000.00 for a disorganized, error-filled and unlicensed cosmetology course, citing its own no-refund policy once training starts.",
      "product": "other_or_unspecified",
      "sentiment": -2,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "the academy relies on a no-refund clause and disputes that lack of a license, scheduling and material errors count as improper service",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I kindly request that you refund the amount of $1000.00", "speaker": "narrative"},
        {"quote": "I consider the service to be unacceptable.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A customer sought a $1000.00 refund from an online cosmetology academy over disorganized, error-filled and unlicensed instruction, and after a long back-and-forth the academy refused and the customer withdrew from the course."
}

R['cfpb_19793761'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "$1900.00 paid via Chase Visa for a short-term rental was never returned after the host repeatedly refused to provide the entry code", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $1900.00 paid for the rental returned since the host never provided access",
  "underlying_driver": "a rental host withdrew $1900.00 from the checking account via Visa but repeatedly refused to give the entry code, forcing the customer to book and pay for another location out of pocket",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "rental payment withheld after host refused entry code",
      "issue_statement": "A host who was paid $1900.00 through the checking account repeatedly refused to provide the entry code needed to check in, and has refused to return the money.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "$1900.00 was withdrawn for a rental the host never provided access to, and the host refuses to return it",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "refuses to return $1900.00 to me", "speaker": "narrative"},
        {"quote": "with me paying for this booking out of my own pocket with no relief provided", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "A rental host who was paid $1900.00 through the customer's checking account never provided the promised entry code and has refused to return the money, and the customer's court complaint about it has stalled on service-of-process problems."
}

R['cfpb_20235704'] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a $13000.00 wire that JPMorgan Chase says was delivered is denied as received by the recipient bank", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants the missing $13000.00 wire located and resolved",
  "underlying_driver": "JPMorgan Chase's own report confirms the wire was delivered to the recipient bank, but that bank continues to officially deny receiving it",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "missing wire disputed between banks",
      "issue_statement": "JPMorgan Chase's report confirms a $13000.00 wire was delivered to the recipient bank, but the recipient bank officially denies receiving the funds.",
      "product": "money_transfer_or_p2p",
      "sentiment": -2,
      "driver_category": "money_held_or_not_returned",
      "driver": "the originating bank's records show delivery of $13000.00 while the receiving bank denies it arrived, leaving the funds unaccounted for",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "JPMC 's own report confirms the funds were delivered to XXXX XXXX ( Routing XXXX ) via XXXX  with XXXX : XXXX.", "speaker": "narrative"},
        {"quote": "XXXX XXXX continues to officially deny receiving the funds.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "An urgent $13000.00 wire that JPMorgan Chase's records show as delivered is being officially denied by the receiving bank, leaving the transfer unresolved."
}

R['cfpb_21351530'] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a payment sent from a personal Chase account to a business account never arrived even though Chase's documentation shows it as sent and completed", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p", "checking_or_savings"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants to know what recourse exists since the money never reached the destination account",
  "underlying_driver": "Chase's own documentation states the transfer was sent and completed, but the funds never arrived at the receiving business account, and neither bank will investigate further",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "transfer marked complete but never arrived",
      "issue_statement": "A payment from a personal Chase account to a business account at another bank never arrived, even though Chase's documentation states the transaction was sent and completed.",
      "product": "money_transfer_or_p2p",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "Chase's own records show the transfer as sent and completed, but the funds never reached the receiving business account and neither bank will investigate further",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "the documentation from chase states transaction sent and completed the funds never got to my business account", "speaker": "narrative"},
        {"quote": "neither bank nor XXXX will do any further investigating", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A payment that Chase's own documentation marks as sent and completed never reached the recipient's business account, and neither bank will investigate further."
}

R['cfpb_22623939'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "Chase refused to dispute charges for merchandise that arrived damaged, defective or incomplete because the charges posted more than 30 days before the dispute was filed", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the disputed charges for damaged, defective and incomplete merchandise credited back",
  "underlying_driver": "Chase would only dispute charges posted within 30 days of the dispute filing, even though the merchandise had not even arrived yet when most of those charges posted",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "dispute denied for charges outside 30-day window",
      "issue_statement": "Chase refused to dispute most of the charges for damaged, defective, wrong-color or incomplete merchandise because they posted more than 30 days before the dispute was filed, even though the goods had not yet arrived.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase applied a 30-day posting window to deny most of the dispute although the merchandise had not arrived, or arrived damaged, within that window",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase refused to work with disputing charges generated in XXXX of XXXX, siting that they would only honor charges that were posted in the first 30 days of dispute", "speaker": "narrative"},
        {"quote": "Chase refuses to reopen claim or assist me with crediting those charges back.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase refused to dispute most charges for damaged, defective or incomplete merchandise, citing a 30-day posting window even though the goods had not yet arrived, and will not reopen the claim."
}

R['cfpb_23335791'] = {
  "contact_reasons": [
    {"reason": "loan_servicing", "specific_reason": "loan statement shows unrecognized payments, misapplied amounts and an unexplained escrow advance that do not match what was actually paid", "is_primary": True}
  ],
  "products": ["mortgage"],
  "services": [],
  "customer_ask": "explanation",
  "stated_reason": "asking what several unrecognized payments are for and why the statement shows misapplied amounts",
  "underlying_driver": "the loan statement lists payments the customer never made, two misapplication entries with matching amounts on the same days, and an unexplained escrow advance not shown in the paperwork sent",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "unrecognized payments and misapplied amounts on statement",
      "issue_statement": "The loan statement lists payments the customer never made, shows two misapplication entries for the same amount on the same days, and an escrow advance not explained in any paperwork received.",
      "product": "mortgage",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "statement shows payments and a misapplication of funds and an escrow advance that were never explained or documented in paperwork sent to the customer",
      "outcome": "unknown",
      "evidence": [
        {"quote": "Also you show a misapplication of XXXX what's that? And a misapplication of XXXX?", "speaker": "narrative"},
        {"quote": "What was the escrow advance on XX/XX/year> of XXXX for?", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unknown",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "A mortgage statement lists payments the customer never made and unexplained misapplied amounts and an escrow advance, none of which match the paperwork sent to the customer."
}

R['cfpb_9553130'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "the account was restricted after depositing a check endorsed over by a fiance whose phone number could not initially be verified as his own", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "a manager was extremely rude and gave contradictory reasons for keeping the restriction even after the fiance's phone company confirmed the number was his", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch", "phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wants the account restriction lifted after depositing a legitimately endorsed inheritance check",
  "underlying_driver": "Chase would not lift the restriction without verifying the fiance's phone number, and kept giving different and contradictory reasons even after the phone company confirmed the number was his",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "account restricted over endorsed check",
      "issue_statement": "The account was restricted after depositing an inheritance check that the fiance, who lacks valid ID, endorsed over to the customer, and Chase would not lift it without verifying his phone number.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "the restriction remained even after the fiance's phone company confirmed his number, because Chase's manager claimed the number was unreachable and that the check was not properly signed",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "My restriction can not be released until they have a valid number for my fiance", "speaker": "narrative"},
        {"quote": "We are now in XX/XX/XXXX and we still don't have the money.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "rude manager gave contradictory explanations",
      "issue_statement": "A manager was extremely rude on the phone and gave contradictory reasons for the restriction, first blaming the phone number and then falsely claiming the fiance had not signed the check.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "staff_attitude_or_competence",
      "driver": "manager was extremely rude and gave shifting explanations, including a false claim that the check was not properly signed",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I held the line for the Manager and he was extremely rude to me.", "speaker": "narrative"},
        {"quote": "The Manager then said that my fiance did not sign the back of the check which he did.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A checking account was restricted after an endorsed inheritance check deposit pending phone verification of the fiance, and even after the phone company confirmed the number, a rude manager kept the restriction with contradictory explanations."
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
    # basic count checks
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
