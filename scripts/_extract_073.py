import json, pathlib
out = pathlib.Path(r"C:/Users/RicardsonAlbuquerque/repos/Hack/data/cache/extract")

records = {}

records["cfpb_9801592"] = {"key": "8476118e9d7f40bb86ab63c3fb57f677d140c162d2a85e745d5962386e28ecdf", "response": {
    "contact_reasons": [{"reason": "rewards_or_promotions", "specific_reason": "a $300.00 promotional statement credit for qualifying hotel stays was never extended after months of calls", "is_primary": True}],
    "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "applied for a Chase credit card for a $300.00 promotional statement credit after staying at qualifying hotels, but the credit was never extended",
    "underlying_driver": "after months of calls being told the claim was valid and escalated, a supervisor finally said a billing system error prevented the promotion, and the case was pushed to marketing to decide",
    "reason_differs": False,
    "topics": [{"topic_label": "promotional hotel credit never honored", "issue_statement": "A $300.00 promotional statement credit for staying at qualifying hotels was never applied despite meeting the terms, after months of being told the claim was valid and being escalated.", "product": "credit_card", "sentiment": -2, "driver_category": "denied_or_declined_without_explanation", "driver": "promised $300.00 hotel credit never posted; blamed on a billing system error the customer says is false since the stays clearly qualified", "outcome": "unresolved", "evidence": [
        {"quote": "I would call several times a month, for the last XXXX  months, to claim my credit and was told I had a valid claim and my issue was being escalated to a supervisor or other department that could approve and post the credit.", "speaker": "narrative"},
        {"quote": "This is completely FALSE, when the representative himself acknowledges that we in fact have stayed a XXXX different XXXX Hotels and it was for this sole reason I applied for the card to begin with.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A $300.00 promotional hotel credit was never applied despite meeting the terms; after months of calls a supervisor blamed a billing system error and pushed the case to marketing."
}}

records["cfpb_10121767"] = {"key": "ece4e59e32ef7ce5ae32339a5942a1068b774f4127a780b50ee609a002ba6a62", "response": {
    "contact_reasons": [
        {"reason": "rewards_or_promotions", "specific_reason": "the advertised $300.00 first-flight credit did not apply and the billed amount did not match what was shown at purchase", "is_primary": True},
        {"reason": "fees_and_charges", "specific_reason": "two late fees charged while disputing the billing error despite being told there would be none", "is_primary": False}
    ],
    "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "a $300.00 first-flight promotional credit did not apply, resulting in an unexpected billed amount",
    "underlying_driver": "Chase told the customer to wait 12-14 days without late fees while disputing, but two late fees were charged anyway with no resolution",
    "reason_differs": False,
    "topics": [
        {"topic_label": "promo not applied to first flight purchase", "issue_statement": "A $300.00 promotional credit for the first Southwest flight did not apply as advertised, and the amount billed did not match the $39.00 the customer saw at purchase.", "product": "credit_card", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "the advertised $300.00 first-flight credit was not applied and the amount charged did not match what was shown at purchase", "outcome": "unresolved", "evidence": [
            {"quote": "when I purchased the flight, the total that was shown that would be put on my card was $39.00 for the flight, due to the special offer that was going on.", "speaker": "narrative"},
            {"quote": "I got my first statement towards the end of XXXX, and the total for the flight, and on my card was as stated above.", "speaker": "narrative"}
        ]},
        {"topic_label": "late fees charged during promised grace period", "issue_statement": "Chase told the customer to wait 12-14 days without incurring a late fee while disputing the billing error, but two late fees were charged anyway.", "product": "credit_card", "sentiment": -1, "driver_category": "unexpected_charge", "driver": "two late fees charged despite being told a payment due during the 12-14 day wait would not trigger one", "outcome": "unresolved", "evidence": [
            {"quote": "they told me to wait 12-14 days to receive something in the mail, and during this time if a payment would come due I wouldn't receive a late fee.", "speaker": "narrative"},
            {"quote": "Now, after trying to dispute this incident and get it corrected, I have received two late fees and no understanding from Chase Bank.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A promised $300.00 first-flight credit never applied correctly and two late fees were charged during the promised dispute grace period, with no resolution from Chase."
}}

records["cfpb_10419001"] = {"key": "95e584955396e56bcb6ecc26181e17e9dc92cd8a4ccefc3ece6a42e9bcba406c", "response": {
    "contact_reasons": [
        {"reason": "funds_hold_or_account_restriction", "specific_reason": "available balance and credit held for extra business days after a $200.00 automatic payment posted", "is_primary": True},
        {"reason": "terms_information_or_communication", "specific_reason": "the delay policy tied to a prior returned payment was never disclosed in writing or in advance", "is_primary": False}
    ],
    "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "fix_error",
    "stated_reason": "a $200.00 automatic payment was taken from checking, but the credit card's available balance/credit was not updated as expected",
    "underlying_driver": "a new undisclosed policy delays balance updates after any returned payment, without required advance notice, and supervisors could not explain further",
    "reason_differs": False,
    "topics": [{"topic_label": "delayed credit update after past returned payment", "issue_statement": "A $200.00 automatic payment was deducted from checking, but the available balance and credit were held for extra business days due to an undisclosed policy tied to a prior returned payment.", "product": "credit_card", "sentiment": -2, "driver_category": "policy_or_terms_change", "driver": "available balance/credit held for extra business days after a returned payment months earlier, a change never disclosed to the customer", "outcome": "unresolved", "evidence": [
        {"quote": "I became extremely upset and requested to speak to a supervisor and upon speaking with him, he merely repeated the same thing that the previous representative had stated!", "speaker": "narrative"},
        {"quote": "the bank did not inform me that this change was taking place, did not provide me/or share with me that this change was occurring in writing, nor did they provide a time frame associated with this significant change", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A $200.00 automatic payment posted but the credit card's available balance was held for extra days under an undisclosed delay policy tied to a past returned payment, leaving the customer extremely upset."
}}

records["cfpb_10871051"] = {"key": "51f0455d7b5729a4c4174fbc2a853550cdfce74828c6fad1705f162191f67627", "response": {
    "contact_reasons": [{"reason": "payment_or_transfer_problem", "specific_reason": "a $22,000.00 international wire was debited but the beneficiary says it was never received, and JP Morgan stopped responding", "is_primary": True}],
    "products": ["money_transfer_or_p2p"], "services": ["branch"], "customer_ask": "refund_or_reversal",
    "stated_reason": "an in-person international wire transfer of $22,000.00 was taken from the account, but the beneficiary claims it was never received",
    "underlying_driver": "despite repeated communications from the beneficiary bank requesting the funds be returned, JP Morgan stopped responding entirely",
    "reason_differs": False,
    "topics": [{"topic_label": "$22,000 wire not received, bank unresponsive", "issue_statement": "A $22,000.00 international wire was taken from the account, the beneficiary says it was never received, and JP Morgan stopped responding to requests to return the funds.", "product": "money_transfer_or_p2p", "sentiment": -1, "driver_category": "no_response_or_follow_up", "driver": "JP Morgan quit responding to the beneficiary bank's repeated requests to return the missing $22,000.00 wire", "outcome": "unresolved", "evidence": [
        {"quote": "The money was taken out of my account and the beneficiary claimed to have not received it.", "speaker": "narrative"},
        {"quote": "Finally XXXX XXXX XXXX  requested the funds be returned XXXX from JP morgan and JP Morgan never responded and has quit responding to all requests.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A $22,000.00 international wire never reached the beneficiary, and JP Morgan has stopped responding to repeated requests from the beneficiary bank to return the funds."
}}

records["cfpb_11159684"] = {"key": "5bb97c280a6777108eba7564ea19795d7953047bfdf34c2c714b267d6a3adfd0", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "received a phishing email impersonating Chase Bank about FBI-recovered compensation funds requesting personal information", "is_primary": True}],
    "products": ["other_or_unspecified"], "services": ["chat_or_email"], "customer_ask": "escalation_or_complaint",
    "stated_reason": "received a scam email impersonating Chase Bank claiming FBI-recovered compensation funds and requesting personal information",
    "underlying_driver": "the customer is reporting this phishing attempt that used Chase's name, quoting it directly as what was told to them",
    "reason_differs": False,
    "topics": [{"topic_label": "phishing email impersonating chase bank", "issue_statement": "The customer received an email impersonating Chase Bank claiming FBI-recovered compensation funds were owed and asking for personal information to claim them.", "product": "other_or_unspecified", "sentiment": 0, "driver_category": "other_or_unclear", "driver": "received an unsolicited email using Chase's name to request personal information under a fake compensation-fund claim", "outcome": "unknown", "evidence": [
        {"quote": "We want to inform you that the Federal Bureau of Investigation ( FBI ) has assigned the payment of the recently recovered unpaid poverty alleviation and economic relief compensation funds to this reputable banking institution", "speaker": "narrative"},
        {"quote": "Upon receipt of this email, send your personal information to ( XXXX ) to apply for your overdue compensation fund claims.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": 0, "resolution_status": "unknown", "positive_moments": [], "redaction_heavy": False,
    "summary": "The customer forwarded a phishing email impersonating Chase Bank that promised FBI-recovered compensation funds in exchange for personal information."
}}

records["cfpb_11491063"] = {"key": "491576728f8ee5ede792e37f758ca007193a71878fb63242b361bf6b34c7ab20", "response": {
    "contact_reasons": [{"reason": "loan_servicing", "specific_reason": "the mortgage assumption to remove the ex-husband's name has been denied twice for shifting, never-mentioned reasons", "is_primary": True}],
    "products": ["mortgage"], "services": ["phone_support"], "customer_ask": "fix_error",
    "stated_reason": "has been trying for over six months to assume the mortgage and remove the ex-husband's name, but Chase keeps changing requirements and denying for shifting reasons",
    "underlying_driver": "after meeting one set of conditions, the application was still denied for different reasons, and the second application faced new demands including explaining name variations, extending the process for months",
    "reason_differs": False,
    "topics": [
        {"topic_label": "denied after meeting conditions to pay off debts", "issue_statement": "After paying off a credit card and car note as a condition, the mortgage assumption application to remove the ex-husband's name was still denied, citing reasons never mentioned before requiring those payments.", "product": "mortgage", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information", "driver": "denied the mortgage assumption citing missing documents that were never mentioned before being told to pay off a car and credit card as a condition of approval", "outcome": "unresolved", "evidence": [
            {"quote": "They had me pay off a cc and my car note as a condition of approval, which was a brand new car, then still did not approve me.", "speaker": "narrative"},
            {"quote": "They told me the reason for denial was because of documents asked for months before asking me to pay off my car, so why even have me do that?!", "speaker": "narrative"}
        ]},
        {"topic_label": "asked to explain ethnic name variations", "issue_statement": "After resubmitting a complete package, Chase asked for an explanation of variations in the customer's name on the credit report, which the customer felt was a microaggression tied to having an ethnic name.", "product": "mortgage", "sentiment": -1, "driver_category": "staff_attitude_or_competence", "driver": "asked to explain typo-driven name variations on the credit report, which felt targeted given it concerned an ethnic name", "outcome": "unresolved", "evidence": [
            {"quote": "they send me a letter saying they need an explanation for variations of my name on my credit report, which were clearly typos.", "speaker": "narrative"},
            {"quote": "I felt like the ask for an explanation of variations in my name was a micro aggression because its an ethnic name.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A months-long mortgage assumption to remove an ex-husband's name has been denied twice for shifting, previously unmentioned reasons, and the customer felt singled out when asked to explain typo-driven variations of an ethnic name."
}}

records["cfpb_12049940"] = {"key": "9f9c909460e2d8bfb49e001b8863581a1e727a69699bd092484716168b630887", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "funds taken through an app that stored the customer's information; the bank gave no proof of authorization", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["mobile_app"], "customer_ask": "refund_or_reversal",
    "stated_reason": "funds were taken through an app that stored the customer's information, and the bank gave no proof after the customer disputed the unauthorized transactions",
    "underlying_driver": "a month later, the same bank is causing more security errors, compounding the problem while the customer urgently needs the funds to pay a small business crew",
    "reason_differs": False,
    "topics": [{"topic_label": "unauthorized transactions with no proof of authorization", "issue_statement": "Funds were taken through an app that stored the customer's information, and the bank offered no proof that the customer authorized the transactions.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "bank gave no proof of authorization for disputed transactions and provided no resolution", "outcome": "unresolved", "evidence": [
        {"quote": "I told my bank that I did not authorize the said transactions and I would like to get to the bottom of it but the bank was no help and gave me no proof of me approving transactions.", "speaker": "narrative"},
        {"quote": "Now I am going through more security errors with the same bank a MONTH later.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Funds were taken through a compromised app with no proof of authorization from the bank, and a month later the same bank is causing more security errors while the customer needs the money to pay a crew."
}}

records["cfpb_12452287"] = {"key": "723c49c56a36ea9bc15adc15db764e19bdc3179d50e8ca9fca20a0ff58f6f586", "response": {
    "contact_reasons": [
        {"reason": "unauthorized_or_fraud", "specific_reason": "two unexplained $300.00 'GD-Loan' charges totaling $600.00 hit the checking account", "is_primary": True},
        {"reason": "dispute_or_chargeback", "specific_reason": "the temporary credit for the disputed charges was revoked without proof of the merchant's identity", "is_primary": False}
    ],
    "products": ["checking_or_savings"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "two unexplained $300.00 charges labeled 'GD-Loan' totaling $600.00 hit the checking account, and Chase revoked the temporary credit claiming the charges were authorized",
    "underlying_driver": "Chase could not correctly identify the merchant and still has not returned the funds despite the customer confirming with the falsely named company that it had no relation",
    "reason_differs": False,
    "topics": [{"topic_label": "unexplained charges, credit revoked without proof", "issue_statement": "Two unexplained $300.00 charges labeled 'GD-Loan' totaling $600.00 were disputed, and Chase revoked the temporary credit claiming the charges were authorized without providing the merchant's identity.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "temporary credit for $600.00 in unrecognized 'GD-Loan' charges was revoked as 'authorized' with no proof, and the merchant Chase first named denied any relation", "outcome": "unresolved", "evidence": [
        {"quote": "On XX/XX/year> they revoke the credit stating the charges was authorized but did not provide me with a number or actual company name.", "speaker": "narrative"},
        {"quote": "First the Chase claim representative stated the charges came from XXXX XXXX XXXX, I told them they were paid on the second of XXXX and another loan was not done. I contacted the company to make sure and they stated they are not affiliated with GD-Loan and no new charges was added to my account by them.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Two unexplained $300.00 'GD-Loan' charges were disputed, and Chase revoked the temporary credit as 'authorized' without identifying the merchant, even after the customer confirmed with the company Chase named that it was uninvolved."
}}

records["cfpb_12952933"] = {"key": "0b0989af797952266969ca26c9cee3bdeddfdeaec5af7bb50db92ae8a2094a84", "response": {
    "contact_reasons": [{"reason": "credit_decision_or_limit", "specific_reason": "denied auto loan credit, allegedly because the dealership never forwarded the submitted financial package to Chase", "is_primary": True}],
    "products": ["auto_loan"], "services": [], "customer_ask": "fix_error",
    "stated_reason": "was denied credit for an auto loan application, allegedly because the dealership failed to forward a complete financial package to JPMorgan Chase",
    "underlying_driver": "the dealership repeatedly failed to send required documents to Chase and legal, causing a wrongful denial and an ongoing dispute",
    "reason_differs": False,
    "topics": [{"topic_label": "credit denied due to dealership's failure to forward documents", "issue_statement": "Chase issued an adverse action denying credit for the auto loan, which the customer attributes to the dealership never forwarding the complete financial package that was submitted.", "product": "auto_loan", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "credit denied by JPMorgan Chase allegedly because the dealership never forwarded the submitted financial package to the CFO or legal", "outcome": "unresolved", "evidence": [
        {"quote": "This complaint involves misconduct by XXXX XXXX XXXX XXXX and their failure to forward my secured credit package to JPMorgan Chase, resulting in an unlawful denial of credit.", "speaker": "narrative"},
        {"quote": "XX/XX/year> Received adverse action letter from JPMorgan Chase.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "An auto loan application was denied by JPMorgan Chase, which the customer attributes to the dealership never forwarding the submitted financial package to the CFO or legal department."
}}

records["cfpb_13467917"] = {"key": "cb62bd73c8e31bf9e883f8dadbc70ec73c92000d650ea39d11465c93382bc5b9", "response": {
    "contact_reasons": [
        {"reason": "payment_or_transfer_problem", "specific_reason": "an ATM withdrawal displayed an error but the money was still taken, then a refund was reversed", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "branch managers and supervisors refused to review the ATM video footage", "is_primary": False}
    ],
    "products": ["checking_or_savings"], "services": ["atm", "branch", "phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "an ATM withdrawal failed with an 'unable to dispense cash' message but the money was still taken from the account",
    "underlying_driver": "the bank initially credited the funds back then reversed and took them again, and branch managers and supervisors refused to review the video footage",
    "reason_differs": False,
    "topics": [
        {"topic_label": "ATM took money without dispensing", "issue_statement": "An ATM withdrawal displayed 'unable to dispense cash' but still took the money from the account; the bank credited it back then reversed and took it again.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "funds were credited back after the failed ATM withdrawal, then reversed and taken again without explanation", "outcome": "unresolved", "evidence": [
            {"quote": "the atm machine on the screen said unable to dispense cash at this time.However the machine still took XXXX out of my account without me receiving anything.", "speaker": "narrative"},
            {"quote": "they transferred the XXXX back into my account XXXX XXXX and then they reversed it XXXX XXXX and took it bank out.", "speaker": "narrative"}
        ]},
        {"topic_label": "refusal to review video footage", "issue_statement": "Multiple branch managers and supervisors refused to review the ATM's video footage to confirm what happened.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "branch managers and phone supervisors declined to review the ATM video footage to verify the failed withdrawal", "outcome": "unresolved", "evidence": [
            {"quote": "Ive spoken to XXXX branch managers a XXXX supervisors over the phone to review the video footage and they said they cant do it unless its XXXX", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "An ATM took money without dispensing it; the bank briefly refunded it then reversed the refund, and branch managers refused to review video footage."
}}

records["cfpb_14019357"] = {"key": "30e668a5689f1eed81cb72bb04ec3a7d307d3b8887654d276c5d89b053704f8b", "response": {
    "contact_reasons": [{"reason": "payment_or_transfer_problem", "specific_reason": "a $2,500.00 ATM deposit malfunctioned and $800.00 of a temporary credit was reversed without explanation", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["atm"], "customer_ask": "refund_or_reversal",
    "stated_reason": "a $2,500.00 ATM cash deposit malfunctioned and did not credit the full amount; Chase later reversed $800.00 of a temporary credit claiming only $1,700.00 was accounted for",
    "underlying_driver": "Chase has not explained how the missing $800.00 disappeared or what evidence supported the reversal despite the customer's clean five-year deposit history",
    "reason_differs": False,
    "topics": [{"topic_label": "$800 reversed from ATM deposit dispute", "issue_statement": "A $2,500.00 ATM cash deposit malfunctioned, and after issuing a temporary credit, Chase reversed $800.00 saying only $1,700.00 was accounted for, without explaining how the rest disappeared.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "$800.00 of a $2,500.00 ATM deposit reversed as unaccounted for, with no explanation or audit evidence provided", "outcome": "unresolved", "evidence": [
        {"quote": "On XX/XX/year>, Chase reversed $800.00 of that temporary credit, stating that only $1700.00 was accounted for by the ATM.", "speaker": "narrative"},
        {"quote": "Chase has not explained how the missing $800.00 could have disappeared or what specific evidence they used to make their determination.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "An ATM malfunctioned during a $2,500.00 cash deposit, and Chase reversed $800.00 of a temporary credit without explaining how the amount went unaccounted for."
}}

records["cfpb_14589707"] = {"key": "92f42169aeca1664893cf7540ef6ee231b8cf541295b102d376fc05907dd16d6", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "scammed into cash app purchases connected to the Chase account; the fraud claim was denied as final without review", "is_primary": True}],
    "products": ["checking_or_savings", "money_transfer_or_p2p"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "was scammed into cash app purchases connected to the Chase account and provided evidence, but the fraud claim was denied as final",
    "underlying_driver": "Chase never reviewed the letter, screenshots, and fraud timeline submitted as proof",
    "reason_differs": False,
    "topics": [{"topic_label": "fraud claim denied without reviewing evidence", "issue_statement": "Scammed into cash app purchases connected to the Chase account, the customer provided a letter and evidence, but the claim was denied as final without Chase reviewing the proof.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "fraud claim denied as final despite a submitted letter, screenshots and fraud timeline, which Chase never reviewed", "outcome": "unresolved", "evidence": [
        {"quote": "I provided Chase with a letter and supporting evidence, including screenshots and a fraud timeline, but my claim was denied. I was told it's final, despite clearly being manipulated.", "speaker": "narrative"},
        {"quote": "Chase never reviewed the proof", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A fraud claim over scam-induced cash app purchases was denied as final, and Chase never reviewed the letter, screenshots and fraud timeline the customer submitted as proof."
}}

records["cfpb_15235728"] = {"key": "5a6f6ffa8f56424a520c9923eeda1640fcf92802c3b01f992d60d9451a6c1fd3", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "a fraudulent credit card application was closed by Chase, but the credit bureau still performed a hard credit pull", "is_primary": True}],
    "products": ["credit_card", "credit_reporting_service"], "services": ["phone_support"], "customer_ask": "fix_error",
    "stated_reason": "received notice of a fraudulent credit card application; Chase closed it but the credit bureau still performed a hard credit pull",
    "underlying_driver": "to dispute the credit pull now on file, the customer was told they would need to file with the FTC rather than have it removed directly",
    "reason_differs": False,
    "topics": [{"topic_label": "fraudulent application closed but credit pull remains", "issue_statement": "A fraudulent credit card application was closed by Chase, but the credit bureau still performed a hard pull that now requires an FTC filing to dispute.", "product": "credit_reporting_service", "sentiment": -1, "driver_category": "error_not_corrected", "driver": "credit bureau's hard pull from the fraudulent application was not simply removed; customer must file a separate FTC report to dispute it", "outcome": "unresolved", "evidence": [
        {"quote": "Chase closed the application and told me to call XXXX.", "speaker": "narrative"},
        {"quote": "XXXX pulled my credit for the application and told me in order to dispute the credit pull I would need to file with the FTC.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "partially_resolved",
    "positive_moments": [{"what": "Chase closed the fraudulent application after being notified", "category": "fast_resolution", "quote": "Chase closed the application and told me to call XXXX.", "speaker": "narrative"}],
    "redaction_heavy": False,
    "summary": "A fraudulent credit card application was closed by Chase, but the resulting credit bureau hard pull remains and now requires a separate FTC filing to dispute."
}}

records["cfpb_15865617"] = {"key": "1e1d5ffd213b459099b9bc2bec3ae9abee979bb775d61f008219d4ae134ffbfd", "response": {
    "contact_reasons": [{"reason": "payment_or_transfer_problem", "specific_reason": "a $2,200.00 balance transfer was sent to a financial institution that does not appear to exist", "is_primary": True}],
    "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "a $2,200.00 balance transfer was sent by Chase to the wrong, seemingly nonexistent, financial institution",
    "underlying_driver": "despite this being Chase's error, they claim it is the customer's responsibility to recover the funds, and dozens of calls produced only conflicting information",
    "reason_differs": False,
    "topics": [{"topic_label": "balance transfer sent to nonexistent institution", "issue_statement": "Chase sent a $2,200.00 balance transfer to a financial institution that does not appear to exist, and claims recovering the funds is the customer's responsibility.", "product": "credit_card", "sentiment": -2, "driver_category": "error_not_corrected", "driver": "Chase sent the $2,200.00 balance transfer to a nonexistent institution and insists it is the customer's job to recover it", "outcome": "unresolved", "evidence": [
        {"quote": "Chase sent the funds to the wrong financial institution XXXX XXXX XXXX XXXX which does not appear to exist. Ive been unable to locate this bank or verify any contact information for it. Despite this, Chase claims it is my responsibility to recover the funds.", "speaker": "narrative"},
        {"quote": "Their lack of follow-up, negligence, and refusal to resolve the issue is unacceptable.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Chase sent a $2,200.00 balance transfer to a seemingly nonexistent institution and insists the customer must recover it themselves, after dozens of calls yielded only conflicting information."
}}

records["cfpb_16605650"] = {"key": "d3ec49e15fc77c2f809d999f82bef328c583bde07de9fbba904980bd10be5369", "response": {
    "contact_reasons": [{"reason": "customer_service_experience", "specific_reason": "a supervisor was extremely rude and sarcastic and refused to transfer to a manager", "is_primary": True}],
    "products": ["other_or_unspecified"], "services": ["phone_support"], "customer_ask": "escalation_or_complaint",
    "stated_reason": "spoke with a supervisor who was extremely rude and sarcastic and refused to connect to a manager",
    "underlying_driver": "unable to get help resolving the original inquiry due to the supervisor's unhelpful and hard-to-understand responses",
    "reason_differs": False,
    "topics": [{"topic_label": "rude, unhelpful supervisor", "issue_statement": "A supervisor was extremely rude and sarcastic on the phone, refused to transfer to a manager, and was difficult to understand, leaving the original inquiry unresolved.", "product": "other_or_unspecified", "sentiment": -1, "driver_category": "staff_attitude_or_competence", "driver": "supervisor was rude and sarcastic, refused to provide a manager, and was hard to understand, leaving the inquiry unresolved", "outcome": "unresolved", "evidence": [
        {"quote": "Speaking to supervisor XXXX which she is extremely rude, sarcastic on the phone Is this how chase treats customers.", "speaker": "narrative"},
        {"quote": "I asked for a manager and she said she was the only person I can speak to.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A rude, sarcastic supervisor refused to transfer the customer to a manager and was hard to understand, leaving the original inquiry unresolved."
}}

records["cfpb_17185860"] = {"key": "d018e1904dc94675ea949fb23404522ca8c266aeb534a6ff3198f99273f65aeb", "response": {
    "contact_reasons": [{"reason": "dispute_or_chargeback", "specific_reason": "disputes over charges made after a gaming site reactivated a self-excluded account without consent were mostly denied", "is_primary": True}],
    "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "disputed charges made after a gaming site reactivated a self-excluded account without consent, but Chase denied most of the disputes as voluntary charges",
    "underlying_driver": "Chase denied most disputes despite evidence the merchant violated its own responsible-gaming policy, even though it had previously credited an identical transaction for the same issue",
    "reason_differs": False,
    "topics": [{"topic_label": "disputes for reactivated self-excluded account denied", "issue_statement": "About $7,000.00 in charges made after a gaming site reactivated a self-excluded account without consent were mostly denied by Chase as voluntary despite submitted evidence.", "product": "credit_card", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "Chase denied most disputes as voluntary charges despite evidence the merchant reactivated a permanently deleted, self-excluded account without consent", "outcome": "unresolved", "evidence": [
        {"quote": "I submitted evidence to Chase showing that the merchant violated its own rules by not enforcing permanent deletion. However, Chase denied most of my disputes, stating that the charges were voluntary, even though they had previously credited me for XXXX identical transaction for the same issue.", "speaker": "narrative"},
        {"quote": "I believe Chase did not properly review my supporting evidence and failed to consider the responsible gaming and consumer protection aspects of the case.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved",
    "positive_moments": [{"what": "Chase had previously credited an identical disputed transaction for the same issue", "category": "fair_outcome", "quote": "even though they had previously credited me for XXXX identical transaction for the same issue.", "speaker": "narrative"}],
    "redaction_heavy": False,
    "summary": "Roughly $7,000.00 in charges made after a gaming site reactivated a self-excluded account without consent were mostly denied by Chase as voluntary, despite the bank previously crediting an identical transaction."
}}

records["cfpb_18221831"] = {"key": "ea04a734a5c13204cc1f9013f2006e5c6c6c81fb2e5c93164ec89c5b4b1919bd", "response": {
    "contact_reasons": [
        {"reason": "funds_hold_or_account_restriction", "specific_reason": "a withdrawal was denied under an undisclosed 'business day' rule that folds weekends into Monday's limit", "is_primary": True},
        {"reason": "access_or_digital_banking", "specific_reason": "repeatedly locked out of the account despite completed identity verification", "is_primary": False}
    ],
    "products": ["checking_or_savings"], "services": ["branch"], "customer_ask": "explanation",
    "stated_reason": "a withdrawal was denied by the branch manager on the grounds of a 'business day' rule that was never fully disclosed",
    "underlying_driver": "the bank lumps weekend days into Monday's daily withdrawal limit without clear disclosure, and access has repeatedly been blocked despite completed identity verification",
    "reason_differs": False,
    "topics": [
        {"topic_label": "withdrawal denied under undisclosed business-day rule", "issue_statement": "A withdrawal was denied by the branch manager under a 'business day' rule that aggregates weekend days into Monday's limit, a rule never fully disclosed to the customer.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "policy_or_terms_change", "driver": "withdrawal denied because weekend days are silently folded into the Monday daily limit, a rule not disclosed to the customer", "outcome": "unresolved", "evidence": [
            {"quote": "Date XXXX Amount XXXX withdrawal denial By : Branch manager on grounds of the '' business day '' rule without full disclosure of said rule during withdrawal XXXX.", "speaker": "narrative"},
            {"quote": "If a bank aggregates weekend withdrawals into one daily limit but describes the limit as \" daily '' then that is unfair, deceptive, or abusive discretionary acts and or or practices.", "speaker": "narrative"}
        ]},
        {"topic_label": "repeated lockouts despite identity verification", "issue_statement": "The customer says the bank repeatedly locks them out of the account despite identity being verified via security questions on multiple occasions.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "repeatedly locked out of the account despite identity verification being completed multiple times via branch security questions", "outcome": "unresolved", "evidence": [
            {"quote": "Chase banking financial Institution has failed in areas of transparency by repeatedly locking me out of my account despite branch management protocols and procedures of identification being established and satisfied on numerous occasions via security question presented by branch manager", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A withdrawal was denied under an undisclosed 'business day' rule folding weekends into Monday's limit, and the customer says the account is repeatedly locked despite completed identity verification."
}}

records["cfpb_18638157"] = {"key": "831fae70fd4b0b52ca1d590890f6a6158c49f44e1a8c2cf207a25a3e5ce4a080", "response": {
    "contact_reasons": [{"reason": "balance_or_statement_error", "specific_reason": "a marketed no-overdraft account posted transactions resulting in a -$100.00 balance with unexplained figures", "is_primary": True}],
    "products": ["checking_or_savings"], "services": [], "customer_ask": "explanation",
    "stated_reason": "Chase Secure Banking, marketed as not allowing overdrafts, ended up with a negative $100.00 balance after transactions posted differently than shown at authorization",
    "underlying_driver": "Chase's stated available balance does not mathematically reconcile with the approved transactions, and it refuses to provide further explanation or updates",
    "reason_differs": False,
    "topics": [{"topic_label": "overdraft on marketed no-overdraft account", "issue_statement": "Chase Secure Banking, marketed as not allowing overdrafts, posted transactions resulting in a -$100.00 balance, and the bank's stated $64.00 available balance does not mathematically match the approved transactions.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information", "driver": "a stated $64.00 available balance does not reconcile with the transactions Chase approved, resulting in an unexplained -$100.00 balance on a marketed no-overdraft account", "outcome": "unresolved", "evidence": [
        {"quote": "Secure Banking accounts are marketed as not allowing overdrafts and declining transactions when funds are unavailable.", "speaker": "narrative"},
        {"quote": "Despite multiple inquiries, Chase did not provide a clear explanation of how my balance was calculated, how deposits were applied, or why transactions were approved if funds were insufficient. Chase has stated they will not provide further updates.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A Chase Secure Banking account marketed as overdraft-free ended up at -$100.00, and the bank's stated available balance does not mathematically reconcile with the transactions it approved."
}}

records["cfpb_19671731"] = {"key": "311ed965cac198eae016986259827c6f2ef94d67dc2eb4a88302cf50c8cd22e7", "response": {
    "contact_reasons": [{"reason": "customer_service_experience", "specific_reason": "months-long failure to update business name and EIN on credit cards despite repeated document submissions", "is_primary": True}],
    "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "fix_error",
    "stated_reason": "requested an update to the business legal name and EIN on two Chase business credit cards after incorporating, but the update has not been completed for months",
    "underlying_driver": "representatives gave conflicting information, documents appear to have been lost or mishandled multiple times, and even an executive complaint has not produced a resolution",
    "reason_differs": False,
    "topics": [
        {"topic_label": "months-long failure to update business name and EIN", "issue_statement": "A request to update the business legal name and EIN on two Chase business credit cards, submitted with all required documents, has remained unresolved for months despite reuploading documents twice.", "product": "credit_card", "sentiment": -1, "driver_category": "no_response_or_follow_up", "driver": "business name and EIN update requested months ago remains incomplete despite documents being submitted twice and a manual update once promised", "outcome": "unresolved", "evidence": [
            {"quote": "A supervisor previously confirmed documents were sufficient and promised a manual update, which was later contradicted.", "speaker": "narrative"},
            {"quote": "The matter has now been unresolved for over XXXX months.", "speaker": "narrative"}
        ]},
        {"topic_label": "conflicting information from representatives", "issue_statement": "Representatives gave contradictory statements about whether the submitted documents were received and whether a manual update was possible.", "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information", "driver": "one supervisor confirmed documents were sufficient and promised a manual update, while another later said the documents could not be located and manual updates were not possible", "outcome": "unresolved", "evidence": [
            {"quote": "Another supervisor stated the documents could not be located and contradicted prior statements, claiming manual updates were not possible and that the request must be routed to a specialized team.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A request to update a business's legal name and EIN on two Chase credit cards has gone unresolved for months amid lost documents and contradictory supervisor statements."
}}

records["cfpb_20158107"] = {"key": "6db528af7e68c1b8f7cc69e5d6c9f78b7ec8cc4ebe876817bab43fba3ecd67d1", "response": {
    "contact_reasons": [{"reason": "fees_and_charges", "specific_reason": "a business checking account overdrew about $2,100.00 with no low-balance alerts, accumulating $500-700 in fees", "is_primary": True}],
    "products": ["checking_or_savings"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "a business checking account became overdrawn by about $2,100.00 without any low-balance or overdraft notifications, accumulating $500-700 in overdraft fees",
    "underlying_driver": "a separate notification setting needed to be manually enabled to receive alerts, a requirement never clearly communicated at onboarding, and Chase would only waive three of the many fees",
    "reason_differs": False,
    "topics": [
        {"topic_label": "overdraft fees from missing balance alerts", "issue_statement": "A business checking account overdrew by about $2,100.00 with no low-balance or overdraft alerts, accumulating $500-700 in fees, because a separate alert setting had to be manually enabled but was never explained at onboarding.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "unexpected_charge", "driver": "$500-700 in overdraft fees accumulated because low-balance alerts required a manual setting never explained during onboarding", "outcome": "unresolved", "evidence": [
            {"quote": "Because I did not receive any low balance or overdraft notifications, additional transactions continued and approximately $500.00 $700.00 in overdraft fees accumulated before I realized the account was overdrawn.", "speaker": "narrative"},
            {"quote": "Chase explained during the call that a separate notification setting must be enabled to receive low balance or overdraft alerts. However, this requirement was not clearly communicated during account onboarding.", "speaker": "narrative"}
        ]},
        {"topic_label": "bank would only waive three fees", "issue_statement": "Chase declined to bring the account current excluding all overdraft fees, saying its policy allows removing only three fees, still leaving over $500.00 owed.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "policy limits fee waivers to three, leaving over $500.00 in fees despite the customer offering to pay the negative balance immediately", "outcome": "unresolved", "evidence": [
            {"quote": "Chase declined and stated that their policy only allows them to remove three fees, which would still leave over $500.00 in fees.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A business checking account overdrew about $2,100.00 with no low-balance alerts because of an undisclosed onboarding requirement, and Chase will waive only three of the resulting overdraft fees."
}}

records["cfpb_21218562"] = {"key": "ab674195b23b509ee26309140a8de91a34880698aae4ce20ddbd79c97f5c31e8", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "a second altered check was found on an account already flagged for a prior $94,000.00 altered check", "is_primary": True}],
    "products": ["checking_or_savings"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "a second fraudulent altered check ($96,000.00, presented and returned NSF) was found on the same account already flagged for an earlier $94,000.00 altered check",
    "underlying_driver": "despite reporting the first altered check and submitting an affidavit, the funds remain debited with no provisional credit, and a second altered check from the same mailing was still processed",
    "reason_differs": False,
    "topics": [
        {"topic_label": "second altered check after first fraud report", "issue_statement": "A second fraudulent altered check for $96,000.00 was presented on the same account already flagged for a $94,000.00 altered check, suggesting inadequate monitoring after the first fraud report.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "a second altered check from the same mailing was processed despite the bank already being notified of fraud on the account", "outcome": "unresolved", "evidence": [
            {"quote": "we have identified a second fraudulent altered check on the same account, confirming an ongoing pattern of fraud.", "speaker": "narrative"},
            {"quote": "The fact that a second altered checkalso originating from the same mailingwas able to be processed through the banking system raises serious concerns about whether adequate safeguards were implemented after the initial fraud report.", "speaker": "narrative"}
        ]},
        {"topic_label": "no provisional credit for first altered check", "issue_statement": "Despite prompt reporting and a submitted affidavit, the funds from the first altered check remain debited with no provisional credit.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "funds from the first altered check remain debited with no provisional credit despite a timely fraud report and affidavit", "outcome": "unresolved", "evidence": [
            {"quote": "Despite prompt reporting and submission of an affidavit on XX/XX/year>, the funds from the first altered check remain debited and no provisional credit has been provided.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A second altered check was presented on an account already flagged for a $94,000.00 fraud report, and funds from the first altered check remain debited with no provisional credit."
}}

records["cfpb_22430725"] = {"key": "419606bd0e9feeaebcd5a0588106f8255a9ebbf4cf4391a2a73fac0351209819", "response": {
    "contact_reasons": [{"reason": "account_opening_or_closure", "specific_reason": "checking account closed for unspecified 'concerning activity' with no details or escalation offered", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["phone_support"], "customer_ask": "explanation",
    "stated_reason": "the personal checking account was closed for 'concerning activity' with no specifics given",
    "underlying_driver": "a phone representative refused to give any details or escalate to a supervisor, and the customer was never given a chance to provide documentation",
    "reason_differs": False,
    "topics": [{"topic_label": "account closed with no explanation", "issue_statement": "The checking account was closed for unspecified 'concerning activity,' and the customer, who denies any wrongdoing, was refused details or a supervisor and given no chance to provide documentation.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "account closed for 'concerning activity' with no details given, no escalation offered, and no opportunity to submit documentation", "outcome": "unresolved", "evidence": [
        {"quote": "On XX/XX/XXXX I called Chase at XXXX to request specific information about what \" concerning activity '' triggered the closure. The representative refused to provide any details and would not escalate my call to a supervisor who could review the case.", "speaker": "narrative"},
        {"quote": "I was not given an opportunity to explain or provide documentation to prove the legitimacy of my account activity.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A checking account was closed for unspecified 'concerning activity,' and the customer was refused details, a supervisor, or the chance to provide documentation."
}}

records["cfpb_23216462"] = {"key": "f585c18cd3bc07f4af1fff556b9309c89007b08b1aea4cf569af84c52540f11d", "response": {
    "contact_reasons": [
        {"reason": "rewards_or_promotions", "specific_reason": "a promotional bonus was not applied due to a missing coupon code, with shifting timelines and eventually no record of the coupon", "is_primary": True},
        {"reason": "fees_and_charges", "specific_reason": "the account became overdrawn while waiting for the promised promotional credit", "is_primary": False}
    ],
    "products": ["checking_or_savings"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "a promotional bonus was not applied because a coupon code was missing, despite being told a manager helped apply it and it would take about 5 business days",
    "underlying_driver": "after multiple calls with shifting timelines, corporate now says there is no record of the coupon and it must restart, while the account has become overdrawn waiting for the promised credit",
    "reason_differs": False,
    "topics": [
        {"topic_label": "promotional bonus stuck with shifting timelines", "issue_statement": "A promotional bonus tied to opening the account was delayed for weeks with shifting timelines, and corporate now says there is no record of the coupon so the process must restart.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "no_response_or_follow_up", "driver": "promised in 5 business days, then repeatedly told longer waits, and corporate now says there's no record of the coupon requiring a fresh start", "outcome": "unresolved", "evidence": [
            {"quote": "I called 5 business days later ( the XXXX ) and they told me its still in their que and theres nothing they can do.", "speaker": "narrative"},
            {"quote": "Then I received a call back that it would take 15 days.", "speaker": "narrative"}
        ]},
        {"topic_label": "overdraft fees while waiting for the promised bonus", "issue_statement": "The account became overdrawn while waiting for the promised promotional credit, and the customer says the overdraft fees are the bank's fault for the delay.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "unexpected_charge", "driver": "account overdrawn and fees accruing while the promised promotional credit remained unapplied", "outcome": "unresolved", "evidence": [
            {"quote": "I had a decline at XXXX and I checked my account to find it has been overdrawn XXXX $ and I called corporate back saying if they would just give me the promotion I wouldnt be overdrawn and I should not be charged for the overdraft fees because its their fault.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A promotional account-opening bonus was delayed for weeks over a missing coupon code, and the account overdrew while waiting, with corporate ultimately saying the coupon must be restarted from scratch."
}}

records["cfpb_9501291"] = {"key": "ee4e8dc9ddec26ceeeb050c9830082dcfca507969c71cfe1f51004da6b9104a5", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "deposited a $3,700.00 check from a dog-sitting job scam and wired $3,200.00 before realizing it was fraud", "is_primary": True}],
    "products": ["checking_or_savings", "money_transfer_or_p2p"], "services": ["mobile_app", "branch"], "customer_ask": "refund_or_reversal",
    "stated_reason": "deposited a $3,700.00 check from a job/dog-sitting scam and wired $3,200.00 of it per the scammer's instructions before realizing it was fraud",
    "underlying_driver": "reported at the local branch but was told the funds likely cannot be recovered, and the customer fears the deposited check will bounce and affect the account",
    "reason_differs": False,
    "topics": [{"topic_label": "check scam led to wiring money unlikely to be recovered", "issue_statement": "A $3,700.00 check from a dog-sitting job scam was deposited, and $3,200.00 was wired per the scammer's request before the customer grew suspicious; the branch said the funds probably cannot be recovered.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "$3,200.00 wired due to a check scam, reported at the branch but told recovery is unlikely", "outcome": "unresolved", "evidence": [
        {"quote": "Using the Chase app on XX/XX/year>, I wired $3200.00 to the contact that they gave me.", "speaker": "narrative"},
        {"quote": "On XX/XX/year>, I reported the incident at my local Chase branch but they said they could probably not recover my funds lost.", "speaker": "narrative"},
        {"quote": "I am worried that when the check inevitably bounces that I will lose my account.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A dog-sitting job scam led to depositing a $3,700.00 fraudulent check and wiring $3,200.00 to the scammer; the branch said recovery is unlikely and the customer fears the bounced check will also affect the account."
}}

records["cfpb_9802454"] = {"key": "fa7da8fa18d10f59d6bf44541cfce542201fd3aedd012549cf070220a4652467", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "a caller impersonating Chase Credit Card Services gave a fake callback number and case number and had old personal data", "is_primary": True}],
    "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "explanation",
    "stated_reason": "received a call claiming to be from Chase Credit Card Services about a card misuse, but the callback number and case number given turned out to be fake",
    "underlying_driver": "the caller had the customer's SSN, date of birth, and an old address, unlike the correct address on file with Chase, raising concern the personal data was compromised elsewhere",
    "reason_differs": False,
    "topics": [{"topic_label": "phishing call using old personal data", "issue_statement": "A caller claiming to be from Chase Credit Card Services gave a callback number and case number that turned out to be fake, and had the customer's SSN, date of birth and an old address that doesn't match the current Chase account.", "product": "credit_card", "sentiment": -1, "driver_category": "other_or_unclear", "driver": "a caller impersonating Chase had the customer's SSN, date of birth, and an old address, and the callback number and case number provided did not check out", "outcome": "unknown", "evidence": [
        {"quote": "when i called back their was it was the right number but that person did not work there and case number did not exist.", "speaker": "narrative"},
        {"quote": "The person that called had my SSN, date of birth, and an old address, but my chase account has my correct address.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unknown", "positive_moments": [], "redaction_heavy": False,
    "summary": "A caller impersonating Chase Credit Card Services gave a fake callback number and case number and had the customer's SSN, date of birth, and an old address, raising concern their personal data was compromised."
}}

for call_id, rec in records.items():
    (out / f"{call_id}.json").write_text(json.dumps({"key": rec["key"], "prompt_version": "ext-1.0",
        "schema_version": "1", "taxonomy_version": "1", "call_id": call_id, "model": "claude-agent-build",
        "produced_by": "claude_agent", "created_at": "2026-09-11T12:00:00Z", "usage": None,
        "response": rec["response"]}, ensure_ascii=False), encoding="utf-8")
print("wrote", len(records))
