import requests
url = "https://www.hsx.vn/Modules/Listed/Web/SymbolList"

querystring = {
    "pageFieldName1":"Code",
    "pageFieldValue1":"",
    "pageFieldOperator1":"eq",
    "pageFieldName2":"Sectors",
    "pageFieldValue2":"",
    "pageFieldOperator2":"",
    "pageFieldName3":"Sector",
    "pageFieldValue3":"00000000-0000-0000-0000-000000000000",
    "pageFieldOperator3":"",
    "pageFieldName4":"StartWith",
    "pageFieldValue4":"","pageFieldOperator4":"",
    "pageCriteriaLength":"4",
    "_search":"false",
    "nd":"1661709603312",
    "rows":"30",
    "page":"1",
    "sidx":"id",
    "sord":"desc"}

payload = ""
headers = {"cookie": '<to preserve personal information, this field will not be show. (Use Postman or Insomnia to generate your own)>'}


content = []
for i in range(1, 15):
    
    querystring['page'] = i
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    rows = response.json()['rows']
    
    for row in rows:
        cell = row['cell']
        content.append(cell[1])
        
    print('finish 1 request & process cycle')

with open('ticker_name.csv', 'w') as f:
    for line in content:
        f.write(line + '\n')
        