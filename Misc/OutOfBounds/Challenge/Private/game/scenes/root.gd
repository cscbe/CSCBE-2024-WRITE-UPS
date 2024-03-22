extends Node2D


# Called when the node enters the scene tree for the first time.
func _ready():
	print("Fading in root scene")
	$CanvasLayerSceneFade/AnimationPlayer.play("fade_in")


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
