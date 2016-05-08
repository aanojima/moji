var ExerciseManager = function(){
	
	$("#character-group-select").select2({
		placeholder: "Select a character group"
	});

	$("#character-select").select2({
		placeholder: "Select a character"
	});

	$.ajax({
		method : "GET",
		url : window.MOJI_URL + "api/characters/blocks/",
		success : function(result){
			var blocks = result["blocks"]
			var blockOption = $("<option></option>").text("");
			$("#character-group-select").append(blockOption);
			for (var blockName in blocks){
				var blockCount = blocks[blockName];
				var blockDisplayName = blockName.replace(/_/g, " ");
				var blockOption = $("<option></option>").text(blockDisplayName).val(blockName);
				$("#character-group-select").append(blockOption);
			}
			$("#character-group-select").select2({
				placeholder: "Select a character group"
			});
		},
		error : function(error){
			console.log(error.responseText);
		}
	});

	$("#character-group-select").on("change", function(e){
		// Enable Character Select
		$("#character-select").prop("disabled", true);

		// Clear All Options from Character Select
		$("#character-select option").remove();

		// Get Unicode Block Name
		var unicodeBlock = $("#character-group-select").val();


		$.ajax({
			method : "GET",
			url : window.MOJI_URL + "api/characters/blocks?unicode_block=" + unicodeBlock,
			success : function(result){
				// todo
				var characters = result["characters"];
				var option = $("<option></option>").text("");
				$("#character-select").append(option);
				for (var i in characters){
					var character = characters[i];
					var characterDisplayName = String.fromCharCode(character["unicode-value"]);
					var characterValue = character["unicode-value"];
					var characterOption = $("<option></option>").text(characterDisplayName).val(characterValue);
					$("#character-select").append(characterOption);
				}
				$("#character-select").select2({
					placeholder: "Select a character"
				});
				$("#character-select").prop("disabled", false);
			},
			error : function(error){
				console.log(error.responseText);
			}
		});
	});
}