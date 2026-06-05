from prometheus_client import Counter, Histogram

PREDICITON_COUNT =  Counter(
    'fraud_prediction_total',
    'Total predicitons',
    ['result']
)

PREDICTION_LATENCY = Histogram(
    'fraud_prediction',
    'prediction latency'

)

REQUEST_COUNT = Counter(
    'api_requests_total',
    'Total requests',
    ['endpoint', 'status']
)