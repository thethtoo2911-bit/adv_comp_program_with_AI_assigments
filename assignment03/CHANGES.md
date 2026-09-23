# Assignment 03 — CHANGES

**Name:**Thet Htoo San **Student ID:**6705140080

## 1 · What I changed

1.I turned lists of raw facts into "smart objects". Before: the program stored items as plain lists of facts like ("Laptop", 1200.0, "electronics"). To get the price the computer had to remember it by itself. If someone changed the order, the whole program would break. After: I build the classes (Product, OrderItem, Order), now the computer can knows exactly which is which.
2.I get rid of repeated if/elif decision chains
3.I seperated math from printing. Before, the function printing the total was also printing the reciept at the same time. After: I build two function to seperate the responsibilities.
4.I also added the checks inside the constructors(__init__) to prevent the program from accidentally creating negative values for the products (the old code didn't stop me for that) 
5.Before: Numbers like 0.07, 0.03, and 10 were scattered randomly inside the math.After: I gave those numbers meaningful names at the top of the file, such as DEFAULT_TAX_RATE = 0.07 and LARGE_ORDER_QTY_THRESHOLD = 10

## 2 · Short reflection (4–6 sentences)

Which change improved the code the most, and why? Where did keeping the behaviour identical force you to be careful?

Replacing the if/elif tier-checking chains with Tier subclasses yielded is the greatest code improvement. Previously, adding or modifying a customer tier required searching through multiple conditional blocks inside calc() to update discount rules and point multipliers independently. By encapsulating these rules inside dedicated tier classes inheriting from a base Tier interface, the system adheres to the Open/Closed Principle; new loyalty tiers can now be added by simply creating a new class without modifying existing calculation logic.

---

## 3 · Prompt log (Level 2 — required)

Record **every** prompt where AI helped. If you wrote a part yourself, say so in one row. AI-shaped code with an empty log does **not** meet the Level-2 policy.

I ask the AI to check the assignment and tell me what do you want me to do. After that I ask the AI to give me the example to reference.

**Ownership statement.** *By submitting, I confirm I understand and can explain every line of code I submitted, and that this prompt log reflects my actual AI use.*

---

## 4 · Before-you-submit checklist

- [done] `python Assignment_03.py` prints **PASS**.
- [done] No tuples / parallel lists left — products, orders, and items are objects.
- [done] No `if tier == ...` chains — tiers are a class family.
- [done] Calculation methods **return** values and do not `print`; printing is separate.
- [done] Constructors validate state; no leftover `global`; magic numbers are named.
- [done] The change table and reflection above are filled in.
- [done] The prompt log is complete and the ownership statement is signed.
