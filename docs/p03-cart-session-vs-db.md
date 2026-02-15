# Project 03 — Cart (Session vs Database) Research

This document answers:

1) In carts that are built using user sessions, is it possible to store the cart directly in the database instead of the session?
2) If yes, how is it usually designed?
3) How are anonymous users vs authenticated users handled?
4) How are quantities managed (override vs increment)?
5) A short analysis inspired by a real e-commerce (example: Digikala-like behavior).

---

## 1) Session-Based Cart vs Database Cart

### A) Session-Based Cart (Classic approach)
A cart is stored in the user's session (cookie-based session id on the client, cart data on the server).

**Pros**
- Very fast to implement
- No DB writes for every add/remove
- Works for anonymous users without any user table dependency

**Cons**
- Session can expire → cart is lost (unless you persist it)
- Harder to share cart across devices
- Limits when you want advanced behaviors (promotions, inventory validation, analytics)

**Common format**
- `session["cart"] = { product_id: quantity, ... }`
- sometimes variant-based keys (e.g., `product_id:size_id:color_id`)

---

### B) Database-Persisted Cart (Industry approach)
Yes, it is absolutely possible (and very common) to store the cart in the database.

Usually you create:
- `Cart` table
- `CartItem` table

This is the standard approach for larger systems because it supports:
- cross-device cart
- long-term persistence
- analytics/reporting
- safe concurrency handling

---

## 2) Typical Database Design

### A) Minimal relational model
- **Cart**
  - `id`
  - `user` (nullable) → null means anonymous cart
  - `status` (active / ordered / abandoned)
  - `created_date`, `updated_date`
  - optional: `session_key` (for anonymous carts)
  - optional: `currency`, `coupon`, `notes`

- **CartItem**
  - `id`
  - `cart` (FK)
  - `product` (FK)
  - `quantity`
  - optional: `price_snapshot` (store product price at the time of add)
  - optional: `variant fields` (color/size) or FK to `ProductVariant`
  - `created_date`, `updated_date`

### B) Why `session_key` is useful
For anonymous users you still have a session id in Django (`request.session.session_key`).
You can store the cart in DB using that `session_key`.

That gives you:
- DB persistence (no lost cart if server restarts)
- still works without login

---

## 3) Anonymous vs Authenticated Users (How to manage both)

### A) Anonymous user (not logged in)
Common strategies:

#### Strategy 1 — Session-only (simple)
- Cart stored only in session, disappears when session expires.

#### Strategy 2 — DB cart linked to `session_key` (recommended for scalable design)
- If user is anonymous:
  - ensure session exists (`request.session.save()` if needed)
  - use `session_key` as identity
  - create/find `Cart(session_key=..., user=NULL, status=active)`
  - store items in DB

**Benefit**
- Later, when user logs in, you can "merge" this cart into the user's cart.

---

### B) Authenticated user (logged in)
- Cart stored in DB linked to `user_id`.

**Key behavior**
- user cart persists across devices/browsers if you identify by user.

---

## 4) What happens on Login (Cart Merge Strategy)

When a user logs in, there are typically two carts:
- Anonymous cart (from `session_key`)
- User cart (from `user_id`)

You should define a deterministic merge policy.

### A) Merge policy options

#### Option 1 — Increment quantity (most common)
If the same product exists in both carts:
- `final_qty = user_qty + anon_qty`

**Pros**
- user expects "added items" to accumulate
- fewer surprises

**Cons**
- may exceed stock → must validate inventory later

#### Option 2 — Override quantity (sometimes used)
If same product exists:
- `final_qty = anon_qty` (or user qty)
This is less common because users expect carts to merge additively.

#### Option 3 — Prefer latest updated cart (rare)
Take whichever cart was updated more recently.

---

### B) Recommended merge (practical)
- If item exists in both carts → **increment**
- After merge:
  - delete anonymous cart or mark it inactive
  - keep user cart active

---

## 5) Quantity Handling (Override vs Increment)

### A) Increment behavior (typical e-commerce UX)
When user clicks "Add to cart":
- quantity increases by 1 (or by selected number)

### B) Override behavior (more common in admin or direct edits)
When user changes quantity inside cart page:
- quantity is overwritten by the new value

**Recommended UX**
- product detail "Add to cart" → increment
- cart page "quantity input" → override

---

## 6) Inventory & Validation Notes (Important for later project steps)

Even if you store cart in DB:
- inventory must be validated when:
  - adding to cart (optional soft-check)
  - checkout (mandatory hard-check)

**Soft-check**
- if not enough stock, prevent increasing quantity

**Hard-check**
- during order finalization, re-check all items stock under transaction/locking

---

## 7) Example Behavior (Digikala-like analysis)

Typical behavior (observed across many e-commerce platforms):
- Anonymous users can add items to cart
- Cart persists for some time (session/cookie)
- On login:
  - cart merges into the user cart
  - quantities usually **increase** (not override)
- Checkout validates stock again
- If stock changed:
  - quantity is reduced or user is notified

This behavior matches user expectations:
- "Whatever I added should still be here"
- login should not delete cart items

---

## 8) Conclusion (Best Practice Recommendation)

### Recommended approach for this project
- Use **DB-backed cart**
- For anonymous users use `session_key`
- For authenticated users use `user`
- Implement merge on login:
  - increment quantities for same products

This design supports the future modules:
- coupons/discount codes
- inventory validation
- order creation from cart
- analytics & admin reporting

---

## 9) Next Step (Implementation plan)
In the code phase (Project 03 implementation):
1) Create `Cart` + `CartItem` models
2) Add API endpoint:
   - `POST /api/cart/items/` → add item (increment)
3) Add API endpoint:
   - `GET /api/cart/` → show cart with items
4) Add merge logic on login (or first request after login)

