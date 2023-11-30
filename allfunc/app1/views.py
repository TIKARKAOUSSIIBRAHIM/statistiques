import base64
import io
import os
from django.shortcuts import redirect, render
from django import forms
from matplotlib import figure
from requests import request
from .forms import FileUploadForm
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt

# Create your views here.
def index(request):
    return render(request, 'index.html')


def python(request):
    return render(request, 'python.html')

def fichierLirepython(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = request.FILES['file'].name  
            uploaded_file = form.cleaned_data['file']
            file_extension = os.path.splitext(file_name)[1]
            df = pd.read_csv(uploaded_file)
            request.session['my_df'] = df.to_dict()  

            return redirect('python') 
            # Redirect or render success message
             
    else:
        form = FileUploadForm()
    return render(request, 'fichier.html',{'form': form})

# def fichierLirepython(request):
#     df=None
#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)      
#         if form.is_valid():
#             file_name = request.FILES['file'].name  
#             uploaded_file = form.cleaned_data['file']
#             file_extension = os.path.splitext(file_name)[1]

#             if  file_extension == '.csv':
                
#                 df = pd.read_csv(uploaded_file)
                
#                 print("Uploaded file name:", uploaded_file.name)
#                 print("Uploaded file size:", uploaded_file.size)

#                 try:
                    
#                     print("Data read from CSV file:")
#                     print(df.head())
                
                    
#                 except Exception as e:
#                     print("Error reading file:", str(e))
                
#         else:
#             form = FileUploadForm()    
      
#     return render(request,'fichier.html',{'df':df})            

# views.py

def file_upload_view(request):
    
                df_dict = request.session.get('my_df')
                
                plot_url = None 
                plot = None 
    
    
                df = pd.DataFrame(df_dict)
    
                df_head=df.head()
                
                selected_graph = request.POST.get('graph')
                val1 = request.POST.get('val1')
                val2 = request.POST.get('val2')
                
                
                plt.figure()

            
                
                df_json = request.session.get('my_df')
                
                sns.set(style="whitegrid")
                if selected_graph == '1' : 
                          plot= sns.lineplot(x=val1,y=val2,data=df,markers='o')
                          plot.set_xlabel=val1
                          plot.set_ylabel=val2
                if selected_graph == '2' : 
                          plot = sns.scatterplot(x=val1, y=val2, data=df, marker='o', s=50)                          
                          plot.set_xlabel=val1
                          plot.set_ylabel=val2
                          
                if selected_graph == '3' : 
                          plot= sns.boxplot(x=val1,y=val2,data=df)
                          plot.set_xlabel=val1
                          plot.set_ylabel=val2
                if selected_graph == '4' : 
                          plot= sns.histplot(x=val1,data=df)  
                          plot.set_xlabel=val1
                if selected_graph == '5' : 
                          plot= sns.kdeplot(x=val1,data=df)     
                          plot.set_xlabel=val1  
                if selected_graph == '6' : 
                          plot= sns.violinplot(x=val1,data=df)   
                          plot.set_xlabel=val1  

                if selected_graph == '7' : 
                          plot= sns.barplot(x=val1,y=val2,data=df)  
                          plot.set_xlabel=val1
                          plot.set_ylabel=val2    
                if selected_graph == '8' : 
                          dff = df.select_dtypes(include=['number'])
                          correlation_matrix = dff.corr()
                          plot=sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
                          plt.title('Heatmap')
                if selected_graph == '9' : 
                          category_counts = df[val1].value_counts()
                          plot=plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)

    # Save the plot as an image  
               
               # Save the plot as an image (you can save it to a file or encode it as base64)
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()
                # Close all     Matplotlib figuliste to clear the state
                plt.close()
                # Encode the plot to base64
                plot_url = base64.b64encode(image_png).decode('utf-8')


          
    
                return render(request, 'python.html', {'plot_url': plot_url,'df_head':df_head}) 


def stats(request):
    liste = None
    tab = None
    name=None
    ligne=None
    lignes=None
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)      
        if form.is_valid():
            file_name = request.FILES['file'].name  
            uploaded_file = form.cleaned_data['file']
            file_extension = os.path.splitext(file_name)[1]

            if  file_extension == '.csv':
                df = pd.read_csv(uploaded_file)
                stats_values = request.POST.get('stats_values')
                ligne_a_afficher = request.POST.get('stats')
                ligne_f_afficher = request.POST.get('statsd')
                ligne_l_afficher = request.POST.get('statsf')
                
                if stats_values:
                    if stats_values == "1":
                        tab=df.head()
                        name="Les 5 premier lignes du fichier"
                    if stats_values == "2":
                        tab =df.tail()
                        name="Les 5 dernier lignes du fichier"
                    if stats_values == "3":
                        liste = df.columns.tolist()
                if ligne_a_afficher:
                        ligne=df.loc[int(ligne_a_afficher)]
                if ligne_f_afficher:
                        lignes=df.loc[int(ligne_f_afficher):int(ligne_l_afficher)]      
    else:  # For GET requests or initial render
        form = FileUploadForm()               
    
    
    return render(request, 'statistiques.html',{'form':form,'tab':tab, 'name':name,'liste':liste,'ligne':ligne, 'lignes':lignes})

