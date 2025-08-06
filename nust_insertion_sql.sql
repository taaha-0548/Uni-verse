-- 🏛️ NUST University Data Insertion Script
-- National University of Sciences and Technology (NUST)

-- =====================================================
-- STEP 1: Insert University
-- =====================================================

INSERT INTO universities (name, sector)
VALUES ('National University of Sciences and Technology (NUST)', 'public')
ON CONFLICT (name) DO NOTHING;

-- =====================================================
-- STEP 2: Insert Campuses
-- =====================================================

WITH uni AS (
  SELECT id FROM universities 
  WHERE name = 'National University of Sciences and Technology (NUST)'
)
INSERT INTO campuses (university_id, name, city)
SELECT uni.id, campus_data.name, campus_data.city
FROM uni CROSS JOIN (
  VALUES 
    ('NUST H-12 Campus', 'Islamabad'),
    ('Military College of Signals (MCS)', 'Rawalpindi'),
    ('College of Electrical and Mechanical Engineering (CoEME)', 'Rawalpindi'),
    ('Military College of Engineering (MCE)', 'Risalpur'),
    ('College of Aeronautical Engineering (CAE)', 'Risalpur'),
    ('Pakistan Navy Engineering College (PNEC)', 'Karachi'),
    ('NUST Balochistan Campus (NBC)', 'Quetta')
) AS campus_data(name, city)
ON CONFLICT (university_id, name) DO NOTHING;

-- =====================================================
-- STEP 3: Insert Programs
-- =====================================================

INSERT INTO programs (name, discipline, code)
VALUES 
  -- Engineering Programs
  ('BE Electrical', 'Engineering', NULL),
  ('BE Software', 'Engineering', NULL),
  ('BE Mechanical', 'Engineering', NULL),
  ('BE Civil', 'Engineering', NULL),
  ('BE Aerospace', 'Engineering', NULL),
  ('BE Metallurgy & Materials', 'Engineering', NULL),
  ('BE Chemical', 'Engineering', NULL),
  ('BE Environmental', 'Engineering', NULL),
  ('BE Geoinformatics', 'Engineering', NULL),
  ('BE Computer', 'Engineering', NULL),
  ('BE Mechatronics', 'Engineering', NULL),
  ('BE Information Security', 'Engineering', NULL),
  ('BE Avionics', 'Engineering', NULL),
  ('BE Naval Architecture', 'Engineering', NULL),

  -- Computing Programs
  ('BS Computer Science', 'Computer Science', NULL),
  ('BS Data Science', 'Computer Science', NULL),
  ('BS Artificial Intelligence', 'Computer Science', NULL),
  ('BS Bioinformatics', 'Natural Sciences', NULL),

  -- Business Programs
  ('BBA Administration', 'Business', NULL),
  ('BS Accounting and Finance', 'Business', NULL),
  ('BS Tourism & Hospitality Management', 'Business', NULL),

  -- Social Sciences Programs
  ('BS Economics', 'Social Sciences', NULL),
  ('BS Mass Communication', 'Social Sciences', NULL),
  ('Bachelor of Public Administration', 'Social Sciences', NULL),
  ('BS Psychology', 'Social Sciences', NULL),
  ('BS English (Language and Literature)', 'Humanities', NULL),

  -- Architecture & Design Programs
  ('Bachelor of Architecture', 'Architecture & Design', NULL),
  ('Bachelor of Industrial Design', 'Architecture & Design', NULL),

  -- Natural Sciences Programs
  ('BS Mathematics', 'Natural Sciences', NULL),
  ('BS Physics', 'Natural Sciences', NULL),
  ('BS Chemistry', 'Natural Sciences', NULL),
  ('BS Environmental Science', 'Natural Sciences', NULL),
  ('BS Biotechnology', 'Natural Sciences', NULL),
  ('BS Food Science and Technology', 'Natural Sciences', NULL),
  ('Bachelor of Science in Agriculture', 'Natural Sciences', NULL),

  -- Law Program
  ('Bachelor of Laws (LLB)', 'Law', NULL),

  -- Medical Programs
  ('MBBS', 'Medicine', NULL),
  ('BS Human Nutrition and Dietetics', 'Health Sciences', NULL)
