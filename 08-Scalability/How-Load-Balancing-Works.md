# How Load Balancing Works: Distributing Traffic at Scale

---

## Introduction

Imagine the world's busiest airport. Tens of thousands of passengers arrive every hour, all trying to reach their gates. Without a system, there would be chaos — everyone funneling into the same security line, the same gate, the same escalator.

The airport solves this with **distribution**: multiple security checkpoints, multiple gates, multiple baggage carousels. A central system directs each passenger to the right place based on current congestion, flight schedules, and gate assignments.

**Load balancing is the airport's traffic management system for the internet.** It distributes incoming network traffic across a group of backend servers, ensuring no single server bears too much load. It's the reason Google, Amazon, Netflix, and every other large-scale service can handle millions of simultaneous users without crashing.

A **load balancer** sits between the user and the servers, acting as the single point of contact. Users connect to the load balancer, and the load balancer forwards each request to one of the backend servers based on configurable rules.

### Why Should Engineers Care About Load Balancing?

Load balancing is not just for huge companies. Any application that runs on more than one server needs it. Engineers who understand load balancing deeply can:

- Design systems that gracefully handle traffic spikes (Black Friday, product launches)
- Build zero-downtime deployment pipelines (rolling updates behind a load balancer)
- Diagnose performance issues caused by uneven traffic distribution
- Design global systems that route users to the nearest data center
- Make informed decisions about which load balancing strategy fits their use case

### Where Is Load Balancing Used?

| Layer | Example | Purpose |
|-------|---------|---------|
| DNS | Global Server Load Balancing | Route users to the nearest data center |
| Network (L4) | AWS NLB, HAProxy TCP mode | Distribute TCP/UDP traffic efficiently |
| Application (L7) | NGINX, AWS ALB, Traefik | Route HTTP requests based on URL, headers, cookies |
| Database | ProxySQL, Pgpool-II | Distribute read queries across replicas |
| Service Mesh | Envoy, Linkerd | Load balance between microservices |

---

## The Problem It Solves

### The Single Server Limit

Every server has finite capacity. A single web server might handle 10,000 concurrent connections, serve 1,000 requests per second, or process 100 Mbps of traffic. When demand exceeds these limits, the server becomes overloaded — response times spike, connections time out, and eventually the server crashes.

### The Scaling Problem

To handle more users, you need more servers. But adding servers creates a new problem: **how do you distribute traffic across them?**

Without a load balancer, you might:

1. **Give users different IPs** — "Try server A, and if it's slow, try server B." This is terrible user experience.
2. **Use DNS round-robin** — Return multiple IPs for the same domain name. Simple, but DNS doesn't know if a server is healthy, and caching means you can't quickly redirect traffic.
3. **Hard-code server lists** — Clients maintain a list of server IPs and randomly pick one. This doesn't scale and creates client management headaches.

### What Load Balancing Provides

| Need | How Load Balancing Solves It |
|------|------------------------------|
| **Scalability** | Add or remove servers without changing client configuration |
| **High availability** | Automatically route around failed servers |
| **Performance** | Distribute load based on server capacity and current utilization |
| **Maintenance** | Drain connections from a server before taking it offline |
| **Security** | Hide backend server architecture from the internet |

### What Happens Without Load Balancing?

- A single server bears all traffic, becoming a bottleneck and single point of failure
- Server failures cause downtime — every user is affected
- Scaling requires manual reconfiguration of every client
- Traffic spikes overwhelm the server, causing cascading failures
- No graceful way to perform maintenance or deploy updates

---

## Historical Background

### 1990s: Hardware Load Balancers

The first load balancers were dedicated hardware appliances — expensive boxes installed in data centers. Companies like **F5 Networks** (founded 1996) and **Citrix** (with its NetScaler product) dominated the market. These appliances offered:

- Dedicated ASICs for fast packet processing
- Built-in SSL termination hardware
- Advanced health checking and failover

**Limitations:** Cost ($10,000–$100,000+ per appliance), limited flexibility, vendor lock-in, and capacity constraints (hardware can only handle so much traffic before you need another $50,000 box).

### 2000s: Software Load Balancers Emerge

As web traffic grew and commodity hardware became more powerful, software-based load balancers emerged:

- **2002: HAProxy** — High-performance TCP/HTTP proxy, became the gold standard for open-source load balancing
- **2004: NGINX** — Started as a web server, evolved into a full-featured load balancer and reverse proxy
- **2009: AWS Elastic Load Balancer** — First major cloud-native load balancer, integrated with auto-scaling

Software load balancers ran on standard servers, cost nothing (or very little compared to hardware), and could be scaled horizontally by adding more instances.

### 2010s: Cloud-Native and Global Load Balancing

The cloud era transformed load balancing:

- **2012: AWS Application Load Balancer (ALB)** — Layer 7 routing, content-based routing
- **2015: Google's Maglev** — Published the design of their software-defined network load balancer
- **2016: Envoy Proxy** — High-performance sidecar proxy for service mesh architectures
- **2017: Cloudflare's Unimog** — Cloudflare's L4 load balancer handling global traffic

Load balancing moved from a hardware appliance in a rack to a distributed software layer running across hundreds of data centers worldwide.

### 2020s: Service Mesh and Multi-Cloud

Modern architectures have made load balancing even more critical:

- Service meshes (Istio, Linkerd) provide per-instance load balancing between microservices
- Multi-cloud deployments require load balancing across providers
- Edge computing pushes load balancing to the network edge (Cloudflare Workers, AWS Lambda@Edge)

---

## Core Concepts

### What Is a Load Balancer?

A **load balancer** is a reverse proxy that distributes incoming traffic across a group of backend servers (called a **server pool**, **backend pool**, or **upstream**).

```
Client ---> Load Balancer ---> Server A
                            --> Server B
                            --> Server C
```

The client sees only the load balancer. The backend servers are hidden behind it.

### Layer 4 vs Layer 7 Load Balancing

Load balancers operate at different layers of the OSI model:

| Feature | Layer 4 (Transport) | Layer 7 (Application) |
|---------|--------------------|----------------------|
| **What it sees** | IP addresses, TCP/UDP ports | HTTP headers, URLs, cookies, request body |
| **Routing decisions** | Source/destination IP, port, protocol | URL path, host header, cookie, content type |
| **Performance** | Very fast (no content inspection) | Slightly slower (content inspection) |
| **Use cases** | TCP, UDP, WebSocket, gaming | HTTP/HTTPS APIs, web applications |
| **Examples** | HAProxy (TCP mode), AWS NLB | NGINX, AWS ALB, Traefik |

