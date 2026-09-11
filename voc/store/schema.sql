-- SQLite index derived from the files under data/. Rebuilt by `voc build-db`.
-- Double-brace placeholders are replaced with taxonomy enums by voc/store/db.py.

CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT);

CREATE TABLE calls (
    call_id TEXT PRIMARY KEY, source TEXT NOT NULL, shape TEXT NOT NULL CHECK (shape IN ({{shape}})),
    date TEXT NOT NULL, week TEXT NOT NULL, month TEXT NOT NULL,
    text TEXT NOT NULL, text_sha TEXT NOT NULL,
    product TEXT NOT NULL CHECK (product IN ({{products}})),
    product_raw TEXT, sub_product_raw TEXT, issue_raw TEXT, sub_issue_raw TEXT,
    region TEXT NOT NULL, region_group TEXT NOT NULL CHECK (region_group IN ({{region_group}})),
    channel TEXT NOT NULL CHECK (channel IN ({{channel}})),
    segment TEXT NOT NULL CHECK (segment IN ({{segment}})),
    company TEXT NOT NULL, sampling_fraction REAL NOT NULL,
    n_turns INTEGER, customer_char_ranges TEXT, meta TEXT
);
CREATE INDEX idx_calls_date ON calls(date);
CREATE INDEX idx_calls_week ON calls(week);
CREATE INDEX idx_calls_month ON calls(month);
CREATE INDEX idx_calls_product ON calls(product);

CREATE TABLE extractions (
    call_id TEXT PRIMARY KEY REFERENCES calls(call_id),
    status TEXT NOT NULL, produced_by TEXT, model TEXT, prompt_version TEXT, schema_version TEXT, extracted_at TEXT,
    overall_sentiment INTEGER, resolution_status TEXT, customer_ask TEXT,
    stated_reason TEXT, underlying_driver TEXT, reason_differs INTEGER,
    redaction_heavy INTEGER, summary TEXT, quote_verify_rate REAL, flags TEXT, json TEXT
);

CREATE TABLE call_reasons (
    call_id TEXT NOT NULL REFERENCES calls(call_id),
    reason TEXT NOT NULL CHECK (reason IN ({{contact_reasons}})),
    specific_reason TEXT, is_primary INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (call_id, reason)
);
CREATE INDEX idx_call_reasons_reason ON call_reasons(reason);

CREATE TABLE call_products (
    call_id TEXT NOT NULL REFERENCES calls(call_id),
    product TEXT NOT NULL CHECK (product IN ({{products}})),
    PRIMARY KEY (call_id, product)
);

CREATE TABLE call_services (
    call_id TEXT NOT NULL REFERENCES calls(call_id),
    service TEXT NOT NULL CHECK (service IN ({{services}})),
    PRIMARY KEY (call_id, service)
);