ON CONFLICT (name) DO NOTHING;

-- =====================================================
-- STEP 4: Insert Entrance Test Types
-- =====================================================

INSERT INTO entrance_test_types (name)
VALUES 
  ('NUST Entry Test (NET)'),
  ('SAT'),
  ('ACT'),
  ('HEC Law Admission Test (LAT)'),
  ('NUMS MDCAT')
ON CONFLICT (name) DO NOTHING;

-- =====================================================
-- STEP 5: Insert Tags
-- =====================================================

INSERT INTO tags (name)
VALUES 
  -- Engineering Tags
  ('engineering'),
  ('electrical-engineering'),
  ('software-engineering'),
  ('mechanical-engineering'),
  ('civil-engineering'),
  ('aerospace-engineering'),
  ('metallurgy'),
  ('materials-engineering'),
  ('chemical-engineering'),
  ('environmental-engineering'),
  ('geoinformatics'),
  ('computer-engineering'),
  ('mechatronics'),
  ('information-security'),
  ('avionics'),
  ('naval-architecture'),
  
  -- Computing Tags
  ('computer-science'),
  ('data-science'),
  ('artificial-intelligence'),
  ('bioinformatics'),
  
  -- Business Tags
  ('business'),
  ('bba'),
  ('accounting'),
  ('finance'),
  ('tourism'),
  ('hospitality-management'),
  
  -- Social Sciences Tags
  ('social-sciences'),
  ('economics'),
  ('mass-communication'),
  ('public-administration'),
  ('psychology'),
  ('humanities'),
  ('english-literature'),
  
  -- Architecture & Arts Tags
  ('architecture'),
  ('industrial-design'),
  
  -- Natural Sciences Tags
  ('natural-sciences'),
  ('mathematics'),
  ('physics'),
  ('chemistry'),
  ('environmental-science'),
  ('biotechnology'),
  ('food-science'),
  ('agriculture'),
  
  -- Law Tags
  ('law'),
  ('llb'),
  
  -- Medical Tags
  ('medicine'),
  ('mbbs'),
  ('health-sciences'),
  ('nutrition'),
  ('dietetics')
ON CONFLICT (name) DO NOTHING;

-- =====================================================
-- STEP 6: Insert Program Offerings
-- =====================================================

WITH campus_mapping AS (
  SELECT 
    c.id AS campus_id,
    c.name AS campus_name,
    c.city
  FROM campuses c
  JOIN universities u ON c.university_id = u.id
  WHERE u.name = 'National University of Sciences and Technology (NUST)'
),
program_offerings_data AS (
  SELECT 
    p.id AS program_id,
    cm.campus_id,
    CASE 
      WHEN p.name = 'MBBS' THEN 80.0
      ELSE 60.0
    END as min_score_pct,
    CASE
      WHEN p.name = 'MBBS' THEN 'mdcat'
      WHEN p.name = 'Bachelor of Laws (LLB)' THEN 'lat'
      ELSE 'ssc_hsc'
    END as min_score_type,
    CASE
      WHEN p.discipline IN ('Business', 'Architecture & Design', 'Law') THEN 506160
      WHEN p.name = 'BS English (Language and Literature)' THEN 175400
      WHEN p.name = 'MBBS' THEN NULL
      ELSE 348100
    END as annual_fee,
    TRUE as hostel_available
  FROM programs p
  CROSS JOIN campus_mapping cm
  WHERE (cm.campus_name, p.name) IN (
    SELECT po.campus_name, po.program_name
    FROM json_to_recordset('[your_program_offerings_json_array]') AS po(
      campus_name text,
      program_name text
    )
  )
)
INSERT INTO program_offerings (
  program_id,
  campus_id,
  min_score_pct,
  min_score_type,
  annual_fee,
  hostel_available
)
SELECT 
  program_id,
  campus_id,
  min_score_pct,
  min_score_type,
  annual_fee,
  hostel_available
