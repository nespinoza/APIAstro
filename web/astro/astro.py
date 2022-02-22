import os
import batman
import json
import string
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_UPLOAD = os.path.join(APP_ROOT, 'upload')
ALLOWED_EXTENSIONS = set(['txt', 'scv', 'dat', 'TXT', 'SCV'])
ESTELAR = pow(10,30)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = APP_UPLOAD

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():

    global content

    if request.method == 'POST':

        x_values = list()
        y_values = list()
        allRows = list()
        flujo = list()
        time = list()
        per=list()
        Per=list()
        periodo = list()
        Periodo=0
        igual_o_puntos = ''


        if 'file' in request.files:
            file = request.files['file']
        if 'file' in request.files and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
                allRows = f.readlines()


            aux = list()
            val=0
            for line in allRows:
                for aux1 in line:
                    if allRows.index(line)==0:
                        if (aux1=='='):
                            igual_o_puntos='igual'
                        elif (aux1 == ':'):
                            igual_o_puntos='puntos'

            for line in allRows:

                for aux1 in line:


                    if allRows.index(line)==0:

                        #obtener el valor del periodo
                        per_ = line
                        if( igual_o_puntos=='igual' ):
                         per_ = per_.split('=')
                         periodo = per_[1]
                         periodo = periodo.replace('\n','')
                         periodo = periodo.replace(' ','')
                         for k in periodo:
                             if k == '\n':
                                 periodo.remove(k)
                             if k == ' ':
                                 periodo.remove(k)
                         Periodo = float(periodo)
                         aux2 =0
                         break;

                        elif(igual_o_puntos=='puntos'):
                         per_ = per_.split(':')
                         periodo = per_[1]
                         periodo = periodo.replace('\n','')
                         periodo = periodo.replace(' ','')
                         for k in periodo:
                             if k == '\n':
                                 periodo.remove(k)
                             if k == ' ':
                                 periodo.remove(k)
                         Periodo = float(periodo)
                         aux2 =0
                         break;
                        else:
                         Periodo = 1.0



                    if line.index(aux1)==0:
                        if aux1=='\n':
                         aux2=0
                         break;
                        if aux==' ':
                         auz2=0
                         break;

                    if aux1=='#':
                        aux2 =0
                        break;
                    if aux1==' ':
                        aux2=0
                        break;

                    else:
                        aux2 = 1
                if aux2==1:
                    line = line.strip()
                    columns = line.split()
                    x_values.append(float(columns[0]))
                    y_values.append(float(columns[1]))

        else:

            if 'x_values' in request.form:
                x_values = json.loads(request.form['x_values'])

            if 'y_values' in request.form:
                y_values = json.loads(request.form['y_values'])

            if 'Periodo' in request.form:
                Periodo = json.loads(request.form['Periodo'])


        radio_planeta = float(request.form['radio_planeta'])
        radio_estrella = float(request.form['radio_estrella'])
        distancia_orbital =  float(request.form['distancia_orbital'])
        inclinacion_orbital = float(request.form['inclinacion_orbital'])
        mover_peak = float(request.form['mover_peak'])


        #transformando numeros de los que recibe batman
        rp = (radio_planeta*6400)/(radio_estrella*700000)
        a = (distancia_orbital*150000000)/(radio_estrella*700000)




        str_x_json = []
        str_y_json = []
        str_y_file_json = []
        str_fbat_t_json = []
        str_f_t_json = []
        str_Res_json = []


        if len(x_values):


            medio = x_values[int(len(x_values)/2)] + mover_peak

            params = batman.TransitParams()
            params.t0 = medio
            params.per = Periodo#float(x_values[0])
            params.rp = rp
            params.a = a
            params.inc = inclinacion_orbital
            params.ecc = 0.
            params.w = 90.
            params.u = [0.1, 0.3]
            params.limb_dark = "quadratic"

        #    x__values = []
        #    for i in x_values:
        ##        if i != x_values[0]:
                #    x__values.append(i)

        #    x_values = x__values
            #x_values.pop(0)


            m = batman.TransitModel(params, np.array(x_values))
            flux = m.light_curve(params)

            #creando datos teoricos mas densos

            t = np.linspace(float(x_values[0]), float(x_values[len(x_values)-1]), 2000)
            m2 = batman.TransitModel(params,t)
            ft = m2.light_curve(params)
            ft = ft.tolist()


            x = np.array(x_values)
            y = np.array(y_values)
            flu = np.array(flux)

            res = flu-y
            res = res.tolist()
            flux = flux.tolist()

            str_x_json = json.dumps(x_values)
            str_y_json = json.dumps(ft)
            str_y_file_json = json.dumps(y_values)
            str_res_json = json.dumps(res)

            #produciendo formato plot de flujo batman
            indx = 0
            fbat_t = list()
            for row in t :
                fbat_t.append([row, ft[indx]])
                indx = indx+1
            str_fbat_t_json = json.dumps(fbat_t)

            #produciendo formato plot de flujo real
            indx = 0
            f_t = list()
            for row in x_values:
                f_t.append([row, y_values[indx]])
                indx = indx+1
            str_f_t_json = json.dumps(f_t)


            #Res = np.array(flux)-np.array(y_values)
            Residuo = list()
            j=0
            for i in x_values:
                val = float(res[j])
                Residuo.append([ i , val ])
                j=j+1
            str_Res_json = json.dumps(Residuo)

            totalRes = []
            for k in res:
                totalRes.append(pow(k,2))


            totalRes_val = pow(sum(totalRes),0.5)



        if 'formato' in request.form and request.form['formato'] == 'json':
            return jsonify(form=request.form, x_json=str_x_json, mover_peak=mover_peak, y_json=str_y_json, y_file=str_y_file_json, fbat_t_json=str_fbat_t_json,f_t_json=str_f_t_json, Res_jason = str_Res_json, hola = Periodo)
        else:
            return render_template('index.html', form=request.form, x_json=str_x_json, mover_peak=mover_peak, y_json=str_y_json, y_file=str_y_file_json, fbat_t_json=str_fbat_t_json,f_t_json=str_f_t_json, Res_jason = str_Res_json,hola=Periodo)


    return render_template('index.html', form=[])




if __name__ == '__main__':
    app.run(debug=True)
