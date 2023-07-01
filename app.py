import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import easyocr
from PIL import Image
import numpy as np
import base64

#hide menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



def app():
    st.title('Image Text Extractor📝')
    uploaded_file = st.file_uploader("Choose an image file" , type=['jpg','png','jpeg'])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img = np.array(image)

        st.image(image, caption='Uploaded Image', use_column_width=True)
        st.write("")

        st.write("Recognized Text")
        reader = easyocr.Reader(['en']) # need to run only once to load model into memory
        result = reader.readtext(img)

        # Initialize dataframe
        df = pd.DataFrame(columns=['Text'])

        # Fill the dataframe with the results
        for i in result:
            df = df.append({'Text': i[1]}, ignore_index=True)

        # Display the data as a table
        df_styled = df.style.set_properties(**{'text-align': 'left'})
        df_styled.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
        st.dataframe(df_styled)

        # Let the user download the results as a CSV file
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="text.csv">Download csv file</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
