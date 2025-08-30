from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorCollection
from store.core.database import db
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException


class ProductUsecase:
    def __init__(self) -> None:
        # Usa a collection "products" diretamente
        self.collection: AsyncIOMotorCollection = db["products"]

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())
        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": str(id)})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(self) -> List[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        result = await self.collection.find_one_and_update(
            {"id": str(id)},
            {"$set": body.model_dump(exclude_none=True)},
            return_document=True,  # motor já entende return_document=True
        )

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        result = await self.collection.delete_one({"id": str(id)})

        if result.deleted_count == 0:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return True


product_usecase = ProductUsecase()