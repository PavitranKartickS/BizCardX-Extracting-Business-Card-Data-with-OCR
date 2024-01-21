import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
import mysql.connector as sql
from PIL import Image
import cv2
import os
import matplotlib.pyplot as plt
import re
import time
import numpy as np


# Page Setup:

webicon = Image.open("Icon.png")

st.set_page_config(layout="wide",
                   page_title= "BizcardX - Extracting Business Card Data with easyOCR",
                   page_icon=webicon,
                   menu_items={'About':"""## This OCR application is brought to you by S.Pavitran Kartick"""})

st.markdown("<h1 style='text-align: center; color: #Ffe3ba ;'</h1>BizcardX - Business Card Data Extraction</h1>", unsafe_allow_html=True)

#Application backdrop

def web_app_backdrop():
    st.markdown(f""" <style>.stApp {{
                        background: url("https://mcdn.wallpapersafari.com/medium/8/20/WVKYy3.jpg");
                        background-size: cover}}
                     </style>""",unsafe_allow_html=True)
web_app_backdrop()


# Connecting to MYSQL Database
mydb = sql.connect(host="localhost",
                   user="root",
                   password="12345",
                   database= "bizcard"
                  )
mycursor = mydb.cursor(buffered=True)

# Creating the main table for data
mycursor.execute('''CREATE TABLE IF NOT EXISTS card_data
                   (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    company_name TEXT,
                    card_holder TEXT,
                    designation TEXT,
                    mobile_number VARCHAR(50),
                    email TEXT,
                    website TEXT,
                    area TEXT,
                    city TEXT,
                    state TEXT,
                    pin_code VARCHAR(10),
                    image LONGBLOB
                    )''')

# Initializing the Reader
reader = easyocr.Reader(['en'])

#Main Option Menu
selected = option_menu(None, ["Home","Upload & Extract","Alter/Modify"], 
                       icons=["house","cloud-upload","pencil-square"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "35px", "text-align": "centre", "margin": "5px", "--hover-color": "#1a7e19"},
                               "icon": {"font-size": "30px"},
                               "container" : {"max-width": "6000px"},
                               "nav-link-selected": {"background-color": "#1a7e19"}})

# Home 
if selected == "Home":
    con1=st.container()
    con2=st.container()
    with con1:
        st.markdown("## :orange[**Concepts Utilized :**] Streamlit, Python, easyOCR, MySQL, Pandas")
        st.markdown("## :orange[**Overview :**] The primary function of this Web application is to extract contact information from business card images uploaded by the user. This information is then stored into a database managed by MySQL. There are features for viewing, deleting and updating the information in the table with the help of streamlit gui and MySQL.")
    with con2:
        st.image("home.jpg")


