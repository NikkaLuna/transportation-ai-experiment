from datetime import datetime

def validate_business_rules(shipment):
    warnings = []
    actions = []

    if shipment.weight is None or shipment.weight <= 0:
        warnings.append("Shipment weight must be greater than 0.")
        actions.append("Verify shipment weight before approval.")

    if shipment.origin and shipment.destination:
        if shipment.origin.strip().lower() == shipment.destination.strip().lower():
            warnings.append("Origin and destination cannot be the same.")
            actions.append("Review origin and destination fields.")

    if shipment.delivery_date is None:
        warnings.append("Delivery date is missing.")
        actions.append("Request or verify delivery date before final approval.")

    if shipment.pickup_date and shipment.delivery_date:
        try:
            pickup = datetime.fromisoformat(shipment.pickup_date)
            delivery = datetime.fromisoformat(shipment.delivery_date)

            if delivery < pickup:
                warnings.append("Delivery date cannot be before pickup date.")
                actions.append("Review pickup and delivery dates.")
        except ValueError:
            warnings.append("Pickup or delivery date is not in valid YYYY-MM-DD format.")
            actions.append("Correct shipment date formatting.")

    if shipment.confidence < 0.75:
        warnings.append("Extraction confidence is below review threshold.")
        actions.append("Send shipment for manual review.")

    return {
        "business_rule_warnings": warnings,
        "business_rule_actions": actions
    }