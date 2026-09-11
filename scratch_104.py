# -*- coding: utf-8 -*-
import json, pathlib

bundle = json.load(open("data/work/extract_bundles/bundle_104.json", encoding="utf-8"))
texts = {r["call_id"]: r["text"] for r in bundle["records"]}
keys = {r["call_id"]: r["cache_key"] for r in bundle["records"]}

records = {}

records["cfpb_15981357"] = {
  "contact_reasons": [
    {"reason": "credit_reporting", "specific_reason": "requesting deletion of an account resulting from unauthorized use, reported to the Sheriff's Office over two years ago", "is_primary": True}
  ],
  "products": ["credit_reporting_service"], "services": [], "customer_ask": "fix_error",
  "stated_reason": "requesting deletion of an account from her credit report resulting from unauthorized use of her credit",
  "underlying_driver": "the itemized statements needed to pursue criminal charges were never received, and now the window to prosecute has closed",
  "reason_differs": False,
  "topics": [
    {"topic_label": "account from unauthorized use never removed",
     "issue_statement": "An account resulting from unauthorized use of the customer's credit, reported to the Sheriff's Office over two years ago, remains on her credit report, and requested itemized statements were never provided.",
     "product": "credit_reporting_service", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "itemized statements requested to pursue criminal charges for unauthorized use were never received, and the account remains on the credit report past the window to prosecute",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The account in question was the result of unauthorized use of my credit, which I reported to the XXXX XXXX Sheriff 's Office over two years ago.", "speaker": "narrative"},
       {"quote": "Despite my efforts, I never received the itemized statements I requested in order to pursue criminal charges.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A customer is requesting deletion of a credit report account resulting from unauthorized use reported to police over two years ago, after never receiving the itemized statements needed to pursue charges."
}

records["cfpb_16718281"] = {
  "contact_reasons": [
    {"reason": "credit_decision_or_limit", "specific_reason": "credit application denied for having too many credit cards despite a strong credit profile", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "underwriting supervisor was disrespectful and hung up rather than transferring the call", "is_primary": False}
  ],
  "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "explanation",
  "stated_reason": "requesting review of a denied credit application and investigation into disrespectful treatment by an underwriting supervisor",
  "underlying_driver": "the application was denied citing too many credit cards despite a strong profile, and the underwriting supervisor hung up rather than transfer the call to his superior",
  "reason_differs": False,
  "topics": [
    {"topic_label": "application denied for too many credit cards",
     "issue_statement": "A credit application was denied despite a strong credit profile, excellent payment history and high income, with the stated reason being too many credit cards.",
     "product": "credit_card", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "denied for having too many credit cards despite a strong credit profile, high income, and excellent payment history",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "which was denied despite my strong credit profile, excellent payment history, and high verified income.", "speaker": "narrative"},
       {"quote": "I was told the reason was that I have too many credit cards, which seems inconsistent, as I know individuals with more open accounts and lower income who were approved for Chase products.", "speaker": "narrative"}
     ]},
    {"topic_label": "supervisor hung up during application call",
     "issue_statement": "During a call about the denial, an underwriting supervisor was disrespectful and hung up after refusing to transfer the customer to his superior.",
     "product": "credit_card", "sentiment": -2, "driver_category": "staff_attitude_or_competence",
     "driver": "underwriting supervisor hung up after refusing to transfer the call to his superior",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I was treated in a disrespectful and unprofessional mannerhe hung up on me after refusing to transfer my call to his superior, XXXX.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A credit application was denied for having 'too many credit cards' despite a strong profile, and an underwriting supervisor hung up on the customer rather than transfer the call, prompting a request for review and investigation."
}

records["cfpb_17294974"] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "a $400.00 checking bonus confirmed owed still hasn't been paid months after the account was closed before it posted", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "months of conflicting instructions across calls and branch visits with no resolution", "is_primary": False}
  ],
  "products": ["checking_or_savings"], "services": ["branch", "phone_support"], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $400.00 new-account bonus paid after qualifying for it before the account was closed",
  "underlying_driver": "Chase closed the checking account for lack of funds before the bonus posted, then gave conflicting instructions over months - a promised check, a branch visit, a new account - without ever depositing the bonus",
  "reason_differs": False,
  "topics": [
    {"topic_label": "$400 bonus never paid after account closure",
     "issue_statement": "After qualifying for a $400.00 new-account bonus, Chase closed the checking account for lack of funds before the bonus posted, and months of calls, a branch visit, and opening a new account still have not resulted in payment.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned",
     "driver": "$400.00 bonus confirmed owed by both phone reps and a branch manager, but unpaid for months after the account closed before it posted",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Without notice, before the bonus posted, Chase closed the checking account for lack of funds.", "speaker": "narrative"},
       {"quote": "We're now in XXXX XXXX and while Chase agrees that I'm owed the bonus, they don't seem to know how or have a mechanism to deposit the bonus amount.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "the branch manager researched and confirmed the bonus was owed and tried to help get it paid", "category": "helpful_staff",
     "quote": "She researches and confirms that I did qualify the for the bonus.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A $400.00 new-account bonus was confirmed owed by both phone support and a branch manager, but months after the checking account closed before the bonus posted, Chase still has not found a way to pay it."
}

records["cfpb_18280222"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a replacement business credit card was issued without consent and used for unauthorized purchases and $22,000.00 in payments", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "Chase has refused to provide account records, transaction details, or documentation despite repeated requests", "is_primary": False}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "explanation",
  "stated_reason": "requesting investigation, release of account records, and reversal of unauthorized activity on a business credit card",
  "underlying_driver": "a former business partner's false report led Chase to issue an unauthorized replacement card, alter alert settings, and allow unauthorized purchases and $22,000.00 in payments without the rightful owner's knowledge, and Chase has refused to provide records",
  "reason_differs": False,
  "topics": [
    {"topic_label": "unauthorized replacement card issued and used",
     "issue_statement": "After a former business partner falsely reported items as undelivered, Chase issued a replacement business credit card without the owner's knowledge, mailed it to an inaccessible address, and it was used for unauthorized purchases and $22,000.00 in payments.",
     "product": "credit_card", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "replacement card issued and mailed without consent to an inaccessible mailbox, then used for unauthorized purchases totaling $22,000.00",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase issued a replacement credit card without my knowledge or consent and mailed it to a mailbox I did not have access to and did not have a key for.", "speaker": "narrative"},
       {"quote": "I received Chase statements showing multiple payments made to this same business credit card totaling $22000.00. I did not make these payments and did not authorize them.", "speaker": "narrative"}
     ]},
    {"topic_label": "records and documentation refused",
     "issue_statement": "Despite repeated requests, Chase has refused to provide account records, transaction details, access logs, or documentation explaining how the replacement cards were issued or why the account was altered.",
     "product": "credit_card", "sentiment": -2, "driver_category": "no_response_or_follow_up",
     "driver": "repeated requests for account records, mailing history, and an explanation of alert changes have all been refused",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Despite repeated requests, Chase has refused to provide account records, transaction details, access logs, mailing history, or documentation explaining how replacement cards were issued, where they were mailed, who made the payments, or why the account was altered without my consent.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "After a former business partner's false report, Chase issued a replacement business credit card without consent, mailed it to an inaccessible address, altered fraud alert settings, and allowed $22,000.00 in unauthorized payments, while refusing to provide any account records."
}

records["cfpb_18815092"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "two ATM withdrawals totaling $700.00 debited without dispensing cash, claims denied without a Regulation E-compliant investigation", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["atm"], "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting reimbursement of $700.00 for two failed ATM withdrawals or documented proof cash was dispensed",
  "underlying_driver": "Chase denied both ATM error claims without providing the electronic journal, cash cassette reconciliation, or network trace required for a reasonable investigation under Regulation E",
  "reason_differs": False,
  "topics": [
    {"topic_label": "atm debited without dispensing cash, claims denied",
     "issue_statement": "Two ATM withdrawals of $400.00 and $300.00 debited the account without dispensing cash, and Chase denied both claims without providing the ATM electronic journal or cash cassette reconciliation required under Regulation E.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "$700.00 in ATM errors denied without the electronic journal, cassette reconciliation, or network trace required for a reasonable Regulation E investigation",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "On XX/XX/scrub>, 2025, I attempted to withdraw $400.00 from an ATM. My account was debited, but no cash was dispensed.", "speaker": "narrative"},
       {"quote": "Chase denied my claims without providing the ATM electronic journal, cash cassette reconciliation, or network trace, as required for a reasonable investigation under Regulation XXXX ( XXXX XXXX XXXX ).", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Two ATM withdrawals totaling $700.00 debited the account without dispensing cash, and Chase denied both claims without providing the electronic journal or cassette reconciliation required for a proper Regulation E investigation."
}

records["cfpb_20299079"] = {
  "contact_reasons": [
    {"reason": "fees_and_charges", "specific_reason": "residual interest charged after paying off a balance transfer promo that expired, and a goodwill adjustment request was denied", "is_primary": True}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting a one-time goodwill adjustment of $240.00 in interest charges after a balance transfer promo expired",
  "underlying_driver": "a calendar misunderstanding let the promo expire, generating $180.00 in interest, and even after paying in full within 14 days, an additional $52.00 in residual interest was charged; Chase refused any goodwill adjustment despite years of perfect payment history",
  "reason_differs": False,
  "topics": [
    {"topic_label": "goodwill adjustment denied after promo expiration",
     "issue_statement": "A balance transfer promo expired due to a calendar misunderstanding, generating $180.00 in interest plus $52.00 in residual interest after paying in full within 14 days, and Chase refused a one-time $240.00 goodwill adjustment citing 'system limitations.'",
     "product": "credit_card", "sentiment": -1, "driver_category": "denied_or_declined_without_explanation",
     "driver": "$180.00 promo-expiration interest plus $52.00 residual interest after paying in full within 14 days; a $240.00 goodwill adjustment was refused citing system limitations despite 7 years of perfect payment history",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase supervisors refuse a one-time goodwill adjustment of $240.00, citing \" system limitations. ''", "speaker": "narrative"},
       {"quote": "I paid the balance in full within 14 days, but was hit with an additional $52.00 in residual interest.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A calendar mix-up let a balance transfer promo expire, generating $180.00 in interest plus $52.00 in residual interest despite paying in full within 14 days, and Chase refused a $240.00 goodwill adjustment for a 7-year, perfect-payment customer."
}

records["cfpb_21420835"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a $120.00 Zelle payment for medication was made under false pretenses by a scammer impersonating a pharmacy, and the fraud claim was denied", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting the fraud claim be reviewed again and the $120.00 reimbursed",
  "underlying_driver": "the seller impersonated a legitimate pharmacy and demanded additional undisclosed fees to release the package, and Chase and Zelle denied the fraud claim saying the customer chose to send the payment",
  "reason_differs": False,
  "topics": [
    {"topic_label": "zelle scam payment denied as fraud",
     "issue_statement": "A $120.00 Zelle payment for medication was made to a seller who then demanded an undisclosed $100.00 fee to release the package; the seller was impersonating a pharmacy, but the fraud claim was denied because the customer had chosen to send the payment.",
     "product": "money_transfer_or_p2p", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "$120.00 Zelle payment made under false pretenses to a fake pharmacy, and the claim was denied on the grounds that the customer chose to send the payment via Zelle",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I was told that I chose to send the money through XXXX, however this transaction was made under false pretenses.", "speaker": "narrative"},
       {"quote": "I was misled into sending money under false pretenses, as the seller was impersonating a legitimate pharmacy, and I was later pressured for additional payments through what appears to be a fake shipping company.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A $120.00 Zelle payment for medication went to a seller impersonating a pharmacy who then demanded an undisclosed fee, but Chase denied the fraud claim on the grounds that the customer chose to send the payment."
}

records["cfpb_22643383"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "8 months trying to get Chase to reverse fraudulent merchant charges despite zero-liability terms", "is_primary": True}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants Chase to reverse fraudulent charges to the merchant and credit the account, per its own zero-liability terms",
  "underlying_driver": "a merchant fraudulently charged the credit card, and despite 8 months of effort and the card's zero-liability terms, Chase has not reversed the charges",
  "reason_differs": False,
  "topics": [
    {"topic_label": "8 months without reversal of fraudulent charges",
     "issue_statement": "A merchant fraudulently charged the credit card $740.00 and $120.00, and after 8 months Chase still has not reversed the charges despite its own zero-liability terms.",
     "product": "credit_card", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "8 months without reversal of fraudulent merchant charges despite the card's zero-liability policy; the customer says Chase is effectively keeping the money",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "for the last 8 months I have tried to get Chase to reverse it.", "speaker": "narrative"},
       {"quote": "Chase is stealing money from me unless they reverse this fraud.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A merchant fraudulently charged the credit card $740.00 and $120.00, and after 8 months without reversal despite the card's zero-liability terms, the customer says Chase is effectively keeping the money."
}

records["cfpb_23445428"] = {
  "contact_reasons": [
    {"reason": "fees_and_charges", "specific_reason": "monthly service fees charged despite veteran fee-waiver eligibility recognized since 2015; only the most recent $25.00 fee refunded", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting reimbursement of all improperly assessed monthly service fees since Chase had prior knowledge of his veteran status",
  "underlying_driver": "Chase recognized the customer's veteran fee-waiver status as early as 2015 but began charging monthly fees anyway, refunding only the most recent fee and citing a refund limit for the rest",
  "reason_differs": False,
  "topics": [
    {"topic_label": "veteran fee waiver not honored for prior charges",
     "issue_statement": "Despite recognizing the customer's veteran status for a fee waiver since 2015, Chase charged monthly service fees and refunded only the most recent $25.00 fee, citing a standard refund limit rather than correcting the underlying account error.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "error_not_corrected",
     "driver": "veteran fee-waiver status recognized since 2015 but not maintained on the account, and Chase refunded only the latest $25.00 fee, refusing earlier fees due to a standard refund-limit policy",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase refunded only the most recent $25.00 fee and confirmed that my account has now been enrolled in military benefits and that future monthly service fees will not be charged.", "speaker": "narrative"},
       {"quote": "Chase refused to refund the earlier fees, stating only that my account had reached its limit of standard refunds for the calendar year.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "partially_resolved",
  "positive_moments": [
    {"what": "Chase confirmed enrollment in military benefits so future fees will not be charged", "category": "fair_outcome",
     "quote": "confirmed that my account has now been enrolled in military benefits and that future monthly service fees will not be charged.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "Although Chase recognized the customer's veteran fee-waiver status as early as 2015, it charged monthly service fees anyway and refunded only the most recent $25.00, refusing to reimburse the rest under a standard refund-limit policy."
}

records["cfpb_9562545"] = {
  "contact_reasons": [
    {"reason": "credit_reporting", "specific_reason": "an unrecognized $150.00 JPMCP Card balance appears intermittently on the credit report though no such card was ever opened", "is_primary": True}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "fix_error",
  "stated_reason": "wants Chase to investigate and remove an unrecognized $150.00 card balance that intermittently appears on the credit report",
  "underlying_driver": "a $150.00 balance under an unfamiliar 'JPMCP Card' appears and disappears on the credit report even though the customer never opened any such account, possibly from a mistake or identity theft",
  "reason_differs": False,
  "topics": [
    {"topic_label": "unrecognized jpmcp card balance appearing",
     "issue_statement": "A $150.00 balance under an unfamiliar 'JPMCP Card' intermittently appears and disappears on the credit report, though the customer has not opened any store or general credit card.",
     "product": "credit_card", "sentiment": -1, "driver_category": "other_or_unclear",
     "driver": "an unrecognized $150.00 card balance intermittently appears on the credit report despite the customer never opening any such account",
     "outcome": "unknown",
     "evidence": [
       {"quote": "It appears as JPMCP Card with a balance of $150.00. I have not opened any credit cards with any stores or a credit card in general.", "speaker": "narrative"},
       {"quote": "I have already got my credit messed up by a apartment that falsely accused me of ending my lease early and now this is bringing down my credit as well.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unknown", "positive_moments": [], "redaction_heavy": False,
  "summary": "An unrecognized $150.00 'JPMCP Card' balance intermittently appears on the customer's credit report even though she never opened such an account, compounding separate credit damage from a disputed apartment lease claim."
}

records["cfpb_9849737"] = {
  "contact_reasons": [
    {"reason": "terms_information_or_communication", "specific_reason": "a letter about migrating from Premier Plus to Sapphire Checking omitted the option to simply keep the current account", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "four different representatives gave conflicting information, including a promised callback that turned out to be a stalling tactic", "is_primary": False}
  ],
  "products": ["checking_or_savings"], "services": ["phone_support", "branch"], "customer_ask": "fix_error",
  "stated_reason": "wants to keep his current Premier Plus Checking account without being required to visit a distant branch, after receiving what he considers a deceptive migration letter",
  "underlying_driver": "a letter about the First Republic-to-Chase account migration implied the only options were switching to Sapphire Checking or changing accounts, omitting that keeping the current account required no action beyond an in-branch visit, which four different reps confirmed was required despite acknowledging it was unreasonable",
  "reason_differs": False,
  "topics": [
    {"topic_label": "deceptive migration letter omits keeping current account",
     "issue_statement": "A letter about migrating from the First Republic-based Premier Plus Checking account to Chase Sapphire Checking only presented options to accept the change or switch accounts, never mentioning that the customer could simply keep his current account with no action needed.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "incorrect_or_conflicting_information",
     "driver": "letter's wording implies only two options (accept Sapphire or switch accounts), omitting that keeping the current Premier Plus account required no changes",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Nowhere in the letter does it say I have the option to keep my previous checking account, the account Chase supplied to me following the First Republic acquisition.", "speaker": "narrative"},
       {"quote": "I find the letter that I received from Chase to be highly deceptive as it clearly suggests ( through omission ) that simply maintaining my current account status is not an option.", "speaker": "narrative"}
     ]},
    {"topic_label": "required to visit distant branch just to keep the account",
     "issue_statement": "Multiple customer service agents and a supervisor said the customer must visit a Chase branch, over two hours away, just to keep his current account with no changes.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "policy_or_terms_change",
     "driver": "four representatives, including a supervisor, confirmed a distant branch visit is required just to make no change to the account, with the supervisor acknowledging it was unreasonable but calling it policy",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "customer support told me that in order to keep my current account and make NO CHANGE to my current customer status, that I need to visit a Chase bank branch and speak with a customer representative.", "speaker": "narrative"},
       {"quote": "She acknowledged that requiring a customer to visit a bank branch for no reason whatsoever was unreasonable, but that this is Chase policy.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A letter about migrating from Premier Plus to Chase Sapphire Checking omitted the option to simply keep the current account, and multiple representatives, including a supervisor, said a distant branch visit was required just to make no change; the customer plans to close his account."
}

records["cfpb_10191304"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "account closed and $2,000.00 frozen shortly after a provisional credit and an ATM withdrawal, with no explanation given", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["atm", "phone_support"], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $2,000.00 currently frozen in the closed account released and a clear justification for the closure",
  "underlying_driver": "after Chase funded a provisional credit and let the customer withdraw funds at an ATM, the account was abruptly closed and the remaining balance frozen with no explanation given despite repeated inquiries",
  "reason_differs": False,
  "topics": [
    {"topic_label": "account closed and funds frozen after provisional credit",
     "issue_statement": "After Chase funded a provisional credit and the customer withdrew some of it at an ATM as advised, the account was closed and the remaining $2,000.00 frozen with no explanation despite repeated inquiries.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned",
     "driver": "$2,000.00 frozen after the account closed right after a Chase-advised ATM withdrawal, with no explanation given despite repeated calls",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Shortly after, I attempted to make a XXXX transaction, only to discover that my account had been closed, and the remaining $2000.00 in my account was frozen.", "speaker": "narrative"},
       {"quote": "I immediately contacted Chase Bank and repeatedly asked for an explanation regarding the closure of my account and when I could expect access to my remaining funds. Unfortunately, Chase Bank has provided no clear answers and continues to withhold my money.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "After Chase funded a provisional credit and advised an ATM withdrawal, the account was abruptly closed with the remaining $2,000.00 frozen and no explanation given despite repeated inquiries, leaving the customer unable to make an urgent car payment."
}

records["cfpb_10504857"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a $32.00 disputed hotel charge was credited then silently rebilled and backdated with no notice or dispute option", "is_primary": True}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "explanation",
  "stated_reason": "wants proper notice or explanation for why a $32.00 credited dispute was rebilled and backdated with no way to dispute it",
  "underlying_driver": "the hotel acknowledged the $32.00 charge was an error, but after Chase initially credited the dispute, the charge was rebilled and backdated with no notice or dispute mechanism",
  "reason_differs": False,
  "topics": [
    {"topic_label": "credited dispute silently rebilled",
     "issue_statement": "A $32.00 hotel charge that the hotel itself acknowledged was an error was initially credited by Chase, but was then tagged 'REBILL' and backdated with no notice and no option to dispute it again.",
     "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "$32.00 credit reversed via a 'REBILL' tag backdated to an earlier transaction date, with no notice or way to dispute it, despite the hotel admitting its own error",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "while an initial credit for $32.00 was given the transaction was tagged as \" REBILL '' and backdated with a transaction date of XX/XX/year> and a posting date of XX/XX/year>.", "speaker": "narrative"},
       {"quote": "No notice or other information is viewable and no option to dispute this charge.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A $32.00 hotel charge the hotel admitted was an error was credited by Chase and then silently rebilled and backdated with no notice or way to dispute it again."
}

records["cfpb_10923340"] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a wire transfer was rejected for security review and stuck with no ETA despite repeated calls and an urgent need", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "given contradictory information about being contacted, transferred repeatedly with no back-office contact, then hung up on", "is_primary": False}
  ],
  "products": ["money_transfer_or_p2p"], "services": ["phone_support"], "customer_ask": "fix_error",
  "stated_reason": "wants the wire transfer completed or the review resolved quickly since the funds are urgently needed to pay bills",
  "underlying_driver": "the wire was flagged for a security review with no ETA, agents gave contradictory claims about calling the customer, there was no way to reach the back office handling the review, and the call was hung up when the customer tried to cancel",
  "reason_differs": False,
  "topics": [
    {"topic_label": "wire stuck in security review with no eta or contact",
     "issue_statement": "A wire transfer was rejected for a security review with no estimated timeline, and after five calls in one day the customer could not reach the back office handling it or get a status update, despite urgently needing the funds to pay bills.",
     "product": "money_transfer_or_p2p", "sentiment": -2, "driver_category": "no_response_or_follow_up",
     "driver": "wire stuck under security review with no ETA, no way to contact the reviewing back office, and contradictory claims about attempted callbacks",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Unfortunately Chase just kicked me back and forth from one to another department, saying that it is still under review, and no ETA.", "speaker": "narrative"},
       {"quote": "I asked them to tell me the contact method of the back office, they said there is no contact info!", "speaker": "narrative"}
     ]},
    {"topic_label": "hung up when trying to cancel the wire",
     "issue_statement": "When the customer called to cancel the stuck wire transfer request, Chase hung up the call.",
     "product": "money_transfer_or_p2p", "sentiment": -2, "driver_category": "staff_attitude_or_competence",
     "driver": "call to cancel the wire transfer was simply hung up on",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "then I called to cancel the wire transfer request, but they just hang up my phone call.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A wire transfer was stuck in an unexplained security review with no ETA or contactable back office despite five calls in one day and an urgent need to pay bills, and a call to cancel it was simply hung up on."
}

records["cfpb_11222962"] = {
  "contact_reasons": [
    {"reason": "collections_or_debt", "specific_reason": "collection calls about a late payment, already resolved, exceeded the legal limit of allowed calls", "is_primary": True}
  ],
  "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "stop_or_block",
  "stated_reason": "wants the excessive collection calls to stop since the late payment issue has already been resolved",
  "underlying_driver": "Chase called more than seven times within seven consecutive days, twice the allowed frequency, even after the late payment was resolved",
  "reason_differs": False,
  "topics": [
    {"topic_label": "excessive collection calls after resolved late payment",
     "issue_statement": "After a late credit card payment was resolved, Chase called more than seven times in seven consecutive days, exceeding the legally allowed call frequency.",
     "product": "credit_card", "sentiment": -1, "driver_category": "other_or_unclear",
     "driver": "more than seven collection calls in seven consecutive days, double the allowed frequency, despite the late payment already being resolved",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I was late on my credit card payment, which has since been resolved.", "speaker": "narrative"},
       {"quote": "More than seven times within seven consecutive calendar days", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Even after resolving a late credit card payment, the customer received more than seven collection calls within seven consecutive days, exceeding the legal call limit, and is asking Chase to stop."
}

records["cfpb_11549569"] = {
  "contact_reasons": [
    {"reason": "payment_or_transfer_problem", "specific_reason": "a payment sent to the wrong person could not be recovered, and Chase said nothing could be done", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants help recovering a payment mistakenly sent to the wrong person",
  "underlying_driver": "after noticing the payment went to the wrong recipient, Chase told the customer nothing could be done and the money was gone",
  "reason_differs": False,
  "topics": [
    {"topic_label": "misdirected payment unrecoverable",
     "issue_statement": "A payment sent to the wrong person through the customer's Chase account could not be recovered, with Chase saying nothing could be done and the money was gone.",
     "product": "money_transfer_or_p2p", "sentiment": -1, "driver_category": "money_held_or_not_returned",
     "driver": "payment sent to the wrong recipient was declared unrecoverable, with Chase saying nothing could be done",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I noticed I sent it to the wrong person and tried to contact chase they told Me that there was nothing that they couldnt done and that basically the money was gone", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A payment mistakenly sent to the wrong person could not be recovered, with Chase telling the customer nothing could be done and the money was gone."
}

records["cfpb_12138665"] = {
  "contact_reasons": [
    {"reason": "customer_service_experience", "specific_reason": "trip delay reimbursement claim accidentally cancelled, refiled multiple times, and mishandled with inconsistent agents and lost documents", "is_primary": True}
  ],
  "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "fix_error",
  "stated_reason": "wants the trip delay reimbursement claim finally processed after months of mishandling",
  "underlying_driver": "the claim was accidentally cancelled, had to be refiled multiple times under different categories, documents were repeatedly lost or unconfirmed, and calls ended in disconnections or promises of callbacks that never came, well past the promised 7 business days",
  "reason_differs": False,
  "topics": [
    {"topic_label": "trip delay claim repeatedly cancelled and refiled",
     "issue_statement": "A trip delay reimbursement claim was accidentally cancelled, could not be reopened, and had to be refiled multiple times under different claim types, with documents repeatedly reported as missing despite multiple resubmissions.",
     "product": "credit_card", "sentiment": -2, "driver_category": "no_response_or_follow_up",
     "driver": "claim cancelled and refiled three times under different categories over months, with documents repeatedly reported missing despite resubmission each time",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "In XXXX the claim was \" accidentally '' cancelled because they thought it was a duplicate or mistake.", "speaker": "narrative"},
       {"quote": "am told that cancelled claims cant be opened and I would need to start a new one.", "speaker": "narrative"}
     ]},
    {"topic_label": "inconsistent agents and disconnected calls",
     "issue_statement": "Different agents gave inconsistent instructions, a promised manager callback never happened, and one call was disconnected while the agent claimed to be finding a manager.",
     "product": "credit_card", "sentiment": -2, "driver_category": "staff_attitude_or_competence",
     "driver": "inconsistent, scripted responses from different agents, a promised manager callback that never came, and a call disconnected mid-hold",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "after 2 minutes on hold the agent disconnected the line.", "speaker": "narrative"},
       {"quote": "There is no consistency between the agents who look into these claims and its very obvious they read from a script and fall back on either hanging up on you or telling you to call back in 7 business days.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A Sapphire Reserve trip delay reimbursement claim was accidentally cancelled and had to be refiled three times under different categories, with documents repeatedly reported missing, inconsistent agent instructions, and a disconnected call, well past the promised 7 business days."
}

records["cfpb_12530940"] = {
  "contact_reasons": [
    {"reason": "loan_servicing", "specific_reason": "Chase's buyback valuation is significantly lower for one identical vehicle trim than another following the manufacturer's bankruptcy", "is_primary": True}
  ],
  "products": ["auto_loan"], "services": [], "customer_ask": "explanation",
  "stated_reason": "requesting an investigation into why Chase's buyback offers for identical vehicle trims differ so drastically between owners",
  "underlying_driver": "Chase offered $36,000.00 for one trim while other owners of an identical trim received offers of $55,000.00-$59,000.00, with no clear justification for the disparity",
  "reason_differs": False,
  "topics": [
    {"topic_label": "inconsistent buyback offers for identical trims",
     "issue_statement": "Chase offered $36,000.00 to buy back a vehicle, while owners of an identical trim with the same MSRP received offers of $55,000.00 to $59,000.00, a roughly $20,000.00 gap with no clear explanation.",
     "product": "auto_loan", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "$36,000.00 buyback offer versus $55,000.00-$59,000.00 for an identical trim, a roughly $20,000.00 gap Chase has not explained",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "On XX/XX/XXXX, I received offcial buyback offer from Chase for $36000.00 for XXXX XXXX.", "speaker": "narrative"},
       {"quote": "Chase is offering offering XXXX XXXX owners $20000.00 less.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Following a manufacturer's bankruptcy, Chase offered $36,000.00 to buy back one vehicle trim while owners of an identical trim received $55,000.00-$59,000.00, and the customer is requesting an investigation into the roughly $20,000.00 disparity."
}

records["cfpb_13044949"] = {
  "contact_reasons": [
    {"reason": "balance_or_statement_error", "specific_reason": "a $40,000.00 payment mistakenly approved despite exceeding the $33,000.00 credit limit, unresolved for nearly three months despite submitted documentation", "is_primary": True}
  ],
  "products": ["credit_card"], "services": ["branch", "phone_support"], "customer_ask": "fix_error",
  "stated_reason": "wants the erroneous $40,000.00 payment, mistakenly approved above the credit limit, corrected after nearly three months",
  "underlying_driver": "a $40,000.00 payment intended to be $1,400.00 was approved despite exceeding the $33,000.00 credit limit, and despite submitting all requested documentation including a voided-transaction receipt, the issue remains unresolved after nearly three months",
  "reason_differs": False,
  "topics": [
    {"topic_label": "erroneous over-limit payment unresolved",
     "issue_statement": "A $40,000.00 payment mistakenly made instead of the intended $1,400.00 was approved by Chase despite exceeding the $33,000.00 credit limit, and remains unresolved after nearly three months of calls, branch visits, and submitted documentation.",
     "product": "credit_card", "sentiment": -1, "driver_category": "error_not_corrected",
     "driver": "$40,000.00 payment approved above the $33,000.00 credit limit remains unresolved nearly three months later despite submitting all requested paperwork, including a voided-transaction receipt",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "My credit limit is $33000.00.", "speaker": "narrative"},
       {"quote": "After nearly three months I have not been able to resolve the situation.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A $40,000.00 payment mistakenly made instead of $1,400.00 was approved despite exceeding the $33,000.00 credit limit, and remains unresolved nearly three months later despite submitting all requested documentation."
}

records["cfpb_13581381"] = {
  "contact_reasons": [
    {"reason": "access_or_digital_banking", "specific_reason": "the online dispute tool won't let disputes start online and always redirects to a phone call", "is_primary": True}
  ],
  "products": ["credit_card"], "services": ["online_banking"], "customer_ask": "fix_error",
  "stated_reason": "wants to be able to start and complete a dispute entirely online instead of being forced to call",
  "underlying_driver": "every attempt to file a dispute online redirects to a phone number instead of allowing the dispute to be started digitally",
  "reason_differs": False,
  "topics": [
    {"topic_label": "online dispute tool forces a phone call",
     "issue_statement": "Every time the customer tries to file a dispute online, the site asks them to call the dispute number instead of letting them start it online.",
     "product": "credit_card", "sentiment": -1, "driver_category": "system_or_app_failure",
     "driver": "online dispute flow never lets the dispute be started digitally, always redirecting to a phone call",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Every time it asked me to call the dispute number, it won't let me start the dispute online, this is both a hassle and the inconvenience.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "The online dispute tool for a Chase Freedom card never lets a dispute be started digitally, always redirecting to a required phone call."
}

records["cfpb_14088293"] = {
  "contact_reasons": [
    {"reason": "balance_or_statement_error", "specific_reason": "the amount on a paid charge-off account doesn't match what the bank statement and the Chase receipt show", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["branch"], "customer_ask": "other",
  "stated_reason": "disputing a mismatch between the paid amount on a charge-off account and what the statement and receipt show",
  "underlying_driver": "the charge-off account payment amount doesn't match the statement or receipt, and the customer also disputes fees and a check that reportedly did not post",
  "reason_differs": False,
  "topics": [
    {"topic_label": "mismatched charge-off payment amount",
     "issue_statement": "The amount paid on a charge-off account does not match what the bank statement and the Chase receipt show, and the customer disputes buying the product reflected.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "paid charge-off account amount conflicts with the statement and the Chase receipt",
     "outcome": "unknown",
     "evidence": [
       {"quote": "was a charge off account that has a different price then what my XXXXXXXX XXXX  Statement says and what Chase Receipt says", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unknown", "positive_moments": [], "redaction_heavy": False,
  "summary": "The customer disputes that a paid charge-off account amount doesn't match the bank statement or Chase receipt, alongside confusion over fees and a check that reportedly did not post."
}

records["cfpb_14684823"] = {
  "contact_reasons": [
    {"reason": "access_or_digital_banking", "specific_reason": "a replacement card is repeatedly declined at one specific merchant despite working everywhere else", "is_primary": True}
  ],
  "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "fix_error",
  "stated_reason": "wants the recurring decline of her replacement card at one specific merchant fixed after months of unresolved back-and-forth",
  "underlying_driver": "a replacement card issued after suspected fraud works everywhere except one merchant, where payments are repeatedly declined, with the merchant and Chase blaming each other and promising fixes that never materialize",
  "reason_differs": False,
  "topics": [
    {"topic_label": "replacement card repeatedly declined at one merchant",
     "issue_statement": "A replacement credit card works for every purchase except at one merchant, where payments are repeatedly declined despite re-entering the card three times and hours of calls, with the merchant and Chase each blaming the other.",
     "product": "credit_card", "sentiment": -1, "driver_category": "system_or_app_failure",
     "driver": "replacement card declines only at one merchant, with each company blaming the other and repeated promised fixes never resolving it",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I can successfully use XXXX rewards money to purchase an item from XXXX but can not charge it.", "speaker": "narrative"},
       {"quote": "XXXX blames Chase ; Chase blames XXXX. Each time I am promised a fix -- just wait 1 -- sometimes 2 -- business days!", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A replacement credit card works everywhere except one merchant, where payments are repeatedly declined; the merchant and Chase blame each other, and promised fixes have not resolved the issue after hours of calls."
}

records["cfpb_15339037"] = {
  "contact_reasons": [
    {"reason": "customer_service_experience", "specific_reason": "trip delay claim bounced between coverage categories with lost documents over months", "is_primary": True}
  ],
  "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "fix_error",
  "stated_reason": "wants the trip delay reimbursement claim finally resolved after months of conflicting instructions and lost documents",
  "underlying_driver": "the claim was bounced between trip delay and trip cancellation categories multiple times, with documents reported as not received despite repeated submissions, well past the promised processing time",
  "reason_differs": False,
  "topics": [
    {"topic_label": "claim bounced between coverage types with lost documents",
     "issue_statement": "A trip delay reimbursement claim was closed and reopened three times under different coverage categories over several months, with documents repeatedly reported as not received despite multiple resubmissions.",
     "product": "credit_card", "sentiment": -1, "driver_category": "no_response_or_follow_up",
     "driver": "claim moved between trip delay and trip cancellation coverage three times over months, with documents reported missing despite repeated resubmission, past the stated 7 business days",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Called and was instructed by an agent to close my original claim and re-file under \" Trip Cancellation and XXXX XXXX. '' New claim XXXX opened.", "speaker": "narrative"},
       {"quote": "I have spent months following XXXX instructions, resubmitting documents, and calling repeatedly, without resolution. Chase representatives only redirect me back to XXXX.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A Sapphire Reserve trip delay reimbursement claim was closed and refiled three times under different coverage categories over months, with documents repeatedly reported missing despite resubmission, well past the promised 7 business days."
}

records["cfpb_15982520"] = {
  "contact_reasons": [
    {"reason": "credit_reporting", "specific_reason": "three late payments caused by Chase's own system errors were reported to credit bureaus, and Chase gave a false response to the CFPB denying any record of the issue", "is_primary": True},
    {"reason": "access_or_digital_banking", "specific_reason": "unable to access the online account for three consecutive months due to incorrect contact information in Chase's system", "is_primary": False}
  ],
  "products": ["credit_card"], "services": ["online_banking", "phone_support"], "customer_ask": "fix_error",
  "stated_reason": "requesting removal of three inaccurate late-payment entries caused by Chase's own system errors and correction of Chase's false response to the CFPB",
  "underlying_driver": "incorrect contact information in Chase's system blocked online account access for three months, but despite Chase's own documented acknowledgments (payment plan emails, fee reversals) it reported three late payments to bureaus and falsely told the CFPB it found no record of the access issue",
  "reason_differs": False,
  "topics": [
    {"topic_label": "late payments from chase's own access errors reported to bureaus",
     "issue_statement": "Incorrect contact information in Chase's system blocked online account access for three consecutive months, preventing timely payments, yet Chase reported three consecutive 30-day late payments to credit bureaus without noting its own system caused them.",
     "product": "credit_card", "sentiment": -2, "driver_category": "error_not_corrected",
     "driver": "Chase's own incorrect contact information blocked payment access for three months, but three resulting late payments were still reported to bureaus without noting the cause",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Unable to access online account for three consecutive months due to Chase 's system errors with my contact information. This prevented me from making timely payments.", "speaker": "narrative"},
       {"quote": "Despite Chase 's documented acknowledgment of their system errors, they reported three consecutive 30-day late payments ( XXXX, XXXX, XX/XX/XXXX ) to all credit bureaus without noting these were caused by their technical problems.", "speaker": "narrative"}
     ]},
    {"topic_label": "false statements to the cfpb contradicting chase's own records",
     "issue_statement": "In response to a CFPB complaint, Chase claimed it had no record of the account access issue, directly contradicted by its own emails confirming a payment plan and a contact-information update request.",
     "product": "credit_card", "sentiment": -2, "driver_category": "incorrect_or_conflicting_information",
     "driver": "Chase told the CFPB it found no record of the access issue, contradicted by its own emails documenting the payment plan and contact-info correction request",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase responded with demonstrably false statements, claiming : '' We were not able to locate any interactions with you concerning your inability to access your online account ''", "speaker": "narrative"},
       {"quote": "Chase 's own email dated XX/XX/XXXX, confirming payment plan setup due to account access issues", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "Chase reversed two late fees tied to the access-issue payment plan", "category": "fair_outcome",
     "quote": "Late Fee Reversals : XX/XX/XXXX : - $40.00 XX/XX/XXXX : - $40.00", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "Chase's own incorrect contact information blocked online account access for three months, causing three late payments that were reported to credit bureaus without explanation, and Chase then told the CFPB it had no record of the issue, contradicted by its own emails, severely damaging the customer's ability to get a mortgage or business funding."
}

records["cfpb_16722265"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "a $470.00 fraud claim for unauthorized purchases was denied twice despite evidence the transactions used different devices and shipped to a different address", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting the fraud claim be reopened after providing evidence that unauthorized purchases were made from different devices and delivered to a different address",
  "underlying_driver": "despite photographic and delivery evidence showing the transactions weren't hers, the bank denied the claim twice based on the merchant's assertion of authorization, and the merchant's own fraud department redirected her back to the bank without resolving it",
  "reason_differs": False,
  "topics": [
    {"topic_label": "fraud claim denied despite contradicting evidence",
     "issue_statement": "A $470.00 fraud claim for unauthorized purchases was denied twice based on the merchant's claim of authorization, even though the transactions used different device addresses and shipped to a different delivery address than the customer's home.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "$470.00 fraud claim denied twice despite evidence of different device addresses and a different delivery address than the customer's home",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The transactions were conducted on two different computers that do not match the XXXX  address of my personal device.", "speaker": "narrative"},
       {"quote": "Despite providing this evidence, my claim was denied again, and I was advised to contact XXXX directly.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A $470.00 fraud claim for unauthorized purchases was denied twice despite evidence showing the transactions came from different devices and shipped to a different address, with the merchant and bank each redirecting the customer to the other."
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
