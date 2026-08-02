<h1 align="center">Jainal Gosaliya</h1>

<p align="center">
  <a href="https://github.com/jainal09">
    <img src="https://readme-svg-typing-generator.vercel.app/api?lines=Software+Engineer;Distributed+Systems+%7C+Backend+%7C+Platform;Building+things+that+scale&animation=typing&color=36BCF7&size=22&center=true&vCenter=true&width=600&height=60&duration=4000&repeat=true" alt="Typing SVG" />
  </a>
</p>

<p align="center"> <img src="https://komarev.com/ghpvc/?username=jainal09&label=Profile%20views&color=0e75b6&style=flat" alt="jainal09" /> </p>

## About

MS in Software Engineering from [Northeastern University, Boston](https://www.northeastern.edu/graduate/program/master-of-science-in-software-engineering-systems-18774/). I work on the parts of a system that have to hold when the load stops cooperating — event-driven backends, high-throughput services, and the brokers underneath them. Currently deep in Kubernetes, Spring Cloud and reactive programming.

<img src="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/stack.svg" alt="a request descending the layers I work in" width="100%" />

That is the slice I get asked about most, not the whole of it — a large private Swift codebase and a pile of C++ do not fit in five bands. I write about how the pieces fit together on [Scale Bites](https://scalebites.substack.com/) — also on [Medium](https://medium.com/@jainal) and [LinkedIn](https://www.linkedin.com/build-relation/newsletter-follow?entityUrn=7169831353377619968).

⚡ I debug distributed systems for fun. Yes, I need better hobbies.

<img src="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/trophies.svg" alt="profile numbers" width="100%" />

---

## Featured Projects

<table><tr><td valign="top" width="50%">

### 🔐 [envdrift](https://github.com/jainal09/envdrift)
**Prevent environment variable drift across teams.**

Sync encrypted `.env` files using your existing cloud vault — no hosted service, no third-party trust, no more "it works on my machine."

**~3.9k downloads/month** · **96 releases in 8 months** · **94.7% coverage**

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

## Open Source

<img src="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/cluster.svg" alt="message flow through a NATS cluster" width="100%" />

I fix the tools I build on. Code I've written ships in NATS Server, NATS NUI and gRPC UI.

<p align="center">
  <a href="https://github.com/nats-io/nats-server/pull/8420"><img src="https://img.shields.io/badge/NATS_Server-27AAE1?style=for-the-badge&logo=natsdotio&logoColor=white" alt="NATS Server" /></a>
  <a href="https://github.com/nats-nui/nui/pull/126"><img src="https://img.shields.io/badge/NATS_NUI-27AAE1?style=for-the-badge&logo=natsdotio&logoColor=white" alt="NATS NUI" /></a>
  <a href="https://github.com/celery/celery/pull/5792"><img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white" alt="Celery" /></a>
  <a href="https://github.com/hoppscotch/hoppscotch/pull/1593"><img src="https://img.shields.io/badge/Hoppscotch-31C48D?style=for-the-badge&logo=hoppscotch&logoColor=white" alt="Hoppscotch" /></a>
  <a href="https://github.com/fullstorydev/grpcui/pull/398"><img src="https://img.shields.io/badge/gRPC_UI-2D3748?style=for-the-badge&logo=grpc&logoColor=white" alt="gRPC UI" /></a>
</p>

> **"preserve dots in cached message types and survive external cache clears. Thanks @jainal09 for the contribution!"**
> — [NATS NUI v0.9.3 release notes](https://github.com/nats-nui/nui/releases/tag/v0.9.3)

Benchmarking NATS against Kafka for [knack](https://github.com/jainal09/knack) turned up three defects that belonged to NATS rather than to my benchmark — a startup notice that contradicted the server's own TLS configuration, a cache that mangled fully-qualified protobuf type names, and no way to cap send rate in the bench tooling. All three merged; two shipped in **nats-server 2.14.4** and **nui 0.9.3**.

---

## Connect

[![Substack](https://img.shields.io/badge/Scale_Bites-FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://scalebites.substack.com/) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jainal09) [![X](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/SysSniper) [![Medium](https://img.shields.io/badge/Medium-000000?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@jainal) [![Dev.to](https://img.shields.io/badge/Dev.to-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white)](https://dev.to/jainal09) [![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-F58025?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/10401497/jainal-gosaliya) [![ORCID](https://img.shields.io/badge/ORCID-A6CE39?style=for-the-badge&logo=orcid&logoColor=white)](https://orcid.org/0000-0002-6328-8836)

---

## Languages and Tools

<p align="left"> <a href="https://skillicons.dev"> <img src="https://skillicons.dev/icons?i=python,java,go,rust,c,cpp,cs,js,ts,html,css,django,fastapi,flask,spring,react,nextjs,vue,nodejs,express,dotnet,graphql,kafka&perline=15" /> </a> </p>

<p align="left"> <a href="https://skillicons.dev"> <img src="https://skillicons.dev/icons?i=rabbitmq,docker,kubernetes,aws,azure,gcp,nginx,jenkins,grafana,elasticsearch,postgres,mysql,mongodb,redis,sqlite,firebase,git,linux,bash,selenium,tensorflow,pytorch,opencv,figma,postman,arduino,heroku&perline=15" /> </a> </p>
