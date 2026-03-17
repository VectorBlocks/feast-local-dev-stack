# Notebooks

Jupyter 노트북 기반 Feast 워크스루입니다.

## feast_walkthrough.ipynb

단계별로 피처스토어(Feast)를 경험하는 워크스루 노트북입니다.

- FeatureStore 연결
- Online 피처 조회 (실시간 추론용)
- Historical 피처 조회 (모델 학습용)

### 실행 방법

`make apply`, `make materialize`까지 완료한 후:

```bash
make notebook
```

브라우저에서 [http://localhost:8889](http://localhost:8889) 접속 후 `feast_walkthrough.ipynb`를 엽니다.
