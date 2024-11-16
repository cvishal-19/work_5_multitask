import re
import json
# def generate_anl_end_to_end(text, components, relations, entities) -> str:
#     # Add IDs to components
#     index_counter = 0
#     for component in components:
#         component['id'] = index_counter
#         index_counter += 1

#     # Sort components by their start index
#     sorted_components = sorted(components, key=lambda x: x['start'])

#     # Create a dictionary to track which component has which relations
#     relation_dict = {}
#     for relation in relations:
#         relation_type = relation['type']
#         head = relation['head']
#         tail = relation['tail']
#         if head not in relation_dict:
#             relation_dict[head] = []
#         relation_dict[head].append((relation_type, tail))

#     # Generate the formatted output
#     formatted_output = ""
#     prev_end = 0  # Track the end of the previous span

#     for comp in sorted_components:
#         comp_index, comp_type, comp_start, comp_end = comp['id'], comp['type'], comp['start'], comp['end']

#         # Add text before the component span
#         formatted_output += text[prev_end:comp_start]

#         component_text = text[comp_start:comp_end]
#         formatted_output += f"[ {component_text} | {comp_type} "

#         # Add relations if any
#         if comp_index in relation_dict:
#             for relation_type, tail in relation_dict[comp_index]:
#                 tail_component = next(filter(lambda x: x['id'] == tail, components))
#                 tail_text = text[tail_component['start']:tail_component['end']]
#                 formatted_output += f"| {relation_type.capitalize()} = {tail_text} "

#         formatted_output += "]"
#         prev_end = comp_end

#     # Add any remaining text after the last component
#     formatted_output += text[prev_end:]

#     target_output = " ".join(formatted_output.split())  # Remove extra spaces

#     # ADD OUTCOMES ENTITIES
#     outcome_entities = [entity for item in entities if item['type'] == 'outcome' for entity in item['entity']]
#     outcome_string = ', '.join(outcome_entities)
#     outcomes = f"Outcomes: (({outcome_string}))"

#     target_output = f"{target_output}\n{outcomes}"

#     print (target_output)
#     print ("\n")
#     return target_output

def generate_anl_end_to_end(text, components, relations) -> str:
    # Add IDs to components
    index_counter = 0
    for component in components:
        component['id'] = index_counter
        index_counter += 1

    # Sort components by their start index
    sorted_components = sorted(components, key=lambda x: x['start'])

    # Create a dictionary to track which component has which relations
    relation_dict = {}
    for relation in relations:
        relation_type = relation['type']
        head = relation['head']
        tail = relation['tail']
        if head not in relation_dict:
            relation_dict[head] = []
        relation_dict[head].append((relation_type, tail))

    # Generate the formatted output
    formatted_output = ""
    prev_end = 0  # Track the end of the previous span

    for comp in sorted_components:
        comp_index, comp_type, comp_start, comp_end = comp['id'], comp['type'], comp['start'], comp['end']

        # Add text before the component span
        formatted_output += text[prev_end:comp_start]
        
        component_text = text[comp_start:comp_end]
        if comp_index not in relation_dict:
            formatted_output += f" {component_text} "

        # Add relations if any
        if comp_index in relation_dict:
            formatted_output += f"[ {component_text} "
            for relation_type, tail in relation_dict[comp_index]:
                tail_component = next(filter(lambda x: x['id'] == tail, components))
                tail_text = text[tail_component['start']:tail_component['end']]
                formatted_output += f"| {relation_type} | {tail_text} "
            formatted_output += "]"    

        
        prev_end = comp_end

    # Add any remaining text after the last component
    formatted_output += text[prev_end:]

    target_output = " ".join(formatted_output.split())  # Remove extra spaces

    # ADD OUTCOMES ENTITIES
    # outcome_entities = [entity for item in entities if item['type'] == 'outcome' for entity in item['entity']]
    # outcome_string = ', '.join(outcome_entities)
    # outcomes = f"Outcomes: (({outcome_string}))"

    # target_output = f"{outcomes}\n{target_output}"

    # print(target_output)
    # print("\n")
    return target_output




