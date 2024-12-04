# adobe-coding-challenge

## Purpose:

Removes duplicate leads based on `_id` and `email` from a JSON file.

### Deduplication Rules:

1. Prefer the record with the latest `entryDate`.
2. If dates are the same, prefer the later record in the input list

## How to Run:

Execute the script `deduplicate.py` in the command line and type/input the JSON file path when prompted.

## Input:

Path to JSON file (e.g. `leads.json`) with a list of leads, each containing fields `_id`, `email`, `firstName`, `lastName`, `address`, and `entryDate`.

## Output:

1. `deduplicated_leads.json`: Contains the deduplicated list of leads.
2. `changelog.json`: Logs changes, showing replaced records and field-level updates. (If a new record is compared and should _not_ replace an existing record, it is _not_ recorded in the changelog since nothing was replaced.)
