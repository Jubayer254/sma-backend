import multiprocessing

# Number of worker processes
workers = multiprocessing.cpu_count() * 2 + 1

# Request timeout
timeout = 300

# Maximum requests before restarting a worker
max_requests = 1000

# Jitter to add to max_requests for randomness
max_requests_jitter = 100

# Keep-alive timeout for connections
keepalive = 5