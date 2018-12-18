from chalice import Chalice

app = Chalice(app_name='back-end')

import pymysql

def connectdb():
    db = pymysql.connect(
        host="host",
        port=3306,
        user="dummyuser",
        passwd="dummypwd",
        db="db")
    return db

def querydb(db):
    cursor = db.cursor()
    
    sql = "SELECT * FROM option_tb"
    try:
       
        cursor.execute(sql)
        
        results = cursor.fetchall()
        return results
    
    except:
        print "Error: unable to fecth data"

def updatedb(db,selected,option):
    
    cursor = db.cursor()

    
    sql = "UPDATE option_tb SET IsSelected = "+str(selected)
    sql+= " WHERE item = '"+option+"'"
    
    print(sql)

    try:

        cursor.execute(sql)

        db.commit()
    except:

        db.rollback()


    
@app.route('/')
def index():
    return {'hello': 'world'}
    
@app.route('/list')
def list():
    options ={}
    connect = connectdb()
    for item in querydb(connect):
        if item[1]==1:
            options[item[0]]=True
        else: options[item[0]]=False
    return options

@app.route('/change',methods=['POST'])
def list_change():
    connect = connectdb()
    items_as_json = app.current_request.json_body
    print(items_as_json['action'])
    print(items_as_json['elements'])
    if len(items_as_json['elements'])>0:
        if items_as_json['action'] =="add":
            print("add")
            for element in items_as_json['elements']:
                updatedb(connect,1,element)
        elif items_as_json['action'] =="remove":
            print("remove")
            for element in items_as_json['elements']:
                updatedb(connect,0,element)
            
    return items_as_json

if __name__ == "__main__":
    connect = connectdb()
    updatedb(connect,1,"Option 1")


