# Flow Log Parser

## Overview
This is a program that can parse a file containing flow log data and maps each row to a tag based on a lookup table. The lookup table is defined as a CSV file with three columns: `dstport`, `protocol`, and `tag`. The program generates an output file containing counts of tags and port/protocol combinations found in the logs.

## Assumptions
- The program **only supports default flow log format** and does not handle custom formats.
- **Only version 2 of the flow logs** is supported.
- The lookup table **must be a properly formatted CSV file** with a header row.
- If a duplicate entry exists in the lookup table for the same `dstport` and `protocol`, the **first occurrence is used**, and a warning is printed.
- If a flow log entry's `dstport` and `protocol` do not match any lookup entry, it is categorized as **"Untagged."**
- Protocol numbers are mapped using a predefined `PROTOCOL_MAP` dictionary with protocals based on based on [IANA registry](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)

## Dependencies
- Python 3.x
- `csv`
- `collections.defaultdict`
- `argparse`

## Installation
Ensure Python 3 is installed on your system. No additional packages are required beyond the standard library.

## Usage
To run the program, use the following command:

```sh
python3 flow_log_parser.py <flow_log_file_path> <lookup_file_path> <output_file>
```

### Example:
```sh
python3 flow_log_parser.py tests/sample_flow_logs.txt tests/lookup_table.csv output.txt
```

## Output
The program generates an output file with two main sections:

1. **Tag Counts:**
   - Count of matches for each tag.

2. **Port/Protocol Combination Counts:**
   - Count of matches for each port/protocol combination.

Example Output:
```
-------Tag Counts:-------
Tag,Count
sv_P2,1
sv_P1,2
sv_P4,1
email,3
Untagged,9

-------Port/Protocol Combination Counts:-------
Port,Protocol,Count
22,tcp,1
23,tcp,1
25,tcp,1
110,tcp,1
143,tcp,1
443,tcp,1
993,tcp,1
1024,tcp,1
49158,tcp,1
80,tcp,1
```

## Testing
### Unit Tests:
The program includes test cases that check:
- Proper parsing of the lookup table.
- Handling of duplicate lookup entries.
- Correct classification of flow log entries.
- Accurate generation of tag and port/protocol counts.
- Edge cases listed below

To run tests:
```sh
pytest test_parser.py
```
If this is not working, please use a virtual enviornment:
```sh
python3 -m venv venv
source venv/bin/activate # activate on macOS/Linux
#or
venv\Scripts\activate  # Activate on Windows
pip install -r requirements.txt
cd tests
PYTHONPATH=$(pwd)/.. pytest
```


### Edge Cases Considered:
- **Malformed flow logs** (e.g., missing fields, incorrect format) are skipped.
- **Lookup table with missing or empty tags** prints a warning and skips those entries.
- **Unknown protocol numbers** are categorized under "unknown protocol."
- **Empty or non-matching entries** are counted as "Untagged."
- **Case Insensitivity** The matches should be case insensitive
- **Empty Lookup tables/flow log files** Assumed untagged will still be counted.
- **Handling Different Line Endings (CRLF vs. LF)** Manually tested

## Known Limitations
- The program does not support **custom flow log formats**.
- The lookup table must be well-formed; the program does not handle syntax errors in the CSV.
- The program currently **does not support multi-threading or parallel processing**.

## Efficiency Analysis
### **Constructing the Lookup Table (`construct_lookup_table`)**
- Reads a CSV file **line by line** and stores entries in a dictionary.
- **Time Complexity:** **O(N)** (where N is the number of rows in the lookup file).  
- Uses **dictionary lookups (`O(1)`)** for checking duplicates.

### **Parsing the Flow Log (`parse_flow_log`)**
- Reads the log **line by line** and extracts necessary fields.
- **Dictionary-based tagging (`O(1)`)** allows fast lookups.
- **Overall Complexity:** **O(M)** (where M is the number of log entries).

### **Generating Output (`generate_output_file`)**
- Writes results to a file in **O(P + Q)** (where P is the number of tags, and Q is the number of port-protocol pairs).

## **4. Summary of Efficiency**
| **Operation**                  | **Time Complexity** | **Space Complexity** | **Bottleneck?** |
|--------------------------------|--------------------|----------------------|----------------|
| Construct Lookup Table         | O(N)              | O(N)                 | If lookup file is large |
| Parse Flow Log                | O(M)              | O(M)                 | If log file is huge |
| Dictionary Lookups             | O(1) (avg), O(N) (worst) | O(N) | Only if hash collisions occur |
| Write Output File              | O(P + Q)          | O(1)                 | Only for very large outputs |

## Future Enhancements
- Add support for more flow log versions.
- Implement a GUI or web interface for user-friendly interactions.
- Allow users to define custom protocol mappings dynamically.


## Author
Daphne Wu

