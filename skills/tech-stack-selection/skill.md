---
name: tech-stack-selection
description: This skill should be used when the user asks to "evaluate technology", "compare frameworks", "choose a database", "pick a language", "select tech stack", or needs structured criteria for technology evaluation and architectural decisions.
patterns: []
---

# Tech Stack Selection Skill

Knowledge for evaluating and selecting technologies.

## What This Skill Provides

- Technology evaluation criteria
- Trade-off analysis
- Future-proofing strategies
- Migration considerations

## Selection Criteria

### 1. Team Expertise
- Does team know this technology?
- How steep is learning curve?
- Hiring availability?

### 2. Ecosystem Maturity
- Library/framework stability
- Community size
- Documentation quality
- Long-term support

### 3. Performance Requirements
- Throughput needs
- Latency requirements
- Resource constraints
- Scaling characteristics

### 4. Development Velocity
- Time to first value
- Iteration speed
- Debugging tools
- Testing support

### 5. Operational Considerations
- Deployment complexity
- Monitoring/observability
- Security track record
- Maintenance burden

### 6. Cost
- Licensing
- Infrastructure
- Training
- Opportunity cost

## Common Tech Stacks

### Language Choices
- **TypeScript:** Type safety, JavaScript ecosystem
- **Python:** Data science, rapid development
- **Go:** Performance, concurrency
- **Rust:** Safety, performance

### Database Choices
- **PostgreSQL:** Relational, ACID, complex queries
- **MongoDB:** Document store, flexibility
- **Redis:** Caching, sessions, real-time

### API Choices
- **REST:** Simple, stateless, cacheable
- **GraphQL:** Flexible queries, type system
- **gRPC:** Performance, streaming, type safety

## Decision Framework

1. List requirements
2. Identify candidates
3. Create evaluation matrix
4. Score each option
5. Consider trade-offs
6. Make decision
7. Document in ADR

## See Also

- `architectural-patterns` - Architecture decisions
- Template: `templates/adr-template.md`
