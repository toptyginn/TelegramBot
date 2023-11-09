from openpyxl import load_workbook

wb = load_workbook('test.xlsx', read_only=True)

ws = wb['Лист1']
matrix = {}
users = []
stands = []
svc = []
print(f'{ws.cell(1,1).value}\t{ws.cell(1,2).value}\t{ws.cell(1,3).value}')
for row in range(2,ws.max_row):
    print(f'{ws.cell(row,1).value}\t{ws.cell(row,2).value}\t{ws.cell(row,3).value}')
