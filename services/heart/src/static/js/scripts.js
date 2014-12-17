Date.prototype.toReadString = function() {
	function numToString(num) {
		return "" + (num > 9 ? num : "0" + num);
	}
	var date = this.getDate();
	var month = this.getMonth() + 1;
	var year = this.getFullYear();
	var hour = this.getHours();
	var minutes = this.getMinutes();
	var seconds = this.getSeconds();
	return numToString(year) + "-" + numToString(month) + "-" + numToString(date) + " " + numToString(hour) + ":" + numToString(minutes) + ":" + numToString(seconds);
}

var login = $.cookie("login");
if(login) {
	$("#login").find("a").text(login);
	$("#login-link").hide();
	$("#register-link").hide();
} else {
	$("#func").attr("disabled", true);
	$("#cond").attr("disabled", true);
	$("#value").attr("disabled", true);
	$("#mssg").attr("disabled", true);
	$(".form-alerts").find("button").attr("disabled", true);
}

var ex = $.cookie("expr");
if(ex) {
	var parts = ex.split(":");
	$("#func").val(parts[0]);
	$("#cond").val(parts[1]);
	$("#value").val(parts[2]);
	$("#mssg").val(parts[3]);
}

function addRow($table, clss, cols) {
	var $tr = $("<tr class='" + clss + "'/>");
	cols.forEach(function (arg) {
		var $td = $("<td/>").text(arg);
		$tr.append($td);
	});
	$table.append($tr);
}
function updateAlerts() {
	var $table = $(".table");
	$.ajax({
		url: "/alerts/"
	}).done(function (data) {
		$table.find("tr").remove();
		if(data && data.msg) {
			addRow($table, "warning", [new Date(data.dt).toReadString(), data.msg]);
		} else {
			addRow($table, "", ["Looks good", ""]);
		}
	}).fail(function (xhr) {
		$table.find("tr").remove();
		addRow($table, "danger", [xhr.responseText ? xhr.responseText : "Unknown error"]);
	});
};
if(login) {
	updateAlerts();
	setInterval(updateAlerts, 30000);
}

$(".form-alerts").submit(function (e) {
	e.preventDefault();
	var $errorMsg = $(this).find(".alert");
	$.ajax({
		url: "/setexpr/",
		method: "POST",
		data: $.param({ expr: "if(" + $("#func").val() + "(stat)" + $("#cond").val() + $("#value").val() + ",\"" + $("#mssg").val() + "\",null)", parts: [$("#func").val(), $("#cond").val(), $("#value").val(), $("#mssg").val()].join(":") })
	}).done(function () {
		$errorMsg.removeClass("alert-danger").addClass("alert-success").hide();
		$errorMsg.text("OK").show();
		setTimeout(function () { window.location = "/"; }, 2000);
	}).fail(function (xhr) {
		$errorMsg.addClass("alert-danger").text(xhr.responseText ? xhr.responseText : "Unknown error").show();
	});
});

function plot() {
	d3.json("/series/", function (error, data) {
		var mindt = new Date();
		var maxdt = new Date(1970, 1, 1);

		var margin = 0;
		var plotWidth = 938;
		var plotHeight = 250;
		var circleRadius = 4;
		var circleOpacity = 0.5;

		var svg = d3.select("#js-case-plot").append("svg")
			.attr("style", "caseplotCanvas")
			.attr("width", plotWidth + margin)
			.attr("height", plotHeight + margin * 2)
			.append("g")
			.attr("transform", "translate(" + margin + "," + margin + ")");

		if(!(data && data.points && data.points.length)) {
			svg
				.append("text")
				.text("No data for period")
				.attr("x", 330)
				.attr("y", 120)
				.attr("font-size", "32px");
			return;
		}

		data = data.points;
		data.forEach(function (d) {
			d.dt = new Date(d.dt);
			d.val = +d.val;
			if(mindt > d.dt)
				mindt = d.dt;
			if(maxdt < d.dt)
				maxdt = d.dt;
		});

		var xScale = d3.time.scale()
			.range([0, plotWidth])
			.domain([mindt, maxdt]);

		var yScale = d3.scale.linear()
			.range([plotHeight, 0])
			.domain([0, 200]);

		var scaleParts = ["200", "150", "100", "80", "60", "0"];
		svg.selectAll("rect")
			.data(scaleParts)
			.enter().append("rect")
			.attr("x", 0)
			.attr("y", function (d, i) { return i * (plotHeight / scaleParts.length); })
			.attr("width", plotWidth)
			.attr("height", plotHeight / scaleParts.length)
			.attr("fill", function (d, i) {
				var colcomp = 200 + i * (65 / (scaleParts.length - 1));
				return "rgb(255," + colcomp + "," + colcomp + ")";
			});

		svg.selectAll(".leftLabels")
			.data(scaleParts)
			.enter().append("text")
			.text(function (d) { return d; })
			.attr("x", 0)
			.attr("y", function (d, i) {
				var partHeight = plotHeight / scaleParts.length;
				return (i + 1) * partHeight - 9;
			})
			.attr("text-anchor", "end")
			.attr("fill", "#333")
			.attr("font-size", 10);

		data.forEach(function (item) {
			if(item.evt) {
				svg.append("line")
					.attr("class", "evtline")
					.attr("x1", xScale(item.dt))
					.attr("y1", 0)
					.attr("x2", xScale(item.dt))
					.attr("y2", 255);
			}
		});

		var line = d3.svg.line()
			.x(function (item) {
				return xScale(item.dt);
			})
			.y(function (item) {
				return yScale(item.val);
			});

		svg.append("path").attr("d", line(data));

		var circles = svg.selectAll("circle")
			.data(data)
			.enter().append("circle")
			.attr("r", circleRadius)
			.attr("cx", function (d) { return xScale(d.dt); })
			.attr("cy", function (d) { return yScale(d.val); })
			.attr("fill-opacity", 0.5)
			.attr("fill", "red");

		$('svg circle').tipsy({
			gravity: 'w',
			html: true,
			offset: 20,
			opacity: 0.7,
			title: function () {
				var d = this.__data__;
				return $("<div/>").text(d.dt.toReadString()).html() + "<br/><br/>" + $("<div/>").text(d.val + " bpm").html() + (d.evt ? "<br/><br/>" + $("<div/>").text(d.evt).html() : "");
			}
		});

		if(!login) {
			svg
				.append("text")
				.text("Example")
				.attr("x", 10)
				.attr("y", 20)
				.attr("font-size", "12px");
		}

		var mouseOnFunc = function () {
			var circle = d3.select(this);
			circle.focused = true;
			circle.transition()
				.duration(800)
				.attr("fill-opacity", 1)
				.attr("r", circleRadius * 2)
				.ease("elastic");
		};

		var mouseOffFunc = function () {
			var circle = d3.select(this);
			circle.focused = false;
			circle.transition()
				.duration(800)
				.attr("fill-opacity", circleOpacity)
				.attr("r", circleRadius)
				.ease("elastic");
		};

		circles.on("mouseover", mouseOnFunc);
		circles.on("mouseout", mouseOffFunc);
	});
};

plot();