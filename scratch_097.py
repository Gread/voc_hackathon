import json, pathlib

bundle = json.load(open('data/work/extract_bundles/bundle_097.json', encoding='utf-8'))
texts = {r['call_id']: r['text'] for r in bundle['records']}
keys = {r['call_id']: r['cache_key'] for r in bundle['records']}

R = {}

R['cfpb_9834865'] = {
  "contact_reasons": [
    {"reason": "other_or_unclear", "specific_reason": "a broad list of alleged problems across account opening, closing, fees, fraud and communication with no specific incident described", "is_primary": True}
  ],
  "products": ["other_or_unspecified"],
  "services": [],
  "customer_ask": "other",
  "stated_reason": "lists many categories of alleged problems with Chase and its subsidiaries without describing a specific incident",
  "underlying_driver": "the complaint names many possible problem categories (fraud, holds, fees, communication, closures) without giving specific amounts, dates or events",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "unspecified problems across multiple accounts",
      "issue_statement": "The customer lists many categories of alleged problems, including fraud, account holds, fees and lack of communication, across multiple Chase accounts without specifying what happened.",
      "product": "other_or_unspecified",
      "sentiment": -1,
      "driver_category": "other_or_unclear",
      "driver": "no specific incident, amount or date is given; only a list of possible problem categories across Chase and its subsidiaries",
      "outcome": "unknown",
      "evidence": [
        {"quote": "complete lack of communication regarding accounts", "speaker": "narrative"},
        {"quote": "complete closure of accounts without my knowledge or communication of closure of accounts", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unknown",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "A broad, unspecific list of alleged problems with Chase Bank and its subsidiaries is given, covering fraud, holds, fees and communication failures, with no specific incident, amount or date described."
}

R['cfpb_10173510'] = {
  "contact_reasons": [
    {"reason": "collections_or_debt", "specific_reason": "Chase changed the phone number on file without consent, which the customer believes was a tactic to prompt a call about an owed credit card bill", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "explanation",
  "stated_reason": "questioning why Chase changed the account phone number without consent",
  "underlying_driver": "the customer believes the unrequested phone number change was a sneaky tactic to prompt a call about a bill he already knows he owes and plans to pay",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "phone number changed without consent",
      "issue_statement": "Chase altered the phone number on the account without consent, which the customer believes was meant to prompt a call about an owed bill he already knew about and planned to pay.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "other_or_unclear",
      "driver": "the account's phone number was changed without the customer's consent, apparently to prompt a collection call",
      "outcome": "unknown",
      "evidence": [
        {"quote": "Chase Credit Card Company altered my phone number without my consent, prompting me to call them.", "speaker": "narrative"},
        {"quote": "for them to change my account info like that is crazy", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unknown",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "The customer says Chase changed the phone number on his credit card account without consent, which he believes was a tactic to prompt a call about a bill he already knew he owed."
}

R['cfpb_10485916'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a Turo reservation was made with a stolen debit card under a name that does not match the account, and Chase denied the fraud claim", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants Chase to reopen the claim and get documentation from Turo explaining the denial",
  "underlying_driver": "Turo confirmed the reservation used the customer's debit card under a different, non-matching name, which the customer never authorized",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "fraud claim denied despite mismatched name",
      "issue_statement": "Chase denied a fraud claim for a Turo reservation made with the customer's stolen debit card, even though Turo confirmed the reservation was booked under a different name that does not match the account.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Turo confirmed the reservation name does not match the cardholder, yet Chase denied the claim without requesting that proof",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "the account that this reservation was made under using my debit card was under a different name and do not match the payment card", "speaker": "narrative"},
        {"quote": "I request that chase bank reopen this and request information from XXXX and send it to me as to why they denied this claim", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase denied a fraud claim for a Turo reservation made with the customer's stolen debit card, even though the reservation was confirmed to be booked under a name that does not match the account."
}

R['cfpb_10909500'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a romance and inheritance scam drained retirement, savings and checking accounts over about a year through daily withdrawals sent to the scammer", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "asking for help because the bank did not stop or freeze the account while it was being drained",
  "underlying_driver": "a scammer built a long-distance relationship and convinced the customer to withdraw money daily for over a year to pay fake inheritance release fees, and the bank never stopped or froze the account",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "romance scam drained retirement and savings",
      "issue_statement": "A romance and inheritance scam led to daily bank visits to withdraw money for over a year, draining retirement, savings and checking accounts totaling $250000.00, while the bank never stopped or froze the account.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "daily withdrawals over about a year to pay fake inheritance release fees were never flagged, stopped or frozen by the bank",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "the bank didnt stop me or freeze my account to protect me", "speaker": "narrative"},
        {"quote": "Total amount of my money and investments $250000.00, and $100000.00 loans and mortgage.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A year-long romance and fake inheritance scam led to daily withdrawals draining $250000.00 in savings, checking and retirement funds, and the customer says the bank never stopped or froze the account to protect her."
}

R['cfpb_11202269'] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a $300.00 ATM cash deposit that failed to post due to a machine error was later credited then reversed after an investigation concluded it was authorized", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "multiple representatives refused to reopen the claim, escalate, or review camera footage, and directed her in circles between branch and claims department", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["atm", "phone_support", "branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $300.00 credited back after the ATM ate her deposit due to a documented machine error",
  "underlying_driver": "an ATM froze and failed to post a $300.00 cash deposit despite documented proof of the machine error, and after an initial credit, Chase reversed it saying the deposit was processed as authorized, then refused to reopen the case or review evidence",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "atm deposit reversed despite proof of machine error",
      "issue_statement": "A $300.00 cash deposit that an ATM froze on and failed to post, confirmed by the bank as a machine error at the time, was later reversed after an investigation concluded it was processed as authorized.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "money_held_or_not_returned",
      "driver": "Chase reversed a previously credited $300.00 ATM deposit, calling it authorized, despite same-night notes confirming the machine had just gone down with an error",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "the representative said he could see the machine had JUST went down with an error", "speaker": "narrative"},
        {"quote": "This is absurd and unethical.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "repeated refusal to reopen or escalate the claim",
      "issue_statement": "Multiple representatives and a manager refused to reopen the investigation, would not review ATM camera footage, said there was no superior to transfer to, and told her to file a police report instead.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "several representatives and a manager refused to reopen the case, declined to review camera footage, and said nothing more could be done",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "they do not look at nor use the cameras around the ATM because that would only prove that I was there when I say I was and not prove how much I deposited", "speaker": "narrative"},
        {"quote": "We ended the call with her telling me to make a police report.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "Chase initially credited the missing deposit after the claim was filed", "category": "fast_resolution", "quote": "Chase then, gave me the credit for my missing cash deposit.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "An ATM froze and failed to post a $300.00 cash deposit despite a documented machine error, and after an initial credit Chase reversed it, then multiple representatives refused to reopen the case, review camera footage, or escalate further."
}

R['cfpb_11520732'] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a $400.00 Zelle payment intended for the customer's mother was accidentally sent to a similarly named person who denies receiving it", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants Chase to reverse the $400.00 payment sent to the wrong person by mistake",
  "underlying_driver": "the customer selected the wrong recipient with a similar name for a routine $400.00 payment, and Chase said it could not help reverse it",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "payment sent to wrong recipient not reversed",
      "issue_statement": "A $400.00 payment normally sent to the customer's mother was mistakenly sent to a similarly named person, and Chase said it could not help reverse it even though the pattern of monthly payments made the mistake obvious.",
      "product": "money_transfer_or_p2p",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "Chase declined to help reverse a $400.00 payment sent to the wrong person, and the recipient denies receiving it and disconnected the linked number",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I tried to contact Chase to reverse the transaction, and they said they could not help me.", "speaker": "narrative"},
        {"quote": "they claimed they didnt receive it and dont use XXXX", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A $400.00 payment meant for the customer's mother was mistakenly sent to a similarly named person, and Chase would not help reverse it even though the recipient denies receiving the funds."
}

R['cfpb_12201484'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "someone hacked a social media account and placed nearly $1500.00 in ads through an unrelated company, and Chase denied the fraud claim citing a prior unrelated transaction", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the almost $1500.00 in fraudulent charges refunded",
  "underlying_driver": "Chase held the customer responsible for the charges because he had previously done business with the same company once, despite proof the ads were placed by a hacker without his knowledge",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "fraud claim denied over prior unrelated transaction",
      "issue_statement": "After a hacker placed almost $1500.00 in ads on the customer's behalf through a company he had used once before, Chase denied the fraud claim, saying prior business with a company means it is not fraud.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase says a single prior transaction with the company a year earlier means the new charges cannot be fraud, despite proof submitted",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase literally told me, if you previously do business with a company its not fraud.", "speaker": "narrative"},
        {"quote": "I also have so much proof, which I sent the bank.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A hacked social media account led to almost $1500.00 in unauthorized ad charges, and Chase denied the fraud claim solely because the customer had done unrelated business with the same company a year earlier."
}

R['cfpb_12527070'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "unauthorized JPMCB Card accounts were fraudulently opened in the customer's name as a result of identity theft", "is_primary": True},
    {"reason": "credit_reporting", "specific_reason": "Chase kept reporting the fraudulent accounts to credit bureaus despite a formal dispute with an FTC identity theft report and proof of identity", "is_primary": False}
  ],
  "products": ["credit_reporting_service"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "requested Chase stop reporting fraudulent accounts opened through identity theft to the credit bureaus",
  "underlying_driver": "despite a formal FCRA dispute with an FTC identity theft report and identity proof, Chase has not taken action to stop reporting the fraudulent accounts",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "fraudulent accounts still reported to credit bureaus",
      "issue_statement": "Fraudulent JPMCB Card accounts opened through identity theft are still being reported to credit bureaus despite a formal dispute with an FTC identity theft report and proof of identity.",
      "product": "credit_reporting_service",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "Chase has not acted on a formal FCRA dispute supported by an FTC identity theft report to stop reporting the fraudulent accounts",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Despite my dispute, Chase has failed to take appropriate action, causing ongoing damage to my credit report.", "speaker": "narrative"},
        {"quote": "unauthorized accounts have been fraudulently opened in my name with JPMCB Card Services", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Fraudulent JPMCB Card accounts opened through identity theft continue to be reported to credit bureaus despite a formal FCRA dispute backed by an FTC report and proof of identity."
}

R['cfpb_13027700'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "an ex-husband stole the customer's identity to open loans and credit cards, and collection agencies are now demanding payment for those debts", "is_primary": True}
  ],
  "products": ["debt_collection", "credit_reporting_service"],
  "services": [],
  "customer_ask": "other",
  "stated_reason": "explains that loans and credit cards were opened fraudulently by an ex-husband who then disappeared",
  "underlying_driver": "the ex-husband opened loans and credit cards using the customer's identity, and credit agencies confused her identity with his, leading to collection calls for debts she says are not hers",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "ex-husband opened fraudulent debts in her name",
      "issue_statement": "An ex-husband stole the customer's identity to open loans and credit cards, and collection agencies are now demanding payment for those debts after he disappeared.",
      "product": "debt_collection",
      "sentiment": -1,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "loans and credit cards opened fraudulently by an ex-husband are now being pursued by collection agencies against the customer",
      "outcome": "unknown",
      "evidence": [
        {"quote": "My ex-husband stole my identity, took out loans and credit cards in my name", "speaker": "narrative"},
        {"quote": "I started receiving calls from collection agencies demanding payment for those debts", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unknown",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "An ex-husband used identity theft to open loans and credit cards in the customer's name, and collection agencies are now pursuing her for those debts after he disappeared."
}

R['cfpb_13551430'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a $330.00 debit card charge the customer says she never made was upheld as valid despite evidence the purchase location was impossible given her work schedule", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support", "branch"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $330.00 fraudulent charge reversed",
  "underlying_driver": "Chase's own documentation showed an IP address in a distant location, and the customer's work clock-in records prove she could not have been there, yet the charge was still upheld as valid",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "fraud charge upheld despite alibi evidence",
      "issue_statement": "A $330.00 charge for jewelry from a suspicious store was upheld as valid even after the customer presented IP location data and work clock-in records proving she could not have made the purchase.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase's own IP evidence and the customer's clock-in records show the purchase location was impossible for her, but the claims department would not reverse the charge",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "they stated that their conclusion after the local Chase representative had faxed my supporting documents was the same and would not reverse the fraudulent charge", "speaker": "narrative"},
        {"quote": "which makes it impossible for me to have made a purchase from the location in XXXX XXXX", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "a branch representative faxed the supporting documents and personally explained the situation to the claims department", "category": "helpful_staff", "quote": "The Chase representative faxed the documentation to their claims department and spoke with them to explain the situation on my behalf.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A $330.00 debit card charge was upheld as valid even after the customer presented IP location data and work clock-in records proving the purchase location was impossible for her."
}

R['cfpb_14074484'] = {
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

R['cfpb_14656959'] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a legitimate $100000.00 overseas payment repeatedly failed and locked the account despite following every verification instruction", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "two escalations to Chase's Executive Office went unanswered with no reason given for the repeated payment rejections", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["phone_support"],
  "customer_ask": "explanation",
  "stated_reason": "wants to know the exact reason the payment kept being rejected and what is being done about it",
  "underlying_driver": "a $100000.00 payment kept failing and locking the account despite verifying identity and trying multiple methods over many international calls, and Chase's Executive Office never responded to two escalations",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "overseas payment repeatedly failed and locked account",
      "issue_statement": "A legitimate $100000.00 payment attempted while traveling overseas repeatedly failed and locked the account despite hours of verification calls and multiple payment methods.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "system_or_app_failure",
      "driver": "the payment failed on every attempt and repeatedly locked the account despite full identity verification and multiple payment methods tried over many international calls",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "All attempts failed, and my account was repeatedly locked, forcing me to go in circles with no resolution.", "speaker": "narrative"},
        {"quote": "No one has provided the exact reason why the payments were rejected or what steps are being taken to resolve the issue.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "A legitimate $100000.00 overseas payment repeatedly failed and locked the account despite extensive verification, and two escalations to Chase's Executive Office went unanswered."
}

R['cfpb_15311592'] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a 401(k) and Principal rollover was sent to the customer's checking account instead of the traditional IRA despite explicit wiring instructions", "is_primary": True}
  ],
  "products": ["other_or_unspecified"],
  "services": [],
  "customer_ask": "fix_error",
  "stated_reason": "wants Chase to reimburse the retirement account for its own rollover mistake",
  "underlying_driver": "Principal gave Chase explicit instructions to roll the retirement funds into the traditional IRA, but Chase deposited the money into the checking account instead, then blamed the customer for not catching it sooner",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "retirement rollover sent to checking instead of IRA",
      "issue_statement": "Despite explicit instructions to roll retirement funds into a traditional IRA, Chase deposited the money into checking instead, then said it was the customer's fault for not noticing sooner.",
      "product": "other_or_unspecified",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "Chase misdirected a retirement rollover into checking against documented instructions, then refused to reimburse the mistake and said the customer should replace the funds herself",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "principal gave Chase specific wiring instructions to roll over the money to my traditional IRA and not my checking and they still proceeded to roll over my money to my checking", "speaker": "narrative"},
        {"quote": "that I should put my own money back into my retirement account and not have them reimburse me for their own mistake", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase deposited a retirement rollover into checking instead of the traditional IRA despite explicit instructions, then told the customer to replace the funds herself instead of fixing its own mistake."
}

R['cfpb_15962539'] = {
  "contact_reasons": [
    {"reason": "loan_servicing", "specific_reason": "a mortgage error dispute has been open for four months, and the Credit Team will not accept a bank statement screenshot as evidence without explaining why", "is_primary": True}
  ],
  "products": ["mortgage"],
  "services": [],
  "customer_ask": "explanation",
  "stated_reason": "wants a written explanation of why the screenshot evidence is unacceptable and confirmation the case will keep being reviewed without further delay",
  "underlying_driver": "the Mortgage Escalation Team representative could not cite any policy or rationale for rejecting the screenshot evidence, after four months without resolution",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "screenshot evidence rejected without policy citation",
      "issue_statement": "After four months, the Credit Team refused to accept a screenshot documenting Chase's own error, insisting on a full official statement, without citing any policy or rationale when asked.",
      "product": "mortgage",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "the Credit Team rejected screenshot evidence of the error and could not provide any policy or regulation supporting the requirement when asked",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "they will only review the matter if I provide the full, official statement", "speaker": "narrative"},
        {"quote": "XXXX was unable to provide any policy, regulation, or rationale supporting this requirement", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A four-month-old mortgage error dispute remains unresolved because the Credit Team rejected screenshot evidence without being able to cite any policy requiring a full official statement instead."
}

R['cfpb_16697411'] = {
  "contact_reasons": [
    {"reason": "balance_or_statement_error", "specific_reason": "returns on a Chase credit card were applied entirely to an undisclosed 24-month Pay Over Time plan instead of the current statement balance", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wants the misapplied returns corrected so the payment plan is not paid off ahead of schedule at extra cost",
  "underlying_driver": "returns were always applied first to the Pay Over Time plan balance rather than the statement balance, a rule never disclosed when the plan was set up, and after escalating through four representatives Chase refused to reverse it",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "returns applied to payment plan instead of statement balance",
      "issue_statement": "A $3500.00, 24-month Pay Over Time plan was nearly paid off early because all card returns were applied to the plan instead of the statement balance, a rule never disclosed when the plan began.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "incorrect_or_conflicting_information",
      "driver": "returns are always applied first to the Pay Over Time plan regardless of the agreed monthly amount, undisclosed when the plan was set up; Chase refused to reverse or escalate",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "returns processed through credit cards are always first applied to payment plans regardless of the agreed monthly payment amount", "speaker": "narrative"},
        {"quote": "I was told they can not reverse this and I was also denied further escalation.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Returns on a Chase credit card were always applied to an undisclosed Pay Over Time plan instead of the statement balance, nearly paying off the 24-month plan early at extra cost, and Chase refused to reverse it or escalate."
}

R['cfpb_17273992'] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "Chase upheld a charge for a flight the airline itself cancelled and confirmed in writing it would refund", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the airline ticket charge reversed since the airline cancelled the flight",
  "underlying_driver": "Chase considered the charge valid even though the customer provided a letter from the airline confirming the flight was cancelled and would be refunded",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "dispute denied despite airline's own cancellation letter",
      "issue_statement": "Chase informed the customer it considers the airline ticket charge valid despite a letter from the airline confirming the flight was cancelled and would be refunded.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase upheld the charge as valid despite the airline's own letter confirming the flight was cancelled and a refund was due",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase informed me that they consider the charge valid despite the fact that I have a letter from the airline that they would refund me", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase upheld a disputed airline ticket charge as valid even though the customer submitted the airline's own letter confirming the flight was cancelled and a refund was due."
}

R['cfpb_18274024'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "$6000.00 from a deposited check has been held since the account was closed because Chase says it could not verify the check maker", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting immediate release of the funds or return of them to the check maker's bank",
  "underlying_driver": "Chase closed the account and has held $6000.00 well beyond a reasonable investigation period because it says it cannot verify the nonresponsive check maker",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "closed account still holding $6000.00",
      "issue_statement": "Chase closed the account and has continued holding $6000.00 from a deposited check far beyond a reasonable investigation period because it says it cannot verify the nonresponsive check maker.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "$6000.00 remains held well beyond a reasonable investigation period, with Chase refusing to either release it to the customer or return it to the maker's bank",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "Chase closed my account in XXXX and has continued to hold $6000.00 from a deposited check because they claim they could not verify the check maker.", "speaker": "narrative"},
        {"quote": "is refusing to either release the funds to me or return the funds to the makers bank", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "Chase closed the account and has held $6000.00 from a deposited check far beyond a reasonable investigation period, refusing to either release the funds or return them to the maker's bank."
}

R['cfpb_18727343'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a tax refund and settlement check deposit was held past the promised release date and then the account was restricted", "is_primary": True},
    {"reason": "account_opening_or_closure", "specific_reason": "the account was closed based on a claimed prior fraudulent account matched only by social security number", "is_primary": False},
    {"reason": "unauthorized_or_fraud", "specific_reason": "the checks were called fictitious even though they later cleared, and the account closure was blamed on an account the customer says she never opened", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch", "phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants her money released after the checks cleared and the account was closed",
  "underlying_driver": "two legitimate checks were held past the date staff promised release, then the account was restricted and closed over a supposed prior fraudulent account matched only by social security number, leaving the family without funds for basic needs",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "check hold extended past promised release date",
      "issue_statement": "A tax refund and settlement check deposit was held past the date multiple representatives promised the funds would be released in full.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "representatives repeatedly promised the hold would be released on specific dates, but the funds were not released each time",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "the person i spoke with assured them they would be clear after the holiday in the a full amount", "speaker": "narrative"},
        {"quote": "They told me the funds would be released later that day but they never did.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "account closed over unrelated fraud match",
      "issue_statement": "The account was restricted and closed after Chase said her social security number matched a fraudulent account she never opened, and the deposited checks were called fictitious though they later cleared.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "the account was closed over a social security number match to an account the customer says she never opened, and the checks were called fictitious despite later clearing",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "your social came back as a match to having an account", "speaker": "narrative"},
        {"quote": "they accused my checks to be fictacious. which they weren't and came back and cleared", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A tax refund and settlement check deposit was held past repeated promised release dates, and the account was then restricted and closed over a social security number match to a fraudulent account the customer denies opening, leaving her family without funds."
}

R['cfpb_19795904'] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "a Chase Ultimate Rewards points transfer took 11 days instead of the promised 7, causing the needed award to become unavailable and a loss of miles value", "is_primary": True}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants Chase to honor the compensation a representative explicitly promised for the mile loss caused by the delay",
  "underlying_driver": "Chase acknowledged a point transfer took 11 days instead of the promised 7 days, causing a needed saver award to become unavailable, and then refused to honor a representative's explicit promise to compensate for the difference",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "delayed points transfer voided promised compensation",
      "issue_statement": "A Chase points transfer took 11 days instead of the promised 7, making a saver-level flight award unavailable and forcing a higher mileage redemption, and Chase then refused to honor a promised compensation.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "Chase acknowledged the transfer delay in writing and a representative promised compensation for the resulting mile loss, but a later letter refused to honor that promise",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "the transfer was not completed until XX/XX/year>, taking 11 days", "speaker": "narrative"},
        {"quote": "Chase issued a written letter stating that although there was a delay in processing the transfer, it would not provide any compensation and would not honor the prior customer service commitment", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A Chase points transfer took 11 days instead of the promised 7, causing a needed saver-level flight award to become unavailable, and Chase later refused to honor a representative's explicit promise to compensate for the resulting mile loss."
}

R['cfpb_20279849'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "$5000.00 in debit card transactions to a merchant the customer never used were ruled not fraud with no explanation, while the merchant says it has no record of the transactions", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": ["mobile_app"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $5000.00 in transactions refunded and believes either Chase or the merchant is responsible for the fraud",
  "underlying_driver": "Chase found no fraud without stating its findings, while the merchant told the customer it has no record of the transactions or his information at all",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "fraud ruled out with no findings given",
      "issue_statement": "Chase ruled that $5000.00 in transactions to an unfamiliar merchant were not fraud without stating its findings, while the merchant says it has no record of the transactions or the customer.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "denied_or_declined_without_explanation",
      "driver": "Chase found no fraud without disclosing its findings, even though the merchant itself says it has no record of the customer or the transactions",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "I got a notification in my Chase app saying no fraud was found although they did not state there investigation findings", "speaker": "narrative"},
        {"quote": "I am giving CFCB the right to publish this publicly unless chases fixes the issue then I will update the report accordingly", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "Chase ruled out fraud on $5000.00 in transactions to an unfamiliar merchant without disclosing its findings, even though the merchant itself says it has no record of the customer or the transactions."
}

R['cfpb_21385013'] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a government impersonation scam used the customer's Chase banking information, and Chase denies responsibility for the resulting loss", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants Chase to make her whole again after the scam and to warn other customers about it",
  "underlying_driver": "a government impersonation scam that specifically references Chase Bank used the customer's personal banking information, and Chase refuses to accept any culpability or warn other customers",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "government impersonation scam using chase information",
      "issue_statement": "A government impersonation scam that specifically references Chase Bank used the customer's personal banking information, and Chase refuses to accept culpability or reimburse the loss.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "fraud_not_stopped_or_not_refunded",
      "driver": "Chase will not accept responsibility or reimburse a loss from a scam that uses its own name and the customer's banking information, and has issued no warning to other customers",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "They refuse to accept their culpability in this scam.", "speaker": "narrative"},
        {"quote": "I want Chase to make me whole again because they did not protect my information.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A government impersonation scam used the customer's Chase banking information and its name directly, and Chase refuses to accept responsibility, reimburse the loss, or warn other customers."
}

R['cfpb_22628179'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a first paycheck deposit could not be verified, so the account was restricted and then closed, and the funds still have not been received months later", "is_primary": True}
  ],
  "products": ["checking_or_savings"],
  "services": [],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the paycheck funds that were withheld after the account closure",
  "underlying_driver": "Chase could not verify a first paycheck deposit, restricted then closed the account, and months later the earned money still has not been received",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "paycheck withheld after unverified deposit closure",
      "issue_statement": "A first paycheck deposit could not be verified by Chase, leading to the account being restricted and then closed, and months later the money for hours worked still has not been received.",
      "product": "checking_or_savings",
      "sentiment": -1,
      "driver_category": "money_held_or_not_returned",
      "driver": "Chase restricted then closed the account over an unverified paycheck deposit, and the earned funds are still unpaid months later, causing missed bills",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "they say they couldnt verify my check so they restricted my account and then closed it", "speaker": "narrative"},
        {"quote": "Were currently approaching month XXXX and I still havent received what I worked a hard XXXX hrs for", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "A first paycheck deposit could not be verified, leading Chase to restrict and close the account, and months later the customer still has not received the pay for hours she worked."
}

R['cfpb_23342912'] = {
  "contact_reasons": [
    {"reason": "fees_and_charges", "specific_reason": "a $150.00 annual membership fee was reassessed on a card the customer had already gone through the process of closing", "is_primary": True},
    {"reason": "credit_reporting", "specific_reason": "a late payment stemming from the wrongly reassessed fee remains on the credit report even after the fee and late fees were removed", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wants the late payment removed from the credit report since the underlying fee was waived and never should have existed",
  "underlying_driver": "the card was not actually closed as promised, so the annual fee was charged again along with late fees, and even after those were waived, the resulting late payment mark was verified and kept on the credit report, dropping the score sharply",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "annual fee reassessed on card believed closed",
      "issue_statement": "A $150.00 annual membership fee was charged again on a United Airlines Explorer card the customer had gone through hoops to close, followed by late fees on that unpaid fee.",
      "product": "credit_card",
      "sentiment": 1,
      "driver_category": "fair_outcome",
      "driver": "after escalation, Chase apologized and removed both the wrongly reassessed annual fee and the resulting late fees, and reconfirmed the card as closed",
      "outcome": "resolved",
      "evidence": [
        {"quote": "Unfortunately this year I found out that the card was not closed and they again assessed the annual fee.", "speaker": "narrative"},
        {"quote": "They apologized and removed both the late fees and the annual membership fee, and again confirmed that the card was now closed.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "late payment stays on credit report",
      "issue_statement": "Even after the wrongly charged annual fee and its late fees were removed, the resulting late payment mark was verified and remains on the credit report, dropping the score sharply.",
      "product": "credit_card",
      "sentiment": -2,
      "driver_category": "error_not_corrected",
      "driver": "a late payment based on a fee that was waived and never should have existed was verified and kept on the credit report, dropping the score from its prior level",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "they verified the charge and it remains on my credit to the detriment of XXXX points", "speaker": "narrative"},
        {"quote": "This is unacceptable.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "partially_resolved",
  "positive_moments": [
    {"what": "Chase apologized and removed the wrongly reassessed annual fee and late fees after escalation", "category": "fair_outcome", "quote": "They apologized and removed both the late fees and the annual membership fee", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A wrongly reassessed annual fee and its late fees on a card believed closed were eventually waived after escalation, but the resulting late payment mark was still verified and kept on the customer's credit report, dropping the score sharply."
}

R['cfpb_9554100'] = {
  "contact_reasons": [
    {"reason": "credit_reporting", "specific_reason": "Chase reported the account as delinquent even though the customer made every payment on a no-interest plan a representative said would not be reported late", "is_primary": True},
    {"reason": "terms_information_or_communication", "specific_reason": "different Chase representatives gave conflicting information about the balance and the payment plan enrollment", "is_primary": False}
  ],
  "products": ["credit_card"],
  "services": ["phone_support"],
  "customer_ask": "fix_error",
  "stated_reason": "wants the inaccurate delinquent reporting corrected since all scheduled payments were made on time",
  "underlying_driver": "a representative promised enrollment in a no-interest payment plan would not be reported as past due if payments were made on time, but Chase later reported the account delinquent despite the payments being made",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "account reported delinquent despite on-time plan payments",
      "issue_statement": "Chase reported the $230.00 balance as delinquent to credit bureaus even though the customer made all three scheduled $77.00 payments on time under a plan a representative promised would not be reported late.",
      "product": "credit_card",
      "sentiment": -1,
      "driver_category": "error_not_corrected",
      "driver": "a representative promised the no-interest plan would not be reported past due if paid on time, but Chase reported it delinquent anyway and gave conflicting account information",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "this representative told me no as long as youre making the $77.00 increment payments on time", "speaker": "narrative"},
        {"quote": "chase reported to credit bureaus that I havent paid anything on my credit card. Reported it as delinquent when thats indeed not true.", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -1,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": False,
  "summary": "A representative promised a no-interest payment plan would not be reported late if paid on time, but Chase reported the account delinquent anyway, dropping the customer's credit score despite all payments being made."
}

R['cfpb_9834882'] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "the account was frozen with an 8-day hold after a stop payment on a check, cutting off access to money and direct deposits", "is_primary": True},
    {"reason": "fees_and_charges", "specific_reason": "two bounced check fees were charged for what should have been only one stop payment", "is_primary": False}
  ],
  "products": ["checking_or_savings"],
  "services": ["branch", "phone_support"],
  "customer_ask": "refund_or_reversal",
  "stated_reason": "wants access to her money and direct deposits restored and the extra bounced check fee removed",
  "underlying_driver": "an 8-day hold followed a stop payment on a check, cutting off access to funds and direct deposits, while two bounced check fees were charged for what should have been one stop payment",
  "reason_differs": False,
  "topics": [
    {
      "topic_label": "account frozen after stop payment",
      "issue_statement": "Chase froze the account with an 8-day hold after a stop payment on a check, cutting off access to money and direct deposits since that date.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "money_held_or_not_returned",
      "driver": "an 8-day hold followed a stop payment, leaving the account frozen with no access to money or direct deposit for an extended period",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "chase put 8 day hold on it!", "speaker": "narrative"},
        {"quote": "I havent my money or any direct since XX/XX/XXXX.", "speaker": "narrative"}
      ]
    },
    {
      "topic_label": "double bounced check fee for one stop payment",
      "issue_statement": "Two bounced check fees were charged even though only one stop payment was made.",
      "product": "checking_or_savings",
      "sentiment": -2,
      "driver_category": "unexpected_charge",
      "driver": "two bounced check fees were applied for what was only one stop payment",
      "outcome": "unresolved",
      "evidence": [
        {"quote": "gone bounce check fee only one stop payment", "speaker": "narrative"},
        {"quote": "I didnt owe chase any money double bounce check fee!", "speaker": "narrative"}
      ]
    }
  ],
  "overall_sentiment": -2,
  "resolution_status": "unresolved",
  "positive_moments": [],
  "redaction_heavy": True,
  "summary": "An 8-day hold following a stop payment froze access to money and direct deposits, and two bounced check fees were charged for what should have been only one stop payment."
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