**Layer 4 Example:**
```
Client connects to load balancer on port 443 (TCP)
Load balancer forwards to backend server:PORT
No inspection of HTTP content
```

**Layer 7 Example:**
```
Client sends HTTP request to load balancer:
  GET /api/users HTTP/1.1
  Host: example.com

Load balancer inspects the URL path:
  /api/* → backend pool "api-servers"
  /images/* → backend pool "image-servers"
```

### Server Pools (Upstreams)

A **server pool** is a group of backend servers that serve the same application or service. The load balancer distributes requests among them.

```
Load Balancer
  │
  ├── upstream "web-servers"
  │   ├── 10.0.1.10:8080 (weight: 5)
  │   ├── 10.0.1.11:8080 (weight: 3)
  │   └── 10.0.1.12:8080 (weight: 1)
  │
  └── upstream "api-servers"
      ├── 10.0.2.10:9000
      └── 10.0.2.11:9000
```

### Health Checks

A load balancer must know which servers are healthy before sending them traffic. **Health checks** are automated probes that test server availability.

**Active health checks:** The load balancer periodically sends requests (e.g., HTTP GET `/health`) to each server. If the server doesn't respond within a timeout or returns an error status, it's marked as unhealthy and removed from the pool.

```
Time t1: Load balancer → GET /health → Server A → 200 OK ✓
Time t2: Load balancer → GET /health → Server A → timeout ✗
         (Server A removed from pool)
Time t3: Load balancer → GET /health → Server A → 200 OK ✓
         (Server A added back to pool)
```

**Passive health checks:** The load balancer monitors real traffic. If a server returns multiple 5xx errors or connections fail, it's marked as unhealthy.

### Session Persistence (Sticky Sessions)

Some applications store session state locally on the server (e.g., a shopping cart in memory). **Session persistence** ensures that all requests from the same client go to the same backend server.

Common persistence methods:
- **Source IP hash:** Client IP determines the server (simple, but breaks if many users share one IP behind NAT)
- **Cookie insertion:** Load balancer sets a cookie identifying the server; client sends it on subsequent requests
- **Application cookie:** Load balancer reads a cookie set by the application itself

### Load Balancing Algorithms

An **algorithm** determines *which* server receives each request. This is the core decision the load balancer makes. (Covered in detail in the next section.)

---

## Real-World Analogy

### The Bank Teller Queue

Imagine a bank with three teller windows. Customers arrive throughout the day.

**No load balancing (single queue per teller):**
- Teller 1 has a long line (helping a customer with mortgage paperwork)
- Teller 2 is idle (just finished with a simple deposit)
- Teller 3 has a moderate line

New customers must guess which line to join. They often guess wrong, joining a long line while a teller sits idle. This is inefficient and frustrating.

**Round-robin load balancing:**
- New customers are directed to tellers in order: 1, 2, 3, 1, 2, 3...
- This works well if all customers take the same amount of time
- But mortgage paperwork takes longer than a deposit, so one teller gets backlogged

**Least connections load balancing:**
- A greeter at the door sends each customer to the teller with the shortest line
- Mortgage paperwork customers still take longer, but at least the lines are balanced
- This adapts to varying request durations

**Source IP hash (persistence):**
- Each customer always goes to the same teller, so the teller can remember their preferences
- If a customer leaves their wallet and comes back, they return to the same teller

**Consistent hashing:**
- The bank assigns customers to tellers using a hash of their account number
- If a new teller opens (scale up), only a few customers need to be reassigned
- If a teller goes to lunch (scale down), only that teller's customers are redirected

---

## How It Works Internally

### The Complete Request Flow

When a client sends a request to a load-balanced service, here's the full sequence:

```
  Client (TCP connection)
       │
       ▼
  ┌─────────────────────────────────────┐
  │        Load Balancer                │
  │                                     │
  │  1. Accept connection (terminate    │
  │     TCP/TLS from client)            │
  │                                     │
  │  2. Parse request (L7) or inspect   │
  │     packet headers (L4)             │
  │                                     │
  │  3. Apply routing rules:            │
  │     - Which pool? (URL, host, etc.) │
  │     - Persistence required?         │
  │     - Any rate limits?              │
  │                                     │
  │  4. Select backend server:          │
  │     - Apply load balancing algorithm│
  │     - Check health status           │
  │     - Get server IP:port            │
  │                                     │
  │  5. Forward request to backend:     │
  │     - Open connection to server     │
  │     - Send request (possibly        │
  │       modified with X-Forwarded-For)│
  │                                     │
  │  6. Receive response from backend   │
  │                                     │
  │  7. Send response to client         │
  └─────────────────────────────────────┘
       │
       ▼
  Backend Server (processes request)
```

### Step-by-Step Detail

**Step 1: Connection Termination**

The load balancer accepts the client's TCP connection and terminates TLS (if HTTPS). This means:
- The load balancer holds the SSL certificate, not the backend servers
- Backend servers receive unencrypted HTTP (or re-encrypted with internal certs)
- This offloads expensive encryption/decryption from application servers

**Step 2: Request Parsing**

For Layer 7 load balancers, the request is fully parsed:
- HTTP method (GET, POST, PUT, DELETE)
- URL path (`/api/users`, `/images/logo.png`)
- Headers (Host, Cookie, Content-Type, Authorization)
- Body (for POST/PUT)

**Step 3: Routing Rules**

Based on the parsed request, the load balancer determines which server pool to use:

```
Host: api.example.com → pool: api-servers
Host: www.example.com → pool: web-servers
Path: /images/* → pool: static-assets
Header: X-Region: eu-west → pool: eu-servers
```

**Step 4: Server Selection**

The load balancer applies the selected algorithm to choose a specific server:
- Excludes unhealthy servers (those failing health checks)
- Checks for session persistence (should this client go to a specific server?)
- Returns the chosen server's IP address and port

**Step 5: Request Forwarding**

