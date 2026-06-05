from prometheus_client import Counter, Histogram, REGISTRY

def get_or_create_counter(name, description, labels=[]):
    try:
        return Counter(name, description, labels)
    except ValueError:
        return REGISTRY._names_to_collectors.get(name)

def get_or_create_histogram(name, description):
    try:
        return Histogram(name, description)
    except ValueError:
        return REGISTRY._names_to_collectors.get(name)

PREDICTION_COUNT = get_or_create_counter(
    'fraud_predictions_total',
    'Total predictions',
    ['result']
)

PREDICTION_LATENCY = get_or_create_histogram(
    'fraud_prediction_latency_seconds',
    'Prediction latency'
)

REQUEST_COUNT = get_or_create_counter(
    'api_requests_total',
    'Total requests',
    ['endpoint', 'status']
)