def gen_only_components(text, components):
    index_counter = 0 
    for comp in components:
        comp['id'] = index_counter
        index_counter +=1
    
    sorted_comps = sorted(components, key = lambda x : x['start'])
    
    formatted_output =""
    prev_end = 0
    for comp in sorted_comps:
        comp_index, comp_type, comp_start, comp_end = comp['id'], comp['type'], comp['start'], comp['end']

        formatted_output += text[prev_end:comp_start]

        component_text = text[comp_start:comp_end]
        formatted_output += f"[ {component_text} | {comp_type} "
        
        formatted_output += "]"
        prev_end = comp_end    
    formatted_output += text[prev_end:]
    target_output = " ".join(formatted_output.split())  # Remove extra spaces
    return target_output

def gen_only_markers(text, markers):
    index_counter = 0 
    for comp in markers:
        comp['id'] = index_counter
        index_counter +=1
    
    sorted_markers = sorted(markers, key = lambda x : x['start'])
    
    formatted_output =""
    prev_end = 0
    for comp in sorted_markers:
        comp_index, comp_start, comp_end = comp['id'], comp['start'], comp['end']
        comp_followedby = comp['followed_by']
        formatted_output += text[prev_end:comp_start]

        component_text = text[comp_start:comp_end+1]
        formatted_output += f"(( {component_text} | followed by [ {comp_followedby} ] "
        
        formatted_output += "))"
        prev_end = comp_end+1    
    formatted_output += text[prev_end:]
    target_output = " ".join(formatted_output.split())  # Remove extra spaces
    return target_output
    
# data = 'datasets/test.json'  
# with open(data, "r") as json_file:
#         data = json.load(json_file)  
# for example in data:
#     target_se = generate_anl_end_to_end(example["paragraph"], example["components"], example["relations"])
#     input_se = example['paragraph']
#     print(f"\n\n\n\n{input_se}\n{target_se}")

def prepare_data(dataset):
    input_sentences = []
    target_sentences = []

    for example in dataset:
        input_sen = example["paragraph"]
        target_sen = generate_anl_end_to_end(example["paragraph"], example["components"], example["relations"])
        
        input_sentences.append(input_sen)
        target_sentences.append(target_sen)
        
        # print(f"\n\n\n{input_sen}\n\n{target_sen}")
    return input_sentences, target_sentences


def prepare_data_multitask(val,dataset, marker_datset):
    p_1 = "Markers : " ## target = with only markers
    p_2 = "Components : "  ## target = with only components 
    p_3 = "Relations : " ## target = final with both components and reltions
        
    input_sentences = []
    target_sentences = []
    markers = []
    
    if val == False: 
        for example in dataset:
            id = example['id']
            if id not in marker_datset:
                marker_datset[id] = []
                
            markers = marker_datset[id]
            if id not in example:
                example['markers'] = []
            for marker in markers:
                if marker['length'] <=76:             
                    example['markers'].append(marker)
        # print(example)        
    for example in dataset: 
        input_sen = example['paragraph']
        target_p2 = gen_only_components(example["paragraph"], example["components"])
        target_p3 = generate_anl_end_to_end(example["paragraph"], example["components"], example["relations"])
        
        if val == False:
            target_p1 = gen_only_markers(example["paragraph"], example["markers"])
            input_sentences.append(p_1 + input_sen)
            target_sentences.append(target_p1)
            
        input_sentences.append(p_2 + input_sen)
        target_sentences.append(target_p2)
        input_sentences.append(p_3 + input_sen)
        target_sentences.append(target_p3)
        
        print(f"input_sen: {input_sen}")
        if val == False:
            print(f"target_p1: {target_p1}")
        print(f"target_p2: {target_p2}")
        print(f"target_p3: {target_p3}")
        print("\n\n\n\n\n\n")
        
    return input_sentences, target_sentences
    
        

def prepare_data_multitask_test(one, dataset, marker_datset):
    p_1 = "Markers : " ## target = with only markers
    p_2 = "Components : "  ## target = with only components 
    p_3 = "Relations : " ## target = final with both components and reltions
        
    input_sentences = []
    target_sentences = []
    markers = []
    
    for example in dataset:
        id = example['id']
        if id not in marker_datset:
            marker_datset[id] = []
            
        markers = marker_datset[id]
        if id not in example:
            example['markers'] = []
        for marker in markers:
            if marker['length'] <=76:             
                example['markers'].append(marker)
        # print(example)        
    for example in dataset: 
        input_sen = example['paragraph']
        target_p2 = gen_only_components(example["paragraph"], example["components"])
        target_p3 = generate_anl_end_to_end(example["paragraph"], example["components"], example["relations"])
        target_p1 = gen_only_markers(example["paragraph"], example["markers"])
        
        
        if one == 1:
            input_sentences.append(p_1 + input_sen)
            target_sentences.append(target_p1)
        if one == 2:    
            input_sentences.append(p_2 + input_sen)
            target_sentences.append(target_p2)
    #  only relations needed, scrap out the components from target_p3
        if one == 3:     
            input_sentences.append(p_3 + input_sen)
            target_sentences.append(target_p3)
        
        # print(f"input_sen: {input_sen}")
        # print(f"target_p1: {target_p1}")
        # print(f"target_p2: {target_p2}")
        # print(f"target_p3: {target_p3}")
        # print("\n\n\n\n\n\n")
        
    return input_sentences, target_sentences            
        

