from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.client import Users
from diagrams.oci.network import Vcn
from diagrams.onprem.ci import GithubActions
from diagrams.oci.compute import Container
from diagrams.onprem.container import Docker


with (Diagram("Infrastructure", show=False, filename="infrastructure")):
    # External user access
    user = Users("User")

    with Cluster("CI/CD"):
        github = Custom("push/merge on main", "./resources/git.png")
        build_docker = GithubActions("Build Docker Image")
        docker_hub = Docker("Docker Hub")

        github >> Edge(color="blue", label="Teiffer Build") >> build_docker
        build_docker >> Edge(color="blue", label="Push Image") >> docker_hub

    # Cloudflare Load Balancer & CDN
    with Cluster("Cloudflare"):
        cloudflare_lb = Custom("Cloudflare Load Balancer", "./resources/cloudflare.png")
        cdn = Custom("Cloudflare CDN", "./resources/cloudflare.png")

    # All Instances inside the VCN (Private Network)
    with Cluster("OCI VCN (Private Network)"):
        vcn = Vcn("OCI VCN")

        oci_compute_1 = Container("OCI EC2 Compute 1")
        oci_compute_2 = Container("OCI EC2 Compute 2")
        oci_compute_db = Container("OCI EC2 MongoDB")

    # Connections between services
    user >> Edge(label="HTTPS", color="black") >> cloudflare_lb
    user >> Edge(label="HTTPS", color="black") >> cdn
    cloudflare_lb >> Edge(label="Load balancing", color="black") >> [oci_compute_1, oci_compute_2]
    cdn << Edge(label="Content Caching", color="black") << oci_compute_1

    # MongoDB network connection
    oci_compute_1 >> Edge(color="red") << vcn
    oci_compute_2 >> Edge(color="red") << vcn
    vcn >> Edge(color="red") << oci_compute_db

    oci_compute_1 >> Edge(color="blue", label="Pull Image") >> docker_hub
    oci_compute_2 >> Edge(color="blue", label="Pull Image") >> docker_hub