The load balancer opens a new TCP connection (or reuses a pooled connection) to the backend server. It modifies request headers to preserve client information:
- `X-Forwarded-For`: Original client IP
- `X-Forwarded-Proto`: Original protocol (http or https)
- `X-Real-IP`: Original client IP (common in NGINX)

**Step 6: Response Handling**

The backend processes the request and sends the response back to the load balancer. The load balancer may:
- Compress the response (if configured)
- Add/modify headers (Set-Cookie for session persistence)
- Cache the response (if configured as a caching proxy)

**Step 7: Client Response**

The load balancer sends the response back to the client over the established TLS connection.

---

## Components and Architecture

### 1. Frontend (Listener)

The frontend defines how the load balancer accepts traffic:
- **Protocol** (HTTP, HTTPS, TCP, UDP)
- **Port** (80, 443, 53, etc.)
- **SSL certificate** (for HTTPS)
- **Access control** (allowed IPs, rate limiting)

### 2. Backend Pool (Upstream)

The backend pool defines the group of servers that serve requests:
- **Server list** (IP:port for each backend)
- **Health check configuration** (interval, path, timeout)
- **Load balancing algorithm** (how to distribute requests)
- **Connection limits** (max connections per server)

### 3. Health Checker

A dedicated component that continuously monitors backend servers:
- Sends probes at configured intervals
- Marks servers as healthy/unhealthy
- Logs health transitions for debugging

### 4. Session Store (optional)

For sticky sessions, the load balancer needs a way to remember which client goes to which server. This can be:
- **In-memory** (on the load balancer itself — lost if the load balancer restarts)
- **Cookie-based** (server identifier stored in a cookie on the client)
- **External store** (Redis, Memcached — survives load balancer restarts)

### 5. Statistics and Monitoring

Load balancers expose metrics for observability:
- Active connections per backend
- Request latency (P50, P95, P99)
- Error rates (4xx, 5xx per backend)
- Health check pass/fail count
- Connection pool utilization

### The Auto-Scaling Integration

In cloud environments, the load balancer is tightly coupled with **auto-scaling**:

```
                     ┌──────────────────┐
                     │  Auto-Scaling    │
                     │  Group           │
                     │                  │
                     │  min: 2          │
                     │  max: 20         │
                     │  scaling metric: │
                     │  CPU > 70%       │
                     └────────┬─────────┘
                              │
                              v
Load Balancer ◄──── EC2 Instances / Pods
(Registers & deregisters     (added/removed
 instances automatically)     by auto-scaling)
```

When CPU utilization exceeds 70%, the auto-scaler launches new instances. The load balancer automatically registers them and starts sending traffic. When traffic drops, instances are terminated and deregistered. The entire process happens without manual intervention.

---

## End-to-End Flow

### Example: A Global E-Commerce Site on Black Friday

Let's trace a complete request through Amazon's load balancing infrastructure during peak traffic.

**Background:**
- The e-commerce site runs across multiple AWS regions (us-east-1, eu-west-1, ap-southeast-1)
- Each region has multiple Availability Zones
- Each service (web, API, images) has its own auto-scaling group and load balancer
- Traffic is directed to the nearest healthy region via Amazon Route 53 (DNS GSLB)

**The Request:**
Alice in London opens `www.example.com` on her laptop at 8 PM on Black Friday.

**Step 1: DNS GSLB (Global Level)**

Alice's browser asks for the IP of `www.example.com`. Route 53 (Amazon's global DNS) checks:
- Alice's IP geolocates to London
- Health check: eu-west-1 servers are healthy
- Latency measurement: eu-west-1 has lowest latency from London

Route 53 returns the IP of the **eu-west-1** load balancer (e.g., `lb-eu-12345678.elb.amazonaws.com`).

**Step 2: Regional Load Balancer (ALB)**

Alice's browser connects to the Application Load Balancer in eu-west-1.

The ALB inspects the request:
```
GET /product/black-friday-deals HTTP/1.1
Host: www.example.com
Cookie: session_id=abc123
```

**Routing:**
- URL path `/product/*` → "product-service" target group
- Session cookie `session_id=abc123` → check session persistence table
- Alice previously hit `10.0.1.15:8080` → route to that server (session persistence)

If this were a new session, the ALB would apply **least outstanding requests** to choose the least-loaded server.

**Step 3: Health Check Validation**

Before forwarding, the ALB verifies the server's health. The "product-service" target group has:
- Health check path: `GET /health`
- Interval: 10 seconds
- Healthy threshold: 2 consecutive successes
- Unhealthy threshold: 3 consecutive failures

Two servers in the target group are showing "unhealthy" because they're at 95% CPU. The ALB excludes them.

**Step 4: Request Forwarded**

Alice's request is forwarded to `10.0.1.15:8080` (the product service). The product service processes the request, queries the database, and returns the Black Friday deals page.

**Step 5: Response and Persistence**

The ALB receives the response, sets a cookie `AWSALB=10.0.1.15:8080` (binding Alice to this server), and sends the response to Alice.

If Alice makes another request, the ALB reads the cookie and routes directly to the same server — no algorithm needed.

**Throughout this process:**
- Auto-scaling is launching new EC2 instances in response to traffic spikes
- New instances are automatically registered with the ALB
- If an instance fails health checks, it's deregistered and auto-scaling replaces it
- Across all regions, the system handles 10 million requests per minute — all because of load balancing

---

## Production Engineering Perspective

### Scalability

Load balancers themselves must scale:

| Level | How It Scales | Example |
|-------|---------------|---------|
| **Single load balancer** | Vertical scaling (bigger instance) | Upgrade from t3.medium to t3.large |
| **Active-passive pair** | Primary handles traffic, standby takes over on failure | HAProxy with keepalived |
| **Active-active cluster** | Multiple load balancers share traffic | DNS round-robin across multiple LBs |
| **Global (Anycast)** | LB instances in multiple locations sharing one IP | Cloudflare, Google Cloud LB |

**Key principle:** The load balancer should never be the bottleneck. In production, use multiple load balancer instances behind a DNS-based or Anycast front-end.

### Reliability

- **Redundancy:** Always run at least two load balancer instances across different availability zones
- **Health checks:** Configure both active (probes) and passive (monitoring real traffic) health checks
- **Graceful degradation:** If all backend servers are unhealthy, the load balancer should return a friendly error page, not a connection refused
- **Connection draining:** When deregistering a server, wait for in-flight requests to complete before dropping connections

