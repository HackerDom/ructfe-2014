<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv='refresh' content='60'>
        <title>RuCTFE 2014 Network Status/</title>
        <style>
              /*body {background-color:lightgray}*/
              h1 {text-align: center; padding-bottom: 0px; }
              h3 {text-align: center; padding-bottom: 0px; }
              h4 {text-align: center; padding-bottom: 0px; }
              td {font-family:Arial, Helvetica, sans-serif; 
                    height: 50px; text-align: center;}
              table {width: 98%;}
              .yesnocell {width: 150px; color: #bbbbbb;}
              .yescell {background-color: #00b500;}
              .nocell {background-color: #ff4040;}
              .graycell {color: gray; font-size:small; }
              .namecell {width: 400px}
              p {color:green}
        </style>
    </head>
    <body>
        <h1> RuCTFE 2014 Network Status </h1>
        <h3> Updated at: {{time}} </h3>
        {% if netopened %}
        <h4> Network is opened </h4>
        {% else %}
        <h4> Network is closed </h4>
        {% endif %}
        <table>
            <tr>
            <th>#</th>
            <th>Name</th>
            <th>Router</th>
            <th>Image</th>
            <th>Jetpack</th>
            <th>Voicebox</th>
            <th>ISS</th>
            <th>VWS</th>
            <th>Heart</th>
            <th>Pidometer</th>
            <th>Glass</th>
            </tr>

            <tr>
            <th></th>
            <th></th>
            <th class="graycell">&sum; = {{sums.s1_ping}}</th>
            <th class="graycell">&sum; = {{sums.image_ping}}</th>
            <th class="graycell">&sum; = {{sums.s2_ping}}</th>
            <th class="graycell">&sum; = {{sums.s3_ping}}</th>
            <th class="graycell">&sum; = {{sums.s4_ping}}</th>
            <th class="graycell">&sum; = {{sums.s5_ping}}</th>
            <th class="graycell">&sum; = {{sums.s6_ping}}</th>
            <th class="graycell">&sum; = {{sums.s7_ping}}</th>
            <th class="graycell">&sum; = {{sums.s8_ping}}</th>
            </tr>
        {% for team in result %}
            <tr>
            <td> {{team.id}} </td>
            <td class="namecell"> {{team.name}} </td>
            {% if team.s1_ping is not none %}
            <td title="{{team.s1_ip}}" class="yesnocell yescell"> {{team.s1_ping}}ms </td>
            {% else %}
            <td title="{{team.s1_ip}}" class="yesnocell nocell">  </td>
            {% endif %}
            {% if team.image_ping is not none %}
            <td title="{{team.image_ip}}" class="yesnocell yescell"> {{team.image_ping}}ms </td>
            {% else %}
            <td title="{{team.image_ip}}" class="yesnocell nocell">  </td>
            {% endif %}

            {% if team.s2_ping is not none %}
            <td title="{{team.s2_ip}}" class="yesnocell yescell"> {{team.s2_ping}}ms </td>
            {% else %}
            <td title="{{team.s2_ip}}" class="yesnocell nocell">  </td>
            {% endif %}

            {% if team.s3_ping is not none %}
            <td title="{{team.s3_ip}}" class="yesnocell yescell"> {{team.s3_ping}}ms </td>
            {% else %}
            <td title="{{team.s3_ip}}" class="yesnocell nocell">  </td>
            {% endif %}

            {% if team.s4_ping is not none %}
            <td title="{{team.s4_ip}}" class="yesnocell yescell"> {{team.s4_ping}}ms </td>
            {% else %}
            <td title="{{team.s4_ip}}" class="yesnocell nocell">  </td>
            {% endif %}

            {% if team.s5_ping is not none %}
            <td title="{{team.s5_ip}}" class="yesnocell yescell"> {{team.s5_ping}}ms </td>
            {% else %}
            <td title="{{team.s5_ip}}" class="yesnocell nocell">  </td>
            {% endif %}

            {% if team.s6_ping is not none %}
            <td title="{{team.s6_ip}}" class="yesnocell yescell"> {{team.s6_ping}}ms </td>
            {% else %}
            <td title="{{team.s6_ip}}" class="yesnocell nocell">  </td>
            {% endif %}

            {% if team.s7_ping is not none %}
            <td title="{{team.s7_ip}}" class="yesnocell yescell"> {{team.s7_ping}}ms </td>
            {% else %}
            <td title="{{team.s7_ip}}" class="yesnocell nocell">  </td>
            {% endif %}

            {% if team.s8_ping is not none %}
            <td title="{{team.s8_ip}}" class="yesnocell yescell"> {{team.s8_ping}}ms </td>
            {% else %}
            <td title="{{team.s8_ip}}" class="yesnocell nocell">  </td>
            {% endif %}

            </tr>
        {% endfor %}
        </table>
    </body>
</html>