FROM program_offerings_data
ON CONFLICT (program_id, campus_id) DO UPDATE SET
  min_score_pct = EXCLUDED.min_score_pct,
  min_score_type = EXCLUDED.min_score_type,
  annual_fee = EXCLUDED.annual_fee,
  hostel_available = EXCLUDED.hostel_available;

-- =====================================================
-- STEP 7: Insert Program Offering Boards
-- =====================================================

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
WHERE u.name = 'National University of Sciences and Technology (NUST)';

-- =====================================================
-- STEP 8: Insert Program Offering Groups
-- =====================================================

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
      WHEN p.name LIKE 'BE –%' THEN ARRAY['Pre-Engineering', 'ICS (Computer Science)']
      WHEN p.name LIKE 'BS – Computer Science' OR p.name LIKE 'BS – Data Science' OR 
           p.name LIKE 'BS – Artificial Intelligence' OR p.name LIKE 'BS – Bioinformatics' THEN ARRAY['Pre-Engineering', 'ICS (Computer Science)']
      WHEN p.name LIKE 'BBA –%' OR p.name LIKE 'BS – Accounting%' OR p.name LIKE 'BS – Tourism%' OR
           p.name LIKE 'BS – Economics' OR p.name LIKE 'BS – Mass Communication' OR 
           p.name LIKE 'BS – Public Administration' OR p.name LIKE 'BS – Psychology' OR
           p.name LIKE 'LLB – Laws' THEN ARRAY['ICom (Commerce)', 'IA (Arts)']
      WHEN p.name LIKE 'B.ARCH –%' OR p.name LIKE 'BS – Industrial Design' THEN ARRAY['Pre-Engineering']
      WHEN p.name LIKE 'BS – Mathematics' OR p.name LIKE 'BS – Physics' OR p.name LIKE 'BS – Chemistry' THEN ARRAY['Pre-Engineering', 'Pre-Medical']
      WHEN p.name LIKE 'BS – Biotechnology' OR p.name LIKE 'BS – Food Science%' OR p.name LIKE 'BS – Agriculture' OR
           p.name LIKE 'MBBS – Medicine' OR p.name LIKE 'BS – Human Nutrition%' THEN ARRAY['Pre-Medical']
      WHEN p.name LIKE 'BMAS – Military Arts%' THEN ARRAY['Pre-Engineering', 'ICom (Commerce)', 'IA (Arts)']
      ELSE ARRAY['Pre-Engineering']
    END AS subject_groups
) sg_array
CROSS JOIN LATERAL unnest(sg_array.subject_groups) AS sg(subject_group)
WHERE u.name = 'National University of Sciences and Technology (NUST)';

-- =====================================================
-- STEP 9: Insert Program Offering Tests
-- =====================================================

INSERT INTO program_offering_tests (offering_id, test_type_id, min_score)
SELECT 
  po.id,
  ett.id,
  CASE 
    WHEN ett.name = 'NUMS MDCAT' THEN 55.0
    ELSE 60.0
  END AS min_score
FROM program_offerings po
JOIN programs p ON po.program_id = p.id
JOIN campuses c ON po.campus_id = c.id
JOIN universities u ON c.university_id = u.id
JOIN entrance_test_types ett ON (
  -- Engineering Programs
  (p.name LIKE 'BE –%' AND ett.name = 'NET-Engineering') OR
  -- Computing Programs
  ((p.name = 'BS – Computer Science' OR p.name = 'BS – Data Science' OR 
    p.name = 'BS – Artificial Intelligence' OR p.name = 'BS – Bioinformatics') AND ett.name = 'NET-Computing') OR
  -- Business & Social Sciences Programs
  ((p.name = 'BBA – Business Administration' OR p.name = 'BS – Accounting and Finance' OR 
    p.name = 'BS – Tourism & Hospitality Management' OR p.name = 'BS – Economics' OR 
    p.name = 'BS – Mass Communication' OR p.name = 'BS – Public Administration' OR 
    p.name = 'BS – Psychology' OR p.name = 'BS – English Language & Literature' OR
    p.name = 'BMAS – Military Arts and Science') AND ett.name = 'NET-Business Studies & Social Sciences') OR
  -- Law Program
  (p.name = 'LLB – Laws' AND ett.name = 'HEC LAT') OR
  -- Architecture Programs
  ((p.name = 'B.ARCH – Architecture' OR p.name = 'BS – Industrial Design') AND ett.name = 'NET-Architecture') OR
  -- Natural Sciences Programs
  (p.name = 'BS – Mathematics' AND ett.name = 'NET-Mathematics') OR
  (p.name = 'BS – Physics' AND ett.name = 'NET-Physics') OR
  (p.name = 'BS – Chemistry' AND ett.name = 'NET-Chemistry') OR
  -- Biosciences Programs
  ((p.name = 'BS – Biotechnology' OR p.name = 'BS – Food Science and Technology' OR 
    p.name = 'BS – Agriculture' OR p.name = 'BS – Human Nutrition and Dietetics') AND ett.name = 'NET-Applied Sciences') OR
  -- Medicine Program
  (p.name = 'MBBS – Medicine' AND ett.name = 'NUMS MDCAT')
)
WHERE u.name = 'National University of Sciences and Technology (NUST)';

