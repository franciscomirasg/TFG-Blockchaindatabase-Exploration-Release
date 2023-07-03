from pydantic import BaseModel


class ShopItem(BaseModel):
    """
    Shop item
    """
    name: str
    description: str
    price: int
    article_id: int

    def __str__(self) -> str:
        return f"{self.name}: {self.description} - {self.price} points"


ITEMS = [
    ShopItem(
        name="T-Shirt",
        description="Cotton T-Shirt",
        price=20,
        article_id=1
    ),
    ShopItem(
        name="Discount Voucher",
        description="10% discount at local restaurants",
        price=100,
        article_id=2
    ),
    ShopItem(
        name="Free Membership",
        description="Free membership to the pool. Access to the pool for 1 month",
        price=150,
        article_id=3
    ),
    ShopItem(
        name="Free Parking Hours",
        description="24 hours of free municipal parking",
        price=30,
        article_id=4
    ),
    ShopItem(
        name="Recycle pin",
        description="A pin that says you recycle",
        price=1,
        article_id=5
    )
]
