import pickle
path=r'D:\Projects\tickets\daimai\cookies.pkl'#pkl文件所在路径
	   
f=open(path,'rb')
data=pickle.load(f,encoding='latin1')
 
print(data)