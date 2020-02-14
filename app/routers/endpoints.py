from typing import List

from fastapi import FastAPI, Depends, Security

from ..models.endpoints import Endpoint, EndpointOut
from ..db import endpoints as endpoint_db
from .auth import Credentials, decode_identity_header

endpoints = FastAPI()


@endpoints.get("/endpoints", response_model=List[EndpointOut])
async def get_endpoints(identity: Credentials = Depends(decode_identity_header)):
    # Depends on security with the account_id
    db_endpoints = await endpoint_db.get_endpoints(account_id=identity.account_number)
    return db_endpoints


@endpoints.post("/endpoints")
async def create_endpoint(endpoint: Endpoint, identity: Credentials = Depends(decode_identity_header)):
    # TODO This should maybe return 204 or something (no response) ? Now it returns null
    await endpoint_db.create_endpoint(account_id=identity.account_number, endpoint=endpoint)


@endpoints.put("/endpoints/email/subscription/{event_type}")
async def subscribe_email_endpoint(event_type: str, identity: Credentials = Depends(decode_identity_header)):
    pass


@endpoints.delete("/endpoints/email/subscription/{event_type}")
async def unsubscribe_email_endpoint(event_type: str, identity: Credentials = Depends(decode_identity_header)):
    pass


@endpoints.get("/endpoints/{id}", response_model=EndpointOut)
async def get_endpoint(id: str, identity: Credentials = Depends(decode_identity_header)):
    return await endpoint_db.get_endpoint(account_id=identity.account_number, id=id)


@endpoints.delete("/endpoints/{id}")
async def delete_endpoint(id: str, identity: Credentials = Depends(decode_identity_header)):
    pass


@endpoints.put("/endpoints/{id}")
async def update_endpoint(id: str, endpoint: Endpoint, identity: Credentials = Depends(decode_identity_header)):
    pass
