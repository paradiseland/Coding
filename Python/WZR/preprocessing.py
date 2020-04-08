import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

credit = pd.read_csv("Credit.csv")


# credit[credit.isnull().values==True]
# ind = credit[credit.isnull().values==True].index
# # get 
# credit.isnull().any()
# credit_null = credit.iloc[ind]
# credit_null["MONTHLY_INCOME_WHITHOUT_TAX"] == "exception"

# ind = credit[credit.isnull().values==True].index
# del na rows
credit = credit.dropna(how='any')


# delete monthly income <1500 and >150000
# credit.drop((credit['MONTHLY_INCOME_WHITHOUT_TAX']<1500) & (credit['MONTHLY_INCOME_WHITHOUT_TAX']>150000))
# AGE  range[18:67]
# 18-25 26-35 36-55 55-

age = sorted(np.array(credit['AGE']).tolist())




# credit['AGE'] = pd.cut(credit['AGE'],[18,25,35,55,70],labels=[])
credit['AGE'] = pd.cut(credit['AGE'],[18,25,35,55,70],labels=["18-25","26-35","36-55",">56"])
age_to_factor = dict(zip(["18-25","26-35","36-55",">56"], [0,1,2,3]))
credit['AGE'] = credit['AGE'].map(age_to_factor)



# GENDER 2 factors
credit["GENDER"].value_counts()
gender_to_factor = dict(zip(['Female', 'Male'], [1, 0]))
credit['GENDER'] = credit['GENDER'].map(gender_to_factor)
# MARITAL_STATUS 4 factors

credit["MARITAL_STATUS"].value_counts()
marital_to_factor = dict(zip(['Single','Married','Unknown','Divorce'], [0,1,2,3]))
credit["MARITAL_STATUS"] = credit["MARITAL_STATUS"].map(marital_to_factor)

# loan type 2 factors
credit["LOANTYPE"].value_counts()
loantype_to_factor = dict(zip(['Frist-Hand', 'Second-Hand'], [0,1]))
credit["LOANTYPE"] = credit["LOANTYPE"].map(loantype_to_factor)


# payment type 2 factors
credit["PAYMENT_TYPE"].value_counts()
paytype_to_factor = dict(zip(['Average_Capital_Plus_Interest_Repayment','Matching_The_Principal_Repayment'],[0,1]))
credit['PAYMENT_TYPE'] = credit['PAYMENT_TYPE'].map(paytype_to_factor)
# apply term time
credit["APPLY_TERM_TIME"].value_counts()

apply_term_to_factor = dict(zip([60,120,180,240,300,360], [0,1,2,3,4,5]))
credit['APPLY_TERM_TIME'] = credit['APPLY_TERM_TIME'].map(apply_term_to_factor)
# MONTHLY_INCOME
# credit['monthly_income'] = pd.cut(credit['MONTHLY_INCOME_WHITHOUT_TAX'],[0, 1500, 10000, 30000, 100000, 100000000],labels=["0-1500", "1500—10000","10000-20000","20000-100000","100000-inf"])

# # GAGE_TOTLE_PRICE
# credit['gage_totle_class'] = pd.cut(credit['GAGE_TOTLE_PRICE'],[0, 500000, 1000000, 2000000, 5000000,100000000000],labels=["0-500,000", "500,000—1,000,000","1,000,000-2,000,000","2,000,000-5,000,000","5,000,000-inf"])

# # APPLY_AMOUNT
# credit['apply_amount_class'] = pd.cut(credit['APPLY_AMOUNT'],[0, 200000, 300000, 400000, 500000, 100000000],labels=["0-200,000", "200,000—300,000","300,000-400,000","400,000-500,000","500,000-inf"])

# # inteest rate
# credit["APPLY_INTEREST_RATE"].value_counts()
# credit['interest_rate_class'] = pd.cut(credit['APPLY_INTEREST_RATE'],[0, 4, 5, 6, 10],labels=["0-4", "4-5","5-6",">6"])



credit['MONTHLY_INCOME_WHITHOUT_TAX'] = pd.cut(credit['MONTHLY_INCOME_WHITHOUT_TAX'],[-1, 1500, 10000, 30000, 100000, 100000000],labels=["0-1500", "1500—10000","10000-20000","20000-100000","100000-inf"])
monthlyincome_to_factor = dict(zip(["0-1500", "1500—10000","10000-20000","20000-100000","100000-inf"],[0,1,2,3,4]))
credit['MONTHLY_INCOME_WHITHOUT_TAX'] = credit['MONTHLY_INCOME_WHITHOUT_TAX'].map(monthlyincome_to_factor)
# GAGE_TOTLE_PRICE
credit['GAGE_TOTLE_PRICE'] = pd.cut(credit['GAGE_TOTLE_PRICE'],[0, 500000, 1000000, 2000000, 5000000,100000000000],labels=["0-500,000", "500,000—1,000,000","1,000,000-2,000,000","2,000,000-5,000,000","5,000,000-inf"])
gage_to_factor = dict(zip(["0-500,000", "500,000—1,000,000","1,000,000-2,000,000","2,000,000-5,000,000","5,000,000-inf"], [0,1,2,3,4]))
credit['GAGE_TOTLE_PRICE'] = credit['GAGE_TOTLE_PRICE'].map(gage_to_factor)

# APPLY_AMOUNT
credit['APPLY_AMOUNT'] = pd.cut(credit['APPLY_AMOUNT'],[0, 200000, 300000, 400000, 500000, 100000000],labels=["0-200,000", "200,000—300,000","300,000-400,000","400,000-500,000","500,000-inf"])
apply_to_factor = dict(zip(["0-200,000", "200,000—300,000","300,000-400,000","400,000-500,000","500,000-inf"], [0,1,2,3,4]))
credit['APPLY_AMOUNT'] = credit['APPLY_AMOUNT'].map(apply_to_factor)
# inteest rate
credit["APPLY_INTEREST_RATE"].value_counts()
credit['APPLY_INTEREST_RATE'] = pd.cut(credit['APPLY_INTEREST_RATE'],[0, 4, 5, 6, 10],labels=["0-4", "4-5","5-6",">6"])
interest_to_factor = dict(zip(["0-4", "4-5","5-6",">6"], [0,1,2,3]))
credit['APPLY_INTEREST_RATE'] = credit['APPLY_INTEREST_RATE'].map(interest_to_factor)

# plt.bar()
# plt.show()
# plt.boxplot()
# plt.show()
credit.to_csv("Credit1.csv")
