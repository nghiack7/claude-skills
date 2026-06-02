---
name: scalability-design
description: This skill should be used when the user asks to "optimize performance", "scale the system", "handle more traffic", "reduce latency", "capacity planning", or mentions scalability design, load balancing, caching strategy, or performance bottlenecks.
patterns: []
---

# Scalability Design Skill

Knowledge of designing systems for scale and performance.

## What This Skill Provides

- Scalability patterns
- Performance optimization
- Bottleneck identification
- Load planning

## Scalability Dimensions

### Vertical Scaling (Scale Up)
Add more resources to single machine
- **Pros:** Simple, no code changes
- **Cons:** Limited ceiling, single point of failure

### Horizontal Scaling (Scale Out)
Add more machines
- **Pros:** Nearly unlimited, fault tolerant
- **Cons:** Complexity, data consistency

## Performance Patterns

### Caching
- **Browser cache:** Static assets
- **CDN:** Global content delivery
- **Application cache:** Redis, Memcached
- **Database cache:** Query results

### Load Balancing
- Round robin
- Least connections
- Geographic routing
- Health-based routing

### Database Scaling
- Read replicas
- Sharding (horizontal partitioning)
- Indexing
- Connection pooling

### Async Processing
- Message queues
- Background jobs
- Event streams

## Performance Metrics

### Latency
- P50, P95, P99 response times
- Target: P95 < 200ms for API

### Throughput
- Requests per second
- Concurrent users
- Data volume

### Resource Utilization
- CPU usage
- Memory consumption
- Network bandwidth
- Disk I/O

## Bottleneck Identification

1. Profile application
2. Identify slow operations
3. Analyze root cause
4. Optimize or scale
5. Measure improvement

## See Also

- `architectural-patterns` - Architecture choices
- `monitoring-observability` - Performance tracking
