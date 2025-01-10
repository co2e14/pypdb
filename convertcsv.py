import pandas as pd
import re

def parse_row(line):
    """
    Parses a line of the CSV and extracts the four fields.
    """
    # Remove the parentheses and any leading/trailing whitespace
    line = line.strip().lstrip('(').rstrip(')')
    
    # Use regex to extract values enclosed in single quotes
    matches = re.findall(r"'([^']*)'", line)
    
    if len(matches) != 4:
        # If the line doesn't have exactly four fields, return None
        return None
    return matches  # Returns [X, Y, Z, PDBID]

def process_file(file_path):
    """
    Processes the CSV file and returns a dataframe with WAVELENGTH, BEAMLINE, and PDBID.
    """
    pairs = []  # List to store the resulting WAVELENGTH, BEAMLINE, and PDBID triples
    
    with open(file_path, 'r') as f:
        for line_number, line in enumerate(f, start=1):
            parsed = parse_row(line)
            if not parsed:
                print(f"Skipping invalid line {line_number}: {line.strip()}")
                continue  # Skip lines that don't match the expected format
            
            X, Y, Z, PDBID = parsed  # Unpack the parsed values
            
            if X != '?':
                # Case 1: X is not '?'
                WAVELENGTH = X.strip()
                BEAMLINE = Z.strip()
                pairs.append({'WAVELENGTH': WAVELENGTH, 'BEAMLINE': BEAMLINE, 'PDBID': PDBID.strip()})
            else:
                # Case 2: X is '?'
                if Y.strip() == '?':
                    # Subcase 2a: Y is also '?', skip this row
                    print(f"Skipping row {line_number} because both X and Y are '?'.")
                    continue
                
                # Split Y and Z values by ',' and remove any extra whitespace
                Y_values = [y.strip() for y in Y.split(',')]
                Z_values = [z.strip() for z in Z.split(',')]
                
                if len(Z_values) == 1:
                    # Subcase 2b: Multiple Y values but only one Z
                    for y in Y_values:
                        pairs.append({'WAVELENGTH': y, 'BEAMLINE': Z_values[0], 'PDBID': PDBID.strip()})
                elif len(Z_values) == len(Y_values):
                    # Subcase 2c: Multiple Y and multiple Z values
                    for y, z in zip(Y_values, Z_values):
                        pairs.append({'WAVELENGTH': y, 'BEAMLINE': z, 'PDBID': PDBID.strip()})
                else:
                    # Subcase 2d: Multiple Y and multiple Z but counts don't match
                    # Pair Y1 with Z1, Y2 with Z2, etc., up to the length of the shorter list
                    min_length = min(len(Y_values), len(Z_values))
                    for i in range(min_length):
                        pairs.append({'WAVELENGTH': Y_values[i], 'BEAMLINE': Z_values[i], 'PDBID': PDBID.strip()})
                    # Handle remaining Y or Z values if lengths differ
                    if len(Y_values) > len(Z_values):
                        # Remaining Y values paired with the last Z value
                        for y in Y_values[min_length:]:
                            pairs.append({'WAVELENGTH': y, 'BEAMLINE': Z_values[-1], 'PDBID': PDBID.strip()})
                    elif len(Z_values) > len(Y_values):
                        print(f"Row {line_number}: More Z values than Y values. Extra Z values are ignored.")
    
    # Create a dataframe from the list of triples
    df = pd.DataFrame(pairs)
    return df

def main():
    # Replace 'input.csv' with the path to your actual CSV file
    input_file = 'allinfoout.csv'
    output_file = 'output_dataframe.csv'
    
    # Process the file to get the dataframe
    df = process_file(input_file)
    
    # Display the dataframe
    print("Processed Dataframe:")
    print(df)
    
    # Save the dataframe to a CSV file
    df.to_csv(output_file, index=False)
    print(f"\nDataframe saved to '{output_file}'.")

if __name__ == "__main__":
    main()