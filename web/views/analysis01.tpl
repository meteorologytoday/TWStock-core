% rebase('bone.tpl')
<script type='text/javascript' src="/static/js/jquery-3.2.1.min.js"></script>
<script type='text/javascript' src="/static/js/jquery.csv.min.js"></script>
<script type='text/javascript'>

$(function(){
	$.get('/static/data/20170513.csv', function(data) {
		var tbody = $("<tbody>")
		var table = $("<table>").addClass("table")
		csv = $.csv.toArrays(data)
		console.log(csv)
		for(let row of csv) {

			var tr = $("<tr>")
			tr.append($("<td>").text(row[0]))
			tr.append($("<td>").text(row[1]))
			tr.append($("<td>").text(row[2]))
			tbody.append(tr)
		}	

		$('#root').append(table.append(tbody))
	})

})
</script>
<div id='root'>
</div>
