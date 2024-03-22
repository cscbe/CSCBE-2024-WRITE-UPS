extends AnimatedSprite2D

@export var idx: int

var dead = false

func _calculate_identifier(server_additional_hash: String):
	var ctx = HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	
	var v2arr = PackedVector2Array([
		global_position, $Area2D.global_position, $Area2D/CollisionShape2D.global_position,
		scale, $Area2D.scale, $Area2D/CollisionShape2D.scale])
	ctx.update(v2arr.to_byte_array())
	
	if server_additional_hash != null:
		ctx.update(server_additional_hash.to_utf8_buffer())
	
	
	# Get the computed hash.
	var res = ctx.finish()
	
	return res.hex_encode()

func _on_area_2d_body_shape_entered(body_rid, body, body_shape_index, local_shape_index):
	if body.is_in_group("player") and not dead:
		
		# Calculate the identifier of the monster to register the capture with the server
		var prev_id = ""
		if idx > 0:
			prev_id = $"/root/GlobalState".blob_server_ids[idx-1]
		var id = _calculate_identifier(prev_id)
		# print("Monster id: " + id)
		
		# Verify with the server
		$"/root/GlobalState".register_blob_captured(idx, id)
		
		dead = true
		get_node("/root/GlobalState").increase_point()
		print("Captured creature")
		$AnimationPlayer.play("die")
		$AudioStreamPlayer2D.play()
		$GPUParticles2D.restart()


var anim_done = false
var sound_done = false

func try_exit():
	if anim_done and sound_done:
		queue_free()

func _on_animation_player_animation_finished(anim_name):
	if anim_name == "die":
		anim_done = true
		try_exit()


func _on_audio_stream_player_2d_finished():
	sound_done = true
	try_exit()
