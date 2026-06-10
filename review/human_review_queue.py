import json
from pathlib import Path
from datetime import datetime


def dedupe_reasons(reasons):
    """Remove duplicate review reasons, including differently worded similar reasons."""
    seen = set()
    deduped = []

    for reason in reasons:
        normalized = reason.lower().strip()

        # Group similar delivery-date warnings together
        if "delivery date" in normalized:
            normalized = "delivery_date_missing"

        # Group similar low-confidence warnings together
        if "confidence" in normalized:
            normalized = "low_confidence"

        if normalized not in seen:
            seen.add(normalized)
            deduped.append(reason)

    return deduped


def add_to_review_queue(
    shipment,
    policy_validation,
    business_rules,
    output_path="review_queue.json"
):
    review_reasons = []

    if shipment.confidence < 0.75:
        review_reasons.append("Low extraction confidence")

    review_reasons.extend(policy_validation.compliance_warnings)
    review_reasons.extend(business_rules["business_rule_warnings"])

    review_reasons = dedupe_reasons(review_reasons)

    if not review_reasons:
        return {
            "review_required": False,
            "review_reasons": []
        }

    review_record = {
        "created_at": datetime.utcnow().isoformat(),
        "shipment_id": shipment.shipment_id,
        "carrier": shipment.carrier,
        "origin": shipment.origin,
        "destination": shipment.destination,
        "review_required": True,
        "review_reasons": review_reasons
    }

    path = Path(output_path)

    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
    else:
        existing = []

    existing.append(review_record)

    path.write_text(json.dumps(existing, indent=2), encoding="utf-8")

    return {
        "review_required": True,
        "review_reasons": review_reasons
    }