function rate(id) {
	val = $("#rate" + id).val();
	$.ajax("http://localhost:8000/rate/" + id + "/" + val + "/");
	$("#rate" + id).prop("disabled", true);
	$("#num" + id).html(parseInt($("#num" + id).html()) + 1);
	return false;
}