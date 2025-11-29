import streamlit as st
import pandas as pd
import numpy as np
import json
import csv
import pymysql

conn=pymysql.connect(
    host='localhost',
    user='root',
    password='M@h!UV127',
    database="customer_data"
)

cursor=conn.cursor()
print("PyMySQL connection established") 


r=st.sidebar.radio('Select:',['Project Introduction','View Tables','Filter Table Data','CRUD Operations','Credit/Debit Details','Analytical Insights','About Creator'])

if r=='Project Introduction':
    st.title("🏦BANK SIGHT: Transaction Intelligence Dashboard")
    st.image("ChatGPT Image Nov 28, 2025, 02_52_11 PM.png")
    st.header("Project Overview")
    st.text("Banksight is a basic financial analytical system built using Python, Streamlit, MySQL and Visual Studio Code. It allows end user to view the account details, transactions, customer details, loan details, tickets details for resolution any bank related issues.")
    st.subheader('''
    Objectives:
             
    Understand customer and transaction behaviour            
    Enable CRUD operations for all datasets                 
    Analyse the account details, customer info and transaction summary  
    View the supporting ticket details raised for resolution of issues  
    Get insights of loan and credit card details for various bank branches                                                               
 '''
 )
    st.subheader('''
    Dataset References:
                 

    **Customers:** contains core demographic details and primary account type for bank customers  
    **Account Balance:** contains the latest account balance information linked to each customer  
    **Transactions:** contains a detailed log of all transactions conducted by customers  
    **Loans:** contains details for various types of loans issued by the bank  
    **Credit Card:** contains details for all credit cards associated with bank accounts  
    **Branches:** contains detailed information about branches of each bank.  
    **Support Tickets:** contains records of customer service interactions, issue details, resolution status
'''
)

if r=='View Tables':
    st.header("📊View Database Tables")
    read=st.selectbox("Select a Table:",['customers','accounts','branches','transactions','loans','credit_cards','support_tickets'])
    df=pd.read_sql_query(f"select * from {read}",conn)
    st.write(df)

   
    

if r=='About Creator':
    st.header("👨‍💼My Intro:")
    st.write('''           
    **Name:** Prabhu Madari         
    **Role:** Data Science Specailist          
    **Expertise:** SQL, Python, StreamLit, Pandas, NumPy  
    **Email:** mahanteshprabhu@gmail.com
    
             
     *Project developed as part of the Bank Sight Analytics Initiative to demonstrate and display the user details.*         
    ''')



    

