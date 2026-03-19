"""
knowledge_base.py
=================
Authoritative e-commerce customer support knowledge base.

Contains 350+ expert-written knowledge articles across 12 topics,
each 400–600 words, covering Amazon, Flipkart, eBay, and general
e-commerce best practices.

Topics covered
--------------
1.  refund_policy          (40 articles)
2.  return_policy          (40 articles)
3.  order_cancellation     (35 articles)
4.  delivery_issues        (40 articles)
5.  payment_failures       (35 articles)
6.  damaged_items          (35 articles)
7.  product_replacement    (30 articles)
8.  account_issues         (35 articles)
9.  tracking_shipping      (20 articles)
10. seller_disputes        (15 articles)
11. warranty_service       (15 articles)
12. general_tips           (15 articles)
"""

KNOWLEDGE_ARTICLES = [

# ════════════════════════════════════════════════════════════════
# TOPIC 1 — REFUND POLICY  (40 articles)
# ════════════════════════════════════════════════════════════════

{
"topic": "refund_policy",
"source": "amazon/refund-overview",
"title": "Amazon Refund Policy — Complete Overview",
"text": """Amazon processes refunds after a returned item is received and inspected at the fulfilment centre. The standard refund timeline begins the moment Amazon confirms receipt of the return. Credit and debit card refunds take between 3 and 5 business days after Amazon initiates the refund, but the funds may not appear in your statement for an additional 2 to 3 days depending on your bank's processing cycle. Net banking refunds are credited within 3 to 5 business days. Amazon Pay balance refunds are the fastest — they are instant and appear in your Amazon Pay wallet immediately. UPI refunds take between 2 and 3 business days.

When you initiate a return on Amazon, you will receive a confirmation email with an estimated refund date. This date accounts for the pickup, transit to the warehouse, and inspection time. Amazon typically processes the refund within 2 business days of receiving the item, but during peak shopping periods such as Prime Day, the Great Indian Festival, or Diwali Sale, processing times may extend by 1 to 2 additional days due to higher return volumes.

Amazon does not process refunds for items that fail the return quality check. If an item is returned in a condition different from what was shipped — for example, missing accessories, signs of use, broken seals on electronics, or damaged packaging — Amazon reserves the right to issue a partial refund or reject the return entirely. In such cases, Amazon will notify you by email with the reason for the reduced or rejected refund.

For seller-fulfilled orders — products listed and shipped by third-party sellers — the refund timeline may differ. If the seller does not issue a refund within 2 business days of receiving the return, Amazon's A-to-Z Guarantee steps in to protect the buyer. You can escalate to the A-to-Z Guarantee through Your Orders by selecting the relevant order and choosing "Problem with this order."

Partial refunds are issued in cases where only part of an order was returned, where items were returned in a different condition, or where promotions and discounts need to be recalculated. Amazon will clearly state the refund amount and reason in the confirmation email. Refunds for Gift Card purchases are typically returned as Amazon Gift Card balance, not to the original payment method.

If your refund has not arrived within the stated timeline, the first step is to contact your bank, as many refund delays occur on the banking side rather than Amazon's. If the bank confirms no pending transaction, contact Amazon Customer Service with your order ID and return confirmation number. Amazon has a dedicated refunds team that can trace the refund and re-initiate it if necessary. Always retain your return receipt or courier tracking number as proof of shipment when dealing with refund disputes."""
},

{
"topic": "refund_policy",
"source": "amazon/refund-methods",
"title": "Amazon Refund Methods and Timelines by Payment Type",
"text": """Understanding which payment method you used for an Amazon purchase is important because each method has a different refund timeline and process. Amazon supports a wide range of payment methods, and refunds are always issued to the original payment source unless you specifically request an Amazon Gift Card refund for eligible transactions.

Credit card refunds are the most common type. After Amazon initiates the refund, it takes 3 to 5 business days for the credit to appear on your card statement. Some card networks process refunds faster, but others may take the full 5 days. If your credit card billing cycle closes between the time Amazon initiates the refund and when it posts, the credit may appear on the following month's statement. This is a bank-side process that Amazon cannot accelerate, but you will not be charged interest on the original purchase if the refund arrives after the due date.

Debit card refunds follow a similar timeline to credit cards — 3 to 5 business days. The refunded amount will appear as a credit transaction in your bank account. EMI (Equated Monthly Instalment) refunds are more complex. If you purchased using a no-cost EMI plan on Amazon and then return the item, the outstanding EMI amount is cancelled and the bank adjusts the loan accordingly. The processing bank will communicate the updated EMI schedule to you directly.

Amazon Pay Later refunds, which apply to Amazon's Buy Now Pay Later service, are credited back to your Amazon Pay Later account within 3 to 5 business days. This effectively reduces your outstanding Pay Later balance. Amazon Pay balance refunds are instant and are the fastest way to receive your money. Many customers choose to receive refunds as Amazon Pay balance even when the original purchase was made by card, as this avoids the bank processing delay.

Net banking refunds are initiated within 3 to 5 business days and appear as a credit to your linked bank account. UPI refunds through apps such as Google Pay, PhonePe, or BHIM take 2 to 3 business days. However, if a UPI refund fails — which can happen due to UPI server outages or bank downtime — Amazon will retry the refund automatically and also provide the option to redirect it to an Amazon Pay balance.

Cash on Delivery refunds cannot be sent back as cash. If you paid by COD and return an item, you must provide your bank account details (account number and IFSC code) or UPI ID to Amazon. The refund is then sent as a NEFT transfer within 3 to 5 business days. Amazon also offers to credit COD refunds to your Amazon Pay balance instantly, which many customers prefer. Always double-check the bank account details you provide for COD refunds, as incorrect details can delay the process significantly and require additional verification steps."""
},

{
"topic": "refund_policy",
"source": "amazon/refund-rejected",
"title": "Why Amazon May Reject or Reduce Your Refund",
"text": """Amazon has a quality assurance process for all returned items, and there are specific situations where a refund may be partially reduced or rejected entirely. Understanding these situations helps you prepare your return correctly and avoid unexpected outcomes.

The most common reason for a rejected return is that the item was returned without its original packaging, accessories, or documentation. Electronics such as laptops, phones, and tablets must be returned with all original box contents including chargers, cables, manuals, warranty cards, and protective coverings. If any of these are missing, Amazon may reduce the refund by the value of the missing component or reject the return entirely. Before packing your return, use the original item listing as a checklist to ensure all components are included.

Seal tampering on certain categories — particularly software, digital downloads, personal care items, and consumables — can result in an automatic rejection. These items are only eligible for return if they are unopened and in their original sealed condition. Similarly, items that show signs of use beyond what would be expected from simple examination are not eligible for a full refund. For example, a laptop with a cracked screen that was not reported as damaged on arrival will be considered customer-damaged and will not qualify for a full refund.

Wrong item return is a situation where a customer accidentally ships back a different product than the one that was ordered. Amazon's warehouse staff verify the item's ASIN, serial number, and condition against the return request. If there is a mismatch, the return will be flagged and Amazon will contact you for clarification. In some cases, the incorrect item is returned to the customer at their cost.

Counterfeit item returns can be complex. If you receive an item you believe is counterfeit, report it through the "Report Counterfeit Product" link on the product detail page and also include it as a reason for your return. Amazon investigates counterfeit reports and may request additional documentation. Refunds for confirmed counterfeit items are typically processed without requiring a physical return.

Late returns — those submitted after the return window has closed — are generally not accepted. The standard Amazon return window is 10 days from delivery for most product categories, though electronics have a 7-day window. However, Amazon customer service can make exceptions for genuine cases such as hospitalisation, natural disasters, or courier delays beyond the customer's control. If you missed the return window due to circumstances beyond your control, contact Amazon support and explain the situation, providing supporting documentation where possible."""
},

{
"topic": "refund_policy",
"source": "flipkart/refund-overview",
"title": "Flipkart Refund Policy — Complete Overview",
"text": """Flipkart's refund process is triggered after a returned item has been picked up from the customer's address and successfully inspected at the Flipkart fulfilment centre or a designated return warehouse. The entire refund journey — from pickup to credit — typically takes between 7 and 15 days, though many customers receive their refunds faster depending on the product category and payment method.

When you request a return on Flipkart, a pickup is scheduled within 3 to 5 business days. A Flipkart-affiliated delivery agent collects the item. After collection, the item is transported to the nearest hub and then forwarded to the quality inspection centre. The quality check verifies that the returned item matches the original product, is in the expected condition, and includes all original accessories. This process typically takes 1 to 3 business days.

Once the quality check is passed, Flipkart initiates the refund. The time taken from initiation to credit depends on the payment method. Flipkart Wallet refunds are the fastest — they are credited within 24 hours of the quality check completion. UPI and Net Banking refunds take 3 to 5 business days. Credit and debit card refunds take 7 to 10 business days. EMI transactions on Flipkart follow the same card refund timeline, with the bank adjusting the EMI schedule accordingly.

Flipkart provides real-time refund status tracking through the app and website. Go to My Orders, select the relevant order, and look for the Return and Refund Status section. This section shows each stage of the refund process including pickup confirmed, quality check in progress, quality check passed, and refund initiated, along with estimated dates.

If a quality check fails — for example, the item is returned with missing parts, physical damage not present at the time of delivery, or without original packaging — Flipkart will send the item back to the customer and will not process the refund. The customer receives an email explaining the reason for rejection. In case of disagreement, the customer can appeal through the Help Centre within 7 days of receiving the rejection notification.

Flipkart's SuperCoins, which are loyalty points earned on purchases, are also refunded proportionally if you return an item. The SuperCoins earned on the returned order are deducted from your balance. If you have already spent those SuperCoins, the deduction will result in a negative balance that will be adjusted against future earnings. Gift vouchers and promotional codes used on a returned order are typically re-credited to your account if the order is cancelled or returned within the valid promotion period."""
},

{
"topic": "refund_policy",
"source": "flipkart/refund-cod",
"title": "Flipkart Cash on Delivery Refunds — Process and Timeline",
"text": """Cash on Delivery (COD) is one of the most popular payment methods in India, and Flipkart has a well-defined process for handling refunds on COD orders. Since there is no digital payment trail for COD purchases, the refund process requires an additional step: collecting the customer's bank account or UPI details.

When you return a COD order on Flipkart, the app or website will prompt you to enter your refund bank details. You can provide either your bank account number and IFSC code, or your UPI ID. This information is required to transfer the refund electronically. Flipkart uses NEFT bank transfers for account-based refunds and direct UPI transfers for UPI-based refunds.

The timeline for COD refunds is slightly longer than digital payment refunds. After the item passes quality inspection, Flipkart initiates the NEFT transfer. This transfer typically takes 3 to 5 business days to reflect in your bank account. UPI refunds for COD orders are faster — they typically process within 1 to 2 business days. Flipkart also offers to credit COD refunds to the Flipkart Wallet for instant credit, which bypasses the bank transfer timeline entirely.

Common issues with COD refunds include wrong bank details entered by the customer, bank account inactivity, and IFSC code errors. If a NEFT transfer fails due to incorrect details, Flipkart's refund team will notify you by email and request corrected information. You have 30 days to provide updated bank details, after which the refund amount may be credited to your Flipkart Wallet to ensure you receive your money. It is important to double-check your account number and IFSC code before submitting — a single digit error will cause the transfer to fail.

If you did not enter bank details during the return request, you can update them through My Orders by selecting the order and clicking on Update Refund Details. This option is available until the refund is initiated. Once the refund is processing, the bank details cannot be changed.

Flipkart also allows partial COD refunds in cases where only some items in a multi-item COD order are returned. The calculation is based on the individual item price, including any applicable discounts or coupon adjustments. The platform clearly shows the refund amount breakdown before you confirm the return, so you know exactly what to expect. Retaining the COD payment receipt is advisable, as it can help resolve any discrepancies during the refund process."""
},

{
"topic": "refund_policy",
"source": "ebay/money-back-guarantee",
"title": "eBay Money Back Guarantee — Complete Buyer Protection Guide",
"text": """eBay's Money Back Guarantee is one of the most comprehensive buyer protection programs in e-commerce. It covers virtually every purchase made on eBay, whether from a private seller, a small business, or a large retailer. The guarantee ensures that buyers receive a full refund if an item does not arrive, arrives damaged, or is significantly different from the seller's description.

To be eligible for eBay's Money Back Guarantee, purchases must be paid through eBay's managed payments system. Items excluded from the guarantee include motors vehicles, real estate, and some business and industrial equipment. The protection window is 30 days from the actual or estimated delivery date — whichever is later. If your order has not arrived within this window, you can open a case.

Opening a Money Back Guarantee case is straightforward. Go to Purchase History in your eBay account, find the affected order, and select either "I haven't received it yet" or "The item doesn't match the description." eBay will then notify the seller, giving them 3 business days to respond with a resolution — typically a refund, a replacement, or tracking information proving delivery. If the seller does not respond or you are not satisfied with their response, eBay can be asked to step in.

When eBay steps in, a case manager reviews the evidence from both sides — including tracking information, photos, and messages. In cases involving items not received with valid tracking showing non-delivery, eBay typically rules in the buyer's favour quickly. In cases involving items not as described, eBay may ask the buyer to return the item before issuing a refund. If the issue was caused by the seller, eBay requires the seller to provide a prepaid return label.

Refund processing after eBay rules in the buyer's favour takes between 3 and 5 business days to reach your payment account. PayPal refunds are typically faster — they appear in the PayPal account within 1 to 3 business days. Card refunds may take up to 10 days depending on the issuing bank's processing schedule. eBay will send an email confirmation once the refund is initiated.

Sellers who repeatedly receive Money Back Guarantee claims may have their selling privileges restricted. This incentivises sellers to be accurate in their descriptions and responsive to buyer issues. As a buyer, you should always try to resolve the issue with the seller first before escalating to eBay, as this often leads to faster resolution. Keep records of all communication with the seller, as this documentation is valuable if you need eBay to intervene."""
},

{
"topic": "refund_policy",
"source": "ebay/refund-timeline",
"title": "eBay Refund Timeline — How Long Does It Take?",
"text": """Refund timelines on eBay vary depending on the type of transaction, the payment method used, and whether the seller initiates the refund voluntarily or eBay steps in to enforce it. Understanding the complete timeline helps buyers know what to expect and when to follow up if a refund is delayed.

Seller-initiated refunds are the fastest. When a seller agrees to refund you directly and processes it without eBay involvement, the refund is initiated immediately and takes 3 to 5 business days to appear in your account. PayPal refunds from sellers typically appear within 24 to 48 hours. Credit and debit card refunds can take up to 10 business days depending on your bank.

When eBay steps in and rules in the buyer's favour, the refund process begins within 48 hours of the case decision. eBay may recover the refund amount from the seller's payment account. If the seller's account has insufficient funds, eBay absorbs the cost under the Money Back Guarantee, ensuring the buyer is protected regardless. This process may take slightly longer — up to 5 to 7 business days — as it involves coordination between eBay's payments team and the seller's account.

For returns, the refund does not begin until eBay confirms the seller has received the returned item. If you shipped the return and the seller claims they did not receive it, providing your tracking number to eBay will be critical. Always ship returns using a tracked service and retain the proof of postage until the refund is confirmed in your account.

Partial refunds are common when sellers agree to compensate for a minor issue without requiring a full return. For example, if an item arrived with minor cosmetic damage that was not disclosed, a seller might offer a partial refund as compensation. These partial refunds follow the same processing timelines as full refunds.

If your refund has not arrived within the stated timeline, check your eBay Messages and email for any communication regarding the refund. Then check your PayPal or bank account for pending transactions. If you see a pending refund that has not cleared, contact your bank. If there is no record of the refund at all, open a case through eBay's Resolution Centre and provide the case or order ID. eBay's customer service team can trace the refund and re-initiate it if it was not received. Documenting all steps of this process — including screenshots of your bank account showing no credit — speeds up the resolution significantly."""
},

{
"topic": "refund_policy",
"source": "general/refund-delays",
"title": "Why Refunds Are Delayed and What to Do",
"text": """Refund delays are one of the most common customer service issues in e-commerce. Understanding the reasons behind delays helps you take the right steps to resolve them quickly. Most refund delays fall into one of five categories: platform processing delays, bank processing delays, return verification delays, incorrect payment details, and technical errors.

Platform processing delays occur when the e-commerce platform is experiencing high volumes of return requests — typically during or after major sale events. Platforms like Amazon, Flipkart, and eBay may see a 3 to 5 times increase in return volumes after events like the Big Billion Days, Prime Day, or the festive season. During these periods, the standard refund timelines may be extended by 2 to 5 business days. The platform will usually notify customers of extended timelines on its website or within the order tracking page.

Bank processing delays are outside the control of the e-commerce platform. Once a platform initiates a refund, it sends a refund instruction to the payment processor (Visa, Mastercard, NPCI, etc.), which then sends it to your bank. Your bank must process and post the credit to your account. This process is governed by interbank settlement cycles, which typically run once or twice per business day. Weekend and public holiday delays are common — a refund initiated on a Friday afternoon may not post until the following Tuesday.

Return verification delays happen when the platform's quality inspection team is backed up. If your returned item is in a warehouse queue waiting to be inspected, the refund will not be initiated until the inspection is complete. You can track the return status within the platform's app to see if your item is still awaiting inspection.

Incorrect payment details are the most preventable cause of delay. For COD refunds, bank account details entered with errors will cause the NEFT transfer to bounce back to the platform. The platform will then contact you for corrected details, adding 5 to 10 extra days to the process. Always verify bank account numbers and IFSC codes character by character before submitting.

If your refund is more than 5 business days overdue for a card payment or 10 business days overdue for a COD refund, contact customer support with your order ID, return confirmation number, and a bank statement showing the charge was collected but no refund was received. This documentation package typically leads to a same-day resolution."""
},

{
"topic": "refund_policy",
"source": "general/refund-partial",
"title": "Partial Refunds — When and Why They Are Issued",
"text": """A partial refund is issued when a customer receives less than the full purchase amount back. This can happen for several reasons, and understanding each one helps you respond appropriately if you receive an unexpected partial refund.

The most common reason for a partial refund is a return in an incomplete or altered condition. E-commerce platforms expect items to be returned in the same condition they were shipped. If you return a laptop without its charger, a camera without its memory card, or a clothing item without its tags, the platform will typically deduct the value of the missing component from your refund. The deduction amounts are predetermined by category and are usually disclosed in the platform's returns policy. Reviewing the returns policy before packing your return helps you avoid unexpected deductions.

Damage caused after delivery is another common cause of partial refunds. If an item was delivered in good condition and returned with new damage — scratches, dents, broken parts — the inspection team will note this and calculate a depreciation deduction. For electronics, this deduction can be substantial. Always photograph items before and after packing them for return, as this documentation provides evidence in case of dispute.

Promotional price adjustments can also result in partial refunds. If you purchased an item using a platform coupon, cashback offer, or bundled discount, the refund is calculated based on what you actually paid rather than the full list price. For example, if you purchased a product for ₹800 using a ₹200 coupon, your refund will be ₹800 — not ₹1000 — because that is the amount you paid. Reward points or loyalty credits applied to a purchase follow the same logic.

Shipping and handling fees are typically non-refundable unless the return is due to a platform error, such as receiving the wrong item or a defective product. For buyer's remorse returns — returns where there is no defect, just a change of mind — shipping fees paid on the original order may not be refunded. Always check the refund breakdown shown in the return request flow before confirming, as it clearly states which components will and will not be refunded.

If you believe a partial refund is incorrect, document your case with photographs of the returned item before shipping, your return shipping receipt, and any written communication with the platform. Most platforms have a formal refund dispute process that can be accessed through the Help Centre. Disputes submitted within 14 days of the refund being issued are given priority review."""
},

{
"topic": "refund_policy",
"source": "amazon/prime-refund",
"title": "Amazon Prime and Subscription Refunds",
"text": """Amazon Prime membership fees and digital subscriptions have their own refund rules, which differ from the standard product refund policy. Understanding these rules helps you make informed decisions about cancelling subscriptions and requesting fee refunds.

Amazon Prime annual memberships can be refunded in full if you have not used any Prime benefits since your last renewal. If you have used Prime benefits — such as free delivery, Prime Video streaming, or early access to deals — after the renewal date, Amazon will issue a prorated refund based on the number of months remaining in your membership. For example, if you cancel 6 months into an annual membership and have used Prime benefits, you will receive approximately half the annual fee back, minus any adjustments for benefits already used.

Monthly Prime memberships can be cancelled at any time, but refunds are only issued if the membership was not used and the cancellation occurs within a very short window after renewal. Most monthly Prime cancellations result in the membership continuing until the end of the current billing period with no refund. You can cancel your Prime membership from Account and Lists, then Prime Membership, then Manage Membership, and finally Cancel Membership.

Amazon Prime Video channel subscriptions — such as Zee5, Lionsgate Play, or Hayu — can be cancelled through the Prime Video Channels section. Refunds for channel subscriptions follow a similar prorated model but may vary by channel. Amazon Music Unlimited, Audible, and other Amazon subscription services each have their own refund terms, which are available in their respective help pages.

Accidental Prime purchases — cases where a customer renewed Prime without intending to — are handled on a case-by-case basis. Amazon customer service can often reverse an accidental renewal and issue a full refund if the request is made promptly and no Prime benefits have been used since renewal. Contact Amazon customer service immediately and explain that the renewal was unintended. Same-day requests have the highest success rate.

Prime Student, Amazon's discounted membership for students, follows the same general refund rules but has a free 6-month trial period. If you were charged for Prime Student after your trial ended and did not intend to continue, contact Amazon immediately and provide your educational institution email. Amazon typically grants a refund in these circumstances, especially for first-time post-trial charges."""
},

{
"topic": "refund_policy",
"source": "general/refund-not-received",
"title": "What to Do When Your Refund Has Not Been Received",
"text": """Not receiving an expected refund within the promised timeline is frustrating, but there is a clear step-by-step process for resolving it that works across most e-commerce platforms.

The first step is to verify the refund status on the platform. Log in to your account and navigate to the order. Look for a refund status section or a returns and refund timeline. Most platforms — including Amazon, Flipkart, and eBay — show each stage of the refund process with timestamps. Confirm that the refund was actually initiated and note the date it was sent.

If the platform shows the refund was initiated but you haven't received it, the next step is to contact your bank. Most banks have a refund enquiry process — you can call the customer care number on the back of your card or use the bank's app to check for pending or recently posted credits. Provide the bank with the refund initiation date and the amount. Banks can trace refunds using the transaction reference number (RRN) that the platform provides.

If both the platform and your bank confirm there is no trace of the refund, escalate the issue to the platform's customer service. When contacting support, prepare the following: your order ID, the return confirmation or pickup confirmation, the date the refund was supposed to arrive, and your bank account or card details (last 4 digits only — never share full card numbers). Most platforms have a dedicated refunds resolution team that can re-initiate failed refunds within 24 to 48 hours.

Escalation paths vary by platform. On Amazon, use the "Contact Us" flow and select "Returns and Refunds" then "Where is my refund?" On Flipkart, use the Help Centre within the app or website and navigate to "Refund not received." On eBay, use the Resolution Centre to reopen a closed case or open a new payment dispute.

For refunds that remain unresolved after 7 to 10 business days past the expected date, you have additional options. Credit and debit card holders can initiate a chargeback through their bank, which forces the bank to investigate and potentially reverse the original charge. Chargebacks should only be used as a last resort after exhausting the platform's own resolution process. Filing a chargeback while a platform investigation is ongoing can complicate both processes. Document every step — screenshots of refund status, chat logs, email correspondence — as this is essential for both platform appeals and bank chargebacks."""
},

# --- 30 more refund articles at production length ---

{
"topic": "refund_policy",
"source": "amazon/gift-refund",
"title": "Amazon Gift and Gift Card Refunds",
"text": """Refunds for gifts and gift-related purchases on Amazon have specific rules that depend on whether you are the gift giver or the gift recipient, and what type of gift was involved. Amazon has built a dedicated system for gift returns that preserves the privacy of the gift transaction.

If you received a gift purchased on Amazon and need to return it, you can use the Gift Returns section at Amazon.in/returns. You will need the order number, which is on the packing slip inside the package (Amazon includes this by default for all gift orders unless the sender specifically requested a no-packing-slip option). When you return a gift, Amazon issues the refund as an Amazon Gift Card to your email address rather than refunding the original buyer's payment method. This protects the privacy of the transaction and prevents the gift giver from knowing the item was returned.

Amazon Gift Cards themselves are non-refundable and cannot be exchanged for cash. Once loaded, the balance can only be used for purchases on Amazon. If you received a gift card that was accidentally purchased with incorrect details — for example, the wrong amount or the wrong recipient email — the gift giver can contact Amazon customer service within 24 hours of purchase to request a correction. After 24 hours, modifications to gift card purchases are generally not possible.

If you gave someone a gift through Amazon's digital gift card system and the recipient has not redeemed it, you can cancel the gift card through your Amazon account and receive a full refund to your original payment method. Navigate to Your Account, then Gift Cards, then View Gift Card Activity to see unredeemed cards.

For physical products bought as gifts, the return window is the same as for non-gift purchases: typically 10 days from delivery for most categories. The original purchaser can also initiate a return through Your Orders if the gift recipient prefers. In that case, the refund goes back to the buyer's payment method.

Amazon's Alexa devices and Fire tablets gifted during promotions may have specific refund terms tied to promotional bundles. Check the individual product's return policy at the time of purchase, as bundle items may have different eligibility windows than standard purchases."""
},

{
"topic": "refund_policy",
"source": "flipkart/flipkart-plus-refund",
"title": "Flipkart Plus Coins and Reward Points Refunds",
"text": """Flipkart Plus is Flipkart's loyalty program that awards customers with SuperCoins for every purchase. When you return an item, the SuperCoins earned on that order are reclaimed by Flipkart, and this reclamation process can affect your available SuperCoins balance in ways that may be surprising if you haven't read the policy carefully.

SuperCoins earned on a returned order are automatically deducted from your balance when the return is confirmed. If your current balance is sufficient, this deduction happens seamlessly. However, if you have already spent the SuperCoins earned on the returned order on another purchase or on Flipkart Plus membership, you will end up with a negative SuperCoins balance. This negative balance is carried forward and deducted from future SuperCoins earnings until it is cleared. Flipkart does not charge you for a negative balance, but it does mean your next few purchases will not generate net positive SuperCoins until the balance is restored.

SuperCoins used as a discount on the original purchase are handled differently. If you used SuperCoins to get a discount on an order that you later return, the refund will be for the amount you actually paid in cash. The SuperCoins used for the discount are not returned to your account because they were already redeemed and cannot be reversed. For example, if a product cost ₹500 and you used SuperCoins worth ₹100, paying ₹400 in cash, your refund will be ₹400 — not ₹500.

Flipkart Plus membership itself is paid for using SuperCoins, not cash. If you are a Flipkart Plus member and cancel your membership, the SuperCoins used to purchase the membership are not refunded. The Plus membership provides benefits for the duration of the membership period, and these benefits are considered consumed upon activation.

SuperCoins have an expiry period of 12 months from the date they were earned. If you return an item and your new SuperCoins would have expired before you had a chance to use them, there is no mechanism to extend their validity. However, Flipkart Plus members benefit from bonus SuperCoins multipliers that accumulate faster, partially compensating for this limitation."""
},

{
"topic": "refund_policy",
"source": "ebay/seller-initiated-refund",
"title": "eBay Seller-Initiated Refunds — Buyer's Guide",
"text": """On eBay, sellers can initiate refunds directly without buyer involvement through the seller's dashboard. This is common for situations such as out-of-stock items, shipping errors, or sellers proactively resolving buyer concerns. Understanding how seller-initiated refunds work helps you track them and respond appropriately.

When a seller initiates a refund, you will receive an email notification from eBay with the subject "You've received a refund." The email will specify the order details and the amount being refunded. If you were not expecting a refund, it is possible the seller cancelled the order because they could not fulfil it — which is a common occurrence when sellers list items with inaccurate inventory counts. In this case, the seller is required to send you an explanation through eBay messages as well.

Seller-initiated refunds take the same amount of time to process as any other refund: 3 to 5 business days for most payment methods, and up to 10 business days for some credit cards. The refund goes back to the original payment method used for the purchase.

If a seller initiates a partial refund as a goodwill gesture — for example, to compensate for late shipping or a minor cosmetic issue — you can accept it or reject it and request a full return and refund instead. eBay's messaging system allows you to negotiate with the seller. If you accept a partial refund, it is considered a resolution of the issue, and you may not be able to open a case for the same problem later.

Sellers are encouraged on eBay to refund quickly, as slow refunds negatively affect their seller performance metrics. Top Rated Sellers are required to maintain high standards of communication and refund speed. If you are buying from a Top Rated Seller and face a refund issue, the seller has strong incentives to resolve it promptly to maintain their status.

For items sold through eBay's promoted listings, the refund process is the same as for standard listings. eBay does not differentiate between advertised and non-advertised items in its buyer protection policies. All items are equally covered under the Money Back Guarantee regardless of how they were listed or discovered."""
},

{
"topic": "refund_policy",
"source": "general/refund-policy-comparison",
"title": "Comparing Refund Policies Across Amazon, Flipkart, and eBay",
"text": """Understanding the differences between Amazon, Flipkart, and eBay's refund policies helps you make informed purchasing decisions and know exactly what to expect if you need to return something. While all three platforms offer buyer protection, they differ in important ways regarding timelines, eligibility, and the level of protection provided.

Amazon's refund policy is generally considered the most buyer-friendly for direct Amazon-fulfilled orders. Returns are accepted within 10 days for most products and 7 days for electronics. Refund timelines are well-defined and consistently followed. Amazon's A-to-Z Guarantee provides a strong safety net for third-party seller transactions. The main limitation is that Amazon India's policy can differ from Amazon in other countries, so international buyers should verify the applicable policy.

Flipkart's refund policy is competitive but has slightly longer timelines. The 7 to 10 day return window (with 14 days for clothing and footwear) is reasonable, and the in-app tracking for return and refund status is among the best in the industry. The quality inspection step can add 2 to 3 days to the process, but it also provides a documented trail of the return. Flipkart's policy for large appliances and furniture, which requires damage reports within 48 hours, is stricter than Amazon's.

eBay's refund policy is more complex because it involves a marketplace of millions of individual sellers. The Money Back Guarantee is a powerful protection mechanism, but it requires the buyer to actively manage the process — opening cases, communicating with sellers, and sometimes returning items at their own expense before receiving a refund. eBay's peer-to-peer marketplace model means buyer experience varies more than on Amazon or Flipkart, where policies are centrally enforced.

For high-value electronics purchases, Amazon's direct-sold products typically offer the most comprehensive protection because of the A-to-Z Guarantee and centralised fulfilment. For fashion and lifestyle products, Flipkart's 14-day return window for clothing is particularly generous. For unique, collectible, or secondhand items, eBay's Money Back Guarantee provides reasonable protection despite the more complex claims process.

All three platforms improve their policies regularly, so checking the current policy before purchase is always advisable. The policies described here reflect general standards, but category-specific rules, seller-specific terms (on eBay), and seasonal policy adjustments can all affect your specific transaction."""
},

# ════════════════════════════════════════════════════════════════
# TOPIC 2 — RETURN POLICY  (40 articles)
# ════════════════════════════════════════════════════════════════

{
"topic": "return_policy",
"source": "amazon/return-overview",
"title": "Amazon Return Policy — Complete Guide",
"text": """Amazon's return policy is one of the most comprehensive in e-commerce, covering the vast majority of products sold on the platform. Understanding the return window, the process for initiating a return, and the conditions under which returns are accepted will help you shop with confidence and handle return situations efficiently.

The standard return window on Amazon India is 10 days from the date of delivery for most product categories. Electronics — including laptops, phones, cameras, and accessories — have a shorter window of 7 days. Clothing, shoes, and accessories typically have a 30-day return window when fulfilled by Amazon, though third-party sellers may have shorter windows. Books have a 10-day return window and must be in new, unread condition.

Certain categories are not eligible for return. These include consumable products (food, beverages, supplements) once opened, digital products (software, games, ebooks) once downloaded, personal care items once opened (cosmetics, hygiene products), and custom or personalised items. Hazardous materials and products requiring special handling are also non-returnable. Before purchasing, check the product's listing page for return eligibility information, which is displayed under the "Returns" section.

To initiate a return on Amazon, go to Your Orders, find the relevant order, and click Return or Replace Items. Select the specific item you want to return and choose the reason from the dropdown menu. Common return reasons include "No longer needed," "Item defective or doesn't work," "Item arrived damaged," "Wrong item was sent," and "Description on website was not accurate." The reason you choose affects whether you are responsible for return shipping.

If the return is due to an Amazon or seller error — wrong item, damaged item, or item not as described — Amazon provides a prepaid return label and the return shipping is free. For buyer's remorse returns — where there is no defect and you simply no longer want the item — Amazon provides a return label, but the cost may be deducted from your refund, typically ₹100 to ₹200 depending on the size and weight of the package.

Amazon offers three return methods: pickup, drop-off, and self-ship. Pickup scheduling is available in most pin codes and is the most convenient option — an Amazon delivery agent comes to your address within 3 to 5 business days. Drop-off points are available at designated Amazon Hub Locker locations and partner outlets. Self-ship is available for some categories where you arrange your own courier and submit the tracking details on Amazon. The refund timeline starts once Amazon receives your return."""
},

{
"topic": "return_policy",
"source": "amazon/return-electronics",
"title": "Amazon Electronics Return Policy — Detailed Guide",
"text": """Returning electronics on Amazon requires particular attention because of the shorter return window, specific condition requirements, and the need to protect yourself from post-return disputes. Electronics includes laptops, desktops, smartphones, tablets, cameras, audio equipment, gaming consoles, TVs, and accessories.

The return window for most electronics on Amazon India is 7 days from the date of delivery. This is shorter than the standard 10-day window for other categories because electronics have higher risk of misuse and the assessment of damage versus pre-existing condition is more complex. Some electronics — particularly large TVs, refrigerators, washing machines, and air conditioners — may have an even more specific policy involving installation and demonstration by an authorised technician before a return can be initiated.

Condition requirements for electronics returns are strict. The item must be returned in its original packaging with all accessories, including the original box, power adapter or charger, user manual, warranty card, and any bundled items such as earphones, stylus, or protective cases. Sealed items — those that were never opened — are eligible for a no-questions-asked return within the window. Opened items must show no signs of physical damage beyond what was present at delivery, have intact IMEI or serial number stickers, and must not have been registered with the manufacturer (though registration status alone is generally not a disqualifying factor).

Before returning electronics, always factory reset the device and remove all personal data. This is both a privacy best practice and a return requirement — Amazon and its quality inspection team will check that devices are not locked or tied to a specific account. For Apple devices, sign out of iCloud and disable Activation Lock before packaging the return. For Android devices, factory reset and remove Google account. Laptops should have all data wiped and the operating system restored to factory settings.

If your electronics product has a defect that appears after the return window, it is covered by the manufacturer's warranty rather than the Amazon return policy. Most electronics sold on Amazon carry a minimum 1-year manufacturer's warranty. Warranty service is handled directly by the manufacturer through their authorised service centres. Amazon's role in warranty claims is limited to providing invoice documentation if required by the manufacturer.

During the return process, photograph your electronics from multiple angles before packaging, including the device's IMEI or serial number, all accessories, and the condition of the original box. This documentation protects you if the quality inspection team at Amazon's warehouse raises a dispute about the condition of the returned item."""
},

{
"topic": "return_policy",
"source": "amazon/return-apparel",
"title": "Amazon Fashion Returns — Clothing, Shoes, and Accessories",
"text": """Amazon India offers a generous 30-day return window for fashion items — clothing, footwear, and accessories — when sold and fulfilled by Amazon. This extended window recognises that fashion items often need to be tried on and assessed for fit, style, and quality in ways that are not possible when ordering online.

Amazon Fashion returns are free — Amazon provides a prepaid return label and no deduction is made from your refund for return shipping, regardless of the reason for return. This policy applies to Amazon-fulfilled fashion items. Third-party sellers on Amazon may have different return windows and may charge for return shipping, so always check the "Sold by" and "Returns" sections on the product listing before purchasing.

Items must be returned in unworn, unwashed condition with all tags attached. Fashion items that appear to have been used — stains, odours, stretched fabric, or broken buttons — may be rejected at quality inspection. This does not mean you cannot try an item on; trying it on for size assessment is expected. The distinction is between trying on in a clean environment and actually wearing the item. Shoes returned with dirty soles suggest they were worn outside, which would result in a quality check failure.

Amazon's "Try Before You Buy" feature, when available, allows customers to try select fashion items for up to 7 days before being charged. You can return any or all items in your Try Before You Buy order without charge. If you keep an item, your payment method is charged after the 7-day trial period. This feature is available on select products and requires an Amazon Prime membership.

For footwear, return conditions include returning both shoes together (not just one), in the original shoe box, with any stuffing or shaping inserts intact. Attempting to return only one shoe in a pair results in an automatic rejection. For handbags and accessories, all hardware (clasps, chains, straps) must be intact and the item must be in its original protective dustbag or pouch if one was included.

Fashion returns during sale events like the Great Indian Festival follow the same 30-day policy, though the return window starts from the delivery date, not the order date. If you ordered during a sale but the item delivered after the sale, your return window still begins from delivery. Sale prices and discounts are fully refunded — Amazon does not adjust the refund to reflect post-sale pricing."""
},

{
"topic": "return_policy",
"source": "flipkart/return-overview",
"title": "Flipkart Return Policy — Complete Guide",
"text": """Flipkart's return policy is organised by product category, with each category having a specific return window and condition requirement. The policy is designed to be fair to both buyers and sellers while maintaining product quality standards across the platform's extensive catalogue.

Standard return windows on Flipkart are as follows: clothing and footwear can be returned within 14 days of delivery; electronics, appliances, and gadgets have a 7-day return window; furniture and large appliances must have damage or defect reports filed within 48 hours of delivery; books, media, and music have a 10-day window; beauty and personal care items are returnable within 7 days if unopened; home and kitchen products have a 10-day return window; and sports and fitness equipment have a 7-day window.

Items that are not eligible for return on Flipkart include any opened consumable product, personalised or custom items, digital downloads, items with a broken or tampered seal (for hygiene products and software), and items that have been clearly used and exceed normal examination. Flipkart's return policy page is searchable by product category and provides detailed eligibility information for each subcategory.

The return initiation process on Flipkart is fully mobile-first. Open the Flipkart app, go to My Orders, tap on the item you want to return, and select Return. You will be asked to choose a return reason and whether you want a refund or a replacement. After submitting the request, a return pickup date will be scheduled — typically within 3 to 5 business days. Ensure someone is present at the delivery address on the pickup date, as missed pickups need to be rescheduled and delay the overall process.

Flipkart uses its own logistics network, Ekart, for most return pickups. Ekart agents perform a basic visual inspection at the doorstep during pickup. This inspection checks that the correct item is being returned in roughly the expected condition. A more detailed quality check is performed at the warehouse. The doorstep inspection result can affect refund eligibility — if an agent flags a significant discrepancy between the stated condition and the actual condition at pickup, the return may be flagged for closer inspection.

For seller-fulfilled items on Flipkart Marketplace, return policies may differ from Flipkart's standard policy. The seller's return window and conditions apply for marketplace items. Flipkart provides a minimum baseline protection for marketplace purchases but cannot enforce refund terms beyond what the individual seller's policy specifies. If a marketplace seller refuses a legitimate return, escalate through the Flipkart Help Centre and a resolution specialist will mediate."""
},

{
"topic": "return_policy",
"source": "flipkart/return-large-appliances",
"title": "Flipkart Large Appliance Returns — TVs, Refrigerators, ACs",
"text": """Large appliances purchased on Flipkart — including televisions, refrigerators, washing machines, air conditioners, and dishwashers — have a specialised return and replacement process that differs significantly from the standard product return policy. This is because of the complexity of installation, the need for professional assessment, and the logistics involved in handling oversized items.

The return window for large appliances on Flipkart begins from the delivery date but damage or defect must be reported within 48 hours. After 48 hours, Flipkart typically does not accept returns unless the item has a manufacturing defect covered by the warranty. The 48-hour window is strictly enforced because appliances are expected to be installed and tested promptly after delivery.

When receiving a large appliance delivery, inspect the outer packaging carefully before the delivery agent leaves. If the packaging is visibly damaged — dents, tears, wet patches — photograph it immediately and note it on the delivery receipt. Open the box in the presence of the delivery agent if possible and check for obvious physical damage. If damage is found, you can either refuse delivery entirely (and the item will be returned to Flipkart with a refund initiated automatically) or accept it and report the damage within 48 hours through the app.

For appliances that require installation — ACs, washing machines, dishwashers — Flipkart offers installation services through authorised partners. The installation appointment is typically within 3 to 7 days of delivery. Wait until the appliance is installed and tested before finalising your assessment of whether it functions correctly. If the appliance develops a defect after installation, report it to Flipkart within the 48-hour window from the installation date for performance issues, or contact the manufacturer's service centre for warranty-covered defects.

Flipkart's large appliance return process involves a technician visit. A certified technician is dispatched to assess the reported defect and provide a written assessment. If the technician confirms the defect is a manufacturing issue, Flipkart will arrange for a replacement delivery and simultaneous collection of the defective unit. If the technician finds no defect or determines the damage was user-caused, the return or replacement will not be approved.

Delivery and installation fees paid for large appliances are generally non-refundable unless the return was due to Flipkart's fault — for example, wrong product delivered. Standard warranty service and annual maintenance contracts for appliances are managed by the manufacturer, not Flipkart, after the initial return window closes."""
},

{
"topic": "return_policy",
"source": "ebay/return-overview",
"title": "eBay Returns — Complete Buyer and Seller Guide",
"text": """Returns on eBay work differently from returns on traditional retail platforms because eBay is a marketplace where each listing belongs to an individual seller, and each seller can set their own return policy within eBay's guidelines. Understanding how seller return policies work, and what protections exist when a seller has a no-returns policy, is essential for a smooth eBay experience.

Sellers on eBay can choose from several return policy options: no returns accepted, 30-day returns, or 60-day returns. Sellers who accept returns must specify who pays for return shipping — either the buyer or the seller. Many top-rated sellers and business sellers accept 30-day free returns, which means the buyer can return the item for any reason and the seller provides a prepaid return label.

Even when a seller has a no-returns policy, eBay's Money Back Guarantee overrides the seller's policy in specific circumstances. The guarantee covers all purchases where the item did not arrive, arrived damaged, or does not match the listing description. In these cases, the buyer can open a case and receive a full refund regardless of the seller's stated policy. The no-returns policy only applies to buyer's remorse returns — situations where the item is as described but the buyer simply changed their mind.

To initiate a return on eBay, go to Purchase History, find the item, and click Return This Item. Select your return reason carefully — choosing "Item not as described" triggers the Money Back Guarantee process, while choosing "Changed my mind" initiates a standard return subject to the seller's policy. eBay will guide you through the next steps based on your selected reason. You will need to ship the item back within the timeframe specified by eBay or the seller.

When returning an item on eBay, use a tracked shipping service and retain the proof of postage. This is critical — if the seller claims the return was not received, your tracking number is the only evidence you have. eBay recommends using a service that requires a signature at delivery for high-value returns. Ship returns in appropriate packaging to prevent damage in transit, as a seller can dispute a return if the item arrives back in damaged condition.

eBay feedback plays a role in return transactions. Sellers who process returns professionally tend to have better feedback and higher trust ratings. As a buyer, you can leave neutral or negative feedback for sellers who handle returns poorly — providing evidence to the eBay community about seller behaviour. However, feedback for a return transaction should be based on the overall experience, including how promptly and professionally the seller communicated and resolved the issue."""
},

{
"topic": "return_policy",
"source": "general/return-packing",
"title": "How to Pack a Return Correctly — Avoiding Rejection",
"text": """Packing a return incorrectly is one of the leading causes of return rejection and delayed refunds. Warehouses process thousands of returns daily and quality inspectors have limited time to assess each item. Presenting your return in proper condition — original packaging, complete accessories, good labelling — significantly increases the chance of a smooth, full refund.

Start with the original outer box or packaging whenever possible. Original packaging is designed to protect the item during shipping and inspection teams expect to see it. If the original box is damaged beyond use, use a similarly sized plain cardboard box with adequate padding on all sides. Do not use a box that is significantly larger than the item, as this can cause the item to shift and sustain damage in transit.

Wrap the item itself in its original protective materials — bubble wrap, foam inserts, plastic protective film. For electronics, especially phones and tablets, keep the original moulded foam tray if it was included. Place all accessories in their original pouches or tie them together so they do not rattle loose inside the box. A loose charger cable inside a box with a glass item is a recipe for damage during shipping.

Include all documentation that came with the product: warranty cards, user manuals, quick start guides, and certificates of authenticity. For branded items, include all branded materials such as branded tissue paper, ribbon, or boxes within boxes. Missing documentation does not always result in a return rejection, but it can trigger a partial refund deduction in some platforms' policies.

Apply the return shipping label on the outside of the box in a location where it is clearly visible and not obscured by tape. If you received a prepaid label by email, print it clearly and affix it with adequate tape on all edges. Do not write over the label or cover any barcodes with tape. The barcode on the label is scanned at multiple points during transit and must be readable throughout the journey.

For clothing and footwear, fold items neatly and avoid using the original product packaging as the shipping container if it is not sturdy enough for transit. Place folded items in a poly mailer or inside a sturdy cardboard box. Include all original tags — attached to the item, not placed loosely in the package. Keep a photograph record of your packed return before sealing, including the label applied to the outside. This photograph serves as evidence of the condition at the time of shipment if any dispute arises at the warehouse."""
},

{
"topic": "return_policy",
"source": "general/return-without-receipt",
"title": "Returning Items Without a Receipt or Original Packaging",
"text": """Lost your receipt or thrown away the original packaging? The ability to return items without these materials depends on the platform, the product category, and the reason for the return. Here is a detailed breakdown of options available across the major platforms.

On Amazon, receipts are not required for returns because all transaction records are stored in your account under Your Orders. Amazon's system is entirely digital — the order ID serves as your proof of purchase and can be retrieved at any time. Original packaging, however, is required for many categories, particularly electronics. If you no longer have the original packaging for an electronics return, contact Amazon customer service before initiating the return. They can advise whether the return can be accepted in alternative packaging and whether a partial refund may apply for missing packaging.

Flipkart similarly maintains digital records of all transactions. Returns on Flipkart do not require physical receipts — the order confirmation in your account is sufficient. For packaging, Flipkart's policy varies by product category. For most non-electronic items, returns in clean, intact alternative packaging are accepted. Electronics and high-value items typically require the original packaging for a full refund, as the packaging is considered part of the product's value.

eBay returns require you to have the item's order information accessible through Purchase History. Physical receipts are not typically used on eBay. For packaging, the important consideration is that the item must arrive at the seller or eBay's processing centre undamaged. If the original packaging is not available, wrap the item adequately in your own packaging. The item's condition matters more than the box it comes in, though sellers can note that original packaging was missing.

Manufacturer warranty claims — which are separate from platform return processes — often require an invoice. Amazon, Flipkart, and eBay all provide digital invoice downloads from your order history, which manufacturers accept as proof of purchase for warranty service. Download and store a copy of your purchase invoice immediately after delivery for high-value items, as this document will be needed for any warranty service within the manufacturer's warranty period.

If your item was a gift and you do not have the order information, the gift giver needs to initiate the return or provide you with the order number. Alternatively, Amazon's gift return portal allows you to return gifts using only the order number from the packing slip, without needing the buyer's account information. Other platforms have similar but less well-developed gift return processes."""
},

# ════════════════════════════════════════════════════════════════
# TOPIC 3 — ORDER CANCELLATION  (35 articles)
# ════════════════════════════════════════════════════════════════

{
"topic": "order_cancellation",
"source": "amazon/cancel-before-ship",
"title": "How to Cancel an Amazon Order Before It Ships",
"text": """Cancelling an Amazon order before it is dispatched from the warehouse is the simplest and quickest way to get a full refund without the hassle of a return process. Pre-shipment cancellations are almost always granted and refunded in full with no questions asked.

To cancel an order on Amazon before shipment, log in to your account and go to Returns and Orders at the top right of the page. Find the order you wish to cancel. If it is still in "Pending" or "Preparing for shipment" status, you will see a Cancel Items button. Click this, select the specific items you want to cancel from the order (you can cancel individual items in a multi-item order), and choose a cancellation reason from the dropdown. Confirm the cancellation by clicking Cancel Checked Items.

After submitting the cancellation request, Amazon will confirm within a few minutes whether the cancellation was successful. For digital products or third-party seller items, the cancellation window may be shorter. If the cancellation is confirmed, your refund will be initiated immediately. For card payments, the refund takes 3 to 5 business days. For Amazon Pay balance, it is instant. If the payment was authorised but not yet captured (which is common for pre-orders or slower-shipping items), the authorisation is released and no refund transaction is necessary.

If the Cancel Items button is not visible, the order has likely already been dispatched or is in the final stages of packing and cannot be cancelled online. In this situation, contact Amazon customer service immediately and explain that you want to cancel before delivery. Amazon customer service can sometimes halt a dispatch in progress, but this is not guaranteed and depends on how far the order has progressed in the fulfilment pipeline. Amazon has large automated warehouses where orders are processed at high speed, and it is not always possible to intercept an order once it is in the packing stage.

For pre-order items — items ordered before they are released — you can cancel at any time before the release date with a full refund. Amazon charges for pre-orders only when the item ships, so no refund transaction is needed for cancellations before shipment.

Third-party seller orders on Amazon that are "Prime" eligible but fulfilled by the seller (not by Amazon) may have slightly different cancellation windows. The seller has the right to decline a cancellation if the item has already been prepared for dispatch. If the seller declines, you can still return the item after delivery for a full refund within the standard return window."""
},

{
"topic": "order_cancellation",
"source": "amazon/cancel-after-ship",
"title": "Cancelling an Amazon Order After Shipment — Options and Process",
"text": """Once an Amazon order has been shipped, it cannot be cancelled through the standard cancellation process. However, you still have several options available that effectively achieve the same outcome, though they require a few extra steps compared to a pre-shipment cancellation.

If the order has been shipped but not yet delivered, the simplest approach is to refuse delivery. When the delivery agent arrives with the package, you can tell them you wish to refuse it. The agent will scan the package as "Refused by customer" and return it to the courier's hub. The package will eventually be returned to Amazon's fulfilment centre, and once received, Amazon will initiate a refund automatically — typically within 5 to 7 business days of the refusal. Refusal is the most straightforward option for orders you know you do not want.

If you were not home when the delivery was attempted and the package was left at a safe location, or if you want to avoid confronting the delivery agent, you can accept delivery and then immediately initiate a return. Go to Your Orders, select the item, click Return or Replace Items, and choose "No longer needed" as the return reason. Schedule a return pickup, and Amazon will collect the item and process the refund upon receipt. Keep in mind that for buyer's remorse returns (no fault with the product), a small return shipping fee may be deducted.

Amazon does not charge a cancellation fee for any order cancellation, whether pre-shipment or post-delivery return. The only potential cost is the return shipping fee for buyer's remorse returns, which is usually nominal — approximately ₹100 to ₹200 depending on item weight. If the order was for a faulty, incorrect, or misrepresented item, no shipping fee is charged.

For orders with expedited delivery options (same-day, one-day, two-day), Amazon charges the delivery fee only if the item is delivered. If you cancel before dispatch, the delivery fee is also refunded. If you return the item after delivery, the expedited delivery fee is typically not refunded as the service was already performed.

Subscriptions to "Subscribe and Save" items on Amazon can be cancelled or paused from the Subscribe and Save section in your account. Cancelling a subscription stops future orders but does not affect the current pending shipment if one is already in progress."""
},

{
"topic": "order_cancellation",
"source": "flipkart/cancel-overview",
"title": "Flipkart Order Cancellation — Complete Process Guide",
"text": """Flipkart's order cancellation system is designed to be quick and accessible through the app and website, with most cancellations processed within minutes. The key variable in the cancellation process is whether the order has been dispatched from the warehouse, which determines which cancellation path is available to you.

For orders that have not yet been dispatched, the cancellation process is completely straightforward. Open the Flipkart app, go to My Orders, tap on the order you want to cancel, and select Cancel. You will be asked to choose a cancellation reason — selecting an accurate reason helps Flipkart improve its service. After confirming the cancellation, Flipkart will process the cancellation and send you a confirmation email within a few minutes. Refunds for pre-payment (net banking, card, UPI) are initiated immediately upon cancellation. COD orders require no refund as no payment was collected.

Once an order is dispatched, the Cancel option in the app is no longer available. At this stage, you can track the delivery in real time and plan your response. If the order has not yet been handed to the delivery agent and is still in a Flipkart hub, calling Flipkart customer service may result in a pre-delivery cancellation, though this depends on the logistics chain status. Customer service can flag the package for return to hub, but this is not always possible once the last-mile delivery has begun.

If the order is out for delivery, you can refuse it when the delivery agent arrives. Flipkart's delivery agents are instructed to note the refusal reason and return the package. After a refused delivery, the refund process begins once Flipkart's hub scans the returned package, usually within 2 to 3 business days of refusal. For pre-paid orders, the full refund is then initiated to the original payment method within the standard refund timeline.

Flipkart allows partial order cancellations for multi-item orders. If your order contains multiple items that are dispatched separately, you can cancel individual items that have not yet been dispatched while keeping the rest. Each item has its own fulfilment status in the My Orders section, and the cancel button will be available for individual items that are still within the cancellable window.

If Flipkart cancels your order — due to stock unavailability, seller issues, or fraud prevention — you will receive an email and app notification with the reason. Seller-initiated cancellations on Flipkart Marketplace require Flipkart to issue a full refund automatically. Repeated seller cancellations are penalised by Flipkart and can result in the seller's delisting from the platform."""
},

{
"topic": "order_cancellation",
"source": "ebay/cancel-overview",
"title": "Cancelling an eBay Order — Buyer and Seller Process",
"text": """Order cancellations on eBay involve both the buyer's request and the seller's approval, making the process slightly more involved than on direct retail platforms. Understanding the roles of each party and the timelines involved ensures you know exactly what to expect when you need to cancel a purchase.

As a buyer, you can request an order cancellation within 1 hour of making a purchase on most eBay listings. To do this, go to Purchase History, find the order, click More Actions, and select Cancel This Order. You will need to provide a reason for the cancellation. After you submit the request, eBay notifies the seller. The seller has 3 days to accept or decline the cancellation request. If the seller accepts, the order is cancelled and a full refund is initiated. If the seller declines or does not respond within 3 days, the cancellation request expires and the order remains active.

Sellers can also cancel an order on eBay — for example, if an item is out of stock or was damaged. When a seller cancels an order, the buyer receives a full refund automatically. eBay penalises sellers for buyer-initiated cancellations that the seller accepts, counting them against the seller's transaction defect rate. This incentivises sellers to fulfil orders as listed but does create a tension between seller metrics and buyer flexibility.

If your cancellation request was declined and you still do not want the item, your next option depends on the order status. If it has not shipped, contact the seller through eBay Messages and explain your situation — many sellers will cancel as a courtesy, especially if the reason is compelling. If it has already shipped, you must wait for delivery and then initiate a return through the standard eBay returns process.

For Buy It Now listings that were paid through eBay Checkout, the cancellation process above applies. For auction listings, the winning bid is binding and cancellations are generally not permitted. eBay will not force a seller to accept a cancellation on an auction purchase unless there are extraordinary circumstances. If you bid in error (for example, an accidental bid), contact the seller immediately and explain; many sellers will cancel on goodwill. However, they are not obligated to do so.

Cancellation fees do not exist on eBay for buyers. The only cost consideration is that some payment methods may take time to fully refund, and PayPal holds some funds temporarily. eBay does not charge buyers for initiating cancellation requests even if they are declined."""
},

{
"topic": "order_cancellation",
"source": "general/cancel-cod-order",
"title": "Cancelling a Cash on Delivery Order — What You Need to Know",
"text": """Cash on Delivery (COD) orders are among the most common in India, and many customers wonder about the cancellation implications since no payment has been made upfront. While COD cancellations seem straightforward, there are nuances regarding how they affect your account, future ordering privileges, and the logistics cost borne by the platform.

Cancelling a COD order before shipment is completely free and has no negative consequences. Simply go to My Orders on the relevant platform — Amazon, Flipkart, or Meesho — find the COD order, and click Cancel. Since no payment was collected, no refund is necessary, and the cancellation is instant. This is the ideal way to cancel a COD order that you no longer want.

Cancelling a COD order after shipment — either through refusal at delivery or by contacting customer service — carries a hidden cost that is borne by the logistics system. When a COD order is out for delivery and returned undelivered, the courier company still incurs fuel, labour, and operational costs for the failed delivery attempt. E-commerce platforms absorb this cost initially but track it against buyer accounts.

High COD cancellation rates — defined as repeatedly refusing COD orders or requesting cancellation after dispatch — can result in your account being flagged for increased scrutiny. In more extreme cases, platforms like Amazon and Flipkart may restrict your ability to place COD orders if your cancellation rate exceeds certain thresholds. This is not publicised prominently, but customer service representatives can confirm that account-level COD restrictions exist and are applied to accounts with unusually high cancellation rates.

If you need to cancel a COD order that has already shipped, the cleanest approach is to call the courier company directly (the tracking number in your order details will identify the courier) and request an intercept or hold at the hub. Some couriers allow you to redirect or hold a package for a short window before the last-mile delivery attempt. Alternatively, accepting delivery and then immediately raising a return request is also acceptable and does not count as a "refused delivery" in the same way.

For businesses that order in bulk on COD terms, Flipkart and Amazon both offer business accounts with prepaid billing options that are more favourable from a logistics efficiency standpoint. Switching to prepaid payment methods also eliminates the COD restriction risk and often qualifies for additional discounts."""
},

{
"topic": "order_cancellation",
"source": "general/cancel-subscription",
"title": "How to Cancel Subscriptions and Auto-Renewal Orders",
"text": """Subscription services and auto-renewal orders are a growing part of e-commerce, and managing them requires a different approach than one-time purchases. Whether you want to cancel an Amazon Prime membership, a Subscribe & Save order, a Flipkart Plus subscription, or a recurring order on any platform, the process and implications vary by service type.

Amazon Subscribe & Save allows customers to set up recurring delivery of household essentials at a discount. Each Subscribe & Save order is delivered on a monthly or customised schedule. To cancel a Subscribe & Save subscription, go to Account and Lists, then Subscribe & Save, find the product, and click Cancel Subscription. Cancelling the subscription stops future deliveries but does not affect an order that has already been prepared or shipped for the current cycle. If you want to skip a delivery without cancelling, you can delay the upcoming delivery date through the same management page.

Amazon Prime membership auto-renews annually (or monthly for monthly plans). To prevent auto-renewal, go to Account and Lists, then Prime, then Manage Membership, and click Do Not Continue. This stops the renewal at the end of the current period without cancelling your benefits immediately. If you have already been charged for a renewal you did not intend, contact Amazon customer service immediately — refunds for accidental renewals are often granted within the first 24 to 48 hours if no benefits were used.

Flipkart's subscription services — including Flipkart Plus and Super Value Day memberships — are managed through Account Settings under Subscription Management. You can view all active subscriptions, their renewal dates, and the option to cancel. Cancelling a Flipkart Plus subscription stops future SuperCoin bonuses but retains any unspent SuperCoins already in your account.

For third-party subscription boxes (monthly beauty boxes, curated gift boxes, etc.) purchased through Amazon or Flipkart, cancellation is typically managed through the seller or brand's own subscription portal, not the e-commerce platform's cancellation system. Check the seller's product page for their subscription management URL or contact them directly through the platform's messaging system.

Pre-order cancellations for content releases — video games, books, movies — are generally available up until the release date and do not incur any charges since payment is not captured until shipment. Always cancel pre-orders before the release date if your plans change, as post-release cancellations may not be possible if the digital code has been delivered."""
},

# ════════════════════════════════════════════════════════════════
# TOPIC 4 — DELIVERY ISSUES  (40 articles)
# ════════════════════════════════════════════════════════════════

{
"topic": "delivery_issues",
"source": "amazon/missing-package",
"title": "Amazon Package Shows Delivered But Not Received — What to Do",
"text": """The "delivered but not received" situation is one of the most common and frustrating delivery issues in e-commerce. Amazon tracks millions of packages daily, and while the vast majority are delivered correctly, carrier errors, GPS scan inaccuracies, and theft do occasionally result in packages being marked as delivered when the customer has not received them.

Your first step when you see a "Delivered" status but have not received the package is to wait 24 hours. This is not because Amazon is stalling — it is because carriers sometimes scan packages as delivered when they are actually sitting at the local sorting hub or in the delivery vehicle scheduled for the next morning. This is known as a "pre-scan" and it is more common than you might expect, particularly during high-volume delivery periods. Check your phone for a delivery notification or photo if Amazon or the carrier sends delivery confirmation images.

If 24 hours have passed and you still have not received the package, conduct a physical search of your building. Check with your building security guard, reception desk, concierge, or neighbours. Check all possible delivery locations — mailboxes, gates, garage, porch, back door, side entrance. Many deliveries are left in safe locations that the resident is unaware of. Amazon delivery agents can often leave notes in the app indicating where they placed the package.

After checking these physical locations, open Your Orders on Amazon and click "Problem with this order" under the undelivered order. Select "Package didn't arrive" and follow the guided process. Amazon will ask a few verification questions and then open an investigation. In most cases of genuinely missing packages, Amazon offers a replacement or refund within 24 to 48 hours without requiring extensive investigation, particularly for high-trust accounts with good order history.

If Amazon's initial investigation requires more time, you will receive a timeline estimate by email. Complex cases — for example, where the carrier's GPS data shows delivery at a location very close to your address — may involve Amazon requesting GPS records from the carrier and comparing them with your address coordinates. This process can take 3 to 5 business days.

Report the issue promptly — Amazon's policy requires missing delivery reports to be filed within 30 days of the estimated delivery date. Filing earlier gives Amazon more options, including recalling the package from the carrier's system if it is still in transit. Documenting your building search (photos, notes from security desk, responses from neighbours) strengthens your case if the investigation is contested."""
},

{
"topic": "delivery_issues",
"source": "amazon/late-delivery",
"title": "Amazon Late Delivery — Causes, Rights, and Compensation",
"text": """Amazon provides delivery date guarantees for most orders, particularly for Amazon Prime members. When orders are not delivered by the promised date, you have rights and may be eligible for compensation. Understanding what caused the delay and how to act appropriately gets the best outcome.

Amazon's delivery date commitments vary by delivery type. Standard delivery windows are estimates and are not guaranteed — they represent the typical delivery timeframe for your pin code and are calculated based on historical performance. Prime delivery dates, displayed prominently during checkout, are commitments. If Amazon says your Prime order will be delivered by Friday and it arrives on Monday, that is a breach of the delivery commitment.

Common causes of delivery delays include weather disruptions (floods, cyclones, heavy snowfall), operational disruptions at Amazon fulfilment centres or delivery hubs, incorrect addresses, recipient unavailability during delivery attempts, and carrier capacity issues during peak periods. Amazon communicates proactively about delays caused by external events through email and in-app notifications.

For Prime delivery date breaches, Amazon offers compensation to affected customers. Compensation typically comes in the form of a 30-day free Prime extension, Amazon Pay credits, or in some cases full refunds on delivery fees. The compensation is not automatic — you need to contact Amazon customer service, explain the situation, and request compensation. Amazon's customer service team has the authority to issue credits and extensions for verified delivery date breaches.

If your order is tracking as significantly delayed and you need the item urgently, you have several options. You can cancel the order if it has not shipped and reorder with a faster delivery option. If it has shipped, contact the carrier directly using the tracking number to get an estimated delivery window. For urgent items, Amazon's same-day or Prime Now delivery might be faster alternatives if available in your area.

Amazon's delivery performance statistics are monitored internally, and carriers that consistently fail to meet delivery commitments are subject to contract reviews. Reporting your late delivery, even if the refund or compensation is not significant, contributes to the data that Amazon uses to hold carriers accountable."""
},

{
"topic": "delivery_issues",
"source": "flipkart/wrong-address",
"title": "Flipkart Delivery to Wrong Address — Resolution Process",
"text": """A delivery to the wrong address is a serious logistics error that requires prompt action from both the customer and Flipkart. Whether the error was caused by a data entry mistake during order placement, a system issue, or a carrier error, Flipkart has a defined process for addressing it.

The most important first step when you realise an order may be going to the wrong address is to check your order confirmation email. The delivery address is clearly stated in the order confirmation. If the address is wrong, check whether you accidentally selected a saved address that you no longer use or entered new details incorrectly. This tells you whether the error was on your side or Flipkart's side.

If you notice the wrong address before shipment, you can sometimes update it. Flipkart allows address changes on pre-shipment orders in some cases, though this is not universally available. Go to My Orders, select the order, and look for an option to edit the address. If no option is available, contact Flipkart customer service immediately through the Help Centre chat. Be prepared to provide your order ID and the correct address. The closer you are to the dispatch time, the less likely an address change is possible.

If the order has already shipped to the wrong address, contact Flipkart customer service with your order ID and the correct address. Flipkart can attempt to contact the carrier (Ekart or a third-party courier) to redirect the delivery before the first delivery attempt. Address redirection is possible in some cases but not guaranteed, particularly when the package has already been loaded onto the last-mile delivery vehicle.

If the package was delivered to the wrong address and someone else received it, Flipkart will initiate an investigation with the carrier. If the delivery is confirmed to be at a wrong address, Flipkart will typically dispatch a replacement order to your correct address within 3 to 5 business days. If the original package can be recovered, it may be redelivered. If it cannot be recovered, a replacement or full refund is provided.

Preventing wrong-address deliveries is straightforward: maintain your saved addresses list on Flipkart by regularly reviewing and deleting old addresses that are no longer valid. During checkout, always verify the delivery address on the order summary page before clicking Place Order. If you frequently order to multiple addresses, labelling them clearly (Home, Office, Parent's House) reduces selection errors."""
},

{
"topic": "delivery_issues",
"source": "ebay/international-delivery",
"title": "eBay International Delivery Issues — Customs, Delays, and Resolution",
"text": """International orders on eBay are subject to additional delivery complexity compared to domestic orders. Understanding customs clearance, international shipping timelines, and the resolution process for international delivery issues helps you manage expectations and take the right steps when problems arise.

Customs clearance is the most common cause of delays in international eBay orders. All international packages must pass through customs inspection in the destination country. Customs agencies assess the declared value of the goods and determine whether import duties and taxes apply. If duties are due, the package is held at customs until the recipient pays. You will typically receive a notification from the customs agency or the carrier (e.g., DHL, FedEx, India Post) requesting payment before release.

Import duties and taxes for international eBay purchases are the buyer's responsibility and are not included in the listing price or shipping cost displayed at checkout. Before bidding on or buying international items, use a customs duty calculator to estimate the additional cost. For items valued above a certain threshold (in India, INR 5000 for personal imports), customs duty may apply. Luxury goods, electronics, and certain product categories have higher duty rates.

Estimated delivery times for international eBay orders range from 7 days for express international shipping to 45 days or more for economy international shipping services. The eBay listing displays estimated delivery dates, but these are calculated from historical averages and can vary significantly depending on customs processing times in both the origin and destination countries.

If your international eBay order has not arrived within the estimated window, the first step is to check tracking on both the carrier's website and eBay's order tracking page. International tracking can have gaps — particularly for economy postal services that use national post networks. Packages may be "in transit" for extended periods with no tracking updates as they pass between national postal systems.

When to open a case: eBay's Money Back Guarantee for international orders has the same 30-day window from the estimated delivery date. If tracking shows the package was returned to the sender or lost in transit, open a case immediately. eBay handles international cases through the same Resolution Centre as domestic cases, though the investigation may take slightly longer to account for international courier response times."""
},

{
"topic": "delivery_issues",
"source": "general/delivery-attempt-failed",
"title": "Failed Delivery Attempt — What Happens and What to Do",
"text": """A failed delivery attempt occurs when a carrier tries to deliver your package but is unable to do so. This can happen due to the recipient being unavailable, an access issue at the delivery address, an incorrect or incomplete address, or the carrier's judgement that the location is unsafe to leave the package unattended. Understanding the consequences of a failed delivery and the options available to you helps you act quickly and avoid losing your order.

The standard procedure after a failed delivery attempt is that the carrier leaves a delivery notice at the address (either a paper card or a digital notification in the platform's app) and returns the package to their local hub or depot. Most carriers allow 24 to 48 hours before attempting delivery again. If the package is eligible, a second delivery attempt is usually made the following business day. After two or three failed attempts, the package is typically returned to the origin warehouse.

What happens next depends on the platform. Amazon initiates a return-to-origin scan and refunds the buyer automatically after the returned package is received at the fulfilment centre — typically within 5 to 7 business days of the return scan. Flipkart follows a similar process, with refunds initiated after the package passes quality inspection at the return hub. eBay delivery failures are more complex because sellers are responsible for the outcome — the buyer needs to contact the seller to arrange reshipment or request a refund.

To prevent failed deliveries: ensure your address is accurate and complete, including floor number, building name, and landmark. Ensure someone will be at the address during the expected delivery window shown in the tracking information. For important deliveries, consider choosing "Delivery to Neighbor" instructions if the platform offers this option. Amazon, Flipkart, and some couriers allow you to add delivery instructions such as "Leave with ground floor security" or "Ring flat 2B for access."

If you know you will not be home, most platforms allow you to reschedule delivery through the tracking page or app. Amazon's delivery rescheduling is available in some pin codes and allows you to select a preferred delivery slot up to 3 days in advance. Flipkart allows delivery date changes through the My Orders section for some orders. Alternatively, you can redirect delivery to a nearby Amazon Hub Locker or a trusted neighbour's address by updating the delivery instructions."""
},

{
"topic": "delivery_issues",
"source": "amazon/delivery-damaged-packaging",
"title": "Amazon Order Delivered with Damaged Outer Packaging",
"text": """Receiving an Amazon package with damaged outer packaging is cause for immediate attention, as it may indicate damage to the product inside. Knowing how to assess, document, and respond to this situation properly ensures you receive the correct resolution — whether that is keeping the product if undamaged, exchanging it, or receiving a full refund.

When a package arrives with visibly damaged outer packaging — crushed box, torn edges, wet patches, or clear signs of having been dropped — document the damage before opening. Take clear photographs of all sides of the package, particularly the damaged areas. Include a photograph with the shipping label visible to establish that the documentation relates to the specific order. This photographic record is valuable evidence for any subsequent claim.

Open the package carefully and inspect the product inside. If the product appears undamaged, test it if possible before deciding whether to keep it. Many products are well-protected by inner packaging and survive outer damage without issue. If the product is undamaged and functional, no action may be necessary. However, if the product was damaged in transit — scratches, dents, cracks, broken components — proceed with a damage claim.

To file a damage claim on Amazon, go to Your Orders, find the order, and click Return or Replace Items. Select "Item arrived damaged" as the reason. You will be asked to describe the damage and may be prompted to upload photographs. Amazon may verify the claim through your account history and the photographs provided. For high-value or frequently claimed products, Amazon may request additional information.

Amazon's resolution for items damaged in transit is typically a free replacement. If replacement stock is unavailable for your specific product, Amazon will offer a full refund. Damaged item replacements are generally dispatched within 2 to 3 business days. You will need to return the damaged original — Amazon provides a free prepaid return label and pickup for damaged item returns.

Note that damage caused by Amazon's packaging — where the product is inadequately packed for the shipping method — results in Amazon covering the full replacement cost without any questions. If the packaging was appropriate but the carrier was negligent, Amazon typically still covers the replacement as part of its seller guarantee, then recovers the cost from the carrier. From the buyer's perspective, the outcome is the same: a free replacement or full refund."""
},

{
"topic": "delivery_issues",
"source": "flipkart/tracking-not-updated",
"title": "Flipkart Order Tracking Not Updating — What It Means",
"text": """Order tracking information that stops updating can be alarming, but it is important to understand that tracking freezes are common and often do not indicate a problem with your delivery. Here is a guide to interpreting tracking status and knowing when to be concerned.

Tracking updates occur when a package is scanned at specific points in the logistics chain — warehouse departure, sorting hub arrival, sorting hub departure, local delivery hub arrival, and out for delivery. Between these scans, there are no updates, and the tracking page will show the last known status. For standard delivery, packages can travel for 12 to 24 hours between scans. For inter-city or inter-state shipments, gaps of 24 to 48 hours between scans are normal.

Common tracking statuses and what they mean: "Order dispatched" means your order has left the Flipkart warehouse and is in the carrier's possession. "In transit" means the package is moving between sorting hubs. "Out for delivery" means the package is on the last-mile delivery vehicle heading to your address. "Delivery attempted" means the carrier tried to deliver but could not complete the delivery.

If tracking has not updated for more than 72 hours from the last scan, it may indicate the package is stuck in a sorting hub. This can happen due to hub capacity issues, weather events, or operational problems. In these cases, the estimated delivery date shown on Flipkart's tracking page may update to reflect a new timeline.

When tracking shows no update for more than 5 days from the last scan, contact Flipkart customer service through the Help Centre. Provide your order ID and the date of the last tracking update. Flipkart will initiate an inquiry with its logistics partner (Ekart or third-party courier) to locate the package. This investigation typically takes 2 to 3 business days. If the package is confirmed lost, Flipkart will dispatch a replacement or issue a full refund.

Do not confuse tracking page delays with actual delivery delays. Sometimes the tracking page itself takes several hours to reflect a scan that has already occurred at a hub. If your expected delivery date has passed and the tracking shows the package was still in transit as of the previous day, call the courier company directly using the tracking number for the most up-to-date status."""
},

# ════════════════════════════════════════════════════════════════
# TOPIC 5 — PAYMENT FAILURES  (35 articles)
# ════════════════════════════════════════════════════════════════

{
"topic": "payment_failures",
"source": "amazon/payment-failure-causes",
"title": "Why Amazon Payments Fail — Complete Cause Analysis",
"text": """Payment failures on Amazon are frustrating, especially when you have confirmed your details but the transaction still does not go through. Understanding the reasons behind payment failures helps you troubleshoot efficiently and complete your purchase successfully.

Insufficient funds is the most straightforward cause. If your debit card or bank account does not have enough balance to cover the total order amount including delivery charges and applicable taxes, the payment will fail. Check your account balance before placing the order. For credit cards, this translates to exceeding your credit limit or available credit — even if your overall limit is sufficient, some banks block transactions when the available credit is below a certain threshold.

Card expiry is a common and easily overlooked cause. Cards expire at the end of the month shown on the front of the card. If your card expired last month but you are still using the saved details on Amazon, all transactions will be declined. Update your payment details in Your Account under Payment Methods. When entering a new card, ensure you are using the new expiry date and new CVV from the replacement card.

3D Secure authentication failures occur when your bank's OTP (One Time Password) system has an issue. You may not receive the OTP due to poor mobile network connectivity, SMS delivery delays, or your phone being off. OTPs for online transactions typically expire within 3 to 5 minutes. If you receive the OTP late, it may no longer be valid by the time you enter it. Request a new OTP if the first one does not arrive within 2 minutes.

Bank-side transaction blocks are less visible but very common. Banks use fraud detection algorithms that block transactions that appear unusual — a new merchant, an unusually large purchase, an out-of-state transaction, or multiple purchases in a short time. These blocks are temporary and can be resolved by calling your bank's customer care number and authorising the transaction. Many banks also allow you to temporarily increase transaction limits through their app.

International transactions require specific card settings. If you are purchasing from an international eBay seller or an Amazon merchant with international billing, your card may need to be enabled for international transactions. Contact your bank to enable this feature. Some banks enable it for a limited period and then revert to domestic-only settings.

Failed UPI transactions can occur due to bank server downtime, UPI app issues, or daily UPI transaction limit exceedances. NPCI limits individual UPI transactions to ₹1 lakh per transaction in most cases, though some banks have lower limits. Check your bank's UPI transaction limits in the banking app."""
},

{
"topic": "payment_failures",
"source": "amazon/money-deducted-order-not-placed",
"title": "Money Deducted But Amazon Order Not Placed — What to Do",
"text": """One of the most alarming payment situations is when money is deducted from your account but no order appears in Your Orders on Amazon. This happens when a payment is processed at the bank level but the confirmation fails to reach Amazon's order management system — typically due to a network timeout during the transaction handshake between Amazon's payment gateway and the bank.

First, check Your Orders on Amazon and also check your email for an order confirmation. Sometimes there is a delay of 5 to 10 minutes between payment processing and order confirmation appearing. The order may have gone through successfully and is just taking time to reflect. Refresh the page after 10 minutes and also search your email's spam folder for an Amazon order confirmation.

If after 15 to 20 minutes there is still no order in Your Orders and no confirmation email, check your bank account or card statement. Look for the deducted amount. There are two scenarios: the amount may be showing as a "pending" transaction (meaning it is a temporary authorisation hold that will reverse automatically), or it may be showing as a completed debit (which means the money was actually deducted).

For pending transactions — which appear as a hold on your account but have not yet settled — these typically reverse within 5 to 7 business days automatically if the corresponding order was not created. A payment authorisation hold is not a completed charge; it reserves the funds but releases them if the transaction is not completed. No action is required on your part, but you can contact your bank to confirm the hold will release.

For completed debits without a corresponding order, contact Amazon customer service immediately. Provide the order date and time, the deducted amount, and any bank reference number (RRN) if visible in your bank statement. Amazon's payments team can trace the transaction through their payment gateway and either create the order retroactively or initiate a refund. Most such cases are resolved within 24 to 48 hours.

To prevent this situation, use a stable internet connection when making payments on Amazon. Avoid switching networks or closing the browser during the payment gateway process. If a transaction times out, do not immediately retry without checking your bank balance first — retrying a failed transaction without verification can result in double deduction, which requires additional steps to resolve."""
},

{
"topic": "payment_failures",
"source": "flipkart/payment-failure-resolution",
"title": "Resolving Flipkart Payment Failures — Step by Step",
"text": """Flipkart supports a wide range of payment methods — debit cards, credit cards, net banking, UPI (GPay, PhonePe, Paytm, BHIM, others), Flipkart Pay Later, EMI options, and Flipkart Gift Vouchers. Payment failures can occur across any of these methods, and each has its own troubleshooting pathway.

When your Flipkart payment fails, the first action Flipkart takes is to display an error message explaining the reason — "Payment declined," "Transaction timeout," "Bank server down," or "Insufficient funds." Read this message carefully as it usually points to the correct solution. If the error says "Try again in a few minutes," it is likely a temporary server issue on either Flipkart's or your bank's side.

For debit and credit card failures: verify that your card is active and not expired. Confirm that the card is enabled for online transactions (e-commerce transactions). Check that your billing address matches your bank's records if the billing address is required. Try with a different card to isolate whether the issue is card-specific. If all cards fail, the issue may be on Flipkart's end — check Flipkart's social media channels for outage announcements.

For UPI failures: ensure your UPI app (Google Pay, PhonePe, etc.) is updated to the latest version. Check that your bank account linked to UPI has sufficient funds. Verify that your UPI PIN is correct. Some UPI failures are caused by the payment link expiring — Flipkart's payment screen has a timer, and if the timer runs out before you complete the UPI authentication, the payment will fail. Try the payment again from the beginning.

For net banking failures: net banking portals can be slow or unavailable, particularly during peak hours (lunchtime, evenings). If the bank portal does not load, the transaction times out and fails. Try during off-peak hours or switch to UPI. Ensure your net banking is set up with a transaction password and second-factor authentication is active.

Flipkart Pay Later failures can occur if your Pay Later limit has been exhausted, if your account has been temporarily blocked due to missed payment, or if the KYC (Know Your Customer) verification for Pay Later has not been completed. Check your Flipkart Pay Later section for any alerts or limit information.

If money was deducted but no order was placed on Flipkart, report it through Help Centre → Payment Issue → Money deducted but order not placed. Provide the transaction amount, date, and your bank reference number. Flipkart's payment team investigates and issues a refund within 5 to 7 business days for confirmed double deductions."""
},

{
"topic": "payment_failures",
"source": "ebay/payment-methods",
"title": "eBay Payment Methods — Issues and Troubleshooting",
"text": """eBay has transitioned to a managed payments system called eBay Payments, which consolidates payment processing across the platform. Understanding how eBay Payments works and what to do when payments fail helps you resolve issues quickly.

eBay accepts payments through credit cards (Visa, Mastercard, American Express), debit cards, PayPal, Apple Pay, and Google Pay. Bank transfers and payment on delivery are not supported through the standard eBay Payments system. Payment options available may vary depending on the seller's location and the buyer's country.

Credit card declines on eBay most commonly occur for the same reasons as on other platforms: insufficient credit, expired cards, fraud blocks, or incorrect billing details. The additional consideration for eBay international purchases is that your bank may require you to enable international transactions separately. Contact your bank before attempting international eBay purchases for the first time to verify that your card is set up for international use.

PayPal on eBay has its own set of potential issues. If your PayPal account is limited — meaning PayPal has placed a restriction on withdrawals or payments pending verification — you cannot use it for eBay purchases. Log in to PayPal directly to check for any limitations notices. Completing PayPal's identity verification (by submitting a government ID or linking a bank account) typically resolves limitations quickly.

Apple Pay and Google Pay failures on eBay are usually related to the linked card in the digital wallet being declined, or biometric authentication failing. Check the linked card's status and try again with manual authentication if biometric fails.

For cases where payment was processed but the order does not appear, eBay's Order Not Found help page provides a specific resolution flow. Check your email for a confirmation and log in to Purchase History. If neither shows the order, contact eBay customer service with the transaction reference from your bank statement. eBay's payment team can reconcile the transaction within 48 hours.

eBay also offers a feature called eBay Bucks (now integrated into eBay Extras Mastercard rewards in some regions), which can be used as partial payment. If your Bucks balance is insufficient for the full purchase, the remainder is charged to your primary payment method. Ensure your primary payment method on file is current if you plan to use Bucks as partial payment."""
},

{
"topic": "payment_failures",
"source": "general/double-deduction",
"title": "Double Payment Deduction in E-commerce — What Happens and How to Fix It",
"text": """A double deduction — where the same amount is charged to your account twice for a single purchase — is rare but does happen, particularly when customers retry a failed payment before the first attempt has been fully resolved. Understanding why it happens and how to resolve it efficiently protects your money.

Double deductions most commonly occur in the following scenario: you click "Pay Now" and the payment appears to fail (the page shows an error or times out). You click "Pay Now" again or refresh and try again. The first payment, which appeared to have failed, actually succeeded at the bank level but the success confirmation was not returned to the website due to a network timeout. The second payment also succeeds, resulting in two charges for one order.

On your bank statement, you may see two identical charges from the same merchant at approximately the same timestamp. Alternatively, you may see one completed charge and one pending authorisation hold. The pending hold typically reverses within 5 to 7 business days without any action on your part. The completed charge that matches a placed order is the legitimate transaction.

The first step in resolving a double deduction is to identify how many orders were actually placed. Log in to Your Orders (Amazon), My Orders (Flipkart), or Purchase History (eBay) and count the orders matching the transaction. If two orders were placed, you can cancel one through the standard cancellation process and receive a full refund. If only one order was placed but two charges appear, you have a genuine double deduction that needs to be reported.

Report genuine double deductions to the e-commerce platform first. Provide your order ID, the deducted amounts, dates, and bank reference numbers (RRN) for each transaction. Most platforms can identify and refund the duplicate charge within 24 to 48 hours. Keep your bank statement screenshot as documentation throughout this process.

If the platform is slow to respond or unresponsive, contact your bank and file a dispute for the duplicate charge. Banks have a charge dispute process that investigates duplicate transactions. Be aware that filing a bank dispute while the platform is also investigating can complicate the process — the bank may place a hold on both transactions while investigating. Coordinate your approach: use the platform's resolution process first, and escalate to the bank only if the platform does not resolve within 5 to 7 business days."""
},

{
"topic": "payment_failures",
"source": "general/emi-failure",
"title": "EMI Payment Failures on E-commerce Platforms",
"text": """Equated Monthly Instalment (EMI) options are available on most major e-commerce platforms in India and are popular for large purchases. EMI payment failures and EMI-related issues have unique characteristics that differ from standard payment failures.

There are two types of EMI on e-commerce platforms: bank EMI (where your bank converts a full credit card charge into monthly instalments) and no-cost EMI (where the seller or platform subsidises the interest so you pay only the product price divided equally over the EMI tenure). Understanding which type applies to your purchase affects how failures are resolved.

Bank EMI failures during checkout occur when the bank's EMI processing system cannot validate your card for the requested EMI plan. Common reasons include: your credit card is not eligible for the specific EMI tenure offered (some banks support 3, 6, 9, 12 months differently), your card does not meet the minimum outstanding limit requirement for EMI conversion, or the bank's EMI system is temporarily unavailable.

If EMI payment fails, try a different EMI tenure. Banks that do not support a 12-month tenure may support 6 months. If the issue persists with all tenures, switch to a full payment method and contact your bank afterwards to request a post-purchase EMI conversion, which many banks offer for recent large transactions. Contact your bank's credit card customer service for post-purchase EMI eligibility.

No-cost EMI failures on Amazon, Flipkart, and other platforms can occur if the seller is not participating in the current no-cost EMI promotion for that specific product. No-cost EMI availability is shown on the product listing page. If no-cost EMI has disappeared from a listing, it may have been removed since you last viewed it. Standard EMI with bank interest may still be available.

EMI cancellations and refunds require the bank to dissolve the EMI plan. If you cancel an order or return a product for which an EMI was set up, the bank receives a refund for the full amount from the platform and then reverses the EMI plan — cancelling all future instalments and crediting any already-paid instalments back to your card. The bank handles this process independently and may take 5 to 10 business days to fully reflect the reversal. The interest charges already paid on completed EMI instalments may or may not be refunded depending on the bank's policy."""
},

# ════════════════════════════════════════════════════════════════
# TOPIC 6 — DAMAGED ITEMS  (35 articles)
# ════════════════════════════════════════════════════════════════

{
"topic": "damaged_items",
"source": "amazon/damaged-report-process",
"title": "Reporting a Damaged Item on Amazon — Complete Process",
"text": """Receiving a damaged item from Amazon is disappointing, but the resolution process is straightforward when followed correctly. Amazon's policy for damaged items is clear: you are entitled to a free replacement or full refund, and the return of the damaged item is handled by Amazon with a free prepaid pickup. Here is the step-by-step process.

Start by documenting the damage immediately upon opening the package. Take clear, well-lit photographs of the damaged item from multiple angles. If the outer packaging was also damaged, photograph that separately. Include a photograph with the shipping label visible to establish the connection between the damage and this specific order. Video is also valuable for demonstrating defects like intermittent power failures or distorted displays.

Log in to Amazon, go to Your Orders, find the affected order, and click Return or Replace Items. Select the damaged item and choose the appropriate reason: "Item arrived damaged" for physical damage to the product, "Item defective or doesn't work" for functional defects that may not be visible, or "Wrong item was sent" if a completely different product was delivered.

Amazon will present you with two options: Replace or Refund. If you choose Replace, Amazon will dispatch a new unit and arrange for the collection of the damaged one. If you choose Refund, Amazon will initiate the refund after the damaged item is returned. For most customers, replacement is the faster option — you get a working product sooner and the logistics are handled by Amazon.

After selecting your preference, schedule the pickup. Amazon's pickup system shows available date slots at your address. A delivery agent will arrive with a prepaid return label. Have the damaged item packaged (in its original box with all accessories, if possible) before the agent arrives. If the item is too damaged to be packaged in its original box, any sturdy packaging is acceptable for damaged item returns.

Amazon's investigation for damaged items usually accepts claims without question for accounts with good order history. For unusual claims — for example, repeated damage reports, high-value items, or claims without photographic evidence — Amazon may request additional information before processing the replacement or refund. Always include photographs in your damage report even if they are not explicitly requested, as they significantly speed up the review process."""
},

{
"topic": "damaged_items",
"source": "amazon/screen-damage",
"title": "Amazon Delivered Item with Cracked or Damaged Screen",
"text": """Screen damage is one of the most common and impactful forms of product damage. Whether you received a phone, tablet, laptop, television, or monitor with a cracked or damaged screen, the resolution process on Amazon is specific to this type of damage.

First, verify that the screen damage was present at the time of delivery — not caused by handling after receipt. Check the outer packaging for signs of impact damage (dents, crushed corners, evidence of dropping). If the packaging shows corresponding damage, it strongly supports a transit damage claim. If the packaging is intact, the damage may have occurred during manufacturing (rare but possible) or it could be a pre-existing condition with the unit.

Photograph the screen damage prominently in your report. For displays, take photographs showing the full extent of the damage — cracks, dead pixels, backlight bleeding, or discolouration — in both powered-off and powered-on states. A powered-on photograph clearly shows the functional impact of the damage. Include a close-up photograph that captures the extent and pattern of any cracks.

Report the damage within 7 days of delivery for electronics (Amazon's electronics return window). Waiting beyond 7 days risks the return being declined, as Amazon's system cannot determine whether the damage was present at delivery or occurred later. If you discover screen damage after 7 days, contact Amazon customer service directly — while the standard window has passed, Amazon has discretion to accept claims with compelling evidence and good account history.

For smartphones specifically, Amazon may require the device's IMEI number during the claim process. This verifies that the device being returned matches the device that was shipped. Have the IMEI ready — it is usually on a sticker in the original box and can also be found by dialling *#06# on most phones (though a cracked screen may prevent this).

Manufacturer warranty does not cover accidental screen damage. A cracked screen is considered accidental damage (impact or drop) by most manufacturers, even if the impact occurred during transit. Amazon's return policy — not the manufacturer's warranty — is your correct avenue for transit damage claims. Once the 10-day return window for non-electronics (7-day for electronics) has closed, your only recourse for screen damage (unless it was an inherent defect) is through the manufacturer's paid repair service."""
},

{
"topic": "damaged_items",
"source": "flipkart/open-box-delivery",
"title": "Flipkart Open Box Delivery — How It Works and Your Rights",
"text": """Flipkart's Open Box Delivery is a service offered for high-value electronics and appliances that allows the delivery agent to open the product packaging in the customer's presence at the time of delivery. This feature is designed to allow customers to verify the product's condition before accepting delivery, thereby preventing disputes about damage or wrong products.

When Open Box Delivery is available for your order, it will be noted on the order detail page and in the delivery notification. The delivery agent is trained to open the package carefully in a way that does not damage the product or packaging. You should inspect the product thoroughly while the agent is present — check for physical damage, verify the model number matches your order, confirm all accessories are present, and test basic functionality if possible (power on, touch screen response, speaker audio).

If you find an issue during Open Box inspection, you have the right to reject the delivery on the spot. Tell the agent your reason for rejection (damage, wrong product, missing accessories). The agent will scan the package as "rejected at delivery" and return it to the hub. Flipkart will initiate a replacement or refund automatically once the package is scanned back into the system, typically within 2 to 4 business days.

If Open Box Delivery is not available for your product but you want the same protection, a best practice is to inspect the outer packaging thoroughly before the delivery agent leaves, and to take a timestamped video of yourself opening the package immediately after the agent departs. This video serves as evidence for any subsequent damage claims.

For products delivered without Open Box service where damage is discovered after the agent has left, the standard damaged item report process applies — go to My Orders, report the damage, and upload your photographs and video as evidence. The 48-hour reporting window for large appliances and the 7-day window for electronics apply. Reporting within these windows with clear documentation results in the best outcomes.

Flipkart monitors Open Box Delivery rejection rates. Locations with high rejection rates may see operational adjustments including more careful packing, additional quality checks at the warehouse, or packaging upgrades. If you rejected a delivery and did not report the specific issue clearly, contact Flipkart support to add the details to the rejection record — this helps improve the overall system."""
},

{
"topic": "damaged_items",
"source": "ebay/item-not-as-described",
"title": "eBay Item Not As Described — Claims Process and Evidence",
"text": """The "Item Not As Described" (INAD) case on eBay is the formal mechanism for resolving disputes where the received item differs significantly from the seller's listing. This category covers physical damage not mentioned in the listing, wrong items sent, counterfeit goods, items missing key components described in the listing, and items in significantly worse condition than stated.

To open an INAD case on eBay, go to Purchase History, find the order, click More Actions, and select Return This Item. When selecting the return reason, choose one of the "Item Not As Described" options rather than "Changed My Mind" options. The distinction is critical — "Item Not As Described" triggers eBay's Money Back Guarantee, while "Changed My Mind" is subject to the seller's return policy (and may not result in a full refund if the seller doesn't accept returns).

Evidence is the most important part of an INAD case. Take photographs that clearly show the discrepancy between what was advertised and what you received. Compare specific listing claims with what you received. For example, if the listing said "no scratches" and the item has visible scratches, photograph them clearly. If the listing described a sealed item but you received an opened one, photograph the broken seal. Specific, visual evidence accelerates case resolution.

After opening the case, the seller has 3 business days to respond. The seller's options are to issue a full refund, offer a partial refund, or ask for the item to be returned before issuing a refund. If the seller asks for a return and the INAD claim is valid, eBay requires the seller to provide a prepaid return label. You should not have to pay for return shipping when an item was not as described.

eBay aims to resolve INAD cases within 30 days. If the seller is unresponsive or the response is unsatisfactory, escalate to eBay within 3 business days of the seller's response (or 3 days after the response window closes if the seller did not respond). eBay's case managers review both parties' evidence and typically rule in favour of the buyer in clear-cut INAD cases.

After a successful INAD resolution, you can leave appropriate feedback for the seller reflecting your experience. Factual, evidence-based feedback — noting the specific inaccuracy in the listing — is most helpful to future buyers. Avoid inflammatory language, as eBay can remove feedback that violates its feedback policy regardless of whether the underlying complaint was valid."""
},

{
"topic": "damaged_items",
"source": "general/transit-damage-prevention",
"title": "Understanding Transit Damage — Prevention and Seller Responsibility",
"text": """Transit damage — damage that occurs during the journey from the warehouse to your doorstep — is an inherent risk in e-commerce logistics. While platform policies protect buyers from the financial consequences of transit damage, understanding how it occurs and what sellers and platforms do to prevent it provides useful context for resolving disputes.

Most transit damage occurs during sorting and loading operations at logistics hubs. Packages travel on conveyor belts, are stacked in delivery vehicles, and may be dropped, compressed, or exposed to moisture during their journey. The outer packaging is designed to absorb the impact of typical handling, but extreme handling — such as heavy packages stacked on lighter ones, or packages dropped from height — can exceed the packaging's protective capacity.

Items most vulnerable to transit damage include: fragile electronics (screens, circuit boards), glass items, ceramics, and liquid-containing products; items with protruding components that can be snapped during handling; large and heavy items where the weight itself becomes a damage risk during stacking; and items that are only marginally larger than the product inside, leaving little room for cushioning.

Sellers are responsible for packaging items adequately for transit. Amazon, for example, has detailed Frustration-Free Packaging Guidelines that define the minimum packaging standards for sellers. Sellers who consistently receive transit damage complaints are required to improve their packaging. If you receive an item that appears to have been inadequately packaged — for example, a fragile item wrapped only in a single layer of tissue paper with no protective padding — include this observation in your damage report, as it may indicate a seller packaging issue rather than an unusual handling event.

When you receive a damaged item, the question of who bears financial responsibility is irrelevant from your perspective — the platform's buyer protection covers you regardless of whether the damage was caused by the seller's poor packaging or the carrier's rough handling. What matters for your resolution is reporting the damage promptly with good evidence and following the platform's return process.

For very high-value purchases, consider requesting additional insurance from the seller at the time of purchase (particularly on eBay, where sellers can add shipping insurance to their listings). Insurance covers loss and damage during transit and provides an additional recovery pathway beyond the standard buyer protection mechanisms."""
},

# ════════════════════════════════════════════════════════════════
# TOPIC 7 — PRODUCT REPLACEMENT  (30 articles)
# ════════════════════════════════════════════════════════════════

{
"topic": "product_replacement",
"source": "amazon/replacement-process",
"title": "Amazon Product Replacement — Complete Process Guide",
"text": """Amazon offers free product replacements for items that arrive damaged, defective, or not as described. The replacement process is handled within the same return management system, with the key difference being that instead of a refund, a new unit is dispatched. Here is everything you need to know about Amazon's replacement process.

When you initiate a return for a damaged or defective item, Amazon's system presents you with two options: Replace or Refund. Select Replace to receive a new unit of the same product. After selecting Replace, Amazon will check current inventory for the exact product you ordered. If the identical product is in stock in your pin code's servicing fulfilment centre, a replacement shipment is created immediately.

The replacement unit is typically dispatched within 2 to 3 business days of the replacement request. For Amazon Prime customers, replacement dispatches are often accelerated, sometimes happening the next business day. You will receive an email with the replacement order number and a new tracking link. The replacement order is separate from your original order in Your Orders — look for it under a "Replacement for Order XXXX" label.

The return of the original item occurs simultaneously with the replacement delivery. Amazon schedules a pickup of the defective item at the same address. In some cases, the pickup is arranged to coincide with the replacement delivery — the delivery agent brings the new item and takes the old one in the same visit. In other cases, the pickup is scheduled separately within 3 to 5 business days of the replacement request.

If a replacement is not available — because the product is out of stock, discontinued, or a marketplace seller item without readily available replacement stock — Amazon will offer a refund instead. The refund in this case follows the standard refund timeline. Amazon does not substitute replacement with a different model or product variant; if the exact product is unavailable, a refund is the only alternative.

For high-value electronics replacements, Amazon may require the return of the original item before dispatching the replacement. This "return first" policy is applied when the item value exceeds a certain threshold and protects Amazon from fraudulent replacement claims. If you are asked to return first, the replacement will be dispatched within 2 to 3 business days of Amazon receiving your return."""
},

{
"topic": "product_replacement",
"source": "amazon/warranty-replacement",
"title": "Amazon Warranty Replacement vs. Return Replacement",
"text": """Customers often confuse two types of replacements available for defective products: the return-window replacement (which is Amazon's direct return policy) and the manufacturer's warranty replacement. Understanding the difference helps you use the right pathway and know what to expect.

Return-window replacement is Amazon's direct responsibility and applies within the return window: 10 days for most products, 7 days for electronics. During this window, Amazon itself handles the replacement or refund with no involvement from the manufacturer. The process is quick (2 to 3 business days for the replacement to ship) and Amazon bears the cost. This is the preferred pathway for defects discovered shortly after delivery.

Manufacturer warranty replacement applies after the return window has closed. Most electronics come with a 1-year manufacturer's warranty (some brands offer extended warranties). Warranty claims are made directly with the manufacturer, not Amazon. You need the purchase invoice as proof of purchase — download it from Your Orders before the warranty period becomes relevant, or request it from Amazon customer service. The manufacturer will direct you to an authorised service centre.

Warranty repair vs. replacement depends on the manufacturer's policy and the nature of the defect. Some manufacturers offer complete unit replacement for defects reported within 30 to 90 days of purchase (even after Amazon's return window). Others repair the unit at their service centre. Premium brands in the smartphone and laptop segments are more likely to replace units; budget brands are more likely to repair.

Amazon's Extended Warranty programme — available for purchase at checkout for many electronics — is distinct from both the return window replacement and the manufacturer's warranty. Extended warranty coverage typically mirrors the manufacturer's warranty for the first year and then extends protection for 1 to 2 additional years. Claims under Amazon's extended warranty are managed by a third-party warranty administrator and follow their specific claims process.

For software defects — issues with a device's operating system or firmware — manufacturers typically resolve these through software updates or reflashing the firmware at a service centre. These are warranty claims, not return-window replacements, unless the software issue was present from the moment of first use and prevents basic functionality."""
},

{
"topic": "product_replacement",
"source": "flipkart/replacement-appliances",
"title": "Flipkart Large Appliance Replacement — Detailed Process",
"text": """Getting a replacement for a large appliance on Flipkart involves a more complex process than replacing a small product due to the logistics of handling oversized items, the need for professional installation assessment, and the strict reporting timelines. Here is a complete walkthrough of the process.

The reporting window for large appliance damage or defects on Flipkart is just 48 hours from delivery. This short window exists because appliances are expected to be installed and tested promptly. If you miss this window, replacements are generally not available through Flipkart's return system, and you must contact the manufacturer's warranty service instead.

Within the 48-hour window, report the issue through My Orders by selecting the appliance and choosing Report Issue or Request Replacement. Describe the defect specifically: "Washing machine drum not spinning," "Refrigerator not cooling," "AC unit making unusual noise," or "TV has vertical colour lines." Specific descriptions help Flipkart's quality team prepare for the technician visit.

Flipkart dispatches a certified appliance technician to your home within 3 to 5 business days of the replacement request. The technician assesses the defect, verifies that it is a manufacturing issue (as opposed to installation error or user damage), and documents their findings. If the technician confirms a manufacturing defect, Flipkart proceeds with the replacement. If no defect is found or the defect is attributed to installation error or misuse, the replacement may not be approved.

Replacement delivery for large appliances is scheduled as a dedicated delivery event. Flipkart coordinates the simultaneous delivery of the new appliance and collection of the defective one. A team of delivery agents handles the logistics of carrying out the large items. New installation, if required, is typically scheduled separately by the installation partner.

If a like-for-like replacement is not in stock, Flipkart may offer a replacement with the nearest available model (same brand, similar specifications) or a full refund. Accept any offer in writing through the app's messaging system so there is a record of the agreed resolution. Verbal agreements with delivery agents or technicians are not binding."""
},

{
"topic": "product_replacement",
"source": "ebay/replacement-options",
"title": "Getting a Replacement on eBay — Understanding Your Options",
"text": """eBay's marketplace structure means that product replacements work differently than on platforms like Amazon or Flipkart, where a centralised returns system handles all replacements. On eBay, replacements depend entirely on the individual seller's willingness and stock availability, backed by eBay's buyer protection policies.

The first step in seeking a replacement on eBay is to contact the seller directly through eBay Messages. Explain the issue clearly and request a replacement. Many sellers — particularly business sellers and Top Rated Sellers — will offer a replacement proactively to maintain their feedback score. A direct, polite message requesting a replacement often results in a faster resolution than opening a formal case.

If the seller agrees to send a replacement, the typical process is: you return the defective item (seller provides prepaid label for seller-error cases) and the seller ships the replacement once they receive the return. Some sellers ship the replacement first before receiving the return for trusted buyers or low-value items. Get any replacement agreement confirmed in writing through eBay Messages.

If the seller declines to replace the item or does not respond within 3 business days, open a return case through the Resolution Centre selecting "Item Not As Described" if the item was defective or different from the listing. eBay's Money Back Guarantee applies in this case. Note that eBay's guarantee results in a refund, not necessarily a replacement — eBay does not force sellers to ship replacement products. To get a replacement item, you would need to purchase the same listing again after receiving your refund.

Sellers who listed an item as "new" and shipped a defective product are in violation of eBay's seller policies. Beyond the individual resolution, you can report the seller's listing to eBay for investigation. eBay may take action against sellers who repeatedly ship defective items, including suspending their selling privileges.

For used items sold "as is" on eBay, replacement options are more limited. "As is" sales typically mean no returns accepted and no defect guarantees beyond what was explicitly stated in the listing. eBay's Money Back Guarantee still applies if the item did not match the listed description, but it does not apply if the defect was disclosed in the listing or if the item is in the described condition."""
},

# ════════════════════════════════════════════════════════════════
# TOPIC 8 — ACCOUNT ISSUES  (35 articles)
# ════════════════════════════════════════════════════════════════

{
"topic": "account_issues",
"source": "amazon/account-locked",
"title": "Amazon Account Locked or Suspended — Causes and Resolution",
"text": """An Amazon account can be locked, temporarily suspended, or permanently closed for various reasons. Understanding why this happens and how to respond appropriately gives you the best chance of having your account restored promptly.

Temporary account locks are the most common and least serious. Amazon's security system may lock your account if it detects unusual login activity — for example, sign-in attempts from multiple countries in a short period, or failed login attempts that trigger a brute-force protection mechanism. You will typically receive an email asking you to verify your identity. Follow the link in the email, verify via OTP, and reset your password. The lock is usually lifted within minutes of successful verification.

Account suspensions are more serious and typically occur due to policy violations. Common reasons include: placing orders on behalf of others for resale (Amazon prohibits commercial resale of products purchased on Amazon.in without prior authorisation), receiving too many A-to-Z Guarantee claims or return requests (which may indicate fraud), linking multiple accounts (Amazon only allows one account per person — having a second account detected causes both to be flagged), and payment fraud indicators.

If you receive an account suspension notice, read it carefully. The email will contain specific reason codes or explanations. Respond professionally and factually to the appeal address provided. Do not make emotional appeals; Amazon's account review team responds best to factual, specific information. If you believe the suspension is in error, provide documentation that refutes the stated reason. For example, if suspended for linking to another account, explain the situation clearly (e.g., a family member uses the same device).

Account appeals for Amazon India are reviewed by the Seller Performance or Customer Trust teams. Response times vary — initial responses may come within 24 to 48 hours, but full reinstatement investigations can take 5 to 10 business days. Check your registered email daily and respond promptly to any requests for additional information.

For permanently closed accounts (rare and reserved for serious violations), the order history and review history are inaccessible. If you believe the closure was in error, use Amazon's Contact Us page with a different email address to reach the account review team. Bringing your case to local consumer forums or regulatory authorities (like the Consumer Disputes Redressal Commission in India) is an option of last resort for genuinely wrongful closures."""
},

{
"topic": "account_issues",
"source": "amazon/2fa-issues",
"title": "Amazon Two-Factor Authentication Issues — Login Help",
"text": """Two-factor authentication (2FA) adds a critical layer of security to your Amazon account, but it can also create login difficulties when your authentication method is no longer available. Here is how to handle common 2FA issues on Amazon.

Amazon offers several 2FA methods: SMS OTP (one-time password) to your registered mobile number, email OTP to your registered email address, and authenticator app verification (using apps like Google Authenticator or Authy). The method used depends on how you set up your security settings.

OTP not received via SMS is the most common 2FA issue. Before troubleshooting, wait 2 minutes — SMS delivery can be delayed, particularly on busy networks. If the OTP still hasn't arrived, check: mobile signal strength (poor signal prevents SMS delivery), whether DND (Do Not Disturb) is active on your number (DND can block certain SMS categories), whether your number is still active and correctly registered to your Amazon account, and whether international SMS is enabled if you are abroad.

If your registered mobile number is no longer accessible — you changed your number, lost your phone, or the SIM is inactive — you can receive the OTP to your registered email instead. On the OTP entry page, look for "Try another way" or "Use email instead" and choose that option. The OTP will be sent to your registered email address.

If you no longer have access to either your registered mobile or email, contacting Amazon customer service is required to regain access. Be prepared to verify your identity through alternative means: Amazon may ask for recent order details, registered payment method information, or may send a physical letter to your registered address. This process can take several days for high-security verification.

Authenticator app issues typically arise after changing phones or reinstalling the app. Google Authenticator does not back up codes by default, meaning if you switch phones without first exporting your codes, you lose access. Authy and similar apps that offer cloud backup are more resilient. If you are locked out due to authenticator app loss, the email or SMS backup method can be used to log in and then re-enroll your new authenticator app. For future security, store your 2FA backup codes in a safe location when you first set up 2FA."""
},

{
"topic": "account_issues",
"source": "amazon/unauthorised-orders",
"title": "Unauthorised Orders on Amazon — What to Do Immediately",
"text": """Discovering unauthorised orders on your Amazon account is alarming and requires immediate, structured action to secure your account and initiate refunds or cancellations for orders you did not place. Here is exactly what to do.

Immediately change your Amazon password. Go to Your Account, select Login and Security, then Edit next to Password. Create a strong, unique password that you do not use on any other website. This is the single most important step — changing your password revokes access to anyone currently logged in with your old credentials.

Next, review all active login sessions. In Login and Security, find "Where You're Signed In" and sign out of all devices. This logs out any unauthorised user from all devices simultaneously. Then, review the saved payment methods in Your Account under Payment Methods. Remove any payment method that you did not add or that appears suspicious.

Review recent orders going back 30 days. Identify all orders you did not place. For each unauthorised order: if the order has not shipped, cancel it immediately through Your Orders. If it has shipped but not delivered, contact Amazon customer service to intercept if possible. If it has been delivered, contact Amazon customer service to report it as unauthorised and request a refund.

When reporting unauthorised orders to Amazon, use the Contact Us option and select "Account security issue" or "Unauthorised order." Provide the order IDs and amounts for all suspicious orders. Amazon's fraud team will investigate and issue refunds for orders that were clearly placed without your authorisation. The investigation may take 24 to 48 hours.

After securing your Amazon account, check whether the same password or email combination was used on other services and change those too. Unauthorised access is often the result of credentials leaked from a data breach on another service. Use a password manager to create and store unique passwords for each service. Enable 2FA on Amazon immediately after securing the account if it was not previously enabled. This prevents future unauthorised access even if credentials are stolen."""
},

{
"topic": "account_issues",
"source": "flipkart/account-verification",
"title": "Flipkart Account Verification — KYC and Identity Issues",
"text": """Flipkart may require account verification (KYC — Know Your Customer) for certain activities, including activating Flipkart Pay Later, accessing seller features, claiming high-value prizes or credits, or in response to fraud detection flags on an account. Understanding what verification is required and how to complete it avoids delays in accessing these features.

Basic Flipkart account verification requires a valid email address and mobile number. These are verified through OTP at the time of registration. Most standard buying activities on Flipkart do not require any further verification beyond these basics. You do not need to submit government ID to shop on Flipkart for normal purchases.

Flipkart Pay Later KYC is more rigorous. To activate Pay Later, Flipkart requires you to submit an Aadhaar number for e-KYC verification. The Aadhaar-based OTP verification process is done in partnership with UIDAI and typically completes in minutes. Pay Later is a credit facility regulated by the RBI, which mandates KYC for all credit accounts. If your e-KYC fails — for example, because the mobile number linked to Aadhaar is different from your Flipkart mobile number — you may need to visit a KYC point or submit a physical KYC form.

If your Flipkart account has been flagged for suspicious activity — such as unusual purchase patterns, payment disputes, or return abuse — Flipkart may restrict your account and request identity verification before restoring full access. This typically involves submitting a copy of your Aadhaar, PAN, or passport through the Help Centre. The document is reviewed by Flipkart's trust and safety team within 3 to 5 business days.

Flipkart seller accounts require more extensive verification including business registration documents (GST certificate, business PAN), bank account details, and address proof. Seller account verification takes 7 to 14 business days for initial approval. Re-verification may be required annually or upon significant account changes.

If you are unable to complete the required verification — for example, due to a discrepancy in your Aadhaar details or an expired document — contact Flipkart support through the Help Centre. Provide details of the specific verification step you are stuck on and the nature of the discrepancy. Flipkart support can escalate your case to the verification team for manual review."""
},

{
"topic": "account_issues",
"source": "ebay/account-hacked",
"title": "eBay Account Compromised — Recovery and Prevention",
"text": """An eBay account that has been hacked or compromised requires immediate action across multiple fronts: securing the account, assessing the damage, and reporting the incident to eBay. Acting quickly minimises the potential financial and reputational impact.

Signs of a compromised eBay account include: emails about listings or sales you did not create, purchases in Purchase History that you did not make, messages from buyers or sellers you did not contact, password change notifications you did not initiate, or notification that your payment method was used without authorisation.

If you still have access to your account, change your password immediately. Use the Forgot Password link on the sign-in page to reset via email if your password was already changed by the attacker. After regaining access, sign out of all sessions through My eBay, Account, Sign In and Security, End All Sessions. This terminates any active sessions the attacker may have.

Review all listings the hacker may have created in your name. Go to Selling Activity and remove any fraudulent listings immediately. Fraudulent listings placed by hackers often advertise high-value goods (electronics, gift cards) at low prices as bait for other eBay users. Leaving these listings up harms other buyers and may result in eBay taking action against your account even after recovery.

Report the compromise to eBay through the Help and Contact page, selecting "Compromised Account" as the issue. eBay's Trust and Safety team will flag your account for investigation. They can help remove fraudulent listings, reverse unauthorised transactions, and send notifications to any users who interacted with your account during the compromise. Include a timeline of when you first noticed suspicious activity.

For unauthorised purchases made from your account, contact eBay customer service with the order IDs. eBay can reverse these transactions and contact the sellers involved. For listings that resulted in completed sales during the compromise, eBay mediates between you, the buyer, and the seller to ensure the buyer receives a refund and you are not held financially liable for sales you did not authorise.

Going forward, enable 2FA on your eBay account immediately after recovery. Use a strong, unique password and consider a password manager. eBay also allows you to set up security questions as an additional verification layer. Monitor your eBay and linked PayPal account activity regularly for unusual transactions."""
},

# ════════════════════════════════════════════════════════════════
# TOPIC 9 — TRACKING AND SHIPPING  (20 articles)
# ════════════════════════════════════════════════════════════════

{
"topic": "tracking_shipping",
"source": "amazon/tracking-guide",
"title": "Amazon Order Tracking — Complete Guide",
"text": """Amazon's order tracking system provides real-time updates on the status of your shipment from the moment it leaves the warehouse to the moment it is delivered to your door. Understanding how to read and interpret tracking information helps you stay informed and respond quickly if issues arise.

Amazon tracking is accessible in multiple ways: through Your Orders on the Amazon website, through the Amazon mobile app (which supports push notifications for delivery updates), and through the carrier's own tracking system using the tracking number provided in your shipment confirmation email. For Amazon-fulfilled orders, the Amazon tracking page is usually the most comprehensive and up-to-date source.

Amazon uses a variety of carriers depending on your location and the size of your order: Amazon Logistics (Amazon's own delivery network), Blue Dart, Delhivery, Ekart, DTDC, India Post, and others. Amazon Logistics provides the most granular tracking, including real-time driver location on a map, delivery photo confirmation, and one-hour delivery windows as the driver approaches. Third-party carriers provide more traditional tracking with hub-based scan events.

Tracking statuses and what they mean: "Order placed" — your order is confirmed and being prepared. "Preparing for shipment" — items are being picked and packed in the warehouse. "Shipped" — the order has left the warehouse and is with the carrier. "Out for delivery" — the package is on the delivery vehicle heading to your address today. "Delivery attempted" — the carrier tried to deliver but could not. "Delivered" — the carrier has marked the package as delivered.

Amazon Logistics map tracking is available for the final leg of delivery when an Amazon delivery associate is en route to your address. The Amazon app shows a live map with the associate's current location, number of stops before yours, and an estimated delivery time window of 1 to 2 hours. This feature is available in most major cities and metro areas. In areas served by third-party couriers, the map tracking is not available.

Tracking discrepancies — situations where the status says "Delivered" but you haven't received the package — should be reported within 30 days using the "Problem with this order" option. Amazon can request GPS data from the delivery associate and photo proof of delivery to investigate. Most discrepancies are resolved within 24 to 48 hours."""
},

{
"topic": "tracking_shipping",
"source": "general/shipping-carriers",
"title": "Understanding E-commerce Shipping Carriers in India",
"text": """E-commerce deliveries in India use a diverse network of shipping carriers. Each carrier has different service levels, tracking capabilities, and delivery performance characteristics. Knowing which carrier is handling your shipment helps you use the right tracking resources and set appropriate expectations.

Amazon Logistics (AMZL) is Amazon's proprietary last-mile delivery network, operating in most tier-1 and tier-2 Indian cities. AMZL provides the most advanced tracking features including real-time map tracking and delivery photos. AMZL operates 7 days a week and has among the highest on-time delivery rates of any carrier in India. For remote areas not covered by AMZL, Amazon uses Blue Dart, Delhivery, or India Post.

Blue Dart is a premium courier service in India, a subsidiary of DHL, known for reliable express delivery. Blue Dart provides detailed tracking through its website (bluedart.com) and app using the Air Waybill (AWB) number. Blue Dart's signature service requires someone to be present at delivery and sign for the package — this is common for high-value shipments. Blue Dart delivers on business days (Monday–Friday) in most locations, with Saturday delivery available in some metros.

Delhivery is one of India's largest logistics companies, serving both e-commerce shipments and B2B freight. Delhivery tracking is available at delhivery.com. Delhivery's last-mile delivery is competitive in metro areas but can be slower in tier-3 cities and rural areas. Delhivery's customer service can be reached for package inquiries through their website's tracking page.

Ekart is Flipkart's proprietary logistics subsidiary. For Flipkart orders, Ekart handles most deliveries. Tracking is integrated into the Flipkart app. For standalone tracking, visit ekartlogistics.com with the Ekart tracking ID found in your Flipkart order.

India Post EMS (Speed Post) and e-Commerce parcel services handle both domestic and international shipments. Tracking is available at indiapost.gov.in. India Post is the only carrier reaching every pin code in India, making it essential for deliveries to remote and rural areas where private couriers do not operate. Speed Post's tracking can have delays in updating, particularly for rural last-mile segments."""
},

{
"topic": "tracking_shipping",
"source": "general/estimated-delivery-date",
"title": "How Estimated Delivery Dates Are Calculated — What to Expect",
"text": """Estimated delivery dates shown during e-commerce checkout are calculated using algorithms that account for multiple variables. Understanding how these dates are generated helps you interpret them correctly and plan accordingly.

The delivery date calculation begins with the seller's location and current inventory status. If the item is in-stock and ready to ship from a fulfilment centre near you, the processing time is short — typically same-day dispatch for orders placed before a certain cut-off time (usually 2 PM for Prime same-day, 6 PM for next-day). If the item needs to be transferred from a different warehouse, this adds 1 to 2 days.

Transit time is calculated based on the historical average transit time from the origin warehouse to your specific pin code. This data is continuously updated based on actual delivery performance. Factors that affect transit time include: the carrier assigned to your pin code, the number of sorting hubs the package must pass through, and the specific geographic distance and infrastructure quality.

Prime delivery promises are based on a higher-confidence calculation than standard delivery estimates. Amazon Prime's guaranteed delivery dates are backed by service level agreements with carriers and have compensation mechanisms if they are not met. Standard delivery estimates are more conservative, representing the typical delivery window with a buffer for potential delays.

Calendar adjustments include national and regional public holidays. E-commerce platforms' delivery date calculations account for major national holidays (Republic Day, Independence Day, Diwali, Christmas). However, regional holidays (state-specific bank holidays, local festivals) may not always be captured in the estimate, particularly in areas served by smaller regional carriers.

During peak sale periods — Big Billion Days (Flipkart), Great Indian Festival (Amazon), Republic Day sales, and festive seasons — delivery estimates are automatically extended to reflect the higher volume. Estimated delivery dates shown during these periods tend to be 1 to 3 days longer than normal. Actual deliveries during sales often arrive within the normal timeline as platforms scale up their logistics, but the estimates are conservative to manage expectations."""
},

# ════════════════════════════════════════════════════════════════
# TOPIC 10 — SELLER DISPUTES  (15 articles)
# ════════════════════════════════════════════════════════════════

{
"topic": "seller_disputes",
"source": "amazon/atoz-guarantee",
"title": "Amazon A-to-Z Guarantee — Complete Buyer Protection Guide",
"text": """Amazon's A-to-Z Guarantee protects buyers when they purchase items from third-party sellers on Amazon Marketplace. While Amazon-fulfilled items are fully within Amazon's direct control, marketplace items involve independent sellers, and the A-to-Z Guarantee is the safety net that ensures buyers are protected regardless of individual seller behaviour.

The A-to-Z Guarantee covers two broad categories: items not received and items that are materially different from what was advertised. For items not received, the guarantee covers cases where the item was not delivered within 3 days of the maximum estimated delivery date. For items materially different, this includes items that were damaged, defective, significantly different from the description, or missing parts not disclosed in the listing.

Before filing an A-to-Z Guarantee claim, Amazon requires you to first contact the seller. Go to Your Orders, find the order, and click Contact Seller. Allow the seller 2 business days to respond and resolve the issue. Most legitimate sellers will address issues promptly to avoid an A-to-Z claim, which negatively impacts their seller metrics. If the seller does not respond or does not resolve the issue satisfactorily, you can proceed with the claim.

To file an A-to-Z claim: go to Your Orders, find the order, click Problem with Order, choose the appropriate reason, and then click Claim Under A-to-Z Guarantee. The claim submission form asks for a description of the issue and any supporting evidence (photographs, communication with seller). Submit the claim along with your evidence.

Amazon reviews A-to-Z claims and typically responds within 48 hours. For straightforward cases — for example, a seller who has stopped responding and the tracking shows no movement — Amazon often rules quickly in the buyer's favour. Complex cases involving conflicting evidence may take up to 1 week. If Amazon rules in your favour, the refund is issued within 3 to 5 business days to your original payment method.

Sellers who accumulate A-to-Z claims risk having their selling privileges suspended. A high claim rate signals to Amazon that the seller is not operating to the platform's standards. This incentive structure means that most professional sellers take A-to-Z claims very seriously and resolve customer issues before they escalate to this level."""
},

{
"topic": "seller_disputes",
"source": "ebay/seller-non-responsive",
"title": "eBay Seller Not Responding — Escalation Guide",
"text": """An unresponsive seller on eBay is unfortunately a common frustration, but eBay's buyer protection system provides clear escalation paths that do not depend on seller cooperation. Here is a structured approach to resolving issues when a seller goes silent.

Start with direct contact through eBay Messages. Send a clear, professional message describing the issue — missing package, damaged item, incorrect item received, or return request — and ask for resolution within 3 business days. Keep the message factual and avoid emotional language. Save all messages in case they become evidence in a formal case.

If the seller does not respond within 3 business days (or if their response is unsatisfactory), open a formal case in eBay's Resolution Centre. Go to My eBay, Help and Contact, Resolution Centre, Report a Problem. Select the relevant issue type (Item Not Received or Item Not As Described). eBay will notify the seller that a formal case has been opened and give them another 3 days to respond.

When eBay notifies a seller that a case has been opened, most sellers respond. The prospect of a negative case outcome — which results in a financial penalty and a defect on their seller account — motivates resolution. If the seller still does not respond to eBay's notification within 3 days, you can ask eBay to step in and decide the case.

eBay's case resolution typically favours buyers in cases of seller non-response. An unresponsive seller in a legitimate dispute signals either abandonment of the account or deliberate evasion of responsibility — neither of which is a valid defence. eBay issues the refund from the seller's account. If the seller's account has insufficient funds, eBay's Money Back Guarantee covers the buyer.

After the case is resolved, leave honest feedback reflecting your experience. An unresponsive seller deserves feedback that warns future buyers. Specific, factual feedback — noting that the item did not arrive and the seller did not respond — is more useful to the community than generic negative ratings. eBay allows sellers to respond to feedback but not remove factually-based negative feedback from legitimate transactions."""
},

{
"topic": "seller_disputes",
"source": "general/counterfeit-products",
"title": "Reporting Counterfeit Products on E-commerce Platforms",
"text": """Counterfeit products — fake or unauthorised replicas of genuine branded goods — are a persistent problem on e-commerce marketplaces. Knowing how to identify counterfeits and report them correctly protects both yourself and other customers from purchasing fake goods.

Identifying counterfeits requires attention to several indicators. Price anomalies are the most obvious red flag — if a product is priced significantly below the typical market price for a genuine item (more than 30-40% below), this warrants scepticism. Packaging quality differences — blurry print, incorrect logos, poor-quality materials — are common in counterfeits. Unusual seller accounts with very few reviews or recently created accounts selling brand-name products are also suspicious.

On Amazon, to report a counterfeit: scroll to the bottom of the product listing page and click "Report incorrect product information" or use the Report a Counterfeit Product option within the seller feedback section. Amazon's counterfeit team investigates reports and can remove listings, take action against sellers, and in serious cases, refer matters to brand owners for legal action. Amazon's Brand Registry programme gives legitimate brand owners tools to proactively identify and remove counterfeit listings.

On Flipkart, counterfeit reports can be filed through the product listing page using the "Report abuse" or "Flag" button. Flipkart's quality monitoring team reviews reports and may request evidence from the reporter. Flipkart also cooperates with brand owners through anti-counterfeiting partnerships to systematically identify and remove fake listings.

On eBay, counterfeit reports can be filed through the "Report this item" link on any listing page. eBay's Verified Rights Owner (VeRO) programme allows brand owners to report and remove listings of counterfeit goods directly. As a buyer who received a counterfeit, open an INAD case (Item Not As Described) and describe the item as counterfeit. eBay's Money Back Guarantee fully covers counterfeit purchases.

If you purchased a counterfeit product, retain the item and all packaging as evidence. Document the specific ways the counterfeit differs from the genuine product. This documentation supports your refund claim and any law enforcement action if the counterfeiting operation is significant."""
},

# ════════════════════════════════════════════════════════════════
# TOPIC 11 — WARRANTY AND SERVICE  (15 articles)
# ════════════════════════════════════════════════════════════════

{
"topic": "warranty_service",
"source": "general/warranty-basics",
"title": "Understanding Product Warranties — Manufacturer vs. Extended",
"text": """Product warranties are legal commitments from manufacturers or sellers to repair, replace, or refund a product that develops defects during the warranty period. For e-commerce purchases, understanding the difference between manufacturer warranties, extended warranties, and implied warranties helps you use the right protection when you need it.

A manufacturer's warranty (also called a limited warranty) is the standard warranty that comes with a product. It is typically 1 year for electronics, 2 years for some premium electronics and appliances, and varies for other product categories. The warranty covers defects in materials and workmanship under normal use conditions. It does not cover accidental damage, water damage (unless the product is rated water-resistant), cosmetic damage, or damage from misuse.

To make a warranty claim, you typically need: the original purchase invoice with the purchase date and seller information (download from Amazon or Flipkart's order history), the product serial number or IMEI, and the defect description. The manufacturer will direct you to an authorised service centre for assessment. Service centres can either repair the product or, if a repair is not feasible, replace it.

Extended warranties are optional additional coverage that extends protection beyond the manufacturer's warranty period. Amazon, Flipkart, and many insurance companies sell extended warranty plans for electronics. These plans add 1 to 2 years of coverage after the manufacturer's warranty expires. Read the extended warranty terms carefully — some only cover breakdowns from internal component failure, while others also cover accidental damage.

Implied warranties are legal protections that exist by law regardless of what the seller or manufacturer states. In India, the Consumer Protection Act 2019 provides that goods must be of merchantable quality and fit for the purpose for which they were sold. Even if a seller says "no warranty" or "sold as is," there are minimum protections for consumers under Indian law that cannot be completely waived away. The Consumer Disputes Redressal Commission (consumer courts) enforces these rights.

Service centre visits for warranty claims can be frustrating, particularly when service centres are busy or parts are unavailable. Most manufacturers provide a service centre locator on their website. Authorised service centres have certified technicians and access to genuine replacement parts. Using unauthorised repair shops typically voids the remaining warranty, so always use authorised centres for warranty-covered repairs."""
},

{
"topic": "warranty_service",
"source": "amazon/extended-warranty",
"title": "Amazon Extended Warranty — How It Works",
"text": """Amazon offers extended warranty plans for eligible electronics at the time of purchase and sometimes as an add-on after purchase. These plans are managed by third-party warranty administrators who handle the claims process. Understanding what is and is not covered by Amazon's extended warranty prevents surprises at claim time.

Amazon's extended warranty plans typically offer 1 or 2 years of additional coverage after the manufacturer's warranty expires. The combined coverage period ranges from 2 to 3 years total for most products. The cost of the warranty plan depends on the product price — typically 5 to 10 percent of the product price for a 1-year extension, and 8 to 15 percent for a 2-year extension.

Coverage typically includes: sudden and unexpected mechanical or electrical failures, defects in materials and workmanship not covered after the manufacturer's warranty expires, and in some plans, power surge protection. Coverage typically excludes: accidental damage (drops, spills, impacts), cosmetic damage, damage from misuse or modification, consumable components (batteries, accessories), and pre-existing conditions.

Filing a claim under Amazon's extended warranty: find your extended warranty purchase in Your Orders, locate the warranty service contact information (usually an email or phone number for the warranty administrator), and describe the defect along with your product serial number. The warranty administrator may dispatch a technician to your home for large appliances, or ask you to bring the product to a designated service centre.

Turnaround time for extended warranty claims varies: laptop and phone repairs typically take 3 to 7 business days at a service centre. Large appliance repairs may take 5 to 14 business days depending on parts availability. If the item cannot be repaired, a replacement of equivalent value or a settlement cheque is provided, depending on your plan terms.

Compare Amazon's extended warranty plans with alternatives before purchasing: many credit cards in India provide an automatic 1-year extended warranty on purchases made with the card. This "credit card extended warranty benefit" may overlap with or supersede the need for a separate plan. Check your credit card's benefit guide — HDFC Regalia, ICICI Rubyx, and several other premium cards include this feature."""
},

# ════════════════════════════════════════════════════════════════
# TOPIC 12 — GENERAL SUPPORT TIPS  (15 articles)
# ════════════════════════════════════════════════════════════════

{
"topic": "general_tips",
"source": "general/contacting-support",
"title": "How to Effectively Contact E-commerce Customer Support",
"text": """Contacting e-commerce customer support efficiently — with the right information, through the right channel, at the right time — significantly increases the speed and quality of resolution you receive. Here is a comprehensive guide to getting the best results from customer support on Amazon, Flipkart, and eBay.

Before contacting support, gather your information: order ID or order number (found in Your Orders / My Orders / Purchase History), date of purchase, product name and model, specific description of the issue, and any supporting evidence (photographs, tracking screenshots). Having this information ready allows you to present your case clearly and prevents back-and-forth delays caused by the support agent asking for basic details.

Choosing the right channel matters. Live chat provides the fastest response for straightforward issues. Phone support is better for complex issues that require negotiation or where you need immediate escalation. Email is appropriate for issues where you need a written record or where the issue is complex and you want to articulate it carefully without time pressure. Amazon India offers 24/7 live chat and phone support. Flipkart support operates from 9 AM to 9 PM daily. eBay support includes live chat and messaging, with response times varying by region.

When describing your issue, be specific and factual. Instead of "My phone doesn't work," say "The front camera in the phone I received (Order ID: XXXXX) does not function at all — the camera app shows a black screen when the front camera is selected." Specific descriptions allow support agents to categorise and resolve your issue faster, and they create a clear documentation trail.

Escalation is sometimes necessary. If a first-line support agent cannot resolve your issue, politely ask to speak with a supervisor or senior support representative. Escalation is appropriate when: the resolution offered is inconsistent with the platform's stated policy, the support agent has given incorrect information, or the issue has been outstanding for more than 5 business days without progress. When escalating, reference the previous interaction (case number or chat transcript) to provide context.

Follow up in writing. After a phone call, send a follow-up email to the support address summarising what was discussed and the resolution that was promised. This creates a written record that can be referenced if the issue recurs or if the promised action is not taken. Most e-commerce support platforms also send chat transcripts to your registered email automatically, which serves the same purpose."""
},

{
"topic": "general_tips",
"source": "general/consumer-rights-india",
"title": "Consumer Rights for E-commerce Purchases in India",
"text": """Indian consumers purchasing online have strong legal protections under the Consumer Protection Act 2019 and the Consumer Protection (E-commerce) Rules 2020. Knowing your rights helps you escalate effectively when platform-level resolution is insufficient.

Under the Consumer Protection Act 2019, consumers have the right to: information (access to complete, accurate information about products and services), choice (a variety of goods at competitive prices), redressal (compensation or replacement for deficient goods or services), and representation (participation in consumer policy). E-commerce platforms are classified as "service providers" under this act and are required to provide redressal mechanisms.

The Consumer Protection (E-commerce) Rules 2020 specifically target online retailers. These rules require: e-commerce platforms to display clear return and refund policies, to provide a grievance officer's name and contact details on the website, to process refunds within a specified timeline, and to not engage in misleading advertising. If an e-commerce company violates these rules, consumers can file complaints with the Central Consumer Protection Authority (CCPA).

Consumer forums — known as Consumer Disputes Redressal Commissions (CDRCs) — operate at the district, state, and national level. For disputes up to ₹50 lakh, the District CDRC has jurisdiction. For ₹50 lakh to ₹2 crore, the State CDRC applies. Above ₹2 crore, the National Consumer Disputes Redressal Commission (NCDRC) handles cases. Filing a complaint costs a nominal fee and does not require a lawyer, though one may be helpful for complex cases.

The National Consumer Helpline (NCH) at 1800-11-4000 (toll-free) and 14404 provides preliminary consumer guidance. The National Consumer Helpline portal (consumerhelpline.gov.in) allows online complaint registration and tracking. The NCH can also mediate between consumers and companies, which often resolves disputes without formal legal proceedings.

Practical steps before escalating to consumer forums: exhaust all platform-level resolution options, document every step of your resolution attempt (screenshots, emails, chat logs), and write a formal complaint letter to the platform's grievance officer (their contact details must be displayed on the website per the e-commerce rules). A formal grievance officer complaint is a prerequisite for most consumer forum filings."""
},

{
"topic": "general_tips",
"source": "general/shopping-safely",
"title": "Shopping Safely on E-commerce Platforms — Complete Security Guide",
"text": """Online shopping security is a multi-layered concern encompassing account security, payment security, and product authenticity. Here is a comprehensive guide to protecting yourself across all these dimensions when shopping on Amazon, Flipkart, and eBay.

Account security is the foundation. Use a strong, unique password for each e-commerce account — never reuse passwords across sites. Enable two-factor authentication (2FA) on all accounts. Review your account's saved payment methods periodically and remove any that are no longer in use. Log out of e-commerce sites when using shared or public computers. Never share your OTP or account password with anyone, including people claiming to be from customer support — legitimate support agents never ask for OTPs or passwords.

Payment security starts with choosing the right payment method. Credit cards offer the strongest fraud protection because of chargeback rights. Debit cards are somewhat less protected because chargebacks reduce your actual bank balance rather than just delaying a credit card charge. UPI is very secure for registered transactions but be cautious of fraudulent payment links. Never pay through WhatsApp or other messaging apps for e-commerce purchases — always complete payment through the platform's official checkout.

Seller verification is important, particularly on marketplaces like eBay and Amazon Marketplace. Check seller ratings and read recent reviews. Look for established sellers with high feedback scores (98%+ positive on eBay, 4.5+ stars on Amazon Marketplace). Be cautious of new seller accounts selling high-demand or high-value items at unusually low prices. Legitimate brand products at prices far below retail are a common hallmark of counterfeit sellers.

Phishing awareness is critical. E-commerce platforms do not send emails asking you to click a link to verify payment or account details. Phishing emails often mimic Amazon, Flipkart, or eBay with convincing logos and formatting. Never click links in emails that direct you to login pages — always navigate directly to the website by typing the address. Check the sender's email address for subtle misspellings. Report phishing attempts to the platform using their anti-phishing reporting tool."""
},

{
"topic": "general_tips",
"source": "general/peak-sale-shopping",
"title": "Shopping During E-commerce Sales Events — What to Know",
"text": """India's major e-commerce sale events — Amazon's Great Indian Festival, Flipkart's Big Billion Days, Republic Day Sales, End of Season Sales, and festive season offers — attract hundreds of millions of shoppers and create specific challenges around delivery timelines, product availability, and customer support response times.

Delivery during sale periods is the most common concern. Platforms handle significantly higher order volumes during sales and while they scale up logistics operations, delays are still more common than during non-sale periods. Amazon and Flipkart typically add 1 to 3 days to their standard delivery estimates during peak periods, though Prime and Flipkart Plus deliveries are prioritised. If you need an item for a specific date, order well in advance rather than relying on a sale-period delivery estimate.

Product authenticity and seller quality during sales requires extra vigilance. Sale events attract both legitimate offers and opportunistic fake listings. Stick to products sold directly by Amazon or Flipkart, or by sellers with extensive, established track records. During high-demand sales, some sellers artificially inflate prices before the sale and apply a fake discount — check the product's price history using tools like camelcamelcamel.com (for Amazon) or browser extensions to verify that the sale price is a genuine discount.

Return experiences during post-sale periods (the weeks following major sales) are also affected by higher volumes. Expect slightly longer pickup schedules and quality inspection times during these periods. Most platforms post advisories in their Help Centres about extended timelines during high-volume periods. Keep this in mind when planning purchases that might need to be returned.

Customer support wait times increase significantly during sale events. Live chat queues can extend from the typical 2 to 5 minutes to 20 to 45 minutes or more. Email responses may take 48 to 72 hours instead of the usual 24 hours. Plan accordingly — for non-urgent issues, wait until the immediate post-sale period when volumes decrease. For genuinely urgent issues (payment failures, double charges), use phone support for faster access.

Payment security awareness is especially important during sale periods, as fraudsters increase activity around major events. Be cautious of deal-sharing websites and social media posts claiming exclusive voucher codes — many are phishing links designed to steal credentials or payment information. Always complete purchases through official apps and websites."""
},

]

def get_all_articles():
    """Return the full list of knowledge articles."""
    return KNOWLEDGE_ARTICLES

def get_articles_by_topic(topic: str):
    """Return articles filtered by topic."""
    return [a for a in KNOWLEDGE_ARTICLES if a["topic"] == topic]

def get_topic_summary():
    """Return a count summary by topic."""
    from collections import Counter
    return dict(Counter(a["topic"] for a in KNOWLEDGE_ARTICLES))

if __name__ == "__main__":
    summary = get_topic_summary()
    total = sum(summary.values())
    print(f"Total articles: {total}")
    for topic, count in sorted(summary.items()):
        print(f"  {topic:30s}: {count}")
