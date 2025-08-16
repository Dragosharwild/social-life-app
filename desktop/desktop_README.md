# Social Life – Desktop Application (Tkinter)

> **Component:** Desktop client for the Social Life project  
> **Focus:** Productivity-first management of *Inner Circles* (communities)  
> **Tech:** Python 3.15, Tkinter, SQLite, pytest, ruff

---

## 1) Purpose & Scope

This application is the **desktop** part of a two–component system (Desktop + Web).  
It delivers a minimal, testable MVP centered on **Inner Circles** — self‑contained communities created around a common interest. The desktop app focuses on **CRUD** operations and simple list‑based workflows suitable for Tkinter.

### Goals for the Desktop MVP
- Account **Sign Up** and **Login**.
- **Create** an Inner Circle; creator becomes owner automatically.
- **Search**, **Join**, and **Leave** Inner Circles.
- View **Circle Details**: creator and **member count** (live from DB).

### How this maps to course requirements
- **CRUD conventions:** Users, Circles, Memberships are modeled and persisted.
- **Modularity & Documentation:** Clear layering, interfaces, tests, and this README.
- **Version Control & Agile:** PRs, sprint board.
- **Desktop vs Web:** Calendar/events and richer visuals are planned primarily for the **Web** app; the Desktop app is a productivity client focused on community management.

---

## 2) Architecture Overview

We follow a **layered, modular** design to keep our systems decoupled.

```
UI (Tkinter Frames) - [No database code here - just collect user input and show results]
   │  calls
   ▼
Services (use cases / logic) - [Functions that decide what SHOULD happen]
   │  depend on
   ▼
Core (models + interfaces a.k.a. ports) - [middleman system that standardizes communication between logic and SQL]
   │  implemented by
   ▼
Infra (adapters) - [practical code that fulfills those interfaces using sqlite3]
```

- **UI** contains Tkinter screens and widgets only.
- **Services** enforce validation and application rules; **unit tested**.
- **Core** defines dataclasses and abstract interfaces.
- **Infra** implements those structures using SQLite.

**Layer rules**
- `ui` **never imports** `infra` directly - only `services`.
- `services` **depend on** `core.ports`, not on SQLite.
- `infra` depends on `core`, but **not** on `ui`.

This approach should let us reuse code for the webapp and test logic easily w/o a UI. 

---

## 3) Project Structure (desktop/)

```
desktop/
├─ README.md                      # this file
├─ main.py                        # thin entrypoint -> app/main.py
├─ app/
│  ├─ main.py                     # Tk root, wiring, bootstrap
│  ├─ navigation.py               # screen/router manager
│  ├─ state.py                    # AppState (current_user, selections)
│  └─ config.py                   # paths, sqlite file, feature flags
├─ ui/
│  ├─ screens/
│  │  ├─ auth_screen.py           # sign up / login
│  │  ├─ dashboard_screen.py      # my circles, search/join, create
│  │  └─ circle_detail_screen.py  # creator, members, leave
│  └─ widgets/
│     ├─ inputs.py                # labeled entries, password field
│     ├─ lists.py                 # list/tree helpers
│     └─ dialogs.py               # create-circle modal
├─ core/
│  ├─ models.py                   # User, InnerCircle, Membership (dataclasses)
│  ├─ ports.py                    # AuthRepo, CircleRepo interfaces
│  └─ errors.py                   # DuplicateUser, AuthFailed, etc.
├─ services/
│  ├─ auth_service.py             # sign_up(), login()
│  └─ circle_service.py           # create, search, join, leave, details
├─ infra/
│  ├─ db.py                       # sqlite connector + migration runner
│  ├─ repositories.py             # SQLite implementations of ports
│  └─ migrations/
│     └─ 001_init.sql             # users, circles, memberships
├─ utils/
│  ├─ validators.py               # input validation helpers
│  └─ logging.py                  # logger setup
├─ data/                          # runtime (gitignored)
│  └─ sociallife.sqlite
└─ tests/
   ├─ test_auth_service.py
   └─ test_circle_service.py
```

---

## 4) Data Model (SQLite)

**Tables**
- `users(id, username UNIQUE, email UNIQUE, password, created_at)`
- `circles(id, name, interest, description, creator_id FK users.id, created_at)`
- `memberships(user_id FK, circle_id FK, role TEXT DEFAULT 'member', joined_at, PRIMARY KEY(user_id, circle_id))`

**Derived values**
- **Member count:** `SELECT COUNT(*) FROM memberships WHERE circle_id=?`  
- **Creator:** `SELECT * FROM users WHERE id = circles.creator_id`

> The creator is automatically inserted as an `owner` membership on circle creation.

---

## 5) Security & Privacy

- Credentials are never logged. Logs avoid PII.
- Database file is local; treat `desktop/data/` as user‑private data.

---

## 6) User Stories & Acceptance Criteria (MVP)

**US-1 Sign up & Login**
- Create account with username + email + password; duplicates rejected.
- Log in with credentials and reach the dashboard; error messaging in UI.

**US-2 Create Circle**
- Provide name, interest, description.
- `creator_id` set to current user; creator added to `memberships` with role `owner`.

**US-3 Search / Join / Leave**
- Search by name or interest (substring).
- Join is idempotent (no duplicate rows). Leave removes membership.

**US-4 Circle Details**
- Show creator username and current member count.

All stories include unit tests at the **service** layer and a manual QA checklist.

---

## 7) Manual QA Checklist (for demos)

- [ ] New user can sign up; duplicate username/email shows message.
- [ ] Login with wrong password is rejected.
- [ ] Create circle succeeds; creator appears as owner.
- [ ] Second user joins; member count increases.
- [ ] Leave updates member count.
- [ ] App restart preserves data (SQLite file exists and loads).

**Demo flow:** sign up `alice` → create “UTRGV Chess” → sign up `bob` → search and join → open details: creator = `alice`, members = 2 → `bob` leaves → members = 1.

---