if r=='Analytical Insights':
  st.header("🧠Analytical Insights:")
  ques=st.selectbox(
  'Select a question:',
   ['Q1: How many customers exist per city, and what is their average account balance?',
    'Q2: Which account type (Savings, Current, Loan, etc.) holds the highest total balance?',
    'Q3: Who are the top 10 customers by total account balance across all account types?',
    'Q4: Which customers opened accounts in 2023 with a balance above ₹1,00,000?',
    'Q5: What is the total transaction volume (sum of amounts) by transaction type?',
    'Q6: How many failed transactions occurred for each transaction type?',
    'Q7: What is the total number of transactions per transaction type?',
    'Q8: Which accounts have 5 or more high-value transactions above ₹20,000?',
    'Q9: What is the average loan amount and interest rate by loan type (Personal, Auto, Home, etc.)?',
    'Q10: Which customers currently hold more than one active or approved loan?',
    'Q11: Who are the top 5 customers with the highest outstanding (non-closed) loan amounts?',
    'Q12: Which branch holds the highest total account balance?',
    'Q13: What is the branch performance summary showing total customers, total loans, and transaction volume?',
    'Q14: Which issue categories have the longest average resolution time?',
    'Q15: Which support agents have resolved the most critical tickets with high customer ratings (≥4)?',
    'Q16: List out the 10 managers who has highest number of employees alloted?',
    'Q17: Display the branch details of highest and lowest branch revenue generated',
    'Q18: What is the best mode of communication utilized to resolve the issue?',
    'Q19: List out the details of maximum amount deposited and withdrawn?',
    'Q20: Which branch lent the highest loan amount?',
    'Q21: What is the loan category where highest amount is lent?',
    'Q22: List out the number of customers according to the category of accounts?',
    'Q23: What is the performance rating received for the maximum number of customers?',
    'Q24: List out the status of credit card holders across all branches',
    'Q25: Who is the 1st customer registered in the customers list?'])
    



  if ques=='Q1: How many customers exist per city, and what is their average account balance?':
    st.dataframe(pd.read_sql_query("select c.city, count(c.customer_id) as 'customer per city', avg(a.account_balance) as 'average account balance' from customers as c left join accounts as a on a.customer_id=c.customer_id group by city",conn))
  if ques=='Q2: Which account type (Savings, Current, Loan, etc.) holds the highest total balance?':
    st.dataframe(pd.read_sql_query("SELECT c.account_type, ROUND(SUM(account_balance),2) AS 'total_balance' FROM customers AS c LEFT JOIN accounts AS a ON c.customer_id=a.customer_id GROUP BY account_type ORDER BY total_balance DESC LIMIT 1",conn))
  if ques=='Q3: Who are the top 10 customers by total account balance across all account types?':
    st.dataframe(pd.read_sql_query("select c.name, sum(a.account_balance) as 'total_balance' from customers as c left join accounts as a on c.customer_id=a.customer_id group by name order by total_balance desc limit 10",conn)) 
  if ques=='Q4: Which customers opened accounts in 2023 with a balance above ₹1,00,000?':
    st.dataframe(pd.read_sql_query("select c.name, a.account_balance, c.join_date from customers as c left join accounts as a on c.customer_id=a.customer_id where account_balance>100000 and join_date>'2022-12-31'",conn))
  if ques=='Q5: What is the total transaction volume (sum of amounts) by transaction type?':
    st.dataframe(pd.read_sql_query("select txn_type as 'Transaction type', sum(amount) as 'Total transaction volume' from transactions group by txn_type",conn))
  if ques=='Q6: How many failed transactions occurred for each transaction type?':
    st.dataframe(pd.read_sql_query("select txn_type, count(status) from transactions where status='failed' group by txn_type",conn))
  if ques=='Q7: What is the total number of transactions per transaction type?':
    st.dataframe(pd.read_sql_query("select txn_type, count(txn_id) from transactions group by txn_type",conn))
  if ques=='Q8: Which accounts have 5 or more high-value transactions above ₹20,000?':
    st.dataframe(pd.read_sql_query("select c.name, sum(t.amount) as 'total' from customers as c left join transactions as t on c.customer_id=t.customer_id where amount>20000 group by name",conn))
  if ques=='Q9: What is the average loan amount and interest rate by loan type (Personal, Auto, Home, etc.)?':
    st.dataframe(pd.read_sql_query("select loan_type, round(avg(loan_amount),2) as 'average_amount', round(avg(interest_rate),2) as 'average_rate' from loans group by loan_type",conn))
  if ques=='Q10: Which customers currently hold more than one active or approved loan?':
    st.dataframe(pd.read_sql_query("select customer_id, count(loan_status) as 'total' from loans where loan_status in ('active', 'approved') group by customer_id having total>1",conn))
  if ques=='Q11: Who are the top 5 customers with the highest outstanding (non-closed) loan amounts?':
    st.dataframe(pd.read_sql_query("select customer_id, loan_amount from loans where loan_status='Defaulted' order by loan_amount desc limit 5",conn))
  if ques=='Q12: Which branch holds the highest total account balance?':
    st.dataframe(pd.read_sql_query("select b.branch_name from branches as b left join accounts as a on b.branch_id=a.customer_id group by branch_name order by sum(account_balance) desc limit 1",conn))
  if ques=='Q13: What is the branch performance summary showing total customers, total loans, and transaction volume?':
    st.dataframe(pd.read_sql_query("select (select count(distinct customer_id) from transactions) as 'total_customers', (select count(distinct loan_id) from loans) as 'total_loans', (select round(sum(amount),2) from transactions) as 'transaction_volume'",conn))
  if ques=='Q14: Which issue categories have the longest average resolution time?':
    st.dataframe(pd.read_sql_query("select issue_category, avg(datediff(date_closed, date_opened)) as 'resolution_time' from support_tickets group by issue_category order by resolution_time desc",conn))
  if ques=='Q15: Which support agents have resolved the most critical tickets with high customer ratings (≥4)?':
    st.dataframe(pd.read_sql_query("select distinct support_agent from support_tickets where priority='Critical' and customer_rating>=4",conn))
  if ques=='Q16: List out the 10 managers who has highest number of employees alloted?':
    st.dataframe(pd.read_sql_query("select distinct manager_name, sum(total_employees) as 'total' from branches group by manager_name order by total desc limit 10;",conn))
  if ques=='Q17: Display the branch details of highest and lowest branch revenue generated':
    st.dataframe(pd.read_sql_query("select max(branch_revenue) as 'maximum', min(branch_revenue) as 'minimum' from branches",conn))
  if ques=='Q18: What is the best mode of communication utilized to resolve the issue?':
    st.dataframe(pd.read_sql_query("select channel, count(channel) as total_cases from support_tickets group by channel order by count(channel) desc limit 1",conn))
  if ques=='Q19: List out the details of maximum amount deposited and withdrawn?':
    st.dataframe(pd.read_sql_query("select txn_type, amount, txn_time from transactions where txn_type in ('deposit', 'withdrawal') order by amount desc limit 2",conn))
  if ques=='Q20: Which branch lent the highest loan amount?':
    st.dataframe(pd.read_sql_query("select branch, sum(loan_amount) as 'total_lent_amount' from loans group by branch order by total_lent_amount desc limit 1",conn))
  if ques=='Q21: What is the loan category where highest amount is lent?':
    st.dataframe(pd.read_sql_query("select loan_type, sum(loan_amount) from loans group by loan_type order by sum(loan_amount) desc limit 1",conn))
  if ques=='Q22: List out the number of customers according to the category of accounts?':
    st.dataframe(pd.read_sql_query("select account_type, count(customer_id) as 'total_accounts' from customers group by account_type order by total_accounts",conn))
  if ques=='Q23: What is the customer rating received for the maximum number of customers?':
    st.dataframe(pd.read_sql_query("select customer_rating, count(ticket_id) as 'total_tickets' from support_tickets group by customer_rating order by total_tickets desc limit 1",conn))
  if ques=='Q24: List out the status of credit card holders across all branches':
    st.dataframe(pd.read_sql_query("select status, count(card_id) as 'total_cards' from credit_cards group by status order by total_cards",conn))
  if ques=='Q25: Who is the 1st customer registered in the customers list?':
    st.dataframe(pd.read_sql_query("select name from customers where customer_id='C0001'",conn ))


