import re
import csv

units = {
    "width": {"centimetre", "foot", "millimetre", "metre", "inch", "yard"},
    "depth": {"centimetre", "foot", "millimetre", "metre", "inch", "yard"},
    "height": {"centimetre", "foot", "millimetre", "metre", "inch", "yard"},
    "item_weight": {"milligram", "kilogram", "microgram", "gram", "ounce", "ton", "pound"},
    "maximum_weight_recommendation": {"milligram", "kilogram", "microgram", "gram", "ounce", "ton", "pound"},
    "voltage": {"millivolt", "kilovolt", "volt"},
    "wattage": {"kilowatt", "watt"},
    "item_volume": {"cubic foot", "microlitre", "cup", "fluid ounce", "centilitre", "imperial gallon", "pint", "decilitre", "litre", "millilitre", "quart", "cubic inch", "gallon"}
}

unit_aliases = {
    'grams': 'gram',
    'g': 'gram',
    'gs': 'gram',
    'kilograms': 'kilogram',
    'kg': 'kilogram',
    'kgs': 'kilogram',
    'milligrams': 'milligram',
    'mg': 'milligram',
    'mgs': 'milligram',
    'micrograms': 'microgram',
    'ug': 'microgram',
    'µg': 'microgram', 
    'ounces': 'ounce',
    'oz': 'ounce',
    'ozs': 'ounce',
    'pounds': 'pound',
    'lbs': 'pound',
    'lb': 'pound',
    'tonnes': 'ton',
    'tons': 'ton',
    
    'millimetres': 'millimetre',
    'mm': 'millimetre',
    'mms': 'millimetre',
    'centimetres': 'centimetre',
    'cm': 'centimetre',
    'cms': 'centimetre',
    'metres': 'metre',
    'meters': 'metre',
    'm': 'metre',
    'ms': 'metre',
    'inches': 'inch',
    'in': 'inch',
    'ins': 'inch',
    '"': 'inch',
    'foot': 'foot',
    'feet': 'foot',
    'ft': 'foot',
    'yd': 'yard',
    'yards': 'yard',
    'yds': 'yard',
    
    'volts': 'volt',
    'v': 'volt',
    'vs': 'volt',
    'kilovolts': 'kilovolt',
    'kv': 'kilovolt',
    'millivolts': 'millivolt',
    'mv': 'millivolt',
    
    'watts': 'watt',
    'w': 'watt',
    'ws': 'watt',
    'kilowatts': 'kilowatt',
    'kw': 'kilowatt',
    
    'litres': 'litre',
    'liters': 'litre',
    'l': 'litre',
    'ls': 'litre',
    'millilitres': 'millilitre',
    'milliliters': 'millilitre',
    'ml': 'millilitre',
    'mls': 'millilitre',
    'cubic inches': 'cubic inch',
    'cu in': 'cubic inch',
    'in3': 'cubic inch',  
    'cubic feet': 'cubic foot',
    'cubic ft': 'cubic foot',
    'cu ft': 'cubic foot',
    'ft3': 'cubic foot',
    'fluid ounces': 'fluid ounce',
    'fl oz': 'fluid ounce',
    'cups': 'cup',
    'pints': 'pint',
    'quarts': 'quart',
    'gallons': 'gallon',
    'imperial gallons': 'imperial gallon',
    'gal': 'gallon',
    'microlitres': 'microlitre',
    'microliters': 'microlitre',
    'µl': 'microlitre',
    'centilitres': 'centilitre',
    'centiliters': 'centilitre', 
    'cl': 'centilitre',
    'decilitres': 'decilitre',
    'deciliters': 'decilitre',
    'dl': 'decilitre',
}

all_units = {u for unit_set in units.values() for u in unit_set}

def normalize_unit(unit):
    return unit_aliases.get(unit.lower(), unit)

def get_default_unit(sentence):
    if "weight" in sentence:
        return "gram"
    elif "volume" in sentence:
        return "litre"
    elif "height" in sentence or "width" in sentence or "depth" in sentence:
        return "centimetre"
    elif "voltage" in sentence:
        return "volt"
    elif "wattage" in sentence:
        return "watt"
    return None


def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def process_csv(input_file_path, output_file_path):
    with open(input_file_path, mode='r', newline='', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        header = next(reader)
        with open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(header)
            for row in reader:
                if len(row) > 1: 
                    if is_integer(row[1]) or extract_value_and_unit(row[1]) is None:
                        row[1] = ""
                    else:
                        row[1] = extract_value_and_unit(row[1]) or row[1]

                writer.writerow(row)


def extract_value_and_unit(sentence):
    sentence = sentence.lower()
    for unit in unit_aliases:
        match = re.search(r'([+-]?\d*\.?\d+)\s*' + re.escape(unit), sentence)
        if match:
            value = match.group(1) 
            normalized_unit = normalize_unit(unit)
            return f"{value} {normalized_unit}"
    return None



input_file_path = 'submission_2_Amazon_ML_Challenge - Sheet1.csv'
output_file_path = 'PROCESSEDsubmission2_2.csv'

process_csv(input_file_path, output_file_path)
