import json
import pandas as df

def write_table(file, column_names, column_data):
    # Ensure all columns have the same length
    if not all(len(column) == len(column_data[0]) for column in column_data):
        raise ValueError("All columns must have the same length")

    # Generate the Markdown table header
    header = "| " + " | ".join(column_names) + " |\n"
    separator = "| " + " | ".join(["---"] * len(column_names)) + " |\n"
    markdown_table = header + separator

    # Generate the Markdown table rows
    for row in zip(*column_data):
        markdown_table += "| " + " | ".join(row) + " |\n"

    # Save the Markdown table to a file
    file.write(markdown_table)
    
# Define a function to get the profiles CSV ImpactInformationProfiles.csv
# and load it in a pandas DataFrame
def load_profiles(file):
    return df.read_csv(file)

# Load the JSON file
with open('Montandon_Schema_V1-00.json', 'r') as file:
    data = json.load(file)
    
# Load the profiles CSV
profiles = load_profiles('ImpactInformationProfiles.csv')
    
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
    write_table(file, ['Estimation Type Code', 'Estimation Type Label'], [code, label])
    file.write("\n")
    
    # Hazard Subtitle
    file.write("## Hazard\n\n")
    
    # Extract the values for Hazard Information Profiles
    code = data['properties']['taxonomies']['properties']['haz_class']['items']['properties']['haz_spec_code'].get('enum', [])
    label = data['properties']['taxonomies']['properties']['haz_class']['items']['properties']['haz_spec_lab'].get('enum', [])
    # Get the cluster and family codes for each code in the list
    cluster_code = [profiles.loc[profiles['name'] == c, "link_group"].values[-1] for c in code]
    family_code = [profiles.loc[profiles['name'] == c, "link_maingroup"].values[-1] for c in code]
    # Get the related labels
    cluster_label = [profiles.loc[profiles['name'] == c, "label"].values[-1] for c in cluster_code]
    cluster_id = [profiles.loc[profiles['name'] == c, "link_maingroup"].values[-1] for c in cluster_code]
    family_label = [profiles.loc[profiles['name'] == c, "label"].values[-1] for c in family_code]
    
    # Write the Hazard Information Profiles table
    file.write("### [UNDRR-ISC 2020 Hazard Information Profiles](https://www.preventionweb.net/drr-glossary/hips)\n\n")
    write_table(file, ['Hazard Code', 'Hazard Label', "Cluster ID", 'Cluster Label', 'Family Label'], [code, label, cluster_id, cluster_label, family_label])
    file.write("\n")
    
    # Impact Subtitle
    file.write("## Impact\n\n")

    # Extract the values for Exposure Category
    code = data['properties']['taxonomies']['properties']['exp_class']['items']['properties']['exp_spec_code'].get('enum', [])
    label = data['properties']['taxonomies']['properties']['exp_class']['items']['properties']['exp_spec_lab'].get('enum', [])
    
    # Write the Exposure Category table
    file.write("### Exposure Category\n\n")
    write_table(file, ['Exposure Category Code', 'Exposure Category Label'], [code, label])
    file.write("\n")
    
    # Extract the values for Impact Type
    code = data['properties']['taxonomies']['properties']['imp_class']['items']['properties']['imp_type_code'].get('enum', [])
    label = data['properties']['taxonomies']['properties']['imp_class']['items']['properties']['imp_type_lab'].get('enum', [])
    
    # Write the Impact Type table
    file.write("### Impact Type\n\n")
    write_table(file, ['Impact Type Code', 'Impact Type Label'], [code, label])
    file.write("\n")
    

print("Markdown table generated and saved to taxonomy.md")