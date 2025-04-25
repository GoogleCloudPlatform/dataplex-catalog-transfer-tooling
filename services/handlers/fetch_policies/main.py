# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module defines a server application using the Fastapi framework.
It is designed to handle cloud tasks related to Google Cloud Platform (GCP)
resources, specifically for managing entry groups and tag templates in a data
catalog.
"""
import asyncio

from fastapi import FastAPI, Response
import uvicorn

from common.entities import FetchPoliciesTaskData
from config import get_application_config
from handler import CloudTaskHandler

app = FastAPI()


config = get_application_config() #TODO: use dependencies
handler = CloudTaskHandler(config)

@app.api_route('/', methods=['POST', 'PUT'])
async def process_task(task_data: FetchPoliciesTaskData, response: Response):
    """
    Route to process cloud tasks.
    """
    loop = asyncio.get_event_loop()
    body, status_code = await loop.run_in_executor(
        None, handler.handle_cloud_task, task_data
    )
    response.status_code = status_code

    return body

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
