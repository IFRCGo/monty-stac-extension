import json

def write_table(file, code, label):

    # Ensure both lists have the same length
    if len(code) != len(label):
        raise ValueError("code and label lists are not of the same length")

    # Generate the Markdown table
    markdown_table = "| code | label |\n"
    markdown_table += "| ---- | ----- |\n"
    for code, lab in zip(code, label):
        markdown_table += f"| {code} | {lab} |\n"

    # Save the Markdown table to a file
    file.write(markdown_table)

# Load the JSON file
with open('Montandon_Schema_V1-00.json', 'r') as file:
    data = json.load(file)
    
with open('taxonomy.md', 'w') as file:

    # Write the title
    file.write("# Taxonomy Tables\n\n")
    
    # Common Subtitle
    file.write("## Common\n\n")
    
    # Extract the values for Estimation Type
    code = data['properties']['taxonomies']['properties']['est_type']['items']['properties']['est_type_code'].get('enum', [])
    label = data['properties']['taxonomies']['properties']['est_type']['items']['properties']['est_type_lab'].get('enum', [])
    
    # Write the Estimation Type table
    file.write("### Estimation Type\n\n")
    write_table(file, code, label)
    file.write("\n")
    
    # Hazard Subtitle
    file.write("## Hazard\n\n")
    
    # Extract the values for Hazard Information Profiles
    code = data['properties']['taxonomies']['properties']['haz_class']['items']['properties']['haz_spec_code'].get('enum', [])
    label = data['properties']['taxonomies']['properties']['haz_class']['items']['properties']['haz_spec_lab'].get('enum', [])
    
    # Write the Hazard Information Profiles table
    file.write("### [UNDRR-ISC 2020 Hazard Information Profiles](https://www.preventionweb.net/drr-glossary/hips)\n\n")
    write_table(file, code, label)
    file.write("\n")
    
    # Impact Subtitle
    file.write("## Impact\n\n")

    # Extract the values for Exposure Category
    code = data['properties']['taxonomies']['properties']['exp_class']['items']['properties']['exp_spec_code'].get('enum', [])
    label = data['properties']['taxonomies']['properties']['exp_class']['items']['properties']['exp_spec_lab'].get('enum', [])
    
    # Write the Exposure Category table
    file.write("### Exposure Category\n\n")
    write_table(file, code, label)
    file.write("\n")
    
    # Extract the values for Impact Type
    code = data['properties']['taxonomies']['properties']['imp_class']['items']['properties']['imp_type_code'].get('enum', [])
    label = data['properties']['taxonomies']['properties']['imp_class']['items']['properties']['imp_type_lab'].get('enum', [])
    
    # Write the Impact Type table
    file.write("### Impact Type\n\n")
    write_table(file, code, label)
    file.write("\n")
    

print("Markdown table generated and saved to taxonomy.md")