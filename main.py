import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Visualizer", page_icon="icon.png", layout="wide", initial_sidebar_state="auto")
# Function to upload file and read data
def upload_file():
    file_col1, file_col2 = st.columns(2)

    with file_col1:
        uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

    with file_col2:
        if uploaded_file is not None:
            try:
                # If it's an Excel file, show the sheet names and let the user choose
                if uploaded_file.name.endswith('xlsx'):
                    xls = pd.ExcelFile(uploaded_file)
                    sheet_names = xls.sheet_names
                    selected_sheet = st.selectbox("Select a worksheet:", sheet_names)
                    df = pd.read_excel(xls, sheet_name=selected_sheet)
                else:
                    # For CSV or other formats, read the data directly
                    df = pd.read_csv(uploaded_file)
                
                return df
            except Exception as e:
                st.error(f"Error: {e}")

    return None



# Main function to display the app
def main():
    st.title("📊 Streamlit Data :orange[Editor] and :orange[Visualizer]")
    
    # Upload file and get DataFrame
    data = upload_file()
    
    if data is not None:
        
        col1, col2 = st.columns(2)
        # Allow user to edit data
        with col1:
            st.subheader("Edit Data")
            edited_data = st.data_editor(data, height=750, width=1000)
        with col2:
        # Display data in visual format
            st.subheader("Visualize Data")
            chart_type = st.selectbox("Select Chart Type", ["Bar Chart",  "Line Chart", "Scatter Plot", "Box Plot", "Violin Plot", "Pie Chart"])
            
            if chart_type == "Bar Chart":
                fig = px.bar(data, x=data.columns[0], y=data.columns[1])
            elif chart_type == "Line Chart":
                fig = px.line(data, x=data.columns[0], y=data.columns[1])
            elif chart_type == "Line Chart":
                fig = px.line(data, x=data.columns[0], y=data.columns[1])
            elif chart_type == "Scatter Plot":
                fig = px.scatter(data, x=data.columns[0], y=data.columns[1])
            elif chart_type == "Box Plot":
                fig = px.box(data, x=data.columns[0], y=data.columns[1])
            elif chart_type == "Violin Plot":
                fig = px.violin(data, x=data.columns[0], y=data.columns[1])
            elif chart_type == "Pie Chart":
                fig = px.pie(data, names=data.columns[0], values=data.columns[1]    )
        
            st.plotly_chart(fig)
            
            # Download charts
            st.subheader("Download Chart")
            download_format = st.selectbox("Select Download Format", ["PNG", "SVG", "JPEG"])
            
            if download_format == "PNG":
                st.download_button(
                    label=f"Download {chart_type} as PNG",
                    data=fig.to_image(format="png"),
                    file_name=f"{chart_type.lower().replace(' ', '_')}_chart.png",
                    key="png-download"
                )
            elif download_format == "SVG":
                st.download_button(
                    label=f"Download {chart_type} as SVG",
                    data=fig.to_image(format="svg"),
                    file_name=f"{chart_type.lower().replace(' ', '_')}_chart.svg",
                    key="svg-download"
                )
            elif download_format == "JPEG":
                st.download_button(
                    label=f"Download {chart_type} as JPEG",
                    data=fig.to_image(format="jpeg"),
                    file_name=f"{chart_type.lower().replace(' ', '_')}_chart.jpeg",
                    key="jpeg-download"
                )

if __name__ == "__main__":
    main()
