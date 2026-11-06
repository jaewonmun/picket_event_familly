# 피켓용 QR 생성: python make_qr.py https://<아이디>.github.io/<저장소>/
import sys, qrcode
from qrcode.constants import ERROR_CORRECT_M

base = sys.argv[1].rstrip("/") + "/"
for m in range(1, 6):
    url = f"{base}?m={m}"
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=40, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    qr.make_image(fill_color="black", back_color="white").save(f"qr_m{m}.png")
    print(f"qr_m{m}.png -> {url}")
