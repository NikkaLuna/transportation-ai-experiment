def evaluate_extraction(actual, expected):
    checks = []
    passed = 0

    def add_check(field, actual_value, expected_value, passed_check):
        nonlocal passed
        if passed_check:
            passed += 1

        checks.append({
            "field": field,
            "actual": actual_value,
            "expected": expected_value,
            "passed": passed_check
        })

    add_check(
        "carrier",
        actual.carrier,
        expected.get("carrier"),
        actual.carrier == expected.get("carrier")
    )

    add_check(
        "weight",
        actual.weight,
        expected.get("weight"),
        actual.weight == expected.get("weight")
    )

    add_check(
        "origin",
        actual.origin,
        expected.get("origin_contains"),
        expected.get("origin_contains", "").lower() in actual.origin.lower()
    )

    add_check(
        "destination",
        actual.destination,
        expected.get("destination_contains"),
        expected.get("destination_contains", "").lower() in actual.destination.lower()
    )

    add_check(
        "pickup_date",
        actual.pickup_date,
        expected.get("pickup_date"),
        actual.pickup_date == expected.get("pickup_date")
    )

    total = len(checks)
    accuracy = passed / total if total > 0 else 0

    return {
        "passed": passed,
        "total": total,
        "accuracy": round(accuracy, 2),
        "checks": checks
    }