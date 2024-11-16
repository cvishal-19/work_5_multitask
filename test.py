import re

target_p1= "(( On the other hand | followed by [ Premise ] )), the significance of competition is that how to become more excellence to gain the victory. (( Hence it is always said that | followed by [ Claim ] )) competition makes the society more effective. (( However | followed by [ Premise ] )), when we consider about the question that how to win the game, we always find that we need the cooperation. The greater our goal is, the more competition we need. Take Olympic games which is a form of competition for instance, it is hard to imagine how an athlete could win the game without the training of his or her coach, and the help of other professional staffs such as the people who take care of his diet, and those who are in charge of the medical care. The winner is the athlete but the success belongs to the whole team. (( Therefore | followed by [ Claim ] )) without the cooperation, there would be no victory of competition."
target_p2= "On the other hand, [ the significance of competition is that how to become more excellence to gain the victory | Premise ]. Hence it is always said that [ competition makes the society more effective | Claim ]. However, [ when we consider about the question that how to win the game, we always find that we need the cooperation | Premise ]. The greater our goal is, the more competition we need. [ Take Olympic games which is a form of competition for instance, it is hard to imagine how an athlete could win the game without the training of his or her coach, and the help of other professional staffs such as the people who take care of his diet, and those who are in charge of the medical care | Premise ]. The winner is the athlete but the success belongs to the whole team. Therefore [ without the cooperation, there would be no victory of competition | Claim ]."
target_p3 = "On the other hand, [ the significance of competition is that how to become more excellence to gain the victory | supports | competition makes the society more effective ]. Hence it is always said that competition makes the society more effective . However, [ when we consider about the question that how to win the game, we always find that we need the cooperation | supports | without the cooperation, there would be no victory of competition ]. The greater our goal is, the more competition we need. [ Take Olympic games which is a form of competition for instance, it is hard to imagine how an athlete could win the game without the training of his or her coach, and the help of other professional staffs such as the people who take care of his diet, and those who are in charge of the medical care | supports | without the cooperation, there would be no victory of competition ]. The winner is the athlete but the success belongs to the whole team. Therefore without the cooperation, there would be no victory of competition ."

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
    return component_tuples, relations
                         

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
        

pred_relation = decode_anl(target_p2)
pred_relation_real = decode_anl_rel(target_p3)
print(pred_relation)
print(pred_relation_real)

# for rel in pred_relation: 
#     print(f"sent1: {rel[0]}")
#     print(f"rel_type: {rel[1]}")
#     print(f"sent2: {rel[2]}")
#     print("\n")
    
    