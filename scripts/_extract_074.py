import json, pathlib
out = pathlib.Path(r"C:/Users/RicardsonAlbuquerque/repos/Hack/data/cache/extract")

records = {}

records["cfpb_10122097"] = {"key": "de08f70b6310bee861bb4f7d09be0e45d40741827b2b680aa77352cbeb5a884f", "response": {
    "contact_reasons": [{"reason": "rewards_or_promotions", "specific_reason": "referral points promised for a successful sign-up were never credited", "is_primary": True}],
    "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "referred a friend to a Chase Ink card who was approved, but never received the promised referral points",
    "underlying_driver": "referral points promised for a successful sign-up were never credited to the account",
    "reason_differs": False,
    "topics": [{"topic_label": "referral points never received", "issue_statement": "Referred a friend who signed up and was approved for the Chase Ink card, but the promised referral points were never credited.", "product": "credit_card", "sentiment": -1, "driver_category": "other_or_unclear", "driver": "referral points promised for a successful sign-up were never credited to the account", "outcome": "unresolved", "evidence": [
        {"quote": "Upon referring it said I would get XXXX points. However, I never got those points.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A friend was successfully referred and approved for a Chase Ink card, but the promised referral points were never credited."
}}

records["cfpb_10420795"] = {"key": "81fcc9077ef18c68a5c03bf2911a001a01373909c570cbd94a4bfd400c787787", "response": {
    "contact_reasons": [
        {"reason": "account_opening_or_closure", "specific_reason": "closed four accounts including one with $6,900.00 and a checking account with about $900.00, but only $270.00 was received", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "an Executive Office complaint was opened but no one followed up", "is_primary": False}
    ],
    "products": ["checking_or_savings", "other_or_unspecified"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "Chase closed four accounts (investment, checking, savings, children's) but only sent $270.00 of the expected balances via cashier's check",
    "underlying_driver": "an Executive Office complaint was opened but no follow-up has occurred",
    "reason_differs": False,
    "topics": [
        {"topic_label": "closed accounts, most funds unreceived", "issue_statement": "After Chase closed four accounts including one holding $6,900.00 and a checking account with about $900.00, only $270.00 was received.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "closed four accounts worth thousands combined, but only $270.00 of the expected cashier's check funds has been received", "outcome": "unresolved", "evidence": [
            {"quote": "On XX/XX/year>, Chase closed my 4 accounts including investment account with balance of, $6900.00, checking account with balance of about $900.00, saving account, and children account.", "speaker": "narrative"},
            {"quote": "I only received $270.00 from Chase for checking account.", "speaker": "narrative"}
        ]},
        {"topic_label": "executive complaint unanswered", "issue_statement": "An Executive Office complaint was opened with a reference number, but no one has followed up.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "no_response_or_follow_up", "driver": "Executive Office complaint opened with a reference number but no follow-up has occurred", "outcome": "unresolved", "evidence": [
            {"quote": "I contacted Chase to Executive Office Complaint with reference number XXXX and was told that someone will resolve this issue. However, I havent heard back from Chase yet.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Chase closed four accounts worth thousands combined but sent only $270.00, and an Executive Office complaint about it has gone unanswered."
}}

records["cfpb_10871391"] = {"key": "23ddafd8813e1db29ee4db82f6dddd8e05fc929d0b3fb918a38ad16fe1fd0c72", "response": {
    "contact_reasons": [{"reason": "funds_hold_or_account_restriction", "specific_reason": "Chase refuses to release $40,000.00 from a still-valid cashier's check, claiming it was sent to Wisconsin's unclaimed property division", "is_primary": True}],
    "products": ["money_transfer_or_p2p", "checking_or_savings"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "Chase is refusing to release $40,000.00 from a still-valid cashier's check, claiming the funds were sent to Wisconsin's unclaimed property division",
    "underlying_driver": "Wisconsin says it never received the funds, and Chase refuses to provide proof of the transfer or a clear resolution after weeks of escalation",
    "reason_differs": False,
    "topics": [{"topic_label": "valid cashier's check funds withheld on unverifiable claim", "issue_statement": "Chase refuses to release $40,000.00 from a cashier's check still valid for years, claiming the funds were sent to Wisconsin's unclaimed property division, though Wisconsin has no record of receiving them.", "product": "money_transfer_or_p2p", "sentiment": -2, "driver_category": "money_held_or_not_returned", "driver": "$40,000.00 cashier's check funds withheld on the claim they were escheated to Wisconsin, which Wisconsin says it never received, with no proof provided", "outcome": "unresolved", "evidence": [
        {"quote": "Chase bank is refusing to release the funds to me for the check stating they sent the funds to the state of Wisconsin this year to unclaimed property division. They refuse to give me proof that they sent the funds to the state of Wisconsin.", "speaker": "narrative"},
        {"quote": "The state of Wisconsin unclaimed property division is telling us that they haven't received any funds from Chase bank.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Chase refuses to release $40,000.00 from a still-valid cashier's check, claiming it escheated the funds to Wisconsin, which has no record of receiving anything, and provides no proof."
}}

records["cfpb_11164968"] = {"key": "39be4a99f0fa0d90dfb462e2a7c63edea392f1cb7e6e4fdec874376c23735ed8", "response": {
    "contact_reasons": [{"reason": "dispute_or_chargeback", "specific_reason": "duplicate hotel charges of $170.00 and $480.00 were disputed twice but upheld with no documentation", "is_primary": True}],
    "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "duplicate hotel charges ($170.00 and $480.00) were disputed, but Chase claims they are valid without providing supporting documentation",
    "underlying_driver": "the hotel itself confirmed it cannot locate these transactions and cannot issue a credit, suggesting Chase failed to properly present the chargeback",
    "reason_differs": False,
    "topics": [{"topic_label": "duplicate charges upheld without documentation", "issue_statement": "Duplicate hotel charges of $170.00 and $480.00 were disputed twice, but Chase both times claimed the charges were valid without any supporting documentation.", "product": "credit_card", "sentiment": -1, "driver_category": "error_not_corrected", "driver": "Chase upheld duplicate $170.00 and $480.00 hotel charges as valid twice with no documentation, even though the hotel cannot locate the transactions", "outcome": "unresolved", "evidence": [
        {"quote": "Chase eventually responded, claiming they investigated the charges and determined them to be valid. However, no supporting documentation or reasoning was provided to justify this conclusion.", "speaker": "narrative"},
        {"quote": "the XXXX XXXX XXXX XXXX has confirmed they are unable to locate these transactions in their system and therefore can not issue a credit.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Duplicate hotel charges were disputed twice and both times upheld by Chase with no supporting documentation, even though the hotel itself cannot find the transactions."
}}

records["cfpb_11491613"] = {"key": "43d96bc99c72fa37f5c9470dec1a7ead953e39d515b89781d76be0fc43ea240f", "response": {
    "contact_reasons": [{"reason": "credit_reporting", "specific_reason": "'abuse of account' reported on the credit file that the customer disputes as inaccurate", "is_primary": True}],
    "products": ["credit_reporting_service"], "services": [], "customer_ask": "fix_error",
    "stated_reason": "Chase reported 'abuse of account' on the credit report which the customer says is inaccurate and never authorized",
    "underlying_driver": "multiple requests to have the information removed have gone unaddressed",
    "reason_differs": False,
    "topics": [{"topic_label": "inaccurate account-abuse reporting", "issue_statement": "Chase reported 'abuse of account' on the credit report, which the customer says is inaccurate and has not been removed despite multiple requests.", "product": "credit_reporting_service", "sentiment": -1, "driver_category": "error_not_corrected", "driver": "'abuse of account' reported on the credit file that the customer disputes as inaccurate, not removed after multiple requests", "outcome": "unresolved", "evidence": [
        {"quote": "JP MORGAN CHASE reports abuse of account this information is inaccurately reported. I have never abused this account.", "speaker": "narrative"},
        {"quote": "Ive reached out multiple times to obtain this information.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Chase reported 'abuse of account' on the credit report, which the customer disputes as inaccurate and has been unable to get removed despite multiple requests."
}}

records["cfpb_12055149"] = {"key": "d48bcdcd2c5a08865fbc437e203bc0042c77c9c569423db3acab2e87e177dd04", "response": {
    "contact_reasons": [
        {"reason": "funds_hold_or_account_restriction", "specific_reason": "a $63,000.00 check was cashed but the account was closed, leaving the funds inaccessible for months", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "identity verification requirements kept shifting across months of calls, blocking resolution", "is_primary": False}
    ],
    "products": ["checking_or_savings"], "services": ["branch", "phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "a $63,000.00 check was deposited into a Chase account that was then closed, and Chase has kept the funds despite months of attempts to verify identity and resolve it",
    "underlying_driver": "conflicting and shifting identity verification requirements (old phone numbers, an unexplained address error) have prevented resolution for months, causing severe financial hardship",
    "reason_differs": False,
    "topics": [
        {"topic_label": "$63,000 check stuck in closed account", "issue_statement": "A $63,000.00 check deposited into a Chase account was cashed, but the account was immediately closed, leaving the money inaccessible for months.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned", "driver": "$63,000.00 check was cashed by Chase but the receiving account was closed immediately, leaving the funds inaccessible for months", "outcome": "unresolved", "evidence": [
            {"quote": "Chase, cashed the check but immediately closed her account, with the funds in her account.", "speaker": "narrative"},
            {"quote": "My check remains in a closed chase account.", "speaker": "narrative"}
        ]},
        {"topic_label": "shifting identity verification requirements", "issue_statement": "Chase's fraud team repeatedly changed identity verification requirements, from old phone numbers to a new paid plan to an unexplained address mismatch, without resolving anything.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "incorrect_or_conflicting_information", "driver": "identity verification kept shifting requirements, from outdated phone numbers to a required paid phone plan to an unexplained address error, with no path to resolution", "outcome": "unresolved", "evidence": [
            {"quote": "The fraud team then attempts to identify me using OLD phone numbers from XXXX years ago that I no longer have.", "speaker": "narrative"},
            {"quote": "they say my name shows up with the phone number, but there is an error with my ADDRESS?? We have no clue what that means and they offer no other information.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A $63,000.00 check was cashed into an account that Chase immediately closed, and months of shifting identity-verification demands have left the funds inaccessible and the family in severe hardship."
}}

records["cfpb_12467801"] = {"key": "82873400ff03be466d5157010598f2843cebf8df8ffe00da2d25961cd2c988a8", "response": {
    "contact_reasons": [
        {"reason": "account_opening_or_closure", "specific_reason": "personal and business accounts closed over a claim of 'inappropriate conduct with employees' the customer says is false", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "ignored at a branch while another customer was helped first, then accounts closed after raising the concern", "is_primary": False}
    ],
    "products": ["checking_or_savings"], "services": ["branch"], "customer_ask": "explanation",
    "stated_reason": "personal and business accounts were closed for alleged 'inappropriate conduct with employees,' which the customer says is false",
    "underlying_driver": "the closure is believed to be retaliation after the customer was ignored at a branch while another customer was served first and raised concerns about the treatment",
    "reason_differs": True,
    "topics": [
        {"topic_label": "accounts closed on false misconduct claim", "issue_statement": "Personal and business accounts were closed over a claim of 'inappropriate conduct with employees' that the customer says is completely false.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "accounts closed citing 'inappropriate conduct with employees,' a claim the customer disputes as false and unsubstantiated", "outcome": "unresolved", "evidence": [
            {"quote": "On XX/XX/2025, I received a notice from Chase stating that my accounts were being closed due to \" inappropriate conduct with employees. '' This claim is completely false, unsubstantiated, and appears to be retaliation for a discriminatory incident that occurred at a Chase branch.", "speaker": "narrative"}
        ]},
        {"topic_label": "ignored at branch, then retaliatory closure", "issue_statement": "The customer was ignored at a branch while another customer was served first, and after raising the concern, the accounts were closed without warning.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "staff_attitude_or_competence", "driver": "ignored at the branch while another customer was helped first, and after raising the concern the accounts were closed without warning", "outcome": "unresolved", "evidence": [
            {"quote": "Despite waiting for service, I was ignored while a XXXX  customer who arrived after me was helped first. When I expressed concern about the discriminatory treatment, the bank staff continued to ignore me.", "speaker": "narrative"},
            {"quote": "Instead of addressing the issue professionally, Chase later closed my accounts without warning, harming both my personal finances and business operations.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Personal and business accounts were closed over an alleged misconduct claim the customer calls false, which they believe was retaliation for raising a discriminatory-treatment complaint at a branch."
}}

records["cfpb_12955262"] = {"key": "1690bb5bd8f82fd2d7df668abc534991dcc732bf4431006213fb6cc41dc95c24", "response": {
    "contact_reasons": [{"reason": "credit_reporting", "specific_reason": "a fraudulent Chase credit card account and several fraudulent inquiries need to be removed from the credit report", "is_primary": True}],
    "products": ["credit_reporting_service", "credit_card"], "services": [], "customer_ask": "fix_error",
    "stated_reason": "a fraudulent Chase credit card account and several fraudulent inquiries are showing on the credit report and must be removed",
    "underlying_driver": "the account and inquiries were never authorized by the customer",
    "reason_differs": False,
    "topics": [{"topic_label": "fraudulent account and inquiries on credit report", "issue_statement": "A fraudulent Chase credit card account and several fraudulent inquiries are showing on the credit report and need to be removed.", "product": "credit_reporting_service", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "a fraudulent Chase credit card account and multiple fraudulent inquiries remain on the credit report", "outcome": "unresolved", "evidence": [
        {"quote": "IT IS SHOWING CHASE BANK FRAUDULENT CREDIT CARD ACCOUNT ENDING XXXX IN MY CREDIT REPORT WHICH IS FRAUDULENT AND MUST BE REMOVED", "speaker": "narrative"},
        {"quote": "I AM THE ONLY PERSON WHO MADE THIS STATEMENT", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A fraudulent Chase credit card account and several fraudulent inquiries appear on the credit report and need to be removed."
}}

records["cfpb_13470111"] = {"key": "83aab8d0b5fa2e1d590f734a03c6474c8ca33f45a54bd0c53b2630cb4dfd7177", "response": {
    "contact_reasons": [{"reason": "collections_or_debt", "specific_reason": "a collection was placed on the credit report without providing required validation information", "is_primary": True}],
    "products": ["debt_collection"], "services": [], "customer_ask": "fix_error",
    "stated_reason": "a collector placed a collection on the consumer report without providing required validation information",
    "underlying_driver": "previous attempts to resolve this directly were ignored, and the customer demands statutory damages or deletion of the accounts",
    "reason_differs": False,
    "topics": [{"topic_label": "collection reported without required validation", "issue_statement": "A collection account was placed on the credit report without providing the validation information required by law, despite prior attempts to resolve it directly.", "product": "debt_collection", "sentiment": -1, "driver_category": "error_not_corrected", "driver": "collection reported without providing required validation information despite prior direct attempts to resolve it", "outcome": "unresolved", "evidence": [
        {"quote": "they have not provided validations information under 12cfr 1006.34 ( b ) ( 5 ) yet they have placed a collection on my consumer report recently.", "speaker": "narrative"},
        {"quote": "i have made previous attempts to fix these issues directly with them and they are violating my rights", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A collection was placed on the credit report without providing the legally required validation information, despite the customer's prior direct attempts to resolve it."
}}

records["cfpb_14020193"] = {"key": "7472415a4b4b90db567ec91d7d3d5c21b8ddc81b4fb289c943e6453ac02a36ea", "response": {
    "contact_reasons": [
        {"reason": "funds_hold_or_account_restriction", "specific_reason": "the account was frozen based on a court order that reportedly does not match the customer's legal name", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "waited over an hour on hold with the legal department without reaching anyone", "is_primary": False}
    ],
    "products": ["checking_or_savings"], "services": ["branch", "phone_support"], "customer_ask": "explanation",
    "stated_reason": "Chase froze the account based on a legal hold tied to a court order that does not have the customer's correct legal name",
    "underlying_driver": "no documentation of the court order has been provided, attempts to reach the referenced attorney failed, and a long hold with Chase's legal department produced no answer",
    "reason_differs": False,
    "topics": [
        {"topic_label": "account frozen on a court order with wrong name", "issue_statement": "The account was frozen based on a legal hold from a court order that reportedly does not contain the customer's correct legal name, with no documentation provided.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "account frozen under a court order that does not match the customer's legal name, with no copy of the order or clear explanation provided", "outcome": "unresolved", "evidence": [
            {"quote": "Chase Bank froze my account based on a legal hold tied to a court order that does not have my correct legal name.", "speaker": "narrative"},
            {"quote": "the legal documents that XXXX received reportedly do not contain my correct legal name, and yet my personal bank account was still frozen.", "speaker": "narrative"}
        ]},
        {"topic_label": "unable to reach anyone to resolve it", "issue_statement": "The customer waited over an hour on hold with Chase's legal department without speaking to anyone and has received unexplained hang-up calls from Chase.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "long_wait_or_delay", "driver": "waited over an hour on hold with the legal department without reaching anyone, plus unexplained calls from Chase that hang up", "outcome": "unresolved", "evidence": [
            {"quote": "I also called Chase 's legal department and was told the wait would be XXXX minutes I waited on hold for XXXX hour and XXXX minutes before giving up, without ever speaking to anyone.", "speaker": "narrative"},
            {"quote": "I have received unexplained phone calls from Chase that hang up when I answer.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "An account was frozen under a court order that reportedly does not match the customer's legal name, and hours of attempts to reach Chase's legal department have produced no documentation or resolution."
}}

records["cfpb_14589994"] = {"key": "b78c9089b231549ac3fb1e6afea4a6f0e8fcf633216590ed7c916d8cae23f64a", "response": {
    "contact_reasons": [
        {"reason": "fees_and_charges", "specific_reason": "charged a late fee the day after covering the payment due with redeemed points plus a checking transfer", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "twelve calls produced a different explanation every time about the resulting past-due status", "is_primary": False}
    ],
    "products": ["credit_card"], "services": ["phone_support", "online_banking"], "customer_ask": "refund_or_reversal",
    "stated_reason": "used points redemption plus a payment from checking to cover the amount due, but was charged a late fee the next day anyway",
    "underlying_driver": "called 12 times and got a different explanation every time; despite years without a late payment, the account now shows being two months behind and won't be corrected",
    "reason_differs": False,
    "topics": [
        {"topic_label": "late fee charged despite covering payment", "issue_statement": "Redeeming points plus a payment from checking was used to cover the amount due, but a late fee was charged the very next day.", "product": "credit_card", "sentiment": -1, "driver_category": "unexpected_charge", "driver": "charged a late fee the day after paying the due amount using redeemed points plus a checking transfer", "outcome": "unresolved", "evidence": [
            {"quote": "I asked could I use the XXXX points I accursed which took 3 years turn into XXXX cash an XXXX from checking total XXXX next day was charged late fee", "speaker": "narrative"}
        ]},
        {"topic_label": "inconsistent explanations across many calls", "issue_statement": "Twelve calls to Chase produced a different explanation every time, and despite years without a late payment the account now shows two months past due.", "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information", "driver": "12 calls each gave a different story, and the account now incorrectly shows two months past due despite years of on-time payments", "outcome": "unresolved", "evidence": [
            {"quote": "I've called Chase 12 times since every time get different story we have never been late for e years now will not resolve", "speaker": "narrative"},
            {"quote": "now says I'm 2 months due horrible service", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A late fee was charged the day after the amount due was covered with redeemed points and a checking transfer, and twelve calls have produced only conflicting explanations while the account now shows two months past due."
}}

records["cfpb_15237181"] = {"key": "ab2abb626a96a966e23fbffb80f3c4a9ef9e7a17082db4f192b31efe76a4c37a", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "a caller using a spoofed Chase number gained account access and Zelled out all the funds", "is_primary": True}],
    "products": ["checking_or_savings", "money_transfer_or_p2p"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "a caller impersonating Chase's claims department, calling from an actual Chase number, gained account access and Zelled all the money out",
    "underlying_driver": "Chase has provided no solution or refund despite the dispute being filed for this unauthorized transaction",
    "reason_differs": False,
    "topics": [{"topic_label": "spoofed chase call drained account via zelle", "issue_statement": "A caller impersonating Chase's claims department, using a spoofed actual Chase number, gained account access and transferred all the money out via Zelle.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "scammer using a spoofed Chase number gained account access and zelled out all funds; no refund provided after the dispute", "outcome": "unresolved", "evidence": [
        {"quote": "a customer service representative claiming to be from XXXX claims department called from an actual chase number stating that my account had been hacked. The representaive after gaining access to account zelled all my money out of the account.", "speaker": "narrative"},
        {"quote": "Contacted chase to file dispute and there has been no solution or refund to my account.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A scammer spoofing a real Chase phone number gained account access and Zelled out all the funds, and Chase has provided no refund after the dispute."
}}

records["cfpb_15877928"] = {"key": "ac450b518a99aa4466f7c353992b5ee674e4947a2331ca04464f354326ad4c29", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "$5,300.00 in unauthorized international shipping charges appeared on the debit card despite two-factor authentication", "is_primary": True}],
    "products": ["checking_or_savings"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "an account was accessed by an unauthorized third party despite two-factor authentication, resulting in $5,300.00 in unauthorized shipping charges on the Chase debit card",
    "underlying_driver": "Chase denied the dispute claiming the charges were authorized simply because of prior business with the merchant, despite police reports and evidence of fraud",
    "reason_differs": False,
    "topics": [{"topic_label": "$5,300 fraud denied despite evidence", "issue_statement": "$5,300.00 in unauthorized international shipping charges appeared on the debit card after an account was hacked despite two-factor authentication, but Chase denied the dispute as authorized based on past business with the merchant.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "denied as authorized because of prior business with the merchant, despite police reports and evidence the $5,300.00 in charges were fraudulent", "outcome": "unresolved", "evidence": [
        {"quote": "This resulted in $5300.00 in unauthorized charges on my Chase Bank debit card for shipments I did not create or approve.", "speaker": "narrative"},
        {"quote": "Chase denied my dispute, claiming the charges were authorized because I had done business with XXXX before, despite clear evidence these transactions were fraudulent and inconsistent with my normal business activity.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "$5,300.00 in unauthorized international shipping charges hit a hacked account despite two-factor authentication, and Chase denied the dispute as authorized based on prior business with the merchant."
}}

records["cfpb_17844345"] = {"key": "4a3baf330eb412acbcc2ea37ecff3c25f09be327c4a8c6e5c2520e84fec12ea9", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "a scammer spoofing Chase's real phone number and branding induced $1,400.00 in Zelle transfers", "is_primary": True}],
    "products": ["checking_or_savings", "money_transfer_or_p2p"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "a scammer spoofing Chase's phone number and branding tricked the customer into sending $1,000.00 and $490.00 via Zelle to 'secure' the account",
    "underlying_driver": "Chase denied the claim because the transactions were made from the customer's own device, despite being manipulated by a sophisticated impersonation scam",
    "reason_differs": False,
    "topics": [{"topic_label": "spoofed chase scam claim denied", "issue_statement": "A scammer spoofing Chase's real phone number and branding convinced the customer to send $1,000.00 and $490.00 via Zelle to 'secure' the account, and Chase denied the claim because the transfers came from the customer's own device.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "claim denied because the $1,400.00 in Zelle transfers were made from the customer's own device, despite being manipulated by a spoofed Chase scam", "outcome": "unresolved", "evidence": [
        {"quote": "The scammer called me pretending to be a Chase fraud XXXX. They had access to my personal information, sent me real Chase-style verification codes, and told me to use XXXX to secure my account.", "speaker": "narrative"},
        {"quote": "they denied my claim, saying the transactions were made from my device, even though I was clearly tricked and manipulated by a scammer posing as Chase.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A scammer spoofing Chase's real phone number and branding induced $1,400.00 in Zelle transfers, and Chase denied the claim because the transfers came from the customer's own device."
}}

records["cfpb_17191768"] = {"key": "46697aea8cf31d33bb95d908b5c567c8f61054a95f0d5d2ba3a290e71b2c15cd", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "a computer hacking scam led to $44,000.00 in wire transfers, and the claim was denied because the laptop was used", "is_primary": True}],
    "products": ["checking_or_savings", "money_transfer_or_p2p"], "services": ["phone_support", "branch"], "customer_ask": "refund_or_reversal",
    "stated_reason": "a computer hacking scam impersonating tech support and the FTC convinced the customer that wire transfers were being made from the Chase account, resulting in $44,000.00 actually being sent",
    "underlying_driver": "despite freezing accounts and providing evidence of the hack to the bank, Chase denied all three family members' claims because their laptops were used to authorize the transfers",
    "reason_differs": False,
    "topics": [{"topic_label": "$44,000 in wire transfers denied despite hack evidence", "issue_statement": "A computer hacking scam led to two wire transfers totaling $44,000.00 being sent from the Chase account, and Chase denied the claim because the laptop was used, despite evidence of the hack.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "claims for $44,000.00 in scam-induced wire transfers denied because the customer's laptop was used, despite confirmed evidence of the computer hack", "outcome": "unresolved", "evidence": [
        {"quote": "By the end of day, XXXX wire transfers ( first for $22000.00 and second for $21000.00 ) total of $44000.00 had been sent.", "speaker": "narrative"},
        {"quote": "After numerous phone calls and visits to the bank, my claims and the claims by XXXX and XXXX were all denied even after we presented information confirming the hack on my laptop. They denied all because my laptop XXXX was used.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A computer hacking scam led to $44,000.00 in wire transfers, and Chase denied fraud claims from the customer and two family members solely because their laptops were used, despite confirmed hack evidence."
}}

records["cfpb_18226451"] = {"key": "fb9c7402d34755b6c6c09242796d951036ccd76ff9e4aac9d843baa6eb1bd3ac", "response": {
    "contact_reasons": [
        {"reason": "fees_and_charges", "specific_reason": "interest charged for two months despite qualifying for Chase's announced government-shutdown relief", "is_primary": True},
        {"reason": "terms_information_or_communication", "specific_reason": "a promised deferral of the minimum payment for the impacted months was never honored", "is_primary": False}
    ],
    "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "Chase publicly promised interest waivers and payment deferrals for customers affected by the government shutdown, but interest was still charged for two months",
    "underlying_driver": "when a refund was requested, Chase said its system rejected it and representatives are now unable or unwilling to reverse the charges or defer the minimum payments as promised",
    "reason_differs": False,
    "topics": [
        {"topic_label": "shutdown relief interest waiver not honored", "issue_statement": "Interest charges were applied for two billing periods despite being eligible for Chase's publicly announced government-shutdown relief, and Chase's system rejected the refund request.", "product": "credit_card", "sentiment": -2, "driver_category": "policy_or_terms_change", "driver": "interest charged for two months despite qualifying for the announced shutdown relief, and the refund request was rejected by Chase's system", "outcome": "unresolved", "evidence": [
            {"quote": "Despite being eligible and impacted, interest charges were applied to my account for two separate months.", "speaker": "narrative"},
            {"quote": "Applying interest in contradiction to stated relief and then refusing to refund it due to internal system limitations is unacceptable and financially harmful.", "speaker": "narrative"}
        ]},
        {"topic_label": "promised minimum payment deferral not honored", "issue_statement": "Chase said the minimum payment due would be deferred for the impacted months, but it charged the full minimum payment instead.", "product": "credit_card", "sentiment": -1, "driver_category": "policy_or_terms_change", "driver": "promised deferral of the minimum payment for the impacted months was never honored; the full minimum was charged instead", "outcome": "unresolved", "evidence": [
            {"quote": "They also stated not just the interest will be reversed but the minimum payment due as well will be deferred for the impacted months however Chase charged me the entire minimum payment due for the impacted months and never even honoured to defer the minimum amounts.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Despite qualifying for Chase's announced government-shutdown relief, interest was charged for two months and the promised minimum-payment deferral was never honored, and the refund request was rejected."
}}

records["cfpb_18640148"] = {"key": "44f01dcfc8697f6365f6dbe1a5944906415861b7c6b68a80ffefde7eb1e75355", "response": {
    "contact_reasons": [{"reason": "credit_decision_or_limit", "specific_reason": "demanding immediate extension of $12,000.00 credit and a $100,000.00 home loan", "is_primary": True}],
    "products": ["credit_card", "mortgage"], "services": [], "customer_ask": "other",
    "stated_reason": "the customer is demanding Chase extend $12,000.00 of credit with auto repay and bureau reporting",
    "underlying_driver": "the text also demands a $100,000.00 minimal home loan at market rate and references a passing 'possibility for fraud' without further explanation",
    "reason_differs": False,
    "topics": [{"topic_label": "demand for credit and home loan extension", "issue_statement": "The customer is demanding Chase immediately extend $12,000.00 of credit with auto repay and bureau reporting, plus a $100,000.00 minimal home loan at market rate.", "product": "credit_card", "sentiment": 0, "driver_category": "other_or_unclear", "driver": "demanding immediate extension of $12,000.00 credit and a $100,000.00 home loan, with a passing reference to possible fraud", "outcome": "unknown", "evidence": [
        {"quote": "$12000.00 approved credit with auto repay and bureau reporting $100000.00 minimal home loan at market rate", "speaker": "narrative"},
        {"quote": "See complaint and possibility for fraud Chase should now extend the following asap.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": 0, "resolution_status": "unknown", "positive_moments": [], "redaction_heavy": False,
    "summary": "A brief, unclear complaint demands Chase immediately extend $12,000.00 in credit and a $100,000.00 home loan, with a passing mention of possible fraud."
}}

records["cfpb_19679770"] = {"key": "4ed20679e0479258ef98265547f0e27302c0eee6304c6c5e760872b91dde4d1c", "response": {
    "contact_reasons": [{"reason": "funds_hold_or_account_restriction", "specific_reason": "funds frozen for over 30 days with no clear legal or factual basis given", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["phone_support"], "customer_ask": "fix_error",
    "stated_reason": "funds have been frozen for over 30 days with no clear legal or factual basis provided for the freeze",
    "underlying_driver": "over 30 different representatives have given conflicting information, and no timely investigation or resolution has occurred as required by law",
    "reason_differs": False,
    "topics": [{"topic_label": "funds frozen over 30 days with no basis given", "issue_statement": "Funds have been frozen for over 30 days without Chase providing a clear legal or factual basis for the freeze.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned", "driver": "funds frozen for over 30 days with no clear legal or factual basis, and over 30 different representatives gave conflicting information", "outcome": "unresolved", "evidence": [
        {"quote": "By freezing my funds for over 30 days, providing conflicting information through over 30 different representatives, and failing to provide a clear legal or factual basis for the freeze, Chase has engaged in practices that are both unfair and abusive to me as a consumer.", "speaker": "narrative"},
        {"quote": "Chase has failed to provide a timely resolution or a valid reason for denying me access to my own money.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Funds have been frozen for over 30 days with no clear legal basis, and more than 30 representatives have given conflicting information about why."
}}

records["cfpb_20162079"] = {"key": "5b709382360ca1cfba3ff4f321d37481d222e0f8b66ad5ca0f7fc83953806361", "response": {
    "contact_reasons": [{"reason": "payment_or_transfer_problem", "specific_reason": "a $400.00 returned transaction was never listed on the account for the customer to redeposit, happening twice", "is_primary": True}],
    "products": ["checking_or_savings"], "services": [], "customer_ask": "other",
    "stated_reason": "a $400.00 returned transaction was never listed on the account for the customer to redeposit despite the bank saying it had been posted",
    "underlying_driver": "this happened twice without the transaction ever appearing, risking cancellation of an insurance policy, and the customer wants Chase to document the error for the insurer",
    "reason_differs": False,
    "topics": [{"topic_label": "returned transaction never appeared to redeposit", "issue_statement": "A $400.00 returned transaction was supposedly posted for the customer to redeposit, but it never appeared on the account, and this happened twice.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "error_not_corrected", "driver": "a $400.00 returned transaction was never actually listed on the account to redeposit, happening twice, risking cancellation of an insurance policy", "outcome": "unresolved", "evidence": [
        {"quote": "They returned this transaction twice without listing it at all for my awareness to deposit.", "speaker": "narrative"},
        {"quote": "This has resulted in possible cancellation of my policy which is a huge deal.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A $400.00 returned transaction was never actually listed on the account for redeposit, happening twice, and now risks the cancellation of an insurance policy."
}}

records["cfpb_21227023"] = {"key": "21079ea79ea95cd63b33fa095babe70ae47bfcaa86f8b8c7962024a0a3dec06a", "response": {
    "contact_reasons": [{"reason": "balance_or_statement_error", "specific_reason": "Chase removed $1,500.00 claiming a duplicate deposit of two different checks with the same amount", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["atm"], "customer_ask": "refund_or_reversal",
    "stated_reason": "Chase claims a $1,500.00 check was deposited twice (two different checks, same amount) and removed $1,500.00 from the account",
    "underlying_driver": "after proving they were two separate checks, Chase claimed a conflicting ATM deposit at another bank cleared first, but neither that bank nor the issuing bank has any record of it, and Chase refuses to investigate further",
    "reason_differs": False,
    "topics": [{"topic_label": "$1,500 removed over unverifiable duplicate claim", "issue_statement": "Chase removed $1,500.00 claiming a duplicate deposit of two different checks with the same amount, then blamed an ATM deposit at another bank that neither bank has any record of.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information", "driver": "$1,500.00 removed over an alleged duplicate deposit; the explanation shifted to an ATM deposit at another bank that has no record of it, and Chase refuses to investigate", "outcome": "unresolved", "evidence": [
        {"quote": "Chase removed $1500.00 from my account two weeks later. Then once I proved that it's two different checks they said a deposit was made at XXXX  through an atm and it cleared before my cheese transaction cleared.", "speaker": "narrative"},
        {"quote": "Chase refuses to look into this and investigate.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Chase removed $1,500.00 over a claimed duplicate deposit, then shifted its explanation to an ATM deposit elsewhere that neither bank has any record of, and refuses to investigate further."
}}

records["cfpb_22436583"] = {"key": "3215f61bba6e7e2b6bf4b08e7989a7a2a21780f640a1a1720c0090c5dded5683", "response": {
    "contact_reasons": [{"reason": "balance_or_statement_error", "specific_reason": "the account shows a balance over the credit limit with no billing documentation explaining how it was generated", "is_primary": True}],
    "products": ["credit_card"], "services": [], "customer_ask": "explanation",
    "stated_reason": "the credit card shows a balance of $3,200.00 against a $2,500.00 limit, resulting in negative available credit, with a highest balance $3,700.00 over the limit",
    "underlying_driver": "Chase confirmed the figures in writing but provided no billing documentation explaining how they were generated",
    "reason_differs": False,
    "topics": [{"topic_label": "over-limit balance with no explanation", "issue_statement": "The account shows a $3,200.00 balance against a $2,500.00 limit and a highest balance $3,700.00 over the limit, and Chase confirmed the figures without any billing documentation explaining them.", "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information", "driver": "balance reported as $3,200.00 against a $2,500.00 limit, and Chase confirmed the figures in writing but provided no billing documentation to explain them", "outcome": "unresolved", "evidence": [
        {"quote": "I noticed my JPMCB Card account ( XXXX XXXXXXXX ) shows a balance of $3200.00 against a credit limit of $2500.00, resulting in negative available credit of - $710.00 on my XXXX  file.", "speaker": "narrative"},
        {"quote": "I contacted Chase and received a written response dated XX/XX/year> confirming those figures but no billing documentation explaining how they were generated.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A credit card shows a balance thousands over its credit limit, and Chase confirmed the figures in writing without providing any billing documentation to explain them."
}}

records["cfpb_23217901"] = {"key": "159a0fae243997b0463b5fbd822c5657643f183d2405cf39cb5c248bd00db6ab", "response": {
    "contact_reasons": [{"reason": "account_opening_or_closure", "specific_reason": "three accounts held over 25 years were arbitrarily closed with no explanation", "is_primary": True}],
    "products": ["checking_or_savings", "other_or_unspecified"], "services": [], "customer_ask": "explanation",
    "stated_reason": "three accounts held for over 25 years were arbitrarily closed with no explanation or reasoning given",
    "underlying_driver": "it took several weeks to get the money back, forcing the customer to transfer investments elsewhere",
    "reason_differs": False,
    "topics": [{"topic_label": "long-held accounts closed with no explanation", "issue_statement": "Three accounts held for over 25 years, originally transferred from another bank, were closed with no explanation, and it took several weeks to get the money back.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "denied_or_declined_without_explanation", "driver": "three long-held accounts closed with no explanation given despite 25 years without any fraud or illegal activity, and it took weeks to recover the funds", "outcome": "partially_resolved", "evidence": [
        {"quote": "I have never committed fraud or any illegal activity on these accounts or any money laundering. I asked for a reason and they wouldn't tell me anything. They just closed the accounts.", "speaker": "narrative"},
        {"quote": "It took me several weeks to get my money from them and I had to transfer all my investments to my XXXX XXXX accounts", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "partially_resolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Three accounts held for over 25 years were closed with no explanation, and it took several weeks to recover the funds, forcing investments to be moved elsewhere."
}}

records["cfpb_9491465"] = {"key": "b85b297be4f5f24a601c776419546c94c6a6b8d0499596d8aafe4bdbc611dbc4", "response": {
    "contact_reasons": [{"reason": "terms_information_or_communication", "specific_reason": "a payment intended for an expiring promotional balance was allocated to a different promotion under Chase's payment guidelines", "is_primary": True}],
    "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "fix_error",
    "stated_reason": "paid $8,400.00 intending to pay off a promotional balance expiring soon, but the payment was applied to a different, higher-interest promotion instead",
    "underlying_driver": "because the payment was allocated to the other promotion first under Chase's payment-allocation policy, the intended promotion expired and now incurs 21.24% interest",
    "reason_differs": False,
    "topics": [{"topic_label": "payment misallocated, causing promo to expire", "issue_statement": "An $8,400.00 payment intended to pay off a 1.99% promotional balance before it expired was instead allocated to a different 0.00% promotion, causing the 1.99% balance to expire and now accrue 21.24% interest.", "product": "credit_card", "sentiment": -1, "driver_category": "policy_or_terms_change", "driver": "payment allocated to the higher-interest promotion per Chase's payment guidelines, causing the intended promotional balance to expire and now accrue 21.24% interest", "outcome": "unresolved", "evidence": [
        {"quote": "When I received my statement for XX/XX/XXXX - XX/XX/XXXX, they allocated my payment to promotion ( XXXX ) because it has a higher interest than promotion ( XXXX ). Because of this allocation promotion ( XXXX ) expired and they are now charging me interest of 21.24 % and the balance now is $8400.00.", "speaker": "narrative"},
        {"quote": "I called the company and relayed my frustration and I was told that is their guidelines in applying the payments.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "An $8,400.00 payment meant to pay off an expiring promotional balance was instead applied to a different promotion under Chase's payment rules, causing the intended balance to expire and start accruing 21.24% interest."
}}

records["cfpb_9802460"] = {"key": "2e33d3a81e885171017097ae6c8bc5b7f8a96dd2cba56fb6d938da8f1436167d", "response": {
    "contact_reasons": [
        {"reason": "unauthorized_or_fraud", "specific_reason": "a wave of unauthorized transactions over several days; later claims were reversed after being told the customer must prove fraud", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "the burden of proof was shifted to the customer, who had to seek records from a merchant that could not provide any", "is_primary": False}
    ],
    "products": ["checking_or_savings"], "services": ["phone_support", "branch"], "customer_ask": "refund_or_reversal",
    "stated_reason": "after a first quickly-resolved fraud incident, further unauthorized transactions were credited temporarily, then reversed when Chase said it could not prove fraud",
    "underlying_driver": "Chase placed the burden of proof on the customer to get records from the merchant, which the merchant could not provide, leaving the claim stuck",
    "reason_differs": False,
    "topics": [
        {"topic_label": "first fraud incident quickly resolved", "issue_statement": "The first fraudulent transaction of around $300.00 was refunded within hours without even requiring a formal claim.", "product": "checking_or_savings", "sentiment": 1, "driver_category": "fast_resolution", "driver": "the first fraud incident was credited back within hours without needing a formal claim", "outcome": "resolved", "evidence": [
            {"quote": "As soon as I realized it that morning I contacted Chase and cancelled my card. A claim was not even necessary to make and they credited the money back into my account within hours.", "speaker": "narrative"}
        ]},
        {"topic_label": "later fraud claims reversed, burden shifted to customer", "issue_statement": "Later unauthorized transactions were temporarily credited but then reversed after Chase said it could not prove fraud, and the customer was told to get proof from the merchant that the merchant could not provide.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "temporary credit for further unauthorized transactions was reversed, with Chase saying it could not prove fraud and placing the burden on the customer to get evidence from the merchant", "outcome": "unresolved", "evidence": [
            {"quote": "Fast forward a week and or so and that $1000.00 claim was reversed ( money taken back out of my account ). I immediately contacted chase was directed to the claims department and they told me that based on their investigation they could not prove that it was fraud.", "speaker": "narrative"},
            {"quote": "It would be my responsibility to reach out to XXXX and acquire proof from them that I would then need to send to my bank just to reopen the claim.", "speaker": "narrative"},
            {"quote": "I contacted XXXX and they were unable to provide me with any receipts or any information at all.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "partially_resolved",
    "positive_moments": [
        {"what": "the first fraud incident was refunded within hours with no claim required", "category": "fast_resolution", "quote": "A claim was not even necessary to make and they credited the money back into my account within hours.", "speaker": "narrative"},
        {"what": "a branch manager recognized all the transactions as fraudulent", "category": "helpful_staff", "quote": "I spoke with a manager and he recognized all these transaction as fraudulent.", "speaker": "narrative"}
    ],
    "redaction_heavy": False,
    "summary": "A first fraud incident was refunded within hours, but a second wave of unauthorized transactions was later reversed after Chase said it could not prove fraud and shifted the burden of proof to the customer."
}}

records["cfpb_10130647"] = {"key": "2b0ab740c9b8660b82f378677718b619391c7feb6ed79b5c35b30cef54fa4266", "response": {
    "contact_reasons": [{"reason": "collections_or_debt", "specific_reason": "a 40% settlement offer made before the due date was stalled, followed by repeated collection calls and emails with no negotiation", "is_primary": True}],
    "products": ["debt_collection"], "services": ["phone_support", "chat_or_email"], "customer_ask": "stop_or_block",
    "stated_reason": "attempted to settle a debt for 40% before the due date, but was told they could not guarantee anything and to call back after the due/statement date",
    "underlying_driver": "after being told they'd consider settling later, the company began repeatedly calling and emailing, refusing to negotiate the 40% offer that was on the table before",
    "reason_differs": False,
    "topics": [{"topic_label": "settlement stalled then followed by repeated collection calls", "issue_statement": "A 40% settlement offer made before the due date was met with no guarantee and instructions to call back later, and the company is now repeatedly calling and emailing without negotiating.", "product": "debt_collection", "sentiment": -1, "driver_category": "repeated_contact_needed", "driver": "after refusing to confirm a 40% settlement before the due date, the company is now repeatedly calling and emailing and won't negotiate at all", "outcome": "unresolved", "evidence": [
        {"quote": "As soon as we wanted to negotiate for 40 % a few days ago before all this happened before the due date, we were told that we couldnt and now theyre harassing us for the money that they said that they so nicely wanted to not settle on.", "speaker": "narrative"},
        {"quote": "Ive gotten a few phone calls a few emails. I mean this hasnt stopped Consistently calling us back-and-forth and do not negotiate", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A 40% debt settlement offer made before the due date was not confirmed, and the company has since repeatedly called and emailed without ever negotiating."
}}

for call_id, rec in records.items():
    (out / f"{call_id}.json").write_text(json.dumps({"key": rec["key"], "prompt_version": "ext-1.0",
        "schema_version": "1", "taxonomy_version": "1", "call_id": call_id, "model": "claude-agent-build",
        "produced_by": "claude_agent", "created_at": "2026-09-11T12:00:00Z", "usage": None,
        "response": rec["response"]}, ensure_ascii=False), encoding="utf-8")
print("wrote", len(records))
