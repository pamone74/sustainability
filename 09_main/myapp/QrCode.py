
import random
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import fitz
#from pyzbar.pyzbar import decode
from PIL import Image
import uuid
import base64


def generate_qr_code(item_name, item_description, random_number, ownership, status, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(f"Item Name: {item_name}\nItem Description: {item_description}\nUnique Number: {random_number}\nStatus: {status}\nOwnership: {ownership}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    filename = f"{filename}.png"
    img.save(filename)
    return filename

def generate_item_list(item_name, item_description, num_items, ownership, status):
    items = []
    item_name = f"{item_name.capitalize()}"
    # This loop is inteded for creating list of items. but it is us.eless if the item being created is only one.
    for i in range(num_items):
        # uuid1 Generates unique ID based on Currrent time and MAC address in (hash)32 hex charaters represent 128 bits
        uuid_cal = uuid.uuid1()
        # Convert it to bytes
        unid_bytes = uuid_cal.bytes
        # Encode bytes using Base64 , keep in mind that Base64 endcoding reduces the length of UUID. We are are endcoding it to be more user friendly.
        encoded_base = base64.urlsafe_b64encode(unid_bytes).decode('utf-8')
        # When we encode, the last two characters are equal signs, so we need to slice it [:-2]
        random_number = str(encoded_base[:-2])


        item = {
            "name": item_name,
            "description": item_description,
            "random_number": random_number,
            "item_status": status,
            "item_ownership": ownership
        }
        items.append(item)
        filename = generate_qr_code(item_name, item_description, random_number, ownership, status, f"{item_name}[{random_number}]")
        item["qr_filename"] = filename
    if num_items == 1:
        item = {
                    "name": item_name,
                    "description": item_description,
                    "random_number": random_number,
                    "item_status": status,
                    "item_ownership": ownership
        }
        filename = generate_qr_code(item_name, item_description, random_number, ownership, status, f"{item_name}[{random_number}]")
        item["qr_filename"] = filename
        return item
    return items

def generate_pdf(item_list, pdf_filename):
    if item_list:
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        y = 750
        # Check if item_list is a single item (dictionary)
        if isinstance(item_list, dict):
            c.drawString(50, y, f"Item Name: {item_list['name']}")
            c.drawImage(item_list["qr_filename"], 50, y-110, width=100, height=100)
            y -= 130
            c.save()
            os.remove(item_list["qr_filename"])
        else:
            for item in item_list:
                c.drawString(50, y, f"Item Name: {item['name']}")
                c.drawImage(item["qr_filename"], 50, y-110, width=100, height=100)
                y -= 130
                c.save()
                # os.remove(item["qr_filename"])
        return pdf_filename



def read_qr_code(filename):
    with open(filename, 'rb') as image_file:
        image = Image.open(image_file)
        decoded_objects = decode(image)
    for obj in decoded_objects:
        if obj.type == 'QRCODE':
            data = obj.data.decode('utf-8')
            lines = data.split('\n')
            for line in lines:
                if 'Unique Number' in line:
                    return line.split(':')[-1].strip()
        else:
            return None



def extract_images_from_pdf(pdf_file, product_code):
    # Open the PDF file
    pdf_document = fitz.open(pdf_file)
    found = False

    images = []

    # Iterate through each page of the PDF
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)

        # Get the images on the page
        image_list = page.get_images(full=True)

        # Iterate through the images on the page
        for img_info in image_list:
            xref = img_info[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_extension = base_image["ext"]
            image_filename = f"page_{page_number}_image_{xref}.{image_extension}"
            if int(read_qr_code(image_filename))== product_code:
                found = True
            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)       
            images.append(image_filename)
            if int(read_qr_code(image_filename))== product_code:
                found = True

    # Close the PDF document
    pdf_document.close()

    return found







# print(uuid_cal)
# print(encoded_base.upper()[:-4])
# Example usage
# pdf_file = "2024-04-01.pdf"
# extracted_images = extract_images_from_pdf(pdf_file, 3850)
# print("Extracted Images:", extracted_images)
# print(("Read Qr cpoed: ", read_qr_code("page_0_image_3.png")))
# 

# print(f"{generate_pdf(generate_item_list("bottle", "none",1, "Amone", "Not recycled"),"created.pdf")} \n")
# 
# print(read_qr_code("Aluminium can_[tfl_ffh_ee6flabihmgumg].png"))