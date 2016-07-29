
var GG = (function() {
	var me = {};

	console.log("Welcome to Gainful");
	me.onCreateGroupClicked = function() {
		console.log("new group");
		var modal = document.getElementById("newGroupModal")
		if (modal.style.display == 'none') {
			modal.style.display = 'flex';
		} else {
			modal.style.display = 'none';
		}
	};

	me.onGroupClicked = function(groupId) {
		console.log("group", groupId);
	};
	
	me.onAddStudentClicked = function() {
		console.log("new group");
		var modal = document.getElementById("newStudentModal")
		if (modal.style.display == 'none') {
			modal.style.display = 'flex';
		} else {
			modal.style.display = 'none';
		}
	};

	me.dismissModal = function() {
		var modal = document.getElementsByClassName("c-modal-overlay")[0];
		modal.style.display = 'none';
	}


	return me;

})();


