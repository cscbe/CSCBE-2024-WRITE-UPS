extends CanvasLayer

var tween = null
func _process(delta):
	$Label.text = str($"/root/GlobalState".points) + " / 3"

	if $"/root/GlobalState".blob_messages[$"/root/GlobalState".next_message] != "":
		$CenterContainer/Label.text = $"/root/GlobalState".blob_messages[$"/root/GlobalState".next_message]
		$"/root/GlobalState".next_message += 1

		if tween != null:
			tween.kill()
		var message_label = $CenterContainer/Label
		message_label.modulate.a = 1.0
		tween = get_tree().create_tween()
		var new_color = message_label.modulate
		new_color.a = 0.0
		tween.tween_property(message_label, "modulate",new_color, 6).set_trans(Tween.TRANS_LINEAR)
