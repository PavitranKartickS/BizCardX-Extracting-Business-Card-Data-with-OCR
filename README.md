# BizCardX-Extracting-Business-Card-Data-with-OCR

## What is EasyOCR?
OCR is formerly known as Optical Character Recognition which is revolutionary for the digital world nowadays. OCR is actually a complete process under which the images/documents which are present in a digital world are processed and from the text are being processed out as normal editable text.EasyOCR is actually a python package that holds PyTorch as a backend handler. It detects the text from images but in my reference, while using it I found that it is the most straightforward way to detect text from images also when high end deep learning library(PyTorch) is supporting it in the backend which makes it accuracy more credible. EasyOCR supports 42+ languages for detection purposes. EasyOCR is created by the company named Jaided AI company.

### Advantages:
- The EasyOCR package can be installed with a single pip command.
- The dependencies on the EasyOCR package are minimal, making it easy to configure your OCR development environment.
- Once EasyOCR is installed, only one import statement is required to import the package into your project.
- From there, all you need is two lines of code to perform OCR — one to initialize the Reader class and then another to OCR the image via the readtext function.

### Features:

- Extracts text information from business card images using EasyOCR.
- Utilizes OpenCV for image preprocessing, such as resizing, cropping, and enhancing.
- Uses regular expressions (RegEx) to parse and extract specific fields like name, designation, company, contact details, etc.
- Stores the extracted information in a MySQL database for easy retrieval and analysis.
- Provides a user-friendly interface built with Streamlit to upload images, extract information, and view/update the database.

## Modules Imported for this Project

   - Pandas - (To Create a DataFrame with the scraped data)
   - OpenCV - (To display the extracted information on the business card)
   - mySQL - (To maintain and display the data)
   - Streamlit - (To Create Graphical user Interface)
   - EasyOCR - (To extract text from images)

## Scope/drawbacks of the Project
- This project can be developed further by deploying authorization systems for restricted user access.
- The project has been designed to specifically work for business cards, and thus cannot provide favorable results for other types of images
- The only language that has been utilized in this web application is english. Thereby business cards for other languages cannot be processed with this web app.

## Acknowledgments
Streamlit - For building interactive web applications with ease.
EasyOCR - For text extraction from images.
OpenCV - For image preprocessing and manipulation.
MySQL - For the database management system.
