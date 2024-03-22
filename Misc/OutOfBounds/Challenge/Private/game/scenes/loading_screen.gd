extends Control

var thread: Thread

var game_hash = null

func _ready():
	thread = Thread.new()
	# You can bind multiple arguments to a function Callable.
	thread.start(check_game_integrity)
	
# Thread must be disposed (or "joined"), for portability.
func _exit_tree():
	thread.wait_to_finish()
	
#func _start_game_integrity_check():
	#check_game_integrity()


var progress_per_delta = .01
var delta_sum = 0.0
func _process(delta):
	if thread.is_started():
		if thread.is_alive():
			delta_sum += delta
			if delta_sum > progress_per_delta:
				delta_sum = 0.0
				$CanvasLayer/ColorRect/CenterContainer/VBoxContainer/ProgressBar.value += 1
				
				if int($CanvasLayer/ColorRect/CenterContainer/VBoxContainer/ProgressBar.value) % 10 == 0:
					progress_per_delta *= 2
				
			# update progressbar
			pass
		else:
			thread.wait_to_finish()
			
			var networking = load("res://objects/networking/Networking.tscn").instantiate()
			add_child(networking)
			networking.send_game_hash(game_hash)
			
			$CanvasLayer/ColorRect/CenterContainer/VBoxContainer/ProgressBar.value = 100
			
			$AudioStreamPlayer.play()
			$CanvasLayer2/AnimationPlayer.play("fade_out")



const CHUNK_SIZE = 1024

func create_custom_session(player_id: int):
	var random_seed = str(randi())
	var player_string: String = str(player_id) + random_seed
	var context = HashingContext.new()
	context.start(HashingContext.HASH_SHA256)
	context.update(player_string.to_utf8_buffer())
	var session_token = context.finish().hex_encode()
	
	# Store 'session_token' to validate subsequent requests or actions.
	return session_token

func get_all_dir_files_recursively(path, file_list):
	var dir = DirAccess.open(path)
	if dir:
		dir.list_dir_begin()
		var file_name = dir.get_next()
		while file_name != "":
			if dir.current_is_dir():
				#print("Found directory: " + path + '/' + file_name)
				get_all_dir_files_recursively(path + '/' + file_name, file_list)
			else:
				file_list.append(path + '/' + file_name)
				#print("Found file: " + path + '/' + file_name)
			file_name = dir.get_next()
	else:
		print('')
		print("An error occurred when trying to access the path.")


func check_game_integrity():
	var files = []
	get_all_dir_files_recursively("res://", files)
	var hash = hash_files(files)
	
	game_hash = hash_executable()
	
	
func hash_executable():
	var ctx = HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	
	var file = FileAccess.open(OS.get_executable_path(), FileAccess.READ)
	while not file.eof_reached():
			ctx.update(file.get_buffer(CHUNK_SIZE))
	var res = ctx.finish()
	return res.hex_encode()

func hash_files(files):
	# Start a SHA-256 context.
	var ctx = HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	
	for path in files:
		# Check that file exists.
		if not FileAccess.file_exists(path):
			continue
			
		if not (path.ends_with('.gd') 
			#or path.ends_with('.tscn') 
			#or path.ends_with('.import') 
			#or path.ends_with('.tres') 
			or path.ends_with('.gdshader')
		):
			continue
	
		# Open the file to hash.
		var file = FileAccess.open(path, FileAccess.READ)
		# Update the context after reading each chunk.
		while not file.eof_reached():
			ctx.update(file.get_buffer(CHUNK_SIZE))
			
	# Get the computed hash.
	var res = ctx.finish()
	# Print the result as hex string and array.
	#printt(res.hex_encode(), Array(res))
	
	return res.hex_encode()
	

func hash_file(path):
	# Check that file exists.
	if not FileAccess.file_exists(path):
		return
	# Start a SHA-256 context.
	var ctx = HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	# Open the file to hash.
	var file = FileAccess.open(path, FileAccess.READ)
	# Update the context after reading each chunk.
	while not file.eof_reached():
		ctx.update(file.get_buffer(CHUNK_SIZE))
	# Get the computed hash.
	var res = ctx.finish()
	# Print the result as hex string and array.
	#printt(res.hex_encode(), Array(res))


func _on_animation_player_animation_finished(anim_name):
	if anim_name == "fade_out":
		$"/root/GlobalState".change_to_root()