-- =====================================================
-- STEP 10: Insert Program Offering Tags
-- =====================================================

INSERT INTO program_offering_tags (offering_id, tag_id)
SELECT DISTINCT
  po.id,
  t.id
FROM program_offerings po
JOIN programs p ON po.program_id = p.id
JOIN campuses c ON po.campus_id = c.id
JOIN universities u ON c.university_id = u.id
JOIN tags t ON (
  -- Engineering Programs
  (p.name = 'BE – Electrical Engineering' AND t.name IN ('engineering', 'electrical-engineering')) OR
  (p.name = 'BE – Software Engineering' AND t.name IN ('engineering', 'software-engineering')) OR
  (p.name = 'BE – Mechanical Engineering' AND t.name IN ('engineering', 'mechanical-engineering')) OR
  (p.name = 'BE – Aerospace Engineering' AND t.name IN ('engineering', 'aerospace-engineering')) OR
  (p.name = 'BE – Metallurgy & Materials Engineering' AND t.name IN ('engineering', 'metallurgical-engineering')) OR
  (p.name = 'BE – Chemical Engineering' AND t.name IN ('engineering', 'chemical-engineering')) OR
  (p.name = 'BE – Environmental Engineering' AND t.name IN ('engineering', 'environmental-engineering')) OR
  (p.name = 'BE – Civil Engineering' AND t.name IN ('engineering', 'civil-engineering')) OR
  (p.name = 'BE – Geoinformatics Engineering' AND t.name IN ('engineering', 'geoinformatics-engineering')) OR
  (p.name = 'BE – Mechatronics Engineering' AND t.name IN ('engineering', 'mechatronics-engineering')) OR
  (p.name = 'BE – Computer Engineering' AND t.name IN ('engineering', 'computer-systems')) OR
  (p.name = 'BE – Information Security Engineering' AND t.name IN ('engineering', 'information-security-engineering')) OR
  (p.name = 'BE – Avionics Engineering' AND t.name IN ('engineering', 'avionics-engineering')) OR
  (p.name = 'BE – Naval Architecture Engineering' AND t.name IN ('engineering', 'naval-architecture-engineering')) OR
  
  -- Computing Programs
  (p.name = 'BS – Computer Science' AND t.name IN ('computer-science')) OR
  (p.name = 'BS – Data Science' AND t.name IN ('computer-science', 'data-science')) OR
  (p.name = 'BS – Artificial Intelligence' AND t.name IN ('computer-science', 'artificial-intelligence')) OR
  (p.name = 'BS – Bioinformatics' AND t.name IN ('computer-science', 'bioinformatics')) OR
  
  -- Business Programs
  (p.name = 'BBA – Business Administration' AND t.name IN ('business-administration')) OR
  (p.name = 'BS – Accounting and Finance' AND t.name IN ('accounting', 'finance')) OR
  (p.name = 'BS – Tourism & Hospitality Management' AND t.name IN ('tourism', 'hospitality-management')) OR
  
  -- Social Sciences Programs
  (p.name = 'BS – Economics' AND t.name IN ('economics')) OR
  (p.name = 'BS – Mass Communication' AND t.name IN ('mass-communication')) OR
  (p.name = 'BS – Public Administration' AND t.name IN ('public-administration')) OR
  (p.name = 'BS – Psychology' AND t.name IN ('psychology')) OR
  (p.name = 'BS – English Language & Literature' AND t.name IN ('english')) OR
  (p.name = 'LLB – Laws' AND t.name IN ('law')) OR
  
  -- Architecture & Arts Programs
  (p.name = 'B.ARCH – Architecture' AND t.name IN ('architecture')) OR
  (p.name = 'BS – Industrial Design' AND t.name IN ('industrial-design')) OR
  
  -- Natural Sciences Programs
  (p.name = 'BS – Mathematics' AND t.name IN ('mathematics')) OR
  (p.name = 'BS – Physics' AND t.name IN ('physics')) OR
  (p.name = 'BS – Chemistry' AND t.name IN ('chemistry')) OR
  
  -- Biosciences Programs
  (p.name = 'BS – Biotechnology' AND t.name IN ('biotechnology')) OR
  (p.name = 'BS – Food Science and Technology' AND t.name IN ('food-science')) OR
  (p.name = 'BS – Agriculture' AND t.name IN ('agriculture')) OR
  
  -- Health Sciences Programs
  (p.name = 'MBBS – Medicine' AND t.name IN ('medicine')) OR
  (p.name = 'BS – Human Nutrition and Dietetics' AND t.name IN ('nutrition', 'dietetics')) OR
  
  -- Military Programs
  (p.name = 'BMAS – Military Arts and Science' AND t.name IN ('military-studies'))
)
WHERE u.name = 'National University of Sciences and Technology (NUST)';

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Check university insertion
SELECT 'University' as entity, COUNT(*) as count FROM universities WHERE name = 'National University of Sciences and Technology (NUST)';