**Connection draining:**
```
Time t0: Server A marked for deregistration
Time t0-t30: Existing connections continue, but no new connections are sent to Server A
Time t30: Server A is fully removed. All remaining connections are forcibly closed.
```

### Performance

| Metric | Target | How to Achieve |
|--------|--------|----------------|
| **Latency added by LB** | < 1ms (L4), < 5ms (L7) | Use kernel bypass (DPDK) for extreme performance |
| **Connection capacity** | 10,000+ concurrent connections | Tune OS limits, use connection pooling |
| **Throughput** | 1+ Gbps per instance | Distribute across multiple LB instances |
| **Health check frequency** | Every 5-10 seconds | Balance between freshness and overhead |

### Availability

- **Multi-AZ deployment:** Load balancer instances spread across at least 2 availability zones
- **Auto-recovery:** If a load balancer instance fails, DNS or health checks redirect traffic to healthy instances
- **No single point of failure:** The load balancer itself must not be a single point of failure

### Maintainability

- **Gradual traffic shifting:** When changing load balancer configuration, shift traffic gradually (1% → 10% → 100%), monitoring for errors at each step
- **Canary deployments:** Route 1% of traffic to a new version of the application through the load balancer, then increase if no errors
- **Logging and monitoring:** Load balancer logs are critical for debugging — enable access logs (shows every request, latency, backend selected)

---

## Tradeoffs

### ✅ Benefits

| Benefit | Explanation |
|---------|------------|
| **Horizontal scaling** | Add servers without changing client configuration |
| **High availability** | Automatic failover around failed servers |
| **Zero-downtime deployments** | Drain servers one at a time during rolling updates |
| **SSL termination** | Offload encryption from application servers |
| **Content-based routing** | Route `/api` to one pool, `/static` to another |
| **Centralized security** | DDoS protection, rate limiting, IP whitelisting in one place |

### ❌ Drawbacks

| Drawback | Explanation |
|----------|------------|
| **Single point of failure** | The load balancer itself can fail (mitigate with redundancy) |
| **Added latency** | Every request passes through an extra hop (typically 1-5ms) |
| **Configuration complexity** | Many settings to tune (algorithms, health checks, timeouts) |
| **Session persistence limitations** | Sticky sessions reduce the benefits of load balancing |
| **Cost** | Hardware LBs are expensive; cloud LBs cost per GB/connection-hour |

### ⚠️ Limitations

- **Load balancers cannot fix slow applications** — If every backend server is slow, distributing load doesn't help. You need to scale or optimize.
- **Stateless applications work best** — The more state your application has, the harder load balancing becomes (sticky sessions, distributed caches).
- **Health checks are not perfect** — A server might pass a health check but still serve broken responses. Passive health checks help but are reactive.

### 🔁 Alternatives

| Approach | When to Use |
|----------|------------|
| **DNS round-robin** | Simple traffic distribution with low precision |
| **Client-side load balancing** | Each client maintains its own list of servers (Netflix Ribbon) |
| **Service mesh** | Per-instance load balancing between microservices (Envoy, Linkerd) |
| **Event-driven architecture** | Use message queues to decouple producers from consumers |

### When NOT to Use a Load Balancer

- **Single-server applications** — Unnecessary complexity if you only have one server
- **Development environments** — Add load balancers after you have multiple instances
- **Serverless architectures** — The platform (AWS Lambda, Cloud Functions) handles distribution internally
- **Time-sensitive peer-to-peer** — Gaming, video conferencing may benefit from direct client-to-client connections

---

## Common Mistakes

### Beginner Mistakes

1. **Single load balancer with no redundancy** — If the single load balancer fails, the entire application goes down. Always run at least two instances across different availability zones.

2. **No health checks** — The load balancer sends traffic to failed servers, causing errors for users. Always configure health checks.

3. **Health check path that returns 200 even when the server is broken** — Using `GET /` instead of a real health check endpoint. The health check should validate that the application can actually process requests.

### Intermediate Mistakes

4. **Too-short or too-long health check intervals** — Checking every 1 second adds unnecessary load; checking every 60 seconds means traffic goes to dead servers for up to a minute. 5–10 seconds is typical.

5. **Misconfigured timeouts** — If your application takes 30 seconds to handle a request, but the load balancer timeout is 15 seconds, requests are killed prematurely. Match timeouts to your application's latency.

6. **Not using connection draining** — When a server is removed from the pool (during deployment or scaling), in-flight requests get dropped. Connection draining allows requests to complete gracefully.

### Senior-Level Architectural Mistakes

7. **Designing stateful applications that require sticky sessions** — Sticky sessions reduce the effectiveness of load balancing and complicate server management. Design stateless applications where possible, storing session data in a distributed cache (Redis) instead.

8. **Not planning for load balancer failure** — The load balancer itself can be overwhelmed by traffic spikes or DDOS attacks. Use DNS-based failover to a backup load balancer in another region.

9. **Using Layer 7 when Layer 4 is sufficient** — Layer 7 load balancing is powerful but adds unnecessary overhead if you only need TCP-level distribution. For high-throughput, low-latency applications (gaming, streaming), prefer Layer 4.

10. **Ignoring the "thundering herd" effect** — When many servers restart simultaneously (after a deployment), they all send health check "OK" at the same time, overwhelming the load balancer. Add jitter to health check timings.

---

## Failure Scenarios

### Scenario 1: Sudden Traffic Spike

**What happens:** A product goes viral. Traffic to a single backend pool increases 50x in 5 minutes.

**Why it fails:** The load balancer correctly distributes traffic, but all backend servers become overloaded. Each server handles fewer requests but requests keep coming. Response times go from 100ms to 10 seconds. Users experience timeouts.

**How to diagnose:**
- Monitor: All servers in the pool show high CPU and latency
- Load balancer metrics: `TargetResponseTime` spikes, `HealthyHostCount` drops (servers failing health checks due to overload)
- Error rates increase: 502, 503 responses

**Solutions:**
- **Auto-scaling:** Automatically add servers when CPU or request count exceeds thresholds
- **Rate limiting:** Configure the load balancer to return 429 (Too Many Requests) to protect backend servers
- **Queuing:** Decouple requests from processing with a queue (SQS, RabbitMQ)
- **Pre-warming:** Before known traffic events (Black Friday, product launch), pre-scale the fleet

