# -*- coding: utf-8 -*-
import json, pathlib

bundle = json.load(open("data/work/extract_bundles/bundle_105.json", encoding="utf-8"))
texts = {r["call_id"]: r["text"] for r in bundle["records"]}
keys = {r["call_id"]: r["cache_key"] for r in bundle["records"]}

records = {}

records["cfpb_17298478"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "$1,000.00 unauthorized withdrawal unresolved well past the Regulation E deadline with no provisional credit", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the required provisional credit issued for a $1,000.00 unauthorized withdrawal that is well past the Regulation E deadline",
  "underlying_driver": "Chase has not issued provisional credit or resolved the claim well beyond the Regulation E business-day deadline, with no written explanation despite multiple follow-up attempts",
  "reason_differs": False,
  "topics": [
    {"topic_label": "provisional credit not issued past reg e deadline",
     "issue_statement": "Chase has not issued the required provisional credit for a $1,000.00 unauthorized withdrawal well beyond the Regulation E business-day deadline, with no written explanation despite multiple follow-up attempts.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned",
     "driver": "$1,000.00 unauthorized withdrawal unresolved well past the Reg E deadline, with no provisional credit or written explanation despite repeated follow-up",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I reported the unauthorized withdrawal on XX/XX/year>, and Chase has still not issued provisional credit or resolved the claim.", "speaker": "narrative"},
       {"quote": "Today is well beyond the XXXXbusiness-day Regulation E deadline, and I have not received any written explanation, follow-up, or assistance.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase has not issued the required provisional credit for a $1,000.00 unauthorized withdrawal well past the Regulation E deadline, deepening financial hardship for a customer grieving the sudden loss of her daughter."
}

records["cfpb_18281265"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "$740.00 in unauthorized transfers made after a compromised device and passwords were used, claim denied", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"], "services": ["mobile_app"], "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting re-investigation and reversal of a denied claim for $740.00 in unauthorized transfers made via a compromised device",
  "underlying_driver": "a third party used the customer's physically obtained phone and compromised passwords to make $740.00 in transfers, and Chase denied the claim despite Regulation E limits on liability for unauthorized transfers",
  "reason_differs": False,
  "topics": [
    {"topic_label": "denied claim for compromised-device transfers",
     "issue_statement": "A total of $740.00 was transferred without authorization after a third party physically obtained the customer's phone and compromised login credentials, but Chase denied the fraud claim.",
     "product": "money_transfer_or_p2p", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "$740.00 in transfers made via a physically compromised phone and stolen credentials, with the claim denied despite Regulation E's limits on liability for unauthorized transfers",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "a total of $740.00 was stolen from my account via unauthorized XXXX transfers after my mobile device was compromised by a third party.", "speaker": "narrative"},
       {"quote": "Chases denial of this claim is a violation of these federal protections.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "After a third party physically obtained the customer's phone and compromised credentials to make $740.00 in unauthorized transfers, Chase denied the fraud claim despite Regulation E protections limiting liability."
}

records["cfpb_18815381"] = {
  "contact_reasons": [
    {"reason": "fees_and_charges", "specific_reason": "purchase interest repeatedly charged despite paying purchase balances in full each month while a promotional balance transfer is active", "is_primary": True}
  ],
  "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "fix_error",
  "stated_reason": "disputing recurring purchase interest charges despite paying purchase balances in full every month during an active promotional balance transfer",
  "underlying_driver": "Chase repeatedly told the customer purchase interest was an error and reversed it, then after several months admitted an active promotional balance transfer causes all new purchases to accrue interest immediately regardless of full payment, contradicting federal payment allocation rules and prior explanations",
  "reason_differs": False,
  "topics": [
    {"topic_label": "purchase interest charged despite full payment",
     "issue_statement": "Despite paying purchase balances in full every month, Chase repeatedly charged purchase interest while a promotional balance transfer was active, reversing it each time as an 'error' until finally saying the policy is that active promotional transfers always trigger purchase interest.",
     "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "purchase interest charged and reversed as an 'error' multiple times over several months before Chase said the real policy is that an active promotional balance transfer always triggers purchase interest regardless of full payment",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Despite this, Chase repeatedly charged purchase interest at approximately XXXX % APR, even though no purchase balance should have remained after my payments.", "speaker": "narrative"},
       {"quote": "a Chase representative told me that simply having an active promotional balance transfer automatically causes all new purchases to accrue interest immediately at the purchase APR, even if those purchases are later paid in full.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Despite paying purchase balances in full every month, Chase repeatedly charged and then reversed purchase interest during an active promotional balance transfer, before finally claiming a policy that contradicts what representatives said for months."
}

records["cfpb_20331284"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "an impersonator posing as Chase fraud staff closed and reissued the debit card, enabling $10,000.00 in fraudulent ATM and in-branch withdrawals", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "the branch allowed a $9,300.00 in-branch withdrawal without checking ID, and Chase denied the claims without pulling video evidence", "is_primary": False}
  ],
  "products": ["checking_or_savings"], "services": ["branch", "atm", "phone_support"], "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting reimbursement of $10,000.00 in fraudulent withdrawals made after an impersonator manipulated her debit card and a branch let someone withdraw cash without ID",
  "underlying_driver": "a scammer impersonating Chase fraud staff got her to trust him enough to reissue her debit card, and someone then withdrew $10,000.00 across ATM and in-branch transactions, including $9,300.00 in branch without ID verification, while Chase denied the claims and didn't pull the promised video evidence",
  "reason_differs": False,
  "topics": [
    {"topic_label": "impersonator manipulated debit card reissue",
     "issue_statement": "A caller impersonating Chase fraud staff, who was able to authenticate details as Chase normally would and even reached her mother and boyfriend, twice got her debit card closed and reissued over two days.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "an impersonator convincingly posed as Chase fraud staff over two calls, closing and reissuing the debit card each time and even contacting unrelated family members",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I trusted the man on the phone because he authenticated everything as Chase normally would.", "speaker": "narrative"},
       {"quote": "He was also able to close out my debit card and get a new XXXX orders.", "speaker": "narrative"}
     ]},
    {"topic_label": "branch allowed $9,300 withdrawal without id",
     "issue_statement": "A branch employee let someone withdraw $9,300.00 in person using only a debit card, without checking identification, and the total fraudulent loss reached $10,000.00.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "branch let an in-person withdrawal of $9,300.00 proceed on debit card alone with no ID check, contributing to a $10,000.00 total loss",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The employee did NOT ask for an ID. This branch allowed this person to withdraw $9300.00 in branch without having shown ID.", "speaker": "narrative"},
       {"quote": "The total amount of loss is $10000.00.", "speaker": "narrative"}
     ]},
    {"topic_label": "claims denied without pulling video evidence",
     "issue_statement": "Chase denied the ATM fraud claims, saying it could not prove the transactions were fraudulent, and did not pull the video evidence it said a police report would allow.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "denied_or_declined_without_explanation",
     "driver": "ATM claims denied for lack of proof despite a filed police report, and Chase never pulled the video evidence it said the report would enable",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase Bank denied mute ATM claims for $910.00 dollars stating they can not prove it was fraudulent", "speaker": "narrative"},
       {"quote": "They denied my ATM claims and did not pull video evidence.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "An impersonator posing as Chase fraud staff manipulated a customer's debit card over two calls, enabling $10,000.00 in fraudulent ATM and in-branch withdrawals, including $9,300.00 taken in branch without an ID check, and Chase denied the claims without pulling the promised video evidence."
}

records["cfpb_21422872"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a $3,000.00 duplicate charge dispute was denied and the temporary credit rebilled, despite the merchant saying it never denied the claim", "is_primary": True}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting review and resolution of a $3,000.00 duplicate charge that was credited during a dispute and then recharged",
  "underlying_driver": "Chase denied the dispute for being outside an allowable timeframe and rebilled the $3,000.00, while the merchant says its own system shows the dispute is still under bank review and expects resolution, leaving the customer out $3,000.00 with conflicting information",
  "reason_differs": False,
  "topics": [
    {"topic_label": "duplicate charge dispute denied and rebilled",
     "issue_statement": "A $3,000.00 duplicate charge was disputed and temporarily credited, but Chase ultimately denied the dispute as outside the allowable timeframe and recharged the $3,000.00 as a rebill, even though the merchant's own system shows the dispute is still under review.",
     "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "dispute denied as untimely and $3,000.00 rebilled, while the merchant's system indicates the dispute is still under bank review with a refund expected, leaving conflicting information between bank and merchant",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Despite this, the dispute was ultimately denied, and the funds were recharged to my account as a rebill on XX/XX/year>, again for $3000.00.", "speaker": "narrative"},
       {"quote": "They informed me that : They did not deny the dispute Their system shows the dispute is still under bank review", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A $3,000.00 duplicate charge was credited during a dispute but ultimately denied and rebilled by Chase as untimely, even though the merchant's own system shows the dispute is still under bank review, leaving the customer out $3,000.00 amid conflicting information."
}

records["cfpb_22643566"] = {
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

records["cfpb_23448374"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "$270.00 disputed transaction with no settlement proof, merchant says it never received payment", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "requesting a full transaction trace and reimbursement of $270.00 since the merchant confirms it never received payment and Chase cannot show settlement proof",
  "underlying_driver": "the merchant canceled the order and confirmed no payment was ever received, but Chase can't provide any settlement record showing where the $270.00 went, despite the customer having repaid the associated financing balance in full",
  "reason_differs": False,
  "topics": [
    {"topic_label": "unresolved $270 transaction with no settlement proof",
     "issue_statement": "The merchant canceled an order and confirmed in writing it never received payment or provided the product, but Chase cannot produce any settlement record showing where the $270.00 charge actually went, despite the customer repaying the linked financing plan in full.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "merchant confirms no payment received while Chase can't provide settlement proof for the $270.00, despite the customer already repaying the associated financing balance",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The merchant later canceled the order after determining I was XXXX  ineligible and has confirmed in writing that no payment was ever received and no product or service was provided.", "speaker": "narrative"},
       {"quote": "Chase has not provided any proof that the merchant received the funds or a settlement record showing where the $270.00 was disbursed.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A merchant confirmed it never received payment or provided goods for a canceled $270.00 order, but Chase cannot produce any settlement proof for where the money went, despite the customer having repaid the linked financing plan in full."
}

records["cfpb_9560165"] = {
  "contact_reasons": [
    {"reason": "terms_information_or_communication", "specific_reason": "misleading balance-transfer check disclosure suggested a fee applied only to balance transfers, and a rep confirmed no fee for the customer's actual use", "is_primary": True}
  ],
  "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "explanation",
  "stated_reason": "pointing out that the promotional check disclosure was misleading about when the transfer fee applies, after being told by customer service there was no fee",
  "underlying_driver": "the promotional offer's wording made the $5.00-or-5%-fee sound tied only to 'balance transfers,' but a Chase rep confirmed no fee would apply to a non-balance-transfer purchase, which the customer says is misleading",
  "reason_differs": False,
  "topics": [
    {"topic_label": "misleading fee disclosure confirmed wrong by customer service",
     "issue_statement": "A promotional check's fee disclosure made it sound like the $5.00-or-5%-fee applied only to 'balance transfers,' and a Chase representative confirmed there would be no fee for using the check for a non-balance-transfer purchase, which the customer says is misleading and has recorded proof of.",
     "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "promotional check disclosure implied the fee applied only to balance transfers, and a Chase rep confirmed on a recorded call that no fee would apply to a non-transfer purchase",
     "outcome": "unknown",
     "evidence": [
       {"quote": "The check page made it appear the fee was for balance transfers.", "speaker": "narrative"},
       {"quote": "I called Chase Credit Card and said I am not doing a balance transfer, it is for a new Heat pump unit, is there a fee for that type of transaction, she said No.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unknown", "positive_moments": [], "redaction_heavy": False,
  "summary": "A promotional balance-transfer check's fee disclosure was worded to suggest the fee only applied to balance transfers, and a Chase representative confirmed on a recorded call that no fee would apply to the customer's non-transfer purchase."
}

records["cfpb_9850436"] = {
  "contact_reasons": [
    {"reason": "dispute_or_chargeback", "specific_reason": "a rental host's fraudulent damage claim charge could not be resolved despite weeks of daily calls to both the platform and Chase", "is_primary": True}
  ],
  "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "stop_or_block",
  "stated_reason": "wants the unauthorized damage charge stopped and the investigation resolved after canceling the card and disputing it as fraud",
  "underlying_driver": "a vacation rental host fabricated damage claims using old, undated evidence, and despite canceling the card and reporting it as fraud, weeks of daily calls to both the rental platform and Chase have produced no resolution",
  "reason_differs": False,
  "topics": [
    {"topic_label": "fraudulent damage charge unresolved after weeks",
     "issue_statement": "A vacation rental host tried to charge for damages using old, undated photos and receipts from years prior, and despite canceling the card and reporting it as fraud, weeks of nearly daily calls to the platform and Chase have produced no resolution.",
     "product": "credit_card", "sentiment": -2, "driver_category": "no_response_or_follow_up",
     "driver": "fraudulent damage claim using undated, years-old evidence remains unresolved after weeks of nearly daily calls to both the rental platform and Chase",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I called Chase right after and canceled my card pleading to take off this charge as it was fraud, I had not authorized anything and the host was committing a crime.", "speaker": "narrative"},
       {"quote": "I have called nearly every day - both XXXX and Chase- for an update and there is none.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A vacation rental host tried to charge for damages using old, undated evidence, and despite canceling the card and reporting it as fraud, weeks of nearly daily calls to both the platform and Chase have produced no resolution."
}

records["cfpb_10198844"] = {
  "contact_reasons": [
    {"reason": "terms_information_or_communication", "specific_reason": "a branch employee submitted a full new credit card application instead of the automatic upgrade the customer expected, resulting in a denial", "is_primary": True}
  ],
  "products": ["credit_card"], "services": ["branch"], "customer_ask": "explanation",
  "stated_reason": "confused and seeking clarity after a branch employee's suggested 'upgrade' turned out to be a new credit card application that was denied",
  "underlying_driver": "the customer expected an automatic upgrade after a year of good standing, but the branch employee instead submitted a new card application without clarifying the distinction, resulting in a denial letter",
  "reason_differs": False,
  "topics": [
    {"topic_label": "branch upgrade suggestion was actually a new application",
     "issue_statement": "A branch employee's suggestion to 'upgrade' the credit card turned out to be a full new-card application rather than the automatic upgrade the customer expected after a year of good standing, and the application was denied.",
     "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "branch employee's ambiguous 'upgrade' offer was actually a new credit card application, not the automatic upgrade expected, resulting in a denial letter",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I had a Chase XXXX XXXX and knew that I would be automatically upgraded to Freedom Unlimited after one year upon staying in a good standing, so I thought he meant it was possible to proceed with the upgrade without waiting for a year.", "speaker": "narrative"},
       {"quote": "the morning of XX/XX/XXXX I received a letter stating that my new application for XXXX XXXX XXXX was denied, and that was when I realized the application he worked on yesterday was the very same thing.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A branch employee's ambiguous credit card 'upgrade' offer turned out to be a full new-card application rather than the automatic upgrade the customer expected, and the application was denied."
}

records["cfpb_10509980"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "settlement check deposits led to account closure and frozen funds over unverifiable phone numbers, with weeks of runaround", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "rude treatment and a promised reopening later reversed", "is_primary": False}
  ],
  "products": ["checking_or_savings"], "services": ["phone_support", "branch"], "customer_ask": "fix_error",
  "stated_reason": "trying to prevent account closure and get access to legal settlement funds by providing verification numbers Chase asked for",
  "underlying_driver": "Chase requires a phone number tied to the deposited settlement checks to verify them, keeps rejecting every number the customer provides, refuses to call the numbers itself, and even after a branch verified the checks with the lawyer, later closed the accounts again",
  "reason_differs": False,
  "topics": [
    {"topic_label": "accounts closed over unverifiable check numbers",
     "issue_statement": "Chase closed the customer's checking and savings accounts and is withholding legal settlement funds because it could not verify the deposited checks, rejecting every phone number the customer provided and refusing to call them.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned",
     "driver": "accounts closed and settlement funds withheld over unverified check numbers, with Chase refusing to call any of the several numbers the customer supplied",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The funds were deposited into my accounts but now Chase is closing my accounts and is refusing to release the funds because they were unable to verify the checks.", "speaker": "narrative"},
       {"quote": "No one from Chase has called these numbers despite them asking me to find them.", "speaker": "narrative"}
     ]},
    {"topic_label": "rude treatment and shifting verification demands",
     "issue_statement": "After a branch verified the checks with the lawyer and said the accounts would be reopened, Chase closed them again and kept asking for new numbers, while a manager was dismissive when the customer cried on the phone.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "staff_attitude_or_competence",
     "driver": "a branch-verified reopening was reversed, with Chase repeatedly asking for new numbers and a manager dismissing the customer's distress",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "One manager told me over the phone crying was not going to help my case.", "speaker": "narrative"},
       {"quote": "they called the other party in the lawsuits lawyer and verified the checks and I was told my accounts would be reopened. However, now my accounts are closed and they are holding on to the funds.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase closed the customer's checking and savings accounts over unverifiable phone numbers tied to deposited legal-settlement checks, refused to call any of several numbers provided, reversed a branch-verified reopening, and a manager was dismissive when the customer cried on the phone."
}

records["cfpb_10926482"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "account closed for suspected identity theft after depositing a legitimate Social Security check, then funds withheld pending Treasury verification", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": [], "customer_ask": "fix_error",
  "stated_reason": "wants the withheld Social Security deposit released after providing the official award letter",
  "underlying_driver": "the account was closed for suspected identity theft, and once identity was confirmed, Chase still withheld the funds pending a Treasury Department verification that is difficult to obtain",
  "reason_differs": False,
  "topics": [
    {"topic_label": "ssa deposit withheld pending treasury verification",
     "issue_statement": "After the bank closed the account for suspected identity theft and confirmed the customer's identity, it continued withholding a legitimate Social Security deposit pending verification from the Treasury Department, despite the customer providing the official award letter.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned",
     "driver": "legitimate SSA deposit withheld pending Treasury Department verification, which is hard to reach, even after the customer's identity was confirmed and an award letter provided",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The bank closed my account for suspected identity theft. Then when my identity was discovered that i was a real person, the bank withheld the funds because the bank needs to verify the amount with the treasury department.", "speaker": "narrative"},
       {"quote": "They will not release the funds to me until they speak to someone in the Treasury Department.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "After closing the account over suspected identity theft and confirming the customer was real, Chase still withholds a legitimate Social Security deposit pending Treasury Department verification, despite the customer providing the official award letter."
}

records["cfpb_11227257"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a wire transfer from a joint account was blocked for refusing to explain the reason, then the account was frozen after the co-owner's death", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "weeks of runaround across branches and departments to close the account, with shifting paperwork demands", "is_primary": False}
  ],
  "products": ["checking_or_savings"], "services": ["branch", "phone_support"], "customer_ask": "fix_error",
  "stated_reason": "trying to access and eventually close a joint account set up for her late mother, whose final expenses she needs to cover",
  "underlying_driver": "Chase blocked a legitimate transfer for refusing to explain its purpose despite full identity verification, then froze the account after her mother's death, and gave conflicting, ever-changing paperwork requirements over weeks that a lawyer estimated would cost nearly half the account's balance to satisfy",
  "reason_differs": False,
  "topics": [
    {"topic_label": "wire transfer denied for refusing to explain reason",
     "issue_statement": "A wire transfer between the customer's own accounts was denied twice after she refused to explain her reason for transferring, even though her identity was verified and a supervisor admitted the funds were available to withdraw in branch.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "denied_or_declined_without_explanation",
     "driver": "wire denied twice for declining to give a 'reason,' with a supervisor citing an arbitrary three-day funds-availability rule never mentioned before, despite admitting the funds were available to withdraw in branch",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Chase blocked my transfer because I wouldn't submit to their interrogation about why i was transferring money.", "speaker": "narrative"},
       {"quote": "the supervisor admitted the funds were showing in my \" available balance '' and if I walked into the branch I would be able to withdraw the funds.", "speaker": "narrative"}
     ]},
    {"topic_label": "account frozen after death with shifting paperwork",
     "issue_statement": "After her mother passed away, Chase froze the joint account and, over multiple branch visits and weeks, kept changing what paperwork was required to close it, discovering along the way that the account had never actually been set up as joint.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "incorrect_or_conflicting_information",
     "driver": "account frozen after the co-owner's death, with the branch admitting the account was set up incorrectly as POA rather than joint, and weeks of shifting, unclear paperwork demands including documents no one could identify",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "the banker told me that the Chase manager who set up the account failed to set it up as a joint account ( that was my request ), and instead set it up as my mother 's account with me having POA access.", "speaker": "narrative"},
       {"quote": "the manager came out to say they couldn't close the account because not all the \" required '' paperwork had been submitted. I asked what was still needed and they basically read a list of the computer. Documents I had never heard of.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase blocked a wire transfer between a customer's own accounts for refusing to explain its purpose, then froze the joint account after her mother's death and, over weeks of branch visits, kept changing the paperwork required to close it, after admitting the account was never properly set up as joint."
}

records["cfpb_11549580"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "$750.00 sent for a cat purchase to scammers, and Chase said it couldn't recover the money or shut down the account", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the $750.00 sent to a fake cat-breeding business recovered",
  "underlying_driver": "after paying a purported cat breeder $750.00 and receiving no response, Chase opened an investigation but ultimately said it could not contact the recipient bank or shut down the account",
  "reason_differs": False,
  "topics": [
    {"topic_label": "cat purchase scam payment unrecoverable",
     "issue_statement": "A $750.00 payment sent to a purported cat-breeding business that never responded again could not be recovered, with Chase saying it could not contact the recipient's bank or shut down the account.",
     "product": "money_transfer_or_p2p", "sentiment": -1, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "$750.00 sent to a scam cat seller could not be recovered; Chase said it couldn't contact the recipient bank or close the scamming account",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "they finally told me they couldnt do anything about getting my money back.", "speaker": "narrative"},
       {"quote": "They couldnt contact the bank or shut down the account that scammed me.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A $750.00 payment to a fake cat-breeding business could not be recovered, with Chase saying it could not contact the recipient's bank or shut down the scamming account."
}

records["cfpb_12138688"] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "account closed for alleged 'abuse of the claims process' with no evidence or opportunity to respond", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["phone_support"], "customer_ask": "explanation",
  "stated_reason": "wants a clear, evidence-based explanation for why the account was closed after being accused of abusing the claims process",
  "underlying_driver": "Chase closed the long-standing account, calling it claims-process abuse with no evidence given, then told the customer repeatedly it doesn't have to explain closures, contradicting its own stated accusation, and the closure cascaded into missed payments, late fees, and lapsed insurance",
  "reason_differs": False,
  "topics": [
    {"topic_label": "account closed over unproven abuse accusation",
     "issue_statement": "Chase closed a long-standing account, accusing the customer of abusing the claims process with no evidence given or chance to respond, then repeatedly said it doesn't have to provide any reason for closing an account.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "denied_or_declined_without_explanation",
     "driver": "account closed over an unproven 'abuse of claims process' accusation with no evidence, while Chase also insists it owes no explanation, a contradiction the customer highlights",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The letter states that I \" abused the claims process. ''", "speaker": "narrative"},
       {"quote": "I was told repeatedly that Chase does not have to give a reason for closing the account and that I should have been aware of this when I opened my account.", "speaker": "narrative"}
     ]},
    {"topic_label": "closure cascaded into missed payments",
     "issue_statement": "The account closure blocked access to payroll checks for weeks, causing life insurance to lapse, late rent and creditor payments, and disrupted autopay across student loans and credit cards.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned",
     "driver": "weeks without access to payroll checks after closure caused lapsed life insurance, late rent, late creditor payments, and disrupted autopay across multiple accounts",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "No access to my payroll checks for weeks and inability to pay creditors on time", "speaker": "narrative"},
       {"quote": "My life insurance policies lapsed", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase closed a long-standing account over an unproven 'abuse of claims process' accusation with no evidence given, and the closure cascaded into weeks without payroll access, lapsed life insurance, late payments, and disrupted autopay."
}

records["cfpb_12531400"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "two deposited checks were held over 5 days, and after release the account became restricted, blocking debit card and ATM use", "is_primary": True},
    {"reason": "customer_service_experience", "specific_reason": "a customer service representative was rude and made derogatory comments", "is_primary": False}
  ],
  "products": ["checking_or_savings"], "services": ["phone_support", "atm"], "customer_ask": "fix_error",
  "stated_reason": "wants the account restriction lifted so she can use her debit card and withdraw money after a check hold",
  "underlying_driver": "after two check deposits were held over 5 days, the account then became restricted upon release, blocking debit card and ATM access, and a customer service rep was rude when the customer tried to ask a question",
  "reason_differs": False,
  "topics": [
    {"topic_label": "account restricted after check hold released",
     "issue_statement": "After two checks were held for over 5 days, once the funds were released the account became restricted, blocking use of the debit card and ATM withdrawals.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned",
     "driver": "account restricted right after a 5+ day check hold was released, blocking debit card and ATM access",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "They held my money for over 5 days so I was not able to pay bills and such.", "speaker": "narrative"},
       {"quote": "Now that they have released my funds into my account now my account became restricted so I am unable to use my debt card or withdraw money from the ATM.", "speaker": "narrative"}
     ]},
    {"topic_label": "rude customer service representative",
     "issue_statement": "A customer service representative accused the customer of not listening and made derogatory comments while she tried to ask a question.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "staff_attitude_or_competence",
     "driver": "representative accused her of not listening and made derogatory comments during the call",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I called customer service and was accused of not listening when I wanted to ask a question by a gentleman name XXXX and treated like trash.", "speaker": "narrative"},
       {"quote": "He was rude and nasty and said some derogatory comments.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "After a 5+ day hold on two check deposits, the account became restricted right after the funds released, blocking debit card and ATM access, and a customer service representative was rude and made derogatory comments."
}

records["cfpb_13044955"] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "a 100% cash-back offer for an app subscription did not activate even though the purchase was made by following Chase's own link and linked payment method", "is_primary": True}
  ],
  "products": ["credit_card"], "services": ["mobile_app"], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the promised 100% cash-back reimbursement for an app subscription purchased by following Chase's own promotional link",
  "underlying_driver": "Chase's offer directed the customer through a link to a third-party app to complete the purchase using a payment method linked to the Chase card, but then refused to honor the offer because the purchase wasn't made directly with the Chase card, a distinction Chase's own reps say confuses other customers too",
  "reason_differs": False,
  "topics": [
    {"topic_label": "cash-back offer denied despite following chase's own link",
     "issue_statement": "A 100% cash-back offer for a $69.00 app subscription did not activate even though the purchase was made by following a link provided within the Chase app and using a payment method directly linked to the Chase credit card.",
     "product": "credit_card", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "cash-back offer denied because the purchase went through a linked payment method via a Chase-provided link rather than directly on the Chase card, a distinction Chase itself admits has confused other customers",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The Chase offer, which should automatically apply to the purchase and reimburse 100 % of the purchase, did not activate.", "speaker": "narrative"},
       {"quote": "A Chase customer service representative informed me he had spoken to another customer who had this same issue, so clearly customers are confused as to why a link from the Chase application to the XXXX application, and then use of XXXX XXXX linked to the Chase credit card is not triggering the refund.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "A 100% cash-back offer for a $69.00 app subscription failed to activate even though the purchase was made through Chase's own promotional link using a payment method linked to the Chase card, a confusing setup Chase itself admits has tripped up other customers."
}

records["cfpb_13582225"] = {
  "contact_reasons": [
    {"reason": "account_opening_or_closure", "specific_reason": "a newly opened checking and savings account was restricted based on a system discrepancy about how it was opened, unresolved after two branch visits", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["branch", "phone_support"], "customer_ask": "fix_error",
  "stated_reason": "trying to get a newly opened account unrestricted after Chase's system disputed how and when it was opened",
  "underlying_driver": "the account was opened in person via a barcode scan process the customer wasn't told counted as 'online' opening, and Chase's system flagged a discrepancy, restricting the account with escalations that went nowhere for an elderly customer who depends on others for transportation",
  "reason_differs": False,
  "topics": [
    {"topic_label": "new account restricted over opening-method discrepancy",
     "issue_statement": "A checking and savings account opened in person, using a barcode scan process the customer wasn't told counted as an online opening, was restricted days later because Chase's system showed a different opening method, and two branch visits have not resolved it.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "account restricted because the system recorded the in-branch barcode-scan opening as an online opening, and escalation to a 'higher level officer' produced no follow-up call",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "they asked me how did you opened your account in XXXX or XXXX i said in XXXX, but they said no system shows something different, you have to visit the branch with ID, so some one can help you.", "speaker": "narrative"},
       {"quote": "i can not do anything since i have to talk to my higher level officer to do it will be solved on Monday.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "the branch representative who helped remembered the customer and tried to sort out the confusion with customer care", "category": "helpful_staff",
     "quote": "she sad i remember you.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A newly opened checking and savings account was restricted because Chase's system disputed how it was opened, and two branch visits and an escalation promise produced no resolution for an elderly customer who depends on others for transportation."
}

records["cfpb_14089178"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "accounts closed for suspected fraud with no explanation required, and a promised refund check for over $10,000.00 was never received", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
  "stated_reason": "demanding immediate return of over $10,000.00 promised after accounts were closed for suspected fraud",
  "underlying_driver": "a Chase fraud department rep closed both accounts over suspected fraud with no obligation to explain, promised a refund check for the balances, but weeks later the accounts are deleted from the app and no money has arrived",
  "reason_differs": False,
  "topics": [
    {"topic_label": "promised refund never received after fraud closure",
     "issue_statement": "After a Chase fraud department representative closed both accounts over suspected fraud and said no explanation was required, a promised refund check for the balances, totaling over $10,000.00, has not arrived weeks later.",
     "product": "checking_or_savings", "sentiment": -2, "driver_category": "money_held_or_not_returned",
     "driver": "over $10,000.00 promised via refund check after a fraud-based account closure has not arrived weeks later, with both accounts deleted from the app",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "I was told that a check would be refunded to me with the balance on both accounts. I have yet to receive my money on either account and both accounts have been deleted from the app.", "speaker": "narrative"},
       {"quote": "It has been over XXXX weeks since my account has been blocked or closed and CHASE BANK still has possession of all my money.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase closed two accounts over suspected fraud with no explanation required and promised a refund check for balances exceeding $10,000.00, but weeks later no money has arrived and the accounts are deleted from the app."
}

records["cfpb_14684835"] = {
  "contact_reasons": [
    {"reason": "funds_hold_or_account_restriction", "specific_reason": "a $1,400.00 mobile check deposit was held 10 days and the account remains restricted afterward despite repeated identity verification", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["mobile_app", "phone_support"], "customer_ask": "fix_error",
  "stated_reason": "wants the account restriction lifted after a 10-day hold on a $1,400.00 mobile deposit",
  "underlying_driver": "even after the 10-day hold on the deposited check ended, Chase restricted the account and continues to require repeated identity verification and justification for the deposit without lifting the restriction",
  "reason_differs": False,
  "topics": [
    {"topic_label": "account still restricted after check hold ended",
     "issue_statement": "After a 10-day hold on a $1,400.00 mobile check deposit from the customer's grandmother, Chase restricted the account, blocking withdrawals, deposits, purchases, and transfers, and repeated identity verification has not lifted it.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "money_held_or_not_returned",
     "driver": "account restricted after a 10-day mobile deposit hold, with repeated identity verification and explanation of the deposit failing to lift the restriction",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "the originally held it for 10 days. After that hold they restricted my account and now I cant make withdrawals, deposits, purchases, or transfers.", "speaker": "narrative"},
       {"quote": "Every time I call them to remove the restriction I have to provide information on why the check was deposited, verifying my identity, and even with that information still my account and funds are restricted.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "After a 10-day hold on a $1,400.00 mobile check deposit from a grandmother, Chase restricted the account entirely, and repeated identity verification calls have not lifted the restriction."
}

records["cfpb_15339652"] = {
  "contact_reasons": [
    {"reason": "unauthorized_or_fraud", "specific_reason": "victim of romance-based crypto investment scams that drained roughly $400,000.00 wired and transferred from a Chase account", "is_primary": True}
  ],
  "products": ["money_transfer_or_p2p"], "services": [], "customer_ask": "other",
  "stated_reason": "reporting a pattern of romance-based crypto investment scams that drained hundreds of thousands of dollars funneled from his Chase account",
  "underlying_driver": "romance scammers convinced the customer to wire and transfer large sums to crypto exchanges under escalating fake penalty and verification fees, though Chase did flag some wire recipients as scammers and refuse those specific wires",
  "reason_differs": False,
  "topics": [
    {"topic_label": "romance-based crypto scam drained hundreds of thousands",
     "issue_statement": "Romance scammers convinced the customer to wire and fund crypto exchange accounts with escalating fake penalty and verification fees, ultimately losing roughly $400,000.00 that was funneled starting from his Chase account.",
     "product": "money_transfer_or_p2p", "sentiment": -2, "driver_category": "fraud_not_stopped_or_not_refunded",
     "driver": "romance-scam crypto investment fraud drained roughly $400,000.00 funneled from wires and crypto purchases originating at Chase, through escalating fake penalty fees",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "The largest loss was to XXXX for about $400000.00.", "speaker": "narrative"},
       {"quote": "The thing they all have in common is that I was required to wire money from my bank account at JPMorgan Chase, to a handful of crypto exchanges as the first step.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved",
  "positive_moments": [
    {"what": "Chase flagged two wire recipients as scammers and refused to process those wires", "category": "other",
     "quote": "Both individuals and their respective banks were flagged by Chase as scammers and Chase would not sent XXXX wires.", "speaker": "narrative"}
  ],
  "redaction_heavy": False,
  "summary": "A romance-based crypto investment scam drained roughly $400,000.00 funneled through wires and crypto purchases originating from a Chase account via escalating fake penalty and verification fees, though Chase did flag and block wires to two identified scam recipients."
}

records["cfpb_15992004"] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "over 5 years of rewards points, worth over $5,000.00, forfeited when Chase closed the accounts for having other banks' accounts despite zero missed payments", "is_primary": True}
  ],
  "products": ["credit_card"], "services": [], "customer_ask": "refund_or_reversal",
  "stated_reason": "wants the rewards points, or their cash value, restored after the accounts were closed for opening accounts at other banks",
  "underlying_driver": "Chase closed the accounts, citing the customer having accounts at other banks despite no missed payments, forfeiting years of accumulated rewards points worth over $5,000.00, using the same generic reasoning as a prior case",
  "reason_differs": False,
  "topics": [
    {"topic_label": "rewards points forfeited after closure",
     "issue_statement": "Chase closed accounts and forfeited over 5 years of accumulated rewards points, worth more than $5,000.00 if redeemed for cash, citing the customer opening accounts at other banks despite zero missed payments.",
     "product": "credit_card", "sentiment": -2, "driver_category": "money_held_or_not_returned",
     "driver": "over $5,000.00 in rewards points forfeited when accounts were closed over holding accounts at other banks, despite a perfect payment history, using generic reasoning repeated from a prior case",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "And closed my accounts due to me opening other accounts at other banks. I missed zero payments so they have no real valid reason to close my account and steal north of XXXX points I earned over 5 years.", "speaker": "narrative"},
       {"quote": "This is north of $5000.00 if I redeemed for cash", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -2, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase closed accounts and forfeited over five years of rewards points worth more than $5,000.00, citing the customer's accounts at other banks despite a perfect payment history."
}

records["cfpb_16724878"] = {
  "contact_reasons": [
    {"reason": "balance_or_statement_error", "specific_reason": "transactions post out of sequence or delayed, repeatedly causing unexpected negative balances despite transferring funds ahead of purchases", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": [], "customer_ask": "fix_error",
  "stated_reason": "wants the recurring unexpected negative balances and overdraft-related activity fixed despite responsibly transferring funds before purchases",
  "underlying_driver": "even with overdraft protection off and funds transferred between accounts ahead of purchases, transactions periodically post out of sequence or after delays, triggering negative balances and overdraft fees at multiple banks including previously at Chase",
  "reason_differs": False,
  "topics": [
    {"topic_label": "transactions posting out of sequence cause negative balances",
     "issue_statement": "Even with overdraft protection turned off and funds transferred between accounts ahead of purchases, transactions periodically post out of sequence or after delays, triggering unexpected negative balances and overdraft fees, a pattern experienced at multiple banks including previously at Chase.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "system_or_app_failure",
     "driver": "transactions post out of sequence or after delays despite funds being transferred ahead of purchases and overdraft protection being off, causing repeated negative balances and fees at multiple banks",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "then without warning, transactions begin posting out of sequence or after delays, and my account suddenly goes negative or shows insufficient funds.", "speaker": "narrative"},
       {"quote": "I have overdraft protection turned off, yet I still see negative balances and occasional overdraft-related activity.", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Despite transferring funds between accounts ahead of purchases and having overdraft protection off, transactions periodically post out of sequence or after delays, triggering unexpected negative balances and fees, a pattern the customer has seen at multiple banks including previously at Chase."
}

records["cfpb_17300118"] = {
  "contact_reasons": [
    {"reason": "rewards_or_promotions", "specific_reason": "a $300.00 new-account bonus is being denied because Chase doesn't count the employer's ACH wage deposits as 'direct deposit'", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": ["phone_support"], "customer_ask": "explanation",
  "stated_reason": "disputing Chase's refusal to count confirmed employer ACH wage payments as qualifying direct deposits for a $300.00 bonus",
  "underlying_driver": "Chase's customer service said the two ACH payroll deposits didn't count as 'direct deposit' and instead called them bank transactions, even though the employer confirmed the wages were paid via ACH direct deposit",
  "reason_differs": False,
  "topics": [
    {"topic_label": "ach payroll deposits not counted as direct deposit",
     "issue_statement": "Chase told the customer his two ACH payroll deposits of $340.00 and $170.00 don't count as 'direct deposit' toward a $300.00 new-account bonus, even though his employer confirmed the wages were paid via ACH direct deposit.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "incorrect_or_conflicting_information",
     "driver": "$300.00 bonus denied because Chase treats confirmed ACH payroll deposits as ordinary bank transactions rather than qualifying direct deposits",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "during the conversation the chase customer service person told me she does not agree my XXXX direct deposit on XXXX and XX/XX/year>, she treat them as bank transaction.", "speaker": "narrative"},
       {"quote": "my employer said they paid my wages through ACH from their bank, so it is directly deposit", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Chase is denying a $300.00 new-account bonus by treating the customer's confirmed employer ACH payroll deposits as ordinary bank transactions rather than qualifying direct deposits."
}

records["cfpb_18282201"] = {
  "contact_reasons": [
    {"reason": "fees_and_charges", "specific_reason": "overdraft fees charged even after resolving the negative balance by deposit, due to a same-day ACH payment reposting the account negative", "is_primary": True}
  ],
  "products": ["checking_or_savings"], "services": [], "customer_ask": "explanation",
  "stated_reason": "disputing overdraft fees charged on transactions that were already resolved by a deposit, blamed on other same-day ACH payments",
  "underlying_driver": "Chase's Overdraft Assist policy charges a fee if the account goes negative again by the next business day, even when the customer already made the account positive with a deposit, because other same-day ACH payments posted afterward and were never publicly disclosed as a trigger",
  "reason_differs": False,
  "topics": [
    {"topic_label": "overdraft fees despite resolving balance same day",
     "issue_statement": "Even after a deposit resolved an overdraft, Chase charged fees because other same-day ACH payments posted afterward and put the account negative again the next business day, a rule not disclosed to the public.",
     "product": "checking_or_savings", "sentiment": -1, "driver_category": "unexpected_charge",
     "driver": "$34.00 overdraft fees charged despite resolving the negative balance with a deposit, because other same-day ACH payments reposted the account negative under an undisclosed rule",
     "outcome": "unresolved",
     "evidence": [
       {"quote": "Im charged for transactions that did get resolved after a deposit was made.", "speaker": "narrative"},
       {"quote": "Chase has now started assessing fees without notification to the public that if account is overdrawn again the following business date even though you made a deposit and had the account positive you will get charged", "speaker": "narrative"}
     ]}
  ],
  "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
  "summary": "Even after a deposit resolved an overdraft, Chase charged additional fees because other same-day ACH payments put the account negative again the next business day, under an undisclosed policy."
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
