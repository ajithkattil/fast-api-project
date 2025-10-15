from uuid import uuid4

from src.api.routes.v1.models import (
    Address,
    ContactNumber,
    FulfillmentOptions,
    OrderPostRequest,
    OrderRecipe,
    PostalAddress,
    SpecialHandlings,
)


def order_post_request() -> OrderPostRequest:
    return OrderPostRequest(
        arrivalDate="2025-05-30",
        recipes=[OrderRecipe(recipeId=uuid4(), quantity=1)],
        fulfillable=True,
        salesChannelId="123",
        brandId="xyz",
        shippingAddress=address(),
        fulfillmentOptions=FulfillmentOptions(
            specialHandlings=[SpecialHandlings("WHITE_GLOVE_BOX")], deliveryOptionToken="abc"
        ),
    )


def address() -> Address:
    postal_address = PostalAddress(
        postalCode="123456",
        administrativeArea="Test Area",
        locality="",
        addressLines=["123 Test St", "Test City"],
        recipients=["Test Recipient"],
    )
    contact_number = ContactNumber(phoneNumber="12345678900")
    return Address(
        postalAddress=postal_address,
        contactNumber=contact_number,
        locationType="RESIDENTIAL",
        deliveryInstructions="delivery instructions",
    )
