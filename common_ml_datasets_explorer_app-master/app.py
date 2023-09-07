import os
import streamlit as st
import warnings

# EDA Pkgs
import pandas as pd 

# Viz Pkgs
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')
import seaborn as sns 

def main():
	warnings.filterwarnings("ignore", category=DeprecationWarning, message="Some specific warning message")
	st.set_option('deprecation.showPyplotGlobalUse', False)
	# """ Common ML Dataset Explorer """
	st.title("DataGlimpze")
	st.subheader("Select a Dataset and get analysis!!")

	html_temp = """
	<div style="background-color:tomato;"><p style="color:white;font-size:50px;padding:10px">Data Visualisation made easy</p></div>
	"""
	st.markdown(html_temp,unsafe_allow_html=True)

	uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
	for uploaded_file in uploaded_files:
		bytes_data = uploaded_file.read()
		st.write("filename:", uploaded_file.name)
		st.write(bytes_data)

	def file_selector(folder_path=r'C:\Users\KIIT\Downloads\common_ml_datasets_explorer_app-master\common_ml_datasets_explorer_app-master\datasets'):
	# def file_selector(folder_path=r"C:\Users\KIIT\Downloads\common_ml_datasets_explorer_app-master\common_ml_datasets_explorer_app-master\datasets"):
		filenames = os.listdir(folder_path)
		selected_filename = st.selectbox("Select A file",filenames)
		return os.path.join(folder_path,selected_filename)

	filename = file_selector()
	st.info("You Selected {}".format(filename))
	# st.info("You Selected {}".format(selected_filename))


	# Read Data
	df = pd.read_csv(filename)
	# Show Dataset

	if st.checkbox("Show Dataset"):
		number = st.number_input("Number of Rows to View")
		st.dataframe(df.head(number))

	# Show Columns
	if st.button("Column Names"):
		st.write(df.columns)

	# Show Shape
	if st.checkbox("Shape of Dataset"):
		data_dim = st.radio("Show Dimension By ",("Rows","Columns"))
		if data_dim == 'Rows':
			st.text("Number of Rows")
			st.write(df.shape[0])
		elif data_dim == 'Columns':
			st.text("Number of Columns")
			st.write(df.shape[1])
		else:
			st.write(df.shape)

	# Select Columns
	if st.checkbox("Select Columns To Show"):
		all_columns = df.columns.tolist()
		selected_columns = st.multiselect("Select",all_columns)
		new_df = df[selected_columns]
		st.dataframe(new_df)
	
	# Show Values
	if st.button("Value Counts"):
		st.text("Value Counts By Target/Class")
		st.write(df.iloc[:,-1].value_counts())


	# Show Datatypes
	if st.button("Data Types"):
		st.write(df.dtypes)



	# Show Summary
	if st.checkbox("Summary"):
		st.write(df.describe().T)

	## Plot and Visualization

	st.subheader("Data Visualization")
	# Correlation
	# Seaborn Plot
	if st.checkbox("Correlation Plot[Seaborn]"):
		st.write(sns.heatmap(df.corr(),annot=True))
		st.pyplot()

	
	# Pie Chart
	if st.checkbox("Pie Plot"):
		all_columns_names = df.columns.tolist()
		if st.button("Generate Pie Plot"):
			st.success("Generating A Pie Plot")
			st.write(df.iloc[:,-1].value_counts().plot.pie(autopct="%1.1f%%"))
			st.pyplot()

	# Count Plot
	if st.checkbox("Plot of Value Counts"):
		st.text("Value Counts By Target")
		all_columns_names = df.columns.tolist()
		primary_col = st.selectbox("Primary Columm to GroupBy",all_columns_names)
		selected_columns_names = st.multiselect("Select Columns",all_columns_names)
		if st.button("Plot"):
			st.text("Generate Plot")
			if selected_columns_names:
				vc_plot = df.groupby(primary_col)[selected_columns_names].count()
			else:
				vc_plot = df.iloc[:,-1].value_counts()
			st.write(vc_plot.plot(kind="bar"))
			st.pyplot()


	# Customizable Plot

	st.subheader("Customizable Plot")
	all_columns_names = df.columns.tolist()
	type_of_plot = st.selectbox("Select Type of Plot",["area","bar","line","hist","box","kde"])
	selected_columns_names = st.multiselect("Select Columns To Plot",all_columns_names)

	if st.button("Generate Plot"):
		st.set_option('deprecation.showPyplotGlobalUse', False)
		st.success("Generating Customizable Plot of {} for {}".format(type_of_plot,selected_columns_names))
		# st.set_option('deprecation.showPyplotGlobalUse', False)

		# Plot By Streamlit
		if type_of_plot == 'area':
			cust_data = df[selected_columns_names]
			st.area_chart(cust_data)

		elif type_of_plot == 'bar':
			cust_data = df[selected_columns_names]
			st.bar_chart(cust_data)

		elif type_of_plot == 'line':
			cust_data = df[selected_columns_names]
			st.line_chart(cust_data)

		# Custom Plot 
		elif type_of_plot:
			cust_plot= df[selected_columns_names].plot(kind=type_of_plot)
			st.write(cust_plot)
			st.pyplot()

	if st.button("Thanks"):
		st.balloons()


	st.sidebar.header("About App")
	st.sidebar.info("Working with raw unprocessed datasets, which are in the form of huge csv files can be confusing and making sense of these big files is a tedious task for a beginner."
					"With DataGlimpze, just select your dataset, and comlpex data visualisation will be on your fingertips! ")

	st.sidebar.header("Get Datasets")
	# st.sidebar.markdown("[Common ML Dataset Repo]("")")
	st.sidebar.markdown("[Common ML Dataset Repo](https://www.kaggle.com/datasets)")

	st.sidebar.header("How?")
	st.sidebar.info("Choose/upload dataset -> analyse!")

	# st.sidebar.header("By:")
	# st.sidebar.info("Swati Mishra")



if __name__ == '__main__':
	main()
