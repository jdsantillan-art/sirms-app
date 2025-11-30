# DFD Quick Reference Guide
## How to Create Your Own Data Flow Diagrams

---

## QUICK START CHECKLIST

### For Context Diagram (Level 0)
- [ ] Identify all external entities (users/systems)
- [ ] Draw ONE circle for your entire system
- [ ] Draw squares for each external entity
- [ ] Draw arrows showing data IN and OUT
- [ ] Label every arrow with data description
- [ ] Verify: No data stores at this level

### For Level 1 DFD
- [ ] Break system into 5-9 major processes
- [ ] Number processes (1.0, 2.0, 3.0, etc.)
- [ ] Keep same external entities from Context
- [ ] Add data stores (databases, files)
- [ ] Connect with data flows
- [ ] Verify: Balancing with Context Diagram

### For Level 2 DFD
- [ ] Pick ONE process from Level 1
- [ ] Break it into sub-processes (2.1, 2.2, 2.3, etc.)
- [ ] Show detailed data flows
- [ ] Add any new data stores needed
- [ ] Verify: Balancing with Level 1

---

## SYMBOLS REFERENCE

### External Entity (Square/Rectangle)
```
┌─────────────┐
│   Student   │
└─────────────┘
```
**What it is:** People or systems OUTSIDE your system
**Examples:** Student, Teacher, Admin, External API

**Rules:**
- Always outside your system boundary
- Can appear multiple times on same diagram
- Cannot connect directly to data stores
- Must connect through processes

---

### Process (Circle/Rounded Rectangle)
```
┌─────────────────┐
│  2.0 Incident   │
│    Reporting    │
└─────────────────┘
```
**What it is:** Actions that transform or manipulate data
**Examples:** Validate Login, Generate Report, Classify Case

**Rules:**
- Must have at least one input and one output
- Should be numbered (1.0, 2.0, 2.1, etc.)
- Use verb-noun naming (e.g., "Validate User", "Store Report")
- Cannot connect directly to other processes (must use data flows)

---

### Data Store (Open Rectangle)
```
═══════════════════
  D1: User Database
═══════════════════
```
**What it is:** Where data is stored (database, file, table)
**Examples:** User Database, Incident Reports, Configuration File

**Rules:**
- Must be numbered (D1, D2, D3, etc.)
- Can only connect to processes (not external entities)
- Data flows can be read or write
- Appears only in Level 1 and below

---

### Data Flow (Arrow)
```
────────────────>
  Incident Report
```
**What it is:** Movement of data between elements
**Examples:** Login Credentials, Report Status, User Data

**Rules:**
- Must be labeled with data description
- Shows direction of data movement
- Can split (one source, multiple destinations)
- Can merge (multiple sources, one destination)

---

## NAMING CONVENTIONS

### Processes
✅ **Good Names:**
- Validate User Login
- Generate Case ID
- Store Incident Report
- Classify Violation
- Send Notification

❌ **Bad Names:**
- Process Data
- Handle Request
- Do Something
- System Function

**Pattern:** Verb + Noun (Action + Object)

---

### Data Flows
✅ **Good Names:**
- Login Credentials
- Incident Report Data
- Classification Decision
- User Profile
- Notification Message

❌ **Bad Names:**
- Data
- Information
- Stuff
- Input/Output

**Pattern:** Descriptive noun phrase

---

### Data Stores
✅ **Good Names:**
- D1: User Database
- D2: Incident Reports
- D3: Classification Records
- D4: System Configuration

❌ **Bad Names:**
- D1: Database
- D2: Data
- D3: Storage

**Pattern:** D# + Descriptive Name

---

## COMMON MISTAKES TO AVOID

### ❌ Mistake 1: Showing Physical Flow
**Wrong:**
```
Student ──Walks to office──> DO ──Hands paper──> File Cabinet
```

**Right:**
```
Student ──Incident Report──> System ──Store Report──> Incident Database
```

**Why:** DFD shows DATA flow, not physical movement

---

### ❌ Mistake 2: Including Control Logic
**Wrong:**
```
Process ──If valid then──> Next Process
        ──Else error──> Error Handler
```

**Right:**
```
Process ──Valid Data──> Next Process
        ──Invalid Data──> Error Handler
```

**Why:** DFD shows data flow, not decision logic (use flowchart for that)

---

### ❌ Mistake 3: Direct Connection Between External Entities
**Wrong:**
```
Student ──Report──> Teacher
```

**Right:**
```
Student ──Report──> System ──Notification──> Teacher
```

