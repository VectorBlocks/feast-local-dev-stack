from feast import Entity, ValueType

# Entity 조인 키 등 기본 설명 (Feast가 비워둔 경우 노트북 피처 정의 보기에서 사용)
DEFAULT_DESCRIPTIONS = {"customer_id": "고객 ID (Customer identifier, entity join key)"}

customer = Entity(
    name="customer",
    join_keys=["customer_id"],
    value_type=ValueType.INT64,
    description="Customer entity",
)
