from fastapi import APIRouter, Response
import segno

router = APIRouter()
URI = "upi://pay?pn={name}&am={amount}&mode=01&pa={upi}"


@router.get("/")
async def create(amount: str, name: str, upi_id: str):
    amount = 10 if not amount else amount
    name = 'Butena' if not name else name
    if not upi_id:
        return Response(content="Nothing", media_type='html/xhtml')

    from io import BytesIO
    buffer = BytesIO()
    uri = URI.format(name=name, amount=amount, upi=upi_id)
    segno.make(uri).save(buffer, kind='svg', scale=4)
    return Response(content=buffer.getvalue(), media_type="image/svg+xml")
