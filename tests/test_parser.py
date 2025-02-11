#test file for flow_log_parser.py
from flow_log_parser import parse_flow_log, generate_output_file, construct_lookup_table

# general test to see if the parser is working
def test_parse_flow_log():
    file_path = "../test_files/test_flow_log.txt"
    output_file_path = "../test_files/output/test_output.csv"
    tag_count, port_proto_count = parse_flow_log(file_path, construct_lookup_table('../test_files/look1.csv'))
    generate_output_file(tag_count, port_proto_count, output_file_path)

    assert tag_count == {
        "sv_P1": 2,
        "sv_P2": 1,
        "Untagged": 2
    }

    assert port_proto_count == {
        ("49153", "tcp"): 1,
        ("49154", "tcp"): 1,
        ("49155", "tcp"): 1,
        ("49156", "udp"): 1,
        ("49157", "any private encryption scheme"): 1
    }

# test to see if the parser is working with case insensitivity
def test_parse_case_insensitivity():
    file_path = "../test_files/test_flow_log2.txt"
    output_file_path = "../test_files/output/test_output2.csv"
    tag_count, port_proto_count = parse_flow_log(file_path, construct_lookup_table('../test_files/look2.csv'))
    generate_output_file(tag_count, port_proto_count, output_file_path)

    assert tag_count == {
        "sv_P1": 2,
        "sv_P2": 1,
        "Untagged": 2
    }

    assert port_proto_count == {
        ("49153", "tcp"): 1,
        ("49154", "tcp"): 1,
        ("49155", "tcp"): 1,
        ("49156", "udp"): 1,
        ("49157", "any private encryption scheme"): 1
    }

# test to see if parser is working with empty logs
def test_parse_empty_logs():
    file_path = "../test_files/test_flow_log3.txt"
    output_file_path = "../test_files/output/test_output3.csv"
    tag_count, port_proto_count = parse_flow_log(file_path, construct_lookup_table('../test_files/look2.csv'))
    generate_output_file(tag_count, port_proto_count, output_file_path)

    assert tag_count == {
        "Untagged": 0
    }

    assert port_proto_count == {
    }

# test to see if parser is working with empty lookup table
def test_parse_empty_lookup():
    file_path = "../test_files/test_flow_log2.txt"
    output_file_path = "../test_files/output/test_output4.csv"
    tag_count, port_proto_count = parse_flow_log(file_path, construct_lookup_table('../test_files/look3.csv'))
    generate_output_file(tag_count, port_proto_count, output_file_path)

    assert tag_count == {
        "Untagged": 5
    }

    assert port_proto_count == {
        ("49153", "tcp"): 1,
        ("49154", "tcp"): 1,
        ("49155", "tcp"): 1,
        ("49156", "udp"): 1,
        ("49157", "any private encryption scheme"): 1
    }

# test to see if parser is working with duplicate lookup table entries
def test_parse_duplicate_lookup():
    file_path = "../test_files/test_flow_log2.txt"
    output_file_path = "../test_files/output/test_output5.csv"
    tag_counts, port_proto_counts = parse_flow_log(file_path, construct_lookup_table('../test_files/look4.csv'))
    generate_output_file(tag_counts, port_proto_counts, output_file_path)

    assert tag_counts == {
        "sv_P1": 2,
        "sv_P2": 1,
        "Untagged": 2
    }

    assert port_proto_counts == {
        ("49153", "tcp"): 1,
        ("49154", "tcp"): 1,
        ("49155", "tcp"): 1,
        ("49156", "udp"): 1,
        ("49157", "any private encryption scheme"): 1
    }

# test to see if parser is working with malformed logs
def test_parse_malformed_logs():
    file_path = "../test_files/test_flow_log4.txt"
    output_file_path = "../test_files/output/test_output6.csv"
    tag_count, port_proto_count = parse_flow_log(file_path, construct_lookup_table('../test_files/look4.csv'))
    generate_output_file(tag_count, port_proto_count, output_file_path)

    assert tag_count == {
        "sv_P1": 2,
        "Untagged": 1
    }

    assert port_proto_count == {
        ("49153", "tcp"): 1,
        ("49155", "tcp"): 1,
        ("49156", "udp"): 1,
    }

# test to see if parser is working with malformed lookup table
def test_parse_malformed_lookup():
    file_path = "../test_files/test_flow_log2.txt"
    output_file_path = "../test_files/output/test_output7.csv"
    tag_count, port_proto_count = parse_flow_log(file_path, construct_lookup_table('../test_files/look5.csv'))
    generate_output_file(tag_count, port_proto_count, output_file_path)

    assert tag_count == {
        "sv_P1": 2,
        "Untagged": 3
    }

    assert port_proto_count == {
        ("49153", "tcp"): 1,
        ("49154", "tcp"): 1,
        ("49155", "tcp"): 1,
        ("49156", "udp"): 1,
        ("49157", "any private encryption scheme"): 1
    }