-- Check campuses
SELECT 'Campuses' as entity, COUNT(*) as count FROM campuses c 
JOIN universities u ON c.university_id = u.id 
WHERE u.name = 'National University of Sciences and Technology (NUST)';

-- Check programs
SELECT 'Programs' as entity, COUNT(*) as count FROM programs 
WHERE name LIKE 'BE –%' OR name LIKE 'BS –%' OR name LIKE 'BBA –%' OR name LIKE 'B.ARCH –%' OR name LIKE 'LLB –%' OR name LIKE 'MBBS –%' OR name LIKE 'BMAS –%';

-- Check program offerings
SELECT 'Program Offerings' as entity, COUNT(*) as count FROM program_offerings po
JOIN campuses c ON po.campus_id = c.id
JOIN universities u ON c.university_id = u.id
WHERE u.name = 'National University of Sciences and Technology (NUST)';

-- Check entrance tests
SELECT 'Entrance Tests' as entity, COUNT(*) as count FROM entrance_test_types 
WHERE name LIKE 'NET-%' OR name = 'NUMS MDCAT' OR name = 'HEC LAT' OR name = 'ACT/SAT';

-- Check tags
SELECT 'Tags' as entity, COUNT(*) as count FROM tags 
WHERE name LIKE '%-engineering' OR name LIKE 'computer-%' OR name LIKE 'business-%' OR name LIKE '%-science' OR name IN ('medicine', 'law', 'architecture', 'military-studies');

-- Check program offering tests
SELECT 'Program Offering Tests' as entity, COUNT(*) as count FROM program_offering_tests pot
JOIN program_offerings po ON pot.offering_id = po.id
JOIN campuses c ON po.campus_id = c.id
JOIN universities u ON c.university_id = u.id
WHERE u.name = 'National University of Sciences and Technology (NUST)';

-- Check program offering tags
SELECT 'Program Offering Tags' as entity, COUNT(*) as count FROM program_offering_tags pot
JOIN program_offerings po ON pot.offering_id = po.id
JOIN campuses c ON po.campus_id = c.id
JOIN universities u ON c.university_id = u.id
WHERE u.name = 'National University of Sciences and Technology (NUST)';

-- =====================================================
-- COMPLETION MESSAGE
-- =====================================================

SELECT 'NUST University data insertion completed successfully!' as status;