**Why:** External entities must interact through the system

---

### ❌ Mistake 4: External Entity to Data Store
**Wrong:**
```
Student ──Data──> Database
```

**Right:**
```
Student ──Data──> Process ──Store──> Database
```

**Why:** Only processes can access data stores

---

### ❌ Mistake 5: Unlabeled Arrows
**Wrong:**
```
Student ────────> Process
```

**Right:**
```
Student ──Login Credentials──> Process
```

**Why:** Every data flow must describe what data is moving

---

### ❌ Mistake 6: Too Many Processes in Level 1
**Wrong:**
```
1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0...
```

**Right:**
```
1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0
```

**Why:** Keep Level 1 to 5-9 major processes for clarity

---

## BALANCING RULES

### What is Balancing?
Balancing ensures consistency between DFD levels. Data flows in/out of a process at one level must match the data flows in/out of its decomposition at the next level.

### Example of Balanced DFD

**Level 1:**
```
Student ──Incident Report──> (2.0 Incident Reporting) ──Confirmation──> Student
                                      │
                                      ↓
                                 Incident Database
```

**Level 2 (Decomposition of 2.0):**
```
Student ──Incident Report──> (2.1 Validate) ──Valid Data──> (2.2 Store) ──Confirmation──> Student
                                                                  │
                                                                  ↓
                                                            Incident Database
```

**Balanced because:**
- Input at Level 1: "Incident Report" from Student
- Input at Level 2: "Incident Report" from Student ✓
- Output at Level 1: "Confirmation" to Student
- Output at Level 2: "Confirmation" to Student ✓
- Data Store at Level 1: Incident Database
- Data Store at Level 2: Incident Database ✓

---

## STEP-BY-STEP PROCESS

### Step 1: Understand the System
**Questions to ask:**
- What is the main purpose of the system?
- Who are the users?
- What data goes in?
- What data comes out?
- Where is data stored?

**For SIRMS:**
- Purpose: Manage student incident reports
- Users: Students, Teachers, DO, Counselors, Principal
- Input: Incident reports, classifications, evaluations
- Output: Notifications, reports, analytics
- Storage: User DB, Incident DB, Classification DB, etc.

---

### Step 2: Create Context Diagram
**Process:**
1. Draw one circle in center (your system)
2. List all external entities
3. Draw squares around the circle
4. Draw arrows for data IN
5. Draw arrows for data OUT
6. Label all arrows

**Time:** 15-30 minutes

---

### Step 3: Identify Major Processes
**Process:**
1. List all major functions of your system
2. Group related functions together
3. Aim for 5-9 major processes
4. Name each process clearly

**For SIRMS:**
1. User Authentication
2. Incident Reporting
3. Case Classification
4. Case Evaluation
5. Sanction Management
6. Schedule Management
7. Analytics & Reporting

**Time:** 30-45 minutes

---

### Step 4: Create Level 1 DFD
**Process:**
1. Draw circles for each major process
2. Number them (1.0, 2.0, 3.0, etc.)
3. Keep external entities from Context
4. Add data stores
5. Connect with data flows
6. Label everything
7. Verify balancing with Context

**Time:** 1-2 hours

---

### Step 5: Create Level 2 DFD (Optional)
**Process:**
1. Pick ONE complex process from Level 1
2. Break it into sub-processes
3. Number them (2.1, 2.2, 2.3, etc.)
4. Show detailed data flows
5. Add any new data stores
6. Verify balancing with Level 1

**Time:** 30-60 minutes per process

---

## TIPS FOR SUCCESS

### 1. Start Simple
Don't try to show everything at once. Start with Context, then Level 1, then Level 2.

### 2. Use Consistent Names
If you call something "Incident Report" in one place, use the same name everywhere.

### 3. Focus on Data, Not Process
DFD shows WHAT data flows, not HOW it's processed.

### 4. Keep It Readable
If your diagram is too cluttered, break it into multiple Level 2 diagrams.

### 5. Get Feedback
Show your DFD to others and ask:
- Is it clear?
- Is anything missing?
- Does the flow make sense?

### 6. Iterate
Your first draft won't be perfect. Revise and improve.

### 7. Use Tools
- Draw.io (free, online)
- Lucidchart (online, templates)
- Microsoft Visio (professional)
- Paper and pencil (quick sketches)

---

## PRACTICE EXERCISE

### Exercise 1: Library System
Create a Context Diagram for a library system.

**Entities:**
- Student
- Librarian
- System Admin

