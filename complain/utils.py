from django.template.context_processors import csrf



def form_1(request):
	form = "<form id='data' action='https://snitch-yl.herokuapp.com/mobile/complain/' method='POST' enctype='multipart/form-data'>"
	form += "<input type='hidden' name='csrfmiddlewaretoken' value='" + str(csrf(request)['csrf_token']) + "'>";
	#form += str(csrf(request)['csrf_token'])

	form += "<div class='input-field col s12'>"
	form += "<input id='title' type='text' name='title' class='validate' style='color: white'>"
	form += "<label for='title'>Title</label>"
	form += "</div>"

	form += "<div class='input-field col s12'>"
	form += "<textarea id='textarea1' name='description' class='materialize-textarea' style='color: white'></textarea>"
	form += "<label for='textarea1'>Report Detail</label>"
	form += "</div>"

	form += "<input type='file' name='document' accept='image/*' capture='camera' multiple>"

	form += "<div class='input-field col s12'>"
	form += "<button class='btn waves-effect waves-light' type='submit' name='action'>Submit"
	form += "<i class='material-icons right'>send</i>"
	form += "</button>"
	form += "</div>"

	form += "</form>"

	return form
