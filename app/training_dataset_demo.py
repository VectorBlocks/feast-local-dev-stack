from __future__ import annotations

from pathlib import Path

import pandas as pd
from feast import FeatureStore


def main() -> None:
    repo_path = Path(__file__).resolve().parents[1] / "example_repo"
    store = FeatureStore(repo_path=str(repo_path))

    # 고정 데이터: 2026-03-05 시점의 피처 조회 (Online과 비교해 시점 차이 확인)
    entity_df = pd.DataFrame(
        {
            "customer_id": [1001, 1002, 1003],
            "event_timestamp": pd.to_datetime([
                "2026-03-05T12:00:00Z",
                "2026-03-05T12:00:00Z",
                "2026-03-05T12:00:00Z",
            ]),
        }
    )

    feature_service = [
        "customer_stats:purchase_count_30d",
        "customer_stats:avg_order_value_30d",
        "customer_stats:days_since_last_purchase",
    ]

    training_df = store.get_historical_features(
        entity_df=entity_df,
        features=feature_service,
    ).to_df()

    print(training_df)


if __name__ == "__main__":
    main()
