extends Node

# signal blob_capture_registered

var server_url = "https://outofbounds.challenges.cybersecuritychallenge.be"

func send_blob_capture(idx, hash):
	print("Send blob capture to servers")
	$HTTPRequestRegisterBlob.set_tls_options(TLSOptions.client_unsafe())
	$HTTPRequestRegisterBlob.request_completed.connect(_on_game_blob_request_completed)
	var body = JSON.stringify({'idx': idx, 'hash': hash})
	var headers = ["Content-Type: application/json"]
	if get_node("/root/GlobalState").session_id != "":
		print("  adding cookie: " + get_node("/root/GlobalState").session_id)
		headers.append("Cookie: " + get_node("/root/GlobalState").session_id)
	var error = $HTTPRequestRegisterBlob.request(server_url + '/register_blob_capture', headers, HTTPClient.METHOD_POST, body)
	if error != OK:
		print_debug("HTTP Request Error Code: %s" % error)
		push_error("An error occurred in the HTTP request, code: " + str(error))

func _on_game_blob_request_completed(result, response_code, headers, body):
	var json = JSON.parse_string(body.get_string_from_utf8())
	if json != null:
		# print(json)
		get_node("/root/GlobalState").blob_server_ids[json["idx"]] = json["confirm_hash"]
		get_node("/root/GlobalState").blob_messages[json["idx"]] = json["message"]

	queue_free()

func send_game_hash(hash):
	$HTTPRequestGameHash.set_tls_options(TLSOptions.client_unsafe())
	$HTTPRequestGameHash.request_completed.connect(_on_request_completed)
	var body = JSON.stringify({'integrity_hash': hash})
	var headers = ["Content-Type: application/json"]
	if get_node("/root/GlobalState").session_id != "":
		headers.append("Cookie: " + get_node("/root/GlobalState").session_id)
	var error = $HTTPRequestGameHash.request(server_url + '/create_session', headers, HTTPClient.METHOD_POST, body)
	if error != OK:
		print_debug("HTTP Request Error Code: %s" % error)
		push_error("An error occurred in the HTTP request, code: " + str(error))

func _on_request_completed(result, response_code, headers, body):
	for h in headers:
		if h.begins_with('set-cookie'):
			var session_cookie = h.split(':')[1].lstrip(' ').split(';')[0]
			# print('Got a new session cookie: ' + session_cookie)
			get_node("/root/GlobalState").session_id = session_cookie
	
	var json = JSON.parse_string(body.get_string_from_utf8())
	if json != null:
		# TODO, enforce webserver stuff
		if json["status"] != "success":
			print("Game is not verified. Could not get a valid session.")
			#get_tree().root.propagate_notification(NOTIFICATION_WM_CLOSE_REQUEST)

	queue_free()
	
func _notification(what):
	if what == NOTIFICATION_WM_CLOSE_REQUEST:
		get_tree().quit(0)

