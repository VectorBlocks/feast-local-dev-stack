"""
고정 데이터셋: 3명 고객, 10일치 (2026-03-01 ~ 2026-03-10)

Online vs Historical 차이를 학습하기 쉽도록:
- 각 고객이 10일 동안 매일 1개 행 보유 (총 30행)
- 날짜별로 피처 값이 변하여 Historical(point-in-time) 조회 시 차이 확인 가능
- Online 조회: 가장 최근(03-10) 값 반환
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

# 고정 기준일: 2026-03-10 (기간: 03-01 ~ 03-10)
BASE_DATE = datetime(2026, 3, 10, tzinfo=timezone.utc).replace(microsecond=0)

# 3명 고객 × 10일 = 30행
# 각 행: (customer_id, event_date_offset, purchase_count_30d, avg_order_value_30d, days_since_last_purchase)
# offset: 0=03-01, 1=03-02, ..., 9=03-10
# 현실적인 패턴: 구매 빈도·금액·마지막구매일이 날짜에 따라 변함
CUSTOMER_DAILY_DATA = [
    # 고객 1001: 활발한 구매자, 10일 내 3회 구매
    (1001, 0, 8, 42000.0, 3),   # 03-01
    (1001, 1, 8, 41500.0, 2),   # 03-02
    (1001, 2, 9, 43000.0, 1),   # 03-03 (전날 구매)
    (1001, 3, 9, 42800.0, 0),   # 03-04 (당일 구매)
    (1001, 4, 9, 42500.0, 1),   # 03-05
    (1001, 5, 9, 42200.0, 2),   # 03-06
    (1001, 6, 10, 43500.0, 0),  # 03-07 (당일 구매)
    (1001, 7, 10, 43200.0, 1),  # 03-08
    (1001, 8, 10, 43000.0, 2),  # 03-09
    (1001, 9, 11, 43800.0, 0),  # 03-10 (최종일 구매)
    # 고객 1002: 보통 구매자, 10일 내 1회 구매
    (1002, 0, 4, 85000.0, 12),  # 03-01
    (1002, 1, 4, 84800.0, 13),  # 03-02
    (1002, 2, 4, 84500.0, 14),  # 03-03
    (1002, 3, 5, 87200.0, 0),   # 03-04 (당일 구매)
    (1002, 4, 5, 86800.0, 1),   # 03-05
    (1002, 5, 5, 86500.0, 2),   # 03-06
    (1002, 6, 5, 86200.0, 3),   # 03-07
    (1002, 7, 5, 86000.0, 4),   # 03-08
    (1002, 8, 5, 85800.0, 5),   # 03-09
    (1002, 9, 5, 85600.0, 7),   # 03-10
    # 고객 1003: 저구매 고객
    (1003, 0, 1, 15000.0, 25),  # 03-01
    (1003, 1, 1, 15000.0, 26),  # 03-02
    (1003, 2, 1, 15000.0, 27),  # 03-03
    (1003, 3, 1, 15000.0, 28),  # 03-04
    (1003, 4, 2, 22500.0, 0),   # 03-05 (당일 구매)
    (1003, 5, 2, 22200.0, 1),   # 03-06
    (1003, 6, 2, 22000.0, 2),   # 03-07
    (1003, 7, 2, 21800.0, 3),   # 03-08
    (1003, 8, 2, 21600.0, 4),   # 03-09
    (1003, 9, 2, 21400.0, 6),   # 03-10
]


def build_rows() -> pd.DataFrame:
    rows = []
    for customer_id, day_offset, purchase_count, avg_value, days_since in CUSTOMER_DAILY_DATA:
        event_ts = BASE_DATE - timedelta(days=9 - day_offset)
        rows.append(
            {
                "customer_id": customer_id,
                "event_timestamp": event_ts,
                "created_timestamp": event_ts,
                "purchase_count_30d": purchase_count,
                "avg_order_value_30d": avg_value,
                "days_since_last_purchase": days_since,
            }
        )
    return pd.DataFrame(rows)


# 고객 프로필 (정적): 고객당 1행
# (customer_id, signup_days_ago, is_vip)
CUSTOMER_PROFILE_DATA = [
    (1001, 90, 1),   # 활발한 구매자, VIP
    (1002, 180, 0),  # 보통 구매자
    (1003, 30, 0),   # 저구매, 신규
]


def build_profile_rows() -> pd.DataFrame:
    # 정적 데이터: event_timestamp는 Feast 필수 필드 (기준일 03-01 사용)
    base_ts = BASE_DATE - timedelta(days=9)
    rows = []
    for customer_id, signup_days_ago, is_vip in CUSTOMER_PROFILE_DATA:
        rows.append(
            {
                "customer_id": customer_id,
                "event_timestamp": base_ts,
                "created_timestamp": base_ts,
                "signup_days_ago": signup_days_ago,
                "is_vip": is_vip,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    out_dir = Path(__file__).parent / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    df = build_rows()
    df.to_parquet(out_dir / "customer_stats.parquet", index=False)
    profile_df = build_profile_rows()
    profile_df.to_parquet(out_dir / "customer_profile.parquet", index=False)
    entity_df = df[["customer_id"]].drop_duplicates()
    entity_df.to_parquet(out_dir / "entity_rows.parquet", index=False)
    print(f"Wrote {len(df)} rows (3 customers × 10 days) to {out_dir / 'customer_stats.parquet'}")
    print(f"Wrote {len(profile_df)} rows (3 customers) to {out_dir / 'customer_profile.parquet'}")


if __name__ == "__main__":
    main()
