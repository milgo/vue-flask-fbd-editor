extends VBoxContainer

func _on_logic_variable_value_changed(memAddr: String, _oldval: Variant, newval: Variant) -> void:
	var newvalf = float(newval)
	for n in find_children("*", "TextureButton", true, false):
		if n.get_meta_list().has("DO"):
			if memAddr.to_lower() == n.get_meta("DO"):
				if newvalf == 1.0:
					n.modulate = Color.LIME
				if newvalf == 0.0:
					n.modulate = Color.WHITE
