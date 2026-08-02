<h1 align="center">Jainal Gosaliya</h1>

<p align="center">
  <a href="https://github.com/jainal09">
    <img src="https://readme-svg-typing-generator.vercel.app/api?lines=Software+Engineer;Distributed+Systems+%7C+Backend+%7C+Platform;Building+things+that+scale&animation=typing&color=36BCF7&size=22&center=true&vCenter=true&width=600&height=60&duration=4000&repeat=true" alt="Typing SVG" />
  </a>
</p>

<p align="center"> <img src="https://komarev.com/ghpvc/?username=jainal09&label=Profile%20views&color=0e75b6&style=flat" alt="jainal09" /> </p>

<p align="center"> <a href="https://github.com/ryo-ma/github-profile-trophy"><img src="https://github-trophies.vercel.app/?username=jainal09&column=6&margin-w=15&margin-h=15" alt="jainal09" /></a> </p>

## About

- 🔭 Building and scaling **distributed systems, event-driven architectures, and high-throughput backend services**
- 🎓 MS in Software Engineering from [Northeastern University, Boston](https://www.northeastern.edu/graduate/program/master-of-science-in-software-engineering-systems-18774/)
- 🛠 Currently deep in **Kubernetes, Spring Cloud, and Reactive Programming**
- 📝 I write about systems design and engineering on [Scale Bites](https://scalebites.substack.com/) — also on [Medium](https://medium.com/@jainal) and [LinkedIn](https://www.linkedin.com/build-relation/newsletter-follow?entityUrn=7169831353377619968)
- 💬 Happy to talk about **Kafka, distributed systems, microservices, Kubernetes, Spring Boot, Python, Django, FastAPI, Flask, Docker**
- ⚡ I debug distributed systems for fun. Yes, I need better hobbies.

---

## Featured Projects

<table><tr><td valign="top" width="50%">

### 🔐 [envdrift](https://github.com/jainal09/envdrift)
**Prevent environment variable drift across teams.**

Sync encrypted `.env` files using your existing cloud vault — no hosted service, no third-party trust, no more "it works on my machine."

[![PyPI](https://img.shields.io/pypi/v/envdrift?style=flat-square)](https://pypi.org/project/envdrift/) [![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue?style=flat-square)](https://www.python.org/downloads/) [![MIT](https://img.shields.io/badge/license-MIT-yellow?style=flat-square)](https://opensource.org/licenses/MIT) [![Docs](https://img.shields.io/badge/docs-mkdocs-blue?style=flat-square)](https://jainal09.github.io/envdrift)

`Pydantic` `pre-commit` `dotenvx` `Azure Key Vault` `AWS Secrets Manager`

</td><td valign="top" width="50%">

### ⚡ [knack](https://github.com/jainal09/knack)
**Kafka + NATS benchmark suite for constrained hardware.**

Production-grade benchmarking across 9 categories — generates 20+ charts, cross-scenario comparisons, and automated recommendations.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue?style=flat-square)](https://www.python.org/downloads/) [![Docker](https://img.shields.io/badge/docker-required-blue?style=flat-square)](https://www.docker.com/) [![MIT](https://img.shields.io/badge/license-MIT-yellow?style=flat-square)](https://opensource.org/licenses/MIT)

`Kafka` `NATS JetStream` `Docker` `Benchmarking` `Observability`

</td></tr></table>

---

## Connect

[![Substack](https://img.shields.io/badge/Scale_Bites-FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://scalebites.substack.com/) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jainal09) [![X](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/SysSniper) [![Medium](https://img.shields.io/badge/Medium-000000?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@jainal) [![Dev.to](https://img.shields.io/badge/Dev.to-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white)](https://dev.to/jainal09) [![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-F58025?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/10401497/jainal-gosaliya) [![ORCID](https://img.shields.io/badge/ORCID-A6CE39?style=for-the-badge&logo=orcid&logoColor=white)](https://orcid.org/0000-0002-6328-8836)

---

## Languages and Tools

<p align="left"> <a href="https://skillicons.dev"> <img src="https://skillicons.dev/icons?i=python,java,go,rust,c,cpp,cs,js,ts,html,css,django,fastapi,flask,spring,react,nextjs,vue,nodejs,express,dotnet,graphql,kafka&perline=15" /> </a> </p>

<p align="left"> <a href="https://skillicons.dev"> <img src="https://skillicons.dev/icons?i=rabbitmq,docker,kubernetes,aws,azure,gcp,nginx,jenkins,grafana,elasticsearch,postgres,mysql,mongodb,redis,sqlite,firebase,git,linux,bash,selenium,tensorflow,pytorch,opencv,figma,postman,arduino,heroku&perline=15" /> </a> </p>

---

## Upstream

I wrote [knack](https://github.com/jainal09/knack) to benchmark NATS against Kafka on constrained hardware. Some of what it surfaced turned out to be defects in NATS rather than in the benchmark, so that is where they were fixed.

- **[nats-server #8420](https://github.com/nats-io/nats-server/pull/8420)** — a server configured with `allow_non_tls` announced `TLS required for client connections` at startup while accepting plaintext on that same port. Shipped in 2.14.4 and 2.12.14.
- **[nui #126](https://github.com/nats-nui/nui/pull/126)** — identifier sanitization stripped the dots from fully-qualified protobuf type names, and a cache that overwrote external clears on unload left no way to recover from the bad state.
- **[natscli #1647](https://github.com/nats-io/natscli/pull/1647)** — `--throughput` for the generator-side `bench` commands, holding aggregate send rate at or below a target and dividing it across `--clients`. Merged to main, not yet in a release.

The one worth reading, though, is **[grpcui #398](https://github.com/fullstorydev/grpcui/pull/398)**. I opened it with a dark mode built on a toggle, JavaScript and cookie storage. The maintainer's response was that this was "a bit much" and that pure CSS would do. I pushed back once with a middle ground, they held their position, and they were right — what merged is a single CSS file, no JavaScript at all.

Older, elsewhere: [hoppscotch #1593](https://github.com/hoppscotch/hoppscotch/pull/1593), [celery #5792](https://github.com/celery/celery/pull/5792).

## Practice

[envdrift](https://github.com/jainal09/envdrift) is where I keep myself honest. Commit format isn't a convention I claim to follow there — commitlint is one of twelve required checks on `main`, with admin enforcement switched on, so a malformed message blocks the merge for me too. release-please then cuts versions straight from that history, which is the point: a careless message becomes a wrong changelog. Ninety-six versions on PyPI in eight months.

The rest is unglamorous on purpose. Integration tests run against real containers instead of mocks — an Azure Key Vault emulator, LocalStack, Vault — and they gate the merge rather than reporting into the void. Renovate carries eight custom managers that bump the pinned scanner binaries inside the source. CodeQL and bandit read the code, benchmarks are recorded per pull request, and every workflow holding `id-token: write` pins its actions to a commit SHA.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/jainal09/jainal09/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/jainal09/jainal09/output/github-snake.svg" />
  <img alt="snake eating contributions" src="https://raw.githubusercontent.com/jainal09/jainal09/output/github-snake.svg" />
</picture>
