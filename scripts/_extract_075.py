import json, pathlib
out = pathlib.Path(r"C:/Users/RicardsonAlbuquerque/repos/Hack/data/cache/extract")

records = {}

records["cfpb_10428942"] = {"key": "4eba135b8da4c03909ec3fc74a01da8ecc347b98241573e174eff5969e6bd796", "response": {
    "contact_reasons": [{"reason": "funds_hold_or_account_restriction", "specific_reason": "a $1,200.00 check deposit has been restricted for a year over an unresolvable verification method", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["branch", "phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "an online checking account has been restricted for a year because the bank could not verify a $1,200.00 deposited check",
    "underlying_driver": "the bank insists on verifying only through the phone number printed on the check, refusing to use the maker's actual current phone number the customer tracked down and connected them with",
    "reason_differs": False,
    "topics": [{"topic_label": "year-long hold over check verification method", "issue_statement": "A $1,200.00 check deposit has been restricted for a year because the bank will only verify it through the phone number printed on the check, even after the customer independently connected them with the maker's actual current number.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "policy_or_terms_change", "driver": "bank refuses to release the $1,200.00 unless the check is verified through the phone number printed on the check, even though that number is unreachable and the maker's actual number was provided", "outcome": "unresolved", "evidence": [
        {"quote": "the account is restricted due to bank employee unable to verify the check so they cant release the fund.", "speaker": "narrative"},
        {"quote": "the bank employee say the only way to verify the check has to be through the phone number thats on the check, which means they will not release the fund until the check get verified with the maker through the phone number thats on the check.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A $1,200.00 check deposit has been restricted for a year because the bank will only verify it through the phone number printed on the check, ignoring the maker's actual current number the customer supplied."
}}

records["cfpb_10875923"] = {"key": "fbd9c1f9df1715a60bb0589de7ec80bf99b6af6edbcb3f2ff379b2518f043b97", "response": {
    "contact_reasons": [
        {"reason": "terms_information_or_communication", "specific_reason": "the bank refused to provide any receipt or documentation of the account's maturity date, interest rate, or account number", "is_primary": True},
        {"reason": "account_opening_or_closure", "specific_reason": "attempts to close the account and get the money back keep being delayed with new excuses", "is_primary": False}
    ],
    "products": ["other_or_unspecified"], "services": ["branch", "phone_support"], "customer_ask": "close_or_cancel",
    "stated_reason": "after opening an account, the bank refused to provide a receipt with maturity date, interest rate, and account number",
    "underlying_driver": "when trying to get the money back or close the account, the bank kept delaying with new excuses and rules",
    "reason_differs": False,
    "topics": [
        {"topic_label": "no documentation provided after opening", "issue_statement": "After opening the account, the bank refused to provide any receipt showing the maturity date, interest rate, or account number.", "product": "other_or_unspecified", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "the bank refused to provide any documentation of the account's maturity date, interest rate, or account number", "outcome": "unresolved", "evidence": [
            {"quote": "They opened the account but refused to give me a receipt with the maturity date, interest rate, and account number.", "speaker": "narrative"},
            {"quote": "I asked to have my money back because if anything happens to me, my family wouldnt even know that the bank has my money. They said they cant do that.", "speaker": "narrative"}
        ]},
        {"topic_label": "closing the account keeps getting delayed", "issue_statement": "Attempts to close the account and get the money back keep being delayed with new excuses each time the customer calls.", "product": "other_or_unspecified", "sentiment": -1, "driver_category": "repeated_contact_needed", "driver": "told to call back Monday to close, then told to wait 5 more days once Monday arrived, with new rules invoked each time", "outcome": "unresolved", "evidence": [
            {"quote": "I called XXXX and they said to call back on Monday to close the account, and today is Monday and they told me to wait another 5 days.", "speaker": "narrative"},
            {"quote": "They come up with new rules in their favor.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A bank refused to give any documentation for a newly opened account and has repeatedly delayed closing it and returning the money, inventing new rules each time."
}}

records["cfpb_11167735"] = {"key": "615a58a56dd2945f232b3e7fef4958c66782b5661128231f843385e5f7d53625", "response": {
    "contact_reasons": [
        {"reason": "funds_hold_or_account_restriction", "specific_reason": "$19,000.00 in checks were cashed then frozen over a name-discrepancy typo, verifiable only through a phone number tied to the wrong name", "is_primary": True},
        {"reason": "account_opening_or_closure", "specific_reason": "the receiving account is being forcibly closed by Chase while the funds remain unresolved", "is_primary": False}
    ],
    "products": ["checking_or_savings", "money_transfer_or_p2p"], "services": ["phone_support", "branch"], "customer_ask": "refund_or_reversal",
    "stated_reason": "three checks totaling $19,000.00 were cashed by Chase but the proceeds were frozen over a name discrepancy from a typo, and the account is being closed",
    "underlying_driver": "Chase insists the only verification method is a phone number tied to a different name, refuses in-person or alternative documentation, and already cashed the checks so the originating bank cannot recall them",
    "reason_differs": False,
    "topics": [
        {"topic_label": "$19,000 in checks frozen on unfixable name discrepancy", "issue_statement": "Three checks totaling $19,000.00 were cashed by Chase but the funds were frozen over a name-discrepancy typo, and Chase's only accepted verification method uses the wrong name.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "$19,000.00 in checks held over a name typo, with Chase accepting only a phone-based verification tied to the wrong name and refusing in-person alternatives", "outcome": "unresolved", "evidence": [
            {"quote": "Chase Bank cashed these checks, but has frozen the proceeds, citing concerns of fraud, and subsequently directed us through circular argumentation, which offered no means to recover the funds.", "speaker": "narrative"},
            {"quote": "No form of verification would be accepted other than the verified phone number of the writer of the checks.", "speaker": "narrative"}
        ]},
        {"topic_label": "checks cannot be recalled since already cashed", "issue_statement": "Because Chase already cashed the checks, the originating bank confirmed it can no longer recall them, leaving the funds stuck with no resolution path.", "product": "money_transfer_or_p2p", "sentiment": -1, "driver_category": "error_not_corrected", "driver": "checks were cashed before Chase raised its fraud concerns, so the originating bank can no longer recall them", "outcome": "unresolved", "evidence": [
            {"quote": "XXXX also informed that Chase Bank already cashed the checks, thus none of the three checks could be recalled by XXXX.", "speaker": "narrative"},
            {"quote": "XXXX bank account is now being forcefully closed by Chase Bank, and our US $19000.00 checks can not be recalled, returned, explained or cleared.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Chase cashed then froze $19,000.00 in checks over a name typo, will only verify through a phone number tied to the wrong name, and the checks can no longer be recalled since they were already cashed."
}}

records["cfpb_11498788"] = {"key": "aad0f995b93d3d7506c5504104c4bddd58d866db1ac3a6eb411367e7b4fbf2fc", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "lost $200,000.00 to a cryptocurrency investment scam and Chase says the wired funds can no longer be recalled", "is_primary": True}],
    "products": ["checking_or_savings", "money_transfer_or_p2p"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "lost $200,000.00 to a cryptocurrency investment scam and asked Chase to recall the wired funds",
    "underlying_driver": "Chase said the funds are no longer available to be recalled",
    "reason_differs": False,
    "topics": [{"topic_label": "scam losses unrecoverable through chase", "issue_statement": "After losing $200,000.00 to a cryptocurrency investment scam, Chase said the wired funds are no longer available to recall.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "Chase said the funds wired to the scam are no longer available and cannot be recalled", "outcome": "unresolved", "evidence": [
        {"quote": "I have tried to reach out to Chase to recall the funds but this has been abortive as Chase says the funds are no longer available.", "speaker": "narrative"},
        {"quote": "it has become unbearable to suffer this loss without any form of help from the institutions where these funds were made available to scammers.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A cryptocurrency investment scam cost the customer $200,000.00, and Chase says the wired funds are no longer available to recall."
}}

records["cfpb_12056464"] = {"key": "36658d38730aeb65de39a097554f6b2daf3cf0fee88090cd8f8677080b7a3c0c", "response": {
    "contact_reasons": [
        {"reason": "funds_hold_or_account_restriction", "specific_reason": "$84,000.00 in a validated trust account was swept when Chase closed the account", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "Fraud, Legal, and branch staff kept redirecting the case and stalled an escalation", "is_primary": False}
    ],
    "products": ["checking_or_savings"], "services": ["branch", "phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "a business trust account holding $84,000.00 (including a $75,000.00 cashier's check) was frozen for fraud review, documentation proving trustee status was provided and validated, yet the account was still closed and the balance swept",
    "underlying_driver": "despite being told the check would be mailed, it never arrived, and staff give conflicting explanations across the Fraud and Legal departments while a vulnerable adult depends on these funds",
    "reason_differs": False,
    "topics": [
        {"topic_label": "trust account closed and funds swept despite validated documents", "issue_statement": "A $75,000.00 cashier's check plus other deposits totaling $84,000.00 in a validated trust account were swept when Chase closed the account, despite documentation proving trustee status having already been uploaded and confirmed.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "$84,000.00 was swept when Chase closed a trust account it had already validated, and the promised check to return the funds was never mailed", "outcome": "unresolved", "evidence": [
            {"quote": "On XXXX I was notified that Chase closed the account and swept the balance of $84000.00 which included the deposited check, the electronic deposit and some interest.", "speaker": "narrative"},
            {"quote": "I never received the check for the $84000.00 plus interest and contacted XXXX XXXX again. She said, they did not mail the check and it is still being disputed.", "speaker": "narrative"}
        ]},
        {"topic_label": "conflicting departments and stalled escalation", "issue_statement": "Fraud, Legal, and branch staff each redirected the case to another department, and a promised executive complaint was repeatedly delayed.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information", "driver": "Fraud and Legal departments each said the issue belonged to the other, and the branch manager repeatedly delayed filing the promised executive complaint", "outcome": "unresolved", "evidence": [
            {"quote": "XXXX contacted the Fraud department and according to them, this issue was with a different department. If I recall correctly, it was with their legal team. She then called legal and said that this issue had to be resolved by the Fraud department.", "speaker": "narrative"},
            {"quote": "In talking to XXXX XXXX, it is clear to me that CHASE is unable to tell me what the path forward to return these funds back to us.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved",
    "positive_moments": [{"what": "the branch manager validated the trustee documents with the fraud department and initially agreed to reinstate the account", "category": "helpful_staff", "quote": "The Fraud department said that they would reinstate the account.", "speaker": "narrative"}],
    "redaction_heavy": False,
    "summary": "Chase closed a validated trust account and swept $84,000.00, and Fraud, Legal, and branch staff have each redirected the case to another department without returning the funds or filing a promised executive complaint."
}}

records["cfpb_12473785"] = {"key": "34c472dcc38a3c3060330795fa6a9ebbb1e5128b45eb1970012e50fba8e50e83", "response": {
    "contact_reasons": [
        {"reason": "account_opening_or_closure", "specific_reason": "the account was closed without notice or explanation", "is_primary": True},
        {"reason": "fees_and_charges", "specific_reason": "Chase now demands $100.00 back, claiming it sent the wrong closing balance due to its own error", "is_primary": False}
    ],
    "products": ["checking_or_savings"], "services": [], "customer_ask": "stop_or_block",
    "stated_reason": "Chase closed the account without notice, sent a check for the balance, and is now demanding $100.00 back claiming they overpaid due to their own miscalculation",
    "underlying_driver": "the customer believes they should not be penalized for Chase's own error, especially since the account was closed against their will",
    "reason_differs": False,
    "topics": [{"topic_label": "demanded repayment for bank's own miscalculation", "issue_statement": "After closing the account without notice and sending a check for the balance, Chase is now demanding $100.00 back, claiming it sent the wrong amount due to its own error.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "unexpected_charge", "driver": "Chase is demanding $100.00 back for its own miscalculation after closing the account without notice", "outcome": "unresolved", "evidence": [
        {"quote": "Within the last XXXX years, Chase Bank closed my account without prior notice or explanation. After closing the account, they sent me a check for the remaining balance that was in my account at the time of closure.", "speaker": "narrative"},
        {"quote": "Now, after the fact, Chase is claiming that they sent me the incorrect amount and are demanding that I send them $100.00 back.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Chase closed an account without notice and sent a closing check, then later demanded $100.00 back, blaming its own miscalculation."
}}

records["cfpb_12957281"] = {"key": "86a69ad34b379fb1cfcbf896aac0bf2baa6640f5c25c3579f03fb2e12c0f0ada", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "held responsible for $326.00 in reported fraudulent charges after the card was frozen and replaced", "is_primary": True}],
    "products": ["checking_or_savings"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "two fraudulent charges ($230.00 and $96.00) were reported, but Chase later said the customer was responsible and charged for them anyway",
    "underlying_driver": "this reversal happened despite the fraud report, and the customer found many other customers have had the same experience with Chase",
    "reason_differs": False,
    "topics": [{"topic_label": "held responsible for reported fraud charges", "issue_statement": "Two fraudulent charges of $230.00 and $96.00 were reported and the card was replaced, but Chase later determined the customer was responsible and charged for them anyway.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "Chase reversed course and held the customer responsible for $326.00 in reported fraudulent charges after initially freezing the card and issuing a new one", "outcome": "unresolved", "evidence": [
        {"quote": "On XX/XX/XXXX and XX/XX/XXXX I received a notice from chase that I was responsible for the transactions and they charged me for it. This is wrong!!!!", "speaker": "narrative"},
        {"quote": "I have never had an issue with chase before and I can not believe that they would be so unhelpful on this.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Two reported fraudulent charges totaling $326.00 were frozen and a new card issued, but Chase then reversed course and held the customer responsible, charging for them anyway."
}}

records["cfpb_13473947"] = {"key": "6b74812e47f5dffd619fb0923f03ab61b31e1a162542afd103c03ace8dfe8c2b", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "a merchant continues making withdrawals already marked fraudulent by Chase", "is_primary": True}],
    "products": ["checking_or_savings"], "services": [], "customer_ask": "stop_or_block",
    "stated_reason": "a merchant is making fraudulent withdrawals from the checking account that have already been marked as fraudulent by Chase",
    "underlying_driver": "despite being marked fraudulent, the withdrawals remain unresolved",
    "reason_differs": False,
    "topics": [{"topic_label": "fraudulent merchant withdrawals continue despite flagging", "issue_statement": "A merchant continues making fraudulent withdrawals from the checking account even though Chase has already marked them as fraudulent.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "merchant withdrawals already marked fraudulent by Chase but not stopped", "outcome": "unresolved", "evidence": [
        {"quote": "THE MERCHANT [ XXXX ] IS MAKING FRAUDULENT WITHDRAWALS FROM MY CHASE BANK CHECKING ACCOUNT, ALL OF THESE WITHDRAWALS HAVE ALREADY BEEN MARKED AS FRAUDULENT WITH MY CHASE BANK.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A merchant is still making fraudulent withdrawals from the checking account even though Chase has already marked the activity as fraudulent."
}}

records["cfpb_14020974"] = {"key": "e8f80443c75eab8bd786402998bdb614e3c71722df43ae6113f260b17ac2c5bd", "response": {
    "contact_reasons": [
        {"reason": "collections_or_debt", "specific_reason": "different representatives gave conflicting hardship settlement amounts on a business credit card balance", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "Chase refused to provide written settlement terms and a promised supervisor callback never came", "is_primary": False}
    ],
    "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "explanation",
    "stated_reason": "offered to settle a Chase Ink Business Credit Card hardship balance for $3,000.00, but was rejected and given no written terms; multiple representatives gave different settlement offers",
    "underlying_driver": "earlier verbal offers ($3,400.00, $4,000.00) were inconsistently honored or dismissed, promised callbacks never happened, and Chase refuses to share its internal settlement policy in writing",
    "reason_differs": False,
    "topics": [
        {"topic_label": "inconsistent settlement offers across representatives", "issue_statement": "A $3,000.00 settlement offer was rejected and countered at $3,700.00, while earlier verbal offers of $3,400.00 and $4,000.00 from other representatives were selectively enforced or dismissed.", "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information", "driver": "different representatives gave different settlement amounts ($3,400.00, $4,000.00, $3,700.00) and inconsistently decided which ones counted", "outcome": "unresolved", "evidence": [
            {"quote": "I offered to settle the account for $3000.00 flat, paid in full, which was reasonable given my financial hardship and prior settlement discussions. XXXX rejected the offer, countered with $3700.00, and refused to provide a written copy of Chases internal policy that supposedly prevents providing written terms before payment.", "speaker": "narrative"},
            {"quote": "Chase has repeatedly stated that settlement offers dont become valid unless the customer agrees, yet here they were enforcing an older, higher offer while refusing to honor a more recent, lower one.", "speaker": "narrative"}
        ]},
        {"topic_label": "refusal of written terms and no follow-up", "issue_statement": "Chase repeatedly refused to provide written settlement terms or its internal policy, and a promised supervisor callback after a call review never happened.", "product": "credit_card", "sentiment": -1, "driver_category": "no_response_or_follow_up", "driver": "a promised supervisor callback after requesting a call review never came, and written terms or the internal policy were refused every time they were requested", "outcome": "unresolved", "evidence": [
            {"quote": "He said it would take XXXX to XXXX business days and that a supervisor, XXXX ( ID XXXX ), would call me back. No one ever followed up.", "speaker": "narrative"},
            {"quote": "Ive asked for written confirmation multiple times and have been denied every time.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Attempts to negotiate a hardship settlement on a business credit card ran into conflicting offer amounts from different representatives, a refusal to provide written terms, and a promised supervisor callback that never came."
}}

records["cfpb_14590200"] = {"key": "07f03e911b89f5e32b538150dfd529f9a797a654d7848e69ba2c1339ccc55a5c", "response": {
    "contact_reasons": [{"reason": "rewards_or_promotions", "specific_reason": "a branch employee assured a checking account offer code was applied, but Chase later said it was never applied and refused the bonus", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["branch", "phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "opened a checking account with an offer code that a branch employee confirmed would be honored, but Chase later said the offer was never applied and refuses to pay the bonus",
    "underlying_driver": "a likely branch processing error during in-person verification caused the offer code to not be applied, despite verbal assurances",
    "reason_differs": False,
    "topics": [{"topic_label": "promotional bonus never applied despite assurance", "issue_statement": "A branch employee assured the offer code was applied and would be honored, but after completing the requirements Chase said the offer was never applied and refused to pay the bonus.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "branch employee assured the offer code was on the application, but Chase later said it was never applied and refused to honor the bonus", "outcome": "unresolved", "evidence": [
        {"quote": "it was indicated to me by the branch employee that the offer remained on my application and would be honored.", "speaker": "narrative"},
        {"quote": "it was indicated to me that the offer was never applied to the account and that Chase would refuse to honor the bonus.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A branch employee assured a checking account bonus offer code was applied and would be honored, but after meeting the requirements Chase said the offer was never applied and refused to pay it."
}}

records["cfpb_15238203"] = {"key": "eb3718c9ecafe585c2ed44c7fedb8c39db9bbb8f832424ce0fb7b40d6aedf4d7", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "a fraud claim was denied because chip usage was assumed to prove the card was the customer's, despite never traveling to that state", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["phone_support"], "customer_ask": "escalation_or_complaint",
    "stated_reason": "a fraud claim was denied because the transaction used a chip, which Chase says means the card must have been used by the customer",
    "underlying_driver": "the customer insists they've always had possession of their cards and never travels to the state where the fraudulent charge occurred",
    "reason_differs": False,
    "topics": [{"topic_label": "fraud claim denied based on chip usage assumption", "issue_statement": "A fraud claim was denied because the transaction used the card's chip, which a Chase representative said meant it must have been the customer's card, despite never traveling to that state.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "claim denied on the assumption that chip use proves the card was in the customer's possession, despite living far away and never visiting the state where the charge occurred", "outcome": "unresolved", "evidence": [
        {"quote": "The second person in a position of higher authority said that since the card used had a special chip it was my card. This is impossible! I have and have always had the cards in my possession.", "speaker": "narrative"},
        {"quote": "I live in XXXX, NY and am XXXX XXXX XXXX. I NEVER GO TO NEW JERSEY.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A fraud claim was denied because Chase assumed chip usage proved the card was the customer's own, even though they never travel to the state where the charge occurred."
}}

records["cfpb_15879086"] = {"key": "81cf77c41c0a8b2868c3258e719a715c41e575044ef6e392fd217413442e704c", "response": {
    "contact_reasons": [{"reason": "funds_hold_or_account_restriction", "specific_reason": "Chase refused to cash a $100,000.00 settlement check over a name variance between ID documents", "is_primary": True}],
    "products": ["checking_or_savings", "money_transfer_or_p2p"], "services": ["branch"], "customer_ask": "refund_or_reversal",
    "stated_reason": "Chase refuses to cash/deposit a $100,000.00 settlement check due to a name variance between the customer's driver's license and Social Security card, despite a notarized affidavit resolving the discrepancy",
    "underlying_driver": "continued refusal after providing multiple forms of ID and legal documentation leaves the customer unable to access the settlement funds",
    "reason_differs": False,
    "topics": [{"topic_label": "$100,000 settlement check refused over name variance", "issue_statement": "Chase refused to cash a $100,000.00 settlement check because the name on the driver's license differs slightly from the Social Security card, despite a notarized affidavit confirming they refer to the same person.", "product": "money_transfer_or_p2p", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "refused to process a $100,000.00 settlement check over a name variance despite a notarized affidavit and multiple forms of ID confirming identity", "outcome": "unresolved", "evidence": [
        {"quote": "Chase refused to cash/deposit the check because my Drivers License identifies me as XXXX XXXX XXXX XXXX XXXX while my Social Security card identifies me as XXXX XXXX XXXX XXXX", "speaker": "narrative"},
        {"quote": "Despite this, Chase has continued to refuse to honor the check, effectively denying me access to my own settlement funds.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Chase refused to honor a $100,000.00 settlement check over a minor name variance between ID documents, despite a notarized affidavit resolving it."
}}

records["cfpb_16622615"] = {"key": "dbb82b1d50fd41fc070c6a9938627dc70a036fabf237dd462831618fbaeae04c", "response": {
    "contact_reasons": [{"reason": "funds_hold_or_account_restriction", "specific_reason": "a closed account's balance has remained unresolved for almost two years", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "an account was closed almost two years ago and the balance remains unresolved",
    "underlying_driver": "every time the customer calls, they are told the bank is still trying to reach the company that issued the check, with no actual progress",
    "reason_differs": False,
    "topics": [{"topic_label": "nearly two years with no progress", "issue_statement": "An account has been closed for almost two years, and every call gets the same answer that the bank is still trying to reach the check's issuing company, with no change.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "no_response_or_follow_up", "driver": "nearly two years of the same excuse that the bank is still trying to reach the check's issuing company, with no visible progress", "outcome": "unresolved", "evidence": [
        {"quote": "its been almost 2 years since it happened i called many times to find out if they resolved the problem but they always tell me the same thing they try to reach the company where the check came from and try to resolve it but i see no changes", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "An account has stayed closed with its balance unresolved for nearly two years, with every call producing the same unfulfilled promise to reach the issuing company."
}}

records["cfpb_17210731"] = {"key": "f0e2ff5b22ecee28c94af74de5ce237c6152b3fe8267d208f3655c185b3a6a7b", "response": {
    "contact_reasons": [
        {"reason": "payment_or_transfer_problem", "specific_reason": "a $1,000.00 Zelle transfer was confirmed received by email but never appeared in the account", "is_primary": True},
        {"reason": "customer_service_experience", "specific_reason": "a claims supervisor was dismissive and redirected the customer instead of investigating", "is_primary": False}
    ],
    "products": ["checking_or_savings", "money_transfer_or_p2p"], "services": ["online_banking", "phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "a $1,000.00 Zelle transfer was confirmed as received by Chase via email, but the funds never appeared in the account and Chase says it cannot locate them",
    "underlying_driver": "the sending bank confirms the funds were delivered to Chase, but a claims supervisor was dismissive and repeatedly told the customer to pursue the matter with the other bank instead of investigating internally",
    "reason_differs": False,
    "topics": [
        {"topic_label": "$1,000 confirmed received but not credited", "issue_statement": "Chase emailed confirmation that $1,000.00 was received into the account, but the funds never appeared, and Chase says it cannot locate the money despite the sending bank confirming delivery.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned", "driver": "$1,000.00 confirmed received by Chase via email and by the sending bank, but Chase says it cannot locate or credit the funds", "outcome": "unresolved", "evidence": [
            {"quote": "I received an email confirmation from Chase stating that I had received the $1000.00 into my account, including a transaction/confirmation number. However, when I checked my Chase account online, the transaction did not appear at all", "speaker": "narrative"},
            {"quote": "the sending bank, which confirmed that the $1000.00 left my account and has been with Chase since XX/XX/XXXX.", "speaker": "narrative"}
        ]},
        {"topic_label": "dismissive supervisor deflects instead of investigating", "issue_statement": "A claims supervisor acknowledged Chase's own system shows the confirmation but was dismissive and kept directing the customer to the other bank instead of investigating.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "staff_attitude_or_competence", "driver": "supervisor acknowledged the email confirmation exists in Chase's system but was dismissive, offered no apology, and redirected the customer to the other bank", "outcome": "unresolved", "evidence": [
            {"quote": "She was dismissive, did not apologize at any point, and made me feel as if I was at fault despite having clear proof that Chase confirmed receipt of the funds", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Chase confirmed receiving a $1,000.00 Zelle transfer by email but says it cannot locate the funds, and a dismissive claims supervisor kept redirecting the customer to the sending bank instead of investigating."
}}

records["cfpb_18226774"] = {"key": "87a6c0cc01ad28402e45dc909feb83ba19af096392326604b6ca120fbb6bd874", "response": {
    "contact_reasons": [{"reason": "payment_or_transfer_problem", "specific_reason": "$440.00 in child support sent to a closed, charged-off account was confirmed returned but only $43.00 was received back", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "$440.00 in child support was deposited to a closed, charged-off account and Chase confirmed multiple times that the funds were rejected and returned, but the customer only received a $43.00 check for a 'difference'",
    "underlying_driver": "Chase representatives say nothing can be done to recover the federally protected child support funds despite the earlier confirmations that the money was returned",
    "reason_differs": False,
    "topics": [{"topic_label": "child support funds not fully returned despite confirmation", "issue_statement": "$440.00 in child support sent to a closed, charged-off account was confirmed rejected and returned by Chase three times, but only a $43.00 difference check was actually received.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned", "driver": "confirmed three times that $440.00 in child support was rejected and returned, but only a $43.00 difference check was received, with no recovery offered for the rest", "outcome": "unresolved", "evidence": [
        {"quote": "I called Chase bank three times and confirmed through the standard customer service department that the funds were going to be sent back because the account was closed and charged off.", "speaker": "narrative"},
        {"quote": "there was nothing I could do to recover the federally exempt funds that were supposed to be returned to the TXSDU and they were sorry.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "$440.00 in child support sent to a closed, charged-off Chase account was confirmed rejected and returned three times, but only a $43.00 difference check was actually received."
}}

records["cfpb_18647643"] = {"key": "907955fb4489b4b7359237a799d15515f49453bf82aaba01f7e1121ab726731e", "response": {
    "contact_reasons": [
        {"reason": "unauthorized_or_fraud", "specific_reason": "an additional card issued to an unauthorized person on the account led to fraudulent charges", "is_primary": True},
        {"reason": "credit_reporting", "specific_reason": "late payments and a charge-off from the fraudulent charges are still being reported despite the bank's acknowledged error", "is_primary": False}
    ],
    "products": ["credit_card", "credit_reporting_service"], "services": ["phone_support"], "customer_ask": "fix_error",
    "stated_reason": "Chase issued an additional card to an unauthorized person on the account, resulting in fraudulent charges that were disputed but never resolved",
    "underlying_driver": "despite acknowledging it should not have issued the extra card, Chase continues reporting late payments and a charge-off from those fraudulent charges, damaging the credit score",
    "reason_differs": False,
    "topics": [{"topic_label": "unauthorized additional card caused fraud, credit still penalized", "issue_statement": "Chase issued a card to an unauthorized man on the account, leading to fraudulent charges that were disputed, yet Chase kept reporting late payments and a charge-off from them despite acknowledging its own error.", "product": "credit_reporting_service", "sentiment": -1, "driver_category": "error_not_corrected", "driver": "Chase admitted it should not have issued a card to another person, but still reports the resulting fraudulent charges as a charge-off with late payments on the credit file", "outcome": "unresolved", "evidence": [
        {"quote": "they issued out a card also to some male person on the same account. The charges on the account were not made by me, however, after making numerous attempts per telecon with the company and filing several written disputes to no avail, the company kept reporting late payments on my credit report.", "speaker": "narrative"},
        {"quote": "They acknowledged they should not have issued a card to anyone other than myself, but are still penalizing my credit score for the huge error that made in doing so.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Chase issued an extra card to an unauthorized person, causing disputed fraudulent charges, and continues reporting the resulting charge-off and late payments despite admitting its own error."
}}

records["cfpb_19682966"] = {"key": "4053b28e70b2222124db29b109d6729804ceea9c15b4e9181c6b2bb9b55647e9", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "recurring $9.00 charges from an unrecognized merchant were reported as fraud but reimbursement was declined", "is_primary": True}],
    "products": ["checking_or_savings"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "recurring $9.00 charges from an unrecognized merchant were never authorized, but Chase declined reimbursement",
    "underlying_driver": "Chase provided no documentation explaining why the recurring charges were considered authorized",
    "reason_differs": False,
    "topics": [{"topic_label": "recurring unauthorized charges denied reimbursement", "issue_statement": "Recurring $9.00 charges from a merchant the customer never enrolled with were reported as fraud, but Chase declined reimbursement without documentation explaining the decision.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "recurring $9.00 unauthorized charges denied reimbursement with no documentation explaining why they were deemed authorized", "outcome": "unresolved", "evidence": [
        {"quote": "I did not authorize, enroll in, or knowingly approve any subscription or recurring payment with this merchant.", "speaker": "narrative"},
        {"quote": "Chase declined to assist or provide reimbursement and did not provide adequate documentation explaining why the charges were considered authorized.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Recurring $9.00 charges from an unrecognized merchant were reported as fraud, but Chase declined reimbursement without explaining why the charges were considered authorized."
}}

records["cfpb_20166209"] = {"key": "0f40257f9aa16cc87c660a7910ea9da9676598236cd16fe44b8dbaaac4aacd07", "response": {
    "contact_reasons": [{"reason": "terms_information_or_communication", "specific_reason": "a Trip Delay Reimbursement claim was denied on grounds contradicted by the submitted documentation", "is_primary": True}],
    "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
    "stated_reason": "a Trip Delay Reimbursement claim was denied on the grounds the covered card wasn't used and the delay wasn't caused by a covered hazard, though documentation proves both were true",
    "underlying_driver": "a reconsideration request with the same supporting documentation was also denied without addressing the evidence",
    "reason_differs": False,
    "topics": [{"topic_label": "trip delay claim denied on incorrect grounds", "issue_statement": "A Trip Delay Reimbursement claim was denied claiming the covered Chase card wasn't used and the delay wasn't caused by a covered hazard, even though the submitted documentation showed the airfare was charged to the card and the delay was due to weather.", "product": "credit_card", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "claim and reconsideration both denied on the claim that the card wasn't used and weather wasn't a covered hazard, contradicted by the submitted documentation", "outcome": "unresolved", "evidence": [
        {"quote": "The denial letter stated that the covered card was not used to pay for the fare and that the delay was not caused by a covered hazard.", "speaker": "narrative"},
        {"quote": "The reconsideration request was also denied without addressing the documentation demonstrating eligibility.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A Trip Delay Reimbursement claim was denied on grounds directly contradicted by the submitted documentation, and a reconsideration request was denied without addressing the evidence."
}}

records["cfpb_21237341"] = {"key": "4e219e11bfb50a0abaeda2d4b2dd7796352dba289ad39e5d2e98056455af862c", "response": {
    "contact_reasons": [{"reason": "account_opening_or_closure", "specific_reason": "an account was closed with no explanation, and new account applications have since been denied with no reason given", "is_primary": True}],
    "products": ["checking_or_savings"], "services": [], "customer_ask": "explanation",
    "stated_reason": "an account was closed with no explanation, and the customer has since been denied the ability to open any new personal or business account with Chase",
    "underlying_driver": "the customer suspects this stems from identity theft they reported to law enforcement, but Chase has not investigated that possibility or disclosed the reason for the adverse action",
    "reason_differs": False,
    "topics": [{"topic_label": "account closed and reopening denied without explanation", "issue_statement": "An account was closed with no explanation, and the customer has since been unable to open any new personal or business account with Chase, with no reason ever disclosed.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "account closed and all subsequent new account applications denied with no explanation, despite a documented identity theft history that could explain it", "outcome": "unresolved", "evidence": [
        {"quote": "In XXXX, Chase Bank closed my account without providing any explanation for the closure. Since then, I have been unable to open a new personal or business account with Chase, and no reason has ever been given for either the original closure or the continued denial.", "speaker": "narrative"},
        {"quote": "Chase has made no effort to investigate this possibility or allow me to present documentation.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "An account was closed with no explanation, and Chase has since denied every attempt to open a new account without disclosing a reason, despite the customer's documented identity theft history."
}}

records["cfpb_22437267"] = {"key": "d97ac2a2106dd55f90b4735b82e53c09fc0039a31cb02ebaa2d641659282fa61", "response": {
    "contact_reasons": [{"reason": "rewards_or_promotions", "specific_reason": "promised Paze promotional credits were denied on two cards despite checkout confirmations proving qualifying use", "is_primary": True}],
    "products": ["credit_card"], "services": ["online_banking", "phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "enrolled in a Chase/Paze promotional offer on two cards, completed the qualifying transactions, but received only a partial enrollment credit and no promised $50.00 statement credits",
    "underlying_driver": "after months of follow-up, Chase says it cannot verify Paze was used despite checkout confirmation showing it, and handled the two enrolled cards inconsistently",
    "reason_differs": False,
    "topics": [{"topic_label": "promotional credits denied despite proof of use", "issue_statement": "After completing qualifying Paze transactions on two enrolled cards, only one received the $5.00 enrollment credit and neither received the promised $50.00 statement credit, despite checkout confirmations showing Paze was used.", "product": "credit_card", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation", "driver": "Chase said it could not verify Paze was used despite checkout confirmations clearly showing it, after months of follow-up, and treated the two enrolled cards inconsistently", "outcome": "unresolved", "evidence": [
        {"quote": "Chase responded by stating they could not determine whether I used XXXX for the transactions and therefore concluded that the terms and conditions were not met.", "speaker": "narrative"},
        {"quote": "Chase provided inconsistent handling, since one card received the enrollment credit while the other did not, despite both being enrolled and used similarly.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Despite checkout confirmations proving qualifying Paze transactions on two cards, Chase denied the promised $50.00 statement credits and handled the two cards' enrollment credit inconsistently."
}}

records["cfpb_23217933"] = {"key": "84b4b93cc388d82d22e75dcde19df92efd25dc9ddf2230f0a60e1184ce1a6983", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "an impersonation scam led to about $13,000.00 in unauthorized check and debit card activity", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "a caller impersonating Chase's fraud department used urgency and banking language to extract information, leading to about $13,000.00 in unauthorized check and debit card activity",
    "underlying_driver": "the stolen funds included student loan money for rent and living expenses, and the customer is awaiting the outcome of the fraud claims opened with Chase",
    "reason_differs": False,
    "topics": [{"topic_label": "impersonation scam led to unauthorized activity", "issue_statement": "A caller impersonating Chase's fraud department used urgency and specific fraud claims to extract information, resulting in about $10,000.00 in fraudulent check activity and over $3,000.00 in unauthorized debit transactions.", "product": "checking_or_savings", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "impersonation scam led to about $13,000.00 in unauthorized check and debit activity, including student loan money meant for rent and living costs", "outcome": "unresolved", "evidence": [
        {"quote": "Approximately $10000.00 was withdrawn through fraudulent check activity, and more than $3000.00 in unauthorized debit card transactions were made.", "speaker": "narrative"},
        {"quote": "The stolen funds included student loan money intended for rent, school expenses, and basic living costs.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved",
    "positive_moments": [{"what": "reported the fraud within hours and Chase opened claims for both the debit card and check fraud", "category": "fast_resolution", "quote": "I reported the fraud to Chase within XXXX  hours of discovering it. Chase opened a debit card fraud claim, claim number XXXX, and a separate check fraud claim, claim number XXXX.", "speaker": "narrative"}],
    "redaction_heavy": False,
    "summary": "An impersonation scam posing as Chase's fraud department led to about $13,000.00 in unauthorized check and debit activity, including student loan money, with claims now under review."
}}

records["cfpb_9498352"] = {"key": "8ef839e56e2185322e6f2fea83e42e23ce329fe6047999a98dc3f45c8b6b2074", "response": {
    "contact_reasons": [{"reason": "funds_hold_or_account_restriction", "specific_reason": "a remaining account balance has been held for 15 months over an unworkable phone verification requirement", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["phone_support", "branch"], "customer_ask": "refund_or_reversal",
    "stated_reason": "an account balance has remained held for 15 months because Chase's phone-based verification requirement doesn't fit the customer's unique situation",
    "underlying_driver": "in-person verification was previously allowed but the policy changed, and now a third party's phone number registered under someone else's name is required, blocking resolution despite documentation",
    "reason_differs": False,
    "topics": [{"topic_label": "15-month hold blocked by inflexible verification", "issue_statement": "A remaining account balance has been held for 15 months because Chase's phone verification requirement for the third party does not match the customer's documented situation, despite substantial evidence supporting the claim.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned", "driver": "15-month hold on remaining balance blocked because the required phone verification does not match the customer's documented, unique circumstances", "outcome": "unresolved", "evidence": [
        {"quote": "It has been 15 months since my account was closed, and I have yet to receive my remaining balance.", "speaker": "narrative"},
        {"quote": "If no action is taken, I will begin preparing for litigation and seek national media coverage on this matter.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "A 15-month hold on a remaining account balance persists because Chase's phone verification requirement does not fit the customer's documented situation, prompting a threat of litigation and media attention."
}}

records["cfpb_9803098"] = {"key": "20b275ec6e555a8d8555135bd932383d72acb9e2974689b8e29d8bc8bb85e759", "response": {
    "contact_reasons": [{"reason": "account_opening_or_closure", "specific_reason": "cannot close a safety deposit box after moving out of state because Chase requires in-person closure", "is_primary": True}],
    "products": ["other_or_unspecified"], "services": ["branch", "phone_support"], "customer_ask": "close_or_cancel",
    "stated_reason": "attempted multiple times to close a safety deposit box after moving out of state, but Chase requires in-person closure with no alternative",
    "underlying_driver": "a mailed form was initially accepted then later deemed invalid, forcing in-person closure that isn't feasible from out of state, and fees continue to accrue",
    "reason_differs": False,
    "topics": [{"topic_label": "cannot close safety deposit box remotely", "issue_statement": "After moving out of state, the safety deposit box cannot be closed because Chase requires in-person closure, and a mailed closure form that was initially accepted was later deemed invalid.", "product": "other_or_unspecified", "sentiment": -1, "driver_category": "policy_or_terms_change", "driver": "in-person-only closure policy leaves an out-of-state customer unable to close the box, accruing fees despite multiple attempts to close it by mail", "outcome": "unresolved", "evidence": [
        {"quote": "they advised me I needed to send a form which I had taken to a branch and get signed by a Chase employee and then mailed back to the branch where my saved deposit box was located so that it could be closed. I completed that form and sent it in only to continue to get letters saying that the safety deposit box was still open and then I owed money.", "speaker": "narrative"},
        {"quote": "I called that branch and they advised me that the form that I sent in was no longer valid and that I had to come in personally to close the account.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "An out-of-state customer cannot close a safety deposit box because Chase requires in-person closure, even after a mailed closure form was initially accepted and later deemed invalid, and fees keep accruing."
}}

records["cfpb_10135618"] = {"key": "5eb97632cc25e62a3dc2163732106167e49ee19a80845543146dac4b0b87cfd7", "response": {
    "contact_reasons": [
        {"reason": "terms_information_or_communication", "specific_reason": "multiple branch employees repeatedly assured that a foreign currency check would definitely be processed and funded", "is_primary": True},
        {"reason": "payment_or_transfer_problem", "specific_reason": "the check was ultimately returned unpaid because foreign regulators prohibit clearing it", "is_primary": False}
    ],
    "products": ["checking_or_savings", "money_transfer_or_p2p"], "services": ["branch", "phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "multiple Chase branch employees repeatedly and explicitly assured that a foreign currency (rupee) check could definitely be processed and funded within weeks, inducing the customer to open an account and spend thousands from a loan in reliance on that promise",
    "underlying_driver": "the check was ultimately returned unpaid because foreign regulators prohibit clearing it, and after being told it was a 'learning experience' for the branch, Chase offered no remedy for the resulting loss",
    "reason_differs": False,
    "topics": [
        {"topic_label": "repeated false assurances the foreign check would clear", "issue_statement": "Multiple Chase employees repeatedly and explicitly assured that a check from India could 'definitely' be processed and funded within weeks, inducing the customer to open an account and spend thousands of dollars from a loan in reliance.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "incorrect_or_conflicting_information", "driver": "multiple employees, including a manager, repeatedly assured the foreign check would definitely be processed and funded within weeks, before it was returned unpaid", "outcome": "unresolved", "evidence": [
            {"quote": "XXXX XXXX assured me and told me yes, dont worry, Chase can definitely process the check and that I would just have to open an account with Chase and I would see the funds in my account in XXXX weeks, maybe more.", "speaker": "narrative"},
            {"quote": "I told XXXX that was unacceptable and I completely relied on XXXX multiple assurances that XXXX would definitely process the check and fund my account in approximately XXXX weeks and that I am relying on Chase to provide me with those funds so I can pay back a loan.", "speaker": "narrative"}
        ]},
        {"topic_label": "check returned unpaid with no remedy offered", "issue_statement": "The check was returned unpaid because foreign regulators prohibit clearing it, and after acknowledging the assurances were wrong, Chase called it a 'learning experience' but offered no remedy.", "product": "money_transfer_or_p2p", "sentiment": -2, "driver_category": "error_not_corrected", "driver": "the check was returned unpaid due to a foreign clearing restriction Chase staff repeatedly said did not apply, and Chase called it only a 'learning experience' with no remedy offered", "outcome": "unresolved", "evidence": [
            {"quote": "the check, which XXXX assured me, on XX/XX/2024, would \" definitely '' be processed and deposited into my account in approximately XXXX weeks, had been returned unpaid because Foreign Regulators Prohibit Clearing of the Check", "speaker": "narrative"},
            {"quote": "XXXX told me that XXXX will use this opportunity as a learning tool to train XXXX employees in the future but that he could nothing for me.", "speaker": "narrative"}
        ]}
    ],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Multiple Chase employees repeatedly assured a foreign currency check would definitely be processed, inducing thousands of dollars in loan spending, but the check was returned unpaid and Chase called it only a 'learning experience' with no remedy."
}}

records["cfpb_10429012"] = {"key": "9291c6b1d93ff582166ad684ce258a99f6736999ea52ee1a2e2313d7817647a4", "response": {
    "contact_reasons": [{"reason": "unauthorized_or_fraud", "specific_reason": "over $900.00 in fraud disputed four times and denied each time despite proof the fraudster admitted responsibility", "is_primary": True}],
    "products": ["checking_or_savings"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
    "stated_reason": "over $900.00 of unauthorized charges were disputed four times and denied each time, despite email transcripts proving the fraudster admitted responsibility",
    "underlying_driver": "Chase gave false promises about timeframes and callbacks, effectively called the customer a liar, and the resulting overdraft has caused severe financial hardship and mental health strain",
    "reason_differs": False,
    "topics": [{"topic_label": "fraud dispute denied four times despite proof", "issue_statement": "Over $900.00 of unauthorized charges were denied four times even though the fraudster admitted responsibility in writing and the customer provided the email transcripts as proof.", "product": "checking_or_savings", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded", "driver": "over $900.00 in fraud denied four times despite email transcripts in which the person who committed the fraud admitted doing so", "outcome": "unresolved", "evidence": [
        {"quote": "They claim I authorized the transactions when I did not. They broke Reg E rules and the person who committed fraud even admitted that they did so on my account. I provided the email transcripts to chase but they continued to deny and close my claims.", "speaker": "narrative"},
        {"quote": "Theyve basically called me a liar when Ive already proven several times otherwise.", "speaker": "narrative"}
    ]}],
    "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
    "summary": "Over $900.00 in fraud was disputed and denied four times despite email proof of the fraudster's admission, leaving the account overdrawn for months and causing severe hardship."
}}

for call_id, rec in records.items():
    (out / f"{call_id}.json").write_text(json.dumps({"key": rec["key"], "prompt_version": "ext-1.0",
        "schema_version": "1", "taxonomy_version": "1", "call_id": call_id, "model": "claude-agent-build",
        "produced_by": "claude_agent", "created_at": "2026-09-11T12:00:00Z", "usage": None,
        "response": rec["response"]}, ensure_ascii=False), encoding="utf-8")
print("wrote", len(records))