### Scenario 2: Cascading Failure

**What happens:** One backend server becomes slightly slow (maybe due to a memory leak). The load balancer, using least-connections, sends more traffic to the faster servers. But the slow server's health check still passes.

Over time, the fast servers become overwhelmed because they're handling more traffic. They become slow too. Now all servers are slow.

**Why it fails:** The load balancer's algorithm (least-connections) actually made things worse by concentrating load on the healthiest servers.

**Solutions:**
- **Least outstanding requests with slow start** — Gradually increase traffic to new or recovering servers
- **Circuit breakers** — If a server is slower than a threshold, temporarily remove it from the pool
- **Request timeouts** — Cap how long a request can take; abort slow requests
- **Bulkhead pattern** — Limit the number of concurrent connections to any single server

### Scenario 3: DNS GSLB Failure

**What happens:** A DNS-based global load balancer routes users to a region that is actually experiencing an outage. Users can't reach the application.

**Why it fails:** DNS responses are cached. Even if the GSLB system detects the outage and changes the DNS response, cached entries may persist for minutes or hours (depending on TTL).

**Solutions:**
- **Short TTLs:** Set DNS TTL to 30–60 seconds for GSLB records
- **Health check integration:** Only return IPs for healthy regions
- **Anycast routing:** Use Anycast instead of (or in addition to) DNS — traffic automatically routes to healthy data centers
- **Client retry:** Configure applications to retry with a different IP if the first one fails

---

## Security Considerations

### DDoS Protection

The load balancer is the first line of defense against DDoS attacks:

- **Rate limiting:** Limit requests per second per client IP at the load balancer level
- **Connection limiting:** Limit concurrent connections from a single IP
- **TCP resets:** Aggressively drop malicious connections at Layer 4
- **Web Application Firewall (WAF):** For Layer 7, inspect requests for SQL injection, XSS, and other attack patterns

### SSL/TLS Termination at the Load Balancer

Terminating TLS at the load balancer offers security benefits:
- Centralized certificate management (one place to install/renew certificates)
- Backend servers communicate over a private network (potentially unencrypted)
- Reduced CPU load on application servers

