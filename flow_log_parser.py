import csv
from collections import defaultdict
import argparse

from protocol_map import PROTOCOL_MAP

# construct lookup table from csv file
def construct_lookup_table(file_path):
    lookup_table = {}
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            if len(row) < 3:
                continue
            dst_port, proto, tag = map(str.strip, row)
            input = (dst_port.lower(), proto.lower())

            if input in lookup_table:
                print(f"WARNING: There was a duplicate entry for {input}. First occurrence was kept: {lookup_table[input]}")
            else:
                lookup_table[input] = tag
    return lookup_table

# export lookup table to csv file
def export_lookup_table(lookup_table, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["dstport", "protocol", "tag"])  # header row
        for (dst_port, proto), tag in lookup_table.items():
            writer.writerow([dst_port, proto, tag])
    print(f"lookup table: {output_file}")

# parse flow log and apply tags
def parse_flow_log(file_path, lookup_table):
    tag_count = defaultdict(int)
    port_proto_count = defaultdict(int)
    untagged_count = 0

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        for row in file:
            fields = row.strip().split()
            if len(fields) < 13:
                continue
            dst_port, proto_num = fields[6], fields[7]
            proto = PROTOCOL_MAP.get(int(proto_num), "unknown protocol")
            input = (dst_port.lower(), proto.lower())
            #print(f"DEBUG: flow log entry - dst_port: {dst_port}, protocol: {protocol}, input: {input}")

            if input in lookup_table:
                tag = lookup_table[input]
                tag_count[tag] += 1
               # print(f"DEBUG: found untagged: {input}, {tag}")  
            else:

                untagged_count += 1
                tag = "Untagged"

            #print(f"DEBUG: port {input}, proto {protocol}")  
            port_proto_count[input] += 1

    tag_count["Untagged"] = untagged_count
    return tag_count, port_proto_count

# generate output file from tag and port/protocol counts
def generate_output_file(tag_count, port_proto_count, file_path):
    with open(file_path, mode='w', encoding='utf-8') as file:
        file.write("-------Tag Counts:-------\nTag,Count\n")
        #print("DEBUG: tagC:", tag_count)
        for tag, count in tag_count.items():
            file.write(f"{tag.strip().lower()},{count}\n")  # strip spaces before writing
        
        file.write("\n-------Port/Protocol Combination Counts:-------\nPort,Protocol,Count\n")
        #print("DEBUG: port/proto c:", port_proto_count)
        for (port, proto), count in port_proto_count.items():
            file.write(f"{port},{proto},{count}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse flow logs and tag according to lookup table.")
    parser.add_argument("flow_log_file", help="Flow log file path.")
    parser.add_argument("lookup_file", help="Table file path.")
    parser.add_argument("output_file", help="Output file path.")
    args = parser.parse_args()
    
    lookup_table = construct_lookup_table(args.lookup_file)
    # export_lookup_table(lookup_table, "exported_lookup.csv")
    tag_count, port_proto_count = parse_flow_log(args.flow_log_file, lookup_table)
    generate_output_file(tag_count, port_proto_count, args.output_file)
    
    print(f"Processing has finished. The output was written to {args.output_file}")


