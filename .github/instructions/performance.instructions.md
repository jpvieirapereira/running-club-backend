---
description: 'Performance optimization guidelines for servidor backend'
applyTo: '**/*.py'
---

# Performance Optimization Guidelines

## General Performance Principles

- **Measure first, optimize later** - Use profiling before optimization
- **Optimize hot paths** - Focus on frequently executed code
- **Avoid premature optimization** - Keep code readable first
- **Use async/await properly** - Don't block the event loop
- **Cache strategically** - Balance speed with consistency

## Python Performance

### Efficient Data Structures

Use appropriate data structures:
- **Lists** for ordered sequences with frequent iteration
- **Sets** for membership testing and unique values
- **Dicts** for key-value lookups
- **Tuples** for immutable sequences

Avoid:
```python
# Slow - O(n) lookup
if item in list_of_items:
    pass
```

Prefer:
```python
# Fast - O(1) lookup
if item in set_of_items:
    pass
```

### List Comprehensions

Use list comprehensions over loops for better performance:

```python
# Faster
result = [x * 2 for x in items if x > 0]

# Slower
result = []
for x in items:
    if x > 0:
        result.append(x * 2)
```

### Generator Expressions

Use generators for large datasets to save memory:

```python
# Memory efficient
total = sum(x * 2 for x in large_dataset)

# Memory intensive
total = sum([x * 2 for x in large_dataset])
```

## FastAPI Performance

### Async vs Sync

Use async for I/O-bound operations:
```python
# Good - async for database/API calls
@router.get("/tasks")
async def list_tasks():
    return await task_service.get_all()

# Bad - sync blocks event loop
@router.get("/tasks")
def list_tasks():
    return task_service.get_all_sync()
```

### Response Models

Use `response_model` for automatic serialization:
```python
@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks():
    # FastAPI handles serialization efficiently
    return await task_service.get_all()
```

### Dependency Caching

Cache expensive dependencies:
```python
from functools import lru_cache

@lru_cache()
def get_settings():
    return Settings()
```

## DynamoDB Performance

### Query Optimization

**Use Queries, not Scans**:
```python
# Fast - O(log n) query with key
response = table.query(
    KeyConditionExpression=Key('user_id').eq(user_id)
)

# Slow - O(n) full table scan
response = table.scan(
    FilterExpression=Attr('user_id').eq(user_id)
)
```

### Batch Operations

Use batch operations for multiple items:
```python
# Efficient batch write
with table.batch_writer() as batch:
    for item in items:
        batch.put_item(Item=item)

# Slow - individual writes
for item in items:
    table.put_item(Item=item)
```

### Projection Expressions

Fetch only needed attributes:
```python
# Fetch only required fields
response = table.get_item(
    Key={'id': task_id},
    ProjectionExpression='id,title,completed'
)
```

### Global Secondary Indexes

Use GSIs for efficient queries on non-key attributes:
- Plan GSIs based on access patterns
- Consider query vs storage costs
- Use sparse indexes when appropriate

## S3 Performance

### Multipart Upload

Use multipart for large files:
```python
# For files > 100MB
s3_client.upload_fileobj(
    file_obj,
    bucket,
    key,
    Config=TransferConfig(multipart_threshold=100 * 1024 * 1024)
)
```

### Parallel Downloads

Download multiple files concurrently:
```python
import asyncio

async def download_files(keys):
    tasks = [download_file(key) for key in keys]
    return await asyncio.gather(*tasks)
```

### Signed URL Caching

Cache signed URLs when possible:
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_signed_url(key: str, expiry: int = 3600):
    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expiry
    )
```

## Caching Strategies

### Application-Level Caching

Use caching for expensive operations:
```python
from functools import lru_cache
from typing import Dict

@lru_cache(maxsize=128)
async def get_user_settings(user_id: str) -> Dict:
    return await settings_repo.get(user_id)
```

### Response Caching

Cache API responses when appropriate:
```python
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

@router.get("/public/tasks")
@cache(expire=60)  # Cache for 60 seconds
async def list_public_tasks():
    return await task_service.get_public_tasks()
```

### Cache Invalidation

Clear cache when data changes:
```python
@router.put("/tasks/{task_id}")
async def update_task(task_id: UUID, data: TaskUpdate):
    result = await task_service.update(task_id, data)
    # Invalidate related caches
    cache.invalidate(f"task:{task_id}")
    return result
```

## Connection Pooling

### boto3 Resource Reuse

Reuse boto3 clients/resources:
```python
# Good - reuse client
class DynamoDBRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('users')

# Bad - create client per request
def get_user():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')
```

## Monitoring Performance

### Profiling

Use profiling tools to identify bottlenecks:
```bash
# Profile code execution
python -m cProfile -s cumulative entrypoints/asgi.py

# Use line profiler for detailed analysis
pip install line_profiler
```

### Logging Performance Metrics

Log slow operations:
```python
import time

async def slow_operation():
    start = time.time()
    result = await expensive_call()
    duration = time.time() - start
    
    if duration > 1.0:  # Log if > 1 second
        logger.warning(f"Slow operation: {duration:.2f}s")
    
    return result
```

### AWS X-Ray

Use X-Ray for Lambda performance monitoring:
```python
from aws_xray_sdk.core import xray_recorder

@xray_recorder.capture('process_task')
async def process_task(task_id):
    # X-Ray will trace this function
    return await task_service.process(task_id)
```

## Memory Optimization

### Avoid Memory Leaks

- Close file handles explicitly
- Clear large data structures when done
- Use generators for large datasets
- Be careful with global state

### Batch Processing

Process large datasets in batches:
```python
async def process_all_users():
    page = 0
    page_size = 100
    
    while True:
        users = await user_repo.get_page(page, page_size)
        if not users:
            break
            
        for user in users:
            await process_user(user)
        
        page += 1
```

## Lambda-Specific Optimizations

### Cold Start Reduction

- Keep deployment package small
- Use Lambda layers for dependencies
- Initialize resources outside handler
- Use provisioned concurrency for critical functions

### Handler Optimization

```python
# Initialize outside handler (reused across invocations)
container = Container()
app = create_app()

# Handler function
def handler(event, context):
    return mangum_handler(event, context)
```

## Performance Testing

### Load Testing

Use tools like `locust` or `k6`:
```bash
# Install locust
pip install locust

# Run load test
locust -f tests/load_test.py --host http://localhost:8000
```

### Benchmarking

Benchmark critical paths:
```python
import timeit

def benchmark_query():
    result = timeit.timeit(
        'task_repo.get_by_user_id(user_id)',
        globals=globals(),
        number=1000
    )
    print(f"Average: {result/1000:.4f}s")
```

## Performance Checklist

- [ ] Database queries use indexes
- [ ] Batch operations where applicable
- [ ] Async/await used correctly
- [ ] Caching implemented for expensive operations
- [ ] Large datasets processed in batches
- [ ] Connection pools configured
- [ ] Monitoring and logging in place
- [ ] Load testing performed
- [ ] Memory usage optimized
- [ ] Lambda cold starts minimized (if applicable)