**Functions:**
- Borrow books
- Return books
- Search catalog
- Manage inventory

**Try it yourself, then check the answer below!**

<details>
<summary>Click to see answer</summary>

```
┌─────────────┐
│   Student   │
└──────┬──────┘
       │
       │ Borrow Request
       │ Search Query
       ↓
       │ Book Information
       │ Due Date
       ↑
       │
┌──────────────────────────────────────┐
│                                      │
│        Library System                │
│                                      │
└──────────────────────────────────────┘
       ↑                    ↑
       │                    │
       │ Return Book        │ Inventory Update
       │ Book Status        │ Reports
       │                    │
       ↓                    ↓
       │ Receipt            │ System Data
       │                    │
┌──────┴──────┐      ┌─────┴──────┐
│  Librarian  │      │   Admin    │
└─────────────┘      └────────────┘
```
</details>

---

### Exercise 2: Online Shopping
Create Level 1 DFD for an online shopping system.

**Major Processes:**
- User Registration
- Product Browsing
- Shopping Cart
- Checkout
- Order Management

**Try it yourself!**

---

## TEMPLATES

### Context Diagram Template
```
┌─────────────┐
│  Entity 1   │
└──────┬──────┘
       │
       │ Data Flow In
       ↓
       │ Data Flow Out
       ↑
       │
┌──────────────────────────────────────┐
│                                      │
│        [Your System Name]            │
│                                      │
└──────────────────────────────────────┘
       ↑
       │
       │ Data Flow In
       ↓
       │ Data Flow Out
       │
┌──────┴──────┐
│  Entity 2   │
└─────────────┘
```

---

### Level 1 DFD Template
```
[External Entity]
       │
       │ Input Data
       ↓
(1.0 Process Name) ←──→ [D1: Data Store]
       │
       │ Output Data
       ↓
(2.0 Process Name) ←──→ [D2: Data Store]
       │
       │ Result
       ↓
[External Entity]
```

---

## CHECKLIST FOR REVIEW

### Before Submitting Your DFD

**Context Diagram:**
- [ ] Only ONE process (the system)
- [ ] All external entities identified
- [ ] All data flows labeled
- [ ] No data stores shown
- [ ] Clear and readable

**Level 1 DFD:**
- [ ] 5-9 major processes
- [ ] All processes numbered
- [ ] All data stores numbered
- [ ] All data flows labeled
- [ ] Balanced with Context Diagram
- [ ] No direct entity-to-entity connections
- [ ] No direct entity-to-datastore connections

**Level 2 DFD:**
- [ ] Sub-processes properly numbered (2.1, 2.2, etc.)
- [ ] Balanced with parent process in Level 1
- [ ] All data flows labeled
- [ ] Shows appropriate level of detail
- [ ] Not too complex

**General:**
- [ ] Consistent naming throughout
- [ ] No control logic shown
- [ ] No physical flow shown
- [ ] Readable and well-organized
- [ ] Reviewed by someone else

---

## RESOURCES

### Online Tools
- **Draw.io** - https://app.diagrams.net/ (Free)
- **Lucidchart** - https://www.lucidchart.com/ (Free tier available)
- **Creately** - https://creately.com/ (Templates available)

### Books
- "Structured Analysis and System Specification" by Tom DeMarco
- "Modern Systems Analysis and Design" by Hoffer, George, Valacich

### Video Tutorials
- Search YouTube for "Data Flow Diagram tutorial"
- Look for "DFD examples" for your specific domain

---

## GLOSSARY

**Balancing:** Ensuring consistency between DFD levels

**Context Diagram:** Level 0 DFD showing entire system as one process

**Data Flow:** Movement of data between elements (shown as arrow)

**Data Store:** Repository where data is stored (database, file, etc.)

**Decomposition:** Breaking down a process into sub-processes

**External Entity:** Person or system outside your system boundary

**Level 1 DFD:** First decomposition showing major processes

**Level 2 DFD:** Further decomposition of one Level 1 process

**Process:** Action that transforms or manipulates data

---

## SUMMARY

Creating a DFD is a systematic process:

1. **Understand** your system thoroughly
2. **Start** with Context Diagram (big picture)
3. **Break down** into Level 1 (major processes)
4. **Detail** with Level 2 (sub-processes)
5. **Verify** balancing at each level
6. **Review** and refine

Remember: DFD shows WHAT data flows, not HOW it's processed!

---

**Created By:** Kiro AI Assistant  
**Date:** November 30, 2025  
**Purpose:** Quick reference for creating Data Flow Diagrams
