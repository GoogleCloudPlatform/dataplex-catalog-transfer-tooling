This is not an officially supported Google product. This project is not
eligible for the [Google Open Source Software Vulnerability Rewards
Program](https://bughunters.google.com/open-source-security).

# Dataplex Catalog Transfer Tooling
# Introduction
In 2024 we released Google Cloud Platform Dataplex Catalog as a successor to the Data Catalog product. In relation to the announced [deprecation of Data Catalog](https://cloud.google.com/data-catalog/docs/release-notes#February_03_2025) our goal was to make sure everyone has an equal opportunity to transfer their data and integrations to the new platform.

To ease the transition process, we exposed a dedicated user interface page [“Manage transition to Dataplex”](https://cloud.google.com/dataplex/docs/transition-to-dataplex-catalog), which gave a graphical interface to the very basic operation related to the data transfer.

Although the user interface-based transition shall work for the smaller datasets, it will most likely not work for the largest ones. They might require performing the transition gradually and being aware of the consequences of each step throughout the process as the transfer process is not reversible.

To address this concern, we released a dedicated tooling that is encapsulated within this repository.

# Capabilities
## Data discovery
You can discover all projects (with either Data Catalog or Dataplex API enabled) and resources (tag templates & entry groups) that are subjected to transfer.

## Impact analysis
You can analyze the consequences of permanently transferring resources to the new system by investigating IAM policies applied at the resources level as well as understand which resources are being actively used by investigating access patterns.

You will also receive a mapping table showing the relation between Data Catalog and Dataplex Catalog resource names that you can use for comparison.

## Transfer at scale
You can convert from private to public tag templates and initiate transfer of all resources at scale.

# Setup
1) Create a new Google Cloud project inside your organization's account.
2) Create a Service Account in the project.
3) Grant the Service Account the following roles at the **organization level**:
   * roles/bigquery.dataEditor
   * roles/browser
   * roles/cloudasset.viewer
   * roles/cloudtasks.admin
   * roles/cloudtasks.enqueuer
   * roles/datacatalog.searchAdmin
   * roles/datacatalog.tagTemplateOwner
   * roles/datacatalog.entryGroupOwner
   * roles/serviceusage.serviceUsageConsumer
   * roles/dataplex.aspectTypeOwner
   * roles/dataplex.entryGroupOwner
   * roles/logging.configWriter
   * roles/iam.securityReviewer
   * roles/run.invoker
   * roles/bigquery.jobUser
   * roles/iam.serviceAccountUser
   * roles/cloudquotas.viewer
   * roles/bigquery.jobUser
4) Enable API:
   * Cloud Resource Manager API
   * BigQuery API
   * Cloud Tasks API
   * Cloud Run Admin API
   * Cloud Data Catalog API
   * Artifact Registry API
   * Cloud Asset API
   * Dataplex API
   * Data Catalog API
   * Cloud Quotas API
5) Create a Docker repository in Google Artifact Registry
6) [Opt in public tag templates and tags](https://cloud.google.com/dataplex/docs/transition-to-dataplex-catalog#opt-in) for simultaneous availability of metadata in universal catalog

# Build
1) Clone the GitHub repository
    ```
    git clone https://github.com/GoogleCloudPlatform/dataplex-catalog-transfer-tooling.git
    ```
2) Build docker images
    ```
    docker build -t <location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-resources-handler:latest -f ./services/handlers/fetch_resources/Dockerfile .
    docker build -t <location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-resources-job:latest -f ./services/jobs/fetch_resources/Dockerfile .
    docker build -t <location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-projects-handler:latest -f ./services/handlers/fetch_projects/Dockerfile .
    docker build -t <location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-projects-job:latest -f ./services/jobs/fetch_projects/Dockerfile .
    docker build -t <location>-docker.pkg.dev/<work_project_id>/<repo_id>/find-resource-names-handler:latest -f ./services/handlers/find_resource_names/Dockerfile .
    docker build -t <location>-docker.pkg.dev/<work_project_id>/<repo_id>/find-resource-names-job:latest -f ./services/jobs/find_resource_names/Dockerfile .
    docker build -t <location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-policies-handler:latest -f ./services/handlers/fetch_policies/Dockerfile .
    docker build -t <location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-policies-job:latest -f ./services/jobs/fetch_policies/Dockerfile .
    docker build -t <location>-docker.pkg.dev/<work_project_id>/<repo_id>/audit-logs-job:latest -f ./services/jobs/audit_logs/Dockerfile .
    docker build -t <location>-docker.pkg.dev/<work_project_id>/<repo_id>/analytics-job:latest -f ./services/jobs/analytics/Dockerfile .
    docker build -t <location>-docker.pkg.dev/<work_project_id>/<repo_id>/transfer-resources-handler:latest -f ./services/handlers/transfer_resources/Dockerfile .
    docker build -t <location>-docker.pkg.dev/<work_project_id>/<repo_id>/transfer-resources-job:latest -f ./services/jobs/transfer_resources/Dockerfile .
    docker build -t <location>-docker.pkg.dev/<work_project_id>/<repo_id>/convert-private-tag-templates-handler:latest -f ./services/handlers/convert_private_tag_templates/Dockerfile .
    docker build -t <location>-docker.pkg.dev/<work_project_id>/<repo_id>/convert-private-tag-templates-job:latest -f ./services/jobs/convert_private_tag_templates/Dockerfile .
    ```
    Where
   * work_project_id - ID of the project you've created for this tool
   * location - location of the repository in Artifact Registry
   * repo_id - ID of the repository in Artifact Registry
