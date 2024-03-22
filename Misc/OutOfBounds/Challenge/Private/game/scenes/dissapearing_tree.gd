extends StaticBody2D


func _process(_delta):
	if $"/root/GlobalState".blob_server_ids[0] != "":
		get_parent().queue_free()
