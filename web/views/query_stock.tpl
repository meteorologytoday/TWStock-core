% rebase("bone.tpl")
<script type='text/javascript'>
	$(function(){
		var s = $('#stock_data')
		var f = $('#stock_form')
		var keys = ['time', 'o_p', 'h_p', 'l_p', 'c_p']
		f.submit(function(evt){
			evt.preventDefault()
			o = {
				'no': $('#no').val(),
				'beg_date': $('#beg_date').val(),
				'end_date': $('#end_date').val()
			}
			url = f.attr('action') + "?" + $.param(o)

			$.getJSON(url, function(data){
				s.empty()
				n = data['time'].length
				d = new Array(n)

				var key, tr, str
				for(var i = 0; i < n; ++i) {
					tr = $('<tr>')
					for(var j=0; j < keys.length; ++j) {
						key = keys[j]
						if(key == 'time') {
							str = new Date(parseInt(data[key][i])*1000).toISOString().substring(0, 10)
						} else {
							str = parseFloat(data[key][i]).toFixed(2)
						}
						tr.append($('<td>').text(str))
					}
					s.append(tr)
				}
			})
		})
	})

</script>
<h1>股票查詢</h1>
<form id="stock_form" method="POST" action="/query_stock/engine">
	<div class="form-group">
		<label for="no">股票代號</label>
		<input type="text" class="form-control" id="no" placeholder="請輸入股票代號">
	</div>

	<div class="form-group row">
		<label for="beg_date" class="col-2 col-form-label">起始日期</label>
		<div class='col-10'>
			<input class="form-control" type="date" value="2011-08-19" id="beg_date">
		</div>
	</div>

	<div class="form-group row">
		<label for="end_date" class="col-2 col-form-label">結尾日期</label>
		<div class="col-10">
			<input class="form-control" type="date" value="2011-08-19" id="end_date">
		</div>
	</div>
	<button type="submit" class="btn btn-primary">送出</button>
</form>
<hr />
<table class='table'>
	<thead>
		<tr>
			<th>日期</th>
			<th>開盤</th>
			<th>最高</th>
			<th>最低</th>
			<th>收盤</th>
		</tr>
	</thead>
	<tbody id='stock_data'>
	</tbody>
</table>
