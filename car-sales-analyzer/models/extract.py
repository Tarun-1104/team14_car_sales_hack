import spacy
import re

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

def extract_information(filepath):
    extracted_data = {
        "car_type": None,
        "fuel_type": None,
        "color": None,
        "distance_traveled": None,
        "make_year": None,
        "transmission_type": None,
        "company_policies": {
            "free_RC_transfer": None,
            "money_back_guarantee": None,
            "free_RSA": None,
            "return_policy": None
        },
        "customer_objections": {
            "refurbishment_quality": None,
            "car_issues": None,
            "price_issues": None,
            "customer_experience_issues": None
        }
    }

    with open(filepath, 'r') as file:
        transcript = file.read()

    doc = nlp(transcript)

    # Define patterns and keywords for matching
    patterns = {
        "car_type": ["suv", "hatchback", "sedan", "truck", "van"],
        "fuel_type": ["diesel", "petrol", "gas"],
        "color": ["blue", "white", "red", "black", "grey", "green", "silver", "brown"],
        "transmission_type": ["manual", "automatic"],
        "company_policies": {
            "free_RC_transfer": "free RC transfer",
            "money_back_guarantee": "5-day money back guarantee",
            "free_RSA": "free RSA for one year",
            "return_policy": "return policy"
        },
        "customer_objections": {
            "refurbishment_quality": "refurbishment",
            "car_issues": "car issues",
            "price_issues": "price issues",
            "customer_experience_issues": "experience issues"
        }
    }

    # Extract make year using regex
    year_match = re.search(r'\b(19|20)\d{2}\b', transcript)
    if year_match:
        extracted_data["make_year"] = year_match.group()

    # Extract data using SpaCy and patterns
    for ent in doc.ents:
        if ent.label_ == "DATE":
            year_match = re.search(r'\b(19|20)\d{2}\b', ent.text)
            if year_match:
                extracted_data["make_year"] = year_match.group()

    # Use pattern matching to find car types, fuel types, etc.
    for category, terms in patterns.items():
        if isinstance(terms, dict):
            for key, pattern in terms.items():
                if re.search(pattern, transcript, re.IGNORECASE):
                    if category == "company_policies":
                        extracted_data["company_policies"][key] = "Yes"
                    elif category == "customer_objections":
                        extracted_data["customer_objections"][key] = "Yes"
        else:
            for term in terms:
                if re.search(term, transcript, re.IGNORECASE):
                    if category == "car_type":
                        for potential_type in patterns["car_type"]:
                            if re.search(potential_type, transcript, re.IGNORECASE):
                                extracted_data["car_type"] = potential_type
                                break
                    else:
                        extracted_data[category] = term
                    break

    # Special handling for colors
    for color in patterns["color"]:
        if re.search(color, transcript, re.IGNORECASE):
            extracted_data["color"] = color
            break

    # Special handling for distance traveled
    distance_match = re.search(r'\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:km|kilometers|miles)\b', transcript, re.IGNORECASE)
    if distance_match:
        extracted_data["distance_traveled"] = distance_match.group()

    return extracted_data