**Key considerations:**
- Use strong TLS versions (TLS 1.3 preferred)
- Use short-lived certificates with automated renewal (Let's Encrypt, ACM)
- On internal networks, consider mutual TLS (mTLS) between load balancer and backend

### Backend Server Exposure

**Never make backend servers directly accessible from the internet.** Only the load balancer should be publicly accessible. Backend servers should be in a private subnet with security groups that only accept traffic from the load balancer.

### IP Spoofing Prevention

Set the `X-Forwarded-For` header at the load balancer to preserve the original client IP. Configure backend servers to trust this header *only* when the request comes from the load balancer (not from the internet).

---

## Performance Considerations

### Bottlenecks

| Bottleneck | Why It Happens | How to Fix |
|------------|---------------|------------|
| **Connection table size** | Load balancer tracks every active connection in memory | Use a load balancer with larger capacity; distribute across more LBs |
| **SSL/TLS handshake** | Every new connection requires expensive asymmetric crypto | Use session resumption; keep connections alive; offload to dedicated hardware |
| **Health check overhead** | Too many health checks overwhelm backend servers | Increase interval; use passive health checks for non-critical paths |
| **Logging throughput** | Every request logged to disk creates I/O bottlenecks | Stream logs to a separate system (CloudWatch, ELK) |
| **Configuration reload** | Changing config requires reloading all backend state | Use dynamic configuration (API-driven, not file-based) |

### Optimization Strategies

1. **Connection pooling:** The load balancer maintains persistent connections to backend servers, avoiding TCP handshake overhead for every request.

2. **HTTP/2 multiplexing:** Single connection from client to load balancer carries multiple concurrent requests, reducing connection overhead.

3. **Keepalive timeouts:** Configure appropriate keepalive values so connections are reused but idle connections are eventually closed.

4. **Linux kernel tuning:** For self-managed load balancers, tune `net.core.somaxconn`, `net.ipv4.tcp_tw_reuse`, and file descriptor limits.

5. **Use DPDK for extreme performance:** For L4 load balancing at 100+ Gbps, use DPDK (Data Plane Development Kit) to bypass the kernel's network stack.

### Scaling Challenges

- **Stateful load balancers** (those maintaining session tables) become a bottleneck. Stateless designs scale better.
- **Global traffic routing** is complex — DNS caching, latency measurement, and health checking across regions all add complexity.
- **TLS everywhere** is increasingly common but computationally expensive. Use hardware acceleration or dedicated TLS proxies.

---

## Real-World Industry Examples

### Amazon Web Services — Elastic Load Balancing (ELB)

AWS offers three types of load balancers:

| Type | Layer | Best For |
|------|-------|----------|
| **ALB (Application LB)** | Layer 7 | HTTP/HTTPS applications, microservices |
| **NLB (Network LB)** | Layer 4 | TCP/UDP, ultra-low latency, static IPs |
| **CLB (Classic LB)** | Legacy | Older applications (being deprecated) |

**ALB features:**
- **Content-based routing:** Route based on URL path, host header, query string parameters, HTTP method
- **Weighted target groups:** Send 90% traffic to v1, 10% to v2 (canary deployments)
- **Sticky sessions:** Cookie-based session persistence
- **AWS WAF integration:** Web Application Firewall for Layer 7 attacks
- **Auto-scaling integration:** Automatically register/deregister EC2 instances, Lambda functions, ECS tasks, and IP targets

**How ALB routes a request:**
```
1. Client connects to ALB's DNS name (CNAME)
2. ALB listener on port 443 terminates TLS
3. Rule evaluation:
   IF path starts with /api AND header X-Version = v2
   THEN forward to target-group "api-v2"
   ELSE forward to target-group "api-v1"
4. Within target group, use "least outstanding requests" algorithm
5. Forward to selected EC2 instance on port 8080
```

### Google — Maglev and Google Front End (GFE)

Google operates some of the world's largest load balancers, handling billions of requests per second across its services.

**Maglev (Software L4 Load Balancer):**
- A distributed, software-defined load balancer running on commodity servers
- Uses **consistent hashing** based on the 5-tuple (source/dest IP, source/dest port, protocol)
- This ensures that all packets from the same connection go to the same backend, even as Maglev servers are added or removed
- 10 Gbps per Maglev instance, scaled horizontally to handle Google's global traffic

**Google Front End (GFE):**
- Terminates TLS globally across hundreds of points of presence
- Routes to the nearest healthy backend
- Performs global load balancing using Google's private network backbone
- Integrates with Google Cloud Armor for DDoS protection

**Key insight:** Google separates L4 load balancing (Maglev) from L7 load balancing (GFE), allowing each to scale independently.

### Meta (Facebook) — Multi-Tiered Load Balancing

Meta's load balancing architecture is designed for global scale:

- **Layer 0 (DNS/Anycast):** Edge routers use BGP to advertise Anycast IPs. Users connect to the nearest Point of Presence.
- **Layer 1 (L4 Load Balancer):** A Maglev-like software load balancer distributes TCP connections across front-end proxies.
- **Layer 2 (L7 Proxy — Proxygen):** A custom HTTP proxy that routes requests to application servers based on URL, cookies, and headers.
- **Layer 3 (Service Mesh):** Internal load balancing between microservices using consistent hashing.

**Key insight:** Meta uses **consistent hashing** at every layer to minimize disruption when servers are added or removed. A single Facebook photo request may pass through 4–5 load balancing layers before reaching the storage layer.

### LinkedIn — Global Traffic Management (GTM)

LinkedIn's architecture routes traffic across multiple data centers:

- **DNS-based GSLB:** Route 53 and internal DNS systems steer users to the nearest healthy data center
- **Local load balancing:** NGINX instances in each data center balance traffic across application servers
- **Capacity-based routing:** If a data center is at 80% capacity, GTM shifts traffic to other data centers
- **Health monitoring:** Every data center continuously reports health metrics to the GTM system

### Netflix — Multi-Region Failover

Netflix uses load balancing to support cross-region failover:

- **DNS-based routing:** Route 53 routes users to the nearest healthy region
- **Regional load balancers:** Each region has ALBs distributing traffic within the region
- **Auto-scaling:** EC2 auto-scaling groups add/remove instances based on demand
- **Chaos testing:** Chaos Monkey randomly kills instances; load balancers naturally route around them
- **Region failover testing:** Chaos Kong simulates a full region failure to verify that the load balancing infrastructure correctly reroutes all traffic

---

## Case Studies

### Case Study 1: Amazon's Load Balancer Choice During Prime Day

**The challenge:** Amazon Prime Day generates traffic spikes of 10x–20x normal volume. The load balancing infrastructure must handle this without alerting the primary database.

**The approach:**
- ALBs distribute traffic across thousands of EC2 instances
- Auto-scaling launches pre-warmed instances within seconds of traffic increase
- The load balancer's "connection draining" ensures graceful shutdown of instances
- Circuit breakers at the ALB level protect downstream services

**Key metric:** During Prime Day 2023, AWS reported that their load balancers handled trillions of requests with 99.99% availability.

**Lesson:** When you know a traffic spike is coming (Prime Day, Black Friday, product launch), pre-warm both the load balancer and backend capacity. Don't rely on auto-scaling alone — it can't react instantly.

### Case Study 2: GitHub's Zero-Downtime Deployments

**The challenge:** GitHub deploys changes hundreds of times per day. Each deployment must not interrupt user requests.

**The approach (rolling deployment with load balancer):**
1. A new version is deployed to one server at a time
2. The load balancer drains connections from that server (connection draining)
3. The server is taken offline for 30 seconds while the new code deploys
4. Health checks verify the new version is healthy
5. The server is re-registered with the load balancer, which gradually increases traffic (slow start)

```
Server A: Draining → Offline → Deploying → Health Check → Online (slow start)
Server B: Active → Draining → Offline → Deploying → Health Check → Online
Server C: Active → Active → Draining → Offline → Deploying → Health Check
```

**Lesson:** Load balancer connection draining and slow start are essential for zero-downtime deployments. Without these, users would see connection errors during the transition.

### Case Study 3: The Thundering Herd at a Social Network

**The problem:** A major social network's caching layer failed simultaneously across all nodes. When it came back up, millions of users refreshed their feeds simultaneously, creating a "thundering herd" that overwhelmed the load balancers and database.

**The cascade:**
1. Cache cluster fails → all requests go directly to database → database becomes overloaded
2. Database health checks fail → load balancer marks database servers as unhealthy
3. All requests return errors → users refresh frantically
4. Cache cluster recovers → all users' requests hit the cache simultaneously
5. Cache was cold (empty) → all requests still hit the database
6. Database remains overloaded → recovery fails

**Solutions implemented:**
- **Rate limiting at the load balancer:** Cap requests per second per user
- **Graceful degradation:** Load balancer returns stale cached content (if available) instead of errors
- **Cache warming:** After a cache failure, gradually reintroduce traffic rather than accepting all at once
- **Jittered retry:** Client retry logic includes random delays to avoid synchronized retry spikes

---

## Practical Code Examples

### NGINX: Layer 7 Load Balancing with Health Checks

```nginx
upstream api_servers {
    least_conn;                       # algorithm: least connections
    server 10.0.1.10:8080 weight=5;
    server 10.0.1.11:8080 weight=3;
    server 10.0.1.12:8080 weight=1 max_fails=3 fail_timeout=30s;
}

server {
    listen 443 ssl;
    server_name api.example.com;

    location /api/ {
        proxy_pass http://api_servers;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 5s;
        proxy_read_timeout 30s;
    }

    location /images/ {
        proxy_pass http://static_assets;   # separate pool, content-based routing
    }
}
```

### HAProxy: Layer 4 TCP Load Balancing

```
frontend tcp_front
    bind *:443
    mode tcp
    default_backend tcp_back

backend tcp_back
    mode tcp
    balance leastconn
    option tcp-check
    server web1 10.0.1.10:443 check inter 10s fall 3 rise 2
    server web2 10.0.1.11:443 check inter 10s fall 3 rise 2
```

### AWS ALB Target Group with Health Checks (Terraform)

```hcl
resource "aws_lb_target_group" "api" {
  name     = "api-servers"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    interval            = 10
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }

  deregistration_delay = 30   # connection draining, in seconds
}
```

### Client-Side Consistent Hashing (Python)

Useful for routing requests to cache shards without needing a central load balancer — the same idea Google's Maglev and Meta's service mesh use internally.

```python
import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, nodes, replicas=100):
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []
        for node in nodes:
            self.add_node(node)

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node):
        for i in range(self.replicas):
            h = self._hash(f"{node}:{i}")
            self.ring[h] = node
            bisect.insort(self.sorted_keys, h)

    def get_node(self, key):
        h = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, h) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]

ring = ConsistentHashRing(["cache-a", "cache-b", "cache-c"])
print(ring.get_node("user:12345"))  # always routes this key to the same node
```

---

## Frequently Asked Questions

**Q: What is the difference between a reverse proxy and a load balancer?**

A reverse proxy accepts requests from clients and forwards them to a single server (or one of many). A load balancer is essentially a reverse proxy that distributes requests across multiple servers. All load balancers are reverse proxies, but not all reverse proxies are load balancers (some only have one backend).

**Q: Should I use a hardware or software load balancer?**

Hardware load balancers (F5, Citrix NetScaler) offer dedicated performance and advanced features but are expensive ($5,000–$100,000+). Software load balancers (HAProxy, NGINX, Envoy) run on commodity hardware, cost much less, and can scale horizontally. For most modern applications, software load balancers are the better choice. Use hardware only when you need specific compliance certifications or extreme throughput with minimal latency.

**Q: How do I choose a load balancing algorithm?**

- **Round-robin:** Good choice for servers with similar capacity and simple applications
- **Least connections:** Better for applications with varying request durations (API servers)
- **IP hash / consistent hashing:** Use when session persistence is needed or for caching layers
- **Weighted algorithms:** Use when servers have different capacities (e.g., during a rollout with mixed instance types)

**Q: What happens if a load balancer itself fails?**

The load balancer is a single point of failure. Production deployments use:
- **Active-passive:** A secondary load balancer monitors the primary and takes over on failure
- **Active-active:** Multiple load balancers share traffic (using DNS round-robin or Anycast)
- **Cloud-managed:** AWS ALB, Google Cloud LB are managed services with built-in redundancy

**Q: Can I use a load balancer for UDP traffic?**

Yes, but not all load balancers support UDP. Layer 4 load balancers (HAProxy TCP mode, AWS NLB, Google Cloud ILB) handle UDP. Layer 7 load balancers (NGINX, AWS ALB) are HTTP-only and do not support UDP.

---

## Interview Questions

### Beginner Questions

**Q1: What is a load balancer and why is it needed?**

A load balancer is a reverse proxy that distributes incoming network traffic across multiple backend servers. It's needed because a single server has limited capacity — a load balancer allows an application to scale horizontally (add more servers) and provides high availability by routing around failed servers.

**Q2: What's the difference between Layer 4 and Layer 7 load balancing?**

Layer 4 load balancing operates at the transport layer (TCP/UDP), making routing decisions based on IP addresses and ports without inspecting the content. It's fast but basic. Layer 7 load balancing operates at the application layer (HTTP/HTTPS), allowing routing decisions based on URLs, headers, cookies, and request bodies. It's more flexible but has slightly higher overhead.

**Q3: What is a health check and why is it important?**

A health check is an automated probe the load balancer sends to backend servers to verify they're healthy. It's important because without it, the load balancer would continue sending traffic to failed servers, causing errors for users. Health checks allow the load balancer to automatically remove unhealthy servers from the pool.

### Intermediate Questions

**Q4: Explain round-robin, least connections, and consistent hashing algorithms.**

- **Round-robin:** Requests are distributed sequentially (A, B, C, A, B, C...). Simple and works well when servers have similar capacity and requests require similar processing time.
- **Least connections:** Requests are sent to the server with the fewest active connections. Adapts to varying request durations — servers handling slow requests receive fewer new connections.
- **Consistent hashing:** Each request is assigned to a server using a hash of some identifier (IP, URL, user ID). When servers are added or removed, only a minimal fraction of assignments change — critical for caching layers where reassignment causes cache misses.

**Q5: How does session persistence (sticky sessions) work and when should you use it?**

Session persistence ensures all requests from a client go to the same backend server. It's typically implemented via cookies: the load balancer sets a cookie containing the server identifier, and subsequent requests from that client include the cookie, allowing the load balancer to route directly to the correct server. Use it when the application stores session state locally (e.g., in-memory session data). For modern applications, it's better to store session state externally (Redis, database) so that any server can handle any request.

**Q6: What is connection draining and why is it important?**

Connection draining (also called "deregistration delay") is the period during which a load balancer stops sending new connections to a server being taken offline but continues to serve existing connections until they complete. It's essential for zero-downtime deployments — without it, terminating a server would drop in-flight requests, causing errors for users.

### Senior Questions

**Q7: Design a global load balancing strategy for a multi-region e-commerce platform.**

A senior answer should cover:
- **DNS-based GSLB (Route 53):** Route users to the nearest healthy region based on latency or geolocation
- **Anycast routing:** For ultra-low-latency routing alongside or instead of DNS
- **Regional load balancers:** ALB or NLB within each region, distributing across availability zones
- **Health-checked failover:** If a region becomes unhealthy, DNS stops returning that region's IP
- **Cross-region failover:** Secondary region can take over 100% of traffic if primary fails
- **Short TTLs (60s):** For DNS records to enable fast failover
- **Capacity-based routing:** Stop routing to regions approaching capacity limits

**Q8: You're seeing 5xx errors from your load balancer during high traffic. How do you debug?**

1. Check load balancer metrics: Backend latency, healthy host count, error rate by target group
2. Isolate the error: 502 (bad gateway from backend) vs 503 (service unavailable) vs 504 (gateway timeout)?
3. Check backend server health: Are servers healthy? Are they running out of memory/CPU?
4. Check health checks: Are servers failing health checks? Is the health check path correct?
5. Check connection draining: Are old servers still registered? Are connections timing out?
6. Check auto-scaling: Are enough servers launched to handle the traffic?
7. Check the load balancer itself: Is it reaching connection limits? Is it healthy?

### Architecture Questions

**Q9: Design a load balancing strategy for a real-time messaging application (WhatsApp-like).**

A strong answer covers:
- **Layer 4 (TCP):** Use NLB or HAProxy for maintaining persistent TCP connections
- **Consistent hashing:** Map each user to a specific server to maintain connection affinity
- **WebSocket support:** Load balancer must support WebSocket upgrades and long-lived connections
- **Session persistence:** Required because WebSocket connections are stateful
- **Connection draining:** Carefully handle when a server goes down — gracefully migrate WebSocket connections
- **Back-pressure:** If a server is overloaded, the load balancer should detect and redirect new connections

**Q10: How would you load balance a system where a single user request triggers multiple microservice calls?**

1. **External load balancer:** (ALB/NGINX) routes the initial request to the API gateway
2. **Service mesh (Envoy/Istio):** Each microservice instance has a sidecar proxy that handles internal load balancing
3. **Client-side load balancing:** Each microservice discovers and load-balances calls to downstream services
4. **Circuit breakers:** If a downstream service is failing, the load balancer circuit-breaks to prevent cascading failures
5. **Retry with backoff:** Transient failures are retried (but careful: don't amplify load with excessive retries)
6. **Distributed tracing:** Every request through every microservice is traceable for debugging

---

## In the AI Era

Load balancing LLM traffic is hard because **request cost varies by orders of magnitude.** A one-line classification and a 100-page document summary are both "one request." Round-robin can pile several giant requests onto one server while others sit idle.

Techniques that work better for inference:

- **Least outstanding work:** route by queued tokens or in-flight requests, not connection count.
- **Cache-aware (prefix-aware) routing:** send requests that share a long prompt prefix to the same replica, so its cached computation can be reused. This is a deliberate trade of perfect balance for higher cache hit rates — the same sticky-session tradeoff described in this chapter.
- **Separate pools by workload:** interactive chat (latency-sensitive) and batch jobs (throughput-sensitive) should not compete in the same queue.

**AI gateways** extend load balancing across *providers and models*: routing between providers for availability, falling back when one returns errors or rate limits, and sending easy requests to smaller, cheaper models while reserving large models for hard ones.

**Try it:** Two replicas each receive 10 requests. On one, all ten are short; on the other, one is a 50,000-token document. Walk through what round-robin and least-outstanding-tokens routing would do with the next request.

---

## Key Takeaways

1. **Load balancing is essential for any application running on more than one server.** It distributes traffic, provides failover, and enables horizontal scaling.

2. **The two main types are Layer 4 and Layer 7.** L4 is faster, L7 is smarter. Choose based on your needs.

3. **Algorithms matter.** Round-robin is simple and effective for uniform workloads. Least connections adapts to varying request durations. Consistent hashing is essential for caching layers.

4. **Health checks are not optional.** Always configure them. A load balancer that sends traffic to dead servers is worse than no load balancer at all.

5. **Design for statelessness.** Sticky sessions limit the benefits of load balancing. Store session state externally where any server can access it.

6. **The load balancer is itself a single point of failure.** Always run multiple instances across different availability zones.

7. **Auto-scaling + load balancing is the standard production pattern.** The load balancer dynamically registers new instances as auto-scaling launches them.

8. **Global Server Load Balancing (GSLB) uses DNS and Anycast.** DNS-based routing directs users to the nearest region; Anycast provides sub-second failover.

9. **Load balancers are critical for security.** They provide rate limiting, SSL termination, DDoS protection, and hide backend infrastructure.

10. **Connection draining enables zero-downtime deployments.** Always configure it before implementing rolling updates.

---

## Further Reading

### Foundational Papers

- **"Maglev: A Fast and Reliable Software Network Load Balancer" (2015)** — Google's Maglev paper: [https://research.google/pubs/maglev-a-fast-and-reliable-software-network-load-balancer/](https://research.google/pubs/maglev-a-fast-and-reliable-software-network-load-balancer/)
- **"Unimog: Cloudflare's L4 Load Balancer" (2021)** — How Cloudflare handles 10+ Tbps at the network edge
- **"The Evolution of Load Balancing at Facebook"** — Meta's multi-tiered load balancing architecture
- **"Consistent Hashing and Random Trees" (1997)** — Karger, Lehman, Leighton et al., the original STOC paper introducing consistent hashing: [https://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/chash.pdf](https://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/chash.pdf)
- **"Maglev" companion — Google's Global Software-Defined Load Balancing (2016 SREcon talk)**: Describes how Google Front End (GFE) and Maglev work together for global traffic management: [https://research.google/pubs/](https://research.google/pubs/)

### Academic Resources

- **MIT 6.033 — Computer Systems Engineering**: Lectures on network architecture and load balancing
- **Stanford CS 244B — Distributed Systems**: Covers consistent hashing and load distribution techniques
- **Cornell CS 5414 — Distributed Computing**: Consensus and consistent hashing in distributed systems

### Industry Engineering Blogs

- **AWS Elastic Load Balancing Documentation**: [https://docs.aws.amazon.com/elasticloadbalancing/](https://docs.aws.amazon.com/elasticloadbalancing/)
- **HAProxy Documentation and Blog**: [https://www.haproxy.com/blog/](https://www.haproxy.com/blog/)
- **NGINX Load Balancing Guide**: [https://docs.nginx.com/nginx/admin-guide/load-balancer/](https://docs.nginx.com/nginx/admin-guide/load-balancer/)
- **Cloudflare Load Balancing**: [https://www.cloudflare.com/load-balancing/](https://www.cloudflare.com/load-balancing/)
- **Envoy Proxy Documentation — Load Balancing**: [https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/load_balancing/load_balancers](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/load_balancing/load_balancers)

### Tools

- **HAProxy** — High-performance TCP/HTTP load balancer
- **NGINX** — Web server, reverse proxy, and load balancer
- **Envoy Proxy** — High-performance sidecar proxy for service meshes
- **Traefik** — Cloud-native edge router and load balancer

### Books

- **"NGINX Cookbook" by Derek DeJonghe** — Practical load balancing recipes
- **"The HAProxy Book" by Willy Tarreau** — Comprehensive HAProxy guide
- **"Designing Distributed Systems" by Brendan Burns** — Patterns for scalable systems including load balancing
- **"Site Reliability Engineering" by Google/Beyer, Jones, Petoff, Murphy** — Chapters on load balancing at Google

---

*This chapter is part of the Software Engineering Handbook — a comprehensive guide to the concepts, principles, and practices that every professional software engineer should know.*
