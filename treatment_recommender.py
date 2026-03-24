"""
Treatment recommendation system for plant diseases
"""

import re
from typing import Dict, List, Optional
from config import TREATMENT_RECOMMENDATIONS, DEFAULT_TREATMENT

class TreatmentRecommender:
    """Treatment recommendation system for plant diseases"""
    
    def __init__(self):
        self.treatment_db = TREATMENT_RECOMMENDATIONS
        self.default_treatment = DEFAULT_TREATMENT
    
    def get_treatment_recommendation(self, disease_name: str, 
                                   confidence: float = None,
                                   plant_type: str = None) -> Dict:
        """
        Get treatment recommendation for a specific disease
        
        Args:
            disease_name (str): Name of the disease
            confidence (float): Confidence score of the prediction
            plant_type (str): Type of plant (optional)
            
        Returns:
            Dict: Treatment recommendation
        """
        # Clean disease name
        clean_disease = self._clean_disease_name(disease_name)
        
        # Get treatment from database
        treatment_info = self.treatment_db.get(clean_disease, self.default_treatment)
        
        # Add confidence-based recommendations
        recommendation = {
            'disease_name': disease_name,
            'description': treatment_info.get('description', ''),
            'treatment': treatment_info.get('treatment', []),
            'prevention': treatment_info.get('prevention', ''),
            'confidence_level': self._get_confidence_level(confidence),
            'urgency': self._get_urgency_level(clean_disease, confidence),
            'plant_specific_advice': self._get_plant_specific_advice(plant_type, clean_disease)
        }
        
        return recommendation
    
    def _clean_disease_name(self, disease_name: str) -> str:
        """Clean and normalize disease name"""
        # Remove common prefixes and suffixes
        clean_name = disease_name.replace('___', '_').replace('__', '_')
        
        # Handle specific cases
        if 'Apple' in clean_name:
            clean_name = clean_name.replace('Apple_', 'Apple___')
        elif 'Tomato' in clean_name:
            clean_name = clean_name.replace('Tomato_', 'Tomato___')
        elif 'Potato' in clean_name:
            clean_name = clean_name.replace('Potato_', 'Potato___')
        
        return clean_name
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Get confidence level description"""
        if confidence is None:
            return "Unknown"
        elif confidence >= 0.9:
            return "Very High"
        elif confidence >= 0.8:
            return "High"
        elif confidence >= 0.7:
            return "Medium"
        elif confidence >= 0.5:
            return "Low"
        else:
            return "Very Low"
    
    def _get_urgency_level(self, disease_name: str, confidence: float) -> str:
        """Get urgency level for treatment"""
        # High urgency diseases
        high_urgency_diseases = [
            'Late_blight', 'Bacterial_spot', 'Black_rot', 'Cedar_apple_rust'
        ]
        
        # Medium urgency diseases
        medium_urgency_diseases = [
            'Early_blight', 'Apple_scab', 'Powdery_mildew', 'Leaf_blight'
        ]
        
        # Check disease urgency
        if any(disease in disease_name for disease in high_urgency_diseases):
            return "High"
        elif any(disease in disease_name for disease in medium_urgency_diseases):
            return "Medium"
        else:
            return "Low"
    
    def _get_plant_specific_advice(self, plant_type: str, disease_name: str) -> List[str]:
        """Get plant-specific advice"""
        if not plant_type:
            return []
        
        plant_type = plant_type.lower()
        advice = []
        
        if 'tomato' in plant_type:
            advice.extend([
                "Remove affected leaves immediately",
                "Avoid overhead watering",
                "Ensure good air circulation",
                "Consider using tomato cages for support"
            ])
        elif 'apple' in plant_type or 'tree' in plant_type:
            advice.extend([
                "Prune affected branches",
                "Remove fallen leaves and debris",
                "Apply dormant sprays in winter",
                "Maintain proper tree spacing"
            ])
        elif 'potato' in plant_type:
            advice.extend([
                "Remove infected plants immediately",
                "Avoid planting in same area next season",
                "Use certified seed potatoes",
                "Improve soil drainage"
            ])
        elif 'grape' in plant_type:
            advice.extend([
                "Prune for better air circulation",
                "Remove infected clusters",
                "Apply fungicide during growing season",
                "Monitor weather conditions"
            ])
        
        return advice
    
    def get_general_plant_care_tips(self) -> Dict[str, List[str]]:
        """Get general plant care tips"""
        return {
            "Watering": [
                "Water at soil level, not on leaves",
                "Water early in the morning",
                "Ensure proper drainage",
                "Avoid overwatering"
            ],
            "Fertilization": [
                "Use balanced fertilizer",
                "Follow recommended application rates",
                "Test soil pH regularly",
                "Apply fertilizer at appropriate times"
            ],
            "Pruning": [
                "Remove dead or diseased branches",
                "Prune during dormant season",
                "Use clean, sharp tools",
                "Make clean cuts at proper angles"
            ],
            "Pest Management": [
                "Monitor plants regularly",
                "Use integrated pest management",
                "Encourage beneficial insects",
                "Remove weeds and debris"
            ],
            "Disease Prevention": [
                "Choose disease-resistant varieties",
                "Practice crop rotation",
                "Maintain proper spacing",
                "Keep garden clean and tidy"
            ]
        }
    
    def get_seasonal_advice(self, season: str) -> Dict[str, List[str]]:
        """Get seasonal plant care advice"""
        seasonal_tips = {
            "Spring": [
                "Start seeds indoors",
                "Prepare garden beds",
                "Apply dormant sprays",
                "Check for winter damage",
                "Begin regular monitoring"
            ],
            "Summer": [
                "Water deeply and regularly",
                "Monitor for pests and diseases",
                "Harvest regularly",
                "Provide shade if needed",
                "Mulch to retain moisture"
            ],
            "Fall": [
                "Harvest remaining crops",
                "Clean up garden debris",
                "Plant cover crops",
                "Prepare for winter",
                "Store tools properly"
            ],
            "Winter": [
                "Plan next season's garden",
                "Order seeds and supplies",
                "Maintain indoor plants",
                "Check stored produce",
                "Review garden records"
            ]
        }
        
        return seasonal_tips.get(season, {})
    
    def get_organic_treatment_options(self, disease_name: str) -> List[str]:
        """Get organic treatment options for diseases"""
        organic_treatments = {
            'Apple_scab': [
                "Copper fungicide spray",
                "Baking soda solution (1 tsp per quart water)",
                "Neem oil application",
                "Sulfur-based fungicide"
            ],
            'Tomato_Blight': [
                "Copper fungicide",
                "Baking soda spray",
                "Milk spray (1 part milk to 9 parts water)",
                "Compost tea application"
            ],
            'Powdery_mildew': [
                "Milk spray",
                "Baking soda solution",
                "Neem oil",
                "Sulfur dust"
            ],
            'Bacterial_spot': [
                "Copper fungicide",
                "Bacillus subtilis",
                "Good sanitation practices",
                "Proper spacing"
            ]
        }
        
        # Find matching treatments
        for disease_key, treatments in organic_treatments.items():
            if disease_key.lower() in disease_name.lower():
                return treatments
        
        # Default organic treatments
        return [
            "Neem oil spray",
            "Baking soda solution",
            "Copper fungicide",
            "Good cultural practices",
            "Beneficial microorganisms"
        ]
    
    def get_chemical_treatment_options(self, disease_name: str) -> List[str]:
        """Get chemical treatment options for diseases"""
        chemical_treatments = {
            'Late_blight': [
                "Chlorothalonil",
                "Mancozeb",
                "Copper hydroxide",
                "Fosetyl-aluminum"
            ],
            'Early_blight': [
                "Chlorothalonil",
                "Azoxystrobin",
                "Propiconazole",
                "Copper fungicides"
            ],
            'Apple_scab': [
                "Myclobutanil",
                "Trifloxystrobin",
                "Captan",
                "Sulfur"
            ],
            'Bacterial_spot': [
                "Copper hydroxide",
                "Streptomycin",
                "Oxytetracycline",
                "Bacillus subtilis"
            ]
        }
        
        # Find matching treatments
        for disease_key, treatments in chemical_treatments.items():
            if disease_key.lower() in disease_name.lower():
                return treatments
        
        # Default chemical treatments
        return [
            "Copper-based fungicides",
            "Systemic fungicides",
            "Contact fungicides",
            "Bactericides (for bacterial diseases)"
        ]
    
    def get_prevention_strategies(self, disease_name: str) -> List[str]:
        """Get prevention strategies for specific diseases"""
        prevention_strategies = {
            'Fungal_diseases': [
                "Improve air circulation",
                "Avoid overhead watering",
                "Remove infected plant material",
                "Use resistant varieties",
                "Practice crop rotation"
            ],
            'Bacterial_diseases': [
                "Use disease-free seeds",
                "Avoid working with wet plants",
                "Disinfect tools regularly",
                "Control insect vectors",
                "Remove infected plants immediately"
            ],
            'Viral_diseases': [
                "Control insect vectors",
                "Use virus-free planting material",
                "Remove infected plants",
                "Practice good sanitation",
                "Avoid mechanical transmission"
            ]
        }
        
        # Determine disease type and return appropriate strategies
        if 'bacterial' in disease_name.lower():
            return prevention_strategies['Bacterial_diseases']
        elif 'virus' in disease_name.lower():
            return prevention_strategies['Viral_diseases']
        else:
            return prevention_strategies['Fungal_diseases']

def main():
    """Test the treatment recommendation system"""
    recommender = TreatmentRecommender()
    
    # Test treatment recommendation
    recommendation = recommender.get_treatment_recommendation(
        disease_name="Tomato___Early_blight",
        confidence=0.92,
        plant_type="tomato"
    )
    
    print("Treatment Recommendation:")
    print(f"Disease: {recommendation['disease_name']}")
    print(f"Description: {recommendation['description']}")
    print(f"Confidence Level: {recommendation['confidence_level']}")
    print(f"Urgency: {recommendation['urgency']}")
    print("Treatment Steps:")
    for i, step in enumerate(recommendation['treatment'], 1):
        print(f"  {i}. {step}")
    
    # Test organic treatments
    organic_options = recommender.get_organic_treatment_options("Tomato___Early_blight")
    print("\nOrganic Treatment Options:")
    for option in organic_options:
        print(f"  - {option}")

if __name__ == "__main__":
    main()
