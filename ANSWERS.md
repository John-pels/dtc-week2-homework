# Module 2 Homework - Answer Sheet

## Quick Reference

| Question | Answer                            | Details                                                |
| -------- | --------------------------------- | ------------------------------------------------------ |
| 1        | **A. 128.3 MiB**                  | Yellow taxi Dec 2020 uncompressed file size            |
| 2        | **B. green_tripdata_2020-04.csv** | Rendered variable with taxi=green, year=2020, month=04 |
| 3        | **B. 24,648,499**                 | Total rows for Yellow taxi 2020 (all months)           |
| 4        | **C. 1,734,051**                  | Total rows for Green taxi 2020 (all months)            |
| 5        | **C. 1,925,152**                  | Rows for Yellow taxi March 2021                        |
| 6        | **B. timezone: America/New_York** | Correct timezone configuration for NYC                 |

---

## Detailed Answers

### Question 1: Yellow Taxi December 2020 - Uncompressed File Size

**Answer: A. 128.3 MiB**

The uncompressed CSV file `yellow_tripdata_2020-12.csv` is exactly 128.3 MiB.

---

### Question 2: Variable Rendering

**Answer: B. green_tripdata_2020-04.csv**

When the variable template `{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv` is rendered with:

- taxi = "green"
- year = "2020"
- month = "04"

The result is: `green_tripdata_2020-04.csv`

---

### Question 3: Yellow Taxi 2020 - Total Rows

**Answer: B. 24,648,499**

Aggregating all 12 months of Yellow taxi data for 2020 gives a total of 24,648,499 rows.

---

### Question 4: Green Taxi 2020 - Total Rows

**Answer: C. 1,734,051**

Aggregating all 12 months of Green taxi data for 2020 gives a total of 1,734,051 rows.

---

### Question 5: Yellow Taxi March 2021 - Rows

**Answer: C. 1,925,152**

The Yellow taxi data for March 2021 contains 1,925,152 rows.

---

### Question 6: Timezone Configuration

**Answer: B. Add a timezone property set to America/New_York in the Schedule trigger configuration**

Kestra uses the IANA Time Zone Database. The correct configuration is:

```yaml
triggers:
  - id: schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 0 1 * *"
    timezone: America/New_York
```

Not:

- ❌ `timezone: EST` (doesn't account for daylight saving)
- ❌ `timezone: UTC-5` (not IANA format)
- ❌ `location: New_York` (wrong property name)

---

## How to Verify

Run the analysis script to verify all answers:

```bash
uv run scripts/answer_homework.py
```

This will download the necessary data files and compute all answers automatically.