# Upload & Extract
if selected == "Upload & Extract":
    st.markdown("### :orange[Upload a Business Card]")
    uploaded_card = st.file_uploader("click here to upload",label_visibility="collapsed",type=["png","jpeg","jpg"])
        
    if uploaded_card is not None:
        
        def save_card(uploaded_card):
            with open(os.path.join("cards",uploaded_card.name), "wb") as f:
                f.write(uploaded_card.getbuffer())   
        save_card(uploaded_card)

        def image_preview(image,res): 
            for (bbox, text, prob) in res: 
              # unpack the bounding box
                (tl, tr, br, bl) = bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                cv2.putText(image, text, (tl[0], tl[1] - 10),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 0, 0), 2)
            plt.rcParams['figure.figsize'] = (15,15)
            plt.axis('off')
            plt.imshow(image)
        
        # DISPLAYING THE UPLOADED CARD
        col1,col2 = st.columns(2,gap="large")
        with col1:
            st.markdown("#     ")
            st.markdown("#     ")
            st.markdown("### You have uploaded the card")
            st.image(uploaded_card)

        # DISPLAYING THE CARD WITH HIGHLIGHTS
        with col2:
            st.markdown("#     ")
            st.markdown("#     ")
            with st.spinner("Please wait processing image..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                saved_img = os.getcwd()+ "\\" + "cards"+ "\\"+ uploaded_card.name
                image = cv2.imread(saved_img)
                res = reader.readtext(saved_img)
                st.markdown("### Image Processed and Data Extracted")
                st.pyplot(image_preview(image,res))

        #easy OCR
        saved_img = os.getcwd()+ "\\" + "cards"+ "\\"+ uploaded_card.name
        result = reader.readtext(saved_img,detail = 0,paragraph=False)
        st.markdown("### Extracted Data:")
        st.write(result)

        #Converting image to binary file for storage in MYSQL
        def img2binary(file):
            with open(saved_img, 'rb') as file:
                binaryData = file.read()
            return binaryData
        
        #Creating dictionary to store all card details:
        data = {"company_name" : [],
                "card_holder" : [],
                "designation" : [],
                "mobile_number" :[],
                "email" : [],
                "website" : [],
                "area" : [],
                "city" : [],
                "state" : [],
                "pin_code" : [],
                "image" : img2binary(saved_img)
               }
        #Function to sort data from result onto the keys of dictionary
        def insert_data(result):
            ph_pattern = r"\+*\d{2,3}-\d{3}-\d{4}"
            name_pattern = r'^[A-Za-z]+ [A-Za-z]+$|^[A-Za-z]+$|^[A-Za-z]+ & [A-Za-z]+$'

            for ind,i in enumerate(result):

                # To get the URL
                if "www " in i.lower() or "www." in i.lower():
                    data["website"].append(i)
                elif "WWW" in i:
                    data["website"] = result[4] +"." + result[5]

                # To get email
                elif "@" in i:
                    data["email"].append(i)

                # To get mobile number 
                elif "-" in i:
                    data["mobile_number"].append(i)
                    if len(data["mobile_number"]) ==2:
                        data["mobile_number"] = " & ".join(data["mobile_number"])

                # To get company  
                elif ind == len(res)-1:
                    data["company_name"].append(i)

                # To get card holder
                elif ind == 0:
                    data["card_holder"].append(i)

                # To get designation
                elif ind == 1:
                    data["designation"].append(i)

                # To get area
                if re.findall('^[0-9].+, [a-zA-Z]+',i):
                    data["area"].append(i.split(',')[0])
                elif re.findall('[0-9] [a-zA-Z]+',i):
                    data["area"].append(i)

                # To get city
                match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
                match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
                match3 = re.findall('^[E].*',i)
                if match1:
                    data["city"].append(match1[0])
                elif match2:
                    data["city"].append(match2[0])
                elif match3:
                    data["city"].append(match3[0])

                # To get state
                state_match = re.findall('[a-zA-Z]{9} +[0-9]',i)
                if state_match:
                     data["state"].append(i[:9])
                elif re.findall('^[0-9].+, ([a-zA-Z]+);',i):
                    data["state"].append(i.split()[-1])
                if len(data["state"])== 2:
                    data["state"].pop(0)

                # To get pincode        
                if len(i)>=6 and i.isdigit():
                    data["pin_code"].append(i)
                elif re.findall('[a-zA-Z]{9} +[0-9]',i):
                    data["pin_code"].append(i[10:])
        insert_data(result)
        


        #create dataframe with the dictionary data
        def create_dataframe(data):
            df = pd.DataFrame(data)
            return df
        df = create_dataframe(data)
        st.success("### Data Procured.")

        if st.button("Upload to database"):
            for i,row in df.iterrows():
                query = """INSERT INTO card_data(company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code,image)
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                mycursor.execute(query, tuple(row))
                mydb.commit()
            st.success("Text extracted & successfully uploaded to database", icon="☑️")


# Alter/Modify
            
if selected == "Alter/Modify":
    with st.spinner('Connecting...'):
            time.sleep(1)
    option = option_menu(None, ['Image data', "Update data", "Delete data"],
                                 orientation="horizontal",
                                 icons=["image", "pencil-fill", 'exclamation-diamond'], default_index=0)
    mycursor.execute("SELECT * FROM card_data")
    myresult = mycursor.fetchall()

    #convert into dataframe using pandas
    df=pd.DataFrame(myresult,columns=['id','company','name','designation','contact','email','website','address','city','state','pincode','image'])
    df.set_index('id', drop=True, inplace=True)
    st.write(df)

    #Displaying data from database
    if option == "Image data":
        left, right = st.columns([2, 2.5])
        with left:
            mycursor.execute("SELECT card_holder,designation FROM card_data")
            rows = mycursor.fetchall()
            row_name = [row[0] for row in rows]   
            row_designation = [row[1] for row in rows]
            # Display the selection box
            selection_name = st.selectbox("Name:", row_name)     
            selection_designation = st.selectbox("Designation:", row_designation)
            if st.button('Show Image'):
                with right:
                    sql = "SELECT image FROM card_data WHERE card_holder = %s AND designation = %s"
                    mycursor.execute(sql, (selection_name, selection_designation))
                    result = mycursor.fetchone()
                    # Check if image data exists
                    if result is not None:
                        # Retrieve the image data from the result
                        image_data = result[0]
                        # Create a file-like object from the image data
                        nparr = np.frombuffer(image_data, np.uint8)
                        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        st.image(image, channels="BGR", use_column_width=True)
                    if result is None:
                        st.error("Image not found for the given name and designation.")
    #update data in database for selected name and designation
    elif option=='Update data':
        name,new_name=st.columns(2)
        with name:
            # Get the available row IDs from the database
            mycursor.execute("SELECT card_holder,designation FROM card_data")
            rows = mycursor.fetchall()
            row_name = [row[0] for row in rows]
            row_designation = [row[1] for row in rows]

            # Display the selection box
            selection_name = st.selectbox("Select name to update", row_name)
            selection_designation = st.selectbox("Select designation to update", row_designation)
        with new_name:
            # Get the column names from the table
            mycursor.execute("SHOW COLUMNS FROM card_data")
            columns = mycursor.fetchall()
            column_names = [i[0] for i in columns if i[0] not in ['id', 'image','name','designation']]

            # Display the selection box for column name
            selection = st.selectbox("Select specific column to update", column_names)
            new_data = st.text_input(f"Enter the new {selection}")

            # Define the SQL query to update the selected rows
            sql = f"UPDATE card_data SET {selection} = %s WHERE card_holder = %s AND designation = %s"

            # Execute the query with the new values
            if st.button("Update"):
                mycursor.execute(sql, (new_data, selection_name, selection_designation))
                # Commit the changes to the database
                mydb.commit()
                st.success("Updated successfully")


    #===delete data for selected name and dsignation===
    else:
        left,right=st.columns([2,2.5])
        with left:
            mycursor.execute("SELECT card_holder,designation FROM card_data")
            rows = mycursor.fetchall()    #collecting all the data
            row_name = [row[0] for row in rows]
            row_designation = [row[1] for row in rows]
        # Display the selection box
            selection_name = st.selectbox("Select name of the entry to delete", row_name)
        with right:
            selection_designation = st.selectbox("Select designation of the entry to delete", row_designation)
        with left:
            if st.button('DELETE'):
                sql = "DELETE FROM card_data WHERE card_holder = %s AND designation = %s"
            # Execute the query with the values as a tuple
                mycursor.execute(sql, (selection_name, selection_designation))
                mydb.commit()
                st.success('Deleted successfully')

        st.write('')
        st.markdown('### :orange[About]')
        st.write('This is a web application that allows users to upload business card images and extract relevant information. The application has been built in a user-friendly way using Streamlit and python as the framework. This application takes the uploaded image and extracts the relevant information from it using easyOCR. The extracted information is then uploaded into the database created with MYSQL. We are also able to perform operations like viewing, updating and deleting the data. This is to combat the lack of accuracy when it comes to EasyOCR.')
        st.info('The detection methods of EasyOCR are less developed compared to latest technology, and hence can have incorrect results. The project has scope for improvement in the future.')

