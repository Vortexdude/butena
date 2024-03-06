import segno

data = "upi://pay?pn=NitinNamdev&am=250&mode=01&pa=9630955003@axl"

qrcode = segno.make_qr(data)
qrcode.save("basic_qrcode.png")
