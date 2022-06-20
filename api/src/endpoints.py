import fastapi

from src.schemas import BodyCreateWallet, ResponseCreateWallet
from src.services import service

app = fastapi.APIRouter()


@app.post(
    "/create/wallet",
    description="Creates a TRON wallet",
    response_model=ResponseCreateWallet,
    tags=["WALLET"]
)
async def create_wallet(body: BodyCreateWallet):
    if body.index is None or body.index == [0, 0]:
        return await service.create_new_wallet(body=body)
    else:
        return await service.generate_wallet(body=body)
