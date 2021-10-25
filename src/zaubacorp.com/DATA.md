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


#Comparison Report

* 1773 data points in 2015 master seed data that is not present in our current dataset.
* Checked a few of them and found that they are old CINs of companies that have been alloted new CINs.
* The new CINs are present in our dataset.
* It would be better to collect company data, which will include the old cins too and then create an exhaustive list and comapre.
* Presently these 1773 cins are stored in data/extra_cin_in_master.json