3) Push the images to the repository in Artifact Registry
```
docker push <location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-resources-handler:latest
docker push <location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-resources-job:latest
docker push <location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-projects-handler:latest
docker push <location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-projects-job:latest
docker push <location>-docker.pkg.dev/<work_project_id>/<repo_id>/find-resource-names-handler:latest
docker push <location>-docker.pkg.dev/<work_project_id>/<repo_id>/find-resource-names-job:latest
docker push <location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-policies-handler:latest
docker push <location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-policies-job:latest
docker push <location>-docker.pkg.dev/<work_project_id>/<repo_id>/audit-logs-job:latest
docker push <location>-docker.pkg.dev/<work_project_id>/<repo_id>/analytics-job:latest
docker push <location>-docker.pkg.dev/<work_project_id>/<repo_id>/convert-private-tag-templates-handler:latest
docker push <location>-docker.pkg.dev/<work_project_id>/<repo_id>/convert-private-tag-templates-job:latest
docker push <location>-docker.pkg.dev/<work_project_id>/<repo_id>/transfer-resources-handler:latest
docker push <location>-docker.pkg.dev/<work_project_id>/<repo_id>/transfer-resources-job:latest
```
# Deploy
When you set up container commands, be sure to input them separately (as in the picture below)
![img_1.png](pictures/cloud_run_args.png)
## fetch-projects-job
1) Create a Cloud Run job
2) Select ```<location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-projects-job:latest``` image
3) In the Container section, use ```python3 main.py``` container command and ```-p <work_project_id>```
container arguments
4) In the Security section, select the Service Account you've created
## fetch-resources-job
1) Create a Cloud Run job
2) Select ```<location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-resources-job:latest``` image
3) In the Container section, use ```python3 main.py``` container command and ```-p <work_project_id>```
container arguments
4) In the Security section, select the Service Account you've created
## find-resource-names-job
1) Create a Cloud Run job
2) Select ```<location>-docker.pkg.dev/<work_project_id>/<repo_id>/find-resource-names-job:latest``` image
3) In the Container section, use ```python3 main.py``` container command and ```-p <work_project_id>```
container arguments
4) In the Security section, select the Service Account you've created
## fetch-policies-job
1) Create a Cloud Run job
2) Select ```<location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-policies-job:latest``` image
3) In the Container section, use ```python3 main.py``` container command and ```-p <work_project_id>```
container arguments
4) Set up scope of fetching with ```-s <scope>``` flag. Scope should be in format ```organizations/{orgNumber}```, ```folders/{folderNumber}``` or ```projects/{projectNumber}```
5) You can set up resource type using ```-rt entry_group|tag_template|both``` flag
6) You can set up system where to fetch policies by using ```-ms data_catalog|dataplex|both``` flag
7) In the Security section, select the Service Account you've created
## audit-logs-job
1) Create a Cloud Run job
2) Select ```<location>-docker.pkg.dev/<work_project_id>/<repo_id>/audit-logs-job:latest``` image
3) In the Container section, use ```python3 main.py``` container command and ```-p <work_project_id>```
container arguments
4) In the Security section, select the Service Account you've created
## analytics-job
1) Create a Cloud Run job
2) Select ```<location>-docker.pkg.dev/<work_project_id>/<repo_id>/analytics:latest``` image
3) In the Container section, use ```python3 main.py``` container command and ```-p <work_project_id>``` 
container arguments
4) In the Security section, select the Service Account you've created
## convert-private-tag-templates-job
1) Create a Cloud Run job
2) Select ```<location>-docker.pkg.dev/<work_project_id>/<repo_id>/convert-private-tag-templates-job:latest``` image
3) In the Container section, use ```python3 main.py``` container command and ```-p <work_project_id>```
container arguments
4) Set up scope of fetching with ```-s <scope>``` flag. Scope should be in format ```organizations/{orgNumber}```, ```folders/{folderNumber}``` or ```projects/{projectNumber}```
5) In the Security section, select the Service Account you've created
## transfer-resources-job
1) Create a Cloud Run job
2) Select ```<location>-docker.pkg.dev/<work_project_id>/<repo_id>/transfer-resources-job:latest``` image
3) In the Container section, use ```python3 main.py``` container command and ```-p <work_project_id>```
container arguments
4) Set up scope of fetching with ```-s <scope>``` flag. Scope should be in format ```organizations/{orgNumber}```, ```folders/{folderNumber}``` or ```projects/{projectNumber}```
5) You can set up resource type using ```-rt entry_group|tag_template|both``` flag
6) In the Security section, select the Service Account you've created
## fetch-projects-handler
1) Create a Cloud Run service
2) Select ```<location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-projects-handler:latest``` image
3) The service name should be ```fetch-projects-handler``` (Cloud tasks will target this name)
4) location ```us-central1```
5) Authentication - Require authentication
6) In Container section, use ```python3 main.py``` container command and ```-p <work_project_id>```
container arguments
7) In the Security section select the Service Account you've created
## fetch-resources-handler
1) Create a Cloud Run service
2) Select ```<location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-resources-handler:latest``` image
3) The service name should be ```fetch-resources-handler``` (Cloud tasks will target this name)
4) location ```us-central1```
5) Authentication - Require authentication
6) In the Container section, use ```python3 main.py``` container command and ```-p <work_project_id>```
container arguments
7) In the Security section, select the Service Account you've created
## find-resource-names-handler
1) Create a Cloud Run service
2) Select ```<location>-docker.pkg.dev/<work_project_id>/<repo_id>/find-resource-names-handler:latest``` image
3) The service name should be ```find-resource-names-handler``` (Cloud tasks will target this name)
4) location ```us-central1```
5) Authentication - Require authentication
6) In the Container section, use ```python3 main.py``` container command and ```-p <work_project_id>```
container arguments
7) In the Security section, select the Service Account you've created
## fetch-policies-handler
1) Create a Cloud Run service
2) Select ```<location>-docker.pkg.dev/<work_project_id>/<repo_id>/fetch-policies-handler:latest``` image
3) The service name should be ```fetch-policies-handler``` (Cloud tasks will target this name)
4) location ```us-central1```
5) Authentication - Require authentication
6) In the Container section, use ```python3 main.py``` container command and ```-p <work_project_id>```
container arguments
7) In the Security section, select the Service Account you've created
## convert-private-tag-templates-handler
1) Create a Cloud Run service
2) Select ```<location>-docker.pkg.dev/<work_project_id>/<repo_id>/convert-private-tag-templates-handler:latest``` image
3) The service name should be ```convert-private-tag-templates-handler``` (Cloud tasks will target this name)
4) location ```us-central1```
5) Authentication - Require authentication
6) In the Container section, use ```python3 main.py``` container command and ```-p <work_project_id>```
container arguments
7) In the Security section, select the Service Account you've created
## transfer-resources-handler
1) Create a Cloud Run service
2) Select ```<location>-docker.pkg.dev/<work_project_id>/<repo_id>/transfer-resources-handler:latest``` image
3) The service name should be ```transfer-resources-handler``` (Cloud tasks will target this name)
4) location ```us-central1```
5) Authentication - Require authentication
6) In the Container section, use ```python3 main.py``` container command and ```-p <work_project_id>```
container arguments
7) In the Security section, select the Service Account you've created

# Gather data
1) Launch fetch-projects-job
2) After finishing, launch fetch-resources-job
3) After finishing, launch find-resource-names-job
4) After finishing, launch fetch-policies-job
5) To see Data Catalog access logs, launch audit-logs-job and follow the instructions in [setup-logs-readme](services/jobs/audit_logs/README.md)
6) After finishing, launch analytics-job
7) All data will appear in ```transfer_tooling``` dataset in Google BigQuery

# Transfer
1) [Optional] Adjust scope parameter of ```convert-private-tag-templates-job``` and run it to convert all private tag templates within given scope to public tag templates
2) Wait 24h
3) Adjust both scope and resource type parameter of ```convert-private-tag-templates-job``` and run it to transfer resources to Dataplex Catalog
