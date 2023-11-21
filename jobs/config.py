config = {
    "openai": {
        "api_key": "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"
    },
    "kafka": {
        "sasl.username": "5ZT56YOWTALOMBQE",
        "sasl.password": "Qt9pFnsiK2trRpl8rugHbAI9kgYQaU7ZPYgU5ssxVc47AQ5ikk8vHSUbiJzqMUv+",
        "bootstrap.servers": "pkc-ldvr1.asia-southeast1.gcp.confluent.cloud:9092",
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'session.timeout.ms': 50000
    },
    "schema_registry": {
        "url": "https://psrc-3w372.australia-southeast1.gcp.confluent.cloud",
        "basic.auth.user.info": "LFAMBU4K6OGMEKIM:U38uBac+u+6V8jJBUnp71Ax6Q1swrPipfw3h6gffpxtm848q4W6IG8tMY3Dw8yC1"
    }
}

# config = {
#     "openai": {
#         "api_key": "OPENAI_KEY"
#     },
#     "kafka": {
#         "sasl.username": "KAFKA_CLUSTER_API_KEY",
#         "sasl.password": "KAFKA_CLUSTER_API_SECRET",
#         "bootstrap.servers": "KAFKA_CLUSTER_BOOTSTRAP_SERVER_URL:PORT",
#         'security.protocol': 'SASL_SSL',
#         'sasl.mechanisms': 'PLAIN',
#         'session.timeout.ms': 50000
#     },
#     "schema_registry": {
#         "url": "SCHEMA_REGISTRY_URL",
#         "basic.auth.user.info": "SR_API_KEY:SR_API_SECRET"

#     }
# }