<!DOCTYPE html>
{% load i18n %}
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>signup</title>
        {% load static %}
        <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
    	<script src="{% static 'js/jquery-3.5.1.min.js' %}"></script>
    	<script src="{% static 'js/bootstrap.min.js' %}"></script>
	</head>
	<body style="padding-top:50px;">
        <div class="jumbotron jumbotron-fluid">
            <div class="container">
                    <h2>{% trans '註冊' %}</h2>
                    <h5 style="font-weight:bold;color:red">{% trans '說明：註冊完畢後，將直接登入進主畫面' %}</h5>
            </div>
        </div>
	   	<div class="container">
            <form action="{% url 'signup' %}" method="post">
                {% csrf_token %}
                {% for field in form %}
                    <p>
                        {{ field.label_tag }}<br>
                        {{ field }}
                        {% if field.help_text %}
                            <small style="color: grey">{{ field.help_text }}</small>
                        {% endif %}
                        {% for error in field.errors %}
                            <p style="color: red">{{ error }}</p>
                        {% endfor %}
                    </p>
                {% endfor %}

                <div class="form-row">
                    <div class="form-group col-md-2">
                        <button type="submit" class="btn btn-primary" style="width:100%">{% trans '送出' %}</button>
                    </div>
                    <div class="form-group col-md-2">
                        <button type="button" class="btn btn-primary" style="width:100%" onclick="location.href='{% url 'login' %}'">{% trans '回到登入' %}</button>
                    </div>
                </div>
            </form>
        </div>
	</body>
</html>
