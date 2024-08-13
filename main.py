import qrcode


def generate_qr_code(student_id, student_info):
    # Combine student info into a formatted string with delimiter
    data = (
        f"{student_id}|{student_info['Name']}|{student_info['Course']}|{student_info['Year']}|{student_info['Age']}|{student_info['Address']}"
    )

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code instance
    img = qr.make_image(fill='black', back_color='white')
    img.save(f"student_{student_id}_qrcode.png")


# Example usage
student_data = {
    '20240001': {'Name': 'John Doe', 'Course': 'BS Computer Science', 'Year': '1st Year', 'Age': '19',
                 'Address': 'Mangatarem Pangasinan'},
    '20240002': {'Name': 'Jane Smith', 'Course': 'BS Information Technology', 'Year': '2nd Year', 'Age': '20',
                 'Address': 'San Clemente Tarlac'},
    '20240003': {'Name': 'Emily Davis', 'Course': 'BS Information Systems', 'Year': '3rd Year', 'Age': '21',
                 'Address': 'Camiling TARLAC'},
}

for student_id, info in student_data.items():
    generate_qr_code(student_id, info)
