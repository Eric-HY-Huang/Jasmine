from flask import Flask,render_template,request
import os,requests,json
app = Flask(__name__)



@app.route('/')
@app.route('/homepage')
def home(name=None):
    myResponse = requests.get("https://diga5o6ore.execute-api.us-east-2.amazonaws.com/api/list")
    if(myResponse.ok):
        jData = json.loads(myResponse.content,"UTF-8")
        print(jData)
    return render_template('homepage.html',name=name,options=jData)

@app.route('/change',methods=['POST'])
def change():
    data = request.get_json(force=True)
    post_json={
        "action":"add",
        "elements": None
    }
    elements = []
    if len(data['added_elements']) >0 :
        for element in data['added_elements']:
            elements.append(element)
    else:
        post_json['action'] = "remove"
        for element in data['removed_elements']:
            elements.append(element)

    post_json['elements'] = elements
    
    res= requests.post('https://diga5o6ore.execute-api.us-east-2.amazonaws.com/api/change', json=post_json)
    print res.content
            
    return "success"
    
if __name__ == "__main__":
    # configure in order page can be preview in Cloud9
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
    app.debug(True)
    