import pypyodbc
try:
    myConnection = pypyodbc.connect('DRIVER={SQL Server};'
                                'Server=tcp:sample559.database.windows.net,1433;'
                                'Database=sample;'
                                'uid=pranathi355;pwd=Mr.@bdul$450;'
                                'Encrypt=yes')
    print("connected")
    
except:
    print("Not Connected")