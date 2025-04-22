from flask import Flask, render_template, request
import math

app = Flask(__name__)

a = 243.04
b = 17.625

def alp(R_H, Td):
    alpha = math.log(R_H / 100) + (a * Td) / (b + Td)
    return alpha

@app.route('/', methods=['GET', 'POST'])
def weather():
    result = {}
    if request.method == 'POST':
        try:
            option = int(request.form['option'])
            temp_dry = float(request.form['temp_dry'])
            temp_wet = float(request.form['temp_wet'])

            nat_n = 2.71828182845904
            N = 0.6687451584

            e_dry = 6.112 * (nat_n**(b * temp_dry / (a + temp_dry)))
            e_wet = 6.112 * (nat_n**(b * temp_wet / (a + temp_wet)))
            relative_humidity = ((e_wet - N * (1 + 0.00115 * temp_wet) * (temp_dry - temp_wet)) * 100) / e_dry
            alpha = alp(relative_humidity, temp_dry)
            dew_point = (b * alpha) / (a - alpha)

            if option in [2, 4]:
                result['relative_humidity'] = f"The relative humidity is :{relative_humidity:.2f}%"

            if option in [1, 4]:
                result['dew_point'] = f"The dew point is :{dew_point:.2f} °C"

            if option in [3, 4]:
                report = ""
                if 40 <= relative_humidity <= 60 and 19 <= temp_dry <= 30:
                    report = "Perfect comfort zone. Great day for a trip!"
                elif 40 <= relative_humidity <= 60 and temp_dry < 19:
                    report = "Comfortable humidity, but cold. Grab some hot chocolate!"
                elif 40 <= relative_humidity <= 60 and temp_dry > 30:
                    report = "Comfortable humidity, but hot. Stay cool!"
                elif relative_humidity < 40 and temp_dry < 19:
                    report = "Dry and cold. Stay hydrated and moisturized."
                elif relative_humidity > 60 and temp_dry < 19:
                    report = "Cold and humid. Might rain—be prepared!"
                elif relative_humidity > 60 and temp_dry > 30:
                    report = "Hot and humid. It's sauna weather!"
                elif relative_humidity < 40 and temp_dry > 30:
                    report = "Hot and dry. Potential storm warning!"
                elif relative_humidity > 60 and 19 <= temp_dry <= 30:
                    report = "Humid but tolerable."
                elif relative_humidity < 40 and 19 <= temp_dry <= 30:
                    report = "Dry but tolerable."
                result['weather_report'] = report

            if temp_dry > 50:
                result['extreme_warning'] = f"Wait a minute how are you surviving in {temp_dry}°C?!"

        except Exception as e:
            result['error'] = f"Error: {str(e)}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

