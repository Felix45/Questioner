
function menuDrawer(){
	var userMenu = document.getElementById('mobile-menu');
	if(userMenu.style.display){
			userMenu.style.display = 'none';
	}else{
			userMenu.style.display = 'block';
	}
}

function displayModal(){
	var modal = document.getElementById('modal');
	console.log(modal.style.display);
	if(modal.style.display == 'none' || modal.style.display == '' ){
			modal.style.display = 'block';
	}else{
			modal.style.display = 'none';
	}
}