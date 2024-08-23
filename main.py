import os
import time
import pyfiglet
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from io import BytesIO
from colorama import init, Fore, Style

# Initialize colorama
init()

def clear():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def first_banner():
    """Display the initial banner."""
    clear()
    salfi = pyfiglet.Figlet(font="starwars")
    banner = salfi.renderText("Cyber Fantics")
    print(f'{Fore.YELLOW}{banner}{Style.RESET_ALL}')
    time.sleep(2)  # Pause to let the banner be read

def create_overlay_pdf(page_number, pagesize, header_text, footer_text):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=pagesize)
    
    # Draw border
    border_margin = 30
    width, height = pagesize
    can.setStrokeColor(HexColor('#4B0000'))  # Dark green border
    can.setLineWidth(3)
    can.roundRect(border_margin, border_margin, width - 2 * border_margin, height - 2 * border_margin, radius=10, stroke=1, fill=0)
    
    # Add page number
    can.setFont("Helvetica", 8)
    can.setFillColor(HexColor('#4B0000'))  # Dark blue color
    can.drawString(width - 71, 15, f'Page {str(page_number)}')
    
    # Add footer with document title and custom footer
    can.setFont("Helvetica", 8)
    can.setFillColor(HexColor('#4B0000'))  # Dark blue color
    can.drawString(50, 15, footer_text)
    can.drawString(width - 89, height - 18, header_text)  # Custom header
    
    can.save()
    packet.seek(0)
    
    # Create a PDF from the canvas
    new_pdf = PdfReader(packet)
    return new_pdf.pages[0]

def add_borders_and_numbers(input_pdf_path, output_pdf_path, header_text, footer_text, start_page_number=None):
    print(f'{Fore.CYAN}Processing {input_pdf_path}...{Style.RESET_ALL}')
    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(input_pdf_path)
    
    for page_number, page in enumerate(pdf_reader.pages, start=start_page_number or 1):
        if start_page_number is not None:
            # Create an overlay with border and page number only if we need it
            overlay = create_overlay_pdf(page_number, letter, header_text, footer_text)
            page.merge_page(overlay)
        pdf_writer.add_page(page)
    
    # Write out the final PDF
    with open(output_pdf_path, 'wb') as f:
        pdf_writer.write(f)
    print(f'{Fore.GREEN}PDF with borders and page numbers saved as {output_pdf_path}{Style.RESET_ALL}')
    time.sleep(2)  # Add a delay of 2 seconds

def merge_pdfs(output_pdf, pdf_files):
    print(f'{Fore.MAGENTA}Merging PDFs...{Style.RESET_ALL}')
    pdf_writer = PdfWriter()
    
    for pdf_file in pdf_files:
        if not os.path.isfile(pdf_file):
            print(f'{Fore.RED}File not found: {pdf_file}{Style.RESET_ALL}')
            time.sleep(1)  # Add a delay of 1 second
            continue
        
        try:
            pdf_reader = PdfReader(pdf_file)
            print(f'{Fore.CYAN}Adding {pdf_file} with {len(pdf_reader.pages)} pages{Style.RESET_ALL}')
            time.sleep(1)  # Add a delay of 1 second
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)
        except Exception as e:
            print(f'{Fore.YELLOW}Error with {pdf_file}: {e}{Style.RESET_ALL}')
            time.sleep(1)  # Add a delay of 1 second
    
    # Save the merged PDF
    with open(output_pdf, 'wb') as f:
        pdf_writer.write(f)
    print(f'{Fore.GREEN}Merged PDF saved as {output_pdf}{Style.RESET_ALL}')
    time.sleep(2)  # Add a delay of 2 seconds

def process_pdfs():
    """Handle the processing of PDF files."""
    # Prompt user for file paths and custom text with colors
    head_pdf_path = input(f"{Fore.MAGENTA}Enter the path for the 'titanic head' PDF file: {Style.RESET_ALL}")
    data_pdf_path = input(f"{Fore.MAGENTA}Enter the path for the 'titanic' PDF file: {Style.RESET_ALL}")
    header_text = input(f"{Fore.MAGENTA}Enter the header text to be used on all pages: {Style.RESET_ALL}")
    footer_text = input(f"{Fore.MAGENTA}Enter the footer text to be used on all pages: {Style.RESET_ALL}")
    
    # Define paths for processed PDFs
    downloads_folder = os.path.expanduser('~/Downloads/merge files')
    processed_head_pdf_path = os.path.join(downloads_folder, 'titanic_head_with_borders_and_numbers.pdf')
    processed_data_pdf_path = os.path.join(downloads_folder, 'titanic_body.pdf')
    
    # Process head.pdf without borders and page numbers
    add_borders_and_numbers(head_pdf_path, processed_head_pdf_path, header_text, footer_text, start_page_number=None)
    
    # Process data.pdf with borders and page numbers starting from 1
    add_borders_and_numbers(data_pdf_path, processed_data_pdf_path, header_text, footer_text, start_page_number=1)
    
    # Merge processed PDFs
    output_pdf = os.path.join(downloads_folder, 'titanic_output.pdf')
    merge_pdfs(output_pdf, [processed_head_pdf_path, processed_data_pdf_path])
    
    # Delete intermediate PDFs
    try:
        os.remove(processed_head_pdf_path)
        print(f'{Fore.RED}Deleted: {processed_head_pdf_path}{Style.RESET_ALL}')
    except FileNotFoundError:
        print(f'{Fore.RED}File not found: {processed_head_pdf_path}{Style.RESET_ALL}')
    
    try:
        os.remove(processed_data_pdf_path)
        print(f'{Fore.RED}Deleted: {processed_data_pdf_path}{Style.RESET_ALL}')
    except FileNotFoundError:
        print(f'{Fore.RED}File not found: {processed_data_pdf_path}{Style.RESET_ALL}')

def main():
    while True:
        first_banner()
        
        print(f'{Fore.MAGENTA}Welcome to the PDF Processing Script!{Style.RESET_ALL}')
        time.sleep(1)
        
        process_pdfs()
        
        # Ask user if they want to process more PDFs
        continue_processing = input(f"{Fore.CYAN}Do you want to process another set of PDFs? (yes/no): {Style.RESET_ALL} ").strip().lower()
        
        if continue_processing[0] != 'y':
            print(f'{Fore.GREEN}Exiting the script. Have a great day!{Style.RESET_ALL}')
            break
        else:
            first_banner()
            print(f'{Fore.YELLOW}Preparing to process more PDFs...{Style.RESET_ALL}')
            time.sleep(2)  # Delay before clearing the screen
            clear()

if __name__ == "__main__":
    main()
