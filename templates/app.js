var predictions_url = 'prediction/'
//url for endpoint for our predictions
//todo -- find documentation regarding how a flask endpoint will work on a heroku app

var directions = ['E', 'ENE', 'ESE', 'N', 'NE', 'NNE', 'NNW', 'NW', 'S',
'SE', 'SSE', 'SSW', 'SW', 'W', 'WNW', 'WSW'  ]
//list of possible wind directions (array -- js)

d3.select("#wind_gust_dir")
.selectAll("option")
.data(directions)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});
//have list of possible directions input into wind_gust_dir id 

d3.select("#wind_direction_9")
.selectAll("option")
.data(directions)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

d3.select("#wind_direction_3")
.selectAll("option")
.data(directions)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

var temp_list = []

for (var i = -2; i < 20; i++){
temp_list.push(i * 3)
}

d3.select("#min_temp")
.selectAll("option")
.data(temp_list)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

d3.select("#max_temp")
.selectAll("option")
.data(temp_list)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

d3.select("#temp_9")
.selectAll("option")
.data(temp_list)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

d3.select("#temp_3")
.selectAll("option")
.data(temp_list)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

var wind_speed = []
for (var i = 0; i < 25; i++){
    wind_speed.push(i * 5)
    }

d3.select("#WindGustSpeed")
.selectAll("option")
.data(wind_speed)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

d3.select("#wind_speed_9a")
.selectAll("option")
.data(wind_speed)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

d3.select("#wind_speed_3")
.selectAll("option")
.data(wind_speed)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

var humidity_list = []
for (var i = 0; i < 21; i++){
    humidity_list.push(i * 5)
    }

d3.select("#Hummidity_9")
.selectAll("option")
.data(humidity_list)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});


d3.select("#Hummidity_3")
.selectAll("option")
.data(humidity_list)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

var rain_list = []
for (var i = 0; i < 21; i++){
    rain_list.push(i)
    }

d3.select("#rainfall")
.selectAll("option")
.data(rain_list)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});



d3.select("#Evaporation")
.selectAll("option")
.data(humidity_list)
//the user will have the option to select 0 to 100. The humidity list has these options already
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

var sunshine_list = []
for (var i = 0; i < 30; i++){
    sunshine_list.push(i * 0.5)
    }

d3.select("#Sunshine")
.selectAll("option")
.data(sunshine_list)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

var pressure_list = []
for (var i = 0; i < 17; i++){
    pressure_list.push((i * 5)+ 970)
    }

d3.select("#pressure_9")
.selectAll("option")
.data(pressure_list)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

d3.select("#pressure_3")
.selectAll("option")
.data(pressure_list)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

var cloud_list = []
for (var i = 0; i < 20; i++){
    cloud_list.push(i * 0.5)
    }

d3.select("#cloud_9")
.selectAll("option")
.data(cloud_list)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

d3.select("#cloud_3")
.selectAll("option")
.data(cloud_list)
.enter()
.append('option')
.text(function(d){return d})
.attr("value", function(d){return d});

function getInputValues(){
var cloud_3 = d3.select('#cloud_3').property('value')
var cloud_9 = d3.select('#cloud_9').property('value')
var pressure_3 = d3.select("#pressure_3").property('value')
var pressure_9 = d3.select('#pressure_9').property('value')
var Sunshine = d3.select('#Sunshine').property('value')
var Evaporation = d3.select('#Evaporation').property('value')
var rainfall = d3.select('#rainfall').property('value')
var Hummidity_3 = d3.select('#Hummidity_3').property('value')
var Hummidity_9 = d3.select('#Hummidity_9').property('value')
var wind_speed_3 = d3.select('#wind_speed_3').property('value')
var wind_speed_9a = d3.select('#wind_speed_9a').property('value')
var WindGustSpeed = d3.select('#WindGustSpeed').property('value')
var temp_3 = d3.select('#temp_3').property('value')
var temp_9 = d3.select('#temp_9').property('value')
var max_temp = d3.select('#max_temp').property('value')
var min_temp = d3.select('#min_temp').property('value')
var wind_direction_3 = d3.select('#wind_direction_3').property('value')
var wind_direction_9 = d3.select('#wind_direction_9').property('value')
var wind_gust_dir = d3.select('#wind_gust_dir').property('value')

if (rainfall === 0){
    var rainToday = 'False'
} else { 
    var rainToday = 'True'
}

getPrediction(min_temp, max_temp, rainfall, Evaporation, Sunshine, WindGustSpeed,
    wind_speed_9a, wind_speed_3, Hummidity_9, Hummidity_3, pressure_9,
    pressure_3, cloud_9, cloud_3, temp_9, temp_3, rainToday, 
    wind_gust_dir, wind_direction_9, wind_direction_3)
}
// submitButton

var predictButton = d3.select('#submitButton')

predictButton.on("click", getInputValues)

function getPrediction(minTemp, maxTemp, rainfall, evaporation, sunshine,
    windGustSpeed, windSpeed9, windSpeed3, humidity9, humidity3, pressure9,
    pressure3, cloud9, cloud3, temp9, temp3, rainToday, windGustDir,
    windDir9, windDir3){
        url1 = `/predict/${minTemp}/${maxTemp}/${rainfall}/${evaporation}/${sunshine}/`
        url2 = `${windGustSpeed}/${windSpeed9}/${windSpeed3}/${humidity9}/${humidity3}/${pressure9}/`
        url3 = `${pressure3}/${cloud9}/${cloud3}/${temp9}/${temp3}/${rainToday}/${windGustDir}/`
        url4 = `${windDir9}/${windDir3}`
        url = url1 + url2 + url3 + url4
        console.log(url)

        var result = d3.json(url).then(function(result_data){
            var mvlr = result_data.MVLR
            var knn = result_data.KNN
            var rf = result_data.RF
            var svm = result_data.SVM
            var agg = result_data.AGG


            document.getElementById("overall").innerHTML = `Aggregate Prediction: ${agg}`
            document.getElementById("mvlr").innerHTML = `MVLR: ${mvlr}`
            document.getElementById("knn").innerHTML = `KNN: ${knn}`
            document.getElementById("rf").innerHTML = `Random Forest: ${rf}`
            document.getElementById("svm").innerHTML = `SVM: ${svm}`
 //           document.getElementById("sum").innerHTML = 'Machine Learning Method and corresponding prediction'

        })
    }

