from feast import FeatureService, Field, FeatureView, FileSource
from feast.types import Float32, Int64

from entities import customer

# --- customer_stats (시계열 피처) ---
customer_stats_source = FileSource(
    name="customer_stats_source",
    path="data/customer_stats.parquet",
    timestamp_field="event_timestamp",
)

customer_stats_fv = FeatureView(
    name="customer_stats",
    entities=[customer],
    ttl=None,
    schema=[
        Field(name="purchase_count_30d", dtype=Int64, description="최근 30일 구매 건수 (Purchase count in the last 30 days)"),
        Field(name="avg_order_value_30d", dtype=Float32, description="최근 30일 평균 주문 금액, 원 (Average order value in the last 30 days, KRW)"),
        Field(name="days_since_last_purchase", dtype=Int64, description="마지막 구매 경과일 (Days since the customer's last purchase)"),
    ],
    online=True,
    source=customer_stats_source,
    tags={"owner": "opensource", "stage": "dev"},
)

# --- customer_profile (정적 피처) ---
customer_profile_source = FileSource(
    name="customer_profile_source",
    path="data/customer_profile.parquet",
    timestamp_field="event_timestamp",
)

customer_profile_fv = FeatureView(
    name="customer_profile",
    entities=[customer],
    ttl=None,
    schema=[
        Field(name="signup_days_ago", dtype=Int64, description="가입 경과일 (Days since customer signup)"),
        Field(name="is_vip", dtype=Int64, description="VIP 멤버십 여부 (0 또는 1) (VIP membership flag (0 or 1))"),
    ],
    online=True,
    source=customer_profile_source,
    tags={"owner": "opensource", "stage": "dev"},
)

# --- Feature Service: 피처 번들링 ---
# 여러 feature view를 묶어 이름 있는 피처 세트로 정의 (팀 협업, 모델별 피처 관리에 유용)
recommendation_fs = FeatureService(
    name="recommendation_features",
    features=[customer_stats_fv, customer_profile_fv],
    description="추천 모델용 피처 (Recommendation model features)",
)
