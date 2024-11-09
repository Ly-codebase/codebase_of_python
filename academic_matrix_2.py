import pandas as pd
import csv
import os 

#先创建read_csv_cell函数以便读取文件中指定的行和列的数据
#（h指数、起止年月、作者id）
def read_csv_cell(file_path,row_index,col_index):
	row_data=[]
	with open(file_path,mode='r',newline='',encoding='UTF-8') as csv_file:
		#创建一个 csv.reader 对象读取csv数据
		csv_reader=csv.reader(csv_file)
		for row_idx,row in enumerate(csv_reader):
			if row_idx==row_index:
				if 0<=col_index<len(row):
					return row[col_index]
				else:
					return None #表示列索引超出范围
		return None #表示行索引超出范围


#创建计算学术迹的函数
def get_academic_matrix(file_path,h_index):
	#从第13行开始读取csv文件
	df=pd.read_csv(file_path,header=12,names=['文献顺序', '引文', '标题'])
	#适应文件格式进行切片计算，从第15行开始
	df_from_15th_row = df.iloc[14:] 
	#发文总数P
	P= df_from_15th_row['引文'].count()
	#引文总数C
	C= df_from_15th_row['引文'].sum()
	#零引文章数P_z
	P_z = df_from_15th_row[df_from_15th_row['引文'] == 0]['引文'].count()
	#h-core文章数
	P_c = df_from_15th_row[df_from_15th_row['引文'] <= h_index]['引文'].count()
	#h-tail文章被引数
	C_t = h_index**2
	#h—core文章被引数
	C_e = df_from_15th_row[df_from_15th_row['引文']>= h_index]['引文'].sum()-C_t 
	#计算学术矩阵的迹T
	T=P_c**2/P + C_t**2/C + C_e**2/C - P_z**2/P
	return T

#创建计算p指数的函数
def get_p_value(file_path):
	#从第13行开始读取csv文件
	df=pd.read_csv(file_path,header=12,names=['文献顺序', '引文', '标题'])
	#适应文件格式进行切片计算，从第15行开始
	df_from_15th_row = df.iloc[14:]
	#发文总数P
	P= df_from_15th_row['引文'].count()
	#引文总数C
	C= df_from_15th_row['引文'].sum()
	#计算p指数
	P_value=(C**2/P)**(1/3)
	return P_value

# 修改csv文件的文件夹路径  
folder_path = "D:/edge下载/parts_of_data_ly"
# 获取文件夹中的所有Excel文件  
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv') ]
# 初始化一个空的DataFrame来存储合并计算后的数据  
combined_df = pd.DataFrame()
# 遍历所有csv文件并合并它们  
for file in csv_files:  
	file_path = os.path.join(folder_path, file)  
	try:
		# 读取csv文件 
		df = pd.read_csv(file_path,header=12,names=['文献顺序', '引文', '标题'])
		#读取h指数
		h_index=int(read_csv_cell(file_path,5,1))
		#读取作者姓名
		author_name=read_csv_cell(file_path,2,1)
		#读取作者scopus_id
		scopus_id=read_csv_cell(file_path,3,1)
		#读取文献起始计数年份
		start_year=read_csv_cell(file_path,7,1)
		#读取文献结束计数年份
		end_year=read_csv_cell(file_path,8,1)
		#计算学术迹T
		T = get_academic_matrix(file_path,h_index)
		#计算P_value
		P_value=get_p_value(file_path);
		data = {  
			'Scopus ID': [scopus_id],   
		    'Author Name': [author_name],   
		    'Start Year': [start_year],  
		    'End Year': [end_year], 
		    'H-Index': [h_index], 
		    'Academic Trace (T)': [T],
		    'P_value':[P_value]  
		}  
		df = pd.DataFrame(data) 
		# 将读取到的DataFrame追加到combined_df中 
		combined_df = pd.concat([combined_df, df], ignore_index=True) 
	except Exception as e:
		print(f"Error processing file {file}: {e}")

# 指定新的Excel文件的路径  
excel_file_path = 'result_file.xlsx'   
# 使用pandas的to_excel方法将数据写入Excel文件  
combined_df.to_excel(excel_file_path, index=False)  # index=False表示不写入DataFrame的索引  

print(f"Data has been written to {excel_file_path}")