import json
markers = dict()
with open("datasets/updated_aaec_para/updated_aaec_para_test_markers_only.json", "r") as json_file:
        dataset = json.load(json_file)
        
                            
for example in dataset:
    id = example['id']
    if id not in markers:
        markers[id] = []   
    markers[id].append(example)


# print(markers)    
    
    
for i in markers:
    print(f"{i}:{markers[i]}")
    print("\n")
