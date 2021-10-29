## links

Table Headers
* CIN 
* Company
* RoC
* Status
* link

CIN as key for dictionary
* 140581 items in total

* 140250 extracted
* 301 integrity errors

* After resolving integrity issues and adding missing data
* 140280 extracted




## trademark
 * Categories / Class of trademarks Explanation: https://ipindiaonline.gov.in/tmrpublicsearch/classfication_goods_service.htm

Storage Format:
CIN - Key of dictionary
values is a list with:
* index 0 = Trademark name
* index 1 = Trademark class
* index 2 = Trademark class description
* index 3 = Application Date
* index 4 = status
* index 5  = Goods and Services Description
* index 6  = Applicant Address
* index 7 = trademark image link

Data Collection:
0-9999: Companies with at least 1 Trademark: 330
10000-19999: Companies with at least 1 Trademark: 317
20000-29999: Companies with at least 1 Trademark: 289
30000-39999: Companies with at least 1 Trademark: 324
40000-49999: Companies with at least 1 Trademark: 350
50000-59999: Companies with at least 1 Trademark: 304
60000-69999: Companies with at least 1 Trademark: 318 - 1 err
70000-79999: Companies with at least 1 Trademark: 353 - 8 err
80000-89999: Companies with at least 1 Trademark: 352 - 3 err
90000-99999: Companies with at least 1 Trademark: 332 - 2 err
100000-104999: Companies with at least 1 Trademark: 166
105000-109999: Companies with at least 1 Trademark: 174 - 1err
110000-114999: Companies with at least 1 Trademark: 161 - 1err
115000-119999: Companies with at least 1 Trademark: 178
120000-124999: Companies with at least 1 Trademark: 144
125000-129999: Companies with at least 1 Trademark: 153
130000-134999: Companies with at least 1 Trademark: 152
135000-139999: Companies with at least 1 Trademark: 148
140000-140279: Companies with at least 1 Trademark: 8

Total: 

#Comparison Report

* 1773 data points in 2015 master seed data that is not present in our current dataset.
* Checked a few of them and found that they are old CINs of companies that have been alloted new CINs.
* The new CINs are present in our dataset.
* It would be better to collect company data, which will include the old cins too and then create an exhaustive list and comapre.
* Presently these 1773 cins are stored in data/extra_cin_in_master.json