# # Post-processing the anl structure------------------------------------------------------------

# def decode_anl(formatted_text):

#     formatted_text = re.sub(r'\](\W)', r'] \1', formatted_text)

#     comp_pattern = re.compile(r'\[(.*?)\|(.*?)\]')
    
#     # Find all matches of the component pattern in the formatted text
#     matches = comp_pattern.findall(formatted_text)
    
#     components = []
#     relations = []

#     for match in matches:
#         comp_str = match[0].strip()  # Text inside the brackets
#         comp_type_relations = match[1].strip().split('|')  # Type and relations

#         comp_type = comp_type_relations[0].strip()
#         if (len(comp_type.split(" ")) > 1):
#             comp_type = comp_type.split(" ")[0]
            
#         comp_relations = [rel.strip() for rel in comp_type_relations[1:]]

#         # Store the component details
#         components.append({
#             'span': comp_str,
#             'type': comp_type,
#             'relations': comp_relations
#         })

#     # Create relations based on extracted components and relations
#     for component in components:
#         for rel in component['relations']:
#             rel_match = re.match(r'(\w+)\s*=\s*(.*)', rel)
#             if rel_match:
#                 rel_type = rel_match.group(1).strip()
#                 rel_target_span = rel_match.group(2).strip()
                
#                 # Find the target component by span
#                 target_component = next((comp for comp in components if comp['span'] == rel_target_span), None)
#                 if target_component:
#                     relations.append((
#                         (component['span'], component['type']),
#                         rel_type,
#                         (target_component['span'], target_component['type'])
#                     ))

#     component_tuples = [(comp['type'], comp['span']) for comp in components]

#     # print("Extracted components:", component_tuples)
#     # print("Extracted relations:", relations)
#     return component_tuples, relations


def decode_anl(formatted_text):
    formatted_text = re.sub(r'\](\W)', r'] \1', formatted_text)

    comp_pattern = re.compile(r'\[(.*?)\|(.*?)\]')
    
    # Find all matches of the component pattern in the formatted text
    matches = comp_pattern.findall(formatted_text)
    
    components = []
    relations = []

    for match in matches:
        comp_str = match[0].strip()  # Text inside the brackets
        comp_type_relations = match[1].strip().split(' ')  # Type and relations

        comp_type = comp_type_relations[0].strip()
        comp_relations = [" ".join([rel.strip() for rel in comp_type_relations[1:]])]

        # print (comp_relations)

        # Store the component details
        components.append({
            'span': comp_str,
            'type': comp_type,
            'relations': comp_relations
        })

    # Create relations based on extracted components and relations
    for component in components:
        for rel in component['relations']:
            rel_match = re.match(r'(\w+)\s*\|\s*(.*)', rel)
            if rel_match:
                rel_type = rel_match.group(1).strip()
                rel_target_span = rel_match.group(2).strip()
                
                # Find the target component by span
                target_component = next((comp for comp in components if comp['span'] == rel_target_span), None)
                if target_component:
                    relations.append((
                        (component['span'], component['type']),
                        rel_type,
                        (target_component['span'], target_component['type'])
                    ))

    component_tuples = [(comp['type'], comp['span']) for comp in components]

    # print("Extracted components:", component_tuples)
    # print("Extracted relations:", relations)
    return component_tuples


def decode_anl_rel(text):
    
    pattern = r'\[\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\]'

    matches = re.findall(pattern, text)
    relations = []
    for match in matches:
        rel_type = match[1].strip()
        rel_sent1 = match[0].strip()
        rel_sent2 = match[2].strip()
        relations.append((rel_sent1, rel_type, rel_sent2))
        
    return relations    

