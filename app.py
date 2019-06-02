  # -*- coding: utf-8 -*-
"""
Created on Sun May  5 22:29:27 2019

@author: shiva
"""

from flask import Flask,render_template,Markup,request,redirect,url_for
import pandas as pd
import numpy as np
#from IPython.display import HTML

app=Flask(__name__)

states=['Jammu and Kashmir','Himachal Pradesh','Punjab','Chandigarh','Uttrakhand','Haryana',
'Delhi','Rajasthan','Uttar Pradesh','Bihar','Sikkim','Arunachal Pradesh','Nagaland','Manipur',
'Mizoram','Tripura','Meghalaya','Assam','West Bengal','Jharkhand','Odisha','Chhatisgarh',
'Madhya Pradesh','Gujarat','Daman & Diu','Dadra & Nagar Haveli','Maharashtra','Andhra Pradesh',
'Karnataka','Goa','Lakshadweep','Kerala','Tamil Nadu','Puducherry','Andaman & Nicobar Islands','Telangana'
]

accr_stud_density=['Medium','Very Low','High','Low']
unaccr_stud_density=['Medium','Very Low','High','Low']
accr_infra=['Satisfactory','Very Good','Bad','Good','Excellent']
unaccr_infra=['Satisfactory','Very Good','Good','Excellent','Bad']

users={'shivam@gmail.com':'shivam123','tejas@gmail.com':'tejas145','suyash@hotmail.com':'suyash789','laya@yahoo.com':'laya657'}


def accr_stud_density_not_req(df,accr,state_code,df_field,infra):
    if infra=='Not Required':
        #infra_code=accr_infra.index(infra)
        df=df[(df.state_code==state_code)&(df[df_field]==1)]
        df2=df.sort_values(['Total_Students','Accr_Score_Percentage','infrastructure_score','Total_Teachers'],ascending=False,inplace=False)
        df2=df2[['college_institution_id','name','city','autonomous','offers_scholarship','offers_loan','Accr_Score_Percentage','Total_Students']]
    else:
        infra_code=accr_infra.index(infra)
        df=df[(df.state_code==state_code)&(df.Infra_quality==infra_code)&(df[df_field]==1)]
        df2=df.sort_values(['Accr_Score_Percentage','Total_Students','infrastructure_score','Total_Teachers'],ascending=False,inplace=False)
        df2=df2[['college_institution_id','name','city','autonomous','offers_scholarship','offers_loan','Accr_Score_Percentage','Total_Students']]
    return df2

def accr_stud_density_req(df,accr,state_code,df_field,density,infra):
    if infra=='Not Required':
        density_code=accr_stud_density.index(density)
        #infra_code=accr_infra.index(infra)
        df=df[(df.state_code==state_code)&(df.Student_Density==density_code)&(df[df_field]==1)]
        df2=df.sort_values(['Accr_Score_Percentage','infrastructure_score','Total_Students','Total_Teachers'],ascending=False,inplace=False)
        df2=df2[['college_institution_id','name','city','autonomous','offers_scholarship','offers_loan','Accr_Score_Percentage','Total_Students']]
    else:
        density_code=accr_stud_density.index(density)
        infra_code=accr_infra.index(infra)
        df=df[(df.state_code==state_code)&(df.Infra_quality==infra_code)&(df.Student_Density==density_code)&(df[df_field]==1)]
        df2=df.sort_values(['Accr_Score_Percentage','infrastructure_score','Total_Students','Total_Teachers'],ascending=False,inplace=False)
        df2=df2[['college_institution_id','name','city','autonomous','offers_scholarship','offers_loan','Accr_Score_Percentage','Total_Students']]
    return df2

def unaccr_stud_density_not_req(df,state_code,df_field,infra):
    if infra=='Not Required':
        #infra_code=accr_infra.index(infra)
        df=df[(df.state_code==state_code)&(df[df_field]==1)]
        df2=df.sort_values(['infrastructure_score','Total_Students','Total_Teachers'],ascending=False,inplace=False)
        df2=df2[['college_institution_id','name','city','autonomous','offers_scholarship','offers_loan','Total_Students']]
    else:
        infra_code=unaccr_infra.index(infra)
        df=df[(df.state_code==state_code)&(df.Infra_quality==infra_code)&(df[df_field]==1)]
        df2=df.sort_values(['infrastructure_score','Total_Students','Total_Teachers'],ascending=False,inplace=False)
        df2=df2[['college_institution_id','name','city','autonomous','offers_scholarship','offers_loan','Total_Students']]
    return df2

def unaccr_stud_density_req(df,state_code,df_field,density,infra):
    if infra=='Not Required':
        density_code=unaccr_stud_density.index(density)
        #infra_code=accr_infra.index(infra)
        df=df[(df.state_code==state_code)&(df.Student_Density==density_code)&(df[df_field]==1)]
        df2=df.sort_values(['infrastructure_score','Total_Students','Total_Teachers'],ascending=False,inplace=False)
        df2=df2[['college_institution_id','name','city','autonomous','offers_scholarship','offers_loan','Total_Students']]
    else:
        density_code=unaccr_stud_density.index(density)
        infra_code=unaccr_infra.index(infra)
        df=df[(df.state_code==state_code)&(df.Infra_quality==infra_code)&(df.Student_Density==density_code)&(df[df_field]==1)]
        df2=df.sort_values(['infrastructure_score','Total_Students','Total_Teachers'],ascending=False,inplace=False)
        df2=df2[['college_institution_id','name','city','autonomous','offers_scholarship','offers_loan','Total_Students']]
    return df2


@app.route('/')
def login():
    return render_template('login.html')
    
@app.route('/home',methods=['GET','POST'])
def home():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['pass']
        if email in users and password==users[email]:
            return render_template('index.html')
        else:
            return redirect(url_for('login'))


@app.route('/result',methods=['GET','POST'])
def result():
    if request.method=='POST':
        accr=(request.form['accredtion'])
        state=request.form['state']
        state_code=states.index(state)+1
        field=request.form['field']
        split_field=field.split(' ')
        df_field='c_'+'_'.join(split_field)
        density=request.form['density']
        infra=request.form['infra']
        if accr=='Yes':
            df=pd.read_csv('accr_clg_custer.csv')
            df2=pd.DataFrame()
            if density=='Not Required':
                #density_code=accr_stud_density.index(density)
                df2=accr_stud_density_not_req(df,accr,state_code,df_field,infra)
            else:
                df2=accr_stud_density_req(df,accr,state_code,df_field,density,infra)
            if df2.empty:
                return render_template('result.html',df='Sorry!! No Results Found')
            else:
                return render_template('result.html',df=Markup(df2.to_html(index=False)))
        
        else:
            df=pd.read_csv('unaccr_clg_custer.csv')
            df2=pd.DataFrame()
            if density=='Not Required':
                #density_code=accr_stud_density.index(density)
                df2=unaccr_stud_density_not_req(df,state_code,df_field,infra)
                    
            else:
                df2=unaccr_stud_density_req(df,state_code,df_field,density,infra)
            if df2.empty:
                return render_template('result.html',df='Sorry!! No Results Found')
            else:
                return render_template('result.html',df=Markup(df2.to_html(index=False)))
        

if __name__=="__main__":
    app.run()