extends Node

var points = 0
func increase_point():
	points += 1
	
var session_id = ""
	
var blob_server_ids = [
	"",
	"",
	""
]
var next_message = 0
var blob_messages = [
	"",
	"",
	"",
	""
]

func register_blob_captured(idx, hash):
	var networking = load("res://objects/networking/Networking.tscn").instantiate()
	add_child(networking)
	networking.send_blob_capture(idx, hash)


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

var next_scene = preload("res://scenes/root.tscn")
func change_to_root():
	print("changing to root scene")
	get_tree().change_scene_to_packed(next_scene)