if r=='Filter Table Data':
  st.header("🔎Filter Data:")
  filt=['customers','accounts','branches','transactions','loans','credit_cards','support_tickets']
  table=st.selectbox("Select table to filter",filt)
  df=pd.read_sql_query(f"select * from {table}",conn)
  st.write("Select columns and values to filter:")
  filters = {} 
  for col in df.columns:
    
    unique_vals = df[col].dropna().unique().tolist()
    selected_vals = st.multiselect(f"{col}:", unique_vals)
    if selected_vals:
     filters[col] = selected_vals

  if filters:
    for k, v in filters.items():
      df = df[df[k].isin(v)]
  st.success("✅ Data filtered successfully!")   
  st.write(df)

  
if r=='Credit/Debit Details':
  st.header("💰Deposit/Withdraw money")
  aa=st.text_input("Enter Account ID:")
  bb=st.number_input("Enter amount(₹)")
  act=st.radio("Select action:",['Check balance', 'Deposit','Withdraw'])
  if act=='Check balance':
    dq1=pd.read_sql_query(f"select account_balance from accounts where customer_id='{aa}'",conn)
    if dq1.empty:
      st.warning("Please enter any value")
    elif st.button("Submit"): 
     act_bal=(dq1.iloc[0]['account_balance']) 
     st.info(act_bal)
    

  if act=='Deposit':
    dq1=pd.read_sql_query(f"select account_balance from accounts where customer_id='{aa}'",conn)
    if dq1.empty:
      st.warning("Please enter any value")
    else:  
     act_bal=(dq1.iloc[0]['account_balance']) 
     rev_bal=act_bal+bb
     updq="UPDATE accounts SET account_balance=%s where customer_id=%s"
     cursor.execute(updq, (rev_bal,{aa}))   
     conn.commit()
    if st.button("Submit"):
      st.info(rev_bal)
    

  if act=='Withdraw':
    
     dq1=pd.read_sql_query(f"select account_balance from accounts where customer_id='{aa}'",conn)
     if dq1.empty:
      st.warning("Please enter any value")
     else:
      act_bal=(dq1.iloc[0]['account_balance']) 
      rev_bal=act_bal-bb
      updq=("UPDATE accounts SET account_balance=%s where customer_id=%s")
      cursor.execute(updq, (rev_bal,{aa}))   
      conn.commit()
     if st.button("Submit"):
      st.info(rev_bal)
     
    
  
    
           

if r=='CRUD Operations':
  st.header("✒CRUD Operations:")
  filt=['customers','accounts','branches','transactions','loans','credit_cards','support_tickets']
  table=st.selectbox("Select table to filter",filt)
  df=pd.read_sql_query(f"select * from {table}",conn)
  df1=st.radio("Select Operation:",['View','Add','Update','Delete'])
  
  if df1=='View':
    st.write(df)
  if df1=='Add':
    st.subheader(f"➕Add new record to {table}")
    df2=pd.read_sql_query(f"select * from {table} limit 1",conn)
    new_data={}
    for col in df.columns:
      new_data[col]=st.text_input(f"Enter {col}")
    if st.button("Add Record"):
      try:
        columns=','.join(new_data.keys())
        placeholders=','.join(['%s']*len(new_data))
        values = list(new_data.values())
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"     
        cursor.execute(query, values)
        conn.commit()
        st.success('✅ Added successfully')
      except Exception as e:
        st.error(f"Error: {e}")  

  if df1=='Update':
    st.subheader(f"🔼Update record in {table}")
    df2=pd.read_sql_query(f"select * from {table} limit 1",conn)
    primary_key = df.columns[0]
    record_id = st.selectbox(f"Select {primary_key} to update", df[primary_key].unique())
    update_col = st.selectbox("Select Column to Update", df.columns)
    new_val = st.text_input("Enter New Value")
    if st.button("Update Record"):
        cursor.execute(f"UPDATE {table} SET {update_col}= %s WHERE {primary_key}=%s", (new_val, record_id))
        conn.commit()
        st.success("✅ Record updated successfully!")

  if df1=='Delete':
    st.subheader(f"🧺Delete record from {table}")
    primary_key = df.columns[0]
    record_id = st.selectbox(f"Select {primary_key} to delete", df[primary_key].unique())
    if st.button("Delete Record"):
      cursor.execute(f"delete from {table} where {primary_key}=%s", (record_id))
      conn.commit()
      st.success("Record deleted successfully!")    