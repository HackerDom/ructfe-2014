<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>RuCTFE 2014 Network Status/</title>
        <style>
              /*body {background-color:lightgray}*/
              h1 {text-align: center; padding-bottom: 0px; }
              td {font-family:Arial, Helvetica, sans-serif; 
                    height: 50px; text-align: center;}
              .yesnocell {width: 150px; color: #bbbbbb;}
              .yescell {background-color: #00b500;}
              .nocell {background-color: #ff4040;}
              .namecell {width: 400px}
              p {color:green}
        </style>
    </head>
    <body>
        <h1> RuCTFE 2014 Network Status </h1>
        <table>
            <tr>
            <th>#</th>
            <th>Name</th>
            <th>Router is UP</th>
            <th>Router was UP</th>
            <th>Image is UP</th>
            <th>Image was UP</th>
            </tr>

        {% for team in result %}
            <tr>
            <td> {{team.id}} </td>
            <td class="namecell"> {{team.name}} </td>
            {% if team.router_ping is not none %}
            <td class="yesnocell yescell"> {{team.router_ping}}ms </td>
            {% else %}
            <td class="yesnocell nocell">  </td>
            {% endif %}
            {% if team.router_pingonce %}
            <td class="yesnocell yescell">  </td>
            {% else %}
            <td class="yesnocell nocell">  </td>
            {% endif %}
            {% if team.image_ping is not none %}
            <td class="yesnocell yescell"> {{team.image_ping}}ms </td>
            {% else %}
            <td class="yesnocell nocell">  </td>
            {% endif %}
            {% if team.image_pingonce %}
            <td class="yesnocell yescell">  </td>
            {% else %}
            <td class="yesnocell nocell">  </td>
            {% endif %}
            </tr>
        {% endfor %}
        </table>
    </body>
</html>