# 🏛️ University Data Insertion Template

This is a **generalized SQL template** for inserting any university into the Uni-verse database. Use this as a reusable pattern when adding new universities.

---

## 🧠 Generalized SQL Insertion Template

Use this as a reusable pattern when adding other universities:

> 📝 **Replace:**
>
> * `'YOUR UNIVERSITY NAME'`
> * `'public'` with the correct sector
> * Program names
> * Campus cities
> * Boards, tags, etc.

---

### 🔹 Step 1: Insert University

```sql
INSERT INTO universities (name, sector)
VALUES ('YOUR UNIVERSITY NAME', 'public')  -- or 'private' / 'semi-government'
ON CONFLICT (name) DO NOTHING;
```

---

### 🔹 Step 2: Insert Programs

```sql
INSERT INTO programs (name, discipline, code)
VALUES 
  ('BS – Computer Science', 'Computer Science', NULL),
  ('BBA', 'Business Administration', NULL)
  -- Add more as needed
ON CONFLICT (name) DO NOTHING;
```

---

### 🔹 Step 3: Insert Campuses

```sql
INSERT INTO campuses (university_id, city)
SELECT u.id, c.city
FROM universities u
CROSS JOIN (
  VALUES 
    ('Lahore'),
    ('Islamabad')  -- Add all campus cities
) AS c(city)
WHERE u.name = 'YOUR UNIVERSITY NAME'
ON CONFLICT (university_id, city) DO NOTHING;
```

---

### 🔹 Step 4: Insert Entrance Test Types

```sql
INSERT INTO entrance_test_types (name)
VALUES ('YOUR ENTRY TEST NAME')
ON CONFLICT (name) DO NOTHING;
```

---

### 🔹 Step 5: Insert Tags

```sql
INSERT INTO tags (name)
VALUES 
  ('computer-science'),
  ('business'),
  ('engineering')
ON CONFLICT (name) DO NOTHING;
```

---

### 🔹 Step 6: Insert Program Offerings

```sql
WITH campus_mapping AS (
  SELECT 
    c.id AS campus_id,
    c.city,
    ROW_NUMBER() OVER (ORDER BY c.id) AS campus_order
  FROM campuses c
  JOIN universities u ON c.university_id = u.id
  WHERE u.name = 'YOUR UNIVERSITY NAME'
),
program_campus_combinations AS (
  SELECT 
    p.id AS program_id,
    cm.campus_id,
    CASE WHEN cm.city = 'Some City' THEN 50000 ELSE 60000 END AS annual_fee,
    TRUE AS should_offer
  FROM programs p
  CROSS JOIN campus_mapping cm
  WHERE p.name IN ('BS – Computer Science', 'BBA')
)
INSERT INTO program_offerings (program_id, campus_id, min_score_pct, min_score_type, annual_fee, hostel_available)
SELECT 
  program_id,
  campus_id,
  60.0,
  'ssc_hsc',
  annual_fee,
  false
FROM program_campus_combinations
WHERE should_offer = TRUE;
```

---

### 🔹 Step 7: Insert Program Offering Boards

```sql
INSERT INTO program_offering_boards (offering_id, board)
SELECT 
  po.id,
  b.board_name
FROM program_offerings po
JOIN campuses c ON po.campus_id = c.id
JOIN universities u ON c.university_id = u.id
CROSS JOIN (
  SELECT 'BISE Lahore' AS board_name
  UNION ALL
  SELECT 'Other Pakistani Boards'
) AS b
WHERE u.name = 'YOUR UNIVERSITY NAME';
```

---

### 🔹 Step 8: Insert Program Offering Groups

```sql
INSERT INTO program_offering_groups (offering_id, subject_group)
SELECT 
  po.id,
  sg.subject_group
FROM program_offerings po
JOIN programs p ON po.program_id = p.id
JOIN campuses c ON po.campus_id = c.id
JOIN universities u ON c.university_id = u.id
CROSS JOIN LATERAL (
  SELECT 
    CASE 
      WHEN p.name LIKE 'BS – Computer Science' THEN ARRAY['Pre-Engineering', 'ICS']
      WHEN p.name LIKE 'BBA' THEN ARRAY['ICom', 'General Science']
      ELSE ARRAY['Pre-Engineering']
    END AS subject_groups
) sg_array
CROSS JOIN LATERAL unnest(sg_array.subject_groups) AS sg(subject_group)
WHERE u.name = 'YOUR UNIVERSITY NAME';
```

---

### 🔹 Step 9: Insert Program Offering Tests

```sql
INSERT INTO program_offering_tests (offering_id, test_type_id, min_score)
SELECT 
  po.id,
  ett.id,
  50.0
FROM program_offerings po
JOIN campuses c ON po.campus_id = c.id
JOIN universities u ON c.university_id = u.id
JOIN entrance_test_types ett ON ett.name = 'YOUR ENTRY TEST NAME'
WHERE u.name = 'YOUR UNIVERSITY NAME';
```

---

### 🔹 Step 10: Insert Program Offering Tags

```sql
INSERT INTO program_offering_tags (offering_id, tag_id)
SELECT DISTINCT
  po.id,
  t.id
FROM program_offerings po
JOIN programs p ON po.program_id = p.id
JOIN campuses c ON po.campus_id = c.id
JOIN universities u ON c.university_id = u.id
JOIN tags t ON (
  (p.name = 'BS – Computer Science' AND t.name IN ('computer-science')) OR
  (p.name = 'BBA' AND t.name IN ('business'))
)
WHERE u.name = 'YOUR UNIVERSITY NAME'
  AND c.city = 'Lahore';  -- Only apply tags once if needed
```

---

## 📋 Checklist for New University Insertion

1. [ ] **Research University Data**
   - University name and sector (public/private/semi-government)
   - All campus locations
   - Complete program list with disciplines
   - Entrance test requirements
   - Fee structure
   - Admission requirements (boards, subject groups)

2. [ ] **Customize Template**
   - Replace `'YOUR UNIVERSITY NAME'` with actual name
   - Update sector type
   - List all programs with correct disciplines
   - Add all campus cities
   - Set appropriate fees for each campus
   - Configure entrance test names
   - Map programs to subject groups
   - Add relevant tags

3. [ ] **Execute SQL Steps**
   - Run steps 1-10 in order
   - Check for errors after each step
   - Verify data insertion with verification queries

4. [ ] **Verify Insertion**
   - Use verification queries to confirm all data
   - Test API endpoints with new university data
   - Check frontend search functionality

---

## 💡 Tips for Success

- **Always use `ON CONFLICT` clauses** to prevent duplicate entries
- **Test with one program first** before adding all programs
- **Use meaningful tags** that match student interests
- **Set realistic fees** based on actual university data
- **Map subject groups carefully** to ensure proper matching
- **Backup database** before large insertions

---

## 🔍 Related Files

- `DATABASE_SETUP_REPORT.md` - Database schema reference
- `backend/models.py` - SQLAlchemy model definitions
- `ned_verification_queries.sql` - Template for verification queries
- `database_troubleshooting.sql` - Debug queries for issues

---

*This template was created based on the successful NED University insertion process.*