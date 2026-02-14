import qrcode
import os

# =============================
# CONFIGURATION
# =============================

BASE_URL = "https://quickbite-ai-yquo.onrender.com"
RESTAURANT_ID = "rest_001"
TABLES = range(1, 11)   # Generates table 1 to 10

OUTPUT_DIR = "qr_codes"

# =============================
# CREATE OUTPUT FOLDER
# =============================

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("🚀 Generating QR codes...")

for table_id in TABLES:

    url = f"{BASE_URL}/menu?restaurant_id={RESTAURANT_ID}&table_id={table_id}"

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    file_path = os.path.join(OUTPUT_DIR, f"table_{table_id}.png")
    img.save(file_path)

    print(f"✅ Generated QR for Table {table_id}")

print("🎉 All QR codes generated successfully!")
