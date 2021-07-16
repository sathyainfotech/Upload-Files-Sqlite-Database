from flask import Flask,render_template,request,flash,redirect,url_for
import os
import sqlite3

app=Flask(__name__)
app.secret_key="123"

app.config['UPLOAD_FOLDER1']="C:/Users/Sathya/Desktop/PDF"
app.config['UPLOAD_FOLDER2']="C:/Users/Sathya/Desktop/Images"

con=sqlite3.connect("MyPDF.db")
con.execute("create table if not exists myfile(pid integer primary key,fname text,fpath blob,imgname text,imgpath blob)")
con.close()

@app.route("/",methods=["GET","POST"])
def upload():
    if request.method == 'POST':
        upload_file = request.files['upload_files']
        upload_image = request.files['upload_image']

        if upload_file.filename != '' and upload_image.filename != '':
            upload_file_path = os.path.join(app.config['UPLOAD_FOLDER1'], upload_file.filename)
            upload_image_path = os.path.join(app.config['UPLOAD_FOLDER2'], upload_image.filename)

            FilesPath = convertToBinaryData(upload_file_path)
            ImagePath = convertToBinaryData(upload_image_path)

            con = sqlite3.connect("MyPDF.db")
            cur = con.cursor()
            cur.execute("insert into myfile(fname,fpath,imgname,imgpath)values(?,?,?,?)",
                        (upload_file.filename, FilesPath, upload_image.filename, ImagePath))
            con.commit()
            flash("File Upload Successfully", "success")

            con = sqlite3.connect("MyPDF.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select * from myfile")
            data = cur.fetchall()

            for row in data:
                fname = row[1]
                imgname = row[3]
                files = row[2]
                images = row[4]

            MyFilePath = "C:/Users/Sathya/Desktop/UploadFiles/static/Files/" + fname
            MyImagePath = "C:/Users/Sathya/Desktop/UploadFiles/static/Image/" + imgname

            writeTofile(files, MyFilePath)
            writeTofile(images, MyImagePath)
            con.close()
        return render_template("upload.html",data=data)
    else:
        con = sqlite3.connect("MyPDF.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from myfile")
        data = cur.fetchall()

        if cur.fetchall() != "":
            return render_template("upload.html",data=data)
        else:
            return render_template("upload.html")
        con.close()




def writeTofile(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
        return blobData


@app.route('/delete_record/<string:id>')
def delete_record(id):
    try:
        con = sqlite3.connect("MyPDF.db")
        cur = con.cursor()
        cur.execute("delete from myfile where pid=?", [id])
        con.commit()
        flash("Record Deleted Successfully", "success")
    except:
        flash("Record Deleted Failed", "danger")
    finally:
        return redirect(url_for("upload"))
        con.close()

if __name__ == '__main__':
    app.run(debug=True)