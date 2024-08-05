from openpyxl import Workbook
from io import BytesIO

# Create a workbook and add a worksheet
wb = Workbook()
ws = wb.active
ws['A1'] = 'Hello, World!'

# Save the workbook to a BytesIO object
byte_stream = BytesIO()
wb.save(byte_stream)

# Get the byte content
byte_content = byte_stream.getvalue()

# Optionally, save the byte content to a file
with open('output.xlsx', 'wb') as f:
    f.write(byte_content)

print("Workbook saved to output.xlsx")
