from __future__ import annotations

from pathlib import Path

from feast import FeatureStore


def main() -> None:
    repo_path = Path(__file__).resolve().parents[1] / "example_repo"
    store = FeatureStore(repo_path=str(repo_path))

    response = store.get_online_features(
        features=[
            "customer_stats:purchase_count_30d",
            "customer_stats:avg_order_value_30d",
            "customer_stats:days_since_last_purchase",
            "customer_profile:signup_days_ago",
            "customer_profile:is_vip",
        ],
        entity_rows=[{"customer_id": 1001}, {"customer_id": 1002}, {"customer_id": 1003}],
    ).to_dict()

    print(response)


if __name__ == "__main__":
    main()
