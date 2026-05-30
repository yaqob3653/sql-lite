from models import Supplier

def compare_suppliers(suppliers, preference=50):
    """
    Ranks suppliers based on a weighted score of:
    - Price (Base Price + Shipping + Taxes) (Lower is better)
    - Quality (High=3, Medium=2, Low=1) (Higher is better)
    - Rating (Higher is better)
    
    Preference (0-100): 
    - 0 focus on Price
    - 100 focus on Quality
    
    Returns sorted list of dictionaries with score.
    """
    ranked_suppliers = []
    
    for supplier in suppliers:
        # Normalize Quality
        quality_score = 1
        if supplier.product_quality == 'High': quality_score = 3
        elif supplier.product_quality == 'Medium': quality_score = 2
        
        # Calculate Total Cost
        # Note: In a real app, base_price would come from the specific product, 
        # here we assume a generic comparison or avg cost.
        total_cost = supplier.shipping_cost + supplier.taxes
        
        # Scoring Algorithm (Weighted)
        # weight_price increases as preference goes to 0
        # weight_quality increases as preference goes to 100
        quality_weight = preference / 100.0  # 0 to 1
        price_weight = 1.0 - quality_weight # 1 to 0
        
        # Base stats
        rating_impact = supplier.rating * 15 # Constant baseline
        quality_impact = (quality_score * 20) * quality_weight
        price_impact = (total_cost * 0.1) * price_weight
        
        score = rating_impact + quality_impact - price_impact
        
        ranked_suppliers.append({
            'supplier': supplier,
            'score': round(score, 2),
            'total_cost': total_cost,
            'is_local': 'Local' in supplier.location,
            'shipping_raw': supplier.shipping_cost,
            'tax_raw': supplier.taxes
        })
    
    # Sort by score descending
    ranked_suppliers.sort(key=lambda x: x['score'], reverse=True)
    return ranked_suppliers
