% rebase("bone.tpl")
<script type='text/javascript'>
$(function(){
	$.getJSON('/status/downloading', updateStatus)
})

function updateStatus(o) {
	if('status' in o) {
		s = o['status']
		if (s == 'idle') {
			$('#download_status').text('閒置')
		} else if (s == 'busy') {
			$('#download_status').text('忙碌')
		} else {
			$('#download_status').text('未知: ' + s)
		}
	}
}
</script>
<h1>控制板</h1>
<div class="panel panel-default">
	<div class="panel-heading">股票抓取程式</div>
	<div class="panel-body">
	<p>...</p>
	</div>
	<ul class="list-group">
		<li class="list-group-item">下載狀態<span class="badge" id='download_status'></span></li>
	</ul>
</div>
