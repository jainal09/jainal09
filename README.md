<h1 align="center">Jainal Gosaliya</h1>

<p align="center"> <img src="https://komarev.com/ghpvc/?username=jainal09&label=Profile%20views&color=0e75b6&style=flat" alt="jainal09" /> </p>

<a href="#gh-dark-mode-only">
  <picture>
    <source media="(max-width: 600px) and (hover: none)" srcset="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/banner-mobile.dark.svg">
    <img src="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/banner.dark.svg" alt="jainal09 — software engineer, distributed systems" width="100%" />
  </picture>
</a>
<a href="#gh-light-mode-only">
  <picture>
    <source media="(max-width: 600px) and (hover: none)" srcset="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/banner-mobile.light.svg">
    <img src="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/banner.light.svg" alt="jainal09 — software engineer, distributed systems" width="100%" />
  </picture>
</a>


I design and build distributed systems that stay dependable when the load stops cooperating — event-driven backends, high-throughput services, and the brokers underneath them. My current work goes deep on Kubernetes, Spring Cloud, and reactive programming. I hold an MS in Software Engineering from [Northeastern University, Boston](https://www.northeastern.edu/graduate/program/master-of-science-in-software-engineering-systems-18774/).

<a href="#gh-dark-mode-only">
  <picture>
    <source media="(max-width: 600px) and (hover: none)" srcset="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/stack-mobile.dark.svg">
    <img src="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/stack.dark.svg" alt="a request descending the layers I work in" width="100%" />
  </picture>
</a>
<a href="#gh-light-mode-only">
  <picture>
    <source media="(max-width: 600px) and (hover: none)" srcset="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/stack-mobile.light.svg">
    <img src="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/stack.light.svg" alt="a request descending the layers I work in" width="100%" />
  </picture>
</a>

That is the slice I get asked about most, not the whole of it — a large private Swift codebase and a pile of C++ do not fit in five bands. I write about how the pieces fit together on [Scale Bites](https://scalebites.substack.com/) — also on [Medium](https://medium.com/@jainal) and [LinkedIn](https://www.linkedin.com/build-relation/newsletter-follow?entityUrn=7169831353377619968).

⚡ I chase race conditions for fun. Yes, I need better hobbies.

&nbsp;

## Contributions

### Commit Frequency

<a href="#gh-dark-mode-only">
  <picture>
    <source media="(max-width: 600px) and (hover: none)" srcset="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/contributions-mobile.dark.svg">
    <img src="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/contributions.dark.svg" alt="contribution graph" width="100%" />
  </picture>
</a>
<a href="#gh-light-mode-only">
  <picture>
    <source media="(max-width: 600px) and (hover: none)" srcset="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/contributions-mobile.light.svg">
    <img src="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/contributions.light.svg" alt="contribution graph" width="100%" />
  </picture>
</a>

### Opensource Projects Contributed

<a href="#gh-dark-mode-only">
  <picture>
    <source media="(max-width: 600px) and (hover: none)" srcset="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/cluster-mobile.dark.svg">
    <img src="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/cluster.dark.svg" alt="message flow through a NATS cluster" width="100%" />
  </picture>
</a>
<a href="#gh-light-mode-only">
  <picture>
    <source media="(max-width: 600px) and (hover: none)" srcset="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/cluster-mobile.light.svg">
    <img src="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/cluster.light.svg" alt="message flow through a NATS cluster" width="100%" />
  </picture>
</a>

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

Benchmarking NATS against Kafka through a tool I made - [knack](https://github.com/jainal09/knack) turned up three defects that belonged to NATS rather than to my benchmark — a startup notice that contradicted the server's own TLS configuration, a cache that mangled fully-qualified protobuf type names, and no way to cap send rate in the bench tooling. All three merged; two shipped in **nats-server 2.14.4** and **nui 0.9.3**.

&nbsp;

## Featured Projects

<p align="center">
  <a href="https://github.com/jainal09/envdrift">envdrift</a> ·
  <a href="https://github.com/jainal09/knack">knack</a> ·
  <a href="https://github.com/jainal09/drill">drill</a> ·
  <a href="https://github.com/jainal09/pyro-bot">Pyro</a>
</p>

<a href="#gh-dark-mode-only">
  <picture>
    <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/projects-mobile.dark.svg">
    <img src="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/projects.dark.svg" alt="Featured projects: envdrift, knack, drill, and Pyro" width="100%" />
  </picture>
</a>
<a href="#gh-light-mode-only">
  <picture>
    <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/projects-mobile.light.svg">
    <img src="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/projects.light.svg" alt="Featured projects: envdrift, knack, drill, and Pyro" width="100%" />
  </picture>
</a>

&nbsp;

## Listening

<a href="#gh-dark-mode-only">
  <picture>
    <source media="(max-width: 600px) and (hover: none)" srcset="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/music-mobile.dark.svg">
    <img src="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/music.dark.svg" alt="what I am listening to" width="100%" />
  </picture>
</a>
<a href="#gh-light-mode-only">
  <picture>
    <source media="(max-width: 600px) and (hover: none)" srcset="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/music-mobile.light.svg">
    <img src="https://raw.githubusercontent.com/jainal09/jainal09/main/assets/music.light.svg" alt="what I am listening to" width="100%" />
  </picture>
</a>


## Connect

[![Substack](https://img.shields.io/badge/Scale_Bites-FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://scalebites.substack.com/) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jainal09) [![X](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/SysSniper) [![Medium](https://img.shields.io/badge/Medium-000000?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@jainal) [![Dev.to](https://img.shields.io/badge/Dev.to-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white)](https://dev.to/jainal09) [![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-F58025?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/10401497/jainal-gosaliya) [![ORCID](https://img.shields.io/badge/ORCID-A6CE39?style=for-the-badge&logo=orcid&logoColor=white)](https://orcid.org/0000-0002-6328-8836)

&nbsp;

## Languages and Tools

<p align="left">
  <a href="https://skillicons.dev">
    <picture>
      <source media="(max-width: 600px)" srcset="https://skillicons.dev/icons?i=python%2Cjava%2Cgo%2Crust%2Cc%2Ccpp%2Ccs%2Cjs%2Cts%2Chtml%2Ccss%2Cdjango%2Cfastapi%2Cflask%2Cspring%2Creact%2Cnextjs%2Cvue%2Cnodejs%2Cexpress%2Cdotnet%2Cgraphql%2Ckafka&amp;perline=7">
      <img src="https://skillicons.dev/icons?i=python,java,go,rust,c,cpp,cs,js,ts,html,css,django,fastapi,flask,spring,react,nextjs,vue,nodejs,express,dotnet,graphql,kafka&amp;perline=15" alt="Languages and application frameworks" />
    </picture>
  </a>
</p>

<p align="left">
  <a href="https://skillicons.dev">
    <picture>
      <source media="(max-width: 600px)" srcset="https://skillicons.dev/icons?i=rabbitmq%2Cdocker%2Ckubernetes%2Caws%2Cazure%2Cgcp%2Cnginx%2Cjenkins%2Cgrafana%2Celasticsearch%2Cpostgres%2Cmysql%2Cmongodb%2Credis%2Csqlite%2Cfirebase%2Cgit%2Clinux%2Cbash%2Cselenium%2Ctensorflow%2Cpytorch%2Copencv%2Cfigma%2Cpostman%2Carduino%2Cheroku&amp;perline=7">
      <img src="https://skillicons.dev/icons?i=rabbitmq,docker,kubernetes,aws,azure,gcp,nginx,jenkins,grafana,elasticsearch,postgres,mysql,mongodb,redis,sqlite,firebase,git,linux,bash,selenium,tensorflow,pytorch,opencv,figma,postman,arduino,heroku&amp;perline=15" alt="Infrastructure, data and tooling" />
    </picture>
  </a>
</p>
