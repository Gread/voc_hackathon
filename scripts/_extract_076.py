import json, pathlib
out = pathlib.Path(r"C:/Users/RicardsonAlbuquerque/repos/Hack/data/cache/extract")

records = {}

records["cfpb_10839155"] = {"key": "e4521ff44aef077be3c3547a811d20778027813cbed179f332807e8a2cd42d64", "response": {
    "contact_reasons": [
        {"reason": "rewards_or_promotions", "specific_reason": "a $300.00 statement credit promotion implied immediate use but only applies after a 7-10 day card delivery window", "is_primary": True},
        {"reason": "terms_information_or_communication", "specific_reason": "the promotion's timing limitation was not disclosed upfront before applying", "is_primary": False}
    ],
    "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "applied for a card based on a promotion implying a $300.00 credit could apply to an immediate hotel booking, but the credit only applies to purchases after the card arrives, 7-10 days later",
    "underlying_driver": "this critical timing limitation was not disclosed upfront, leaving the customer stuck with an annual fee on a card they wouldn't have gotten otherwise",
    "reason_differs": False,
    "topics": [{"topic_label": "misleading promo timing left unwanted fee", "issue_statement": "A $300.00 statement credit promotion implied it could apply to an immediate hotel booking, but it only applies to purchases made after the card arrives 7-10 days later, leaving the customer stuck with an unwanted annual fee.", "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information", "driver": "the promotion implied the $300.00 credit could be applied to an immediate booking, but it only applies after a 7-10 day card delivery window, a limitation not disclosed upfront", "outcome": "unresolved", "evidence": [
        {"quote": "The way the offer was presented clearly implied that the credit could be applied toward the stay I was booking.", "speaker": "narrative"},
        {"quote": "the $300.00 statement credit is only applicable to purchases made after the card is received, which takes 710 business days to arrive.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A promised $300.00 statement credit was presented as usable for an immediate hotel booking, but only applies after a 7-10 day card delivery window, leaving the customer with an unwanted annual fee."
}}

records["cfpb_11167983"] = {"key": "88724ed6267440433f3b87f6b0dc05b40e7ce30f2406789d81b1514447197487", "response": {
    "contact_reasons": [{"reason": "credit_decision_or_limit", "specific_reason": "two credit cards were suddenly closed with no explanation despite a clean payment history", "is_primary": True}],
    "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "explanation",
    "stated_reason": "two Chase credit cards were suddenly closed despite an excellent FICO score, no delinquencies, and staying under credit limits",
    "underlying_driver": "a supervisor could not explain the closure, and the customer could not find any rule violation justifying it",
    "reason_differs": False,
    "topics": [{"topic_label": "cards closed with no explanation", "issue_statement": "Two Chase credit cards were suddenly closed despite an excellent FICO score, no delinquent payments, and never exceeding the credit limit, and a supervisor could not explain why.", "product": "credit_card", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "two cards closed with no explanation despite a clean payment history, and a supervisor could not identify any rule violation", "outcome": "unresolved", "evidence": [
        {"quote": "My FICO score is XXXX, no delinquent payments, no going above the credit limit. I called Chase and after talking to a supervisor she could not tell me why.", "speaker": "narrative"},
        {"quote": "I checked again what the 'rules ' of the cardsnwere and I can not find any reason for this sudden cancellation.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Two Chase credit cards were suddenly closed with no explanation despite an excellent credit history, and a supervisor could not identify a reason."
}}

records["cfpb_11487715"] = {"key": "e794d097a968ccc6b02b6f1f91c21b0e3ee58eb8898eaa7fc9976984a0cf5384", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "one of two fraud claims after a phone robbery was denied based on an impossible identity-verification claim", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "after a phone was forcibly stolen, two fraudulent charges were made; one fraud claim was approved but the other was denied",
    "underlying_driver": "the denial cited a Face ID scan supposedly verifying identity, which is impossible since the customer did not have the phone at the time",
    "reason_differs": False,
    "topics": [{"topic_label": "fraud claim denied on impossible verification claim", "issue_statement": "After a phone was forcibly stolen, one of two fraudulent charges was denied because the bank claimed a Face ID scan verified identity, which is impossible since the phone was not in the customer's possession.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "claim denied on the basis of a Face ID verification that could not have occurred since the phone was stolen at the time of the transaction", "outcome": "unresolved", "evidence": [
        {"quote": "The reason for the denied claim was that their team found evidence that my XXXX XXXX ID scan was used to verify my identity, so they did not see it as fraudulent.", "speaker": "narrative"},
        {"quote": "they were unable to provide any source or evidence from the claim that my XXXX XXXX  was used to make the transaction, which is impossible as I did not have possession of my device at the time of the transaction.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "partially_resolved",
    "positive_moments": [{"what": "one of the two fraud claims was approved", "category": "fair_outcome", "quote": "the fraudulent claims were finished processing, and one claim was approved and one denied.", "speaker": "narrative"}],
    "redaction_heavy": False,
    "summary": "After a phone robbery led to two fraudulent charges, one claim was approved but the other was denied based on a Face ID verification that could not have occurred while the phone was stolen."
}}

records["cfpb_12056645"] = {"key": "5e3dcf162b4cd9ebb715cef29a457ba22f5850a0d455eab270fdaaf1f4a1ece8", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "a credit card was fraudulently opened using the customer's stolen identity", "is_primary": True}],
    "products": ["credit_card", "credit_reporting_service"], "services": ["phone_support"], "customer_ask": "fix_error",
    "stated_reason": "received a billing statement for a credit card never applied for, discovering identity theft",
    "underlying_driver": "reported to both the bank and the credit reporting company immediately",
    "reason_differs": False,
    "topics": [{"topic_label": "fraudulently opened credit card", "issue_statement": "A billing statement arrived for a credit card the customer never applied for, revealing identity theft was used to open it.", "product": "credit_card", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "a credit card was fraudulently opened using the customer's stolen identity", "outcome": "unknown", "evidence": [
        {"quote": "I recieved a billing statement by email from the bank on a credit card that I never applied for.", "speaker": "narrative"},
        {"quote": "Someone stole my identity and were able to open a credit card on my name successfully.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unknown", "positive_moments": [], "redaction_heavy": False,
    "summary": "A credit card was fraudulently opened using the customer's stolen identity, discovered after an unexpected billing statement arrived."
}}

records["cfpb_12481121"] = {"key": "118512a18359a9df64ec1f585015297280f79d38b76139e64216ee4a1db6a57f", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "two wire transfers reported as fraud were not frozen and the claim was denied with no apparent investigation", "is_primary": True}],
    "products": ["checking_or_savings", "money_transfer_or_p2p"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "reported two wire transfers as fraud/scam and asked for them to be stopped, but Chase did not freeze the funds even though it was a Chase-to-Chase transfer",
    "underlying_driver": "the claim was denied with no apparent investigation despite providing the account number, routing number, and recipient name",
    "reason_differs": False,
    "topics": [{"topic_label": "wire transfers not frozen, claim denied", "issue_statement": "Two wire transfers reported as fraud and requested to be stopped were not frozen, even though it was a Chase-to-Chase transfer, and the claim was denied with no apparent investigation.", "product": "money_transfer_or_p2p", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "wire transfers reported as fraud were not frozen despite being a Chase-to-Chase transfer, and the claim was denied with no investigation conducted", "outcome": "unresolved", "evidence": [
        {"quote": "To no avail they didn't freeze the wires I was given a claim # and was told that they will be investigating and a representative would get in touch with me. No one has reach out and a letter from Chase was sent to me stating the claim is denied.", "speaker": "narrative"},
        {"quote": "I have reported this to Elder Fraud Hot line, left a message for XXXX XXXX and now filing a complaint regarding my bank with you. I will also be reporting this to OCC and FTC and my local police department.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Two wire transfers reported as fraud were never frozen despite being a Chase-to-Chase transfer, and the claim was denied without any apparent investigation, prompting reports to multiple regulators."
}}

records["cfpb_12960928"] = {"key": "2ce2d533a6b7114c51d21d0bedd513c0d5e44b37053e6e61e5eeb96fea1e6b04", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "a fraud dispute for over $11,000.00 was denied despite a police report and FTC affidavit", "is_primary": True}],
    "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "a fraud dispute for over $11,000.00 in unauthorized transactions was denied despite a police report, FTC affidavit, and evidence the transactions occurred online without the customer's involvement",
    "underlying_driver": "Chase failed to conduct a reasonable investigation or provide documentation proving the charges were authorized, prompting threats of legal action",
    "reason_differs": False,
    "topics": [{"topic_label": "$11,000 fraud dispute denied despite evidence", "issue_statement": "A fraud dispute for over $11,000.00 was denied despite a police report, an FTC Identity Theft Affidavit, and evidence the transactions occurred online without the customer's involvement.", "product": "credit_card", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "$11,000.00+ in disputed transactions denied with no reasonable investigation despite a police report and FTC affidavit", "outcome": "unresolved", "evidence": [
        {"quote": "Despite providing : A police report An FTC Identity Theft Affidavit Proof the majority of transactions occurred online Communications with merchants confirming my lack of involvement Chase has wrongfully denied my chargeback request", "speaker": "narrative"},
        {"quote": "Failure to take corrective action will result in legal proceedings seeking full relief for statutory, actual, and punitive damages.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A fraud dispute for over $11,000.00 was denied despite a police report and FTC affidavit, prompting the customer to threaten legal action."
}}

records["cfpb_13473953"] = {"key": "33ca5c30deff1983352bad675dc2ec26a117e38ff6cdc684b2a65f53c1740e37", "response": {
    "contact_reasons": [{"reason": "fees_and_charges", "specific_reason": "charged again for chargebacks and fees on transactions already covered by a $100,000.00 reserve", "is_primary": True}],
    "products": ["other_or_unspecified"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "a $100,000.00 reserve was established to cover chargebacks and fees, but the business is still being separately charged for refunds and chargebacks on the same transactions",
    "underlying_driver": "this results in double-charging for transactions whose original funds were never received, and the business demands the reserve be used and prior charges refunded",
    "reason_differs": False,
    "topics": [{"topic_label": "double-charged for chargebacks despite reserve", "issue_statement": "A $100,000.00 reserve was set up specifically to cover chargebacks and fees, yet the business is being separately charged again for refunds and chargebacks on transactions whose original funds were never received.", "product": "other_or_unspecified", "sentiment": -2, "driver_category": "unexpected_charge", "driver": "charged again for chargebacks and fees on transactions already covered by a $100,000.00 reserve specifically established for that purpose", "outcome": "unresolved", "evidence": [
        {"quote": "these funds were withheld from our daily settlements and/or debited from our settlement account, and you explicitly stated they would be used to satisfy any amounts owedsuch as chargebacks and associated fees.", "speaker": "narrative"},
        {"quote": "we are currently being charged again for refunds and chargebacks, for transactions tied to funds that you are already holding.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A merchant account was double-charged for chargebacks and fees on transactions already covered by a $100,000.00 reserve fund set up for exactly that purpose."
}}

records["cfpb_14026260"] = {"key": "d8de0b7aa1bdd7aca8e16cfea231f990373013975fc09854b734aa66ad9f8083", "response": {
    "contact_reasons": [{"reason": "dispute_or_chargeback", "specific_reason": "a dispute over a fully refundable $870.00 ticket was denied despite proof of eligibility", "is_primary": True}],
    "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "a fully refundable $870.00 return ticket dispute was denied by Chase despite proof of the refund eligibility",
    "underlying_driver": "Chase told the customer not to contact them again about the issue after a second attempt, even though the merchant's handling looked like fraud",
    "reason_differs": False,
    "topics": [{"topic_label": "refund dispute denied and told not to contact again", "issue_statement": "A dispute over an $870.00 fully refundable ticket was denied by Chase despite proof of eligibility, and the customer was told not to contact them again about it.", "product": "credit_card", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "denied a refund dispute for an $870.00 fully refundable ticket despite documentation, and told not to contact again after a second attempt", "outcome": "unresolved", "evidence": [
        {"quote": "The Chase credit card company denied the claim and told me not contact again for the issue after second attempt even though it was obvious fraud", "speaker": "narrative"},
        {"quote": "In the meantime my mother has already left after purchasing a new ticket as the ticket with XXXX was in suspended status even after reaching out to XXXX.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A dispute over an $870.00 fully refundable ticket was denied despite documentation proving eligibility, and Chase told the customer not to contact them again."
}}

records["cfpb_14596453"] = {"key": "3d1a56f08abcd8649f0d8cdd8eec0e5cc8fbca067ac147a2a69dc813a2285ebf", "response": {
    "contact_reasons": [
        {"reason": "account_opening_or_closure", "specific_reason": "a closure request after repeated unauthorized transactions was redirected into a trouble ticket, and the account was later closed and restricted", "is_primary": True},
        {"reason": "unauthorized_or_fraud", "specific_reason": "this was the third unauthorized transaction incident in three months", "is_primary": False}
    ],
    "products": ["checking_or_savings"], "services": ["branch", "phone_support"], "customer_ask": "stop_or_block",
    "stated_reason": "after a third unauthorized-transaction incident in three months, the customer asked to close the account but was told to file a trouble ticket instead, and the account was later closed and restricted",
    "underlying_driver": "despite being told the account was restricted with nothing going in or out, overdraft notices keep arriving, and the customer feels they shouldn't be responsible for charges after their initial closure request",
    "reason_differs": False,
    "topics": [{"topic_label": "closure request redirected, overdraft notices persist", "issue_statement": "A request to close the account after a third unauthorized-transaction incident was redirected into a trouble ticket, and even after the account was closed and restricted, overdraft notices keep arriving.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "error_not_corrected", "driver": "account closure request redirected to a trouble ticket, and overdraft notices continue even though the account is supposedly restricted with nothing moving", "outcome": "unresolved", "evidence": [
        {"quote": "The banker informed me that I couldn't close the account but had to submit a trouble ticket - so i sat in the bank lobby on the phone with the XXXX number to submit the fraud claim.", "speaker": "narrative"},
        {"quote": "I continue to receive notices of the account being overdrawn even after being told that the account was restricted and nothing was going in or out.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A request to close an account after a third unauthorized-transaction incident was redirected into a trouble ticket, and overdraft notices kept arriving even after the account was closed and restricted."
}}

records["cfpb_15239711"] = {"key": "94f79ff800750883054e0663e9625f21e6992bcb70cd233cabe09abc1300318c", "response": {
    "contact_reasons": [
        {"reason": "credit_reporting", "specific_reason": "a 90-day delinquency was reported during an active forbearance renewal process", "is_primary": True},
        {"reason": "loan_servicing", "specific_reason": "Chase's own processing delay in approving the forbearance renewal caused the reporting gap", "is_primary": False}
    ],
    "products": ["mortgage"], "services": ["phone_support"], "customer_ask": "fix_error",
    "stated_reason": "Chase reported a 90-day delinquency during an active forbearance renewal process, despite reapplying before the first forbearance ended",
    "underlying_driver": "Chase's own processing delay in approving the renewal, not any customer inaction, caused the reporting gap, contradicting assurances from a relationship manager",
    "reason_differs": False,
    "topics": [{"topic_label": "delinquency reported during processing delay", "issue_statement": "A 90-day delinquency was reported during an active forbearance renewal that Chase itself delayed approving, contradicting assurances that credit would not be affected during the review.", "product": "mortgage", "sentiment": -1, "driver_category": "error_not_corrected", "driver": "90-day delinquency reported for a gap caused by Chase's own delay in approving a forbearance renewal, despite assurances credit would not be affected", "outcome": "unresolved", "evidence": [
        {"quote": "Chase reported me 90 days delinquent in XX/XX/year>XXXX  during an active forbearance renewal process.", "speaker": "narrative"},
        {"quote": "My relationship manager told me my credit would not be affected during the review.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A 90-day delinquency was reported during a forbearance renewal that Chase's own processing delay caused, contradicting assurances that credit would not be affected."
}}

records["cfpb_15883045"] = {"key": "5af45133ed56835cd33a7151c0c74a83595357274312afae1d3e035299bb5fd5", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "two unauthorized $280.00 debit charges were denied after the fraud department gave false verification instructions", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "two unauthorized $280.00 debit charges were reported, but the fraud department gave incorrect information about a verification process that didn't exist",
    "underlying_driver": "after being forced to make many calls for consistent information, Chase denied the claim, shifting the burden to the customer to obtain merchant documentation, which the merchant provided but Chase still denied",
    "reason_differs": False,
    "topics": [{"topic_label": "false verification instructions, burden shifted to customer", "issue_statement": "The fraud department gave false information about obtaining a token from Technical Support, and Chase ultimately denied the claim after shifting the burden onto the customer to prove no relationship with the merchant.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information", "driver": "fraud department gave false instructions about a token verification process, requiring many calls, and the burden was shifted onto the customer to gather merchant proof", "outcome": "unresolved", "evidence": [
        {"quote": "the XXXX Department told me I could obtain a token number from Technical Support to prove the charges did not originate from my device. When I called XXXX XXXX, they stated that they had no knowledge of such a process and that the information given by Fraud was incorrect.", "speaker": "narrative"},
        {"quote": "The merchant acknowledged my inquiry, escalated the issue to their processor, and filed a report, but Chase still denied my claim.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Chase's fraud department gave false instructions about a nonexistent verification process for two unauthorized $280.00 charges, then denied the claim after shifting the proof burden to the customer."
}}

records["cfpb_16625381"] = {"key": "a7179704f30a16cedeb6b59d073ad19c38920942866ff4c1e4409945833d7f65", "response": {
    "contact_reasons": [
        {"reason": "funds_hold_or_account_restriction", "specific_reason": "a $12,000.00 cashier's check deposit was frozen for over a year over shifting phone verification requirements", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "five CFPB complaints about this issue have been closed without resolution", "is_primary": False}
    ],
    "products": ["checking_or_savings", "money_transfer_or_p2p"], "services": ["branch", "phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "a $12,000.00 cashier's check deposit led to the account being closed and the funds frozen because Chase's Fraud Prevention Department could not verify the maker of the check",
    "underlying_driver": "over more than a year of weekly follow-up calls, the phone-number verification requirement kept shifting, leaving the funds permanently stuck with no resolution path even after five CFPB complaints",
    "reason_differs": False,
    "topics": [
        {"topic_label": "$12,000 frozen over shifting verification requirements", "issue_statement": "A $12,000.00 cashier's check deposit was frozen and the account closed because Chase could not verify the check's maker, and after more than a year of follow-up the verification requirements kept shifting with no resolution.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "$12,000.00 frozen for over a year while Chase's phone verification requirements for the check's maker kept shifting, from an inactive number to needing the number in public records", "outcome": "unresolved", "evidence": [
            {"quote": "The Chase Fraud Department mentioned that the only way to clear the check is by verifying with the maker of the check through a phone call.", "speaker": "narrative"},
            {"quote": "It's been already more than a year since my fund is held by Chase Bank. I'm still calling Chase Fraud Prevention Department and asking for an update. However, there is still no way out.", "speaker": "narrative"}
        ]},
        {"topic_label": "repeated CFPB complaints closed without resolution", "issue_statement": "Five CFPB complaints about this issue have been closed without resolution, and Chase provides no explanation when contacted directly.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "no_response_or_follow_up", "driver": "five CFPB complaints filed and closed without any explanation from Chase about the underlying issue", "outcome": "unresolved", "evidence": [
            {"quote": "This is my fifth time filing a complaint through CFPB and the complaints always closed right away.", "speaker": "narrative"},
            {"quote": "I called Chase Bank and there is no explanation about my complaints.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A $12,000.00 cashier's check deposit has been frozen for over a year under shifting phone-verification requirements, and five CFPB complaints have been closed without any explanation from Chase."
}}

records["cfpb_17208132"] = {"key": "9211ec751a94eed95f489b0f61eafc5bffa36fdf6876f145b147e0f16d2c6b6c", "response": {
    "contact_reasons": [{"reason": "account_opening_or_closure", "specific_reason": "accounts held for almost 10 years are being closed with the notice mailed only to an inaccessible old address", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["phone_support", "online_banking"], "customer_ask": "explanation",
    "stated_reason": "accounts held for almost 10 years are being closed, with notice only mailed to an outdated address the customer can no longer access",
    "underlying_driver": "Chase refused to give any further information or post the notice online, leaving the customer scrambling to redo years of auto payments and linked children's accounts",
    "reason_differs": False,
    "topics": [{"topic_label": "closure notice sent only to inaccessible address", "issue_statement": "Accounts held for almost 10 years are being closed, but the notice was mailed only to an old Oregon address the customer can no longer access, and Chase refused to post it online or give more details.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "denied_or_declined_without_explanation", "driver": "closure notice mailed only to an inaccessible old address, with Chase refusing to post it online or provide further details", "outcome": "unresolved", "evidence": [
        {"quote": "Told them I am at house in Florida and have become Florida resident and can not access it. Asked them why it was not posted on-line so I could read it under messages and notices. They did not have answer for it. They refused to give me any more information.", "speaker": "narrative"},
        {"quote": "This is outrageously wrong, capricious, arbitrary and morally wrong. Have trusted this bank for almost 10 years. This should be illegal.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Accounts held for almost 10 years are being closed, but the notice was mailed only to an old, inaccessible address, and Chase refused to post it online or give further details."
}}

records["cfpb_18227992"] = {"key": "b9117fec58b9b765e8314e76edbb64bea8bc448700c3646b755eed6ad288692e", "response": {
    "contact_reasons": [{"reason": "collections_or_debt", "specific_reason": "continued calls about an auto loan tied to alleged seller fraud despite revoked consent", "is_primary": True}],
    "products": ["auto_loan"], "services": ["phone_support"], "customer_ask": "stop_or_block",
    "stated_reason": "Chase continues calling about an auto loan tied to alleged fraudulent misrepresentation by the seller, despite the customer revoking consent to verbal contact in writing multiple times",
    "underlying_driver": "calls keep coming from different numbers and branches with repeated voicemails demanding a callback",
    "reason_differs": False,
    "topics": [{"topic_label": "continued calls despite revoked consent", "issue_statement": "Chase keeps calling from multiple numbers about an auto loan tied to alleged seller fraud, despite the customer revoking consent to verbal contact in writing over ten times.", "product": "auto_loan", "sentiment": -2, "driver_category": "repeated_contact_needed", "driver": "continued calls from many different numbers despite the customer revoking verbal contact consent in writing more than ten times", "outcome": "unresolved", "evidence": [
        {"quote": "I put this in writing over XXXX times now. XXXX still refuses to stop harassing me over an auto loan that has to do with fraudulent misrepresentation from the seller of the XXXX loan.", "speaker": "narrative"},
        {"quote": "Calling from XXXX different numbers - locations - branches - leaving constant voicemails just saying we need a return phone call after I have revoked consent.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Chase keeps calling from many different numbers about an auto loan tied to alleged seller fraud, despite the customer revoking verbal-contact consent in writing more than ten times."
}}

records["cfpb_18650234"] = {"key": "4add658bdaddeaa823fab6c20f55bc11d9329f1c540ed4d54b31749de9f65bfe", "response": {
    "contact_reasons": [
        {"reason": "dispute_or_chargeback", "specific_reason": "a Chase Travel advisor's confirmed misinformation caused an unnecessary $1,100.00 purchase, but Chase refused to correct the billing", "is_primary": True},
        {"reason": "terms_information_or_communication", "specific_reason": "the advisor incorrectly said flight credits were non-transferable when they were not", "is_primary": False}
    ],
    "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "a Chase Travel advisor incorrectly said flight credits were non-transferable, causing an unnecessary $1,100.00 ticket purchase instead of using the transferable credits",
    "underlying_driver": "despite Chase's own investigation confirming the misinformation caused the charge, it has repeatedly refused to correct the billing error, offering shifting and inconsistent reasons for denial",
    "reason_differs": False,
    "topics": [{"topic_label": "confirmed misinformation caused unnecessary purchase", "issue_statement": "A Chase Travel advisor incorrectly said flight credits were non-transferable, causing an unnecessary $1,100.00 purchase, and despite Chase's own investigation confirming the misinformation, it has refused to correct the billing error.", "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information", "driver": "advisor's confirmed misinformation about non-transferable credits caused an unnecessary $1,100.00 purchase, which Chase refuses to reverse despite verifying the error", "outcome": "unresolved", "evidence": [
        {"quote": "Multiple subsequent reviews by Chase of the recorded call have confirmed that the advisor provided me with this misinformation, and XXXX XXXX has confirmed with both myself and Chase that the credits were, in fact, transferable", "speaker": "narrative"},
        {"quote": "Despite finding in its investigation that the Chase XXXX advisor provided incorrect information and that this misinformation caused the charge, Chase has refused to correct the billing error.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A Chase Travel advisor's confirmed misinformation about non-transferable flight credits caused an unnecessary $1,100.00 purchase, and Chase has refused to correct the billing error despite verifying the mistake."
}}

records["cfpb_19693072"] = {"key": "6265c8b7966786f3aed0fde205e916cb42abfabe443189bc72f5efb4d6170a3a", "response": {
    "contact_reasons": [{"reason": "funds_hold_or_account_restriction", "specific_reason": "claims Chase blacklisted the customer's identity and froze account access following unauthorized device access", "is_primary": True}],
    "products": ["other_or_unspecified"], "services": [], "customer_ask": "fix_error",
    "stated_reason": "alleges that after unauthorized access to a mobile device, Chase used an internal system to blacklist identity and freeze account access",
    "underlying_driver": "the account of events is largely unclear, referencing concepts that are difficult to substantiate from the text alone",
    "reason_differs": False,
    "topics": [{"topic_label": "account access frozen following alleged hack", "issue_statement": "The customer says Chase blacklisted their identity and froze account access following unauthorized access to their mobile device, and is demanding the flags be removed.", "product": "other_or_unspecified", "sentiment": -1, "driver_category": "other_or_unclear", "driver": "claims an internal flagging system was used to freeze account access following unauthorized device access, demanding the flags be removed", "outcome": "unknown", "evidence": [
        {"quote": "Following unauthorized access to my mobile device ( Hacking reported to FBI IC3 ), XXXX weaponized the XXXX XXXX XXXX XXXX XXXXXXXX  ) system to blacklist my identity.", "speaker": "narrative"},
        {"quote": "I demand the immediate removal of all manual XXXX  flags and full restoration of access to my assets.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unknown", "positive_moments": [], "redaction_heavy": True,
    "summary": "The customer alleges Chase used an internal flagging system to blacklist their identity and freeze account access after a reported device hack, demanding the flags be removed."
}}

records["cfpb_20166718"] = {"key": "532d55f7ceec17e149ce8a45f6d034da0b1bc5963e01490dd9b2ef548c14c9a6", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "a $390.00 fraudulent charge was removed twice then reappeared, with Chase now calling it legitimate", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["phone_support", "mobile_app"], "customer_ask": "refund_or_reversal",
    "stated_reason": "a $390.00 charge initially declined was somehow authorized, removed twice after being confirmed fraudulent, but reappeared and Chase now insists it's legitimate",
    "underlying_driver": "Chase bases its legitimacy determination solely on the fraudster having used the customer's email, phone number, and address, disregarding the declined-charge text, police report, and transfer receipt provided as evidence",
    "reason_differs": False,
    "topics": [{"topic_label": "fraudulent charge reinstated after being removed twice", "issue_statement": "A $390.00 charge that was declined, then authorized, then removed twice after being confirmed fraudulent, reappeared and Chase now insists it is legitimate.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "a $390.00 fraudulent charge removed twice reappeared, with Chase basing 'legitimate' on the fraudster having obtained the customer's email, phone, and address", "outcome": "unresolved", "evidence": [
        {"quote": "On XX/XX/XXXX I noticed the charge was not removed and called Chase Bank again and got confirmation that it would be removed. The charge was removed.", "speaker": "narrative"},
        {"quote": "Chase responded on XX/XX/XXXX through their app messages that they were reconfirming their stance that the fraudulent charge was legitimate because my email, phone number and address was used to make the fraudulent money withdrawal.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A $390.00 fraudulent charge was removed twice after being confirmed fraud, but it reappeared and Chase now insists it is legitimate based only on the fraudster having the customer's contact information."
}}

records["cfpb_21242934"] = {"key": "79e0b530b0505000d56c7362f0603d2756957302cca2692a9b3205a5d79c86d2", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "$4,000.00 in Zelle transfers processed despite a real-time fraud call requesting all transactions be blocked", "is_primary": True}],
    "products": ["checking_or_savings", "money_transfer_or_p2p"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "after being robbed and immediately locking the stolen phone and calling Chase's fraud department to block transactions, $4,000.00 in unauthorized Zelle transfers were still processed",
    "underlying_driver": "Chase issued repeated generic denials calling the transactions authorized without addressing the robbery, the real-time fraud notification, or the request to block transactions, and has not provided requested investigation details",
    "reason_differs": False,
    "topics": [{"topic_label": "zelle transfers processed despite fraud block request", "issue_statement": "Despite calling Chase's fraud department the evening of a robbery to report the stolen phone and request all transactions be blocked, $4,000.00 in unauthorized Zelle transfers were still processed.", "product": "money_transfer_or_p2p", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "$4,000.00 in Zelle transfers processed after the customer called Chase's fraud department to report a robbery and explicitly request all transactions be blocked", "outcome": "unresolved", "evidence": [
        {"quote": "During that call, I clearly instructed Chase to block all transactions and secure my account. Despite this real-time notification of fraud, Chase allowed XXXX transfers XXXX be processed from my account.", "speaker": "narrative"},
        {"quote": "Chase issued repeated generic denials dated XX/XX/XXXX and XX/XX/year>, stating that the transactions were authorized. These responses did not address the facts of the robbery, the immediate fraud notification, or my request to block transactions.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "After reporting a robbery and asking Chase's fraud department to block all transactions, $4,000.00 in Zelle transfers went through anyway, and Chase repeatedly denied the claims as authorized without addressing the robbery."
}}

records["cfpb_22438334"] = {"key": "398a84459589548dbb94cafa74a96280cb20e41b74b6dd1e174247fa06e57716", "response": {
    "contact_reasons": [
        {"reason": "rewards_or_promotions", "specific_reason": "reward points lost significant value after a transfer between spousal accounts despite repeated assurance otherwise", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "Chase confirmed the representative gave wrong information but a supervisor said nothing could be done", "is_primary": False}
    ],
    "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "was assured multiple times that transferring a spouse's points would not affect their value, but the points lost significant value after the transfer",
    "underlying_driver": "Chase confirmed the representative gave wrong information and promised resolution, but a supervisor later said nothing could be done",
    "reason_differs": False,
    "topics": [{"topic_label": "points lost value despite repeated assurance", "issue_statement": "A representative repeatedly swore that transferring the wife's points would not affect their value, but the points lost significant value after the transfer was completed.", "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information", "driver": "representative repeatedly assured no value loss before a points transfer, but the points lost significant value afterward", "outcome": "unresolved", "evidence": [
        {"quote": "I checked with the representative that I talked to at least XXXX times that my wife 's point will not lose valuation which is currently worth XXXX per XXXX point. He swore to me the whole time it will not affect it so I went ahead and transferred the points and when I checked it XXXX weeks after it did lose the value", "speaker": "narrative"},
        {"quote": "I called them back again XX/XX/XXXX and I was told by a supervisor there's nothing they can do so basically I have to suffer the consequences of them having a rep that's not properly train or lied to me and Chase won't take responsibility for their mistakes.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A representative repeatedly promised that transferring a spouse's reward points would not affect their value, but the points lost significant value afterward, and Chase says nothing can be done."
}}

records["cfpb_23226244"] = {"key": "6ec2ef17f3126e16b61cd6eff8eaf8b4bf95d330b4678bf5d514106ffcdd9ccf", "response": {
    "contact_reasons": [
        {"reason": "account_opening_or_closure", "specific_reason": "legitimate pandemic unemployment deposits from another state caused the account to be flagged and closed", "is_primary": True},
        {"reason": "funds_hold_or_account_restriction", "specific_reason": "funds were frozen for two to three months before being released with no explanation", "is_primary": False}
    ],
    "products": ["checking_or_savings"], "services": [], "customer_ask": "fix_error",
    "stated_reason": "legitimate out-of-state pandemic unemployment benefit deposits caused the account to be flagged as suspicious and closed, freezing the funds for months",
    "underlying_driver": "no proper explanation or apology was given, and now the customer's identity/SSN is permanently restricted internally, blocking any new account",
    "reason_differs": False,
    "topics": [
        {"topic_label": "legitimate benefits flagged, funds frozen for months", "issue_statement": "Legitimate out-of-state pandemic unemployment deposits caused the account to be flagged as suspicious and closed, freezing the funds for two to three months without a proper explanation.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "legitimate pandemic unemployment deposits from another state caused the account to be closed and funds frozen for months with no explanation given", "outcome": "resolved", "evidence": [
            {"quote": "Because of these out-of-state government deposits, Chase flagged my account as suspicious and abruptly closed it.", "speaker": "narrative"},
            {"quote": "My legitimate funds were frozen for XXXX to XXXX months before being released, causing severe financial strain, and I was never given a proper explanation or apology.", "speaker": "narrative"}
        ]},
        {"topic_label": "permanent identity restriction blocks new accounts", "issue_statement": "Chase has permanently restricted the customer's identity and SSN internally, preventing any new account from being opened even though no fraud occurred.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "identity/SSN permanently restricted internally after a mistaken fraud flag, blocking any new account despite no actual fraud", "outcome": "unresolved", "evidence": [
            {"quote": "Now, I am trying to open a new account and discovered that Chase has permanently restricted my identity/SSN in their internal system.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "partially_resolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Legitimate pandemic unemployment deposits caused an account to be flagged, closed, and frozen for months, and now the customer's identity is permanently restricted from opening any new Chase account."
}}

records["cfpb_9504216"] = {"key": "22e82cacae311a9f571298f97389c63949eec97d6d9e34b8f687fc03bb4f31a9", "response": {
    "contact_reasons": [
        {"reason": "access_or_digital_banking", "specific_reason": "repeated login failures across multiple browsers and phone-only two-factor verification have blocked bill payment access", "is_primary": True},
        {"reason": "fees_and_charges", "specific_reason": "a late fee was incurred because being locked out prevented paying on time", "is_primary": False}
    ],
    "products": ["credit_card"], "services": ["online_banking", "mobile_app"], "customer_ask": "fix_error",
    "stated_reason": "persistent login problems, including repeated 'unsupported browser' messages across three different browsers and device-recognition failures, have blocked access to view and pay bills",
    "underlying_driver": "the only verification methods require a phone the customer doesn't have working, with no email option, and this compounds a separate unresolved dispute about the correct legal name on the account, resulting in late fees",
    "reason_differs": False,
    "topics": [
        {"topic_label": "persistent login failures blocking bill payment", "issue_statement": "Repeated 'unsupported browser' errors across three browsers and device-recognition failures have blocked online access needed to view and pay bills, with only phone-based verification offered and no email option.", "product": "credit_card", "sentiment": -1, "driver_category": "system_or_app_failure", "driver": "repeated login failures across multiple browsers plus phone-only two-factor verification with no working phone have blocked bill payment access", "outcome": "unresolved", "evidence": [
            {"quote": "The first problem is that the login page will tell me that the browser is no longer supported which has resulted in me having to install a new browser. I've had this issue on XXXX, and then XXXX, and then XXXX.", "speaker": "narrative"},
            {"quote": "I can not verify my account either because it only provides XXXX methods of verification, each requires a phone and my phone is XXXX There is no email verification option.", "speaker": "narrative"}
        ]},
        {"topic_label": "late fees from being locked out", "issue_statement": "Being unable to log in has already caused one late fee and risks another, along with a possible negative credit report mark.", "product": "credit_card", "sentiment": -1, "driver_category": "unexpected_charge", "driver": "a late fee was incurred because login was blocked, and continued lockout risks another late fee and a negative credit report mark", "outcome": "unresolved", "evidence": [
            {"quote": "I last was able to make a payment on XX/XX/XXXX for $180.00 which included a late fee from not being able to login to pay in XXXX.", "speaker": "narrative"},
            {"quote": "I believe that this is intentional. By making it as difficult as possible to login they actively ensure that I pay them fees.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Repeated login failures across multiple browsers and phone-only verification have blocked bill payment access, already causing one late fee and risking a negative credit report mark."
}}

records["cfpb_9804113"] = {"key": "30593897b84ec58ac0e7d4a22fec7f5e60625ee2d9498f9aca4fedaa18527c52", "response": {
    "contact_reasons": [{"reason": "rewards_or_promotions", "specific_reason": "a $200.00 savings bonus confirmed as met by a branch employee was never applied", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["branch", "chat_or_email"], "customer_ask": "refund_or_reversal",
    "stated_reason": "a $200.00 savings bonus tied to a multi-step promotion was never applied even though a branch employee confirmed on screen that the requirements were met",
    "underlying_driver": "the employee promised a follow-up email and never sent it, and two further email follow-ups requesting a status update or escalation went completely unanswered",
    "reason_differs": False,
    "topics": [{"topic_label": "savings bonus confirmed met but never paid", "issue_statement": "A branch employee showed on his screen that the $200.00 savings bonus requirements were met and promised a follow-up email, but the bonus was never applied and no follow-up ever came.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "no_response_or_follow_up", "driver": "branch employee confirmed the $200.00 bonus requirements were met and promised a follow-up email, but never sent it, and two later emails requesting a status update went unanswered", "outcome": "unresolved", "evidence": [
        {"quote": "XXXX XXXX assured me that I had met the requirements for the savings account bonus, showing me on his screen that this was the case.", "speaker": "narrative"},
        {"quote": "I followed up on XX/XX/2024, emailing XXXX XXXX directly asking for a status update. He never responded. I followed up again on XX/XX/2024 emailing XXXX XXXX for an update, or to escalate. He never responded.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A branch employee confirmed on screen that a $200.00 savings bonus's requirements were met and promised a follow-up email, but the bonus was never applied and subsequent emails went unanswered."
}}

records["cfpb_10136094"] = {"key": "8dbe76a8612c79af84f0b9598a3afd839dd3406d3f05402698cc439d088cbac8", "response": {
    "contact_reasons": [{"reason": "funds_hold_or_account_restriction", "specific_reason": "payroll and business deposits were frozen without explanation and remain unreleased after the account was closed", "is_primary": True}],
    "products": ["checking_or_savings"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "payroll and business deposits were frozen by Chase without any explanation",
    "underlying_driver": "the account was subsequently closed, but the frozen funds still have not been released to the customer or the business over a month later",
    "reason_differs": False,
    "topics": [{"topic_label": "payroll deposits frozen and unreleased", "issue_statement": "Payroll and business deposits were frozen without explanation, the account was later closed, but the funds have still not been released over a month later.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "payroll and business deposit funds remain frozen and unreleased more than a month after the account was closed, with no explanation given", "outcome": "unresolved", "evidence": [
        {"quote": "Chase Bank froze these funds without any explanation.", "speaker": "narrative"},
        {"quote": "They subsequently closed the account, but have not yet released these funds to me or back to the business.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Payroll and business deposits were frozen without explanation, and the funds remain unreleased more than a month after the account was closed."
}}

records["cfpb_10431935"] = {"key": "19c678bcb71b8727e615e8387f3aec688c42f9e348a69c57b3e45b0473eecb84", "response": {
    "contact_reasons": [
        {"reason": "customer_service_experience", "specific_reason": "employees allegedly provoke and mistreat customers with disabilities and mental health conditions in branches and by phone", "is_primary": True},
        {"reason": "account_opening_or_closure", "specific_reason": "the checking account is being closed, which will bounce a government direct deposit relied on for medications", "is_primary": False}
    ],
    "products": ["checking_or_savings"], "services": ["branch", "phone_support"], "customer_ask": "stop_or_block",
    "stated_reason": "JPMorgan Chase notified the customer that their checking account would be closed, which will disrupt a government direct deposit relied on for medications",
    "underlying_driver": "the customer describes a pattern of Chase employees provoking and mistreating customers with disabilities and mental health conditions, and being unaccommodating over the phone despite documented medical limitations",
    "reason_differs": True,
    "topics": [
        {"topic_label": "account closure will disrupt direct deposit", "issue_statement": "Chase's notice that the checking account will be closed threatens a financial burden because a government direct deposit will bounce, delaying access to funds needed for medications by 14 to 30 days.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "denied_or_declined_without_explanation", "driver": "checking account being closed over alleged 'inappropriate behavior' will bounce a government direct deposit relied on for medications, with a 14-30 day delay to reissue", "outcome": "unresolved", "evidence": [
            {"quote": "On XXXX JP Morgan Chase Bank sent me a letter stating they were going to close my checking account ending in XXXX on XX/XX/year>. This will cause me a FINANCIAL BURDEN because i get paid a Direct Deposit from The Government", "speaker": "narrative"},
            {"quote": "Now my Direct Deposit will be sent back and i'll have to wait at least 14 to 30 days to wait for it to go back and for them to reissue the payment which will cause me to not be able to pay for medications i need that my insurance doesn't pay for.", "speaker": "narrative"}
        ]},
        {"topic_label": "pattern of callous treatment toward customers with disabilities", "issue_statement": "The customer describes Chase employees repeatedly provoking, mocking, and mistreating customers with disabilities and mental health conditions in branches and over the phone.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "staff_attitude_or_competence", "driver": "employees allegedly provoke and mock customers with disabilities, keep them on long calls despite stated medical limitations, and a supervisor ignores repeated complaints", "outcome": "unresolved", "evidence": [
            {"quote": "Instead of Chase employees trying to work with XXXX or XXXX XXXX customers that might be going thru a crisis over the phone or in a branch their employees will just make fun of you then play the victim.", "speaker": "narrative"},
            {"quote": "the Supervisor at this Location just walk around as if she doesn't see anything and she'll just tell you she'll call you and never do because it's been months and i never heard from her.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A checking account closure threatens to disrupt a government direct deposit needed for medications, amid a broader complaint about Chase employees allegedly provoking and mistreating customers with disabilities."
}}

records["cfpb_10840355"] = {"key": "f60dcc519d373d064e25482a503df01088718d95f9ec4ec86fa6165d2f7424b0", "response": {
    "contact_reasons": [{"reason": "credit_decision_or_limit", "specific_reason": "a credit limit was cut from $21,000.00 to $6,900.00, exactly matching the balance and spiking utilization to 100%", "is_primary": True}],
    "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "fix_error",
    "stated_reason": "a credit limit was cut from $21,000.00 to $6,900.00 (matching the balance, causing 100% utilization) with only a vague, shifting explanation",
    "underlying_driver": "an earlier similar cut during the pandemic was handled the same way, offering only a fresh hard credit pull that changes nothing, and the rep admitted nothing would differ from days earlier",
    "reason_differs": False,
    "topics": [
        {"topic_label": "credit limit slashed to match balance", "issue_statement": "A credit limit was cut from $21,000.00 to $6,900.00, exactly matching the balance and pushing utilization to 100%, tanking the credit score.", "product": "credit_card", "sentiment": -2, "driver_category": "policy_or_terms_change", "driver": "credit limit lowered from $21,000.00 to $6,900.00, exactly matching the balance and spiking utilization to 100%, based on vague reasoning about other non-Chase accounts", "outcome": "unresolved", "evidence": [
            {"quote": "I looked into it and found out Chase lowered my credit line from $21000.00 down to $6900.00, which is what the balance on the card was, putting me at 100 % usage, skyrocketing my monthly minimum and tanking my credit score.", "speaker": "narrative"},
            {"quote": "I was told the decision was not because of my good relationship with Chase, but because some of my other NON-Chase accounts were 'higher than they like '. It always seems to be a different vague reason with no basis of merit.", "speaker": "narrative"}
        ]},
        {"topic_label": "offered only a pointless hard credit pull", "issue_statement": "When asking for reconsideration, Chase's only offer was another hard credit pull, which the representative admitted would show nothing different from days earlier.", "product": "credit_card", "sentiment": -2, "driver_category": "staff_attitude_or_competence", "driver": "offered a new hard credit pull to 'reconsider' the cut even though the representative admitted nothing would be different from the pull days earlier", "outcome": "unresolved", "evidence": [
            {"quote": "they offered to \" reconsider '' by again doing a hard pull of my credit, even knowing nothing would be different from XXXX days ago, and the rep on the phone didn't deny it either, but they're willing to hurt their customers credit even more with a hard inquiry", "speaker": "narrative"},
            {"quote": "This PREDATORY practice hurts Chase customers not only financially, but in regards to XXXX XXXX too and it shouldn't be allowed to continue.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A credit limit was slashed to exactly match the balance, spiking utilization to 100% and tanking the credit score, and Chase's only offer to reconsider was a pointless new hard credit pull."
}}

for call_id, rec in records.items():
    (out / f"{call_id}.json").write_text(json.dumps({"key": rec["key"], "prompt_version": "ext-1.0",
        "schema_version": "1", "taxonomy_version": "1", "call_id": call_id, "model": "claude-agent-build",
        "produced_by": "claude_agent", "created_at": "2026-09-11T12:00:00Z", "usage": None,
        "response": rec["response"]}, ensure_ascii=False), encoding="utf-8")
print("wrote", len(records))
