import pandas as pd
import ast
import re

def clean_and_unify_locations(file_path):
    # Load the dataset
    df = pd.read_csv('appartment_data.csv')

    mapping_rules = {
        # 1. AIRPORTS & RAILWAYS
        r".*(Indira Gandhi|IGI|IGIA|Delhi International|International Airport|IG International).*": "Indira Gandhi International Airport",
        r".*(Gurgaon Railway|Gurugram Railway).*": "Gurugram Railway Station",
        r".*(Basai Dhankot|Basai Dhancourt).*": "Basai Dhankot Railway Station",
        r".*(Garhi Harsaru|Garhi harsaru).*": "Garhi Harsaru Junction",
        r".*Bijwasan Railway.*": "Bijwasan Railway Station",
        r".*Patli Railway.*": "Patli Railway Station",
        r".*Sealdah Railway.*|.*Sealdah.*": "Sealdah Railway Station",

        # 2. METRO STATIONS
        r".*(HUDA City Centre|Huda city center|HUDA City Center).*": "HUDA City Centre Metro Station",
        r".*(Sector 55-56 Metro|Sector 55/56 Metro|Rapid Metro Station Sector 56|Sector 55-56 Rapid Metro).*": "Sector 55-56 Metro Station",
        r".*(Sector 53-54 Metro|Sector 53/54 Metro|Sector 53-54 Rapid Metro).*": "Sector 53-54 Metro Station",
        r".*(Sector 42-43 Metro|Sector 42-43 Rapid Metro).*": "Sector 42-43 Metro Station",
        r".*Sector 54 Chowk Metro.*": "Sector 54 Chowk Metro Station",
        r".*Dwarka Sector 21 Metro.*|.*Sector-21 Metro Dwarka.*": "Dwarka Sector 21 Metro Station",
        r".*IFFCO Chowk Metro.*|.*Iffco Chowk Metro.*": "IFFCO Chowk Metro Station",

        # 3. HIGHWAYS & ROADS
        r".*(Dwarka Exp|Dwaraka Exp|Northern Peripheral|Dwarka Expressway).*": "Dwarka Expressway",
        r".*(NH-48|NH 48|NH8|NH-8|NH -8|Delhi-Jaipur|Delhi Jaipur|Delhi Gurgaon Exp|Gurgaon - Delhi Exp|National Highway 48|National Highway 8|N\.H-8).*": "NH-48 (Delhi-Jaipur Expressway)",
        r".*(Golf Course Ext|SPR|Southern Peripheral|Southern Periphery).*": "Golf Course Extension Road",
        r".*(Sohna Rd|Sohna Road|Badshahpur Sohna|Sohna Gurgaon Road|Sohna-Gurgaon Rd).*": "Sohna Road",
        r".*(Pataudi Rd|Pataudi Road).*": "Pataudi Road",
        r".*Faridabad.*Gurgaon.*": "Faridabad-Gurgaon Road",
        r".*(KMP|Kundli Manesar Palwal|Western Peripheral).*": "KMP Expressway",
        r".*Mehrauli-Gurgaon Road.*|.*Mehrauli-Gurgaon Rd.*|.*MG Road.*": "MG Road (Mehrauli-Gurgaon Road)",
        r".*Central Peripheral Road.*|.*Central Periphery Road.*|.*CPR.*": "Central Peripheral Road",

        # 4. HOSPITALS
        r".*Miracles Apollo.*|.*Spectra Hospital.*": "Miracles Apollo Cradle Hospital",
        r".*Park Hospital.*": "Park Hospital",
        r".*Aarvy.*|.*Arvy Hospital.*": "Aarvy Healthcare Hospital",
        r".*CK Birla.*": "CK Birla Hospital",
        r".*Medanta.*|.*Medicity.*": "Medanta The Medicity",
        r".*Vardaan.*": "Vardaan Hospital",
        r".*Signature.*Hospital.*|.*Signature.*Speciality.*": "Signature Advanced Hospital",
        r".*Shri Balaji.*": "Shri Balaji's Multispeciality Hospital",
        r".*Artemis.*|.*Artimis.*": "Artemis Hospital",
        r".*Paras Hospital.*|.*Paras Hospitals.*": "Paras Hospital",
        r".*Fortis.*": "Fortis Hospital",
        r".*W Pratiksha.*": "W Pratiksha Hospital",
        r".*Silver Streak.*": "Silver Streak Multi Speciality Hospital",
        r".*Swastik Hospital.*|.*Swastik Multispeciality.*": "Swastik Hospital",

        # 5. SCHOOLS & UNIVERSITIES
        r".*St\.? Xavier.*|.*Xavier’s International.*": "St. Xavier's High School",
        r".*Delhi Public School.*|^DPS$|.*DPS .*": "Delhi Public School (DPS)",
        r".*GD Goenka.*|.*G D Goenka.*|.*Gd goenka.*": "GD Goenka Institution",
        r".*Heritage.*School.*": "The Heritage School",
        r".*Euro.*Int.*School.*|.*EuroKids.*|.*Euro Intl School.*|.*Euro Int\. School.*": "Euro International School",
        r".*NorthCap.*|.*Baghera University.*": "The NorthCap University",
        r".*Gurugram University.*": "Gurugram University",
        r".*SGT University.*|.*SGT Medical College.*": "SGT University",
        r".*K\.?R\.? Mangalam.*|.*KR Mangalam.*": "K.R. Mangalam University",
        r".*Amity University.*|.*Amity.*": "Amity University",
        r".*DPG Degree College.*|.*DPG Institute of Technology.*|.*DPGITM.*": "DPG Group of Institutions",
        r".*KIIT College.*": "KIIT College of Engineering",
        r".*Lotus Valley.*": "Lotus Valley International School",
        r".*Alpine Convent School.*|.*Alpine School.*": "Alpine Convent School",
        r".*Pathways School.*|.*Pathways.*": "Pathways School",
        r".*Sushant University.*": "Sushant University",
        r".*The Shri Ram School.*|.*The Shriram Millennium.*": "The Shri Ram School",

        # 6. MALLS & ENTERTAINMENT
        r".*Sapphire (83|93).*|.*Sapphire Mall.*": "Sapphire Mall",
        r".*Vatika Town Square.*": "Vatika Town Square",
        r".*SkyJumper.*|.*Zooper.*Trampoline.*": "SkyJumper Trampoline Park",
        r".*Fun N Food.*": "Fun N Food Village",
        r".*(Omaxe|OMAXE|Omex).*Mall.*|.*Omaxe City Centre.*|.*Omaxe Celebration Mall.*": "Omaxe Mall",
        r".*Airia Mall.*": "Airia Mall",
        r".*Ambience Mall.*": "Ambience Mall",
        r".*Ardee Mall.*": "Ardee Mall",
        r".*IRIS Broadway Mall.*|.*Iris Broadway.*": "IRIS Broadway Mall",
        r".*M3M (Cosmopolitan|IFC|SCO|65th Avenue).*": "M3M Mall/Commercial",
        r".*Global City Centre.*": "Global City Centre Mall",

        # 7. HOTELS
        r".*Hyatt Regency.*|.*Hyatt Place.*": "Hyatt Hotel Group",
        r".*DoubleTree by Hilton.*|.*Double Tree by Hilton.*": "DoubleTree by Hilton",
        r".*Lemon Tree Hotel.*": "Lemon Tree Hotel",
        r".*Holiday Inn.*": "Holiday Inn",
        r".*Country Inn.*": "Country Inn & Suites",
        r".*Radisson.*": "Radisson Hotel",
        r".*The Westin.*|.*Westin.*": "The Westin Hotel",
        r".*Taj City Centre.*|.*Taj Hotel.*|.*Vivanta.*": "Taj/Vivanta Hotel Group",
        r".*The Oberoi.*|.*Trident Hotel.*": "The Oberoi/Trident",

        # 8. MISC
        r".*IMT Manesar.*": "IMT Manesar",
        r".*Tau Devi.*Lal.*": "Tau Devi Lal Sports Complex",
        r".*Aapno Ghar.*|.*AapnoGhar.*": "AapnoGhar",
        r".*Cyber City.*|.*DLF Cyber City.*": "DLF Cyber City"
    }

    def extract_distance_km(dist_str):
        try:
            dist_str = str(dist_str).lower().strip()
            num = float(re.findall(r"[-+]?\d*\.\d+|\d+", dist_str)[0])
            if 'm' in dist_str and 'km' not in dist_str:
                return num / 1000.0
            return num
        except:
            return 999.0

    def process_advantages(row_val):
        if pd.isna(row_val) or str(row_val).strip() == "": return "{}"
        try:
            loc_dict = ast.literal_eval(row_val)
            clean_dict = {}
            for key, val in loc_dict.items():
                new_key = key.strip()
                for pattern, standard_name in mapping_rules.items():
                    if re.match(pattern, new_key, re.IGNORECASE):
                        new_key = standard_name
                        break
                new_dist = extract_distance_km(val)
                if new_key in clean_dict:
                    clean_dict[new_key] = min(clean_dict[new_key], new_dist)
                else:
                    clean_dict[new_key] = new_dist
            return str({k: f"{v} KM" for k, v in clean_dict.items() if v != 999.0})
        except: return row_val

    def process_nearby(row_val):
        if pd.isna(row_val) or str(row_val).strip() == "": return "[]"
        try:
            loc_list = ast.literal_eval(row_val)
            clean_list = []
            for item in loc_list:
                new_item = item.strip()
                for pattern, standard_name in mapping_rules.items():
                    if re.match(pattern, new_item, re.IGNORECASE):
                        new_item = standard_name
                        break
                if new_item not in clean_list: clean_list.append(new_item)
            return str(clean_list)
        except: return row_val

    df['LocationAdvantages'] = df['LocationAdvantages'].apply(process_advantages)
    df['NearbyLocations'] = df['NearbyLocations'].apply(process_nearby)
    
    output_filename = 'fully_fixed_real_estate_data.csv'
    df.to_csv(output_filename, index=False)
    print(f"Data successfully cleaned and saved to {output_filename}")

clean_and_unify_locations('deep_cleaned_real_estate_data (1).csv')