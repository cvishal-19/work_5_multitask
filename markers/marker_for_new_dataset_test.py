import json
import copy
import string

splits=['test']
for split in splits:
    json_filename = f"updated_aaec_para_test.json"
    
    with open(json_filename, "r") as json_file:
        dataset = json.load(json_file)
    
    #example_iterator = -1
    markers = dict()
    #unique_chars=set()
    #ent=set()
    for entry in dataset:
        identifier=entry["id"]
        components = entry["components"]
        paragraph=entry["paragraph"]
        relations=entry["relations"]
        #noise=entry["noise"]
        #for char in paragraph:
        #    if char=='+':
         #       ent.add(entry["id"])
          #  unique_chars.add(char)
        
        comp_end_indexes = []
        for item in components:
           end_index = item["end"]
           comp_end_indexes.append(end_index)
        
        for component in components:
            start = component["start"]
            end = component["end"]
            contenttype=component["type"]
            span=component["span"]
            
            reverse_char=[]
            
            i=start-2
            while i>=0:
                char=paragraph[i]
                #checked on internet these are only possible in most cases and 
                #in the unique_chars got following
                #{'K', 'x', 's', '6', '.', '3', 'N', '\n', 'c', 'M', 'G', 'e', 'l', 'j', '(', '9', 'U', ':', 'R', 'E', '/', '“', 'J', 'é', 'P', 'O', '7', 'g', 'S', 'y', 'Z', 'L', '%', 'V', 'h', ';', "'", '”', 'T', 'a', 'Y', 'r', 'w', 'z', 'i', ',', 'W', 'H', '?', '&', 'Q', 'm', '0', 'q', 'D', '!', '8', 'u', 'A', 'B', 't', '–', 'b', 'n', '-', '1', '4', 'v', 'd', 'F', 'f', 'k', 'I', '+', '5', 'C', '’', 'o', '‘', 'X', '"', '\t', ' ', 'p', '2', ')'}
                
                #so according to me these are only characters possible for 
                #end of sentence
                if char=='.' or char=='?' or char=='!' or i in comp_end_indexes:
                    i+=1
                    if reverse_char:
                        reverse_char=reverse_char[:-1]
                    break
                else:
                    reverse_char.append(char)
                    i-=1
                    
            reverse_char = reverse_char[::-1]
            backward_sentence= "".join(reverse_char)
            
            if backward_sentence and not all(char in string.punctuation for char in backward_sentence):
               marker_dict = dict()  # Create a new dictionary for each component
               
               marker_dict["start"] = i + 1
               marker_dict["end"] = start - 2
            
               for component in components:
                    if component['start'] == (marker_dict['end'] + 2):
                        marker_dict['followed_by'] = component['type']
                        
               if paragraph[marker_dict["end"]] in string.punctuation:
                   marker_dict["end"]=marker_dict["end"]-1
                   backward_sentence = backward_sentence[:-1]
               
               marker_dict["length"] = marker_dict["end"] - marker_dict["start"] + 1
               
               marker_dict["span"] = backward_sentence
               
               exists = any(all(d[key] == marker_dict[key] for key in marker_dict if key != "id") for d in markers)
               
               if not exists:
                   marker_dict["id"] = entry["id"]
                #    new_dict["id"] = marker_dict
                   markers["id"].append((marker_dict))

#print(ent)
#print(unique_chars)

output_json_filename = f"result_for_new_dataset_test.json"  # Change the output file name as needed
with open(output_json_filename, "w") as outfile:
    
    json.dump(markers, outfile, indent=4)



sorted_markers = sorted(markers, key=lambda x: x['length'])
for marker in sorted_markers:
    print(f"Marker:  {marker['span']}\nLength:  {marker['length']}\nID:  {marker['id']}\nBoundary:  {marker['start']} to {marker['end']}\n")
               
            
            
            
            
            
            
            
