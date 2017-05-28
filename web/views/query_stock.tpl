% rebase("bone.tpl")

<h1>股票查詢</h1>
<form method="POST" action="/query_stock">

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