CREATE TABLE topics (
    topic_id TEXT PRIMARY KEY, call_id TEXT NOT NULL REFERENCES calls(call_id), idx INTEGER NOT NULL,
    topic_label TEXT, issue_statement TEXT NOT NULL,
    product TEXT NOT NULL CHECK (product IN ({{products}})),
    sentiment INTEGER NOT NULL CHECK (sentiment BETWEEN -2 AND 2),
    driver_category TEXT NOT NULL CHECK (driver_category IN ({{driver_categories}})),
    driver TEXT, outcome TEXT, evidence_ok INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX idx_topics_call ON topics(call_id);
CREATE INDEX idx_topics_driver ON topics(driver_category);

CREATE TABLE evidence (
    evidence_id TEXT PRIMARY KEY, topic_id TEXT NOT NULL REFERENCES topics(topic_id),
    call_id TEXT NOT NULL REFERENCES calls(call_id),
    quote TEXT NOT NULL, char_start INTEGER, char_end INTEGER, speaker TEXT,
    verified INTEGER NOT NULL DEFAULT 0, match_kind TEXT
);
CREATE INDEX idx_evidence_topic ON evidence(topic_id);
CREATE INDEX idx_evidence_call ON evidence(call_id);

CREATE TABLE positive_moments (
    pm_id TEXT PRIMARY KEY, call_id TEXT NOT NULL REFERENCES calls(call_id),
    what TEXT, category TEXT, quote TEXT, char_start INTEGER, char_end INTEGER, speaker TEXT,
    verified INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE themes (
    theme_id TEXT PRIMARY KEY, name TEXT NOT NULL, problem_statement TEXT, root_cause TEXT,
    polarity TEXT NOT NULL CHECK (polarity IN ({{polarity}})),
    driver_category TEXT, bucket TEXT, status TEXT NOT NULL, merged_into TEXT, effective_theme_id TEXT,
    created_pass TEXT, codebook_version INTEGER,
    n_calls INTEGER DEFAULT 0, n_wordings INTEGER DEFAULT 0, n_products INTEGER DEFAULT 0,
    first_seen_week TEXT, grouping_quality TEXT DEFAULT 'ok'
);

CREATE TABLE theme_merges (
    from_theme TEXT PRIMARY KEY, into_theme TEXT NOT NULL, pass TEXT, reason TEXT, judged_by TEXT, created_at TEXT
);

CREATE TABLE theme_members (
    topic_id TEXT PRIMARY KEY REFERENCES topics(topic_id),
    theme_id TEXT NOT NULL, effective_theme_id TEXT NOT NULL,
    confidence REAL, pass TEXT, batch_id TEXT
);
CREATE INDEX idx_members_effective ON theme_members(effective_theme_id);

CREATE TABLE theme_wordings (
    theme_id TEXT NOT NULL, rank INTEGER NOT NULL, topic_id TEXT NOT NULL, call_id TEXT NOT NULL,
    issue_statement TEXT NOT NULL, product TEXT, date TEXT,
    PRIMARY KEY (theme_id, rank)
);

CREATE TABLE period_totals (
    period_kind TEXT NOT NULL, period TEXT NOT NULL, n_calls INTEGER NOT NULL, population_n INTEGER,
    PRIMARY KEY (period_kind, period)
);

CREATE TABLE dim_totals (dim TEXT NOT NULL, value TEXT NOT NULL, n_calls INTEGER NOT NULL, PRIMARY KEY (dim, value));

CREATE TABLE entity_period (
    entity_type TEXT NOT NULL, entity_id TEXT NOT NULL, period_kind TEXT NOT NULL, period TEXT NOT NULL,
    n_calls INTEGER NOT NULL, share REAL, neg_mass REAL, pos_mass REAL, mean_sentiment REAL,
    PRIMARY KEY (entity_type, entity_id, period_kind, period)
);

CREATE TABLE entity_dim (
    entity_type TEXT NOT NULL, entity_id TEXT NOT NULL, dim TEXT NOT NULL, value TEXT NOT NULL,
    n_calls INTEGER NOT NULL, n_slice INTEGER NOT NULL, share REAL, ci_lo REAL, ci_hi REAL, lift REAL,
    suppressed INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (entity_type, entity_id, dim, value)
);

CREATE TABLE emerging_scores (
    entity_type TEXT NOT NULL, entity_id TEXT NOT NULL, as_of_week TEXT NOT NULL,
    n_recent INTEGER, expected_recent REAL, n_baseline INTEGER, z REAL, ratio REAL, weeks_recent INTEGER,
    share_recent REAL, first_seen_week TEXT, status TEXT, status_8w TEXT, emerging_score REAL,
    novel_vocabulary INTEGER DEFAULT 0, n_tested INTEGER, expected_false_positives REAL,
    PRIMARY KEY (entity_type, entity_id, as_of_week)
);
CREATE INDEX idx_emerging_asof ON emerging_scores(as_of_week, status);

CREATE TABLE answers_cache (
    qhash TEXT PRIMARY KEY, question TEXT NOT NULL, filters TEXT, as_of_week TEXT, data_version TEXT,
    prompt_version TEXT, mode TEXT, model TEXT, effort TEXT, answer TEXT, trace TEXT, validation TEXT, created_at TEXT
);

CREATE TABLE tool_results (
    result_id TEXT PRIMARY KEY, qhash TEXT, tool TEXT NOT NULL, args TEXT, sql TEXT, call_ids TEXT, created_at TEXT
);

CREATE TABLE run_log (
    run_id TEXT, stage TEXT, started_at TEXT, ended_at TEXT, n_ok INTEGER, n_err INTEGER,
    input_tokens INTEGER, output_tokens INTEGER, cache_read_tokens INTEGER, est_usd REAL, args TEXT
);

-- Full-text search (external content tables, populated by build-db)
CREATE VIRTUAL TABLE calls_fts USING fts5(text, content='calls', content_rowid='rowid');
CREATE VIRTUAL TABLE topics_fts USING fts5(issue_statement, topic_label, driver, content='topics', content_rowid='rowid');

-- Views: the SQL-native extension surface
CREATE VIEW v_effective_theme AS
    SELECT topic_id, theme_id, effective_theme_id, confidence, pass FROM theme_members;

CREATE VIEW v_theme_calls AS
    SELECT DISTINCT tm.effective_theme_id AS theme_id, t.call_id
    FROM theme_members tm JOIN topics t ON t.topic_id = tm.topic_id;

CREATE VIEW v_topic_full AS
    SELECT t.topic_id, t.call_id, t.idx, t.topic_label, t.issue_statement, t.product AS topic_product,
           t.sentiment, t.driver_category, t.driver, t.outcome, t.evidence_ok,
           c.date, c.week, c.month, c.product, c.region, c.region_group, c.channel, c.segment, c.company,
           tm.effective_theme_id AS theme_id, tm.confidence AS theme_confidence,
           (SELECT COUNT(*) FROM evidence e WHERE e.topic_id = t.topic_id AND e.verified = 1) AS n_verified_evidence
    FROM topics t JOIN calls c ON c.call_id = t.call_id
    LEFT JOIN theme_members tm ON tm.topic_id = t.topic_id;

CREATE VIEW v_theme_call_sentiment AS
    SELECT tm.effective_theme_id AS theme_id, t.call_id,
           MIN(t.sentiment) AS min_sentiment, MAX(t.sentiment) AS max_sentiment
    FROM theme_members tm JOIN topics t ON t.topic_id = tm.topic_id
    GROUP BY tm.effective_theme_id, t.call_id;

CREATE VIEW v_theme_summary AS
    SELECT th.theme_id, th.name, th.problem_statement, th.root_cause, th.polarity, th.driver_category,
           th.status, th.n_wordings, th.n_products, th.first_seen_week, th.grouping_quality,
           COUNT(s.call_id) AS n_calls,
           SUM(CASE WHEN s.min_sentiment < 0 THEN -s.min_sentiment ELSE 0 END) AS neg_mass,
           SUM(CASE WHEN s.max_sentiment > 0 THEN s.max_sentiment ELSE 0 END) AS pos_mass,
           AVG(CASE WHEN th.polarity = 'positive' THEN s.max_sentiment ELSE s.min_sentiment END) AS mean_sentiment
    FROM themes th LEFT JOIN v_theme_call_sentiment s ON s.theme_id = th.theme_id
    WHERE th.status IN ('active', 'catch_all')
    GROUP BY th.theme_id;

CREATE VIEW v_negative_drivers AS
    SELECT * FROM v_theme_summary WHERE polarity = 'negative' AND status = 'active' ORDER BY neg_mass DESC;

CREATE VIEW v_positive_experiences AS
    SELECT * FROM v_theme_summary WHERE polarity = 'positive' AND status = 'active' ORDER BY pos_mass DESC;

CREATE VIEW v_reason_by_month AS
    SELECT c.month, r.reason, COUNT(DISTINCT r.call_id) AS n_calls,
           SUM(CASE WHEN r.is_primary = 1 THEN 1 ELSE 0 END) AS n_primary
    FROM call_reasons r JOIN calls c ON c.call_id = r.call_id
    GROUP BY c.month, r.reason;
