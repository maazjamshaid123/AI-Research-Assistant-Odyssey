import streamlit as st
import pandas as pd
import plotly.express as px
from skimage import io 
import numpy as np
import plotly.graph_objects as go

def show_analysis():
    st.title("_Astronomical Analysis_")

    st.markdown("---")
 
    with open("image.jpg", "rb") as file:
        btn = st.download_button(
                label="Sample Image",
                data=file,
                file_name="Black Hole M87.jpg",
                mime="image/jpg")
    # with col2:
    def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = pd.read_csv("data.csv", index_col=None)
    csv = convert_df(csv)
    st.download_button(
    label="Sample CSV",
    data=csv,
    file_name='Black Holes.csv',
    mime='text/csv',)

    def plot_data(data, plot_type, x_col, y_col=None, z_col=None, scatter_matrix_cols=None):
        if plot_type == 'Scatter':
            fig = px.scatter(data, x=x_col, y=y_col)
        elif plot_type == 'Color-Color':
            fig = px.scatter(data, x=x_col, y=y_col, color=z_col)
        elif plot_type == 'Line':
            fig = px.line(data, x=x_col, y=y_col)
        elif plot_type == 'Light Curve':
            fig = px.line(data, x=x_col, y=y_col, color=z_col)
        elif plot_type == 'Bar':
            fig = px.bar(data, x=x_col, y=y_col)
        elif plot_type == 'Horizontal Bar':
            fig = px.bar(data, x=x_col, y=y_col, color=z_col, orientation='h')
        elif plot_type == 'Histogram':
            fig = px.histogram(data, x=x_col)
        elif plot_type == 'Density Heatmap':
            fig = px.density_heatmap(data, x=x_col, y=y_col,color_continuous_scale="Viridis")
        elif plot_type == '3D Scatter':
            fig = px.scatter_3d(data, x=x_col, y=y_col, z=z_col, color=z_col)
        elif plot_type == 'PCA Analysis':
            fig = px.scatter_matrix(data, dimensions=scatter_matrix_cols, color=z_col)
        elif plot_type == 'Analyze Image':
            fig = px.imshow(data)
        elif plot_type == 'Contour Plot':
            fig = px.density_contour(data, x=x_col, y=y_col, z=z_col)
        elif plot_type == 'Surface Plot with Contours':
                    fig = go.Figure(data=[go.Surface(z=data[z_col].values.reshape(data[x_col].nunique(), data[y_col].nunique()))])
                    fig.add_trace(go.Contour(z=data[z_col].values.reshape(data[x_col].nunique(), data[y_col].nunique()),
                                            x=data[x_col].unique(),
                                            y=data[y_col].unique(),
                                            contours=dict(coloring='lines', showlabels=True, labelfont=dict(size=12))))
        st.plotly_chart(fig)

    def main():
        file = st.file_uploader("Upload a file to get started", type=["csv", "xlsx", "jpg", "jpeg", "png"])
        if file is not None:
            if file.name.endswith('.csv'):
                data = pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                data = pd.read_excel(file, engine='openpyxl')
            elif file.name.endswith('.jpg') or file.name.endswith('.jpeg') or file.name.endswith('.png'):
                data = io.imread(file)
                data = px.imshow(data, width=1000, height=700)
            st.subheader("Data:")
            st.write(data)

            if file.name.endswith('.csv') or file.name.endswith('.xlsx'):
                plot_type = st.selectbox("Select Plot Type", ["Scatter", "Color-Color", "Line", "Light Curve", "Bar", "Horizontal Bar", "Histogram", "Density Heatmap", "PCA Analysis", "Contour Plot", "Surface Plot with Contours", "3D Scatter"])
                if plot_type == '3D Scatter':
                    x_col = st.selectbox("Select 1st Feature", data.columns)
                    y_col = st.selectbox("Select 2nd Feature", data.columns)
                    z_col = st.selectbox("Select 3rd Feature", data.columns)
                elif plot_type == 'Color-Color':
                    x_col = st.selectbox("Select 1st Feature", data.columns)
                    y_col = st.selectbox("Select 2nd Feature", data.columns)
                    z_col = st.selectbox("Select 3rd Feature", data.columns)
                elif plot_type == 'Light Curve':
                    x_col = st.selectbox("Select 1st Feature", data.columns)
                    y_col = st.selectbox("Select 2nd Feature", data.columns)
                    z_col = st.selectbox("Select 3rd Feature", data.columns)
                elif plot_type == 'Horizontal Bar':
                    x_col = st.selectbox("Select 1st Feature", data.columns)
                    y_col = st.selectbox("Select 2nd Feature", data.columns)
                    z_col = st.selectbox("Select 3rd Feature", data.columns)
                elif plot_type == 'Histogram':
                    x_col = st.selectbox("Select 1st Feature", data.columns)
                    y_col = None
                    z_col = None
                elif plot_type == 'PCA Analysis':
                    features = st.multiselect("Select Features", data.columns)
                    x_col = None
                    y_col = None
                    z_col = st.selectbox("Select 3rd Feature", data.columns)
                elif plot_type == 'Contour Plot':
                    x_col = st.selectbox("Select 1st Feature", data.columns)
                    y_col = st.selectbox("Select 2nd Feature", data.columns)
                    z_col = st.selectbox("Select 3rd Feature", data.columns)
                elif plot_type == 'Surface Plot with Contours':
                    x_col = st.selectbox("Select 1st Feature", data.columns)
                    y_col = st.selectbox("Select 2nd Feature", data.columns)
                    z_col = st.selectbox("Select 3rd Feature", data.columns)
                else:
                    x_col = st.selectbox("Select 1st Feature", data.columns)
                    y_col = st.selectbox("Select 2nd Feature", data.columns)
                    z_col = None

                if x_col is not None:
                    if data[x_col].dtype in [float, int]:
                        if st.checkbox("Log 1st Feature"):
                            data[x_col] = np.log10(data[x_col]+1)

                if y_col is not None:
                    if data[y_col].dtype in [float, int]:
                        if st.checkbox("Log 2nd Feature"):
                            data[y_col] = np.log10(data[y_col]+1)

                if z_col is not None:
                    if data[z_col].dtype in [float, int]:
                        if st.checkbox("Log 3rd Feature"):
                            data[z_col] = np.log10(data[z_col]+1)

                if plot_type == 'PCA Analysis':
                    if features is not None:
                        scatter_matrix_cols = [col for col in data.columns if col in features]
                        plot_data(data, plot_type, None, None, z_col, scatter_matrix_cols)
                if plot_type == 'Surface Plot with Contours':
                    fig = go.Figure(data=[go.Surface(x=data[x_col], y=data[y_col], z=data[z_col])])
                    fig.update_traces(contours_z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True))
                    st.plotly_chart(fig)
                else:
                    plot_data(data, plot_type, x_col, y_col, z_col)
                    
    main()

