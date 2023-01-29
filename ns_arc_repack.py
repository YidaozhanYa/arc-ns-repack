#!/usr/bin/python3
from hashlib import new
import sys
import json
import os

dump_path = "dump"
    
arcpack = open(sys.argv[2],'wb')

arcjson_orig = open(sys.argv[1], 'r')

data = json.load(arcjson_orig)

group_offset = 0
group_length = 0
all_length = 0

new_groups = []
for group in data["Groups"]:
    group_offset += group_length
    group_length = 0
    new_ordered_entries = []
    for ordered_entry in group["OrderedEntries"]:
        file_path = dump_path + "/" + group["Name"] + "/" + ordered_entry["OriginalFilename"]
        with open(file_path, 'rb') as single_file:
            arcpack.write(single_file.read())
            size = single_file.tell()
            group_length += size
            all_length += size
            single_file.close()
            new_ordered_entries.append({
                "OriginalFilename": ordered_entry["OriginalFilename"],
                "Offset": all_length - size,
                "Length": size
            })
    new_groups.append({
        "Name": group["Name"],
        "Offset": group_offset,
        "Length": group_length,
        "OrderedEntries": new_ordered_entries
    })
with open(sys.argv[3], 'w', newline='\r\n') as arcjson_new:
    arcjson_new.write(json.dumps({
        "Groups": new_groups
    }, indent=2))
    arcjson_new.close()
arcpack.close() 
