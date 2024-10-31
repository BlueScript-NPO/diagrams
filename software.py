from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.network import Traefik
from diagrams.onprem.client import Client
from diagrams.onprem.storage import Portworx, Ceph
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.framework import FastAPI

with (Diagram("Architecture", show=False, filename="software")):
    # External browser access
    browser = Client("Browser")

    with Cluster("CloudFlare"):
        cache = Custom("Cache/CDN", "./resources/cloudflare.png")

    with Cluster("OCI VCN (Private Network)"):
        with Cluster("EC2 Instance"):
            with Cluster("Ubuntu 22.04"):
                with Cluster("Docker Compose"):
                    traefik = Traefik("Traefik Proxy")

                    with Cluster("UVicorn (ASGI Web Server)"):
                        with Cluster("Python 3.12"):
                            backend = FastAPI("FastAPI Backend")

                    with Cluster("Node.js 22.7.x"):
                        with Cluster("Nuxt.js"):
                            nuxtjs = Custom("SSR Engine", "./resources/nuxt.png")
                            nitro = Custom("Nitro Engine", "./resources/nitro.png")
                        mini_search = Ceph("MiniSearch")
                        asset = Portworx("Asset Storage")

                    nitro >> Edge(color="red") << asset
                    traefik >> Edge(label="API Request", color="black") >> backend
                    traefik >> Edge(label="Web Request", color="black") >> nuxtjs >> Edge(label="API Request", color="black") >> backend
                    nuxtjs >> Edge(label="Search Document", color="red") >> mini_search
                    mini_search << Edge(label="Index Document", color="red") << nitro
                    nuxtjs >> Edge(label="Request Document", color="red") >> nitro

        with Cluster("EC2 Instance (DB)"):
            with Cluster("Ubuntu 22.04"):
                postgres = PostgreSQL("PostgreSQL DB")

    nuxtjs >> Edge(label="", color="black") >> asset
    browser >> Edge(label="HTTPS", color="black") >> [traefik]
    browser >> Edge(label="HTTPS", color="black") >> cache
    backend >> Edge(label="DB Connection", color="blue") << postgres

    cache >> Edge(label="Cache Request/Update", color="orange") >> nuxtjs