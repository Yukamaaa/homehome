from flask import Flask, request, render_template
app = Flask(__name__)
file_path = "./sensor_data.csv"
port_num = 17104

@app.route('/', methods = ['GET'])
def get_html():
    return render_template('./index.html')

@app.route('/exist', methods = ['POST'])
def update_exist():
    date = request.form["date"]
    time = request.form["time"]
    exist = request.form["exist"]
    try:
        f = open(file_path, 'w')
        f.write(date + "," + time + "," + exist)
        return "succeeded to write"
    except Exception as e:
        print(e)
        return "failed to write"
    finally:
        f.close()

@app.route('/exist', methods = ['GET'])
def get_exist():
    try:
        f = open(file_path, 'r')
        for row in f:
            exist = row
    except Exception as e:
        print(e)
        return e
    finally:
        f.close()
        return exist

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port_num)